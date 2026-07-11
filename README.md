# AgonAlpha

AgonAlpha is an agent-based framework for automated alpha discovery. It follows the principles of [Prompt Economy](https://arxiv.org/abs/2606.24177).

## TODO

- [x] Integrate WorldQuant BRAIN
- [ ] Integrate vectorbt
- [ ] Integrate QuantConnect LEAN

## Quick Start

```
cd alphas
claude --plugin-dir .. --dangerously-skip-permissions --model claude-sonnet-5[1m]
# in claude code
/alpha-mcts 1
```

## Research Foundation

- **Topic**: [docs/topic.md](docs/topic.md) — Agon Alpha research direction
- **Landscape**: [docs/landscape.md](docs/landscape.md) — 158 full-text paper survey across 24 sub-domains
- **Landscape v2**: [docs/landscape-v2.md](docs/landscape-v2.md) — Independently reviewed, corrected version

## Key Findings (from 158 paper survey)

- **Zero collision on core claims**: No existing system combines factory-loop architecture, adversarial overfitting defense, deep lit → factor closed loop, multi-model consensus, and full lifecycle management
- **25 identified building blocks** from competitor papers that can be directly integrated
- **Chen & Welch (2026)**: Published academic alphas post-2005 yield median 7bp/month in large-cap stocks — statistically indistinguishable from zero
