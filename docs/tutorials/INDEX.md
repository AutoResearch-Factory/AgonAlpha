# BRAIN Tutorials

## Discover BRAIN

- [*Read this First * - Starter Pack](read-first-starter-pack.md) - 介绍 BRAIN 研究顾问计划、金融与量化基础、Fast Expression、数据字段、运算符及技术和基本面分析方法。
- [Introduction to Alphas](about-brain-platform.md) - 说明 Alpha 的定义与生命周期、权重分配和多空头寸，以及 BRAIN 从表达式构建组合并计算 PnL 的机制。
- [Introduction to BRAIN Expression Language](introduction-brain-expression-language.md) - 说明 Fast Expression 的定义、由数据字段、运算符和数值构成的表达式结构，以及注释与分号等语法元素。
- [Intermediate Pack - Understand Results [1/2]](intermediate-pack-part-1.md) - 讲解累计 PnL、Sharpe、Turnover、Fitness、Returns、Drawdown 和 Margin，并汇总 IS 阶段测试及常见错误信息。
- [Intermediate Pack - Improve your Alpha [2/2]](intermediate-pack-part-2.md) - 讲解除法、rank、ts_rank 和 ts_delta 运算符，以及 Region、Universe、Decay、Truncation 和 Neutralization 设置。
- [10 Steps to Start on BRAIN](10-steps-start-brain-platform.md) - 包含一份由培训、Starter Pack、简单表达式、模拟设置、结果解释、活动与社区资源组成的十项 BRAIN 入门清单。
- [WorldQuant Challenge](challenge-help.md) - 介绍 WorldQuant Challenge 的参赛机制、每日计分的数量与质量因子、积分上限及 Bronze、Silver、Gold 等级。

## Create Alphas

- [Simulate your first Alpha](running-your-first-alpha.md) - 通过 `-ts_delta(close, 5)` 示例说明首次模拟的设置、结果指标、Alpha 属性和提交环节。
- [Test Period](test-period.md) - 说明 Test Period 将五年 IS 划分为 Train 与 Test 后的统计展示、图表标识及提交关系。
- [How to choose the Simulation Settings](simulation-settings.md) - 说明 Language、Instrument Type、Region、Universe、Delay、Decay、Truncation、Neutralization、Pasteurize、NaN Handling 和 Unit Handling 设置的含义与取值。
- [⭐ How BRAIN works](how-brain-platform-works.md) - 以 `rank(-returns)` 为例说明 BRAIN 从数据矩阵生成权重、持仓、每日 PnL 和累计 PnL 的七步模拟过程及 Decay 计算。

## Examples

- [⭐ Alpha Examples for Beginners](19-alpha-examples.md) - 包含 5 个初学者 Alpha 示例，覆盖营业收益率、负债升值、财务杠杆、收益率动量和短期情绪量稳定性，并给出假设、表达式与模拟设置。
- [⭐ Alpha Examples for Bronze Users 🥉](alpha-examples-bronze-users.md) - 包含现金流估值、股票高估和波动率套利 3 个 Bronze Alpha 示例及其假设、表达式与模拟设置。
- [⭐ Alpha Examples for Silver Users🥈](alpha-examples-silver-users.md) - 包含隐含波动率价差、看涨看跌波动率偏斜、同业收益差、未来投资、自由现金流质量和 Bull Trap 6 个 Silver Alpha 示例及其假设、表达式与模拟设置。

## Interpret Results

- [Clear these tests before submitting an Alpha](alpha-submission.md) - 汇总 Alpha 提交的 Fitness、Sharpe、Turnover、Weight、Sub-universe 和 Self-correlation 测试，以及特殊 Alpha 类型、地区稳健性规则和状态信息。
- [Parameters in the Simulation results](parameters-simulation-results.md) - 说明模拟结果中的评级、Return、Sharpe、IR、Fitness、累计 PnL、IS Summary、自相关、IS、Semi-OS、OS 和 Alpha 状态。

## Understanding Data

- [Understanding Data in BRAIN: Key Concepts and Tips](data.md) - 说明数据字段、数据集、Matrix、Vector、数据覆盖率和 Dataset Value Score，并列出 6 组字段特征检验表达式。
- [How to use the Data Explorer](how-use-data-explorer.md) - 说明 Data Explorer 的想法搜索、字段条件过滤、数据集搜索，以及关键词与缩写匹配机制。
- [Getting Started with Option6 Implied volatility (IV)](getting-started-option6-implied-volatility-iv.md) - 介绍 Option6 的覆盖与字段规模，以及恒定期限 IV、波动率曲面、预测、财报效应、股息和跨资产比率六类字段。
