from __future__ import annotations

import importlib.util
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

import pytest
import requests


MODULE_PATH = Path(__file__).resolve().parents[1] / "brain_client.py"
SPEC = importlib.util.spec_from_file_location("brain_client", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
brain_client = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = brain_client
SPEC.loader.exec_module(brain_client)


def response(status: int, body=None, headers=None) -> requests.Response:
    result = requests.Response()
    result.status_code = status
    result.headers.update(headers or {})
    result._content = (
        b"" if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    )
    result.encoding = "utf-8"
    return result


def write_env(path: Path) -> Path:
    path.write_text(
        'export BRAIN_EMAIL="researcher@example.com"\n'
        "BRAIN_PASSWORD='secret=with#symbols'\n",
        encoding="utf-8",
    )
    return path


class FakeSession:
    def __init__(self, *, posts=(), requests_=()):
        self.posts = list(posts)
        self.requests = list(requests_)
        self.post_calls = []
        self.request_calls = []

    def post(self, url, **kwargs):
        self.post_calls.append((url, kwargs))
        item = self.posts.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    def request(self, method, url, **kwargs):
        self.request_calls.append((method, url, kwargs))
        item = self.requests.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class Clock:
    def __init__(self):
        self.monotonic_value = 0.0
        self.wall_value = 1_800_000_000.0
        self.sleeps = []

    def monotonic(self):
        return self.monotonic_value

    def wall(self):
        return self.wall_value

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.monotonic_value += seconds
        self.wall_value += seconds


class FakeBatchClient:
    def __init__(self, clock: Clock, *, old_alpha=False, missing_created_at=False):
        self._monotonic = clock.monotonic
        self._wall_time = clock.wall
        self._sleep = clock.sleep
        self.old_alpha = old_alpha
        self.missing_created_at = missing_created_at
        self.events = []
        self.simulations = {}
        self.names = {}
        self.inflight = 0
        self.max_inflight = 0

    def register(self, location, candidate):
        alpha_id = f"alpha-{candidate['key']}"
        self.simulations[location] = (candidate, alpha_id)

    def create_simulation(self, payload):
        key = payload["regular"]
        location = f"https://brain.test/simulations/{key}"
        candidate = {
            "key": key,
            "name": f"name-{key}",
            "regular": payload["regular"],
            "settings": payload["settings"],
        }
        self.register(location, candidate)
        self.events.append(("create", key))
        self.inflight += 1
        self.max_inflight = max(self.max_inflight, self.inflight)
        return location, brain_client.APIResponse(201, {"Location": location}, "")

    def simulation_status(self, location):
        candidate, alpha_id = self.simulations[location]
        self.events.append(("poll", candidate["key"]))
        self.inflight = max(self.inflight - 1, 0)
        return brain_client.APIResponse(200, {}, {"alpha": alpha_id})

    def alpha(self, alpha_id):
        candidate = next(
            candidate
            for candidate, current_alpha in self.simulations.values()
            if current_alpha == alpha_id
        )
        if self.old_alpha:
            created = "2020-01-01T00:00:00+00:00"
            name = "ancestor-alpha"
        else:
            created = datetime.fromtimestamp(
                self._wall_time(), timezone.utc
            ).isoformat()
            name = self.names.get(alpha_id)
        if self.missing_created_at:
            created = None
        return {
            "id": alpha_id,
            "name": name,
            "dateCreated": created,
            "regular": {"code": candidate["regular"]},
            "settings": candidate["settings"],
            "is": {"fitness": 1.0},
            "status": "UNSUBMITTED",
            "stage": "IS",
        }

    def set_alpha_name(self, alpha_id, name):
        self.events.append(("name", alpha_id))
        self.names[alpha_id] = name
        return brain_client.APIResponse(200, {}, {"name": name})


class DelayedBatchClient(FakeBatchClient):
    def __init__(self, clock: Clock, retry_after: str):
        super().__init__(clock)
        self.retry_after = retry_after
        self.poll_times = []
        self.waiting = True

    def simulation_status(self, location):
        candidate, alpha_id = self.simulations[location]
        self.events.append(("poll", candidate["key"]))
        self.poll_times.append(self._monotonic())
        if self.waiting:
            self.waiting = False
            return brain_client.APIResponse(
                200, {"Retry-After": self.retry_after}, {"progress": 0.5}
            )
        self.inflight = max(self.inflight - 1, 0)
        return brain_client.APIResponse(200, {}, {"alpha": alpha_id})


class ConcurrencyLimitedBatchClient(FakeBatchClient):
    def __init__(self, clock: Clock):
        super().__init__(clock)
        self.create_attempts = 0

    def create_simulation(self, payload):
        self.create_attempts += 1
        if self.create_attempts == 1:
            raise brain_client.BrainAPIError(
                "POST",
                "https://brain.test/simulations",
                brain_client.APIResponse(
                    429,
                    {"Retry-After": "2"},
                    {"detail": "CONCURRENT_SIMULATION_LIMIT_EXCEEDED"},
                ),
            )
        return super().create_simulation(payload)


def candidate(key: str) -> dict:
    return {
        "key": key,
        "name": f"name-{key}",
        "type": "REGULAR",
        "regular": key,
        "settings": {"region": "USA", "delay": 1},
    }


def simulation_registry(tmp_path, clock):
    return brain_client.SimulationRegistry(
        tmp_path / ".brain-simulations.json",
        wall_time=clock.wall,
    )


def authenticated_client(tmp_path, clock, *, requests_=()):
    session = FakeSession(requests_=requests_)
    client = brain_client.BrainClient(
        write_env(tmp_path / ".env"),
        session=session,
        sleep=clock.sleep,
        monotonic=clock.monotonic,
        wall_time=clock.wall,
    )
    client.authenticated = True
    return client


def test_simulation_registry_atomically_caps_concurrent_leases(tmp_path):
    clock = Clock()
    registry = simulation_registry(tmp_path, clock)

    with ThreadPoolExecutor(max_workers=10) as pool:
        lease_ids = list(
            pool.map(
                lambda index: registry.try_acquire(
                    candidate=f"candidate-{index}", workdir=tmp_path / str(index)
                ),
                range(10),
            )
        )

    acquired = [lease_id for lease_id in lease_ids if lease_id is not None]
    assert len(acquired) == 3
    assert len(registry.snapshot()) == 3


def test_simulation_registry_prunes_one_hour_zombies_and_ignores_old_release(
    tmp_path,
):
    clock = Clock()
    registry = simulation_registry(tmp_path, clock)
    old_leases = [
        registry.try_acquire(
            candidate=f"old-{index}", workdir=tmp_path / f"old-{index}"
        )
        for index in range(brain_client.MAX_CONCURRENT_SIMULATIONS)
    ]
    assert all(lease_id is not None for lease_id in old_leases)
    assert (
        registry.try_acquire(candidate="blocked", workdir=tmp_path / "blocked") is None
    )

    clock.wall_value += brain_client.SIMULATION_LEASE_TIMEOUT_SECONDS
    new_lease = registry.try_acquire(candidate="new", workdir=tmp_path / "new")

    assert new_lease is not None
    assert registry.release(old_leases[0]) is False
    assert set(registry.snapshot()) == {new_lease}


def test_request_reauthenticates_once(tmp_path):
    session = FakeSession(
        posts=(response(201), response(201)),
        requests_=(
            response(401, {"detail": "expired"}),
            response(200, {"ok": True}),
        ),
    )
    sleeps = []
    client = brain_client.BrainClient(
        write_env(tmp_path / ".env"), session=session, sleep=sleeps.append
    )

    result = client.request("GET", "alphas/example")

    assert result.body == {"ok": True}
    assert len(session.post_calls) == 2
    assert len(session.request_calls) == 2
    assert sleeps == []
    auth = session.post_calls[0][1]["auth"]
    assert auth.username == "researcher@example.com"
    assert auth.password == "secret=with#symbols"


def test_submission_checks_retry_empty_200_response(tmp_path):
    clock = Clock()
    checks = {"is": {"checks": [{"name": "fitness", "result": "PASS"}]}}
    client = authenticated_client(
        tmp_path, clock,
        requests_=(
            response(200, None, {"Retry-After": "2"}),
            response(200, checks),
        ),
    )

    assert client.submission_checks("alpha-1") == checks
    assert clock.sleeps == [2.0]


def test_submission_checks_waits_for_pending_to_resolve(tmp_path):
    clock = Clock()
    pending = {"is": {"checks": [
        {"name": "LOW_SHARPE", "result": "PASS"},
        {"name": "SELF_CORRELATION", "result": "PENDING"},
    ]}}
    resolved = {"is": {"checks": [
        {"name": "LOW_SHARPE", "result": "PASS"},
        {"name": "SELF_CORRELATION", "result": "PASS"},
    ]}}
    client = authenticated_client(
        tmp_path, clock,
        requests_=(response(200, pending), response(200, resolved)),
    )

    assert client.submission_checks("alpha-1") == resolved
    assert len(clock.sleeps) == 1


def test_submission_checks_returns_immediately_when_fail_and_pending(tmp_path):
    clock = Clock()
    checks = {"is": {"checks": [
        {"name": "LOW_SHARPE", "result": "FAIL"},
        {"name": "SELF_CORRELATION", "result": "PENDING"},
    ]}}
    client = authenticated_client(
        tmp_path, clock, requests_=(response(200, checks),)
    )

    assert client.submission_checks("alpha-1") == checks
    assert clock.sleeps == []


def test_submit_accepts_empty_201_and_verifies_eventual_alpha_state(tmp_path):
    clock = Clock()
    before = {
        "id": "alpha-1",
        "name": "candidate",
        "status": "UNSUBMITTED",
        "stage": "IS",
    }
    pending = {"id": "alpha-1", "name": "candidate", "status": "PENDING", "stage": "IS"}
    active = {"id": "alpha-1", "name": "candidate", "status": "ACTIVE", "stage": "OS"}
    client = authenticated_client(
        tmp_path, clock,
        requests_=(
            response(200, before),
            response(201, None, {"Retry-After": "2"}),
            response(200, pending),
            response(200, active),
        ),
    )

    result = client.submit_alpha("alpha-1")

    assert result["submission"]["status_code"] == 201
    assert result["submission"]["body"] == ""
    assert result["alpha"] == active
    assert clock.sleeps == [2.0, 5.0]


def test_retry_after_accepts_http_date_and_rejects_bad_values():
    now = 1_800_000_000.0
    future = format_datetime(
        datetime.fromtimestamp(now + 17, timezone.utc), usegmt=True
    )

    assert brain_client.retry_after_seconds(
        {"retry-after": future}, 3.0, now=now
    ) == pytest.approx(17.0)
    assert (
        brain_client.retry_after_seconds({"Retry-After": "not-a-date"}, 3.0, now=now)
        == 3.0
    )


def test_run_dir_must_match_the_execution_directory(tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    assert brain_client.run_dir_for_current_workdir(run_dir, cwd=run_dir) == run_dir
    with pytest.raises(ValueError, match="must be the current working directory"):
        brain_client.run_dir_for_current_workdir(tmp_path / "other", cwd=run_dir)


def test_candidate_names_must_match_the_workdir_loop_and_slug():
    brain_client.validate_candidate_names([{"name": "0007-12-short-reversal"}], "0007")

    with pytest.raises(ValueError, match="must start with '0007-'"):
        brain_client.validate_candidate_names(
            [{"name": "0008-12-short-reversal"}], "0007"
        )
    with pytest.raises(ValueError, match="CANDIDATE_ID.*LOOP_ID.*SLUG"):
        brain_client.validate_candidate_names(
            [{"name": "0007-0-Short_Reversal"}], "0007"
        )


@pytest.mark.parametrize(
    "rows, message",
    [
        (
            [
                {
                    "name": "alpha-one",
                    "regular": "rank(close)",
                    "settings": {"delay": 1},
                },
                {
                    "name": "alpha-two",
                    "regular": "rank(close)",
                    "settings": {"delay": 1},
                },
            ],
            "Duplicate candidate payload",
        ),
        (
            [
                {
                    "name": "../escape",
                    "regular": "rank(close)",
                    "settings": {"delay": 1},
                }
            ],
            "unsafe name",
        ),
        (
            [
                {
                    "slug": "alpha-one",
                    "name": "alpha-one",
                    "regular": "rank(close)",
                    "settings": {"delay": 1},
                }
            ],
            "must use name instead of slug",
        ),
    ],
)
def test_candidate_loading_blocks_deduplication_and_path_escape(
    tmp_path, rows, message
):
    path = tmp_path / "candidates.json"
    path.write_text(json.dumps(rows), encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        brain_client.load_candidates(path)


def test_simulate_candidates_keeps_multiple_jobs_inflight_and_names_results(tmp_path):
    clock = Clock()
    client = FakeBatchClient(clock)
    candidates = [candidate("a"), candidate("b"), candidate("c")]

    summary = brain_client.simulate_candidates(
        client,
        candidates,
        tmp_path / "run",
        max_active=2,
        registry=simulation_registry(tmp_path, clock),
    )

    assert summary["completed_count"] == 3
    assert summary["failure_count"] == 0
    assert client.max_inflight == 2
    assert client.events[:2] == [("create", "a"), ("create", "b")]
    assert [result["name"] for result in summary["results"]] == [
        "name-a",
        "name-b",
        "name-c",
    ]
    for key in "abc":
        directory = tmp_path / "run" / "brain" / key
        result = json.loads((directory / "result.json").read_text())
        assert result["alpha_id"] == f"alpha-{key}"
        assert result["simulation_location"].endswith(f"/{key}")
        assert {path.name for path in directory.iterdir()} == {
            "alpha.json",
            "candidate.json",
            "result.json",
        }


def test_concurrency_limit_error_requeues_instead_of_becoming_terminal(tmp_path):
    clock = Clock()
    client = ConcurrencyLimitedBatchClient(clock)
    registry = simulation_registry(tmp_path, clock)

    summary = brain_client.simulate_candidates(
        client,
        [candidate("a")],
        tmp_path / "run",
        registry=registry,
    )

    assert summary["completed_count"] == 1
    assert summary["failure_count"] == 0
    assert client.create_attempts == 2
    assert clock.sleeps[0] == 2.0
    assert not (tmp_path / "run" / "brain" / "a" / "error.json").exists()
    assert registry.snapshot() == {}


def test_simulate_candidates_writes_brain_summary_on_timeout(tmp_path):
    clock = Clock()
    client = DelayedBatchClient(clock, "30")

    with pytest.raises(brain_client.BatchTimeout):
        brain_client.simulate_candidates(
            client,
            [candidate("a")],
            tmp_path / "run",
            max_runtime=1.0,
            registry=simulation_registry(tmp_path, clock),
        )

    summary_path = tmp_path / "run" / "brain_summary.json"
    assert summary_path.exists()
    summary = json.loads(summary_path.read_text())
    assert summary["candidate_count"] == 1
    assert summary["completed_count"] == 0
    directory = tmp_path / "run" / "brain" / "a"
    assert {path.name for path in directory.iterdir()} == {
        "candidate.json",
        "creation.json",
    }
    assert set(json.loads((directory / "creation.json").read_text())) == {
        "global_count_active",
        "lease_id",
        "location",
        "requested_at",
    }


def test_brain_summary_rotates_previous_batches(tmp_path):
    clock = Clock()
    client = FakeBatchClient(clock)
    run_dir = tmp_path / "run"
    registry = simulation_registry(tmp_path, clock)

    for key in "abc":
        brain_client.simulate_candidates(
            client, [candidate(key)], run_dir, registry=registry
        )

    def result_names(path):
        return [result["name"] for result in json.loads(path.read_text())["results"]]

    assert result_names(run_dir / "brain_summary.json") == ["name-c"]
    assert result_names(run_dir / "brain_summary.1.json") == ["name-b"]
    assert result_names(run_dir / "brain_summary.2.json") == ["name-a"]
    assert not (run_dir / "brain_summary.3.json").exists()


@pytest.mark.parametrize(
    ("retry_after", "expected_second_poll"),
    [("5", 30.0), ("45", 45.0)],
)
def test_simulation_polling_uses_the_larger_of_retry_after_and_default_interval(
    tmp_path, retry_after, expected_second_poll
):
    clock = Clock()
    client = DelayedBatchClient(clock, retry_after)

    summary = brain_client.simulate_candidates(
        client,
        [candidate("a")],
        tmp_path / "run",
        registry=simulation_registry(tmp_path, clock),
    )

    assert summary["completed_count"] == 1
    assert client.poll_times == [0.0, expected_second_poll]


def test_simulate_candidates_resumes_saved_location_without_resubmitting(tmp_path):
    clock = Clock()
    client = FakeBatchClient(clock)
    candidates = [candidate("a"), candidate("b")]
    run_dir = tmp_path / "run"
    active_dir = run_dir / "brain" / "a"
    active_dir.mkdir(parents=True)
    brain_client.write_json(active_dir / "candidate.json", candidates[0])
    location = "https://brain.test/simulations/resumed-a"
    registry = simulation_registry(tmp_path, clock)
    lease_id = registry.try_acquire(
        candidate=candidates[0]["key"], workdir=active_dir, location=location
    )
    assert lease_id is not None
    brain_client.write_json(
        active_dir / "creation.json",
        {
            "location": location,
            "requested_at": clock.wall(),
            "lease_id": lease_id,
            "global_count_active": True,
            "response": {},
        },
    )
    client.register(location, candidates[0])

    complete_dir = run_dir / "brain" / "b"
    complete_dir.mkdir(parents=True)
    saved_result = {
        "candidate": candidates[1],
        "alpha_id": "saved-b",
        "name": "name-b",
    }
    brain_client.write_json(complete_dir / "result.json", saved_result)

    summary = brain_client.simulate_candidates(
        client, candidates, run_dir, registry=registry
    )

    assert summary["completed_count"] == 2
    assert not any(event[0] == "create" for event in client.events)
    assert client.events[0] == ("poll", "a")
    assert registry.snapshot() == {}


def test_reused_old_alpha_is_never_renamed(tmp_path):
    clock = Clock()
    client = FakeBatchClient(clock, old_alpha=True)

    summary = brain_client.simulate_candidates(
        client,
        [candidate("a")],
        tmp_path / "run",
        registry=simulation_registry(tmp_path, clock),
    )

    assert summary["completed_count"] == 0
    assert summary["failure_count"] == 1
    assert "predates this simulation" in summary["failures"][0]["error"]["message"]
    assert not any(event[0] == "name" for event in client.events)


def test_alpha_without_creation_time_is_never_renamed(tmp_path):
    clock = Clock()
    client = FakeBatchClient(clock, missing_created_at=True)

    summary = brain_client.simulate_candidates(
        client,
        [candidate("a")],
        tmp_path / "run",
        registry=simulation_registry(tmp_path, clock),
    )

    assert summary["completed_count"] == 0
    assert len(summary["failures"]) == 1
    assert "no valid dateCreated" in summary["failures"][0]["error"]["message"]
    assert not any(event[0] == "name" for event in client.events)


# --- _checks_resolved unit tests ---


@pytest.mark.parametrize(
    ("checks", "expected"),
    [
        ([], False),
        ([{"name": "A", "result": "PASS"}], True),
        ([{"name": "A", "result": "PASS"}, {"name": "B", "result": "PASS"}], True),
        ([{"name": "A", "result": "FAIL"}], True),
        ([{"name": "A", "result": "PENDING"}], False),
        ([{"name": "A", "result": "PASS"}, {"name": "B", "result": "PENDING"}], False),
        (
            [{"name": "A", "result": "FAIL"}, {"name": "B", "result": "PENDING"}],
            True,
        ),
        (
            [
                {"name": "A", "result": "FAIL"},
                {"name": "B", "result": "PASS"},
                {"name": "C", "result": "PENDING"},
            ],
            True,
        ),
    ],
)
def test_checks_resolved_covers_all_state_combinations(checks, expected):
    assert brain_client._checks_resolved(checks) is expected


# --- submission_checks edge cases ---


def test_submission_checks_keeps_polling_on_empty_checks_list(tmp_path):
    clock = Clock()
    empty = {"is": {"checks": []}}
    resolved = {"is": {"checks": [{"name": "A", "result": "PASS"}]}}
    client = authenticated_client(
        tmp_path, clock,
        requests_=(response(200, empty), response(200, resolved)),
    )

    assert client.submission_checks("alpha-1") == resolved
    assert len(clock.sleeps) == 1


def test_submission_checks_raises_batch_timeout(tmp_path):
    clock = Clock()
    client = authenticated_client(
        tmp_path, clock,
        requests_=(response(200, None), response(200, None)),
    )

    with pytest.raises(brain_client.BatchTimeout, match="timed out"):
        client.submission_checks("alpha-1", max_wait=1.0)


def test_submission_checks_raises_protocol_error_on_missing_checks(tmp_path):
    clock = Clock()
    client = authenticated_client(
        tmp_path, clock, requests_=(response(200, {"is": {}}),)
    )

    with pytest.raises(brain_client.BrainProtocolError, match="omitted is.checks"):
        client.submission_checks("alpha-1")


def test_submission_checks_raises_protocol_error_on_invalid_body(tmp_path):
    clock = Clock()
    client = authenticated_client(
        tmp_path, clock, requests_=(response(200, 42),)
    )

    with pytest.raises(brain_client.BrainProtocolError, match="invalid"):
        client.submission_checks("alpha-1")


# --- CLI exit code ---


def test_check_command_exits_nonzero_on_failed_check(tmp_path, monkeypatch):
    checks = {"is": {"checks": [{"name": "A", "result": "FAIL"}]}}
    fake = FakeSession(
        posts=(response(201),),
        requests_=(response(200, checks),),
    )
    monkeypatch.setattr("sys.argv", [
        "brain_client", "--env", str(write_env(tmp_path / ".env")),
        "check", "alpha-1",
    ])
    monkeypatch.setattr(requests, "Session", lambda: fake)

    with pytest.raises(SystemExit) as exc_info:
        brain_client.main()
    assert exc_info.value.code == 1


def test_check_command_exits_zero_on_all_pass(tmp_path, monkeypatch):
    checks = {"is": {"checks": [{"name": "A", "result": "PASS"}]}}
    fake = FakeSession(
        posts=(response(201),),
        requests_=(response(200, checks),),
    )
    monkeypatch.setattr("sys.argv", [
        "brain_client", "--env", str(write_env(tmp_path / ".env")),
        "check", "alpha-1",
    ])
    monkeypatch.setattr(requests, "Session", lambda: fake)

    brain_client.main()


# --- request reauthentication ---


def test_request_raises_on_second_consecutive_401(tmp_path):
    session = FakeSession(
        posts=(response(201), response(201)),
        requests_=(response(401), response(401)),
    )
    client = brain_client.BrainClient(
        write_env(tmp_path / ".env"), session=session, sleep=lambda _: None
    )

    with pytest.raises(brain_client.BrainAPIError) as exc_info:
        client.request("GET", "alphas/test")
    assert exc_info.value.response.status_code == 401


# --- load_env ---


def test_load_env_handles_utf8_bom(tmp_path):
    path = tmp_path / ".env"
    path.write_bytes(
        b"\xef\xbb\xbf"
        b'BRAIN_EMAIL="user@example.com"\n'
        b"BRAIN_PASSWORD=secret\n"
    )
    env = brain_client.load_env(path)
    assert env["BRAIN_EMAIL"] == "user@example.com"
    assert env["BRAIN_PASSWORD"] == "secret"


# --- retry_after_seconds ---


def test_retry_after_parses_numeric_seconds():
    assert brain_client.retry_after_seconds({"Retry-After": "5"}, 3.0) == 5.0
    assert brain_client.retry_after_seconds({"Retry-After": "0"}, 3.0) == 0.0


# --- load_candidates ---


def test_candidate_loading_accepts_wrapped_candidates_object(tmp_path):
    rows = [{"name": "a", "regular": "rank(close)", "settings": {"delay": 1}}]
    path = tmp_path / "candidates.json"
    path.write_text(json.dumps({"candidates": rows}), encoding="utf-8")
    result = brain_client.load_candidates(path)
    assert len(result) == 1
    assert result[0]["name"] == "a"


def test_candidate_loading_rejects_duplicate_names(tmp_path):
    rows = [
        {"name": "alpha-one", "regular": "rank(close)", "settings": {"delay": 1}},
        {"name": "alpha-one", "regular": "rank(open)", "settings": {"delay": 2}},
    ]
    path = tmp_path / "candidates.json"
    path.write_text(json.dumps(rows), encoding="utf-8")
    with pytest.raises(ValueError, match="Duplicate candidate name"):
        brain_client.load_candidates(path)


# --- SimulationRegistry ---


def test_simulation_registry_update_location_and_reset(tmp_path):
    clock = Clock()
    registry = simulation_registry(tmp_path, clock)
    lease_id = registry.try_acquire(candidate="a", workdir=tmp_path / "a")
    assert lease_id is not None

    assert registry.update_location(lease_id, "https://brain.test/sim/1")
    assert registry.snapshot()[lease_id]["location"] == "https://brain.test/sim/1"
    assert not registry.update_location("nonexistent", "https://brain.test/sim/2")

    registry.try_acquire(candidate="b", workdir=tmp_path / "b")
    assert len(registry.snapshot()) == 2
    registry.reset()
    assert registry.snapshot() == {}


# --- simulate_candidates resume validation ---


def test_simulate_candidates_rejects_corrupt_creation_json(tmp_path):
    clock = Clock()
    client = FakeBatchClient(clock)
    candidates = [candidate("a")]
    run_dir = tmp_path / "run"
    directory = run_dir / "brain" / "a"
    directory.mkdir(parents=True)
    brain_client.write_json(directory / "candidate.json", candidates[0])
    brain_client.write_json(
        directory / "creation.json",
        {
            "location": None,
            "requested_at": 1.0,
            "lease_id": None,
            "global_count_active": False,
        },
    )

    with pytest.raises(ValueError, match="Corrupt creation.json"):
        brain_client.simulate_candidates(
            client, candidates, run_dir, registry=simulation_registry(tmp_path, clock)
        )
