# Event Indicator

Course: Sentiment Data
Category: Data
Duration: PT7M10S
Source: VidYard
Last modified: 2023-04-28T11:39:51.754754-04:00

## Description

This video looks at how data can be analyzed to discover events based on sentiment volume and how an alpha can be built to try to take advantage of a corporate event using sentiment data.
The four graphical results in the video starting at 06:10 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants.
The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

We will build an Alpha
that captures an event and
uses sentiment data to take
positions on equities. With
the advent of social media, many
discussions about future stock price movements
happen on those platforms.
This activity is captured
in the social media sentiment data.
Social sentiment volume represents
the amount of discussions and
posts activity being conducted
on social media platforms.
A higher value indicates more activity.
High activity is generally observed
around a significant event for a company.
We will use this data to capture
the occurrence of an event.
Social sentiment value is a normalized
value of the sentiment derived
from social media.
This value can help us determine
whether sentiment is bearish or
bullish.
A higher value is associated with
bullish sentiment. A lower value
is associated with bearish
sentiment. This leads us to our
hypothesis: if the current
social sentiment volume of
a stock is high compared
with itself and other stocks
in the universe, it indicates
the occurrence of an event.
Using this condition and comparing
the recent social sentiment value
with the maximum sentiment
value observed in the past
quarter,
we can assign more capital to stocks
with higher values of the ratio,
indicating bullish sentiment
and lower weight to stocks, with
lower values of the ratio
indicating bearish sentiment.
Now let's look at the implementation
of the idea.
The implementation uses six operators:
the rank, group rank,
time series rank, conditional,
sum, and time
series maximum operators. The
rank operator ranks the input
argument of a stock among
all the stocks in the universe so
that the assigned value is equally
distributed between 0
and 1.
The group rank operator ranks
the second input argument
of a stock among all the stocks
in the grouping provided to the operator
as the first argument and
returns a value equally distributed
between zero and one. The
time series rank operator ranks
the first argument current value
with respect to its own values
over the preceding N days, where
N is the second argument. The
operator returns a value that's
always between zero and one.
The conditional operator is the
"if else operator" with states: if
the condition mentioned is true,
Alpha is equal to expression one,
else expression two. The
sum operator sums the input
argument value over the preceding
n days where n is
the second input argument.
This operator is mostly used
to calculate the simple average
of data over the past
n days. The time series maximum
operator returns the maximum
observed value of the first
input argument over preceding
n days where n is the second
input argument.
The back testing simulation runs
for previous five years to generate
an Alpha vector for each day.
If the value for the stock is negative,
it shorts the stock and goes
long on stocks with positive value.
For our simulation, we are using
the top 3000 US stocks
on the basis of liquidity.
The maximum capital any stock can
take is 10%.
We are using the data with the delay of
one to prevent any look
ahead bias.
The Alpha is neutralized over market.
Now let's discuss how our idea
gets implemented using the expression.
The time series rank of social
sentiment volume over the preceding
60 days gives an output
on how the sentiment volume captured
on social media has been
trending over the past quarter.
The rank operator equally
distributes
the time series rank output
for various stocks between zero
and one. Using the conditional operator,
we first identify stocks
for which there was high
social sentiment volume compared
with both themselves and other
stocks, indicating the
occurrence of an event. For these
stocks the ratio of recent
sentiment values
derived from social media
to the maximum value observed
over the past 60 days
is used to take positions.
This ratio represents the
recent sentiment strength
for the stock. Using the conditional
operator,
we first identify stocks for
which there was higher social
sentiment volume compared
with both themselves and
other stocks, indicating the occurrence
of an event. For these stocks the
ratio of recent sentiment values
derived from social media to
the maximum value observed over
the past 60 days is used
to take positions.
The ratio represents recent sentiment
strength for the stock. And finally,
we group rank this ratio over
subindustry to return an equally
distributed weight between zero
and one for all the stocks in
the subindustry. When we look at the results,
the Sharpe is around 2.2.
The return-to-drawdown ratio is approximately
2.5, and turnover is
about 25%.
Now let's take a look at the detailed performance
parameters.
We have decent coverage for this
idea.
We observe coverage oscillations
because of sentiment data values are
not available for all the stocks at
a given time.
The PnL generated is evenly distributed
across all capitalization groups,
indicating the diversification
of Alpha performance.
The capital appears to be evenly distributed
across industries,
and finally the Sharpe looks decent
across different sectors. One
potential way to improve the idea
is by specifying a data
based position for the false
case of the event condition.
We can also incorporate information
from other sentiment data fields
to further enhance the signal.
