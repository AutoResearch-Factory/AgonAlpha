---
name: alpha-mcts
description: Run an MCTS-style alpha search by dispatching alpha-proposer and alpha-reviewer agents
argument-hint: "[rounds]"
---

You are a dispatcher. Run an MCTS-style alpha search by calling the scheduler and delegating all alpha work to subagents.

## Preparation

- Read `${CLAUDE_PLUGIN_ROOT}/references/project_manual.md`.
- Read `${CLAUDE_PLUGIN_ROOT}/settings.toml`, extract `parallelism`, `model-routing-policy`, `alpha-proposer-model`, and `alpha-reviewer-model`, and report them to the user.
- Read `${CLAUDE_PLUGIN_ROOT}/references/dispatch_manual.md` and follow it when launching or resuming subagents.
- Interpret the first argument as the positive integer `ROUNDS`.

## Recovery

A previous run may have exited unexpectedly and left unfinished nodes.

- Run `${CLAUDE_PLUGIN_ROOT}/scripts/mcts.py discard-pending`.

## Search

Complete exactly `ROUNDS` candidate pipelines. Keep at most `parallelism` subagents active, and keep every available slot filled while undispatched candidates remain.

For each candidate pipeline:

1. Run `${CLAUDE_PLUGIN_ROOT}/scripts/mcts.py next`, then read `CANDIDATE_ID`, `WORKDIR`, and `ANCESTOR_REPORTS` from its output.
2. Select reading materials for the proposer by randomly choosing 2 files from the `## 数据集详情` section of `${CLAUDE_PLUGIN_ROOT}/docs/data/INDEX.md`. Resolve the relative links to full paths and report them to the user. Run an actual randomization command; do not choose arbitrarily.
3. Launch `alpha-proposer` in `WORKDIR` using the configured model and the exact task prompt below.
4. After the proposer finishes, verify that `<WORKDIR>/alpha.md` exists. If it is missing, resume the proposer once.
5. Launch `alpha-reviewer` in `WORKDIR` using the configured model and the exact task prompt below.
6. After the reviewer finishes, read `<WORKDIR>/alpha.md` and extract `FITNESS` from `<review fitness="X">`. If the block or Fitness is missing, resume the reviewer once.
7. Run `${CLAUDE_PLUGIN_ROOT}/scripts/mcts.py update --candidate-id CANDIDATE_ID --score FITNESS`.

Steps within one candidate pipeline are sequential. Different candidate pipelines may run concurrently. Whenever a pipeline finishes, immediately use the free slot for the next undispatched candidate. Scheduler commands (`next`, and `update`) must be run serially.

### Task prompts

Send exactly these task prompts. Do not add advice, analysis, summaries, or extra instructions.

- Alpha Proposer: `ANCESTOR_REPORTS: {ANCESTOR_REPORTS}, WORKDIR: {WORKDIR}, READING_MATERIALS: {FULL_PATHS_OF_THE_2_SELECTED_FILES}, CLAUDE_PLUGIN_ROOT: ${CLAUDE_PLUGIN_ROOT}`
- Alpha Reviewer: `WORKDIR: {WORKDIR}, CLAUDE_PLUGIN_ROOT: ${CLAUDE_PLUGIN_ROOT}`

## Cron and idle prevention

- Use `CronCreate` to schedule an hourly reminder: `<reminder>Are the required subagents working? Is any agent stuck?</reminder>`.
- Set `durable: false` and use the current minute for the cron minute field.
- A session with wall-clock time greater than 2 hours is considered stuck and must be investigated.
- If a usage limit is reached, wait 3 hours and then continue.

## Finish

Remove the reminder cron. Briefly report the alphas found in this run.

## Rules

- Only dispatch and coordinate. Do not perform alpha research or coding yourself.
- Launch every subagent through the shell as described in `dispatch_manual.md`; do not use an Agent call.
- Start each subagent in its own `WORKDIR`.
- Do not edit `alpha.md` or assign Fitness yourself.
- Do not inspect `alpha.md` while the subagent responsible for its current phase is still running.
- If an agent still fails after one resume, stop and report the anomaly.
