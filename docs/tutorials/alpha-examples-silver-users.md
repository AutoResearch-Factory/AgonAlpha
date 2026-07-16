# ⭐ Alpha Examples for Silver Users🥈

Access level: Silver

## Table of Contents

1. [Implied Volatility Spread as a predictor](#implied-volatility-spread-as-a-predictor)
2. [6-Month Call–Put Volatility Skew](#6-month-callput-volatility-skew)
3. [5-Day Peer vs. Stock Performance Gap](#5-day-peer-vs-stock-performance-gap)
4. [Investing for the Future](#investing-for-the-future)
5. [Free Cash Flow Quality and Inventory Efficiency Signal](#free-cash-flow-quality-and-inventory-efficiency-signal)
6. [Bull Trap](#bull-trap)

## Implied Volatility Spread as a predictor

### Hypothesis

If the Call Open interest is higher than the Put Open interest, the stock may rise based on the intensity of the implied volatility spread or vice versa.

### Implementation

Use 'trade_when' operator, with condition on the call-put open interest ratio. If it is less than unity, go long on stock based on intensity of the (Implied Volatility) IV spread, using option data.

### Hint to improve the Alpha

Can using custom neutralization on the Alpha based on self-created groups (like historical volatility) help improve sub-universe performance? Use floor or bucket operator combined with rank operator to implement custom neutralization

### Alpha expression

```text
trade_when(pcr_oi_270 < 1, (implied_volatility_call_270-implied_volatility_put_270), -1)
```

### Simulation Settings

| Region | Universe | Language | Decay | Delay | Truncation | Neutralization | Pasteurization | Lookback | Max Trade | Max Position |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| USA | TOP3000 | Fast Expression | 4 | 1 | 0.08 | Market | On | — | OFF | OFF |

## 6-Month Call–Put Volatility Skew

### Hypothesis

When call implied volatility is higher than put implied volatility relative to average ATM volatility, options traders may be more focused on upside moves than downside risk, indicating bullish sentiment.

### Implementation

Take the ratio of the difference between 6‑month call implied volatility and 6‑month put implied volatility over the 6‑month mean implied volatility and prefer stocks with higher values.

### Hint to improve the Alpha

Preprocess data with ts_backfill() to pass the Weight Test. Also, the turnover is too high, can you come up with ideas to reduce it?

### Alpha expression

```text
(implied_volatility_call_180- implied_volatility_put_180)/implied_volatility_mean_180
```

### Simulation Settings

| Region | Universe | Language | Decay | Delay | Truncation | Neutralization | Pasteurization | Lookback | Max Trade | Max Position |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| USA | TOP3000 | Fast Expression | 0 | 0 | 0.08 | Subindustry | On | — | OFF | OFF |

## 5-Day Peer vs. Stock Performance Gap

### Hypothesis

If peers have done much better than the stock, the stock may be a short-term laggard that could mean-revert up

### Implementation

Comparing the 5-day cumulative return of peer group to the 5-day cumulative return of the stock

### Hint to improve the Alpha

When the gap is small and volatile, the signal may trade too much. Can you use trade_when to execute trades only when the gap is significant?

### Alpha expression

```text
cum_rel_return = (1+ts_delay(rel_ret_all,4))*(1+ts_delay(rel_ret_all,3))*(1+ts_delay(rel_ret_all,2))*(1+ts_delay(rel_ret_all,1))*(1+rel_ret_all);
cum_return = (1+ts_delay(returns,4))*(1+ts_delay(returns,3))*(1+ts_delay(returns,2))*(1+ts_delay(returns,1))*(1+returns);
cum_rel_return -cum_return
```

### Simulation Settings

| Region | Universe | Language | Decay | Delay | Truncation | Neutralization | Pasteurization | Lookback | Max Trade | Max Position |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| USA | TOP3000 | Fast Expression | 0 | 1 | 0.08 | Sector | On | — | OFF | OFF |

## Investing for the Future

### Hypothesis

The firms those invest more and more to the long-term may get more profit in the future than those who do not thus we should long them

### Implementation

Use fnd6_newqv1300_ivltq as the long-term investment measure. Backfill it over 60 days and sum over 252 days to create a rolling yearly long-term investment series.

Run ts_regression( … , ts_step(1), 756, rettype = 2) over 3 years with ts_step(1) as the time variable; this extracts the trend of yearly long-term investment.

### Hint to improve the Alpha

Can you boost performance by adding more weight to firms that also have recently increasing revenue?

### Alpha expression

```text
ts_regression(ts_sum(ts_backfill(fnd6_newqv1300_ivltq,60),252),ts_step(1),756,rettype = 2)
```

### Simulation Settings

| Region | Universe | Language | Decay | Delay | Truncation | Neutralization | Pasteurization | Lookback | Max Trade | Max Position |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| USA | TOP3000 | Fast Expression | 0 | 1 | 0.08 | Subindustry | On | — | OFF | OFF |

## Free Cash Flow Quality and Inventory Efficiency Signal

### Hypothesis

Companies with persistently high estimated operating cash flow relative to their capital expenditure are expected to outperform. This reflects superior free cash flow generation, which the market tends to reward with higher valuations over time.

### Implementation

Using est_cashflow_op - est_capex as Proxy for Free Cash Flow quality then normalize across time series (252-day window) and smooth signal with ts_decay.

### Hint to improve the Alpha

When those same companies also show a dramatic improvement in inventory turnover (>50% better than a year ago), the signal is amplified — suggesting accelerating business momentum.

### Alpha expression

```text
ts_decay_linear(ts_scale(est_cashflow_op,252),22)-ts_decay_linear(ts_scale(est_capex,252),22)
```

### Simulation Settings

| Region | Universe | Language | Decay | Delay | Truncation | Neutralization | Pasteurization | Lookback | Max Trade | Max Position |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| USA | TOP3000 | Fast Expression | 2 | 1 | 0.08 | Industry | On | — | OFF | OFF |

## Bull Trap

### Hypothesis

When the multi-day slope of first-minute reactions is deteriorating but a large up-spike occurs today, it flags potential trap.

### Implementation

Compute the 5‑day slope of first‑minute news reactions using ts_regression on news_pct_1min with rettype =2, then multiply the negative of the recent max post‑news upside return by the absolute value of this slope. Finally, winsorize the result with std = 4 to normalize extreme values and use it to flag potential bull traps.

### Hint to improve the Alpha

Try to improve turnover.

### Alpha expression

```text
slope = ts_regression(ts_backfill(news_pct_1min,60), ts_step(1), 5, rettype=2);
winsorize(-ts_backfill(news_max_up_ret,60) * abs(slope),std = 4)
```

### Simulation Settings

| Region | Universe | Language | Decay | Delay | Truncation | Neutralization | Pasteurization | Lookback | Max Trade | Max Position |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| USA | TOP3000 | Fast Expression | 0 | 1 | 0.08 | Industry | On | — | OFF | OFF |
