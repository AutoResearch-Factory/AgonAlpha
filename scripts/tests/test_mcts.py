from __future__ import annotations

import bisect
import importlib.util
import itertools
import json
import math
from argparse import Namespace
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

            mean_reward = sum(mcts._percentile_reward(score, scores) for score in scores) / size
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
    assert rewards["branch"] < rewards["direct"] < rewards["leaf"]
    assert mcts._subtree_reward_sum(state, rewards, "branch") == pytest.approx(10)

    # At the exact widening boundary, subtree value selects the branch.
    assert not mcts._should_widen(state["nodes"]["root"], 1.0, 0.5)
    assert mcts._select_parent(state) == "branch"

    # More visits open another progressive-widening slot at the root.
    state["nodes"]["root"]["visits"] = 9
    assert mcts._select_parent(state) == "root"

    state["nodes"]["unvisited"] = mcts._new_node("unvisited", "root", 1)
    assert math.isinf(mcts._ucb(state, rewards, "unvisited", 9, 10.0))


def test_backpropagation_and_ancestor_order_follow_only_the_selected_path():
    state = {
        "nodes": {
            "root": mcts._new_node("root", None, 0, "root"),
            "grandparent": mcts._new_node("grandparent", "root", 1),
            "parent": mcts._new_node("parent", "grandparent", 2),
            "leaf": mcts._new_node("leaf", "parent", 3),
            "sibling": mcts._new_node("sibling", "grandparent", 2),
        }
    }

    assert mcts._ancestor_ids(state, "leaf") == ["parent", "grandparent"]
    mcts._backprop_visit(state, "leaf")

    assert state["nodes"]["leaf"]["visits"] == 1
    assert state["nodes"]["parent"]["visits"] == 1
    assert state["nodes"]["grandparent"]["visits"] == 1
    assert state["nodes"]["root"]["visits"] == 1
    assert state["nodes"]["sibling"]["visits"] == 0


def test_init_preserves_existing_alpha_files_and_refuses_to_reset_state(alphas_dir, capsys):
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


def test_candidate_flow_persists_widening_ancestry_and_maximize_selection(alphas_dir, capsys):
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
    assert state["nodes"]["0003"]["visits"] == 1
    assert state["nodes"]["0004"]["status"] == "pending"
    assert mcts._candidate_dir("0004").is_dir()


def test_update_failures_are_non_destructive_and_duplicate_update_is_rejected(alphas_dir, capsys):
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

    with pytest.raises(SystemExit, match="candidate is not pending"):
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

    mcts._print_next("0004")
    output = capsys.readouterr().out

    assert f"ancestor 1 (father): {mcts._alpha_path('0003')}" in output
    assert f"ancestor 2 (grandfather): {mcts._alpha_path('0002')}" in output
    assert f"ancestor 3: {mcts._alpha_path('0001')}" in output
    assert "root/alpha.md" not in output
