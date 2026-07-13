# Simulate your first Alpha

Source: https://platform.worldquantbrain.com/learn/documentation/create-alphas/running-your-first-alpha
Last modified: 2026-03-09T06:50:21.997260-04:00

[Alphas](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=A-,Alpha,-An) are created and simulated on the Simulate page in the Alphas dropdown tab. To run your first [simulation](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=definition.-,Simulation,-Simulation), click on the gear icon at the top right-hand side corner. This will open the settings panel. Here, select “US: TOP3000” for [Region](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=details.-,Region,-Set) and [Universe](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=U-,Universe,-Universe), “[Subindustry](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=SuperAlphas.%C2%A0-,Subindustry,-Sub)” for [Neutralization](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=strategy.-,Neutralization,-Neutralization) and apply your settings. Make sure both Code and Result are ticked by clicking on them. In the Alpha expression text box, enter -Delta(close, 5) for now and click on "Simulate". The Simulation Result page will show a graph for Cumulative Profit. This graph can be zoomed in to plot area for shorter time periods (1 month or 1 year).

The display consists of 2 graphs, one for [PnL](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=consultants-,Profit%20and%20Loss%20(PnL),-Profit) vs. Time and the other for [Sharpe Ratio](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=details.-,Sharpe%20ratio,-Sharpe) vs. Time.

In the Stats tab, a good Alpha tend to have consistently increasing PnL and high Annual Return, Sharpe Ratio, % Profitable Days and Profit per Dollar Traded. It should have low [Drawdown](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=today-,Drawdown,-Drawdown) and [Turnover](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=details.-,Turnover,-Average). And more importantly, it shouldn’t have high fluctuations in the cumulative profit graph. If the standard deviation is low, there tends to be lesser fluctuations in the graph. If the graph shows high fluctuations/volatility, despite the [returns](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=details.-,Returns,-Returns) being high, the Alpha will not be deemed good enough. An Alpha is considered to be “good” if:

- Its turnover is low, but not less than 1%

- Its Percentage Drawdown is less than 10%

- Its Sharpe is greater than 2.0 for [delay](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=days-,Delay,-An) 0 Alphas and greater than 1.25 for [delay](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=days-,Delay,-An) 1 Alphas
The graph above for Alpha expression -Delta(close, 5) shows several significant drawdowns, as well as a flattening of returns in 2017. The table below marks this Alpha as Inferior (Needs Improvement). PnL and Sharpe for 2017 drop low, and drawdown is large in 2014 and 2015. This Alpha is Inferior (Needs Improvement) due to high volatility and low returns.

```
{
  "settings": {
    "instrumentType": "EQUITY",
    "region": "USA",
    "universe": "TOP3000",
    "delay": 1,
    "decay": 0,
    "neutralization": "MARKET",
    "truncation": 0.08,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "language": "FASTEXPR",
    "maxTrade": "OFF",
    "maxPosition": "OFF"
  },
  "type": "REGULAR",
  "regular": "-ts_delta(close, 5)"
}
```

![stats](images/running-your-first-alpha--005-stats.png)

Use the green refreshing button in the Correlation block to get the information about the [correlation](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=locations.-,Correlation,-Correlation) of the currently simulated Alpha with the Alphas in your own [OS (Out-of-Sample)](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=details.-,Out-of-sample%20(OS),-Out) pool. This will be explained further on the [Simulation Results page](parameters-simulation-results.md).

The image below shows the Properties of the Alpha. You can name your Alpha, assign a category and color code, and add user-defined tags to them. You can add a brief description about your Alpha for your reference. Suggestion - keep the number of user-defined tags low so that they don't proliferate and are easily searchable in the My Alphas page.

![properties](images/running-your-first-alpha--007-properties.png)

To Submit Alpha for OS Test, click the "Submit Alpha" button in the [Submission](https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions#:~:text=details%C2%A0*).-,Submission,-The) tab of the results panel. This will check if the Alpha meets the [Correlation](https://platform.worldquantbrain.com/learn/documentation/interpret-results/parameters-simulation-results) and [Sharpe](https://platform.worldquantbrain.com/learn/documentation/interpret-results/parameters-simulation-results) criteria before submitting it.

Check out the below video for another example.
