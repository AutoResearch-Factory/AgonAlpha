from __future__ import annotations

import importlib.util
import json
import sys
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


def candidate(key: str) -> dict:
    return {
        "key": key,
        "name": f"name-{key}",
        "type": "REGULAR",
        "regular": key,
        "settings": {"region": "USA", "delay": 1},
    }


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


def test_retry_after_accepts_http_date_and_rejects_bad_values():
    now = 1_800_000_000.0
    future = format_datetime(datetime.fromtimestamp(now + 17, timezone.utc), usegmt=True)

    assert brain_client.retry_after_seconds(
        {"retry-after": future}, 3.0, now=now
    ) == pytest.approx(17.0)
    assert brain_client.retry_after_seconds(
        {"Retry-After": "not-a-date"}, 3.0, now=now
    ) == 3.0


def test_run_dir_must_match_the_execution_directory(tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    assert brain_client.run_dir_for_current_workdir(run_dir, cwd=run_dir) == run_dir
    with pytest.raises(ValueError, match="must be the current working directory"):
        brain_client.run_dir_for_current_workdir(tmp_path / "other", cwd=run_dir)


def test_candidate_names_must_match_the_workdir_loop_and_slug():
    brain_client.validate_candidate_names(
        [{"name": "0007-12-short-reversal"}], "0007"
    )

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
def test_candidate_loading_blocks_deduplication_and_path_escape(tmp_path, rows, message):
    path = tmp_path / "candidates.json"
    path.write_text(json.dumps(rows), encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        brain_client.load_candidates(path)


def test_simulate_candidates_keeps_multiple_jobs_inflight_and_names_results(tmp_path):
    clock = Clock()
    client = FakeBatchClient(clock)
    candidates = [candidate("a"), candidate("b"), candidate("c")]

    summary = brain_client.simulate_candidates(
        client, candidates, tmp_path / "run", max_active=2
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
        result = json.loads((tmp_path / "run" / key / "result.json").read_text())
        assert result["alpha_id"] == f"alpha-{key}"


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
        client, [candidate("a")], tmp_path / "run"
    )

    assert summary["completed_count"] == 1
    assert client.poll_times == [0.0, expected_second_poll]


def test_simulate_candidates_resumes_saved_location_without_resubmitting(tmp_path):
    clock = Clock()
    client = FakeBatchClient(clock)
    candidates = [candidate("a"), candidate("b")]
    run_dir = tmp_path / "run"
    active_dir = run_dir / "a"
    active_dir.mkdir(parents=True)
    brain_client.write_json(active_dir / "candidate.json", candidates[0])
    brain_client.write_json(active_dir / "payload.json", brain_client._payload(candidates[0]))
    location = "https://brain.test/simulations/resumed-a"
    brain_client.write_json(
        active_dir / "creation.json",
        {"location": location, "requested_at": clock.wall(), "response": {}},
    )
    client.register(location, candidates[0])

    complete_dir = run_dir / "b"
    complete_dir.mkdir(parents=True)
    saved_result = {
        "candidate": candidates[1],
        "alpha_id": "saved-b",
        "name": "name-b",
    }
    brain_client.write_json(complete_dir / "result.json", saved_result)

    summary = brain_client.simulate_candidates(client, candidates, run_dir)

    assert summary["completed_count"] == 2
    assert not [event for event in client.events if event[0] == "create"]
    assert client.events[0] == ("poll", "a")


def test_reused_old_alpha_is_never_renamed(tmp_path):
    clock = Clock()
    client = FakeBatchClient(clock, old_alpha=True)

    summary = brain_client.simulate_candidates(
        client, [candidate("a")], tmp_path / "run"
    )

    assert summary["completed_count"] == 0
    assert summary["failure_count"] == 1
    assert "predates this simulation" in summary["failures"][0]["error"]["message"]
    assert not [event for event in client.events if event[0] == "name"]


def test_alpha_without_creation_time_is_never_renamed(tmp_path):
    clock = Clock()
    client = FakeBatchClient(clock, missing_created_at=True)

    summary = brain_client.simulate_candidates(
        client, [candidate("a")], tmp_path / "run"
    )

    assert summary["completed_count"] == 0
    assert "no valid dateCreated" in summary["failures"][0]["error"]["message"]
    assert not [event for event in client.events if event[0] == "name"]
