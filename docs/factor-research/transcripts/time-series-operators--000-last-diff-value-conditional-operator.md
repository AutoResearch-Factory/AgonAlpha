# Last Diff Value Conditional Operator

Course: Time Series Operators
Category: Operators
Duration: PT5M1S
Source: VidYard
Last modified: 2023-04-28T11:23:14.653555-04:00

## Description

This video demonstrates how earnings per share (EPS) can be used to generate alphas, as well as how EPS data can be combined with current volume data to strengthen an alpha.
The four graphical results in the video starting at 03:40 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants. The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

Earnings per share
is very rich information
that can be used to develop many
different kinds of Alphas. If a stock's
earnings have increased more than
the earnings of other stocks in the
universe,
we want to go long that stock.
That's because this increase
in earnings will generate a
positive sentiment about the stock
in the market. Also, if the
short term reversion signal says
the price is going to increase,
that further strengthens our confidence
in this signal.
As we previously discussed, higher
current volume also indicates
positive sentiment about the stock.
This information can be used along
with the earning per share information
to strengthen the signal.
The simple implementation of this idea
is on your screen. As you can see,
this implementation uses two operators,
the last different value operator
and the conditional operator. The
last different value operator returns
the last different value in history.
It is especially useful for
the fundamental data. Why?
Because the values don't change frequently
for the fundamental data. The conditional
operator
is the 'if else' operator which
states:
if the condition mentioned is
true, Alpha is equal
to expression one
else the Alpha is equal to
expression 2. The backtesting
simulation runs for the previous five
years to generate an Alpha
vector for each day. If
the value for the stock is negative,
the simulator shorts the stock
and it goes long on stocks with
positive values. In the simulation
environment, we are using the
top 3000 US stocks on
the basis of the liquidity.
The maximum capital any stock can
take is 10%, and the
data is used with a delay of
one to prevent any look
ahead bias. The Alpha is neutralized
over the subindustry. Now, let's
talk about how the idea I explained
gets implemented using the expression.
The condition for the conditional operator
is true when the rank
of the ratio of current
earnings per share
to the last earnings per share value
for a stock is greater than
0.7 or
if today's volume is greater than
yesterday's volume.
This condition is true when the
change in earnings for a stock
is much higher than for the
other stocks in the universe, or
if the current day volume is higher,
than the past day volume.
If this condition is true,
the Alpha assigned to the stock
is derived from the strength of
the reversion signal as
rank of minus of
difference of the close price over
the last five days. This means
you should put more capital on
stocks whose current prices
are below their price five days
ago. The reversion is predicting
the rise in the price.
If the condition is not true, the
Alpha will be equal to -1,
which implies you should short
the stock. If we look at the results:
The Sharpe is 2.
The returns-to-drawdown ratio is
greater than 4.
And the turnover is around 45%.
If we analyze the detailed performance
parameters
we have good coverage
across the universe that we decided
to trade in the simulation settings.
The PnL is generated across
different capitalization of stocks,
which means that different cap stocks
are contributing towards the performance.
The capital is evenly distributed
across various industries, so we
do not have a concentration risk on any
particular industry,
and there is a good predictability
across various sectors which
has been represented by
the Sharpe across various sectors.
This idea can be improved either
by making the condition in the conditional
operator more predictive
of the long-short behavior
or by changing the Alpha
signal assigned when the condition
goes true. The conditional operator
is one of the most highly used operators,
so make the best use of it in
your implementation. A point to
note here is that you also
can use the conditional operator as
the nested operator so
you can call on it over and over
again within the operator
to apply multiple if else conditions.
