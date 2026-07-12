# Fundamental Data & Base Data

Course: Fundamental Data
Category: Data
Duration: PT6M38S
Source: VidYard
Last modified: 2023-04-28T11:31:45.758258-04:00

## Description

This video explains how fundamental data, such as revenue per share, can be combined with price volume data to strengthen an alpha. It also looks at how various operators can be used to further develop an alpha.
The four graphical results in the video starting at 5:09 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants. The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video,
we will discuss an idea based
on the combination of fundamental data
and base data, which is
also sometimes called as the price
volume data.
Fundamental data based Alphas
can be strengthened when they are combined
with the base data.
There are several ways to do this
Today we will talk about one of
the ways we can use fundamental
data as a filter for taking
positions on stocks. The
position taken would be a price
volume based signal.
The fundamental filter is based
on sales per share,
also called the revenue per
share, which computes the
total revenue earned per share
over a period,
usually 12 months.
It's calculated by dividing the
total revenue earned in the fiscal
year by the weighted average
of the outstanding shares for
that fiscal year.
The sales per share ratio
is used to evaluate a company's
business activities in comparison
with its share price. The
higher the ratio, the more active
the company. The reason for
choosing this ratio is that
investors are usually interested
in company's sales number.
If this metric increases,
investors might react positively
and the stock prices might raise.
Our hypothesis states
that if a company's sales
per share is higher
than the previous reported value
an upward momentum is established
for the stock price
else the stock price might
follow the usual mean-reversion.
Now let's look at the
implementation of this idea. The
implementation uses four
operators:
the rank operator, delta
operator, conditional
operator and the last
different value operator. The
rank operator ranks the input
argument of a stock among
all the stocks in the universe
so that the assigned
value is equally distributed
between zero and one.
The delta operator calculates the
difference between the current
value of the first argument and
the value observed N days
back,
where N is the second argument.
If the data value has been increasing
with time, the value returned
by the delta operator will be positive.
If the data value has been decreasing
with time, the value returned will
be negative.
The conditional operator
Is the 'if else' operator, which
states: if the condition mentioned
is true, Alpha is equal
to the expression one
else the Alpha is equal to the
expression 2. The last different
value operator returns the
most recent value of the
input argument,
which is different from the current value
of the input argument. This
operator is highly useful
for finding the last different
value of less frequently
updated data, such as
fundamental data and analyst
data.
The back testing simulation runs
for previous five years to generate
an Alpha vector for each day.
If the value of the stock
is negative, it shorts the
stock and goes long on
the stocks with positive value.
For the simulation, we are using the top
3000 US stocks on the basis
of liquidity.
The maximum capital any stock
can take is 1%.
We are using the data with Delay-1
to prevent any look-ahead bias,
and the Alpha is neutralized over
subindustry.
Now let's discuss how our idea
gets implemented using the expression.
The conditional operator checks
on whether the company's sales
per share is higher than the last
different value of sales per
share. If that's the case,
we assign the stock of weight
of one, which is the max
value the rank operator can assign
and represents a strong long
position on the stock. For
stocks that don't meet this condition
we use the weekly reversion signal,
ranking it to smooth the
output value to an equally
distributed number between
zero and one. This
helps us maintain a common
scale of assigned values for
the two different scenarios.
When we look at the results,
The Sharpe is around two.
The return-to-drawdown ratio is approximately
two again,
and the turnover is around 40%.
Now let's analyze the detailed
performance parameters.
We have decent coverage for this idea
across selected universe.
We observe coverage oscillations
because the fundamental data values
are updated on a quarterly
basis and aren't available
for all the stocks at a
given time.
The PnL generated across different
capitalization groups is also
good, which means performance
has been derived from
various equity capitalizations.
The capital distribution across various
industries is evenly distributed.
And finally, if you look at the
Sharpe across different sectors, this
idea has a decent predictability
across various sectors.
Now,
let's talk about the potential ways
to improve this idea. This
idea could be improved
by laying down a condition
which could help us compare
the magnitude of sales per
share with the last different
value of the sales per share.
Also, we can use more
creative ways to assign weight
to the stocks based on fundamental
or price volume data, instead
of giving a constant value of
one.
