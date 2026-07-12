# Getting Started with Option6 Implied volatility (IV)

Source: https://platform.worldquantbrain.com/learn/documentation/understanding-data/getting-started-option6-implied-volatility-iv
Last modified: 2026-06-15T23:55:25.566566-04:00

Option6 Implied volatility (IV) is one of the most studied numbers in equity markets. But it is also closely tied to its own past. The interesting questions in vol research are rarely "what is IV today?". They are "what does the shape of the surface tell us?", "what does the model think IV could be in 20 days?", and "how sure is the model in that view?".

The Option6 dataset is built around those questions.

## Dataset Highlight

The Option6 dataset sits under the Option category > Option Volatility subcategory.

- Data Type: MATRIX only

- Delays: 0 (131 Fields) and 1 (133 Fields)

- Universes: TOP3000, TOP500, TOP200, TOP1000, TOPSP500, TOP2000

- Coverage: 95% on USA/D1 and 97% on USA/D0

## Dataset Feature

The Option6 fields fall into six families. Knowing which family a field belongs to is the most useful thing you can do before building an Alpha.

### Constant-Maturity Implied Volatility

he IV surface is interpolated to fixed tenors. The at-the-money level is then published. The main fields are opt6_30div (short-dated constant-maturity implied volatility; the field name says "30" but the underlying window is 20 days - use it as your short-dated anchor) and opt6_vimta3m (at-the-money implied volatility for options expiring in the third calendar month). A 1-month range percentile, opt6_ivpctile1m, is also published. These series move slowly by construction. The interpolation acts as a filter. So they behave like macro-style data. Time-series operators on a quarter window tend to work better than short-window deltas.

### Volatility Surface Shape (Skew, Slope, Curvature)

The IV surface is parameterized as a level, a slope (skew across strikes), and a derivative (curvature). The slope cluster comes pre-aggregated. You get opt6_slopeavg1m and opt6_slopeavg1y (rolling averages), opt6_slopestd1y (its yearly dispersion), opt6_slopepctile (one-year percentile rank), and opt6_slopeinf (the implied infinite slope). For curvature you get opt6_derivinf (the implied derivative of the surface extrapolated to the infinite-strike limit) and opt6_vired, which measures how quickly the vol smile tilts as you move away from at-the-money toward out-of-the-money calls. A large opt6_vired means the smile bends sharply; a small one means it is nearly flat. The slope captures the demand for downside puts versus upside calls. The derivative captures the demand for tail risk versus body. These shape signals are richer than raw IV. They tend to mean-revert at the sector level.

### Forecast Family

This is the defining feature of the dataset. It carries 20-day forward forecasts of both historical realized volatility and implied volatility, plus the goodness of fit of those forecasts. Fields with fcst in the name belong here. Two key ones are opt6_2rtscf (R-squared of the 20-day realized-volatility forecast - how well the model predicted where realized vol landed) and opt6_fcstr2imp (R-squared of the implied-volatility forecast - how well the model predicted where implied vol landed 20 days later). The R² fields are not directional. They are confidence signals. A stock whose forecast R² has been steady and high is a stock where the options model is "in regime" and signals from this dataset carry more weight. That makes them ideal trade_when gates.

### Earnings-Effect Series

A real strength of this dataset is that many series come in both "with earnings" and "ex-earnings" variants. opt6_impliediee is the market-implied earnings effect. It is solved from a term-structure equation where the earnings effects adjust the months affected by earnings. opt6_absavgernmv is the average percentage absolute stock-price move tied to the next earnings announcement. opt6_lastern gives the date of the last earnings release. (Note: opt6_nexterntod and opt6_lasterntod are flagged as deprecated in the field descriptions - avoid them.) These are options model inputs computed continuously from the live option surface, not sparse event-driven fields. They do not need aggressive backfilling - a short ts_backfill of 5 days is enough to handle the occasional missing day

### Dividend Cluster

Often overlooked. The dataset publishes the annualized dividend yield (opt6_divyield), the dividend frequency (opt6_divfreq), and the dividend amount (opt6_divamt) as inputs to the options pricing engine. These are really fundamental data riding inside an options dataset. They are less crowded than the equivalent fields in pure fundamental datasets. The dividend group is one of the most rewarding starting points in the dataset.

### Cross-Asset Ratios

For most key metrics, the dataset publishes the ratio against SPY and the ratio against the matched sector ETF, along with 1-month and 1-year averages of those ratios. The fields share an iv...ratio... pattern: opt6_ivspyratio, opt6_ivspyratioavg1y, opt6_ivetfratio, opt6_ivetfratioavg1m. Pair correlations like opt6_correlspy1m and opt6_correletf1y go with them. Using a ratio field means the cross-asset adjustment is already done for you. Then neutralizing such a signal at the market level is often cleaner than at the sector level.

## Usage Advice

- Backfill sparingly. Option6 fields update continuously from the live option surface, so long backfill windows introduce stale option pricing assumptions. A short ts_backfill of 5 days is enough to handle occasional missing days. The interpolated IV fields and forecast R² fields are dense and need no backfill at all.

- Neutralization. We recommend Market or Sector for option datasets. As a rule, signals built on raw vol-surface fields (slope, IV level, derivative) benefit from Sector neutralization, since volatility is priced sector by sector. Signals built on the *ivspyratio* or *ivetfratio* fields already have the market exposure removed. So Market neutralization is the cleaner pair.

- Watch the timescales. The constant-maturity IV fields and the ratio averages (avg1m, avg1y) are already smoothed. A ts_mean on top is redundant. Prefer ts_delta, ts_av_diff, or ts_zscore over windows on the order of a quarter. Asking "what changed in the last 5 days?" mostly measures noise on these series. Asking "where does today sit relative to the last 60 days?" measures signal.

- Be cautious with ts_corr between two Option6 fields. Many fields are mechanically related. IV is anchored to HV. Slope is bounded by surface shape. Correlations between them tend to capture the dataset's internal structure rather than any real cross-asset behaviour. Prefer ts_regression(..., rettype=0) to extract the residual part. Or take the standardized spread: subtract(ts_zscore(X, 60), ts_zscore(Y, 60)).

- Use forecast confidence as a filter. Stocks with steadily high opt6_fcstr2imp over the last quarter are stocks where the volatility model is "in regime". Many soft signals improve sharply when gated by trade_when(ts_mean(opt6_fcstr2imp, 60) > 0.5, signal, -1). This is a quiet but powerful technique.
