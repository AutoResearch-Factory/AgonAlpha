# Intermediate Pack - Understand Results [1/2]

Source: https://platform.worldquantbrain.com/learn/documentation/discover-brain/intermediate-pack-part-1
Last modified: 2025-09-08T05:22:10.878298-04:00

This Intermediate guide aims to further your understanding of the Alphas you have simulated. The documentation will provide you with an in-depth understanding of commonly used operators and get you up to speed to improve your ability to create a high-performing Alpha.

## Understanding Your Results

Cumulative PnL Chart

![Cumulative PnL Chart](../images/intermediate-pack-part-1--004-cumulative-pnl-chart.png)

If you’ve followed the examples in the Starter pack, chances are you’ve ended up with the first 2 graphs. What both graphs have in common is that they have multiple periods of significant losses, producing a graph with high fluctuations. This means that your simulated portfolio could lose a large percentage of its value in one day, and that wouldn’t be ideal. Rather, a good Alpha should produce a steadily rising PnL chart (3rd graph) with few fluctuations and no major drawdown.

In-sample (IS) Summary

In-sample simulation uses data over a 5-year timeframe, and tests out how well your Alpha performs in the historical period. After the simulation, you will see the IS Summary row with 6 metrics: Sharpe, Turnover, Fitness, Returns, Drawdown, and Margin.

![pic_155.png](../images/intermediate-pack-part-1--006-pic_155.png)

Sharpe

This ratio measures the excess return (or risk premium) per unit of deviation of returns of an Alpha. It takes the mean of the PnL divided by the standard deviation of the PnL. The higher the Sharpe Ratio or Information Ratio (IR), the more consistent the Alpha’s returns are potentially likely to be, and consistency is an ideal trait. The passing requirement for Sharpe on BRAIN is to be above 1.25.

$$
Sharpe =\sqrt{252} * \left(\frac{Mean(PnL)}{Stdev(PnL)}\right)
$$

Turnover

Turnover of an Alpha is metric that measures the simulated daily trading activity, i.e., how often the Alpha trades. It can be defined as the ratio of value traded to book size. The higher the turnover, the more often a trade occurs. Since trading incurs transaction costs, reducing turnover is generally an ideal trait. The passing requirement for turnover on BRAIN is to be between 1% and 70%.

$$
Turnover= \frac{Dollar Trading Value}{Booksize}
$$

Fitness

Fitness of an Alpha is a function of Returns, Turnover & Sharpe. Fitness is defined as:

$$
Fitness =Sharpe *  \sqrt{\frac{abs(Returns)}{max(Turnover,0.125)}}
$$

Good Alphas generally have high fitness. You can seek to improve the performance of your Alphas by increasing Sharpe (or returns) and reducing turnover. The passing requirement for fitness on BRAIN is to be greater than 1.0.

Returns

Returns is the amount made or lost by the Alpha during a defined period and is expressed in percentages. BRAIN defines returns as:

$$
Annual Return = \frac{Annualized PnL}{0.5 *  Book Size}
$$

Drawdown

Drawdown of an Alpha is the largest reduction in simulated PnL during a given period, expressed as a percentage. It is calculated as follows:

$$
Drawdown = \frac {Dollar Amount Of Largest Peak To Trough Gap In PnL}{0.5 * Book Size}
$$

Margin

Margin is the simulated profit per dollar traded of an Alpha; calculated as:

$$
Margin = \frac{PnL}{Total Dollars Traded}
$$

## Passing IS Stage and Troubleshooting

![pic2.png](../images/intermediate-pack-part-1--020-pic2.png)

- One of the most common challenges users face is Low Sharpe, and users commonly see that their Sharpe ratio is below the specified cutoff. How do you get a higher Sharpe? We suggest that you can either increase you Alpha return or reduce your volatility. Read more [here](https://support.worldquantbrain.com/hc/en-us/community/posts/8123350778391-How-do-you-get-a-higher-Sharpe-).

- Another challenge is the weight test that measures the capital concentration in each stock. You might see these error messages in your IS tests: “Maximum weight on an instrument is greater than 10%” OR “Weight is too strongly concentrated” OR “Too few instruments are assigned weight.” Common fixes to this include: Adding range-normalized functions such as rank, setting truncation at 0.1, and using ts_backfill. Read more [here](https://support.worldquantbrain.com/hc/en-us/community/posts/8419305084823--BRAIN-TIPS-Weight-Coverage-common-issues-and-advice).

- Another difficulty is that the Sub-universe Sharpe is not above cutoff. This means that the Sharpe in the sub-universe must be higher than at least one threshold. There are 2 thresholds that scale down Sharpe with sub-universe size.

![threshold main.PNG](../images/intermediate-pack-part-1--022-threshold-main.png)

Thus, you can try to improve the Sub-Universe Sharpe by increasing the Universe of instruments (i.e. selecting Top3000).

## Common Error Messages

Syntax error in expression.

Check your spelling of the data fields and operators and ensure that your expression is logical. The tokens (operators and keywords) allowed in your Alpha expression can be found in the [Available Market Data](https://platform.worldquantbrain.com/data) and [Available Operators](https://platform.worldquantbrain.com/learn/data-and-operators/operators) pages. Alpha expressions also accept integers and floating point numbers.

Incompatible unit for input at index 0, expected "Unit[]", found "Unit[CSPrice:1]"

Unit warnings are provided for reference in simple cases and do not prevent submission. Usually, this warning appears when data fields having two different units are added or multiplied. E.g. if you add "close" to "cap". "close" has units of price but "cap" has units of price*shares. You can safely ignore these warnings if you're sure the Alpha correctly handles data units.
