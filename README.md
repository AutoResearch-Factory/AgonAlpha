# AgonAlpha

English | [中文](README_zh.md)

AgonAlpha ([paper](https://arxiv.org/abs/2608.11250)) is an agentic framework for reproducible quantitative alpha discovery. It searches over complete research artifacts—hypotheses, executable expressions, evaluation evidence, rationales, and review status—while a Monte Carlo tree search (MCTS) scheduler allocates work across candidate lineages.

The repository provides the orchestration layer. Data, credentials, evaluator integrations, generated candidates, and evaluation results remain local and are excluded from version control.

## How it works

Each search pipeline has two roles:

1. The **alpha proposer** generates or refines candidates, evaluates them with a user-supplied local evaluator, and records a reproducible report.
2. The **alpha reviewer** independently checks the report and its evidence, reruns evaluations when necessary, and assigns the verified Fitness used by the scheduler.

The scheduler combines percentile-based rewards, upper-confidence-bound selection, progressive widening, and visit backpropagation. Candidate reports are immutable ancestry records: a new candidate sees only the reports on its selected ancestor path.

## Repository layout

```text
agents/                         proposer and adversarial reviewer prompts
commands/alpha-mcts.md          search orchestration command
references/project_manual.md    candidate artifact format
references/dispatch_manual.md   supported subagent launch procedure
references/evaluator.example.md local evaluator contract template
scripts/mcts.py                 deterministic MCTS scheduler
scripts/tests/test_mcts.py      scheduler tests
settings.example.toml           model routing and concurrency example
```

## Requirements

- Python 3.10 or newer
- `pytest` to run the test suite
- Claude Code with local plugin support
- At least one supported agent CLI configured as described in `references/dispatch_manual.md`
- A local evaluation system capable of returning a finite numeric Fitness

## Setup

Clone the repository and create the local configuration files:

```bash
git clone https://github.com/AutoResearch-Factory/AgonAlpha.git
cd AgonAlpha
cp settings.example.toml settings.toml
cp references/evaluator.example.md references/evaluator.md
```

Edit `settings.toml` to choose concurrency and agent backends. Then complete `references/evaluator.md` with the available data, candidate syntax, executable evaluation interface, Fitness definition, acceptance checks, and authorization boundaries. Both files are ignored by Git.

Run the scheduler tests:

```bash
python -m pytest scripts/tests
```

## Usage

Start Claude Code with this repository loaded as a plugin:

```bash
claude --plugin-dir .
```

From the interactive session, request one or more completed candidate pipelines:

```text
/alpha-mcts 1
```

Replace `1` with the number of pipelines to complete. The command initializes `alphas/state.json` when needed, keeps up to `parallelism` pipelines active, and writes each candidate under `alphas/<candidate-id>/`. The entire `alphas/` workspace is ignored so expressions, evidence, and results are not committed accidentally.

The MCTS scheduler can also be exercised directly:

```bash
python scripts/mcts.py init
python scripts/mcts.py next
python scripts/mcts.py update --candidate-id 0001 --score 1.25
```

## Security and reproducibility

- Keep credentials in environment variables or a local secret store; never put values in `references/evaluator.md`.
- Save raw evaluation inputs and outputs inside the candidate work directory so the reviewer can reproduce the score.
- Do not commit generated alpha expressions, proprietary datasets, private platform documentation, or evaluation artifacts.
- Treat external submission, publication, and deployment as disabled unless they are explicitly authorized in the local evaluator contract.

## Citation

If AgonAlpha is useful in your research, please cite:

> W. Ye, Y. Sun, X. Ren, S. Yu, C. Yi, and H. Yang, “AgonAlpha: Autonomous Alpha Discovery via Prompt Economy and Scalable Agentic Search,” arXiv:2608.11250, 2026. [https://arxiv.org/abs/2608.11250](https://arxiv.org/abs/2608.11250)

```bibtex
@article{ye2026agonalpha,
  title   = {AgonAlpha: Autonomous Alpha Discovery via Prompt Economy and Scalable Agentic Search},
  author  = {Ye, Weicheng and Sun, Youran and Ren, Xingyu and Yu, Shunyao and Yi, Chugang and Yang, Haizhao},
  journal = {arXiv preprint arXiv:2608.11250},
  year    = {2026}
}
```
