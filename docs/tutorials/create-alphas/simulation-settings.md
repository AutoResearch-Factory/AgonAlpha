# How to choose the Simulation Settings

Source: https://platform.worldquantbrain.com/learn/documentation/create-alphas/simulation-settings
Last modified: 2025-11-05T03:49:33.672757-05:00

The settings panel can be found by clicking the Settings button at the top right hand corner of the Simulate page. You can specify parameters like language, instrument type, universe, delay, neutralization, etc., which will be applied to your next simulation after clicking the "Apply" button.

## Language

Fast Expression is available on BRAIN. To learn more, refer to the [Available Operators](../../syntax/operators.md).

## Instrument type

Only Equity instrument type can be used at the moment

## Region and Universe

The only region currently available to all BRAIN users is the US market. The regions Europe and Asia are currently available only to our research consultants.

Universe is a set of trading instruments prepared by BRAIN. For example, "US: TOP3000" represents the top 3000 most liquid stocks in the US market (determined by highest average daily dollar volume traded).

## Delay

Delay refers to the availability of data, relative to decision time. In other words, delay is the assumption of when we can trade stock once we decide on a position.

Assume that you are looking at the data today before market close and you decide that you want to buy stock. We can choose an aggressive approach and trade stock in the time left till market close. In this case, the position is based on data available on the same day (today). This is called Delay 0 simulation.

Alternatively, we could choose a conservative trading strategy and trade stock the next day(tomorrow). Then the position is achieved tomorrow and it is based on today’s data. In this case, there is a lag of 1 day. This is called Delay 1 simulation. In expression language, delay is applied automatically and you do not have to bother about it.

## Decay

This performs a linear decay function over the past n days by combining today’s value with previous days’ decayed value. It performs the following function:

$$
Decay\_linear(x,n)=\frac{x[date]*n +x[date-1]*(n-1)+...+x[date-n-1]}{n+(n-1)+...+1}
$$

Legal values for Decay: Integer 'n' where n >= 0. NOTE: Using negative or non-integer values for Decay will break simulations.

Tip: Decay can be used to reduce turnover, but decay values that are too large will attenuate the signal.

## Truncation

The maximum weight for each stock in the overall portfolio. When it is set to 0, there is no restriction.

Legal values for Truncation: Float 'x' where 0 <= x <= 1 (NOTE: Any values for Truncation outside this range can impact/break simulations.)

Tip: Truncation aims to guard from being too exposed to movements in individual stocks. The recommended setting is between 0.05 and 0.1 (entailing 5-10%).

## Neutralization

Neutralization is an operation used to make our strategy market/industry/sub-industry neutral. When Neutralization = “Market” it does the following operation:

Alpha = Alpha – mean(Alpha)

where Alpha is the vector of weights.

Basically, it makes the mean of the Alpha vector zero. Thus no net position is taken with respect to the market. In other words, the long exposure cancels out the short exposure completely, making our strategy market neutral.

When Neutralization = Industry or Subindustry, all the instruments in the Alpha vector are grouped into smaller buckets corresponding to industry or sub-industry and neutralization is applied separately to each of the buckets. For illustration of industry/subindustry classification, see [GICS](https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard) (note: this is not necessarily the same classification standard used by BRAIN platform).

To learn more about Neutralization, refer the [Neutralization FAQ](https://support.worldquantbrain.com/hc/en-us/sections/4418582007959-Neutralizing-Alphas) section.

![settings_view](../images/simulation-settings--018-settings_view.png)

## Pasteurize

![simulation_settings_pasteurize.png](../images/simulation-settings--020-simulation_settings_pasteurize.png)

Pasteurization replaces input values with NaN (pasteurizes) for instruments not in the Alpha universe. When Pasteurize = ‘On’, inputs to will be converted to NaN for instruments not in the universe selected in Simulation Settings. When Pasteurize = ‘Off’, this operation does not happen and all available inputs are used.

Pasteurized data has non-NaN values only for instruments in the Alpha universe. While pasteurized data contains less information, it may be more appropriate when considering cross-sectional or group operations. The default Pasteurize setting is ‘On’. Researchers can switch it to ‘Off’ and use pasteurize(x) operator for manual pasteurization.

Example

Assume the following settings are used: Universe TOP500, Pasteurize: ‘Off’. The following code calculates the difference between sector rank of sales_growth in Alpha universe and sector rank of sales_growth among all instruments:

```
{
  "settings": {
    "instrumentType": "EQUITY",
    "region": "USA",
    "universe": "TOP3000",
    "delay": 1,
    "decay": 4,
    "neutralization": "MARKET",
    "truncation": 0.01,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "language": "FASTEXPR",
    "maxTrade": "OFF",
    "maxPosition": "OFF"
  },
  "type": "REGULAR",
  "regular": "group_rank(pasteurize(sales_growth),sector) - group_rank(sales_growth,sector)"
}
```

The pasteurize operator in the first group_rank pasteurizes input to the Alpha universe (TOP500), while the second group_rank ranks sales_growth among all instruments.

## Nan Handling

![simulation_settings_nan_handling.png](../images/simulation-settings--025-simulation_settings_nan_handling.png)

NaNHandling replaces NaN values with other values. If NaNHandling: ‘On’, NaN values are handled based on operator type. For time series operators, if all inputs are NaN, 0 is returned. For group operators returning one value per group (e.g. groupmedian, groupcount), if the input value for an instrument is NaN, the value for the group is returned.

If NaNHandling : ‘Off’, NaNs are preserved. For time series operators, if all inputs are NaN, NaN is returned. For group operators, if the input value for an instrument is NaN, NaN is returned. Researchers should handle NaNs manually in this case. The default setting NaNHandling value is ‘Off’. Some ways to manually handle NaN values can replicate “On” behavior.

Example

```
{
  "settings": {
    "instrumentType": "EQUITY",
    "region": "USA",
    "universe": "TOP3000",
    "delay": 1,
    "decay": 4,
    "neutralization": "MARKET",
    "truncation": 0.01,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "language": "FASTEXPR",
    "maxTrade": "OFF",
    "maxPosition": "OFF"
  },
  "type": "REGULAR",
  "regular": "ts_zscore(etz_eps, 252)"
}
```

Assume NaNHandling = ‘On’. Then for a stock with etz_eps == NaN for all 252 days, 0 is returned. However, ts_zscore(x, d) also returns 0 when x == tsmean(x, d), which is different from x == NaN (“no data is available”). This means that NaNHandling = ‘On’ increases coverage, but may introduce ambiguous information into the Alpha.

If NaNHandling = ‘Off’, NaNs can be handled other ways:

is_nan(ts_zscore(etz_eps, 252)) ? ts_zscore(est_eps, 252) : ts_zscore(etz_eps, 252)

Here, est_eps is used when etz_eps has NaN value for all 252 days.

Example

```
{
  "settings": {
    "instrumentType": "EQUITY",
    "region": "USA",
    "universe": "TOP3000",
    "delay": 1,
    "decay": 3,
    "neutralization": "NONE",
    "truncation": 0.01,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "language": "FASTEXPR",
    "maxTrade": "OFF",
    "maxPosition": "OFF"
  },
  "type": "REGULAR",
  "regular": "groupmax(sales, industry)"
}
```

When NaNHandling = ‘Off’ and sales is NaN for a given instrument, the operator’s output is NaN. When NaNHandling = ‘On’ and sales is NaN for a given instrument, the operator’s output is the maximum value of sales in the instrument’s industry.

## Unit Handling

Unit Handling option allows raising a warning when incompatible units are used in an operator. This warning appears if expression uses data fields that are incompatible, for example, a warning will be shown for an attempt to add price to volume.
