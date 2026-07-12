# Correlation & Rank Operators

Course: Basic Operators
Category: Operators
Duration: PT7M50S
Source: YouTube
Last modified: 2026-06-02T08:02:39.361074-04:00

## Description

This video demonstrates an alpha idea using price volume data and how this idea can be implemented with the correlation and rank operators available on the platform.

Note that ASI region and the MINVOL1M universe are visible only to consultants. The four graphical results in the video starting at 5:44 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants. The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In the process of Alpha
generation.
First, let's talk about an Alpha
idea. After that, we will
discuss the correlation operator
and how we can use it to implement
the idea that we will discuss.
This is a more sophisticated idea,
and I like how easily
it's implemented using a
correlation operator and a
rank operator.
The platform provides you with price
and volume data.
Price tells you in which direction
the stock is moving.
Volume tells you whether there
are buyers or sellers for
the stock. So the idea is
for the given universe of stocks
that one decides to trade.
If the ratio of actual volume
to the average volume over the
past 20 days is increasing
relative to the other stocks in the universe,
then we expect a reversal
in price,
assuming the market is
reacting
and absorbing the price information.
On the other hand, if the ratio
of volume
to the average volume over the past
20 days
is decreasing relative to other
stocks in the universe,
then we expect the stock
to continue the trend because
the market hasn't absorbed
the price information. The
implementation of this idea
is as you can see on your screen.
We have two operators here,
the correlation operator and
the rank operator.
The correlation operator calculates
the correlation of the values in
the input vectors X and
Y, for the past N days.
Note that this parameter
N must be less than 512.
The rank operator ranks
the values of the input X among
all the instruments,
and it returns values
which are float numbers equally
distributed between zero
and 1.
So the stock with the maximum value of
X will get a one, and the stock
with the minimum value of X will get zero.
And the rest of the stocks will get
a value between zero and one,
depending on the rank in the universe.
The backtesting of this
idea is done over the
last five years,
and it generates an Alpha vector
for each day.
If the value for the stock is negative,
the simulator would shot
the stock
and if the value is positive,
the simulator would long the stock.
In terms of the simulation environment
which we control from the simulation
settings, the maximum capital that we
would put on any stock is less than
10%, and the
neutralization is subindustry.
Now let's talk about
how the idea I explained gets
implemented using the expression.
There are four scenarios that
are explained by the expression that
you can see on the screen.
First, if the close price
and the volume ratio have
increased more than those
of the other stocks in the universe,
the correlation will be positive.
We say the market has absorbed
the price information
by increased volume ratio,
and we will see the reversal
in price. So we will want to
short the stock,
and placing a negative sign in
front of the expression will help us
achieve that.
Second, if the close price
and the volume ratio have fallen
more than those of the other stocks
in the universe,
the correlation will be positive.
We say the market hasn't
absorbed the price information because
the volume ratio is falling as
compared to the other stocks
in the universe.
The probability of reversal is weaker
than for the other stocks, so
the stock will continue the trend in
the direction of the price.
In this case, the prices are falling
more as compared to other stocks,
so we will short this stock
and placing a negative sign in
front of the expression helps us achieve
that.
In the 3rd scenario,
the close price has increased
and the volume ratio has fallen
compared to the other stocks in the
universe.
And using the similar logic, we
assume the market hasn't
yet reacted strongly compared
to how it has done for the other stocks.
So the price trend will likely continue
and we want to long the stock.
In this case, the correlation is negative,
so the negative sign in front of the
expression will make the expression positive
and we will long stock.
Finally,
if the close price has fallen
and the volume ratio has increased
as compared to the other stocks in the universe,
the market has reacted strongly,
so the price trend will likely revert
and we want to long the stock.
In this case, the correlation is
negative, so the negative sign in
front of the expression will make
the expression positive and we will long
the stock.
So if we look at the results,
the Sharpe is somewhere around 2.
The turnover is around 40%
and the return to draw down ratio is
greater than one
and if we look at the detailed analysis,
we have a good coverage across
the universe that we selected to trade.
The PnL generated across different
capitalization groups is quite
decent and the capital is distributed
across industries, which
shows that the performance is also
driven from different industries.
And finally, if we look at the Sharpe
generated from various sectors, it
shows that the idea has decent
prediction value across different
sectors.
So this illustration helps us
understand how a correlation
operator can help us develop
an Alpha
Using information from two
data inputs that affect
each other.
It also highlights the strength
of the rank operator.
The rank operator helps
smooth out the relative difference
among the stocks in the universe
and facilitates the capital allocation
and the long short decisions.
Now, what could be possible improvements
to this idea?
In this idea, we have taken
a correlation between two
entities over five days.
As a possible improvement to this idea.
You can try compare the short
term correlation between the two quantities
within long term correlation,
and you can try to understand whether
the short term correlation will
tend towards the long term
correlation between these two entities.
So this illustration helps us
understand how a correlation
operator can help us develop an
Alpha using information
from two data inputs that
affect each other. It
also highlights the strength
of the rank operator with
smooths out the relative difference
among the stocks in the universe
and facilitates the capital
allocation and the long short decisions.
