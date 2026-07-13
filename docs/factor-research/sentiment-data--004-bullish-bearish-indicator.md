# Bullish & Bearish Indicator

Course: Sentiment Data
Category: Data
Duration: PT5M59S
Source: VidYard
Last modified: 2023-04-28T11:41:27.776887-04:00

## Description

This video looks at how bullish and bearish sentiment on stocks can be used to generate an alpha and how various operators can be used to further develop an alpha. The video is purely for instructional purposes; the data is not supported. Please use the video solely as a source of ideas.
The four graphical results in the video starting at 5:02 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants.
The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video,
we will talk about a sentiment data
based indicator
and use it to build an Alpha.
Sentiment data represents investors'
overall feeling about the future
price trend of a security.
When investors sentiment is high,
it's very likely, due to excessive
buying, a security becomes
overpriced.
If sentiment is very
low due to excessive selling, a
security can become underpriced.
The amount of discussion, posts
and comments investors make
about a security on social
media platforms
determine the volume of sentiment
data derived from social
media. This data
can be important to us because
enhanced investor activity
is often followed by reversals
of price trend. This leads
us to our hypothesis.
If the sentiment surrounding a stock
is high, then the stock
price is likely to decrease
in the future because of overpricing.
Similarly, if the sentiment for a
stock is low, then its price
should rise in the future because
of underpricing.
Now let's look at the implementation
of the idea.
The implementation uses three operators:
the rank,
time series minimum, and
time series maximum operators.
The rank operator ranks the input
argument of a stock among
all the stocks in the universe so
that the assigned value is equally
distributed between zero
and one.
The time series minimum operator computes
the minimum value of the first
input argument observed
over the preceding n days, here
n is the second argument to the operator.
The time series maximum operator
computes the maximum value
of the first input argument observed
over the preceding n days,
here n is the second input
argument to the operator. The
backtesting simulation runs
for previous five years to generate
an Alpha vector for each day.
If the value for the stock is negative,
it shorts the stock
and goes long on stocks with a positive
value. For
the simulation, we are using the top
2000 US stocks on the basis
of liquidity.
The maximum capital any stock can take
is 1%.
We are using the data with the
Delay-1 to prevent any look
ahead bias.
The Alpha is neutralized over the market.
Now let's discuss how our
idea gets implemented using
the expression.
The overall sentiment is calculated
by subtracting the bearish
sentiment value from the bullish
sentiment value in the first expression.
The resulting value is assigned
to variable Y.
This technique of assignment is used
to keep an Alpha expression
neat. The variable Y,
which represents overall sentiment,
is then used to compute
our Alpha expression. The minimum
value of the overall sentiment, or
Y, is computed over the
preceding 10 days using
the ts_min operator.
The maximum value is computed
using the ts_max operator.
Next, we subtract the minimum
value of Y from its current
value and divide the resulting
expression by the range
of maximum and minimum
values of Y observed over
the preceding 10 days. The resulting
expression helps us gauge
where the overall sentiment levels exist
with respect to the maximum
minimum range created. If the
current value is the maximum
value observed over the preceding
10 days, then the value returned
by the expression would be one.
If the current value is the minimum value,
the resulting expression would throw
a value of zero. Finally,
we rank the negative of the expression
to implement the reversion. The
rank operator equally distributes
the input value of the expression
between zero and one
for all the stocks in our universe,
so that a stock with high overall
sentiment get shorted after
neutralization and vice versa
for a stock with low overall
sentiment. When we look at the results,
the Sharpe is around 1.9.
The returns-to-drawdown ratio is approximately
three and turnover is around 45%.
Now let's take a look at the detailed
performance parameters.
We have decent coverage for this idea.
The increase in the Alpha coverage
with time reflects the increase
in the coverage of the sentiment data over
time. PnL is
evenly distributed across stock
capitalization groups,
and capital appears to be evenly distributed
across industries.
And finally looking at the Sharpe
across the different sectors, we
see that the idea has decent
predictability across various sectors.
A potential way to improve
the idea might be to enhance
the reversion signal by incorporating
in different ways the reversion
indicated by price volume
data.
