# AutoAlpha Manual

## Directory layout

```
alphas/
├── .venv                       # shared venv; use Python 3.13 unless specified otherwise
├── state.json
├── 0001/
│   ├── alpha.md                # main alpha file
│   └── ...                     # other artifacts
└── 0002/
    ├── alpha.md
    └── ...
```

All BRAIN simulations must be created through `${CLAUDE_PLUGIN_ROOT}/scripts/brain_client.py`; do not send `POST /simulations` directly. The shared client enforces the account-wide concurrency limit across every agent working under `alphas/`.

## Alpha file format

<template>

# Alpha Report: <slug>

## One sentence

State the proposed alpha in one sentence, using LaTeX syntax for the formulae.

### Hypothesis

State the testable market belief behind the alpha. Describe the observed condition and the expected direction of future returns. Briefly explain the economic or behavioral intuition connecting them. Focus on what should happen and why.

## Final expression

Report the exact submitted Fast Expression and the BRAIN alpha name/ID.

## Motivation and explanation

Explain the intuition behind the alpha and the role of each component in its formula.
Explain every non-obvious sign, numeric constant, and lookback window. If a
constant or window is mainly search/tournament-selected rather than economically
or calendar-motivated, flag it as a possible overfitting risk.

## Performance

Report the final alpha's requested and actual simulation settings, performance
metrics, and submission checks. Include sub-universe and self-correlation results.
Include a year-by-year IS table with at least Fitness, and state whether
performance is broad-based or concentrated in specific years. `ACTIVE` / `OS`
means the alpha entered OS tracking; do not describe OS performance as known
unless OS metrics are available.

## Alternative attempts

Summarize the main alternatives tested, their results, and why they were pruned.
Emphasize lessons for descendants: what to preserve, what to mutate, and what to
avoid retrying, especially failed signs, strange constants, and fragile windows.

## Artifacts

List the files needed to inspect or reproduce the work.

<review fitness="X">
...
</review>

</template>

The alpha file body is written by the alpha proposer; the review block is written by the alpha reviewer.
