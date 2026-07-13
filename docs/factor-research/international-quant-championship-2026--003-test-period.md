# Test Period

Course: International Quant Championship 2026
Category: Alpha Performance
Duration: PT3M41S
Source: YouTube
Last modified: 2026-05-26T11:09:04.510774-04:00

## Description

In this video, you will learn about a unique feature on BRAIN called the Test Period, designed to enhance your alpha robustness testing process

## Transcript

Hi, everyone.

Welcome to this video, where you will learn about a unique feature on Brain called the **test period**, designed to enhance your alpha robustness testing process.

An alpha is considered robust if its out-of-sample performance is similar to its in-sample performance. Thus, this feature can help you potentially avoid overfitting within your alphas.

Let's understand how to use the test period tool through an example. We will now test an alpha idea based on a company's improvement in operating earnings yield over the last year, using the **TS rank** operator. Operating earnings yield is calculated as the operating income of the company divided by its market capitalization.

As a user on Brain, you can backtest your alpha ideas over a five-year in-sample period to check the robustness of your idea. Before simulating the alpha, you need to access the simulation settings.

Here, you can set a test period of one year, click on "Apply," and then click on "Simulate." This allows you to divide your in-sample period into a **train period** of four years and a **test period** of one year. The train period is ideal for developing your alphas, while the test period is crucial for validating them.

In this example, we selected a testing period of one year, as having 20% of testing data is commonly used for data analysis. However, you can experiment with different periods as well.

After simulating the alpha, you can observe its performance over the train period of four years by scrolling down to see the train period alpha statistics. You can determine if the idea generates a decent signal during this period.

To validate the robustness of the alpha idea and avoid overfitting, you need to evaluate its performance over the test period by scrolling up and clicking on the "Show Test Period" button. You can view the alpha's performance in the last year of in-sample data, represented by the orange-colored line on the cumulative P&L chart.

Upon observation, if the alpha performs well during the test period, it boosts our confidence in the idea and encourages us to further improve it before submitting. As is the case in this example, by clicking on the "IS" button, you can see the overall five-year in-sample performance of the alpha.

To become submittable on Brain, an alpha must pass various in-sample tests. In this case, the alpha is failing the fitness test, indicating a need for improvement. You can think of various ways to make this alpha submittable by iterating on the idea and refining it further.

Scrolling up, you will see a button named "Hide Test Period," which allows you to hide the test period if desired. **Note:** An alpha can only be submitted when the test period is revealed by clicking on the "Show Test Period" button.

**To summarize:**
The test period feature helps avoid overfitting and assesses the robustness of an alpha idea. By setting a test period, you can analyze its performance separately from the training period. This feature provides valuable insights without directly affecting the simulation itself. Use the test period to accept or reject alpha ideas and optimize your resource allocation for developing robust alphas.
