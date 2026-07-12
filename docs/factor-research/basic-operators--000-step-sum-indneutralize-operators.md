# Step sum & IndNeutralize operators

Course: Basic Operators
Category: Operators
Duration: PT6M51S
Source: YouTube
Last modified: 2026-06-02T07:43:43.626822-04:00

## Description

This video shows how an alpha can be created using the current volume data and how various operators and neutralization can be used to modify and improve the alpha.
The 4 graphical results from 03:06 onwards are only visible to consultants: PnL by Capitalization, Alpha Coverage, Capital Distribution and Sharpe by Sector.
The simulation setting “Max stock weight” has been renamed to “Truncation”.
The operator "IndNeutralize" has been renamed to "group_neutralize".

## Transcript

In this video we will discuss an
idea that's driven by the volume data
Our hypothesis is
a large current volume
compared with average volume
over the past month or
quarter implies a
bullish sentiment about the
stock. Therefore a
trader might want to go long
on that stock. As you can
see on the screen, this idea
has a very simple implementation.
We used two operators here,
the sum operator and
the indneutralize operator.
The sum operator sums
the value in the vector X
for the past n days.
Note that the parameter n
that we input to the sum operator
must be less than 512.
We usually use the sum operator
when we want to find the average
of a given quantity.
The indneutralize operator
takes as input the Alpha x
and the group.
It neutralizes the Alpha x
against the specified groupings which
can be any matrix such
as the sub-industry, industry,
sector or a constant.
You also can use your own
customized group to do the neutralization.
The back testing simulation runs
for previous five years
to generate an Alpha vector for
each day. If the value for the stock
is negative, the simulator
would short that stock
and it would go long on the stocks with
positive values of the Alpha.
In this Alpha all the values are
positive,
but the Alpha is neutralized
over the sector
using the indneutralize operator.
This leads to going long on
the stocks with Alpha values higher
than the sector average and going
short on the stocks with Alpha
values below the sector average.
In the simulation environment, we
are using the top 3000
US stocks on the basis of liquidity.
The maximum capital any stock can
take is 10%.
I'm using the data with delay one
to prevent any look ahead bias.
Now let's talk about how
the idea I have explained gets
implemented using the expression
the ratio of current volume to
the average volume over the
past quarter is calculated.
clearly, the higher the value of
this expression for a given stock,
the more the simulator will bet
to go long on it.
This is in line with the hypothesis
we wanted to test and if we
look at the results,
the Sharpe is 2
The return to drawdown ratio is approximately 2.5
The turnover is around 40%.
And if we look at the detailed results
about the performance parameters,
if we look at the coverage, we have
a decent coverage for these top 3000
stocks
and if we look at the PnL generated
by different capitalization of stocks,
we will see that PnL is being
contributed by various groups
of stocks on the basis of capitalization.
And if we look at the capital distribution
across various industries,
there is a good distribution of
capital across different industries, we
are trading and the Sharpe
is also good on different sectors.
Now let's discuss a small improvement
to this idea and implement
it in a slightly different way.
So as you can see on the screen,
this is the new implementation with a
slight improvement.
We have used this step operator here
The step operator
creates a vector for each
instrument whose value is
n for today,
n-1 for yesterday and so on.
So if we look at the expression that
we have on the screen,
the ratio of the current volume
to the average volume over the past
quarter is calculated again.
When this ratio is multiplied with
step(20),
a weighted average of this ratio
over the preceding 20 days
is calculated.
The highest weight of 20 is
given to the current days ratio
a weight of 19 to yesterday's
ratio and so on
to a weight of one to the ratio
20 days ago.
The step function here helps to smooth
out the effect of the large
change in the ratio on a given
day compared with its usual
value. This prevents
any sudden change in positions and
controls the turnover or the cost
involved in trading.
To repeat the parameters for
this simulation environment: we are using
the TOP3000 US stocks on
the basis of the liquidity. The maximum
capital any stock can take is 10%
which is being taken care of by the max
stock fraction parameter in the simulation
settings.
I'm using the data with delay one
to prevent any look ahead bias
and I'm also neutralizing this
Alpha using the group sub-industry
in this simulation setting.
Again,
the higher the value of this expression
for a given stock,
the more the simulator will bet to
go long on it.
When we look at the results, the
Sharpe is 2.1.
The returns to drawdown ratio
is approximately 5 and
the turnover is around 40%.
If we analyze these results in detail,
The coverage is again decent for the top
3000 stocks, we are still trading
on average a big set of universe.
The PnL is generated from
various capitalization of stocks.
The capital is distributed across
industries and the
Sharpe over different sectors is also
quite decent, telling us that
the Alpha has a good predictability
over various sectors.
Now, possible improvements to this
idea might include combining
the volume information with
other data, such as price
sentiment, fundamental
to improve the signals predictability
and by varying the duration of the
step operator
to incorporate stock's volatility
profile, you might improve
the idea further
