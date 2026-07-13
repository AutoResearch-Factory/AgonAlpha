# Inventory Turnover

Course: Fundamental Data
Category: Data
Duration: PT6M29S
Source: VidYard
Last modified: 2023-04-28T11:30:53.077182-04:00

## Description

This video demonstrates how changes in inventory over time can impact a company’s stock performance and how this can be used to generate an alpha signal. The four graphical results in the video starting at 5:09 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants. The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video,
we'll talk about an idea based
on a company's inventory turnover.
Inventory turnover is a type
of activity ratio
that captures a company's activity
on the inventory management front.
Inventory turnover is a measure
of how fast, or how many
times, a company sells through
and replaces its inventory.
It's calculated as the sales
divided by the average
inventory.
The average inventory is calculated
as the beginning inventory, plus
the ending inventory, the whole
divided by two. The speed
with which a company can sell
its inventory is a critical
measure of business performance,
because higher
inventory levels are associated
with expenses like storage
costs, insurance and deterioration.
The hypothesis is that
a stock will perform better if
the company's inventory turnover
improves over time,
and its performance will be worse
if the company's inventory turnover
worsens over time due to the
decreased efficiency and
the higher costs associated with
higher levels of inventory.
Now let's look at the implementation
of this idea.
The implementation uses two
operators,
the rank operator and the
Z-score operator.
The rank operator ranks
the input argument of a stock
among all the stocks in the universe
so that the assigned
value is equally distributed
between zero and one.
The Z-score operator returns
the Z-score of today's input
argument value over the past
N days.
The Z-score is calculated
by subtracting the mean
of input values over
the past N days from
today's input value and then
dividing the expression by
the standard deviation of input
values over the past N
days.
The operator is highly efficient
in detecting any significant
changes in the input value with
respect to its own historical
values
as it considers not only
the difference of the current value
from the mean value observed, but
also adjusts the difference
with the standard deviation of
the values seen over the look
back period.
The back testing simulation runs
for previous five years to generate
an Alpha vector for each day.
If the value for the stock is negative,
it shorts the stock and
goes long on the stocks with the positive
value. For the simulation, we
are using the top 1000
US Stocks on the basis of
liquidity.
The maximum capital any stock
can take is 10%.
We are using the data before
a particular time stamp for a day
and start trading after that
time stamp to prevent any look ahead
bias.
This is captured by using
delay zero in the settings.
The Alpha is neutralized over
industry. Now
let's discuss how our idea
gets implemented using the expression.
The time series Z-score
operator computes the
Z-score of the current inventory turnover
using the inventory turnover
values observed over
the past 240 days.
A relatively low inventory
turnover implies weak
sales and therefore excess
inventory.
A relatively high ratio implies
either strong sales or
less inventory, and we would
want to long that stock relative
to others. A company with
increasing inventory turnover
will have a higher Z-score
and get more capital allocated
to its stock,
vice versa for a company with a
decreasing inventory turnover.
The reason 240
days is chosen as a parameter
in the Z-score operator is
that it represents approximately
the total number of trading days in
a year.
The rank operator smooths
the value returned by the Z-score operator
across all the stocks in
the universe and returns a
value equally distributed
between zero and one.
This helps prevent us from assigning
too much weight to a small
set of stocks. When we look
at the results, the Sharpe ratio
is around 2.5.
The returns-to-drawdown ratio
is approximately five,
and the turnover is about 6%.
When we analyze the detailed performance
parameters,
we have decent coverage for the idea
across the selected universe.
We observe coverage oscillations
because inventory turnover data
values are updated only
on a quarterly basis.
The PnL generated across
different capitalization groups is
also good,
which means performance has
been derived from various
equity capitalizations. The
capital distribution across industries
is evenly distributed.
And finally, if you look
at the Sharpe across sectors,
the idea has decent predictability
across the various sectors. Now
let's talk about the potential ways
to improve the idea.
This idea could be improved
by combining the inventory
turnover data with the other
fundamental information to incorporate
the impact of the other company
level information while deciding
the long short positions.
Data on earnings and the cost
of goods may also help
improve this idea.
