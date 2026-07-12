# Group_Neutralize Operator

Course: Fundamental Data
Category: Data
Duration: PT6M9S
Source: VidYard
Last modified: 2024-06-07T05:22:44.411874-04:00

## Description

This video looks at how a company’s debt ratio is used as a signal to create alphas and how the ratio can impact share performance.
The four graphical results in the video starting at 5:03 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants.
The simulation setting “Max stock weight” has been renamed to “Truncation”.
The operator "IndNeutralize" has been renamed to "group_neutralize".

## Transcript

In this video,
we will discuss an idea
based on the change in a company's debt
relative to its total assets
and how this information can
be used as a signal to generate
an Alpha. Debt financing
is a form of financing in which a company
acquires capital from creditors,
for example, commercial banks.
This type of financing comes
with the obligation to repay the
debt with interest charged
on the amount borrowed.
The debt ratio is a financial ratio
that measures the extent of company's
leverage.
It's defined as the ratio of total
debt to total assets
and is expressed as a decimal
or percentage.
It can be interpreted as the
proportion of company's assets
that are financed by debt.
The higher the debt ratio, the
more leveraged a company is.
This implies greater financial
risk. At the same
time, leverage is an important
tool that companies use to grow,
and many businesses find sustainable
uses for debt.  With this
Alpha our hypothesis is:
if a company's debt has decreased
from previous quarter
as a ratio of its total assets,
its financial leverage, or
riskiness, has decreased,
and we will want to go long on
that stock. On the other hand, if
the value of the debt has risen
from the previous quarter, we
will want to short that stock
due to the increased leverage.
Now let's look at the implementation
of the idea.
The implementation uses three operators:
the rank, delta
and industry neutralize operators.
The rank operator ranks the input
argument of a stock among
all the stocks in the universe so
that the assigned value is equally
distributed between zero
and one.
The delta operator calculates
the difference between the current value
of the first argument and the
value observed N days back,
where N is the second argument.
If the data value has been increasing
with time, the value returned
by delta operator will be positive.
If the data value has been decreasing
with time, the value returned will
be negative. The industry neutralize
operator neutralizes the expression
provided to it as the first argument
while considering the grouping
provided to the operator as
a second argument. This operator
helps us perform sector neutralization.
The backtesting simulation runs
for the preceding five years
to generate an Alpha vector for
each day. If the value for the stock
is negative, it shorts
the stock
and goes long on stocks
with positive value. For the simulation
we are using the top 3000
US stocks on the basis of liquidity.
The maximum capital any
stock can take is 1%.
We are using the data
with the delay one to prevent
any look ahead bias.
The industry neutralize operator
neutralizes the Alpha over
sector.
Please note that we set
the neutralization in the Alpha
setting box to none and neutralize
over the sector by using
only the industry neutralize operators.
Now let's talk about how our idea
gets implemented using the
expression.
The expression on your screen calculates
the negative of the difference in
company's debt today
and the debt value observed 60 days
back, divided by the total
assets.
60 days roughly represents
the number of trading days in
a quarter. The change in the debt
divided by the total assets aims
to capture the change in
a company's financial leverage. The
rank operator then smooths
this value across all the stocks
in the universe and returns an
equally distributed value between
zero and one.
If a company's debt has decreased
since the previous quarter, the delta
operator will return a value
in proportion to the magnitude
of the change. This value will
flow through the rank operator and
finally result in more capital
being allocated to the stock
and vice versa.
When we look at the results, the Sharpe
is around 2.1.
The returns-to-drawdown ratio is
approximately 4.
And the turnover is about 6%.
When we analyze the detailed performance
parameters, we have decent coverage
for this idea across the selected
universe.
We observe coverage oscillations
because the fundamental data values
are updated only on a quarterly
basis and are unavailable for
all the stocks in our universe. The
PnL generated across different
capitalization groups is also
good, which means performance
is diversified across different
capitalizations.
The capital distribution across
industries is evenly distributed.
Finally, if we look at the Sharpe
across sectors, the idea has
decent predictability.
Potential ways to improve the
idea include combining
change in financial leverage
with change in company's liquidity stance.
With increased financial leverage
and increased payment obligations,
a company's liquidity gets
stressed.
