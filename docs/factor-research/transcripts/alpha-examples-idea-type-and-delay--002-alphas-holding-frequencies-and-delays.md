# Alphas by Holding Frequencies and Delays

Course: Alpha Examples by Idea type and Delay
Category: Getting Started
Duration: PT7M2S
Source: YouTube
Last modified: 2025-08-01T10:16:41.002744-04:00

## Description

Learn about the  holding periods in quant finance and the importance of delayed data to prevent look-ahead bias through an example.

## Transcript

Alphas by Holding Frequencies and Delays**

As a reminder, WorldQuant defines an alpha as a mathematical model that seeks to predict the future price movement of various financial instruments.

I'm Nitish Maini, your partner in learning about quant finance research. I'm the Chief Strategy Officer at WorldQuant. In my role, I help define our firm's strategy and drive several cross-functional business initiatives, including new avenues for growth and innovation.

In this video, we will focus on the role played by holding frequencies and data delays.

**Holding frequency** is the total length of time an investor expects to hold a portfolio or security. The holding period has implications on risk, returns, and transaction costs.

**Data delay** refers to the time before which the alpha is allowed to use the data in its backtest. More recent data contains up-to-date information, which may benefit alpha performance, but data delay helps ensure there are no look-ahead biases—an important concept we will explain in depth in this video.

If an alpha uses data from the day before the date of the backtest, I will call it a **delay-1 alpha**. If the alpha uses today's price up to a chosen time during the day for simulation to run after that time, I will call it a **delay-0 alpha**, because it uses same-day information.

We will also put our ideas to the test on WorldQuant Brain, our cloud-based platform where we can get real-time feedback. If you would like to try this as I explain these ideas, log into Brain now.

Alphas can be classified into three categories based on the holding period:

1. **Medium- to low-frequency alphas:**
   These are alphas with holding periods that range from a few days to months, and sometimes even longer.

2. **Intraday trading alphas:**
   These update positions much more frequently, ranging from every minute to a few hours. They are typically based on price-volume signals to capitalize on short-lived price patterns. They can also use news data, earnings announcements, or faster intraday data like sentiment or options.

3. **High-frequency trading (HFT) alphas:**
   These hold positions from nanoseconds to a few seconds. HFT signals can be market-making strategies that provide market liquidity, or price arbitrage strategies that capitalize on price discrepancies between related assets or markets. They can also take short-term directional trades based on price patterns, such as short-term momentum.

It is important to prevent biases in the data during backtesting. **Look-ahead bias** happens when you use future information in your analysis that wouldn't have been known or available during the period being analyzed. This bias can lead to over-optimistic performance predictions that don't hold up in reality, skewing our expectations and potentially leading to costly surprises.

To avoid look-ahead bias, quants use delayed data in the backtest. **Delay-1 alphas** use yesterday's price. **Delay-0 alphas** use today's price up to a chosen time during the day. Theoretically, delay-0 alphas are expected to perform better than delay-1, but have lower trading capacity due to the shorter time available to trade.

We have reviewed several delay-1 alphas in our previous videos, so let's shift to a delay-0 example.

We will use volatility data, focusing on **at-the-money implied volatility** of call options expiring within four months, and their **Parkinson's volatility**. Parkinson's volatility measures realized volatility using the high and low prices within a day. It captures large intraday price variations, even when the previous day's close and the current day's close price change is small. The **strike price** is where the call option starts making a profit, and **implied volatility** represents the expected future stock movement, highly influenced by option demand. At-the-money implied volatility aggregates implied volatilities of call options where the strike price equals the stock's current price, and the option expires within four months.

Our alpha idea captures call option demand using the implied volatility of its at-the-money call options expiring up to four months ahead, scaled by Parkinson's volatility over the past four months. If the implied volatility to Parkinson's volatility ratio is high, the hypothesis is that we expect high future stock returns, and vice versa.

Now, let's implement this idea on WorldQuant Brain using its proprietary expressions language. In this example, we simply take the ratio of the implied volatility of at-the-money call options to Parkinson's volatility for the stock, using the data fields on the Brain platform. These delay-0 values are available by the cutoff time each day in the markets for the alpha to generate positions.

The results show a consistent Sharpe ratio of about 2 across years, 14% gross returns, a 1.2% return-to-drawdown ratio, 29% turnover, and decent coverage across the selected universe.

In this video, we learned about three holding periods in quant finance, the importance of delayed data to prevent look-ahead biases, and reviewed a delay-0 alpha example. In the next video, we will discuss the power of diversity of alphas. Step by step, I hope you are powering up your knowledge and testing out your ideas with me.

Let's go quant—see you in Brain.
