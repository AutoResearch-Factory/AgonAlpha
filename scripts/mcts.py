#!/usr/bin/env python3
"""MCTS scheduler for AgonAlpha.

This script does not call LLMs and does not evaluate candidates.
It only manages tree state and returns the next candidate workdir.

Commands:
  mcts.py init
  mcts.py discard-pending
  mcts.py next
  mcts.py update --candidate-id ID --score X
"""

from __future__ import annotations

import argparse
import fcntl
import json
import math
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

ALPHAS_DIR = (Path(__file__).resolve().parent / "../alphas").resolve()
ROOT_ID = "root"
DEFAULT_UCB_C = 10.0
DEFAULT_PW_K = 1.0
DEFAULT_PW_ALPHA = 0.5
SIMULATION_REGISTRY_FILENAME = ".brain-simulations.json"


def _state_path() -> Path:
    return ALPHAS_DIR / "state.json"


def _candidate_dir(cid: str) -> Path:
    return ALPHAS_DIR / cid


def _alpha_path(cid: str) -> Path:
    return _candidate_dir(cid) / "alpha.md"


def _lock_path() -> Path:
    return ALPHAS_DIR / ".state.lock"


def _simulation_registry_path() -> Path:
    return ALPHAS_DIR / SIMULATION_REGISTRY_FILENAME


def _reset_simulation_registry() -> None:
    path = _simulation_registry_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    with os.fdopen(fd, "r+", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.seek(0)
            json.dump({"simulations": {}}, f, indent=2, sort_keys=True)
            f.write("\n")
            f.truncate()
            f.flush()
            os.fsync(f.fileno())
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


@contextmanager
def _state_lock():
    ALPHAS_DIR.mkdir(parents=True, exist_ok=True)
    with _lock_path().open("a") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _load_state() -> dict:
    with _state_path().open(encoding="utf-8") as f:
        return json.load(f)


def _save_state(state: dict) -> None:
    ALPHAS_DIR.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(state, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=".state.", suffix=".tmp", dir=ALPHAS_DIR)
    tmp_path = Path(tmp_name)
    try:
        try:
            f = os.fdopen(fd, "w", encoding="utf-8")
        except BaseException:
            os.close(fd)
            raise
        with f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, _state_path())
    finally:
        tmp_path.unlink(missing_ok=True)


def _new_node(node_id: str, parent: str | None, depth: int, status: str) -> dict:
    return {
        "id": node_id,
        "parent": parent,
        "children": [],
        "depth": depth,
        "visits": 0,
        "score": None,
        "status": status,
    }


def _initial_state(
    ucb_c: float = DEFAULT_UCB_C,
    pw_k: float = DEFAULT_PW_K,
    pw_alpha: float = DEFAULT_PW_ALPHA,
) -> dict:
    return {
        "method": "alpha-mcts",
        "next_candidate_num": 0,
        "config": {
            "ucb_c": ucb_c,
            "pw_k": pw_k,
            "pw_alpha": pw_alpha,
        },
        "nodes": {ROOT_ID: _new_node(ROOT_ID, None, 0, status="root")},
    }


def _next_candidate_id(state: dict) -> str:
    limit = state["next_candidate_num"] + len(state["nodes"]) + 1
    while state["next_candidate_num"] < limit:
        state["next_candidate_num"] += 1
        cid = f"{state['next_candidate_num']:04d}"
        if cid not in state["nodes"]:
            return cid
    raise RuntimeError("could not allocate a candidate id")


def _score_history(state: dict) -> list[float]:
    return [
        float(node["score"])
        for cid, node in state["nodes"].items()
        if cid != ROOT_ID
        and node.get("status") == "done"
        and node.get("score") is not None
    ]


def _percentile_reward(score: float, scores: list[float]) -> float:
    if not scores:
        raise ValueError("scores must not be empty")
    if not math.isfinite(score) or any(not math.isfinite(s) for s in scores):
        raise ValueError("scores must be finite")
    below = sum(1 for s in scores if s < score)
    at_or_below = sum(1 for s in scores if s <= score)
    rank = (below + at_or_below) / 2
    return 10.0 * rank / len(scores)


def _node_rewards(state: dict) -> dict[str, float]:
    scores = _score_history(state)
    if not scores:
        return {}
    return {
        cid: _percentile_reward(float(node["score"]), scores)
        for cid, node in state["nodes"].items()
        if cid != ROOT_ID
        and node.get("status") == "done"
        and node.get("score") is not None
    }


def _subtree_reward_sum(
    state: dict,
    rewards: dict[str, float],
    node_id: str,
    _seen: set[str] | None = None,
) -> float:
    if _seen is None:
        _seen = set()
    if node_id in _seen:
        raise ValueError(f"cycle in subtree: {node_id}")
    _seen.add(node_id)
    total = rewards.get(node_id, 0.0)
    for child_id in state["nodes"][node_id]["children"]:
        if state["nodes"][child_id].get("status") == "done":
            total += _subtree_reward_sum(state, rewards, child_id, _seen)
    return total


def _pending_counts(state: dict) -> dict[str, int]:
    nodes = state["nodes"]
    counts = {node_id: 0 for node_id in nodes}
    for node_id, node in nodes.items():
        if node.get("status") != "pending":
            continue
        cur: str | None = node_id
        seen: set[str] = set()
        while cur is not None:
            if cur in seen:
                raise ValueError(f"cycle in parent path: {node_id}")
            if cur not in nodes:
                raise ValueError(f"unknown parent in path from: {node_id}")
            seen.add(cur)
            counts[cur] += 1
            cur = nodes[cur]["parent"]
    return counts


def _done_children(state: dict, node_id: str) -> list[str]:
    nodes = state["nodes"]
    return [
        child_id
        for child_id in nodes[node_id]["children"]
        if nodes[child_id].get("status") == "done"
    ]


def _has_pending_child(state: dict, node_id: str) -> bool:
    nodes = state["nodes"]
    return any(
        nodes[child_id].get("status") == "pending"
        for child_id in nodes[node_id]["children"]
    )


def _ucb(
    state: dict,
    rewards: dict[str, float],
    pending_counts: dict[str, int],
    parent_id: str,
    child_id: str,
    c: float,
) -> float:
    child = state["nodes"][child_id]
    if child["visits"] == 0:
        return float("inf")
    q = _subtree_reward_sum(state, rewards, child_id) / child["visits"]
    parent_samples = state["nodes"][parent_id]["visits"] + pending_counts[parent_id]
    child_samples = child["visits"] + pending_counts[child_id]
    return q + c * math.sqrt(math.log(max(parent_samples, 1)) / child_samples)


def _should_widen(
    state: dict,
    pending_counts: dict[str, int],
    node_id: str,
    pw_k: float,
    pw_alpha: float,
) -> bool:
    node = state["nodes"][node_id]
    done_child_count = len(_done_children(state, node_id))
    samples = node["visits"] + pending_counts[node_id]
    return done_child_count < pw_k * (max(samples, 1) ** pw_alpha)


def _select_parent(state: dict) -> str:
    rewards = _node_rewards(state)
    pending_counts = _pending_counts(state)
    c = state["config"]["ucb_c"]
    pw_k = state["config"]["pw_k"]
    pw_alpha = state["config"]["pw_alpha"]

    def search(node_id: str) -> str | None:
        # A non-root node may have at most one direct pending child. While that
        # child is running, the node itself cannot be expanded again, although
        # its completed descendants remain selectable.
        can_expand = node_id == ROOT_ID or not _has_pending_child(state, node_id)
        if can_expand and _should_widen(state, pending_counts, node_id, pw_k, pw_alpha):
            return node_id

        done_children = _done_children(state, node_id)
        ranked_children = sorted(
            done_children,
            key=lambda child_id: _ucb(
                state, rewards, pending_counts, node_id, child_id, c
            ),
            reverse=True,
        )
        for child_id in ranked_children:
            selected = search(child_id)
            if selected is not None:
                return selected
        return None

    # If every non-root branch is busy, root is the deliberate fallback even
    # when its progressive-widening condition is currently closed.
    return search(ROOT_ID) or ROOT_ID


def _backprop_visit(state: dict, node_id: str) -> None:
    nodes = state["nodes"]
    seen: set[str] = set()
    cur: str | None = node_id
    while cur is not None:
        if cur in seen:
            raise ValueError(f"cycle in parent path: {node_id}")
        seen.add(cur)
        nodes[cur]["visits"] += 1
        cur = nodes[cur]["parent"]


def _ancestor_ids(state: dict, node_id: str) -> list[str]:
    nodes = state["nodes"]
    out: list[str] = []
    seen: set[str] = {node_id}
    cur = nodes[node_id]["parent"]
    while cur is not None and cur != ROOT_ID:
        if cur in seen:
            raise ValueError(f"cycle in parent path: {node_id}")
        seen.add(cur)
        out.append(cur)
        cur = nodes[cur]["parent"]
    return out


def _print_next(state: dict, cid: str) -> None:
    print(f"CANDIDATE_ID: {cid}")
    print(f"WORKDIR: {_candidate_dir(cid)}")
    ancestors = _ancestor_ids(state, cid)
    print("ANCESTOR_REPORTS:")
    if not ancestors:
        print("none")
        return
    QUALIFIERS = ("father", "grandfather")
    for i, aid in enumerate(ancestors):
        suffix = f" ({QUALIFIERS[i]})" if i < len(QUALIFIERS) else ""
        print(f"- ancestor {i + 1}{suffix}: {_alpha_path(aid)}")


def cmd_init(args: argparse.Namespace) -> None:
    with _state_lock():
        if _state_path().exists():
            raise SystemExit(f"state already exists: {_state_path()}")
        _save_state(_initial_state(args.ucb_c, args.pw_k, args.pw_alpha))
        print(f"ALPHAS_DIR: {ALPHAS_DIR}")


def cmd_discard_pending(args: argparse.Namespace) -> None:
    with _state_lock():
        _reset_simulation_registry()
        if not _state_path().exists():
            return
        state = _load_state()
        nodes = state["nodes"]
        pending_ids = sorted(
            cid
            for cid, node in nodes.items()
            if cid != ROOT_ID and node.get("status") == "pending"
        )
        for cid in pending_ids:
            if nodes[cid]["children"]:
                raise SystemExit(f"pending candidate has children: {cid}")
            nodes[cid]["status"] = "discarded"
        if pending_ids:
            _save_state(state)

        discarded_workdirs = sorted(
            _candidate_dir(cid)
            for cid, node in nodes.items()
            if cid != ROOT_ID
            and node.get("status") == "discarded"
            and _candidate_dir(cid).exists()
        )
        for workdir in discarded_workdirs:
            print(f"DISCARDED_WORKDIR: {workdir}")


def cmd_next(args: argparse.Namespace) -> None:
    with _state_lock():
        if not _state_path().exists():
            _save_state(_initial_state())
        state = _load_state()

        parent_id = _select_parent(state)
        parent = state["nodes"][parent_id]
        cid = _next_candidate_id(state)
        state["nodes"][cid] = _new_node(
            cid, parent_id, parent["depth"] + 1, status="pending"
        )
        parent["children"].append(cid)
        _candidate_dir(cid).mkdir(parents=True, exist_ok=True)
        _save_state(state)
        _print_next(state, cid)


def cmd_update(args: argparse.Namespace) -> None:
    score = args.score
    if not math.isfinite(score):
        raise SystemExit("score must be finite")

    with _state_lock():
        state = _load_state()
        cid = args.candidate_id
        if cid not in state["nodes"] or cid == ROOT_ID:
            raise SystemExit(f"unknown candidate id: {cid}")
        node = state["nodes"][cid]
        if node.get("status") == "done":
            if float(node["score"]) == score:
                print(f"ALREADY_UPDATED: {cid} score={score:.4g}")
                return
            raise SystemExit(f"candidate already has a different score: {cid}")
        if node.get("status") != "pending":
            raise SystemExit(f"candidate is not pending: {cid}")

        node["score"] = score
        node["status"] = "done"
        _backprop_visit(state, cid)
        _save_state(state)
        print(f"UPDATED: {cid} score={score:.4g}")


def _best_metrics(cid: str) -> tuple[float | None, float | None]:
    best_fitness: float | None = None
    best_sharpe: float | None = None
    directory = _candidate_dir(cid)
    paths = [directory / "brain_summary.json"]
    paths.extend(directory.glob("brain_summary.*.json"))
    for path in paths:
        if not path.exists():
            continue
        try:
            with path.open(encoding="utf-8") as f:
                summary = json.load(f)
        except (ValueError, OSError):
            continue
        for result in summary.get("results", []):
            is_data = result.get("is") if isinstance(result, dict) else None
            if not isinstance(is_data, dict):
                continue
            fitness = is_data.get("fitness")
            if isinstance(fitness, (int, float)) and (
                best_fitness is None or fitness > best_fitness
            ):
                best_fitness = fitness
                sharpe = is_data.get("sharpe")
                best_sharpe = sharpe if isinstance(sharpe, (int, float)) else None
    return best_fitness, best_sharpe


def cmd_tree(args: argparse.Namespace) -> None:
    if not _state_path().exists():
        raise SystemExit("no state file found")
    with _state_lock():
        state = _load_state()
    nodes = state["nodes"]

    def label(node_id: str) -> str:
        node = nodes[node_id]
        status = node.get("status", "?")
        visits = node.get("visits", 0)
        score = node.get("score")
        tag = f"{status}, v={visits}"
        if score is not None:
            tag += f", s={score:.4g}"
        parts = [node_id, f"[{tag}]"]
        if node_id != ROOT_ID and status == "done":
            fitness, sharpe = _best_metrics(node_id)
            if fitness is not None:
                parts.append(f"fitness={fitness:.3g}")
            if sharpe is not None:
                parts.append(f"sharpe={sharpe:.3g}")
        return " ".join(parts)

    def walk(node_id: str, prefix: str) -> None:
        children = nodes[node_id].get("children", [])
        for i, child_id in enumerate(children):
            is_last = i == len(children) - 1
            print(f"{prefix}{'└── ' if is_last else '├── '}{label(child_id)}")
            walk(child_id, prefix + ("    " if is_last else "│   "))

    print(label(ROOT_ID))
    walk(ROOT_ID, "")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--ucb-c", type=float, default=DEFAULT_UCB_C)
    p_init.add_argument("--pw-k", type=float, default=DEFAULT_PW_K)
    p_init.add_argument("--pw-alpha", type=float, default=DEFAULT_PW_ALPHA)
    p_init.set_defaults(func=cmd_init)

    p_discard_pending = sub.add_parser("discard-pending")
    p_discard_pending.set_defaults(func=cmd_discard_pending)

    p_next = sub.add_parser("next")
    p_next.set_defaults(func=cmd_next)

    p_update = sub.add_parser("update")
    p_update.add_argument("--candidate-id", required=True)
    p_update.add_argument("--score", required=True, type=float)
    p_update.set_defaults(func=cmd_update)

    p_tree = sub.add_parser("tree")
    p_tree.set_defaults(func=cmd_tree)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
