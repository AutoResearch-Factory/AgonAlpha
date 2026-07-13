# Customer & Sentiment Data

Course: Relationship Data
Category: Data
Duration: PT5M9S
Source: VidYard
Last modified: 2023-04-28T11:37:08.413081-04:00

## Description

This video explains how an alpha can be developed using the number of customers a company has and its sentiment volume generated from social media.
The four graphical results in the video starting at 03:58 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants.
The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

In this video,
we will discuss how to build an
Alpha based on the relationship
data using both
the number of customers of a company
and the sentiment volumes
captured on social media.
The number of customers of a
company represents the
total number of different end users
of the products
and services the company provides.
In this context, the customers
could also be a publicly traded
company. The social sentiment volume
represents how much a company
is being discussed or posted
on social media. This
indicates the level of interest
people or investors
are taking in a company's business
activities or stock.
If a company's social sentiment volume
is increasing, it represents
higher interest in a company.
However, we need
to normalize this figure with
company's number of customers
because as the number of customers
increase, the social sentiment
volume also increases.
This leads us to our
hypothesis:
If per customer social sentiment
volume is increasing,
then the level of interest investors
are taking in the company is increasing.
As a result, the company's stock
price could increase and
vice versa for a stock
with decreasing per customer
social sentiment volume. Now
let's look at the implementation
of the idea.
The implementation uses one
operator,
the time series rank operator.
The time series rank operator
ranks the first argument's
current value with respect
to its own values over the preceding
N days, where N is
the second argument.
The operator returns a value
that's always between zero
and 1.
The backtesting simulation runs
for previous five years to generate
an Alpha vector for each day.
If the value for the stock is negative,
it shorts the stock and goes
long on stocks with positive
value. For the simulation, we
are using the top 3000
US stocks on the basis of liquidity.
The maximum capital any stock can
take is 1%.
We are using the data with the delay-1
to prevent any look
ahead bias
the Alpha is neutralized over
the market.
Now let's discuss, how our
idea gets implemented
using the expression.
The time series rank operator
measures the trend of
per customer social sentiment
volume over the preceding
60 days. If per customer
sentiment volume is increasing,
the value returned by the
operator is high. If
it is decreasing, the value returned
is low.
The value returned acts
as a weight for the stock and
corresponds to the amount of capital
being allocated to it.
Therefore, a company
with improving per customers'
social sentiment volume
would be allocated more capital
and vice versa for a company
with deteriorating per customers
social sentiment volume.
When we look at the results, the
Sharpe is around 1.9.
The returns-to-drawdown ratio is
approximately four, and turnover
is about 30%.
Now let's analyze the
detailed performance parameters. We
have decent coverage for this idea
across the selected universe.
We observe coverage oscillations
because the relationship data
and sentiment data values are
not available for all the
stocks at a given time,
this is more pronounced in the less liquid
universe.
The PnL generated across different
capitalization also looks good,
which means the performance is diversified.
The capital is evenly distributed
across industries.
And finally, if you look at the Sharpe
across different sectors, the idea
has a decent Sharpe as well.
Now, potential ways of improving the
idea might include incorporating
whether the sentiment about the stock
around given time is positive
or negative.
This can be done in many ways using
different kinds of data fields.
