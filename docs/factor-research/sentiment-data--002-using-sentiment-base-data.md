# Using Sentiment & Base Data

Course: Sentiment Data
Category: Data
Duration: PT5M7S
Source: VidYard
Last modified: 2023-04-28T11:42:15.766571-04:00

## Description

This video explains how sentiment data generated from social media is combined with base data to build an alpha using the rank and time series rank operators.
The four graphical results in the video starting at 03:55 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants. The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

We will build an Alpha
by combining sentiment and
base data.
A lot of discussions about future
stock price movements take
place on social media platforms.
The amount of this activity is captured
in the social sentiment volume
data field.
A higher value indicates more
investor activity.
Many investors can be influenced
by the amount of content and
related content they see on
social media, especially
when there's an increased activity.
This leads us to our hypothesis.
If a stock's closing price was
less than the midpoint of the
high
and low range that day,
then it's likely that the price
will increase the next day.
The reverse would be true for a stock
whose closing price was more
than the midpoint of the high
and low range observed on
a given day. If you witnessed increased
investor activity on social media
captured using social sentiment volume,
the chances of reversal are higher.
Now let's look at the implementation
of the idea.
The implementation uses two operators:
the rank and the time series
rank operators.
The rank operator ranks the input
argument of a stock among
all the stocks in the universe so
that the assigned value is
equally distributed between
zero and one.
The time series rank operator
ranks the first argument current
value with respect to its
own values over the preceding
n days, where n is
the second argument. The operator
always returns a value that's
between zero and one.
The backtesting simulation
runs for previous five years
to generate an Alpha vector
for each day.
If the value for the stock is negative,
it shorts the stock and goes
long on stocks with a positive
value. For the simulation we
are using the top 3000 US stocks
on the basis of liquidity.
The maximum capital any stock can
take is 10%.
We are using the data with the Delay-1
to prevent any look ahead bias
and the Alpha is neutralized over
subindustry.
Now let's discuss how our
idea gets implemented using
the expression. The time series rank
of the social sentiment volume over
the preceding 40 days throws
an output based on how to
sentiment volume captured
on social media has been trending
over time.
The value returned would
be higher for a stock with increased
social sentiment volume than
for a stock with a declining social
sentiment volume.
The rank operator equally distributes
the time series rank output between
zero and one. The
closing price is subtracted from the
average value of the high and
low price to capture the reversion
signal. If the closing
price is greater than the midpoint value
of the high and low prices, the
resulting value of the expression would be
negative and vice versa. This
expression is normalized by dividing
it with the high low price
range observed for the day
to avoid assigning large
weights to high priced stocks.
When we look at the results, the Sharpe
is around 2.3.
The returns-to-drawdown ratio is approximately
three and the turnover is about 40%.
When we analyze
the detailed performance parameters, we
have decent coverage for this idea
across the selected universe.
We observe coverage oscillations because
the sentiment data coverage varies
with time.
The PnL generated is decently distributed
across all the capitalization groups,
but slightly more performance derived
from small cap and mid cap stocks.
The capital appears to be evenly distributed
across industries,
and finally, the Sharpe also looks
pretty decent across the
various sectors.
Potential ways of improving the idea
include controlling for turnover
using the tradewhen operator
where we can mention our trigger trade
condition based on increased
volatility, trading volume
and so forth to reduce
the trading activity where possible.
We can also improve the idea
by capturing insights about
the sentiment value of the securities
in our existing signal.
