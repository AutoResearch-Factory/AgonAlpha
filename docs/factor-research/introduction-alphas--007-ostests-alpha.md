# OSTests in an Alpha

Course: Introduction to Alphas
Category: Introduction
Duration: PT8M31S
Source: YouTube
Last modified: 2026-06-02T07:38:07.012928-04:00

## Description

This video explains the various out-of-sample (OS) tests run by the platform and how to interpret the results. The OS tests evaluates the potential usefulness of an alpha. The simulation setting “Max stock weight” has been renamed to “Truncation”

HIGHLIGHTS GENERATED WITH THE HELP OF AI

•	🔍 Base tests include the check weight test (ensuring capital isn't overly concentrated on a few stocks), subuniverse test (ensuring performance isn't derived from a small set of instruments), superuniverse test (checking performance in the next largest universe), rank Sharpe test (evaluating the Sharpe ratio after applying specific operators), bias test (detecting any forward bias), and correlation test (evaluating uniqueness).
•	🎯 Performance tests include the IS Sharpe test (separating random noise from true Alpha), OS Sharpe test (similar to IS Sharpe but with different intervals), and new high test (checking if the Alpha reaches a new high in the cumulative PnL curve).
•	✅ To pass these tests, Alphas should have consistent performance across years, maximize the Sharpe ratio, incorporate logical parameters, avoid overfitting, and ensure diversification across different stocks.

## Transcript

An Alpha must
go through different stages before it enters
production and starts getting
used for trading. After
you develop and submit your Alpha
WorldQuant applies various tests
to it. These tests fall
into two categories.
First, the base tests. There
are eight base tests, which
are carried out in the OSTEST-PENDING
phase
The OSTEST-FAIL status
means your Alpha failed
at least one of these tests. The
second kinds of tests are the performance
tests.
There are two performance tests which
are conducted in the OSTEST2-PENDING phase.
It usually takes longer
to pass these tests. I
will now explain each of these
tests in detail and provides
some guidelines to help you
pass these tests for your
Alphas.
The first test is the check weight
test. It is a base
test, and it ensures
that you don't have a huge amount
of capital assigned to
a very few stocks.
Controlling this makes sure
your Alpha is diversified
and can survive different scenarios
in the financial markets.
This test is applied before
you submit your Alpha.
An Alpha passes this test
if the maximum weight in any
stock is less than 10%.
An Alpha can fail this test
if too few stocks are assigned
weight for a significant number
of days in a year.
Note that
assigning zero weights to all
stocks at the start of the simulation
does not fail this condition.
It only applies after the Alpha
starts assigning the weights.
The exact number of the minimum
stocks varies with the simulation
universe.
An Alpha can fail the test
if the weight is too concentrated
on one stock.
For example, if a stock has
30% of all the Alpha weight,
it will fail.
Now, let me tell you how to make your Alpha
pass this test.
If you have set the Truncation to less than 0.1
in the simulation settings, your
Alpha will pass this test.
The next test is the subuniverse
test. The subuniverse
value is the Sharpe in the next
smallest standard universe.
This test makes sure
that the performance of your Alpha
isn't derived from a very small
set of instruments in the chosen universe.
An Alpha will pass the subuniverse
test if it's
subuniverse Sharpe is
greater than the Sharpe calculated
by the formula, as you can see
on your screen right now.
The formula is different for Delay-1
and Delay-0 Alphas as
you can see on the screen.
To improve the chance that your
Alpha will pass this test, always
check the performance of your Alpha
in the next smallest universe
before submitting it.
Develop your Alphas on the next
smallest universe and submit on
the higher universe.
This can also help you make sure
that your Alpha is passing the subuniverse
test. The next test
is the SuperUniverse test.
Similar to the subuniverse test,
the superuniverse value
is the Sharpe of the next
largest standard universe.
And Alpha will pass the SuperUniverse
test when the
Sharpe calculated on the next
larger universe for this particular
Alpha is greater than 0.7
times the Sharpe of the Alpha
itself.
To make sure your Alpha passes
this test, check its performance
in the next largest universe
before you submit it.
The next important test is the rank
Sharpe test. The rank Sharpe
is defined as the Sharpe of the Alpha
after applying the operator
rank
and the power with
the exponential three separately,
to the long and the
short sides of the Alpha.
Later, the rescaling of each
side is done to the original
size.
An Alpha passes the rank Sharpe
test if
it has a positive Sharpe.
And after that, if the ratio of
the rank Sharpe to the original
Sharpe is greater than or
equal to 0.5,
or the rank Sharpe
is greater than 0.15.
The next test is the bias
test.
The goal of the bias test is
to detect any forward bias
in your Alpha. If your Alpha
passes this test, it means
that while doing the backtesting,
you have not used any data
from a time period more
recent than the simulation date.
An expression Alpha will
not fail this test, but
for the python Alphas, make sure
you write 'di-delay'
in your codes wherever required.
The next test is the correlation
test. This is a uniqueness
test. An Alpha passes
the correlation test versus
external WebSim Alphas when
one of the falling criteria is
met: if the PnL correlation
of the Alpha with any external WebSim
Alpha is less than 0.7,
it passes the test.
If the Alpha's PnL position
or trade correlation with
external WebSim Alpha in the same
group is less than 0.4,
it would pass the test.
And lastly, if the Alpha has
10% higher Sharpe than
any Alpha in the same group
with PnL positions
or trade correlation above
the 0.7 correlation threshold,
your Alpha would pass the test.
The CheckCorrAll test takes
at least three weekends to run,
and during this time, the OSTEST
status page will describe
the test's result as pending.
to make your Alpha pass this
test, try new ideas,
try different operators, try
different categories of datasets
and try alternate implementations
of your ideas.
The next test is the IS Sharpe test.
The goal of the IS Sharpe test
is to weed out any random noise
from the true Alpha.
To make your Alpha pass this test, try
to have consistent performance
across years and maximize
your Sharpe.
Now let's talk about the two performance
tests that we have.
The first test is the OS
Sharpe test.
Just like the IS Sharpe test,
the OS Sharpe test's
aim is to separate random
noise from true Alpha
An Alpha must meet the
set requirements for the Sharpe
for different intervals to pass
this test. For a better OS
Sharpe incorporate logical
parameters, try not to do
a lot of overfitting for your Alpha
and the probability of your Alpha
passing this test would be very high.
The last test is the new high test.
As the name suggests,
this test is passed, when the submitted
Alpha reaches a new high
in the cumulative PnL curve visible
to you on the platform.
A good Alpha usually passes this
test easily.
Having understood each of these
tests
and the different ways to make your
Alpha pass this test,
please try to follow these practices
before you submit your Alpha.
This would ensure that a big
piece of the Alphas submitted by you
pass the tests and go into
production.
