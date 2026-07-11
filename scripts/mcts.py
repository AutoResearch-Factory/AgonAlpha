#!/usr/bin/env python3
"""MCTS scheduler for AgonAlpha.

This script does not call LLMs and does not evaluate candidates.
It only manages tree state and returns the next candidate workdir.

Commands:
  mcts.py init
  mcts.py next
  mcts.py update --candidate-id ID --score X
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ALPHAS_DIR = (Path(__file__).resolve().parent / "../alphas").resolve()
ROOT_ID = "root"
DEFAULT_UCB_C = 10.0
DEFAULT_PW_K = 1.0
DEFAULT_PW_ALPHA = 0.5


def _state_path() -> Path:
    return ALPHAS_DIR / "state.json"


def _candidate_dir(cid: str) -> Path:
    return ALPHAS_DIR / cid


def _alpha_path(cid: str) -> Path:
    return _candidate_dir(cid) / "alpha.md"


def _load_state() -> dict:
    with _state_path().open() as f:
        return json.load(f)


def _save_state(state: dict) -> None:
    _state_path().write_text(json.dumps(state, indent=2) + "\n")


def _new_node(node_id: str, parent: str | None, depth: int, status: str = "open") -> dict:
    return {
        "id": node_id,
        "parent": parent,
        "children": [],
        "depth": depth,
        "visits": 0,
        "score": None,
        "status": status,
    }


def _next_candidate_id(state: dict) -> str:
    state["next_candidate_num"] += 1
    return f"{state['next_candidate_num']:04d}"


def _score_history(state: dict) -> list[float]:
    scores = []
    for cid, node in state["nodes"].items():
        if cid != ROOT_ID and node.get("score") is not None:
            scores.append(float(node["score"]))
    return scores


def _percentile_reward(score: float, scores: list[float]) -> float:
    if not scores:
        raise ValueError("scores must not be empty")
    if not math.isfinite(score) or any(not math.isfinite(s) for s in scores):
        raise ValueError("scores must be finite")
    inf = sum(1 for s in scores if s < score)
    sup = sum(1 for s in scores if s <= score)
    rank = (inf + sup) / 2
    return 10.0 * rank / len(scores)


def _node_rewards(state: dict) -> dict[str, float]:
    scores = _score_history(state)
    rewards: dict[str, float] = {}
    for cid, node in state["nodes"].items():
        if cid == ROOT_ID or node.get("score") is None:
            continue
        rewards[cid] = _percentile_reward(float(node["score"]), scores)
    return rewards


def _subtree_reward_sum(state: dict, rewards: dict[str, float], node_id: str) -> float:
    total = rewards.get(node_id, 0.0)
    for child_id in state["nodes"][node_id]["children"]:
        total += _subtree_reward_sum(state, rewards, child_id)
    return total


def _ucb(state: dict, rewards: dict[str, float], child_id: str, parent_visits: int, c: float) -> float:
    child = state["nodes"][child_id]
    if child["visits"] == 0:
        return float("inf")
    q = _subtree_reward_sum(state, rewards, child_id) / child["visits"]
    return q + c * math.sqrt(math.log(max(parent_visits, 1)) / child["visits"])


def _should_widen(node: dict, pw_k: float, pw_alpha: float) -> bool:
    return len(node["children"]) < pw_k * (max(node["visits"], 1) ** pw_alpha)


def _select_parent(state: dict) -> str:
    nodes = state["nodes"]
    rewards = _node_rewards(state)
    c = state["config"]["ucb_c"]
    pw_k = state["config"]["pw_k"]
    pw_alpha = state["config"]["pw_alpha"]

    cur_id = ROOT_ID
    while True:
        cur = nodes[cur_id]
        if _should_widen(cur, pw_k, pw_alpha):
            return cur_id
        if not cur["children"]:
            return cur_id
        parent_visits = max(cur["visits"], 1)
        cur_id = max(cur["children"], key=lambda cid: _ucb(state, rewards, cid, parent_visits, c))


def _backprop_visit(state: dict, node_id: str) -> None:
    nodes = state["nodes"]
    cur: str | None = node_id
    while cur is not None:
        nodes[cur]["visits"] += 1
        cur = nodes[cur]["parent"]


def _ancestor_ids(state: dict, node_id: str) -> list[str]:
    nodes = state["nodes"]
    out: list[str] = []
    cur = nodes[node_id]["parent"]
    while cur is not None and cur != ROOT_ID:
        out.append(cur)
        cur = nodes[cur]["parent"]
    return out


def _print_next(cid: str) -> None:
    print(f"CANDIDATE_ID: {cid}")
    print(f"WORKDIR: {_candidate_dir(cid)}")
    ancestors = _ancestor_ids(_load_state(), cid)
    print("ANCESTOR_REPORTS:")
    if not ancestors:
        print("none")
        return
    labels = {0: "ancestor 1 (father)", 1: "ancestor 2 (grandfather)"}
    for i, aid in enumerate(ancestors):
        label = labels.get(i, f"ancestor {i + 1}")
        print(f"- {label}: {_alpha_path(aid)}")


def cmd_init(args: argparse.Namespace) -> None:
    ALPHAS_DIR.mkdir(parents=True, exist_ok=True)
    if _state_path().exists():
        raise SystemExit(f"state already exists: {_state_path()}")
    state = {
        "method": "alpha-mcts",
        "next_candidate_num": 0,
        "config": {
            "ucb_c": args.ucb_c,
            "pw_k": args.pw_k,
            "pw_alpha": args.pw_alpha,
        },
        "nodes": {ROOT_ID: _new_node(ROOT_ID, None, 0, status="root")},
    }
    _save_state(state)
    print(f"ALPHAS_DIR: {ALPHAS_DIR}")


def cmd_next(args: argparse.Namespace) -> None:
    state = _load_state()

    for cid, node in sorted(state["nodes"].items()):
        if cid != ROOT_ID and node.get("status") == "pending":
            _candidate_dir(cid).mkdir(parents=True, exist_ok=True)
            _print_next(cid)
            return

    parent_id = _select_parent(state)
    parent = state["nodes"][parent_id]
    cid = _next_candidate_id(state)
    state["nodes"][cid] = _new_node(cid, parent_id, parent["depth"] + 1, status="pending")
    parent["children"].append(cid)
    _candidate_dir(cid).mkdir(parents=True)
    _save_state(state)
    _print_next(cid)


def cmd_update(args: argparse.Namespace) -> None:
    state = _load_state()
    cid = args.candidate_id
    if cid not in state["nodes"] or cid == ROOT_ID:
        raise SystemExit(f"unknown candidate id: {cid}")
    node = state["nodes"][cid]
    if node.get("status") != "pending":
        raise SystemExit(f"candidate is not pending: {cid}")
    score = float(args.score)
    if not math.isfinite(score):
        raise SystemExit("score must be finite")

    node["score"] = score
    node["status"] = "done"
    _backprop_visit(state, cid)
    _save_state(state)
    print(f"UPDATED: {cid} score={score:.4g}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--ucb-c", type=float, default=DEFAULT_UCB_C)
    p_init.add_argument("--pw-k", type=float, default=DEFAULT_PW_K)
    p_init.add_argument("--pw-alpha", type=float, default=DEFAULT_PW_ALPHA)
    p_init.set_defaults(func=cmd_init)

    p_next = sub.add_parser("next")
    p_next.set_defaults(func=cmd_next)

    p_update = sub.add_parser("update")
    p_update.add_argument("--candidate-id", required=True)
    p_update.add_argument("--score", required=True, type=float)
    p_update.set_defaults(func=cmd_update)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
