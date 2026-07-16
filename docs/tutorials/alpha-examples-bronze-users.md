# ⭐ Alpha Examples for Bronze Users 🥉

Source: https://platform.worldquantbrain.com/learn/documentation/create-alphas/sample-alpha-concepts
Access level: Bronze

## Table of Contents

1. [Valuation based on cash flow](#valuation-based-on-cash-flow)
2. [Overpriced stocks](#overpriced-stocks)
3. [Volatility arbitrage](#volatility-arbitrage)

## Valuation based on cash flow

### Hypothesis

A lower EV/CF usually suggests the company is becoming cheaper relative to its cash-generating ability; a higher multiple suggests it’s getting more expensive.

### Implementation

Use `ts_zscore` to standardize the change of the ratio and `group_rank` to control turnover.

### Hint to Improve Alpha

There are various types of cash flow, and switching the type used in the metric may improve its performance.

### Alpha expression

```text
group_rank(-ts_zscore(enterprise_value/cashflow, 63),industry)
```

### Simulation settings

| Region | Universe | Language | Decay | Delay | Truncation | Neutralization | Pasteurization | Lookback | Max Trade | Max Position |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| USA | TOP3000 | Fast Expression | 0 | 1 | 0.08 | Industry | On | — | OFF | OFF |

## Overpriced stocks

### Hypothesis

When analyst price target estimates (`est_ptp`) and free-cash-flow estimates (`est_fcf`) move highly in sync over the past month (high positive correlation), it may signal that the market has already fully priced cash-flow expectations into price targets, leaving little room for further upside.

### Implementation

Use `est_ptp` to capture price estimates and `est_fcf` to capture free cash flow, then calculate their dynamics with `ts_corr`.

### Hint to Improve Alpha

The window of one year might be too long to react to the price correction. Try a shorter window.

### Alpha expression

```text
-ts_corr(est_ptp,est_fcf,252)
```

### Simulation settings

| Region | Universe | Language | Decay | Delay | Truncation | Neutralization | Pasteurization | Lookback | Max Trade | Max Position |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| USA | TOP3000 | Fast Expression | 0 | 1 | 0.08 | Market | On | — | OFF | OFF |

## Volatility arbitrage

### Hypothesis

Higher volatility is often observed during bearish markets, while lower volatility is typically seen during bullish markets. A lower Parkinson's volatility coupled with a higher implied volatility may suggest stronger bullish sentiment for the stock in the future.

### Implementation

Go long when implied volatility significantly exceeds historical volatility, and short in the opposite case.

### Hint to Improve Alpha

Can you use `ts_backfill` to avoid missing data on certain days?

### Alpha expression

```text
implied_volatility_call_120/parkinson_volatility_120
```

### Simulation settings

| Region | Universe | Language | Decay | Delay | Truncation | Neutralization | Pasteurization | Lookback | Max Trade | Max Position |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| USA | TOP200 | Fast Expression | 0 | 1 | 0.08 | Sector | On | — | OFF | OFF |
