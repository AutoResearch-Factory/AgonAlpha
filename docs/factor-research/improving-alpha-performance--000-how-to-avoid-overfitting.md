# How to Avoid Overfitting

Course: Improving Alpha Performance
Category: Alpha Performance
Duration: PT6M32S
Source: VidYard
Last modified: 2023-04-28T11:27:57.280932-04:00

## Description

This video discusses the concept of overfitting in the context of Alpha creation and provides three practical steps to help minimize overfitting in your Alphas.

## Transcript

In this video, we
will discuss overfitting, which
is very important aspect of Alpha
development. Alpha
is nothing but a mathematic model for financial markets.
There's no definite approach
that can help us avoid
overfitting. But there are certainly
good practices one can follow
to reduce the extent of overfitting.
In this video, I will share
the approach I took towards my research
to avoid or control
the extent of overfitting.
So we'll talk about three key things.
First, what is overfitting?
Second, what are good practices
to help us avoid overfitting.
And finally, what tests
we can carry out to check
the robustness of the signal
or the level of overfitting.
Now let's start by discussing what overfitting
is. In the process
of Alpha development, a quant runs
his strategy algorithm on
the historical data to build
an expectation about the future
performance of his strategy.
While executing his idea, he
can introduce a lots of conditions
and parameters to maximize
the Alpha's performance on
the past data.
But over doing this to make
the data present, good back
testing results can lead to
poor performance. So this process,
where the performance of the model on
future unseen data
varies a lot from the performance
of the model on the data it was
trained on, is called overfitting.
Here are three good practices
to help us avoid overfitting
First, go by the idea.
The process of improvising
the backtesting results of
the strategy should mainly be
driven by making improvements
to the idea behind the signal.
It's not a good practice to try
make improvements by introducing
random conditions and parameters.
Second, good practice is to
avoid changes that result
in very small difference in
the performance in the backtesting results.
While making changes to the implementation
of the Alpha, you should try
avoiding making changes that result
in very small differences in
the in sample performance. The
impact of these small changes can
be much bigger in out of sample
and could be the reason of the poorer
performance.
So lesser the number of conditions and
the parameters we can introduce
while developing over Alpha,
the better it is. So the third
good practice is logical
parameter fitting.
While fitting various parameters,
you shouldn't try random numbers.
Instead, you should make logical
changes in the parameters. For
example, if you're training the
Alpha on the duration or
time period, you can use
values like five days for a
week,
or 10 days for 2 weeks.
You can also use 20 days,
which is a month or 60
days for a quarter, 120
for half a year, 250 for a
year, and so on. In short,
the simpler and more explainable
the ideas execution, the
higher its expectation of having
similar in sample and
out sample results. There are a
few tests you can do to
check the robustness of the ideas, execution
or the level of overfitting
that could have happened while doing the
backtesting. You can test the idea
by analyzing its performance
on various subsets of stocks
in its universe.
For example, if the original
signal was created on the top
2000 liquid stocks in US,
you can test the same
execution on top 500
liquid stocks.
Given that the idea is now being
tested on much more liquid group,
we would expect performance to fall.
But the performance shouldn't completely vanish
as even these 500 stocks
were a part of the universe and were contributing
into the performance. A complete
fallen performance or much less
performance in the liquid universe as
compared to the top 2000
would indicate that most of the performance
was derived by fitting the model
on a relatively illiquid group
of instruments in the universe.
On the Websim platform,
a positive value of expression
for a stock represents going long
and a negative value represents going short.
The magnitude of the value represents
the proportion in which the capital
will be allocated across various
stocks in the universe. It
is important to test the strength
of predictability of the direction
and the magnitude in an Alpha.
There could be lots of ways of doing
this, but I'll share with you
two ways of doing this. The predictability
of going long and short on
a stock can be tested by
removing the impact of
magnitude from the signal.
This can be done by taking sign
of the whole expression
which will equalize the capital
on all stocks. The results
will represent the Alpha strength
in predicting the long and
short direction,
and this could also act like a test
for overfitting of an Alpha
on the basis of the capital allocation
or on the basis of the sign
or the direction of the signal. The second
approach, which is basically to test
how much of the performance is
driven by the capital allocation.
You can take the rank of the expression
which will define a more normalized
way of distributing capital.
If the results are still good, it
indicates that the Alpha is not
over fitted and not deriving
its performance from a very few stocks.
So there are many more approaches you can
take, but this could be a good
start.
