# Making an Alpha: Simulating an Alpha

Course: Introduction to Alphas
Category: Introduction
Duration: PT3M29S
Source: YouTube
Last modified: 2026-06-02T07:01:10.819994-04:00

## Description

This video demonstrates what happens after simulation settings and parameters have been set and the type of results the platform generates for analysis.
The “Aggregate Results table” at 2:16 has a new layout, without the columns of Drawdown, PNL and Book Size. The PNL by year is now visible in the Chart above the IS Summary. The four graphical results in the video starting at 02:42 (Alpha Coverage, Capital Distribution, PnL by Capitalization and Sharpe by Sector) are visible on the BRAIN platform only to consultants.

HIGHLIGHTS GENERATED WITH THE HELP OF AI

•	💡 Begin with formulating an idea for Alpha simulation. It can range from simple to complex.
•	🛠️ Choose the operators and datasets required to implement the idea.
•	⚙️ Set up appropriate simulation settings for the idea.
•	📝 Enter an Alpha expression, combining data, operators, and constants, for Alpha idea implementation.
•	🔄 The platform evaluates the input code for each instrument to construct a fictitious portfolio, allocating investments in each stock for a one-day period in proportion to the values of the expression.
•	📊 If specified, neutralization calculates the final value, where a negative variable denotes short positions and a positive variable indicates long positions.
•	💰 The platform calculates and displays the simulated PnL based on daily positions.

## Transcript

In the past few
videos, we have learned about
Alphas, the simulation settings
and how to analyze the performance
parameters. Now let's
discuss what steps you should take
while simulating an Alpha and
what goes on in the background while
you wait for the simulation results.
The first thing you need to do is
think of an idea to create an
Alpha.
It can be very simple or
complex.
Next, you should think of the operators
and the data sets you will use
to implement your idea. After
that, you need to decide upon
the right simulation settings for
your idea.
The next step is to enter
the simulation settings and
an Alpha expression that consists
of data, operators
and constants, which you have decided
to implement your Alpha idea.
The input code is evaluated
for each instrument to construct
a portfolio. The platform
will then allocate an investment
in each stock for one
day period in proportion
to the values of the expression.
The process repeats each day.
And if the user specifies the neutralization,
the raw values - that is
the values of the expression -
aren't used directly,
and the neutralization operation is
applied to calculate the final value.
With the final values,
negative numbers would result in
short positions.
The positive numbers will result in long positions.
And based on their daily positions,
PnL is calculated and
displayed to the user.
The NaN means no positions,
and thus there would be no PnL.
Once the simulation is complete, the
platform will present to you
with the results.
They come in two forms.
First,
it provides you an aggregate
performance parameters like
the Sharpe ratio,
the returns,
the turnover and the drawdown.
You will analyze these to decide
if the results are satisfactory or
if you need to work more to improve
your signal.
You will also get a detailed analysis
of the aggregate performance parameters.
These would include graphical
results representing the
capital distribution,
the coverage, the Sharpe
ratio and the PnL generated
from different capitalization stocks
grouped together
or different stocks within industries,
all sectors grouped together.
Keep in mind that the more
diversified the sources of performance
across sectors, industries
and capitalization,
the more robust your Alpha is.
We will follow this process
in all our future videos,
and I will use Alpha examples
to explain how to use different
operators
and data sets for creating Alphas.
