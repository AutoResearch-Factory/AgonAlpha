# Max & Min Operators

Course: Time Series Operators
Category: Operators
Duration: PT8M30S
Source: VidYard
Last modified: 2023-04-28T11:27:13.322725-04:00

## Description

This video talks about how an alpha can be developed employing a mean reversion method that uses variation in the range of prices over time to capture the level of reversion.
The four graphical results in the video starting at 03:57 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants. The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video, we
will talk about another reversion idea
that uses a variation in
the range of prices to capture
the level of reversion. We
will test two different kinds of ideas,
one that uses the max
and min operator to output
the maximum or minimum between
two quantities.
And the second, which uses
the time series max operator
and the time series min operator
to output the maximum or
minimum of one quantity
over a time period. Now
let's talk about the first idea.
The hypothesis is
that stock has a higher probability
of reversion if the difference between
the close price today and
the minimum price between
today and yesterday's close price
both inclusive,
is high
when compared with the maximum
range of price variation
between today's close
and yesterday's close for
the same stock.
Sounds a little complex?
This will become clearer when we look at
the implementation.
So as you can see on your screen
the formula for the implementation.
This implementation uses two
operators:
the max operator and
the min operator.
The max operator takes two vectors
as arguments
and returns a single vector.
The parallel maxima of
the vectors that are given as the input.
Similarly, the min operator
Takes two vectors as arguments
and returns a single vector,
giving the parallel minima
of the vectors provided as the
input to the operator
the backtesting simulation runs
for the previous five years
to generate an Alpha vector
for each day.
If the value for the stock is negative,
the simulator short the stock
And it goes long on the stocks with
positive values
in the simulation environment, we are
using the top 3000
US stocks on the basis of the
liquidity.
The maximum capital any stock can
take is 10%
and I'm using the data before
a particular time stamp in a day
and start trading after
time stamp to prevent
any look ahead bias.
And this is captured using the delay
zero in these settings
as in the implementation,
the numerator calculates
the five days average
of the delta of the close
and the minimum price
between close price that day
or the day before,
both inclusive
and the denominator calculates
the average of the minimum
range of price between
that day and the close
price the day before. The
numerator will be greater than or
equal to zero,
and the denominator will always
be greater than zero.
The negative sign in front of the
expression signifies a
strong reversion if the ratio
is high
and a weaker reversion
if the ratio is low compared
with the stocks in the universe we
decided to trade and as mentioned
in the simulation settings. Now looking
at the results, the results
have a Sharpe of 2.2.
The returns-to-drawdown ratio is
approximately 4,
and the turnover is around
35%. Now, looking
at the detailed performance parameters,
there is a good coverage for this
Alpha idea.
So we decided to trade top 3000
stocks and we have a decent coverage.
The PnL is generated from
different capitalization of stocks,
which means the idea is working
well across different cap stocks.
Then the capital is distributed well
across different industries,
which means that we have a
good enough concentration of capital in
different groups of stocks.
And finally, we have a decent
Sharpe across different sectors,
which means that the idea has
a prediction power across different
sectors.
So this gives us a little confidence about
the robustness of our idea. Now let's
discuss this second idea. The
hypothesis is
the probability of reversion
in a stock is much higher
if the difference between the close
price today
and the maximum
of the high price in
the past five days is
large.
This reversal would be relatively
weak in a stock
whose maximum range of price
variation over previous five
days was also high.
As you look on your screen, the implementation
of this idea is right there.
So this implementation uses two
operators:
the time series max operator
and the time series min operator.
Ts_max operator or
the time series maximum operator
calculates the maximum value
of the quantity X over
the past N days,
and the Ts_min operator calculates
the minimum value of X over
the past N days
In the simulation environment, we are using
the top 3000 US stocks
on the basis of the liquidity.
The maximum capital
any stock can take is 10%.
This avoids any concentration on one stock,
and I'm using the data with Delay-1
to prevent any look ahead
bias.
note that these operators
are different from the max and
the min operator we used in the
first idea.
As you see in the implementation,
the numerator calculates the
difference in the current close
and the highest price in
the previous five days.
The denominator calculates the
maximum price variation
in the past five days.
If the ratio is high, it
suggests stronger reversion
as we discuss in the hypothesis.
The rank operator is finally
applied to the ratio to
smooth out the output and
provide a number between
zero and 1.
The results have a Sharpe of 2
The return to drawdown ratio is approximately  4
and the turnover is around 40%.
And if we analyze the detailed
performance parameters: again,
we have a good coverage for
the top 3000 universe be selected
to trade. The PnL is generated
from different capitalization
of stocks, and the capital
is distributed well across
different industries.
And finally, if we look at the Sharpe
from different sectors, we see
that we have a decent Sharpe
from different sectors, which implies
that the prediction of this idea is quite
decent across different sectors
that we are trading
as a possible improvement to both
the ideas
try to combine different durations
of price change to make the results
more robust and less parameter
sensitive.
You also could try different
time periods, depending on the
volatility of the stocks.
Bear in mind that smaller
cap stocks have longer
trends than the large cap stocks,
which could also mean that
the large cap stocks have strong
reversion as compared to
the small cap stocks. As
you try to implement these improvements
to the idea or try
other ideas that you have,
the signal would improve and provide you
better results.
