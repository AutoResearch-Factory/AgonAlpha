#!/usr/bin/env python3
"""Shared BRAIN client for simulation, submission checks, and submission.

The ``simulate`` command accepts either a JSON list or an object containing a
``candidates`` list. Every candidate must contain ``name``, ``settings``, and
either ``regular`` or ``expression``. ``name`` is also its artifact-directory
name and must be ``{CANDIDATE_ID}-{LOOP_ID}-{SLUG}``.

The ``check`` command waits for non-empty submission checks. The ``submit``
command preserves those checks, accepts the empty HTTP 201 response, and
verifies the final Alpha state.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import math
import os
import re
import sys
import time
import uuid
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV = PROJECT_ROOT / "alphas" / ".env"
DEFAULT_SIMULATION_REGISTRY = PROJECT_ROOT / "alphas" / ".brain-simulations.json"
DEFAULT_BASE_URL = "https://api.worldquantbrain.com"
MAX_CONCURRENT_SIMULATIONS = 3
DEFAULT_MAX_ACTIVE = MAX_CONCURRENT_SIMULATIONS
SIMULATION_LEASE_TIMEOUT_SECONDS = 60.0 * 60.0
SIMULATION_SLOT_RETRY_SECONDS = 1.0
DEFAULT_POLL_INTERVAL = 30.0
SAFE_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
KEBAB_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ARTIFACTS_SUBDIR = "brain"
SUMMARY_FILENAME = "brain_summary.json"


class BrainAPIError(RuntimeError):
    """An unexpected HTTP response from BRAIN."""

    def __init__(self, method: str, url: str, response: APIResponse):
        super().__init__(
            f"{method} {url} returned HTTP {response.status_code}: "
            f"{str(response.body)[:1000]}"
        )
        self.method = method
        self.url = url
        self.response = response


class BrainProtocolError(RuntimeError):
    """A successful response that violates an expected BRAIN invariant."""


class AlphaReuseError(RuntimeError):
    """A simulation resolved to an existing Alpha that must not be renamed."""


class BatchTimeout(TimeoutError):
    """The internal deadline expired; rerunning resumes the saved batch."""


class SimulationRegistry:
    """Cross-process registry for account-wide active BRAIN simulations."""

    def __init__(
        self,
        path: Path = DEFAULT_SIMULATION_REGISTRY,
        *,
        wall_time: Callable[[], float] = time.time,
    ) -> None:
        self.path = path
        self._wall_time = wall_time

    @contextmanager
    def _locked_simulations(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
        with os.fdopen(descriptor, "r+", encoding="utf-8") as registry_file:
            fcntl.flock(registry_file.fileno(), fcntl.LOCK_EX)
            try:
                registry_file.seek(0)
                source = registry_file.read().strip()
                state = json.loads(source) if source else {"simulations": {}}
                simulations = (
                    state.get("simulations") if isinstance(state, dict) else None
                )
                if not isinstance(simulations, dict):
                    raise ValueError(f"Invalid simulation registry: {self.path}")

                now = self._wall_time()
                for lease_id, entry in list(simulations.items()):
                    started_at = (
                        entry.get("started_at") if isinstance(entry, dict) else None
                    )
                    if not isinstance(started_at, (int, float)):
                        raise ValueError(
                            f"Invalid simulation lease {lease_id!r}: {self.path}"
                        )
                    if now - float(started_at) >= SIMULATION_LEASE_TIMEOUT_SECONDS:
                        del simulations[lease_id]

                yield simulations

                registry_file.seek(0)
                json.dump(
                    {"simulations": simulations},
                    registry_file,
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=False,
                )
                registry_file.write("\n")
                registry_file.truncate()
                registry_file.flush()
                os.fsync(registry_file.fileno())
            finally:
                fcntl.flock(registry_file.fileno(), fcntl.LOCK_UN)

    def try_acquire(
        self,
        *,
        candidate: str,
        workdir: Path,
        location: str | None = None,
    ) -> str | None:
        with self._locked_simulations() as simulations:
            if len(simulations) >= MAX_CONCURRENT_SIMULATIONS:
                return None
            lease_id = uuid.uuid4().hex
            simulations[lease_id] = {
                "candidate": candidate,
                "workdir": str(workdir.resolve()),
                "location": location,
                "started_at": self._wall_time(),
            }
            return lease_id

    def update_location(self, lease_id: str, location: str) -> bool:
        with self._locked_simulations() as simulations:
            entry = simulations.get(lease_id)
            if not isinstance(entry, dict):
                return False
            entry["location"] = location
            return True

    def release(self, lease_id: str | None) -> bool:
        if lease_id is None:
            return False
        with self._locked_simulations() as simulations:
            return simulations.pop(lease_id, None) is not None

    def reset(self) -> None:
        with self._locked_simulations() as simulations:
            simulations.clear()

    def snapshot(self) -> dict[str, dict[str, Any]]:
        with self._locked_simulations() as simulations:
            return {lease_id: dict(entry) for lease_id, entry in simulations.items()}


@dataclass(frozen=True)
class APIResponse:
    status_code: int
    headers: dict[str, str]
    body: Any

    @classmethod
    def from_requests(cls, response: requests.Response) -> APIResponse:
        try:
            body: Any = response.json()
        except requests.exceptions.JSONDecodeError:
            body = response.text
        return cls(
            response.status_code,
            {str(key): str(value) for key, value in response.headers.items()},
            body,
        )

    def header(self, name: str) -> str | None:
        target = name.casefold()
        return next(
            (value for key, value in self.headers.items() if key.casefold() == target),
            None,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "status_code": self.status_code,
            "headers": self.headers,
            "body": self.body,
        }


@dataclass
class ActiveSimulation:
    candidate: dict[str, Any]
    directory: Path
    location: str
    requested_at: float
    lease_id: str | None
    next_poll: float = 0.0


def load_env(path: Path = DEFAULT_ENV) -> dict[str, str]:
    """Read BRAIN credentials without exposing them in artifacts."""
    values: dict[str, str] = {}
    for line_number, source in enumerate(
        path.read_text(encoding="utf-8-sig").splitlines(), 1
    ):
        line = source.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").strip()
        key, separator, value = line.partition("=")
        if not separator:
            raise ValueError(f"Malformed dotenv line {line_number} in {path}")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key.strip()] = value
    missing = [key for key in ("BRAIN_EMAIL", "BRAIN_PASSWORD") if not values.get(key)]
    if missing:
        raise ValueError(f"Missing {', '.join(missing)} in {path}")
    return values


def write_json(path: Path, value: Any) -> None:
    """Atomically write JSON so interrupted runs do not leave partial files."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def write_rotated_json(path: Path, value: Any) -> None:
    """Write the latest JSON at ``path`` and retain every previous version."""
    if path.exists():
        prefix = f"{path.stem}."
        suffix = path.suffix
        archives: list[tuple[int, Path]] = []
        for candidate in path.parent.glob(f"{path.stem}.*{suffix}"):
            version = candidate.name[len(prefix) : -len(suffix)]
            if version.isdecimal() and not version.startswith("0"):
                archives.append((int(version), candidate))
        for version, candidate in sorted(archives, reverse=True):
            candidate.replace(
                path.with_name(f"{path.stem}.{version + 1}{path.suffix}")
            )
        path.replace(path.with_name(f"{path.stem}.1{path.suffix}"))
    write_json(path, value)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _candidate_dir(run_dir: Path, key: str) -> Path:
    return run_dir / ARTIFACTS_SUBDIR / key


def retry_after_seconds(
    headers: Mapping[str, str],
    default: float,
    *,
    now: float | None = None,
) -> float:
    """Parse Retry-After as seconds or an HTTP date."""
    raw = next(
        (value for key, value in headers.items() if key.casefold() == "retry-after"),
        None,
    )
    if raw is None:
        return default
    try:
        return max(float(raw), 0.0)
    except ValueError:
        try:
            target = parsedate_to_datetime(raw)
        except (TypeError, ValueError, OverflowError):
            return default
        if target.tzinfo is None:
            target = target.replace(tzinfo=timezone.utc)
        current = time.time() if now is None else now
        return max(target.timestamp() - current, 0.0)


def _parse_datetime(value: Any) -> float | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def _checks_resolved(checks: list[dict[str, Any]]) -> bool:
    """True when every check has reached a terminal state.

    BRAIN leaves dependent checks PENDING when a prerequisite fails, so a mix
    of FAIL and PENDING is also considered resolved.
    """
    if not checks:
        return False
    has_failure = False
    has_pending = False
    for check in checks:
        result = check.get("result") if isinstance(check, dict) else None
        if result == "PENDING":
            has_pending = True
        elif result == "FAIL":
            has_failure = True
    return has_failure or not has_pending


class BrainClient:
    """Cookie-backed API session with network retry and reauthentication."""

    def __init__(
        self,
        env_path: Path = DEFAULT_ENV,
        *,
        base_url: str | None = None,
        timeout_seconds: float = 60.0,
        max_retries: int = 6,
        session: requests.Session | None = None,
        sleep: Callable[[float], None] = time.sleep,
        monotonic: Callable[[], float] = time.monotonic,
        wall_time: Callable[[], float] = time.time,
    ) -> None:
        env = load_env(env_path)
        configured_url = (
            base_url
            or env.get("BRAIN_API_BASE_URL")
            or env.get("BRAIN_API_URL")
            or env.get("WORLDQUANT_API_URL")
            or DEFAULT_BASE_URL
        )
        self.base_url = configured_url.rstrip("/") + "/"
        self.email = env["BRAIN_EMAIL"]
        self.password = env["BRAIN_PASSWORD"]
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.session = session or requests.Session()
        self._sleep = sleep
        self._monotonic = monotonic
        self._wall_time = wall_time
        self.authenticated = False

    def url(self, path_or_url: str) -> str:
        if path_or_url.startswith(("http://", "https://")):
            return path_or_url
        return urljoin(self.base_url, path_or_url.lstrip("/"))

    def authenticate(self) -> APIResponse:
        target = self.url("authentication")
        for attempt in range(self.max_retries + 1):
            try:
                raw = self.session.post(
                    target,
                    auth=HTTPBasicAuth(self.email, self.password),
                    timeout=self.timeout_seconds,
                )
            except requests.RequestException:
                if attempt == self.max_retries:
                    raise
                self._sleep(min(2**attempt, 30.0))
                continue
            response = APIResponse.from_requests(raw)
            if response.status_code == 201:
                self.authenticated = True
                return response
            raise BrainAPIError("POST", target, response)
        raise AssertionError("authentication loop ended unexpectedly")

    def request(
        self,
        method: str,
        path_or_url: str,
        *,
        expected: Iterable[int] = (200,),
        **kwargs: Any,
    ) -> APIResponse:
        if not self.authenticated:
            self.authenticate()
        target = self.url(path_or_url)
        allowed = set(expected)
        reauthenticated = False
        for attempt in range(self.max_retries + 1):
            try:
                raw = self.session.request(
                    method,
                    target,
                    timeout=self.timeout_seconds,
                    **kwargs,
                )
            except requests.RequestException:
                if attempt == self.max_retries:
                    raise
                self._sleep(min(2**attempt, 30.0))
                continue
            response = APIResponse.from_requests(raw)
            if response.status_code in allowed:
                return response
            if response.status_code == 401 and not reauthenticated:
                self.authenticated = False
                self.authenticate()
                reauthenticated = True
                continue
            raise BrainAPIError(method, target, response)
        raise AssertionError("request loop ended unexpectedly")

    def create_simulation(self, payload: dict[str, Any]) -> tuple[str, APIResponse]:
        response = self.request("POST", "simulations", expected=(201,), json=payload)
        location = response.header("Location")
        if not location:
            raise BrainProtocolError("Simulation response omitted Location")
        return location, response

    def simulation_status(self, location: str) -> APIResponse:
        return self.request("GET", location)

    def alpha(self, alpha_id: str) -> dict[str, Any]:
        body = self.request("GET", f"alphas/{alpha_id}").body
        if not isinstance(body, dict):
            raise BrainProtocolError(f"Alpha {alpha_id} response is not an object")
        return body

    def set_alpha_name(self, alpha_id: str, name: str) -> APIResponse:
        return self.request("PATCH", f"alphas/{alpha_id}", json={"name": name})

    def submission_checks(
        self,
        alpha_id: str,
        *,
        max_wait: float = 300.0,
        poll_interval: float = 5.0,
    ) -> dict[str, Any]:
        """Wait for submission checks to reach terminal states."""
        if not math.isfinite(max_wait) or max_wait <= 0:
            raise ValueError("max_wait must be positive and finite")
        started = self._monotonic()
        while True:
            response = self.request("GET", f"alphas/{alpha_id}/check")
            body = response.body
            if isinstance(body, dict):
                in_sample = body.get("is")
                checks = (
                    in_sample.get("checks") if isinstance(in_sample, dict) else None
                )
                if not isinstance(checks, list):
                    raise BrainProtocolError(
                        f"Submission checks for {alpha_id} omitted is.checks"
                    )
                if _checks_resolved(checks):
                    return body
            elif body is not None and not (isinstance(body, str) and not body.strip()):
                raise BrainProtocolError(
                    f"Submission checks for {alpha_id} are invalid"
                )
            elapsed = self._monotonic() - started
            if elapsed >= max_wait:
                raise BatchTimeout(f"Submission checks for {alpha_id} timed out")
            delay = retry_after_seconds(response.headers, poll_interval)
            self._sleep(min(max(delay, 0.25), max_wait - elapsed))

    def submit_alpha(
        self,
        alpha_id: str,
        *,
        max_wait: float = 300.0,
        poll_interval: float = 5.0,
    ) -> dict[str, Any]:
        """Preserve submission checks, submit, and verify the ACTIVE/OS state."""
        if not math.isfinite(max_wait) or max_wait <= 0:
            raise ValueError("max_wait must be positive and finite")
        pre_submission_check = self.submission_checks(
            alpha_id,
            max_wait=max_wait,
            poll_interval=poll_interval,
        )
        before = self.alpha(alpha_id)
        expected_name = before.get("name")
        submission = self.request("POST", f"alphas/{alpha_id}/submit", expected=(201,))
        started = self._monotonic()
        delay = retry_after_seconds(submission.headers, poll_interval)
        if delay > 0:
            self._sleep(min(delay, max_wait))

        while True:
            detail = self.alpha(alpha_id)
            if detail.get("name") != expected_name:
                raise BrainProtocolError(
                    f"Alpha {alpha_id} name changed during submission"
                )
            if detail.get("status") == "ACTIVE" and detail.get("stage") == "OS":
                return {
                    "pre_submission_check": pre_submission_check,
                    "submission": submission.as_dict(),
                    "alpha": detail,
                }
            elapsed = self._monotonic() - started
            if elapsed >= max_wait:
                raise BatchTimeout(f"Submission for {alpha_id} timed out")
            self._sleep(min(poll_interval, max_wait - elapsed))


def _normalized_candidate(source: Mapping[str, Any]) -> dict[str, Any]:
    expression = source.get("regular", source.get("expression"))
    unsupported = [field for field in ("slug", "id") if field in source]
    if unsupported:
        raise ValueError(
            f"Candidate must use name instead of {' and '.join(unsupported)}"
        )
    name = source.get("name")
    settings = source.get("settings")
    if not isinstance(name, str) or not SAFE_KEY.fullmatch(name):
        raise ValueError(f"Candidate has an unsafe name: {name!r}")
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError(f"Candidate {name} has no expression")
    if not isinstance(settings, dict):
        raise ValueError(f"Candidate {name} settings are not an object")
    return {
        "key": name,
        "name": name,
        "type": source.get("type", "REGULAR"),
        "regular": expression,
        "settings": settings,
    }


def _payload(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "type": candidate["type"],
        "settings": candidate["settings"],
        "regular": candidate["regular"],
    }


def load_candidates(path: Path) -> list[dict[str, Any]]:
    document = read_json(path)
    rows = document.get("candidates") if isinstance(document, dict) else document
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{path} contains no candidates")
    candidates = [_normalized_candidate(row) for row in rows]
    names = [candidate["name"] for candidate in candidates]
    payloads = [
        json.dumps(_payload(candidate), sort_keys=True, separators=(",", ":"))
        for candidate in candidates
    ]
    for label, values in (("name", names), ("payload", payloads)):
        duplicates = [value for value, count in Counter(values).items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate candidate {label}: {duplicates[0]}")
    return candidates


def validate_candidate_names(
    candidates: Iterable[Mapping[str, Any]], candidate_id: str
) -> None:
    """Require the documented BRAIN name format for this candidate workdir."""
    if not SAFE_KEY.fullmatch(candidate_id):
        raise ValueError(f"Candidate workdir name is unsafe: {candidate_id!r}")
    prefix = f"{candidate_id}-"
    for candidate in candidates:
        name = candidate.get("name")
        if not isinstance(name, str) or not name.startswith(prefix):
            raise ValueError(f"Candidate name must start with {prefix!r}: {name!r}")
        loop_id, separator, slug = name[len(prefix) :].partition("-")
        if (
            not separator
            or not loop_id.isdecimal()
            or int(loop_id) < 1
            or not KEBAB_SLUG.fullmatch(slug)
        ):
            raise ValueError(
                "Candidate name must use "
                "{CANDIDATE_ID}-{LOOP_ID}-{SLUG}: "
                f"{name!r}"
            )


def run_dir_for_current_workdir(run_dir: Path, *, cwd: Path | None = None) -> Path:
    """Require the CLI artifact directory to be its execution directory."""
    selected = run_dir.resolve()
    current = (Path.cwd() if cwd is None else cwd).resolve()
    if selected != current:
        raise ValueError(
            f"--run-dir must be the current working directory: {current}; got {selected}"
        )
    return selected


def _settings_match(requested: Mapping[str, Any], actual: Mapping[str, Any]) -> bool:
    return all(actual.get(key) == value for key, value in requested.items())


def _complete_candidate(
    client: BrainClient,
    active: ActiveSimulation,
    alpha_id: str,
    claimed: dict[str, str],
) -> dict[str, Any]:
    candidate = active.candidate
    detail = client.alpha(alpha_id)
    # Retain one raw Alpha snapshot for troubleshooting or future API changes.
    # On success it is replaced with the final, named Alpha; on validation
    # failure it preserves the response that caused the rejection.
    write_json(active.directory / "alpha.json", detail)
    if detail.get("id") != alpha_id:
        raise BrainProtocolError(f"Alpha response returned {detail.get('id')!r}")
    previous_key = claimed.get(alpha_id)
    if previous_key is not None and previous_key != candidate["key"]:
        raise AlphaReuseError(f"Alpha {alpha_id} is already claimed by {previous_key}")
    regular = detail.get("regular")
    if not isinstance(regular, dict) or regular.get("code") != candidate["regular"]:
        raise AlphaReuseError(f"Alpha {alpha_id} expression does not match")
    actual_settings = detail.get("settings")
    if not isinstance(actual_settings, dict) or not _settings_match(
        candidate["settings"], actual_settings
    ):
        raise AlphaReuseError(f"Alpha {alpha_id} settings do not match")

    current_name = detail.get("name")
    created_at = _parse_datetime(detail.get("dateCreated"))
    if current_name != candidate["name"]:
        if created_at is None:
            raise AlphaReuseError(
                f"Alpha {alpha_id} has no valid dateCreated; refusing to rename it"
            )
        if created_at < active.requested_at - 60.0:
            raise AlphaReuseError(
                f"Alpha {alpha_id} predates this simulation and will not be renamed"
            )
    if current_name not in {None, "", candidate["name"]}:
        raise AlphaReuseError(f"Alpha {alpha_id} is already named {current_name!r}")
    if current_name != candidate["name"]:
        client.set_alpha_name(alpha_id, candidate["name"])

    try:
        final = client.alpha(alpha_id)
    except (BrainAPIError, requests.RequestException):
        final = {**detail, "name": candidate["name"]}
    if final.get("name") != candidate["name"]:
        raise BrainProtocolError(f"Alpha {alpha_id} name was not applied")
    write_json(active.directory / "alpha.json", final)
    result = {
        "candidate": candidate,
        "alpha_id": alpha_id,
        "name": final["name"],
        "regular": final.get("regular"),
        "settings_actual": final.get("settings"),
        "is": final.get("is"),
        "status": final.get("status"),
        "stage": final.get("stage"),
        "simulation_location": active.location,
        "requested_at": active.requested_at,
    }
    write_json(active.directory / "result.json", result)
    (active.directory / "creation.json").unlink(missing_ok=True)
    claimed[alpha_id] = candidate["key"]
    return result


def _summary(
    candidates: list[dict[str, Any]],
    results: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    pending: list[tuple[dict[str, Any], Path]],
    active: Mapping[str, ActiveSimulation],
) -> dict[str, Any]:
    return {
        "candidate_count": len(candidates),
        "completed_count": len(results),
        "failure_count": len(failures),
        "pending": [candidate["key"] for candidate, _ in pending],
        "active": sorted(active),
        "results": results,
        "failures": failures,
    }


def _is_concurrency_limit_error(error: Exception) -> bool:
    if not isinstance(error, BrainAPIError) or error.response.status_code != 429:
        return False
    body = error.response.body
    return isinstance(body, dict) and body.get("detail") == "CONCURRENT_SIMULATION_LIMIT_EXCEEDED"


def _release_active_lease(
    registry: SimulationRegistry, active: ActiveSimulation
) -> None:
    if active.lease_id is None:
        return
    creation_path = active.directory / "creation.json"
    if creation_path.exists():
        creation = read_json(creation_path)
        creation["global_count_active"] = False
        write_json(creation_path, creation)
    registry.release(active.lease_id)
    active.lease_id = None


def simulate_candidates(
    client: BrainClient,
    candidates: list[dict[str, Any]],
    run_dir: Path,
    *,
    max_active: int = DEFAULT_MAX_ACTIVE,
    max_runtime: float = 540.0,
    registry: SimulationRegistry | None = None,
) -> dict[str, Any]:
    """Run server-side simulations concurrently and persist resumable artifacts."""
    if max_active < 1:
        raise ValueError("max_active must be positive")
    if not math.isfinite(max_runtime) or max_runtime <= 0:
        raise ValueError("max_runtime must be positive and finite")
    registry = registry or SimulationRegistry()
    run_dir.mkdir(parents=True, exist_ok=True)
    pending: list[tuple[dict[str, Any], Path]] = []
    active: dict[str, ActiveSimulation] = {}
    results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    claimed: dict[str, str] = {}

    for candidate in candidates:
        directory = _candidate_dir(run_dir, candidate["key"])
        directory.mkdir(parents=True, exist_ok=True)
        candidate_path = directory / "candidate.json"
        if candidate_path.exists() and read_json(candidate_path) != candidate:
            raise ValueError(f"Saved candidate differs from input: {candidate['key']}")
        write_json(candidate_path, candidate)
        if (directory / "result.json").exists():
            result = read_json(directory / "result.json")
            alpha_id = result.get("alpha_id")
            if not isinstance(alpha_id, str):
                raise ValueError(f"Saved result has no Alpha ID: {directory}")
            if alpha_id in claimed:
                raise AlphaReuseError(f"Saved Alpha {alpha_id} is duplicated")
            claimed[alpha_id] = candidate["key"]
            results.append(result)
        elif (directory / "error.json").exists():
            failures.append(
                {"key": candidate["key"], "error": read_json(directory / "error.json")}
            )
        elif (directory / "creation.json").exists():
            creation = read_json(directory / "creation.json")
            lease_id = creation.get("lease_id")
            if not creation.get("global_count_active"):
                registry.release(lease_id if isinstance(lease_id, str) else None)
                lease_id = None
            elif not isinstance(lease_id, str):
                lease_id = None
            location = creation.get("location")
            requested_at = creation.get("requested_at")
            if not isinstance(location, str) or not isinstance(
                requested_at, (int, float)
            ):
                raise ValueError(
                    f"Corrupt creation.json for {candidate['key']}: {directory}"
                )
            active[candidate["key"]] = ActiveSimulation(
                candidate,
                directory,
                location,
                float(requested_at),
                lease_id,
            )
        else:
            pending.append((candidate, directory))

    started = client._monotonic()
    while pending or active:
        if client._monotonic() - started >= max_runtime:
            write_rotated_json(
                run_dir / SUMMARY_FILENAME,
                _summary(candidates, results, failures, pending, active),
            )
            raise BatchTimeout("Batch deadline reached; rerun the command to resume")

        while pending and len(active) < max_active:
            candidate, directory = pending[0]
            lease_id = registry.try_acquire(
                candidate=candidate["key"], workdir=directory
            )
            if lease_id is None:
                break
            pending.pop(0)
            requested_at = client._wall_time()
            try:
                location, _response = client.create_simulation(_payload(candidate))
            except (BrainAPIError, requests.RequestException) as error:
                registry.release(lease_id)
                if _is_concurrency_limit_error(error):
                    pending.insert(0, (candidate, directory))
                    delay = retry_after_seconds(
                        error.response.headers,
                        SIMULATION_SLOT_RETRY_SECONDS,
                        now=client._wall_time(),
                    )
                    client._sleep(max(delay, SIMULATION_SLOT_RETRY_SECONDS))
                    break
                failure = {"phase": "create", "message": str(error)}
                write_json(directory / "error.json", failure)
                failures.append({"key": candidate["key"], "error": failure})
                continue
            if not registry.update_location(lease_id, location):
                raise BrainProtocolError(
                    f"Simulation lease expired before creation completed: {lease_id}"
                )
            write_json(
                directory / "creation.json",
                {
                    "location": location,
                    "requested_at": requested_at,
                    "lease_id": lease_id,
                    "global_count_active": True,
                },
            )
            active[candidate["key"]] = ActiveSimulation(
                candidate, directory, location, requested_at, lease_id
            )

        now = client._monotonic()
        made_request = False
        for key, item in list(active.items()):
            if item.next_poll > now:
                continue
            made_request = True
            try:
                response = client.simulation_status(item.location)
                body = response.body
                if not isinstance(body, dict):
                    raise BrainProtocolError(f"Simulation status for {key} is invalid")
                if body.get("status") == "ERROR" or body.get("error"):
                    _release_active_lease(registry, item)
                    raise BrainProtocolError(f"Simulation {key} failed: {body}")
                alpha_id = body.get("alpha")
                if isinstance(alpha_id, str):
                    _release_active_lease(registry, item)
                    results.append(_complete_candidate(client, item, alpha_id, claimed))
                    del active[key]
                    continue
                delay = retry_after_seconds(
                    response.headers, DEFAULT_POLL_INTERVAL, now=client._wall_time()
                )
                item.next_poll = now + max(delay, DEFAULT_POLL_INTERVAL)
            except (
                AlphaReuseError,
                BrainAPIError,
                BrainProtocolError,
                requests.RequestException,
            ) as error:
                failure = {"phase": "poll-or-finish", "message": str(error)}
                write_json(item.directory / "error.json", failure)
                failures.append({"key": key, "error": failure})
                del active[key]

        if active and not made_request:
            next_poll = min(item.next_poll for item in active.values())
            client._sleep(max(min(next_poll - client._monotonic(), 10.0), 0.25))
        elif pending and not active and not made_request:
            client._sleep(SIMULATION_SLOT_RETRY_SECONDS)

    summary = _summary(candidates, results, failures, pending, active)
    write_rotated_json(run_dir / SUMMARY_FILENAME, summary)
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV)
    subparsers = parser.add_subparsers(dest="command", required=True)
    simulate = subparsers.add_parser("simulate")
    simulate.add_argument("candidates", type=Path)
    simulate.add_argument("--run-dir", type=Path, required=True)
    simulate.add_argument("--max-active", type=int, default=DEFAULT_MAX_ACTIVE)
    simulate.add_argument("--max-runtime", type=float, default=540.0)
    check = subparsers.add_parser("check")
    check.add_argument("alpha_id")
    check.add_argument("--max-wait", type=float, default=1800.0)
    submit = subparsers.add_parser("submit")
    submit.add_argument("alpha_id")
    submit.add_argument("--run-dir", type=Path, required=True)
    submit.add_argument("--max-wait", type=float, default=1800.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = BrainClient(args.env)
    if args.command == "check":
        result = client.submission_checks(args.alpha_id, max_wait=args.max_wait)
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
        checks = result.get("is", {}).get("checks", [])
        if any(
            isinstance(c, dict) and c.get("result") != "PASS" for c in checks
        ):
            raise SystemExit(1)
        return
    if args.command == "submit":
        try:
            run_dir = run_dir_for_current_workdir(args.run_dir)
        except ValueError as error:
            raise SystemExit(str(error)) from error
        result = client.submit_alpha(args.alpha_id, max_wait=args.max_wait)
        output = run_dir / "brain_submitted.json"
        write_rotated_json(output, result)
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
        print(f"Saved to {output}", file=sys.stderr)
        return

    try:
        run_dir = run_dir_for_current_workdir(args.run_dir)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    candidates = load_candidates(args.candidates)
    try:
        validate_candidate_names(candidates, run_dir.name)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    result = simulate_candidates(
        client,
        candidates,
        run_dir,
        max_active=args.max_active,
        max_runtime=args.max_runtime,
    )
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    if result["failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
