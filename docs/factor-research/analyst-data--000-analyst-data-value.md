# Analyst Data Value

Course: Analyst Data
Category: Data
Duration: PT5M17S
Source: VidYard
Last modified: 2023-04-28T11:33:25.404503-04:00

## Description

The video demonstrates how an alpha can be generated based on analysts’ estimate of earnings per share (EPS) and how combining this ratio with estimates such as the sales per share ratio can improve an alpha.
The four graphical results in the video starting at 04:03 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants. The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video,
we will discuss an idea based
on an analyst data value,
which is the estimate
of the earnings per share. This
is a consensus analyst estimate.
Earnings per share represents the
amount of net income a company
generates per share.
It indicates a company's
profitability. Earnings per share
is calculated by dividing
the net income after the distribution
of dividends on preferred
stock by the average number
of outstanding shares over
a period.
The estimate of earnings per share
by the close price represents
the amount of estimated profit
a company will generate in the future
for each outstanding share
at the current stock price.
The higher the number, the more
attractive stock is to buy and
vice versa. The estimate value
makes this ratio forward looking
and helps us generate an Alpha
based on this ratio.
Our hypothesis is, if
a company's estimated earnings per
share by the close ratio
is improving with time,
the higher ratio indicates higher
return potential for the stock,
and it's likely that the stock
prices will increase. However,
if the ratio is decreasing with
time due to decreased return
potential, the stock price might
decrease. Now, let's look
at the implementation of the idea.
The implementation uses two operators,
the rank operator and
the time series rank operator. The
rank operator ranks the
input argument of stock
among all the stocks in the universe
so that the assigned
value is equally distributed
between zero and one.
The time series rank operator
ranks the first argument value
with respect to its own values
over the past N days,
where N is the second argument.
And the operator returns the rank
of the current value and the value
lies between zero and one.
The backtesting simulation runs
for the previous five years to
generate an Alpha vector for each
day. If the value for the
stock is negative, it shorts
the stock and goes long
on stocks with positive values.
For this simulation, we are using
the top 3000 US stocks
on the basis of liquidity.
The maximum capital any stock can take
is 10%.
We are using the data with the Delay-1
to prevent any look ahead
bias,
and the Alpha is neutralized over subindustry.
Now let's
talk how our idea gets implemented
using the expression.
The time series rank operator
compares the current value
of the estimated earnings per
share by close with the
values over the past 40
days. If the stock price decreases
or the estimated earnings per
share of the stock is revised
to a higher value, the ratio
will increase.
The increased ratio will result
in higher values being assigned by
the time series rank operator.
The duration of 40 days represents
a two-month trading period. Now
the rank operator smooths the value
returned by the time series rank
operator
so that the output values are
equally distributed between zero
and one for all the stocks
in the universe. When we look at the
results,
the Sharpe is around 1.9,
the returns-to-drawdown ratio is approximately
two, and turnover is about 40%.
When we analyze the detailed performance
parameters,
we have decent coverage for this idea
across the selected universe.
The PnL generated is decently
distributed across all the
capitalization groups.
The capital distribution across
industries
is also even,
and finally, if you look at the Sharpe
across the different sectors,
this idea has decent predictability
across various sectors.
Now let's talk about the potential
ways to improve the idea.
This idea could be improved by
combining the estimate value
of earnings per share with
the other estimate the analysts have
provided. This will help us incorporate
more information about the market
consensus values. For example,
we can use the estimate sales
per share value,
which could be combined with this
existing ratio to capture more
insights about companies expected
business performance on the revenue
front.
