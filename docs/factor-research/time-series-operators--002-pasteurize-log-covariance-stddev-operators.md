# Pasteurize, Log, Covariance & StdDev Operators

Course: Time Series Operators
Category: Operators
Duration: PT5M38S
Source: VidYard
Last modified: 2023-04-28T11:25:28.831437-04:00

## Description

Quantitative alphas may require checks to ensure that they are working correctly. This video demonstrates some techniques that can be used to check alphas.
The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video,
we will talk about some important
checks a quantitative Alpha
might need depending on
the implementation.
We will also discuss how to use
a few techniques, such as log
covariance and standard deviation.
A quant usually trades a big
set of stocks, so it's very
important to apply some checks
to the Alphas to ensure
nothing is going wrong.
We have already talked about the simulation settings.
There are two other checks you
should take care of,
especially while you are working
with the python framework. First
check to make sure you are trading
the right set of stocks as
defined by the universe.
Second, check to see
if any value in the expression
isn't tending towards infinity.
The operator Pasteurize helps
us do that.
It sets to NaN if the signal
is infinite or if
the underlying instrument isn't in the
universe.
To demonstrate how pasteurize
is used, let's apply
it to a simple Alpha idea. We
vwap over close. The implementation
of this Alpha is as
on your screen.
The operator log outputs
the natural logarithm of the
value given by the input expression,
the back testing simulation runs
for the previous five years to
generate an Alpha vector
for each day.
If the value for the stock is negative,
the simulator shorts the stock,
and goes long on the stocks with
positive values.
In the simulation environment, we
are using the top 3000 U.S.
stocks on the basis of liquidity.
The maximum capital and the stock can
take is 10%.
I'm using the data with Delay-one
to prevent any look ahead bias
and the Alpha is neutralized over
subindustry.
When we look at the results,
the Sharpe is 2.
The returns-to-drawdown ratio is
approximately 3
and the turnover is around 40%.
You should also look at the detailed performance
parameters to check
if the performance is derived
from a bigger set of stocks
as we explained in 'The simulation
results' video.
Now,
let's discuss an Alpha that uses
covariance and standard deviation
operators.
The idea is if the covariance
between the volatility of returns
and the delta of close price
and the volume weighted average
price over the past month is
high, we should go long
that stock and vice versa.
Now let's discuss the implementation
of this idea using an expression
The covariance operator
takes as input two vectors
x and y, as well
as the time period
and outputs the covariance,
which is a measure of how much two
random variables change together,
Note that the time period must
be less than 512 days.
The standard deviation operator
takes as input vector X
and the time period and outputs
the standard deviation, which
is a measure used to quantify
the amount of variation or
dispersion of a set of
data values. Note that
the time period must be less than 512
days. The backtesting simulation
runs for previous five years
to generate an Alpha vector
for each day.
If the value for the stock is negative,
the simulators shorts the stocks
and goes long on stocks
with positive values.
In the simulation environment, we
are using the top 3000 US
Stocks on the basis of liquidity.
The maximum capital any stock can
take is 10%.
I'm using the data before a particular
time stamp in a day and start
trading after that time stamp
to prevent any look ahead bias.
This is captured by using Delay-zero.
In these settings,
the neutralization used is
subindustry,
and if we look at the results, the
Sharpe is 2.
The returns-to-drawdown ratio is greater
than 5
and the turnover is around 25%.
You should also look at the detailed performance
parameters to check if the
performance is derived from
a bigger set of stocks. As
we explained in this simulation results
video. To summarize,
while developing a quantitative Alpha,
you should always take care of corner
cases to avoid any
potential biases or errors
in the implementation.
Also, various statistical
techniques are available that
can be used to implement the same idea
in many different ways.
