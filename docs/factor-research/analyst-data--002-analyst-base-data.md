# Analyst & Base Data

Course: Analyst Data
Category: Data
Duration: PT5M57S
Source: VidYard
Last modified: 2023-04-28T11:35:20.403908-04:00

## Description

This video shows how an alpha can be created by combining analyst estimates and earnings per share with price volume data.
The data field  at <1:20> is only available to consultants, not users. Users can use the field  instead.
The four graphical results in the video starting at 04:34 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants. The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video,
we will talk about building an Alpha
based on a combination of analyst
data and base data.
In certain situations analyst
data can be used as a good
filter for taking positions.
If there are revisions in the analyst
estimates,
investors will take the new information
and trade on it to update
the price of the stock. The
estimated earnings per share reported
is a consensus of analyst
estimates of a company's earnings
per share or the EPS.
This will be reported in the coming quarter,
fiscal year, or in the next
fiscal year.
Let's take a look at our hypothesis.
If the estimate of earnings per share
is higher than the last estimate
provided by the analysts,
it's considered positive news
and should set an upward
price momentum for the stock.
In the absence of such a situation,
we can use the weekly mean
reversion signal as our default
signal.
Now let's look at the implementation of
the idea.
The implementation uses four
operators:
the rank operator,
conditional operator,
last different value operator,
and the delta operator.
The rank operator ranks the input
argument of a stock among
all the stocks in the universe so
that the assigned value
is equally distributed between
zero and one.
The conditional operator is the 'if else'
operator
which states: if the condition
mentioned is true, Alpha is
equal to expression 1,
else the Alpha is equal to the expression 2
the last different value operator
returns the most recent value
of the input argument,
which is different from the current value
of the input argument. This operator
is highly useful for finding the
last different value of
less frequently updated data sets,
such as the fundamental and
the analyst data.
The delta operator calculates the difference
in the current value of the first
argument and the value observed
N days back, where N
is the second argument.
If the data value has been increasing
with time,
the value returned by the delta operator
will be positive.
If the data value has been decreasing
with time, the value returned will be
negative. The back testing
simulation runs for previous
five years to generate an Alpha
vector for each day. If
the value for the stock is negative,
it shorts the stock and goes
long on stocks with the positive
value. For the simulation
we are using the top 3000 US
stocks on the basis of liquidity.
The maximum capital any
stock can take is 1%.
We are using the data with
the Delay-1 to prevent any look
ahead bias,
and the Alpha is neutralized
over subindustry.
Now let's discuss how our
idea gets implemented using
the expression. The conditional operator
checks on whether the latest
value of the estimate of
reported earnings per share
is greater than the last
different value of the estimated
reported earnings per share.
If the condition is true, we go
long on the stock and assign it a
value of one.
However, if the condition is false,
we take the rank of a negative
of delta of the close
price over the past
five days.
This implements a weekly reversion
signal. If the price of the
stock increased over the past
five days due to the delta operator
with a negative sign, a negative
value is returned and vice
versa.
The rank operator then smoothes
the input value and returns
an equally distributed number
between zero and one
for all the stocks in the universe.
When we look at the results, the
Sharpe is around 2,
the returns to draw down ratio is approximately
three, and the turnover is around
40%.
Now let's take a look at the detailed performance
parameters.
We have a decent coverage
for this idea.
We observe coverage oscillations
because the analysts data values are
updated less frequently and are not
available for all the stocks at a
given time.
If we look at the PnL distribution across
all the capitalization groups of the stocks,
it is evenly distributed and
well diversified.
The capital distribution across industries
appears evenly distributed as well.
And finally, looking at the Sharpe
across different sectors, we see
that the idea has decent predictability
across the various sectors.
Now let's discuss some potential
ways of improving the idea.
This idea could be improved by
incorporating the sentiment
data in our signals.
Why? Because such revisions
are usually associated with investors
change in sentiment for a stock.
Also, we could improve our
filter condition to incorporate
the negative revision case and
assign a different signal
than a constant value of one.
