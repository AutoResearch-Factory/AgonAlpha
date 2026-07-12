# Financial Ratios

Course: Fundamental Data
Category: Available Data and Operators
Duration: PT4M17S
Source: VidYard
Last modified: 2023-04-28T11:29:25.422122-04:00

## Description

This video explains how the debt-to-equity ratio can be used as a signal to create alphas and also shows how the ratio differs across industries. The simulation setting “Max stock weight” has been renamed to “Truncation”.

## Transcript

A company can use
two ways to finance its operations.
First, it could be debt from
the creditors or lenders like banks.
Second, it could be equity from the investors
or the shareholders. Unlike equity
financing, debt must be repaid
to the lender.
Since debt financing also requires
debt servicing or regular interest
payments,
debt can be far more expensive
form of financing.
Companies taking on large amount of
debt might not be able to make
the payments.
A debt-to-equity ratio
of 1 would mean
that the investors and creditors
have equal stake in the business assets.
A lower debt-to-equity ratio
usually implies a more
financially stable business. Companies
with higher debt-to-equity ratio are considered
more risky to the creditors and investors
than companies with the lower ratio.
This is because the high
debt-to-equity ratio shows
that the investors haven't funded the operations
as much as the creditors have.
In the other words, investors don't
have as much skin in the game
as the creditors do.
This could mean that investors don't
want to fund the business operations because
the company isn't performing well. Lack
of performance might also be
the reason why the company is seeking
extra debt financing. We can
use this idea to make an Alpha.
It could be done in a strategy
where we long the stocks of the companies
that have lower debt to equity ratios
as compared to the ones that
have higher debt to equity ratios. We
might also want to take into account
that industries have different debt
to equity ratios as some tend
to use more debt financing as
compared to the others, which might want to use
more equity financing.
Now let's look into the implementation
of this idea. Ts_rank
of minus debt to equity for
240 days. The rank operator
first puts all industries
on the same scale, incorporating
the fact that different stocks may
have different benchmarks. The
time series rank
of the debt to equity ratio helps
us understand if the current
level of this ratio is high
as compared to the normal level
over the last 240 trading days,
and it looks for this number
for every stock. Finally,
it outputs a number between zero
and one, where one represents
a high debt-to-equity ratio
and zero represents a low
debt-to-equity ratio.
Now look at the negative sign. The negative
sign in front of this debt equity
ratio implies that we
want to short the stock.
The neutralization operator on this vector
will then make sure we
invest equal amount in the long positions
and equal amount in the short positions.
The strategy would short the stocks
with debt-to-equity ratios higher
than the average for the group
and go long on the stocks with
debt-to-equity ratios less than
the average.
The simulation is run for five
years. The decay is zero.
The delay is one, and the neutralization
is done on the group market.
The results are quite consistent over
several years, it has only
one month for 2016 in
the simulation so it does not speak
much. But if you would see
the Sharpe ratio is 1.8,
The returns to draw down ratio is greater
than two, and the turnover is
less than 10%.
Now you can combine this idea
with other financial ratios to
incorporate more fundamental information
and further strengthen the signal.
This idea helps establish
that fundamental ratios offer
great insights into the companies and
can be instrumental in predicting the
long and the short direction
of the stocks.
