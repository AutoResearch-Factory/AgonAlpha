# Sentiment Strength

Course: Sentiment Data
Category: Data
Duration: PT5M33S
Source: VidYard
Last modified: 2023-04-28T11:40:35.382446-04:00

## Description

This video explains how a stock’s sentiment strength can affect its price and how this signal may be used to create an alpha. The video is purely for instructional purposes; the data is not supported. Please use the video solely as a source of ideas.
The four graphical results in the video starting at 04:18 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants.
The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video,
we will build an Alpha based on the
stocks sentiment strength.
When there's bullish sentiment,
most investors expect
upward price movement.
When sentiment is bearish,
most investors expect
prices to move downward.
The bearish sentiment data field has
its value high when prices
are in a downtrend.
Similarly, the bullish sentiment
data field has its value
high when prices are moving
up. The sentiment
volumes indicate how much information
about the stock, such as discussions,
posts and news
is flowing in the market. Higher
sentiment volume indicates a
stronger sentiment value
signal because more
market participants might be involved
in the discussions. The ratio
of bullish sentiment to bearish
sentiment data field is a proxy
of overall market sentiment.
When the value of this ratio is
greater than one, bullish
sentiment dominates the market.
With values less than one, the
market is dominated by bearish
sentiment.
This leads us to our hypothesis:
when the ratio of bullish sentiment
to bearish sentiment in the market is
high
and the sentiment volumes captured
on social media are also
rising, the stock prices
might increase.
Along the same lines, when there are
low values of both the ratio
and social sentiment volumes,
stock prices might fall.
Now let's look at the implementation
of the idea.
The implementation uses two
operators:
The group rank operator and
the time series rank operator.
The group rank operator ranks
the second
input argument of a stock
among all the stocks in the grouping
provided to the operator as
the first argument
and returns a value equally
distributed between zero
and one. The time series rank
operator ranks the first
argument current value with
respect to its own values
over the preceding n days,
where n is the second argument.
The operator always returns
a value that's between zero
and 1.
The backtesting simulation runs
for preceding five years
to generate an Alpha vector
for each day.
If the value for the stock
is negative, it shorts the
stock and goes long on
stocks with positive values.
For the simulation, we are using
the top 3000 US stocks
on the basis of liquidity.
The maximum capital any stock
can take is 10%.
We are using the data with the delay-1
to prevent any look ahead bias.
The Alpha is neutralized over the
market.
Now let's discuss how our idea
gets implemented using
the expression.
The ratio of bullish sentiment
to bearish sentiment value
captures the overall sentiment
of a stock.
The group rank operator
ranks this ratio among all
the stocks in the group
market and assigns
a number equally distributed
between zero and one.
The time series rank
of the social sentiment volume
Over the past 254
days
returns a number between zero
and one,
based on how the sentiment
volume capture on social
media has trended over
the year.
254 days represent the
number of trading days in a year. When
we look at the results,
the Sharpe is around 1.9.
The returns-to-drawdown ratio is
approximately three and turnover
is around 35%.
And when we analyze the detailed performance
parameters, we have decent coverage
for this idea across the selected
universe.
The increase in Alpha coverage
with time is due to the increase
in coverage of sentiment data over
time. The PnL
generated is fairly well
distributed across all
the capitalization groups, with
slightly more performance derived
from mid cap and small cap
stocks.
Capital is evenly distributed
across industries
and finally, the Sharpe across
various sectors looks decent
as well. Now the potential ways
of improving the idea
include
checking to see if the higher sentiment
volume is resulting in
higher trading activity or
trading volume. Also, we
can strengthen our signal by
using this sentiment value derived
from social media to further
diversify the sources of
our sentiment strength signal.
