# IQC Scoring: Merged Alpha Performance criteria

Course: International Quant Championship 2026
Category: Introduction
Duration: PT12M21S
Source: YouTube
Last modified: 2026-05-26T11:07:48.814613-04:00

## Description

Overview of IQC scoring criteria

## Transcript

Hi, everyone.

Welcome to another video related to the International Quant Championship (IQC).
If you and your teammates have just registered for the IQC, you might be wondering how the scoring works. Some of you may have already started submitting alphas and are curious about how to improve your score and climb up the leaderboard. Don’t worry—we have you covered in this video.

Let’s understand how IQC scoring works.

Unlike the WorldQuant Challenge, where individual alphas are scored with a limit of 2,000 points per day, scoring in the International Quant Championship is structured differently. The scoring is based on the **merged alpha performance** of your team.

Before we go into the details of the scoring, let’s understand what **merged P&L** means.
Merged P&L is the P&L chart generated after combining the performance of all the individual alphas submitted by you and your teammates in the IQC. Your merged alpha performance score is calculated from this merged P&L chart.

The illustration here should help you understand how the merged P&L chart is generated. When you submit your first IQC alpha, your merged P&L chart will be the P&L chart for that single alpha. After your first submission, you can see how your merged P&L chart and score would look based on the alphas you have submitted, and how it would change if you submit more alphas.

The merged P&L chart is generated assuming **equal weight** on all the submitted alphas of your team. From this merged P&L chart, your merged performance score is calculated and is largely a function of three parameters:

1. **Merged Performance Sharpe Ratio:**
   The Sharpe ratio measures the return on an investment compared to the level of risk taken. The higher the Sharpe, the better the score, assuming all other parameters are the same.

2. **Merged Performance Return-to-Drawdown Ratio:**
   Drawdown is the largest reduction in P&L during a given period, expressed as a percentage. The larger the merged performance return-to-drawdown ratio, the better the score.

3. **Merged Performance Turnover:**
   Turnover is the average measure of daily trading activity. Alphas with low turnover have lower transaction costs. Thus, the higher the merged performance turnover of your alphas, the lower the score, assuming all other parameters are the same.

It is essential to balance these parameters in your merged alpha performance. For example, an alpha with high turnover or transaction costs must be compensated with a comparatively higher Sharpe ratio.

You can think of merged performance as simulating a diverse pool of alphas to get an overall merged performance for your team. This merged performance can be optimized by working on new and diverse ideas.

Every time you simulate an alpha on the platform, you can see your merged performance score on the **Performance Comparison** tab within the alpha simulation results, just below the correlation and in-sample testing status tab. When you click **Refresh**, you can see both your current score and how the simulated alpha would impact your merged performance score if you decide to submit it.

Be aware that submitting alphas that do not add value to your already existing pool of submitted alphas can reduce your merged performance score, as shown in the illustration. By "not adding value," we mean the alpha does not contribute to improving the overall performance parameters of your merged alpha.

In addition to the scores, you can also see the merged performance metrics of your merged P&L chart. As shown here, you can see the Sharpe ratio, turnover, and other metrics of your merged P&L chart should you decide to submit the simulated alpha.

Note that an increase in the merged P&L returns by itself does not necessarily imply an increase in the merged performance score. The score is a function of various parameters of the merged performance of alphas submitted by your team, as we saw earlier.

During **Stage 1** of the International Quant Championship, only the **in-sample merged performance** of alphas is used to calculate the scores on the leaderboard.
While in **Stage 2**, **out-of-sample (OS) performance** is also taken into account to calculate the final score.

If you’re new to Brain and wondering what in-sample and out-of-sample performance mean, I suggest you go through the Introduction to Alpha course in the Learn section. For a brief explanation:

- **In-sample model performance** is the result you see on the platform after the alpha simulation is completed. This is derived from only the data visible to you at the time of building your alpha. For example, only data from March 2016 to February 2021 may be visible.
- **Out-of-sample model performance** displays how your alpha performs on data not visible to you—such as the two years after February 2021. Measuring out-of-sample performance is important to avoid overfitting your model to the data. A robust model would have OS performance similar to in-sample performance.

During Stage 1, only your in-sample delay-1 and delay-0 performance drives your score. Note that the merged performance scores for delay-1 and delay-0 alphas are calculated separately, and the final score is calculated according to the formula you see here. So make sure you submit both delay-1 and delay-0 alphas.

During Stage 2, OS scores are also considered to calculate the final scores on the leaderboard. For this, both the in-sample and out-of-sample scores are scaled and make equal contributions to the final score. Note that all alphas submitted by your team since the start of Stage 1 are considered for scoring during Stage 2.

As you submit alphas, you should see your team climb up the global IQC leaderboard. You can filter the leaderboard results to view how you are performing within your own university and your country. You can also see the separate delay-1 and delay-0 scores of the teams on the leaderboard and compare where you stand versus your competition.

**To help you climb the leaderboard, here are a few things you can focus on:**

- The most important is to submit **unique and diverse ideas**. Working on new ideas is the best way to increase your score, as diversification has the potential to reduce the risk of your merged performance and thus improve your Sharpe ratio.
- Explore creating alphas using data sets you haven’t worked on before.
- Create both delay-1 and delay-0 alphas. Note that the delay-1 alpha’s merged performance score has a higher contribution to your final score.
- Create alphas across both liquid and illiquid universes. For example, if you’re submitting alphas in the USA top 3,000, submitting alphas in the top 200 or top 500 universe might add value to your merged performance score.
- Keep the turnover of your alphas in check. Higher turnover inversely impacts your score. For price-volume data sets, keeping turnover less than or close to 40% is recommended, but make sure it is compensated with a higher Sharpe ratio.
- Creating alphas with data sets that have lower turnover can reduce the average turnover of your merged P&L. If your merged P&L metrics have high turnover, you can try to improve your score by submitting alphas with lower turnover.
- Go through all the available operators in the Learn section of the Brain platform, as you can implement a single idea in multiple ways through the use of diverse operators.
- Avoid overfitting your alphas to in-sample performance. Overfitting may not produce good out-of-sample performance and can reduce your OS score.

**Additional tips:**

- Make sure to watch the Learn section videos and read the documentation. The Learn section is continually updated with new resources.
- You are informed about all updates and other learning resources through the announcements section on the home page of the Brain platform.
- Explore and engage with the community forum. If you have any open queries regarding alpha research or specific questions on niche aspects of the platform, it is possible that what you’re looking for is already answered on the forum.
- Check out the Brain Tips series on the forum. This series is regularly updated and provides useful guidance on a diverse range of topics related to alpha research.
- During the alpha creation process, do not just submit the first submittable version of an alpha that improves your score. It is possible that you can improve your alpha further without overfitting, which could lead to a significant difference in your score.
- If you have registered as a team, you can have different team members work on different data sets to create alphas, so your overall alpha pool has more diversity. After some time, you and your team members can switch data sets, as each person may have a different approach to creating alphas with specific data sets, potentially improving your overall team score. This can also be a good opportunity for learning and brainstorming within the team.
- Organize and manage your alpha lists efficiently, as you may need to revisit your alphas as you progress through the competition. The Brain platform has features to name, color, and assign tags to your alphas to help you stay organized.
- Attend webinars and Q&A sessions where experienced researchers at WorldQuant provide useful training and tips for your alpha research. You also have the opportunity to directly ask questions to the Brain team in these sessions.

So, all the best with the International Quant Championship!
We hope you reach the top of the leaderboard.
