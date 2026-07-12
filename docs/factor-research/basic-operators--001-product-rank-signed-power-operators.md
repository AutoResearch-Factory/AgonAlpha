# Product Rank & Signed Power Operators

Course: Basic Operators
Category: Operators
Duration: PT6M55S
Source: YouTube
Last modified: 2026-06-02T07:51:25.429419-04:00

## Description

This video explains how an alpha generated using the mean reversion idea can be implemented with the different operators available on the platform.
The four graphical results in the video starting at 04:29 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants.
The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video
series, we will talk about reversion
and the many ways of implementing this
idea. The hypothesis is that
if something increases today,
it will fall tomorrow. And if something
decreases today, it will increase tomorrow.
This something can be anything:
price, volume, correlation
between two things
or the other things that you can think of
while developing your Alpha.
Let's try to test this idea using
price.
As a quick recap,
the back testing is done over
the previous five years to
generate an Alpha vector for
each day. If the value for the stock
is negative, the simulator shorts
the stock and it goes long
on stocks with the positive values
as you can see on the screen. It's
the very basic implementation of
this reversion idea. It is minus
of the difference of today's price
and the yesterday's price. So
if today's price is greater than the yesterday's
price, the expression in
the bracket is positive,
and my hypothesis is tomorrow
the price will fall, so we
should short this stock. I'll
put a negative sign in front of the expression
to achieve this objective.
Similarly, if today's prices is less
than the yesterday's price, the expression
in the bracket is negative,
but according to our hypothesis, the
price might increase tomorrow.
So we might want to long the
stock and a negative sign
in front of the expression will
help us make it positive. And we will
achieve the behavior of going
long on the stock. So this
implementation highlights reversion in
a very simple form.
Now let's look at an alternate implementation
of this idea using the product
operator. So the implementation
of this idea is, as you can see
on your screen, we are using two
operators here, the product operator
and the rank operator.
The product operator outputs the
product of the values in vector
X for the past N days,
the rank operator ranks
the value of the input X
among all the instruments,
and it returns the values
which are float numbers
equally distributed between
zero and one. So the stock
with the maximum value of X
will get one, and
the stock with the minimum value of
X will get zero.
The rest of the stocks will get a value
between zero and one, depending
on the rank in the universe. So this
is a very good operator and is used
in many ways in the Alpha implementations.
In the simulation environment, we
are using the top 3000
US stocks on the basis of
liquidity. The maximum capital
any stock can take is 10%
and I'm using the data with the delay
of one to prevent any
look ahead bias. Now let's discuss
how the idea I have explained gets
implemented using the expression.
As you can see, we are again
using the change in price.
But instead of yesterday's price,
we are using a price derived
from information over the past
five days. How do we do this?
The prices over the previous five days
are multiplied together
And the power of 0.2
is taken to bring this back
to the same scale. Before
subtracting from today's price,
the rank is taken to bring
the scale between zero and
one. This mellows down the
high price effect.
You wonder what does this mean?
We expect the stocks with
the high prices to have a
bigger change, and the magnitude
will define the proportion
in which we distribute the
capital. However,
we need to ensure this does
not lead to a large amount
of capital being allocated
to very few stocks
and rank helps us do that.
When we look at the results,
the Sharpe is 2.
The returns-to-drawdown ratio is
greater than 3, and
the turnover is around 40%.
Now let's analyze the detailed
performance parameters. If we look
at the coverage for this Alpha,
we have covered a big set of
stocks for the top 3000
universe that we selected in the simulation
settings.
If we look at the PnL generated
from different capitalization groups,
we see that the PnL has been
contributed by different
capitalization of stocks. And
if we look at the capital distribution across
different industries, we see
that we have evenly distributed the
capital across various industries
we are planning to create.
And finally, if we look at
the Sharpe across various sectors,
we can see that this idea has
a predictability across various sectors
in our universe. As an alternate
implementation of this idea
you can see on your screen a different
expression.
In this implementation,
we have used the SignedPower
operator.
This operator takes as input
the expression
and the power to be applied
on the expression.
It outputs the same sign
as the input value and applies
the power to the absolute
value of the input expression.
Everything else being the same, as
explained earlier, it would take
a power of two of the
input expression.
Again,
if we look at the results, the Sharpe
is 2.
The returns-to-drawdown ratio is greater than
3. The turnover is around
40%,
and if we analyze the detailed performance
parameters,
we have good coverage on
the universe we decided to trade.
The PnL is generated across
various capitalization of stocks. The
capital distribution across industries
is also even,
and the Sharpe is generated
by various sectors as well. So,
as a possible improvement, you
might try to combine different
durations of price change
to make the results more robust
and less parameter sensitive.
Or you can try alternate
implementations of the same idea,
say, by using other operators, which
we will also discuss in the future video.
