# Delta in Financial Ratios

Course: Analyst Data
Category: Data
Duration: PT5M20S
Source: VidYard
Last modified: 2023-04-28T11:34:31.373130-04:00

## Description

This video demonstrates how changes in financial ratios such as earnings per share (EPS) and price to earnings (P/E) generated from analyst estimates can be used to develop an alpha.
The four graphical results in the video starting at 04:12 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants.
The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video, we will discuss an
idea that's based on the change
in the financial ratio and uses
the analyst data.
Earnings per share or EPS
is the net earnings
a company makes
for each outstanding share of the
stock in a given period.
Net earnings are calculated after
a company disburses its
preferred stock dividends.
The estimated earnings per share
is a consensus of analyst
estimates of earnings
per share for a company.
The estimates are generally constructed
for the coming quarter, fiscal
year or the next fiscal year.
Close over the estimated earnings
per share
represents the leading price
to estimated earnings or
the P/E ratio.
This ratio tells us how
much investors are paying for
each unit of company's estimated
earnings.
This is also called the premium.
The ratio is leading because it
uses the expected earnings
for a future period.
Now let's go through our
hypothesis.
The price to earnings ratio is by
nature mean-reverting ratio.
We are capturing the weekly mean
reversion element of the ratio
by going long on the stock
whose leading P/E ratio
decreased in the previous five days
and going short on the stock whose
leading P/E ratio increased
in that period. Now
let's look at the implementation of
the idea.
This implementation uses two operators.
The rank operator and the
delta operator.
The rank operator ranks the
input argument of a stock
among all the stocks in the universe
so that the assigned value
is equally distributed between zero
and one.
The delta operator calculates the difference
between the current value of
the first argument and the value
observed n days back where
n is the second argument.
If the data value has been increasing
with time, the value returned
by the delta operator will be positive.
If the data value has been decreasing
with time the value returned will
be negative.
The back testing simulation runs
for the previous five years to
generate an Alpha vector for each
day. If the value for the stock
is negative, it shorts the stock
and goes long on the stocks with
a positive value.
For the simulation, we are
using the top 3000
U.S. stocks on the basis of
liquidity.
The maximum capital any stock can
take is 1%.
We are using the data with delay one
to prevent any look ahead-bias
and the Alpha is neutralized over
industry.
Now let's discuss how our
idea gets implemented using
the expression.
the delta operator calculates
the difference in the value of the leading
P/E ratio today and five
days back.
The negative sign before the delta
operator is used to implement
a reversion idea: A stock
whose leading price to earnings
ratio increased in the previous
five days has negative output
and vice versa. The rank operator
is used to smooth the input
value and returns an
equally distributed number between
zero and one for
all the stocks in the universe.
When we look at the results, the
Sharpe is around 1.8.
The returns-to-drawdown ratio is approximately
two and the turnover is around
40%.
Let's take a look at the detailed performance
parameters.
We have decent coverage for this
idea across this elected universe.
The PnL generated is distributed
evenly across the capitalization
groups, showing that performance
is diversified across equity
capitalizations.
The capital distribution across industries
is evenly distributed.
And finally looking at the Sharpe
across different sectors, we see
that the idea has decent predictability
across various sectors.
Now, let's see how we
can improve this idea.
This idea can be further improved
by incorporating the degree
of dispersion in the estimates
for the earnings per share data.
Also, we can incorporate
volume data to better capture
the mean reversion patterns of
the ratio.
