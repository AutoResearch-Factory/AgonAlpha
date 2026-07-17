---
下载时间: 2026-07-12
---

# WorldQuant BRAIN 文档归档

## API

- [API 使用说明](../references/worldquant-api-spec.md) - 记录 BRAIN API 的认证、操作符、数据字段、回测、Alpha 查询与提交接口，以及批量回测客户端的输入输出约定。
- [回测接口 Schema](api/simulations-options.json) - 包含 `/simulations` POST 请求与响应字段的类型、必填和只读属性、可选值及数值约束。
- [Alpha 接口 Schema](api/alpha-options.json) - 包含 `/alphas/<alpha_id>` PUT 字段的类型、必填和只读属性、设置选项及 Alpha 状态和指标结构。
- [官方 API 搜索结果](api/official-api-search.json) - 保存 API 相关检索在参考资料、教程、视频、推荐阅读、FAQ、活动、消息和竞赛八类内容中的 41 条命中结果。
- [官方 API 页面访问状态](api/official-page-status.json) - 记录 6 个 API 相关官方教程页面的 HTTP 访问状态，当前状态均为 404。

## 数据

- [数据索引](data/INDEX.md) - 登记 14 个数据集及其详情文件，并收录 USA、TOP3000、Delay 1 范围内 4367 个数据字段的完整 JSON。
- [数据分类](data/categories.json) - 包含 7 个数据分类及其子分类的名称、数据集数、字段数、Alpha 数、用户数、价值评分和地区范围。
- [数据字段 JSON](data/fields.json) - 包含查询范围、字段总数和 4367 个字段对象，对象记录字段说明、分类、类型、覆盖率、使用统计及创建时间。

## 语法

- [操作符说明](syntax/operators.md) - 按 7 个类别整理 66 个 Fast Expression 操作符的定义、作用域、等级、说明和文档路径。
- [操作符原始数据](syntax/operators.json) - 由 66 个操作符对象组成的原始 JSON 数组，包含名称、类别、作用域、定义、说明、文档路径和等级。

## 因子研究

- [因子研究索引](factor-research/INDEX.md) - 登记 FAQ、推荐阅读、机器可读研究资料和按 16 个课程系列分组的 69 篇视频课程文档。
- [FAQ](factor-research/faqs.md) - 汇集 97 组有关 Alpha、数据、操作符、仿真、绩效与提交等主题的 BRAIN 问答。
- [推荐阅读](factor-research/recommended-reading.md) - 收录 22 篇有关资产定价、股票收益预测、分析师、期权与机器学习等主题的论文链接。
- [研究论文链接](factor-research/research-papers.json) - 包含 14 条 WorldQuant BRAIN 社区研究论文帖子的标题、类型和链接。

## Tutorials

- [教程索引](tutorials/INDEX.md) - 登记按 Discover BRAIN、Create Alphas、Examples、Interpret Results 和 Understanding Data 分组的 19 篇教程正文。
- [⭐ Alpha Examples for Bronze Users 🥉](tutorials/alpha-examples-bronze-users.md) - 包含现金流估值、股票高估和波动率套利 3 个 Bronze Alpha 示例及其假设、表达式与模拟设置。
- [⭐ Alpha Examples for Silver Users🥈](tutorials/alpha-examples-silver-users.md) - 包含隐含波动率价差、看涨看跌波动率偏斜、同业收益差、未来投资、自由现金流质量和 Bull Trap 6 个 Silver Alpha 示例及其假设、表达式与模拟设置。
