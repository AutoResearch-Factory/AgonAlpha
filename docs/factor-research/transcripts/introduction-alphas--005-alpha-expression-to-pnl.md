# Alpha expression to PnL Chart

Course: Introduction to Alphas
Category: Introduction
Duration: PT11M22S
Source: YouTube
Last modified: 2026-06-02T07:16:03.223370-04:00

## Description

This video shows the calculations that translate the alpha expression into the cumulative PnL chart

## Transcript

This video assumes that you have already watched the "Getting Started with Brain" course videos 1, 2, and 3.
If you haven't done this yet, I suggest you go back and watch those videos first.

In the preceding videos, we showed that after you type an alpha expression into the simulate window and press the "Simulate" button, a profit and loss (PnL) chart is generated that corresponds to that alpha expression. The Brain platform does this automatically, but we want to give you a brief glimpse of what happens in the background—what calculations are happening that translate the alpha expression and create the cumulative PnL chart.

Even though you will never need to do these calculations yourself, developing an intuition for them will help you in the alpha-making process.

Let's illustrate this using the alpha example **rank of negative returns**.
The hypothesis in this expression is that we want to buy (go long) on those stocks tomorrow that had negative or comparatively lower returns today, and we want to sell (go short) those stocks tomorrow that had positive or comparatively higher returns today. This is a very basic example of a reversion idea.

We have used the **rank** operator here, which ranks the input values inside the operator and returns values equally distributed between zero and one.

When you click "Simulate" and input the simulation settings, the Brain simulator takes a long or short position for each financial instrument and generates the PnL chart you see. Behind the scenes, seven steps or operations are performed before the final PnL chart is generated.

Normally, in an alpha simulation, there would be between 200 and 3,000 stock instruments in the universe. But to better understand this concept, we will assume a hypothetical scenario in which the simulation universe has only eight stocks.

We simulate the expression "rank of negative returns" with market neutralization, delay-1, and decay-0 settings for now.

- **Column B**: The eight stocks in the alpha vector.
- **Column C**: The returns of the stocks as of, let's say, February 1. These serve as the input data for the alpha expression "rank of negative returns."

**Step 1:**
The first step in the process is to evaluate the alpha expression for each stock to generate the alpha vector for the given date. Since we have assumed delay-1 settings, this date would be February 2. The delay-1 setting uses data as of T-1 date to create the alpha vector as of T date.

To produce the alpha vector, the simulator performs the rank operation on negative returns and produces a vector of values corresponding to each stock. The resulting vector depends on the operators used in the alpha expression. Since we have used the rank operator, we see equally distributed values between zero and one in **column D**. Note that the stock with the lowest return has the highest value and vice versa, in line with our hypothesis.

**Step 2:**
The second step is to subtract the average of the vector values in the group from each value in the vector so that the sum of all values in the vector is zero. This is called **neutralization**. The group can be the entire market, or you can perform this neutralization operation on sector, industry, or sub-industry groupings of stocks.

In our example, since we have only eight stocks in the simulation universe, we have assumed neutralization over the market. So, we take the average of the numbers in cell D12 and subtract the average from each stock. This gives us a new vector in **column F**. Note that both the sum and average of these numbers are equal to zero. Also, the sum of positive values is equal to the sum of negative values.

**Step 3:**
In step three, the resulting values are then **scaled or normalized** so that the absolute sum of the values in the alpha vector is one. Here, we sum the absolute values of each row and find the sum, which is 2.3. Then, we divide each row by this sum, which results in normalized values. By "normalized," we mean that the total absolute sum of **column H** is one. We can also call this vector a normalized vector of weights.

**Step 4:**
In the next step, using these normalized weights, the Brain simulator allocates capital to each stock from a fictitious book of $20 million and constructs a portfolio. **Column G** has a total of $20 million of fictional money allocated to the stocks using the normalized weights in **column H**.

This means we have a position of minus $4.4 million in stock one (i.e., we have shorted $4.4 million worth of stock one) and a long position of $0.6 million in stock five (i.e., we have invested $0.6 million in stock five). This is a result of long-short market neutralization and is the backbone of creating these predictive models, or alphas, on Brain. With this technique, a strategy can have the potential to be profitable regardless of the direction of the market.

**Step 5:**
We calculate the daily PnL generated by the alpha based on the observed stock returns of the next day. After allocating dollar positions on the stocks, we calculate the PnL generated by each stock based on the returns each stock had that day.

Suppose the actual returns on these stocks as of February 2 are shown in **column K**. We see that although we expected stock one and stock two to fall in price, they actually went up, so we had a loss as shown in **column L**. We also expected stock six to go up in price, but it stayed flat, so we were wrong in general about three stocks, but we were right about five. In total, we made a gain of $0.03 million on this day with our alpha, which is calculated by adding the PnLs of all the stocks in our vector.

This is how the simulator calculates the PnL generated by the alpha for any given date.

**Step 6:**
We repeat the same process from step one to step five for each date in a several-year history span, also called the **in-sample period** or the IS period, to calculate the daily PnL generated by the alpha for each day in the IS period.

**Step 7:**
From this, the simulator calculates the alpha's accumulated PnL from the start to the end of the IS period to get the alpha's accumulated PnL chart. This can be better understood with the help of the PnL chart of the alpha we simulated earlier.

In this chart, we have a period of five years from February 2016 to January 2021. Using the steps we discussed in our example, the simulator would calculate the daily PnL of the alpha and derive the cumulative PnL chart as we see here.

Note that the two years from February 2021 to January 2023 are not visible to us in the simulation window; that's called the **out-of-sample** or OS period. After you submit an alpha, several tests are run to analyze the alpha's performance in the OS period. An alpha that passes both the in-sample as well as the out-of-sample test can be said to be a robust alpha.

This is how the Brain simulator creates the PnL chart from an alpha expression.

In our example, we have assumed that we are using market neutralization and decay-zero settings. But if you use any other neutralization settings, similar operations would be performed on the alpha. For example, if we have 80 stocks in the simulation universe consisting of 10 groups or industries with eight stocks each, the simulator would perform these operations on each of the 10 groups and finally add the PnL from each group to get the daily PnL of the alpha and create the cumulative PnL chart.

However, if we introduce **decay** into our alpha settings, an additional step must be performed to get the final alpha vector. Suppose we use a decay of three in our simulation settings. The final vector of weights in the alpha would be calculated by combining today's values with the previous day's decayed value.

In our example, we calculated the normalized weight in our alpha as of February 2. Let's assume that the normalized weights of stocks in the alpha vector as of February 1 and January 31 are as shown in columns N and O, respectively. Then, the final weights in the alpha would be calculated using the given weighted average formula in column P. Using this new derived vector, the simulator would calculate the daily PnL and, consequently, the cumulative PnL chart.

Note that even if decay is used, more weight is assigned to the most recent values. Decay is a very important factor in reducing transaction costs or turnover, as it includes information from previous days as well, preventing the alpha from being overly reactive.

**To summarize:**
Once we input the alpha expression and the simulation settings in the Brain simulator, it performs the operations we discussed in this video to take long or short positions for each financial instrument and generate the PnL chart.

Now, I suggest that you move to videos four and five to learn more about how to interpret the PnL chart and the accompanying statistics.
