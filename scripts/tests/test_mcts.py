from __future__ import annotations

import bisect
import importlib.util
import itertools
import json
import math
import shutil
from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "mcts.py"
SPEC = importlib.util.spec_from_file_location("mcts", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
mcts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mcts)


@pytest.fixture
def alphas_dir(tmp_path, monkeypatch):
    path = tmp_path / "alphas"
    monkeypatch.setattr(mcts, "ALPHAS_DIR", path)
    return path


def init_args(**overrides):
    values = {
        "ucb_c": mcts.DEFAULT_UCB_C,
        "pw_k": mcts.DEFAULT_PW_K,
        "pw_alpha": mcts.DEFAULT_PW_ALPHA,
    }
    values.update(overrides)
    return Namespace(**values)


def update_args(candidate_id, score):
    return Namespace(candidate_id=candidate_id, score=score)


def mid_cdf_reward(score, scores):
    ordered = sorted(scores)
    inf = bisect.bisect_left(ordered, score)
    sup = bisect.bisect_right(ordered, score)
    return 5.0 * (inf + sup) / len(ordered)


def test_percentile_reward_matches_mid_cdf_and_stays_unbiased_with_ties():
    values = (-1, 0, 1)
    queries = (-2, -1, -0.5, 0, 0.5, 1, 2)

    for size in range(1, 7):
        for population in itertools.product(values, repeat=size):
            scores = list(population)
            for score in queries:
                actual = mcts._percentile_reward(score, scores)
                assert actual == pytest.approx(mid_cdf_reward(score, scores))
                assert 0 <= actual <= 10

            mean_reward = (
                sum(mcts._percentile_reward(score, scores) for score in scores) / size
            )
            assert mean_reward == pytest.approx(5)

    adjacent = math.nextafter(0.0, 1.0)
    assert mcts._percentile_reward(0.0, [0.0, adjacent]) == 2.5
    assert mcts._percentile_reward(adjacent, [0.0, adjacent]) == 7.5
    assert mcts._percentile_reward(-0.0, [-0.0, 0.0]) == 5


@pytest.mark.parametrize(
    ("score", "scores", "message"),
    [
        (0.0, [], "scores must not be empty"),
        (math.nan, [0.0], "scores must be finite"),
        (math.inf, [0.0], "scores must be finite"),
        (0.0, [math.nan], "scores must be finite"),
        (0.0, [-math.inf], "scores must be finite"),
    ],
)
def test_percentile_reward_rejects_undefined_populations(score, scores, message):
    with pytest.raises(ValueError, match=message):
        mcts._percentile_reward(score, scores)


def test_parent_selection_combines_subtree_reward_ucb_and_progressive_widening():
    state = {
        "config": {"ucb_c": 10.0, "pw_k": 1.0, "pw_alpha": 0.5},
        "nodes": {
            "root": mcts._new_node("root", None, 0, "root"),
            "branch": mcts._new_node("branch", "root", 1, "done"),
            "direct": mcts._new_node("direct", "root", 1, "done"),
            "leaf": mcts._new_node("leaf", "branch", 2, "done"),
        },
    }
    state["nodes"]["root"].update(children=["branch", "direct"], visits=4)
    state["nodes"]["branch"].update(children=["leaf"], visits=2, score=-2.0)
    state["nodes"]["direct"].update(visits=2, score=0.0)
    state["nodes"]["leaf"].update(visits=1, score=2.0)

    rewards = mcts._node_rewards(state)
    pending_counts = mcts._pending_counts(state)
    assert rewards["branch"] < rewards["direct"] < rewards["leaf"]
    assert mcts._subtree_reward_sum(state, rewards, "branch") == pytest.approx(10)

    # At the exact widening boundary, subtree value selects the branch.
    assert not mcts._should_widen(state, pending_counts, "root", 1.0, 0.5)
    assert mcts._select_parent(state) == "branch"

    # More visits open another progressive-widening slot at the root.
    state["nodes"]["root"]["visits"] = 9
    assert mcts._select_parent(state) == "root"

    state["nodes"]["unvisited"] = mcts._new_node("unvisited", "root", 1, "done")
    pending_counts["unvisited"] = 0
    assert math.isinf(
        mcts._ucb(state, rewards, pending_counts, "root", "unvisited", 10.0)
    )


def test_pending_counts_follow_each_in_flight_path_and_ignore_discarded_nodes():
    nodes = {
        "root": mcts._new_node("root", None, 0, "root"),
        "a": mcts._new_node("a", "root", 1, "done"),
        "b": mcts._new_node("b", "root", 1, "done"),
        "b1": mcts._new_node("b1", "b", 2, "done"),
        "p_root": mcts._new_node("p_root", "root", 1, "pending"),
        "p_a": mcts._new_node("p_a", "a", 2, "pending"),
        "p_deep": mcts._new_node("p_deep", "b1", 3, "pending"),
        "old": mcts._new_node("old", "root", 1, "discarded"),
    }
    nodes["root"]["children"] = ["a", "b", "p_root", "old"]
    nodes["a"]["children"] = ["p_a"]
    nodes["b"]["children"] = ["b1"]
    nodes["b1"]["children"] = ["p_deep"]

    counts = mcts._pending_counts({"nodes": nodes})

    assert counts == {
        "root": 3,
        "a": 1,
        "b": 1,
        "b1": 1,
        "p_root": 1,
        "p_a": 1,
        "p_deep": 1,
        "old": 0,
    }


def test_pending_and_discarded_scores_never_enter_completed_rewards():
    nodes = {
        "root": mcts._new_node("root", None, 0, "root"),
        "done": mcts._new_node("done", "root", 1, "done"),
        "pending": mcts._new_node("pending", "root", 1, "pending"),
        "discarded": mcts._new_node("discarded", "root", 1, "discarded"),
    }
    nodes["root"]["children"] = ["done", "pending", "discarded"]
    nodes["done"].update(score=1.0, visits=1)
    # Deliberately malformed scores prove that status, not only nullness, is used.
    nodes["pending"]["score"] = 100.0
    nodes["discarded"]["score"] = 200.0
    state = {"nodes": nodes}

    assert mcts._score_history(state) == [1.0]
    assert mcts._node_rewards(state) == {"done": 5.0}
    assert mcts._subtree_reward_sum(state, mcts._node_rewards(state), "root") == 5.0


def test_wu_uct_prefers_equivalent_sibling_without_in_flight_work():
    state = {
        "config": {"ucb_c": 10.0, "pw_k": 1.0, "pw_alpha": 0.5},
        "nodes": {
            "root": mcts._new_node("root", None, 0, "root"),
            "busy": mcts._new_node("busy", "root", 1, "done"),
            "free": mcts._new_node("free", "root", 1, "done"),
            "in_flight": mcts._new_node("in_flight", "busy", 2, "pending"),
        },
    }
    state["nodes"]["root"].update(children=["busy", "free"], visits=2)
    state["nodes"]["busy"].update(children=["in_flight"], visits=1, score=1.0)
    state["nodes"]["free"].update(visits=1, score=1.0)

    rewards = mcts._node_rewards(state)
    pending_counts = mcts._pending_counts(state)
    busy_ucb = mcts._ucb(
        state, rewards, pending_counts, "root", "busy", state["config"]["ucb_c"]
    )
    free_ucb = mcts._ucb(
        state, rewards, pending_counts, "root", "free", state["config"]["ucb_c"]
    )

    assert free_ucb > busy_ucb
    assert mcts._select_parent(state) == "free"


def test_progressive_widening_uses_done_children_and_completed_plus_pending_samples():
    state = {
        "nodes": {"root": mcts._new_node("root", None, 0, "root")},
    }
    root = state["nodes"]["root"]
    root["visits"] = 1
    for cid in ("d1", "d2"):
        state["nodes"][cid] = mcts._new_node(cid, "root", 1, "done")
        root["children"].append(cid)
    for cid in ("p1", "p2", "p3", "p4"):
        state["nodes"][cid] = mcts._new_node(cid, "root", 1, "pending")
        root["children"].append(cid)
    state["nodes"]["old"] = mcts._new_node("old", "root", 1, "discarded")
    root["children"].append("old")

    no_pending = {node_id: 0 for node_id in state["nodes"]}
    assert not mcts._should_widen(state, no_pending, "root", 1.0, 0.5)
    assert mcts._should_widen(state, mcts._pending_counts(state), "root", 1.0, 0.5)


def test_root_is_fallback_when_every_non_root_branch_has_a_pending_child():
    state = {
        "config": {"ucb_c": 10.0, "pw_k": 1.0, "pw_alpha": 0.5},
        "nodes": {"root": mcts._new_node("root", None, 0, "root")},
    }
    root = state["nodes"]["root"]
    root["visits"] = 3
    for index in range(3):
        done_id = f"d{index}"
        pending_id = f"p{index}"
        state["nodes"][done_id] = mcts._new_node(done_id, "root", 1, "done")
        state["nodes"][done_id].update(
            children=[pending_id], visits=1, score=float(index)
        )
        state["nodes"][pending_id] = mcts._new_node(pending_id, done_id, 2, "pending")
        root["children"].append(done_id)

    counts = mcts._pending_counts(state)
    assert not mcts._should_widen(state, counts, "root", 1.0, 0.5)
    assert mcts._select_parent(state) == "root"


def test_backpropagation_and_ancestor_order_follow_only_the_selected_path():
    state = {
        "nodes": {
            "root": mcts._new_node("root", None, 0, "root"),
            "grandparent": mcts._new_node("grandparent", "root", 1, "done"),
            "parent": mcts._new_node("parent", "grandparent", 2, "done"),
            "leaf": mcts._new_node("leaf", "parent", 3, "done"),
            "sibling": mcts._new_node("sibling", "grandparent", 2, "done"),
        }
    }

    assert mcts._ancestor_ids(state, "leaf") == ["parent", "grandparent"]
    mcts._backprop_visit(state, "leaf")

    assert state["nodes"]["leaf"]["visits"] == 1
    assert state["nodes"]["parent"]["visits"] == 1
    assert state["nodes"]["grandparent"]["visits"] == 1
    assert state["nodes"]["root"]["visits"] == 1
    assert state["nodes"]["sibling"]["visits"] == 0


def test_init_preserves_existing_alpha_files_and_refuses_to_reset_state(
    alphas_dir, capsys
):
    alphas_dir.mkdir()
    env_file = alphas_dir / ".env"
    env_file.write_text("sentinel")

    args = init_args(ucb_c=7.5, pw_k=1.25, pw_alpha=0.6)
    mcts.cmd_init(args)
    output = capsys.readouterr().out
    state_before = mcts._state_path().read_bytes()
    state = mcts._load_state()

    assert output == f"ALPHAS_DIR: {alphas_dir}\n"
    assert env_file.read_text() == "sentinel"
    assert state["config"] == {"ucb_c": 7.5, "pw_k": 1.25, "pw_alpha": 0.6}
    assert "run_dir" not in state
    assert "score_direction" not in state["config"]

    with pytest.raises(SystemExit, match="state already exists"):
        mcts.cmd_init(args)
    assert mcts._state_path().read_bytes() == state_before
    assert env_file.read_text() == "sentinel"


def test_next_initializes_missing_state_with_defaults(alphas_dir, capsys):
    alphas_dir.mkdir()
    env_file = alphas_dir / ".env"
    env_file.write_text("sentinel")

    mcts.cmd_next(Namespace())
    output = capsys.readouterr().out
    state = mcts._load_state()

    assert "CANDIDATE_ID: 0001" in output
    assert "ANCESTOR_REPORTS:\nnone" in output
    assert state["config"] == {
        "ucb_c": mcts.DEFAULT_UCB_C,
        "pw_k": mcts.DEFAULT_PW_K,
        "pw_alpha": mcts.DEFAULT_PW_ALPHA,
    }
    assert state["nodes"]["0001"]["status"] == "pending"
    assert mcts._candidate_dir("0001").is_dir()
    assert env_file.read_text() == "sentinel"


def test_consecutive_next_calls_create_distinct_pending_root_children(
    alphas_dir, capsys
):
    for _ in range(3):
        mcts.cmd_next(Namespace())
        capsys.readouterr()

    state = mcts._load_state()

    assert state["nodes"]["root"]["children"] == ["0001", "0002", "0003"]
    for cid in ("0001", "0002", "0003"):
        assert state["nodes"][cid]["parent"] == "root"
        assert state["nodes"][cid]["status"] == "pending"
        assert mcts._candidate_dir(cid).is_dir()


def test_state_lock_prevents_overlapping_next_calls_from_losing_updates(
    alphas_dir, capsys
):
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda _: mcts.cmd_next(Namespace()), range(2)))
    capsys.readouterr()

    state = mcts._load_state()
    assert state["next_candidate_num"] == 2
    assert state["nodes"]["root"]["children"] == ["0001", "0002"]
    assert set(state["nodes"]) == {"root", "0001", "0002"}


def test_atomic_save_failure_preserves_previous_state(alphas_dir, monkeypatch):
    alphas_dir.mkdir()
    original = mcts._initial_state()
    mcts._save_state(original)
    before = mcts._state_path().read_bytes()

    def fail_replace(source, destination):
        raise OSError("replace failed")

    monkeypatch.setattr(mcts.os, "replace", fail_replace)
    changed = mcts._initial_state(ucb_c=99.0)
    with pytest.raises(OSError, match="replace failed"):
        mcts._save_state(changed)

    assert mcts._state_path().read_bytes() == before
    assert list(alphas_dir.glob(".state.*.tmp")) == []


def test_discard_pending_resets_simulation_registry_without_state(alphas_dir, capsys):
    mcts.cmd_discard_pending(Namespace())

    assert capsys.readouterr().out == ""
    assert not mcts._state_path().exists()
    assert json.loads(mcts._simulation_registry_path().read_text()) == {
        "simulations": {}
    }


def test_discard_pending_keeps_tombstones_retries_cleanup_and_never_reuses_ids(
    alphas_dir, capsys
):
    alphas_dir.mkdir()
    nodes = {
        "root": mcts._new_node("root", None, 0, "root"),
        "0001": mcts._new_node("0001", "root", 1, "done"),
        "0002": mcts._new_node("0002", "0001", 2, "done"),
        "0003": mcts._new_node("0003", "root", 1, "pending"),
        "0004": mcts._new_node("0004", "root", 1, "done"),
        "0005": mcts._new_node("0005", "root", 1, "pending"),
    }
    nodes["root"].update(children=["0001", "0003", "0004", "0005"], visits=3)
    nodes["0001"].update(children=["0002"], visits=2, score=1.0)
    nodes["0002"].update(visits=1, score=2.0)
    nodes["0004"].update(visits=1, score=3.0)
    state = {
        "method": "alpha-mcts",
        "next_candidate_num": 5,
        "config": {
            "ucb_c": mcts.DEFAULT_UCB_C,
            "pw_k": mcts.DEFAULT_PW_K,
            "pw_alpha": mcts.DEFAULT_PW_ALPHA,
        },
        "nodes": nodes,
    }
    mcts._save_state(state)
    mcts._simulation_registry_path().write_text(
        json.dumps(
            {
                "simulations": {
                    "stale": {
                        "candidate": "0003",
                        "workdir": str(mcts._candidate_dir("0003")),
                        "location": "https://brain.test/simulations/stale",
                        "started_at": 1.0,
                    }
                }
            }
        )
    )
    for cid in ("0003", "0005"):
        mcts._candidate_dir(cid).mkdir()
        (mcts._candidate_dir(cid) / "sentinel").write_text(cid)

    mcts.cmd_discard_pending(Namespace())
    output = capsys.readouterr().out
    cleaned = mcts._load_state()

    assert output == (
        f"DISCARDED_WORKDIR: {mcts._candidate_dir('0003')}\n"
        f"DISCARDED_WORKDIR: {mcts._candidate_dir('0005')}\n"
    )
    assert set(cleaned["nodes"]) == {"root", "0001", "0002", "0003", "0004", "0005"}
    assert cleaned["nodes"]["root"]["children"] == ["0001", "0003", "0004", "0005"]
    assert cleaned["nodes"]["0001"]["children"] == ["0002"]
    assert cleaned["nodes"]["0003"]["status"] == "discarded"
    assert cleaned["nodes"]["0005"]["status"] == "discarded"
    assert cleaned["next_candidate_num"] == 5
    assert all(count == 0 for count in mcts._pending_counts(cleaned).values())
    assert json.loads(mcts._simulation_registry_path().read_text()) == {
        "simulations": {}
    }

    # Cleanup output is repeatable until the dispatcher removes the directories.
    mcts.cmd_discard_pending(Namespace())
    assert capsys.readouterr().out == output
    for cid in ("0003", "0005"):
        assert (mcts._candidate_dir(cid) / "sentinel").read_text() == cid
        shutil.rmtree(mcts._candidate_dir(cid))

    mcts.cmd_discard_pending(Namespace())
    assert capsys.readouterr().out == ""

    mcts.cmd_next(Namespace())
    assert "CANDIDATE_ID: 0006" in capsys.readouterr().out


def test_discard_pending_rejects_non_pending_descendants_without_modifying_state(
    alphas_dir, capsys
):
    alphas_dir.mkdir()
    nodes = {
        "root": mcts._new_node("root", None, 0, "root"),
        "0001": mcts._new_node("0001", "root", 1, "pending"),
        "0002": mcts._new_node("0002", "0001", 2, "done"),
    }
    nodes["root"]["children"] = ["0001"]
    nodes["0001"]["children"] = ["0002"]
    state = {"next_candidate_num": 2, "nodes": nodes}
    mcts._save_state(state)
    before = mcts._state_path().read_bytes()

    with pytest.raises(SystemExit, match="pending candidate has children: 0001"):
        mcts.cmd_discard_pending(Namespace())

    assert capsys.readouterr().out == ""
    assert mcts._state_path().read_bytes() == before


def test_candidate_flow_persists_widening_ancestry_and_maximize_selection(
    alphas_dir, capsys
):
    mcts.cmd_init(init_args())
    capsys.readouterr()

    mcts.cmd_next(Namespace())
    first_output = capsys.readouterr().out
    assert "CANDIDATE_ID: 0001" in first_output
    assert "ANCESTOR_REPORTS:\nnone" in first_output
    mcts._alpha_path("0001").write_text("alpha 1")
    mcts.cmd_update(update_args("0001", -0.5))
    capsys.readouterr()

    mcts.cmd_next(Namespace())
    second_output = capsys.readouterr().out
    assert "CANDIDATE_ID: 0002" in second_output
    assert f"ancestor 1 (father): {mcts._alpha_path('0001')}" in second_output
    mcts._alpha_path("0002").write_text("alpha 2")
    mcts.cmd_update(update_args("0002", -0.5))
    capsys.readouterr()

    # Two completed visits open a second root branch.
    mcts.cmd_next(Namespace())
    third_output = capsys.readouterr().out
    assert "CANDIDATE_ID: 0003" in third_output
    assert "ANCESTOR_REPORTS:\nnone" in third_output
    mcts._alpha_path("0003").write_text("alpha 3")
    mcts.cmd_update(update_args("0003", 1.5))
    capsys.readouterr()

    # With widening closed again, maximize selects the high-Fitness branch.
    mcts.cmd_next(Namespace())
    fourth_output = capsys.readouterr().out
    assert "CANDIDATE_ID: 0004" in fourth_output
    assert f"ancestor 1 (father): {mcts._alpha_path('0003')}" in fourth_output

    state = mcts._load_state()
    assert state["nodes"]["0001"]["parent"] == "root"
    assert state["nodes"]["0002"]["parent"] == "0001"
    assert state["nodes"]["0003"]["parent"] == "root"
    assert state["nodes"]["0004"]["parent"] == "0003"
    assert state["nodes"]["root"]["visits"] == 3
    assert state["nodes"]["0001"]["visits"] == 2
    assert state["nodes"]["0002"]["visits"] == 1
    assert state["nodes"]["0003"]["visits"] == 1
    assert state["nodes"]["0004"]["status"] == "pending"
    assert mcts._candidate_dir("0004").is_dir()


def test_update_failures_are_non_destructive_and_same_score_retry_is_idempotent(
    alphas_dir, capsys
):
    mcts.cmd_init(init_args())
    mcts.cmd_next(Namespace())
    capsys.readouterr()
    pending_state = mcts._state_path().read_bytes()

    invalid_updates = [
        ("missing", 1.0, "unknown candidate id"),
        ("root", 1.0, "unknown candidate id"),
        ("0001", math.nan, "score must be finite"),
        ("0001", math.inf, "score must be finite"),
    ]
    for candidate_id, score, message in invalid_updates:
        with pytest.raises(SystemExit, match=message):
            mcts.cmd_update(update_args(candidate_id, score))
        assert mcts._state_path().read_bytes() == pending_state

    mcts.cmd_update(update_args("0001", 0.0))
    capsys.readouterr()
    completed_state = mcts._state_path().read_bytes()

    mcts.cmd_update(update_args("0001", 0.0))
    assert capsys.readouterr().out == "ALREADY_UPDATED: 0001 score=0\n"
    assert mcts._state_path().read_bytes() == completed_state

    with pytest.raises(SystemExit, match="candidate already has a different score"):
        mcts.cmd_update(update_args("0001", 2.0))
    assert mcts._state_path().read_bytes() == completed_state

    state = json.loads(completed_state)
    assert state["nodes"]["0001"]["score"] == 0
    assert state["nodes"]["0001"]["visits"] == 1
    assert state["nodes"]["root"]["visits"] == 1


def test_print_next_labels_deep_ancestors_without_including_root(alphas_dir, capsys):
    alphas_dir.mkdir()
    nodes = {"root": mcts._new_node("root", None, 0, "root")}
    parent = "root"
    for depth, candidate_id in enumerate(("0001", "0002", "0003", "0004"), start=1):
        nodes[candidate_id] = mcts._new_node(candidate_id, parent, depth, "done")
        nodes[parent]["children"].append(candidate_id)
        parent = candidate_id
    mcts._save_state({"nodes": nodes})

    mcts._print_next({"nodes": nodes}, "0004")
    output = capsys.readouterr().out

    assert f"ancestor 1 (father): {mcts._alpha_path('0003')}" in output
    assert f"ancestor 2 (grandfather): {mcts._alpha_path('0002')}" in output
    assert f"ancestor 3: {mcts._alpha_path('0001')}" in output
    assert "root/alpha.md" not in output


# --- _save_state fd protection ---


def test_save_state_closes_fd_on_fdopen_failure(alphas_dir, monkeypatch):
    alphas_dir.mkdir()
    mcts._save_state(mcts._initial_state())
    before = mcts._state_path().read_bytes()

    def failing_fdopen(fd, *args, **kwargs):
        raise OSError("fdopen failed")

    monkeypatch.setattr(mcts.os, "fdopen", failing_fdopen)

    with pytest.raises(OSError, match="fdopen failed"):
        mcts._save_state(mcts._initial_state(ucb_c=99.0))

    assert mcts._state_path().read_bytes() == before
    assert list(alphas_dir.glob(".state.*.tmp")) == []


# --- cycle detection ---


def test_subtree_reward_sum_raises_on_cycle():
    nodes = {
        "root": mcts._new_node("root", None, 0, "root"),
        "a": mcts._new_node("a", "root", 1, "done"),
        "b": mcts._new_node("b", "a", 2, "done"),
    }
    nodes["root"]["children"] = ["a"]
    nodes["a"]["children"] = ["b"]
    nodes["b"]["children"] = ["a"]
    nodes["a"].update(score=1.0, visits=1)
    nodes["b"].update(score=1.0, visits=1)

    with pytest.raises(ValueError, match="cycle in subtree"):
        mcts._subtree_reward_sum({"nodes": nodes}, {"a": 5.0, "b": 5.0}, "root")


def test_backprop_visit_raises_on_cycle():
    nodes = {
        "root": mcts._new_node("root", None, 0, "root"),
        "a": mcts._new_node("a", "root", 1, "done"),
    }
    nodes["a"]["parent"] = "a"

    with pytest.raises(ValueError, match="cycle in parent path"):
        mcts._backprop_visit({"nodes": nodes}, "a")


def test_ancestor_ids_raises_on_cycle():
    nodes = {
        "root": mcts._new_node("root", None, 0, "root"),
        "a": mcts._new_node("a", "root", 1, "done"),
        "b": mcts._new_node("b", "a", 2, "done"),
    }
    nodes["a"]["parent"] = "b"

    with pytest.raises(ValueError, match="cycle in parent path"):
        mcts._ancestor_ids({"nodes": nodes}, "b")


# --- _next_candidate_id bounded loop ---


def test_next_candidate_id_raises_on_exhaustion():
    state = mcts._initial_state()

    class AlwaysContains(dict):
        def __contains__(self, key):
            return True

    state["nodes"] = AlwaysContains(state["nodes"])

    with pytest.raises(RuntimeError, match="could not allocate a candidate id"):
        mcts._next_candidate_id(state)


# --- non-ASCII round-trip ---


def test_save_and_load_state_round_trips_non_ascii(alphas_dir):
    alphas_dir.mkdir()
    state = mcts._initial_state()
    state["nodes"]["0001"] = mcts._new_node("0001", "root", 1, "done")
    state["nodes"]["0001"]["score"] = "日本語テスト"
    mcts._save_state(state)
    loaded = mcts._load_state()
    assert loaded["nodes"]["0001"]["score"] == "日本語テスト"
