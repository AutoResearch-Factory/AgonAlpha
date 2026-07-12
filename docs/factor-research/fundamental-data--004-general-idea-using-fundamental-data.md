# General Idea Using Fundamental Data

Course: Fundamental Data
Category: Data
Duration: PT5M42S
Source: VidYard
Last modified: 2023-04-28T11:32:39.216595-04:00

## Description

This video explains how fundamental ratios such as inventory turnover and cost of goods sold, property, plant and equipment can impact a stock’s performance and how these ratios can be  combined to strengthen an alpha signal. The four graphical results in the video starting at 04:22 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants. The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video,
we will talk about an idea
that combines two fundamental ratios
that capture different aspects
of a company's business activity.
The first ratio, as shown
on your screen, is the cost
of goods sold, divided by
property, plant, and equipment.
This ratio captures how efficiently
a company uses it's fixed
assets to generate the goods
that are used for business activities.
The second ratio is inventory
turnover, which measures
how fast, or how many times
a company sells through and
replaces its inventory.
The speed with which a company can sell
its inventory
is a critical measure of business
performance because higher
inventory levels are associated
with higher expenses such
as storage costs, insurance
and deterioration. Inventory
turnover is calculated as
sales divided by average
inventory, where average inventory
is calculated as beginning inventory
plus ending inventory, divided
by two. A higher ratio is associated
with higher operational efficiency.
This brings us to our idea:
if a company's cost of goods sold
divided by
the property, plant, and equipment
ratio
and the inventory ratio
are improving with time, it's
likely that the stock prices will increase.
If both the ratios decrease
with time, the company's stock
price might decrease. Now
let's look at the implementation of
this idea.
The implementation uses two operators:
the rank operator
and the time series rank
operator.
The rank operator ranks the
input argument of a stock
among all the stocks in the universe
so that the assigned
value is equally distributed
between 0 and 1.
The time series rank operator
ranks the first argument
value
with respect to its own values
over the past N days, where
N is the second argument, the
operator returns the rank
of the current value
and the values lie between 0
and 1.
The backtesting simulation runs
for the previous five years
to generate an Alpha vector for
each day.
If the value for the stock is negative,
it shorts the stock and
goes long on stocks with a positive
value. For the simulation we are using
the top 3000 US stocks
on the basis of liquidity.
The maximum capital any stock can
take is 1%.
We are using the data with the delay
of one
to prevent any look-ahead bias
and the Alpha is neutralized
over subindustry.
Now let's talk about
how our idea gets implemented
using the expression.
The time series rank operator
compares the current value
of the ratio of the cost
of goods sold to the cost
of property, plant and equipment
with its past values over
the last 240
days. If the ratio has been
improving,
the value returned by the operator
is high and vice versa.
The same happens with the inventory
turnover ratio. The rank operator
smooths the value returned by
the time series rank operator so
that the output values are
equally distributed between zero and
one. Finally,
we combine the two ratios
to capture the information
contained in both the ratios and
strengthen the overall signal by
multiplying them as shown in the expression.
When we look at the results,
the Sharpe is around 1.8
the returns-to-drawdown ratio is approximately
3.5 and turnover
is around 7%.
Now let's analyze the detailed
performance parameters.
We have decent coverage for this idea
across the selected universe.
We observe coverage oscillations
because the fundamental data values
are updated only on a quarterly
basis and aren't available
for all the stocks at a given time.
The PnL generated across different
capitalization groups is also
good, which means performance
is diversified across various
equity capitalizations. The capital
distribution across industries is
evenly distributed,
and finally, this idea has
a decent Sharpe across various
sectors, representing
that we are deriving performance from
various sectors.
Now let's talk about the potential
ways to improve the idea.
This idea could be improved by
combining more fundamental
ratios to capture other
aspects of company's business
performance.
So, for example, you can use the profitability
ratios. Also, we
can use various technical indicators
as entry exit points
for trading the stocks.
