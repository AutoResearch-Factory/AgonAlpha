# The Power of Diversity

Course: Combining Alphas and Risk Management
Category: Introduction
Duration: PT8M11S
Source: YouTube
Last modified: 2025-08-01T10:12:23.204089-04:00

## Description

Learn how to create diverse Alphas and the various techniques to combine them through an example.

## Transcript

The Power of Diversity

I'm Nitish Maini, the Chief Strategy Officer at WorldQuant. In my role, I help define the strategy of our firm and drive several cross-functional business initiatives, including new avenues for growth and innovation.

This series is your gateway to powering up your quant finance research skills, developing your mastery of quant research, and enabling you to implement what you learn on WorldQuant Brain as we go along.

In this video, we will focus on the power of diversity. So, let's log into Brain.

So far in the series, we have explored how to create alphas across various data types, holding periods, and idea categories. It is rare that a single alpha is strong enough to be used directly. Hence, quants often combine these signals to form stronger signals. Now, we are going to dive deeper into this combination process.

First, we will understand what types of signals, when combined, can result in robust ideas, and then explore combination techniques that can maximize the robustness of a strategy.

Let's get started. We will be leveraging WorldQuant Brain to demonstrate the combination of alphas.

As a reminder, WorldQuant defines an alpha as a mathematical model that seeks to predict the future price movement of various financial instruments.

Many financial models have been developed over the years, such as the Capital Asset Pricing Model, the Security Market Line, the Two-Fund Theorem, and Harry Markowitz's mean-variance optimal portfolios. But one core principle remains consistent throughout: diversity is the cornerstone of quant research. The reason is simple—the more diverse our signals are, the better the risk-adjusted returns, or Sharpe ratio, of our approaches may be.

This graph demonstrates concepts of risk and return, and most importantly, their interaction. Risk and return refer to the idea of combining securities to achieve the greatest possible return for a given level of risk. This chart is a theoretical illustration of the efficient frontier, where the y-axis represents expected return and the x-axis indicates risk as standard deviation. Each point on this graph represents a different portfolio constructed by combining securities in different ratios. The parabolic line joining these portfolios is the efficient frontier. The minimum variance portfolio is, as the name suggests, the portfolio plotted on the efficient frontier that exhibits the lowest risk.

Why is this the case? According to the theory, when we combine alphas that have low correlation (less than 0.5), the fluctuations in one alpha's returns are offset by variations in other low-correlated alphas. This diversity may result in lower volatility for the targeted returns of the portfolio, leading to a better Sharpe ratio.

Also, lower correlation leads to lower turnover, as the buy-sell positions of one alpha offset another alpha's positions. This decreases the overall turnover of the portfolio without significantly impacting other performance metrics. The result could be better after-cost performance, after factoring in trading costs.

Diversity can be achieved by using different underlying data, creating diverse alphas, and combining alphas in different ways. Let's expand a little more on each.

Alphas, or predictive models, are created using available information. The more and different information we have, the more diverse the alphas. This information is captured via various data categories. Alphas created using different data categories can be valuable in how novel they are to each other. Some of the data categories include sentiment, analyst, options, or model data, etc.

There are many dimensions to how you can diversify your alphas. Some of them include:

The variety of trading ideas,
The diversity in functions used, such as time series functions or cross-sectional functions.
Time series functions process data from a single company over a span of time. For instance, calculating the average revenue of a company over the past five years. On the other hand, cross-sectional functions analyze a snapshot of data from multiple companies at a specific point in time. An example would be calculating the average revenue of healthcare sector companies in the current month.

Let's try these ideas out. You can also diversify by using different holding periods or turnover buckets—for example, low turnover (less than 5%), medium turnover (5% to 15%), and high turnover (more than 15%)—or by building a pool of alphas created by different authors.

We can also diversify by using different combination techniques:

Equal-weighted combination: This method simply averages the alpha positions each day.
Risk parity technique: This combines alphas so that each alpha is allocated the same amount of risk in the portfolio.
Correlation-weighted combination: Here, we give more weight to novel alphas that have lower correlation within the pool.
Mean-variance optimization: This approach favors alphas with better risk-adjusted performance in the recent past.
To illustrate the power of diversity, let's filter for medium-turnover and low-correlation alphas on the Brain platform. We will combine 250 such alphas using an equal-weight strategy to form a single super alpha. The Sharpe ratio of the super alpha is significantly higher than any component alpha due to enhanced returns and lower volatility.

A return-to-drawdown ratio above 1 is considered good. This super alpha has a ratio of 13 because the combination of 250 components increases returns and reduces drawdowns, leading to a strong improvement in the returns-to-drawdown ratio.

In summary: We explored how diversity in a pool of alphas can strengthen portfolio construction. Lower volatility, decreased turnover, and improved after-cost performance are just some of the potential benefits. We have learned how to create diverse alphas, the various techniques to combine them, and seen one such technique in action.

In our next video, we will look at different models to manage risk in our research.

Let's go quant—see you in Brain.
