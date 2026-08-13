# Local evaluator contract

Copy this file to `references/evaluator.md` and replace every placeholder before running a search. The copied file is intentionally ignored by Git so deployment-specific endpoints, datasets, credentials, and research artifacts stay local.

## Research scope

- Market and instrument universe: `<describe>`
- Available date range: `<describe>`
- Permitted datasets: `<describe>`
- Expression syntax or strategy interface: `<describe and link to local documentation>`
- Prohibited inputs and leakage rules: `<describe>`

## Evaluation interface

Document an executable, non-interactive command or API wrapper that accepts a candidate expression and configuration. Include:

- exact invocation;
- input and output schemas;
- timeout and retry behavior;
- required environment variables, without putting secret values in this file;
- where raw requests, responses, logs, and run identifiers must be saved under the candidate work directory.

## Fitness

Define a single finite numeric `Fitness` value to maximize. Specify the formula, units, valid range, treatment of failed evaluations, and whether sign reversal is equivalent.

## Acceptance checks

List every required check for a final candidate, including statistical, operational, and policy constraints. State how each check is executed and what constitutes a pass.

## Finalization authorization

State whether the agent may perform a local-only finalization step. External submission, publication, deployment, or messaging must remain disabled unless explicitly authorized here.
