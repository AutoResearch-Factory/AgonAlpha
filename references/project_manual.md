# AutoAlpha Manual

## Run layout

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

## One sentence

State the proposed alpha in one sentence, using LaTeX syntax for the formulae.

## Motivation and explanation

## Performance

## Artifacts

<review fitness="X">
...
</review>

</template>

The alpha file body is written by the alpha proposer; the review block is written by the alpha reviewer.
