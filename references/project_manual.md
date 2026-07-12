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

## Alpha file format

<template>

# Alpha Report: <slug>

## One sentence

State the proposed alpha in one sentence, using LaTeX syntax for the formulae.

## Motivation and explanation

Explain the intuition behind the alpha and the role of each component in its formula.

## Performance

Report the final alpha's simulation settings, performance metrics, and submission checks.

## Alternative attempts

Summarize the main alternatives tested, their results, and why they were pruned.

## Artifacts

List the files needed to inspect or reproduce the work.

<review fitness="X">
...
</review>

</template>

The alpha file body is written by the alpha proposer; the review block is written by the alpha reviewer.
