# Making an Alpha: Simulation Settings

Course: Introduction to Alphas
Category: Introduction
Duration: PT4M3S
Source: YouTube
Last modified: 2026-06-02T06:34:54.792423-04:00

## Description

This video shows how to use the simulation settings available on the platform and how they affect your Alpha results.
Simulation settings are now simpler than ever! At 3:40, we now take care of the “Lookback days” metric for you and auto-populate the value. The simulation setting “Max stock weight” has been renamed to “Truncation”

HIGHLIGHTS GENERATED WITH THE HELP OF AI

•	🌍 Deciding the region and universe of financial instruments to be traded is the first step in setting up the simulation environment for an Alpha.
•	💧 The liquidity of the stocks to trade is a critical factor, with highly liquid universes like top 500 or top 200 potentially being more challenging but also more valuable due to lower trading costs.
•	🕰️ The timing of the data used for the Alpha, referred to as Delay, can be set to use either yesterday's prices (Delay-1) or today's prices up to a chosen time (Delay-0).
•	⚖️ Decay is a setting that provides a weighted sum of the Alpha values for a specified number of past days, helping to remove major fluctuations or outliers.
•	🔄 Neutralization is an important setting when developing a long-short neutral Alpha, allowing the Alpha to be neutralized over a chosen group such as a market exchange or an industry.

## Transcript

It is very important
to decide the simulation environment
for each Alpha you create.
These simulation settings are like a checklist
you need to follow to ensure
you are doing the right thing.
The settings are very easy to customize
on the platform.
I will explain what each setting
does and how you should decide
upon the correct setting.
The first thing you need to decide is
the region and the universe you
want to trade.
Say you decide to trade the US
equities, the next step
would be to choose how many of
the most liquid stocks to trade.
For example, you might choose to
trade the USA top 3000
or the USA top 500.
It is relatively difficult to make an
Alpha for a highly liquid universe
like top 500 or top 200.
That's because the information
gets absorbed much faster
due to higher tradable volumes
available for these stocks.
But such Alphas are also
more valuable because
they have lower trading costs
attached to them. Next
simulation setting that you need to decide
is the timing of the data you
want to use for your Alpha.
We refer to it as Delay in the simulation
settings. Delay-1 uses
yesterday's prices. While Delay-0
uses today's prices
up to a chosen time during
the day. The next simulation
setting you need to set is
to decide if you want to use
some Decay for your Alpha.
Decay provides a weighted sum
of the Alpha values for a specified
number of days in the past.
it helps remove any major fluctuations
or outliers in the Alpha values
on any given day.
Decay helps if you want to use the previous
day's Alphas value.
You should use it if you think it
would be logical for your Alpha idea
or if you need to reduce your
Alpha's turnover.
The next very important setting
is using the neutralization.
When you're developing a long-short
neutral Alpha, you need to choose
the group in the simulation setting
you want to neutralize your Alpha over.
It could be a market exchange
or an industry.
This can also be done in the expression
box by using the IndNeut
operator, which gives
you the flexibility to define
your own group.
The next simulation setting is
the Truncation. Truncation helps ensure you
don't have a huge amount of capital
assigned to very few stocks
in your Alpha.
It also helps make sure that
the Alpha is diversified
and can survive different scenarios
in the financial markets.
We recommend setting this value
at or below 0.1,
which means you are trying to control
the exposure on any given
stock up to a level of
10%. The next simulation
setting is this simulation duration.
This setting signifies the duration
you choose to backtest your
Alpha idea.
We recommend using a window
of at least five years for your
simulation.
The next simulation setting you need
to look into is the lookback days.
Your Alpha idea usually needs
to use information from the past
to generate the current days
positions.
The number of lookback days must be set
greater than or equal to
the days your Alpha looks
back in the past.
