#!/usr/bin/env python3
"""Shared BRAIN client for resumable, parallel Alpha simulation.

The ``simulate`` command accepts either a JSON list or an object containing a
``candidates`` list. Every candidate must contain ``name``, ``settings``, and
either ``regular`` or ``expression``. ``name`` is also its artifact-directory
name and must be ``{CANDIDATE_ID}-{LOOP_ID}-{SLUG}``.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import time
from collections import Counter
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
DEFAULT_BASE_URL = "https://api.worldquantbrain.com"
DEFAULT_MAX_ACTIVE = 4
DEFAULT_POLL_INTERVAL = 30.0
SAFE_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
KEBAB_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


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
    next_poll: float = 0.0


def load_env(path: Path = DEFAULT_ENV) -> dict[str, str]:
    """Read BRAIN credentials without exposing them in artifacts."""
    values: dict[str, str] = {}
    for line_number, source in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
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
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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


def _normalized_candidate(source: Mapping[str, Any]) -> dict[str, Any]:
    expression = source.get("regular", source.get("expression"))
    unsupported = [field for field in ("slug", "id") if field in source]
    if unsupported:
        raise ValueError(
            f"Candidate must use name instead of {' and '.join(unsupported)}"
        )
    name = source.get("name")
    key = name
    settings = source.get("settings")
    if not isinstance(key, str) or not SAFE_KEY.fullmatch(key):
        raise ValueError(f"Candidate has an unsafe name: {key!r}")
    if not isinstance(name, str) or not name:
        raise ValueError(f"Candidate {key} has no name")
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError(f"Candidate {key} has no expression")
    if not isinstance(settings, dict):
        raise ValueError(f"Candidate {key} settings are not an object")
    return {
        "key": key,
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


def validate_candidate_names(candidates: Iterable[Mapping[str, Any]], candidate_id: str) -> None:
    """Require the documented BRAIN name format for this candidate workdir."""
    if not SAFE_KEY.fullmatch(candidate_id):
        raise ValueError(f"Candidate workdir name is unsafe: {candidate_id!r}")
    prefix = f"{candidate_id}-"
    for candidate in candidates:
        name = candidate.get("name")
        if not isinstance(name, str) or not name.startswith(prefix):
            raise ValueError(
                f"Candidate name must start with {prefix!r}: {name!r}"
            )
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
    write_json(active.directory / "alpha-before-name.json", detail)
    if detail.get("id") != alpha_id:
        raise BrainProtocolError(f"Alpha response returned {detail.get('id')!r}")
    previous_key = claimed.get(alpha_id)
    if previous_key is not None and previous_key != candidate["key"]:
        raise AlphaReuseError(f"Alpha {alpha_id} is already claimed by {previous_key}")
    if detail.get("regular", {}).get("code") != candidate["regular"]:
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
        response = client.set_alpha_name(alpha_id, candidate["name"])
        write_json(active.directory / "name-response.json", response.as_dict())

    final = client.alpha(alpha_id)
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
    }
    write_json(active.directory / "result.json", result)
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


def simulate_candidates(
    client: BrainClient,
    candidates: list[dict[str, Any]],
    run_dir: Path,
    *,
    max_active: int = DEFAULT_MAX_ACTIVE,
    max_runtime: float = 540.0,
) -> dict[str, Any]:
    """Run server-side simulations concurrently and persist resumable artifacts."""
    if max_active < 1:
        raise ValueError("max_active must be positive")
    if not math.isfinite(max_runtime) or max_runtime <= 0:
        raise ValueError("max_runtime must be positive and finite")
    run_dir.mkdir(parents=True, exist_ok=True)
    pending: list[tuple[dict[str, Any], Path]] = []
    active: dict[str, ActiveSimulation] = {}
    results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    claimed: dict[str, str] = {}

    for candidate in candidates:
        directory = run_dir / candidate["key"]
        directory.mkdir(parents=True, exist_ok=True)
        candidate_path = directory / "candidate.json"
        if candidate_path.exists() and read_json(candidate_path) != candidate:
            raise ValueError(f"Saved candidate differs from input: {candidate['key']}")
        write_json(candidate_path, candidate)
        write_json(directory / "payload.json", _payload(candidate))
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
            active[candidate["key"]] = ActiveSimulation(
                candidate,
                directory,
                creation["location"],
                float(creation["requested_at"]),
            )
        else:
            pending.append((candidate, directory))

    started = client._monotonic()
    while pending or active:
        if client._monotonic() - started >= max_runtime:
            write_json(run_dir / "summary.json", _summary(candidates, results, failures, pending, active))
            raise BatchTimeout("Batch deadline reached; rerun the command to resume")

        while pending and len(active) < max_active:
            candidate, directory = pending.pop(0)
            requested_at = client._wall_time()
            try:
                location, response = client.create_simulation(_payload(candidate))
            except (BrainAPIError, requests.RequestException) as error:
                failure = {"phase": "create", "message": str(error)}
                write_json(directory / "error.json", failure)
                failures.append({"key": candidate["key"], "error": failure})
                continue
            write_json(
                directory / "creation.json",
                {
                    "location": location,
                    "requested_at": requested_at,
                    "response": response.as_dict(),
                },
            )
            active[candidate["key"]] = ActiveSimulation(
                candidate, directory, location, requested_at
            )

        now = client._monotonic()
        made_request = False
        for key, item in list(active.items()):
            if item.next_poll > now:
                continue
            made_request = True
            try:
                response = client.simulation_status(item.location)
                write_json(item.directory / "status-latest.json", response.as_dict())
                body = response.body
                if not isinstance(body, dict):
                    raise BrainProtocolError(f"Simulation status for {key} is invalid")
                if body.get("status") == "ERROR" or body.get("error"):
                    raise BrainProtocolError(f"Simulation {key} failed: {body}")
                alpha_id = body.get("alpha")
                if isinstance(alpha_id, str):
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

    summary = _summary(candidates, results, failures, pending, active)
    write_json(run_dir / "summary.json", summary)
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
    return parser


def main() -> None:
    args = build_parser().parse_args()
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
        BrainClient(args.env),
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
