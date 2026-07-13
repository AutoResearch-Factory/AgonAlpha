# General Idea Using Analyst Estimates

Course: Analyst Data
Category: Data
Duration: PT7M8S
Source: VidYard
Last modified: 2023-04-28T11:36:14.717551-04:00

## Description

This video demonstrates how to generate an alpha idea using inventory levels as a proportion of total assets, as well as inventory turnover.
The data fields  and  at <2:44> are only available to consultants, not users. Users can instead use the data fields  and .
The four graphical results in the video starting at 5:41 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants.
The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video,
we will talk about building an Alpha
based on inventory levels
as a proportion of total assets,
and we will evolve it using inventory
turnover of the stock. It's
important to analyze the ratio of inventory
value to total assets.
Because higher values
of this ratio can be a problem
for a company, it can
result in cash flow troubles or
higher expenses due to the
cost of carrying inventory.
Goodwill is the value associated
with the company, for example, brand
value, which is not captured
on a company's balance sheet but is paid
when a company is acquired.
We remove the estimate of goodwill
from the estimate of total
assets because goodwill
is an intangible asset that
isn't directly used to build
inventories for the business.
Also, because goodwill's value
is not frequently tested for
impairment, there's a possibility
that its relation to total assets
can be manipulated.
Inventory turnover measures
how fast, or how many times,
a company sells through and
replaces its inventory. The
speed with which a company sells
its inventory is a critical
performance measure because
higher inventory levels are associated
with higher expenses
such as storage costs,
insurance,
and deterioration.
Inventory turnover is calculated
as sales divided by
average inventory.
Where, average inventory is calculated
as beginning inventory plus
ending inventory, the whole divided by 2.
Higher
ratio levels, are associated with
higher operational efficiency. Our
hypothesis is that a company
with an increasing ratio of inventory
to the total estimate of assets,
adjusted for the total estimated
goodwill, should result
in inefficiencies
and eventually be reflected
in poor stock price performance.
However, if the company's inventory
turnover is increasing over
time, the adverse affect
due to former ratio is mitigated
because the company can still
efficiently manage its inventory.
Now let's look at the implementation
of the idea.
The implementation uses two
operators,
the rank operator and the
time series rank operator.
The rank operator ranks
the input argument of the stock
among all the stocks
in the universe so that
The assigned value is equally
distributed between zero
and 1.
The time series rank operator
ranks the first argument value
with respect to its own values
over the past 10 days, where
N is the second argument.
This operator returns the
rank of the current value and the
value is distributed between zero
and 1.
The back testing simulation
runs for the previous five years
to generate an Alpha vector for
each day. If the value
for the stock is negative, it shorts
the stock and goes long on
stocks with a positive value. For
the simulation we are using the top
3000 US stocks on the basis
of liquidity.
The maximum capital any stock can take
is 1%.
We are using the data with the Delay
one to prevent any look ahead bias
and the Alpha is neutralized
over industry.
Now let's talk
about the implementation of this
idea using the expression.
The time series rank of inventory
to the estimated total assets,
adjusted for estimated goodwill,
captures the performance of the ratio
with respect to its own values over
the past three months.
A similar process takes place
for the inventory turnover ratio.
The rank operator then smoothes
the value returned by the time
series rank operator and returns
an equally distributed number
between zero and one for
all the stocks in the universe.
Finally,
we multiply the two expressions
to get the combined output for each
stock.
In the first expression for
companies with rank output
of less than 0.5,
which represents the lower inventory
to total assets ratio, we take
a long position
and vice versa.
We strengthen our signal by
multiplying it with the second expression,
capturing the variation of
inventory turnover over time
so that a company with
decreasing inventory to total assets
ratio
and increasing inventory turnover
gets higher capital assigned to
it and vice versa.
When we look at the results, the
Sharpe is around 1.7.
The returns to drawdown ratio is approximately
three,
and turnover is around 15%.
Now let's take a
look at the detailed performance parameters.
We have a decent coverage for this idea.
We observe coverage oscillations
because the analyst and
fundamental data values are updated
less frequently and aren't
available for all the stocks at a given
time. Looking at the PnL
distribution across all stocks
capitalization groups,
we find it is evenly distributed
and well diversified.
The capital distribution across industries
looks evenly distributed as well,
and finally looking at the Sharpe
across the different sectors, we observe
that the idea has decent predictability
across various sectors.
Now let's discuss how
we can improve this idea.
potential ways to improve the idea
include investigating the company's
operating cash flow
and checking its performance with
respect to time along
with the inventory levels.
Also, we can add other
analysts data to capture
the company's performance on other
parameters such as liquidity
and profitability,
so these ideas can potentially help
us improve the performance
of this Alpha.
