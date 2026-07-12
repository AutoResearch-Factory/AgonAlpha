# Backtesting & Potential Biases

Course: Improving Alpha Performance
Category: Alpha Performance
Duration: PT4M8S
Source: VidYard
Last modified: 2023-04-28T11:28:36.015130-04:00

## Description

This video explains the importance of backtesting and how potential biases can negatively impact Alpha generation.

## Transcript

We'll discuss
back testing
and how to prevent biases that can
be introduced during this process.
One of quants' key competitive
advantages is their ability
to backtest their strategies by
exposing their strategy algorithm
to a stream of historical financial
data to generate its past
performance.
The process by which this is carried out
is known as backtesting. The
benefits of this tool are significant
because you can determine whether
your proposed investment strategy
would have resulted in gains
or losses.
As well as the potential exposures,
the maximum drawdowns it would
have incurred, the returns
it would have generated and the likely
costs.
Typically, backtesting
involves a programmer coding
the idea into the proprietary language
hosted by the trading platform.
In the process of backtesting,
it is important that we take
care of the different kinds of biases
that can occur in this process
if not done in a correct
manner. Three of the most
common biases that can occur
in the backtesting process
are look-ahead bias,
survivorship bias and
psychological bias.
Let's talk about each of
these and how we can avoid them.
Look-ahead bias occurs
when future data is accidentally
included at a point in time in
the simulation where the data
wouldn't have actually been available.
So it's very important to make sure
during the implementation that
the code doesn't try to access data
from the period before the
particular time stamp.
The second common bias which
could come in is the survivorship bias.
Survivorship bias
can lead to significantly
inflated performance for certain
strategy types.
It occurs when
strategies are tested on datasets
that don't include the
full universe of prior assets
that may have been chosen
at that particular point in time,
but only consider those that have
survived to the current time.
For example, consider
testing a strategy on random
selection of equities before
and after the 2001
market crash.
Some technology
stocks failed while others
managed to stay afloat and even
prosper.
If we would have restricted the strategy
to stocks that made it through the market
during the drawdown period,
we will be introducing a survivorship
bias.
Because those stocks have already
demonstrated their success. The
third bias isn't actually a bias
but it can become a bias.
It's the psychological pressure.
If historical drawdowns
of say 2% or more
occur in the backtest, then in
all likelihood you will see
periods of similar drawdowns in live
trading. We have all
seen drawdowns,
they are unpleasant,
they are psychologically difficult to endure.
So even if the backtest suggests
such periods will occur, often
a strategy that otherwise would
be successful is stopped from
trading during the times of extended
drawdown. This would lead to significant
underperformance compared to the backtest.
So that should be taken care
of. I don't say that you should
not cut the strategies if they're going in
a drawdown, but there should be some definite
measures which helps you understand
when is the right time.
