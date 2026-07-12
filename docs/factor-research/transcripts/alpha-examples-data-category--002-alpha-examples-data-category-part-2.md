# Alpha Examples by Data Category: Part 2

Course: Alpha Examples by Data Category
Category: Alpha Tutorials
Duration: PT7M34S
Source: YouTube
Last modified: 2025-08-01T10:20:14.183520-04:00

## Description

Explore Options and Sentiment data with Alpha examples.

## Transcript

Alpha Examples by Data Category, Part 2

I'm Nitish Maini, your partner in learning more about quant finance research. By day, I am the Chief Strategy Officer at WorldQuant. In my role, I help define the firm's strategy and drive several cross-functional business initiatives, including new avenues for growth and innovation.

Quants, in our last video, we explored alpha examples by data categories. Let's continue with the next set of categories.

The next category is **sentiment data**. Sentiment data quantifies the emotions of the masses towards a stock or the market in general. The data are captured from various mediums like social media channels, news, and blogs. Quant researchers monitor popular opinion in an effort to predict the direction of movement in stock prices and the intensity underlying these sentiments. They also analyze **sentiment buzz**—the degree of activity or attention investors are giving to a particular stock.

Let's review an example for such an alpha on Brain, our simulation platform.

Remember, at WorldQuant, we define an alpha as a mathematical model that seeks to predict the future price movement of various financial instruments. The hypothesis for this alpha idea is that if a stock's sentiment buzz is rising compared to its historical average, it means the stock is attracting higher investor attention lately and is possibly overpriced. So, we expect lower future returns and short the stock. Conversely, we go long on stocks with falling buzz, anticipating higher future returns.

Now, let's implement this idea on WorldQuant Brain with the proprietary expression language. By the way, you can access all data categories discussed in this series on Brain.

We compute the ratio of today's sentiment buzz for a stock to the mean over the last 10 trading days (or two calendar weeks) using the time series mean function. Values greater than 1 indicate an increasing trend in sentiment buzz. We apply a negative sign before the expression to express our bearish outlook for stocks with increasing recent buzz.

The backtesting simulation runs for the previous five years to generate an alpha vector for each day in the simulation. If the value for a stock is negative, it shorts the stock and goes long on stocks with positive values. We simulate the expression on the top 200 US stocks based on liquidity and on delay-1 data to prevent any look-ahead bias. We neutralize the alpha over the industry, apply a decay of 10 to smooth out any noise in the buzz data, and restrict the maximum capital on a single stock to 1%.

The results show a consistent Sharpe ratio of 1.6 across years, returns over 9%, and decent coverage across the selected universe.

The last data category we will explore is **options**.

Options are contracts within the derivatives market that give the right, but not the obligation, to buy or sell an underlying security at a specific strike price. While the world of options can be complex, in this example, we will focus on extracting information from equity options, particularly focusing on a metric called **implied volatility**. Implied volatility is the expected future fluctuation in the price of the underlying stock. It is computed using multiple variables like the price of options, time to expiry, interest rates, strike prices, etc. Higher option prices generally lead to higher implied volatility, reflecting increased demand for the option.

When the price of the stock moves above the strike price, the holder of a call option makes a profit. When the price of the stock goes below the strike price, the holder of a put option makes a profit. For our analysis, we use implied volatility derived from at-the-money call and put options. An **at-the-money option** is one whose underlying asset price is very close to the strike price of the option.

The idea of our alpha is based on capturing the difference in the demand for at-the-money call and put options, as measured by their implied volatility over a long horizon, to capture longer-term trends in stock prices. This leads us to a hypothesis:
If implied volatility derived from call options expiring up to two years in the future is higher than the implied volatility derived from put options expiring up to two years in the future, then the demand for the stock exceeds its supply, and we expect the stock price to appreciate in the future. We go long on such stocks. For stocks where the difference in implied volatility is negative, we have a bearish outlook and go short.

Now, let's discuss how our idea is implemented using Brain's expression language. We store our call and put options implied volatilities in two variables, IV_call and IV_put, respectively. Our alpha captures the net demand of the stock as the difference in the implied volatilities.

We simulate the expression on the top 3,000 US stocks based on liquidity and on delay-1 data to prevent any look-ahead bias. We neutralize the alpha over the industry, apply a decay of 7 to smooth the signal, and restrict the maximum capital on any single stock to 1%.

The results show a consistent Sharpe ratio of around 2 across years, returns of 14%, a return-to-drawdown ratio of 3, turnover of 25%, and decent coverage across the selected universe.

To improve alpha performance, we can consider trends in other variables from options trading, like open interest and options volume, which are indicative of the demand for the underlying stock.

In this video, we explored sentiment and options data categories with corresponding alpha examples. In our next video, we are going to explore alphas categorized by idea type.

Let's continue our quant research journey together. Quant on with me!
