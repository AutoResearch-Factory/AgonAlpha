# Competitors & Returns

Course: Relationship Data
Category: Data
Duration: PT5M42S
Source: VidYard
Last modified: 2023-04-28T11:38:00.869270-04:00

## Description

This video looks at how an alpha can be developed using relationship data and the impact a company’s competitors can have on its returns.
The four graphical results in the video starting at 04:41 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants. The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video
we will talk about how to build an
Alpha based on the relationship
data using the returns
of customers and the number
of competitors. The returns
of customer companies have
a significant impact on a company's
returns.
If the customer company's
business is growing as
implied by high returns,
it's likely that the revenue
of the subject company might also
grow thanks to increase
customer orders, the increased
revenue will result in higher
profits
and returns for the subject
company. The number of competitors
of the company represents the total
number of companies that are conducting
business similar to that
of the subject company and compete
with one another for revenue
from the industry customer base.
The higher the number of competitors
vying for similar set of customers,
the more pieces the pie
has to be divided into
and the less effect the customer
company's stock returns will
have on the subject company.
This leads us to a hypothesis:
if the ratio of the returns of
the customer company's stocks
to the number of competitors is
growing, then the stock price
of the subject company could increase.
Along the same lines, the
stock price could decrease for a
company with a declining ratio.
Now let's look at the implementation
of the idea.
The implementation
uses two operators:
The group rank operator and
the ArgMin operator.
The group rank operator ranks
the second input argument
of a stock among all
the stocks in the grouping
provided to the operator as
the first argument
and returns a value equally
distributed between zero
and 1.
The ArgMin operator returns
the relative index of the
minimum value of the input
argument observed over
the preceding N days.
For example, if for
the current day we observe
the minimum value, it returns
zero.
If for previous day we observe
the minimum value, it returns
one and so on.
If all the values over the preceding
N days are NaN, it
returns zero.
The backtesting simulation runs
for previous five years to
generate an Alpha vector for
each day.
If the value for the stock is
negative, it shorts the stock
and goes long on stocks with
a positive value.
For the simulation, we
are using the top 3000 US
stocks on the basis of liquidity.
The maximum capital any stock can
take is 10%.
We are using the data with the delay-1
to prevent any look ahead
bias.
The Alpha is neutralized over industry.
Now let's discuss how our
Idea gets implemented using
the expression.
The ArgMin operator calculates
how the ratio of average
returns of the customers
to the number of competitors of
the company changed over
the previous 15 days and
assigns it a relative index
based on its trend.
If the ratio has been increasing, the
ArgMin operator will return
the index of the minimum
value, which would be high.
This will assign more capital to the stock
and vice versa for decreasing
ratio values.
The group rank operator
ranks the output of the
ArgMin operator for a stock
among all the stocks in the sub industry
So that the output number is equally
distributed between zero
and 1.
When we look at the results, the
Sharpe is around 1.9.
The returns-to-drawdown ratio is approximately
3.5.
And turnover is around 15%.
Now let's analyze the
detailed performance parameters.
We have decent coverage
for this idea across the selected
universe.
The PnL generated is decently
distributed across all the
capitalization groups. The
capital looks to be evenly distributed
across industries.
And finally, looking at the Sharpe
across the different sectors we
see that the idea has decent
predictability across sectors.
Potential ways of improving
the idea include incorporating
the effect of stock returns
of the partner companies on
the subject company
because they,
along with the customers,
play an important role in the company's
day to day business activities.
