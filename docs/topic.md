---
target-venue: [NeurIPS, ICML, ICLR, Nature Computational Science, Journal of Financial Data Science]
preferred-contribution-types: [method, system]
---

# Agon Alpha：基于 Prompt Economy 的自主量化研究系统

## 一句话

**Agon Alpha** 把 Agon（arXiv:2606.24177）的 factory-loop 架构搬到量化投资领域——造一台能自己读文献、提因子假说、写回测代码、对抗性审查、迭代改进、最后写出完整研究论文的自主量化研究机器。人不挖因子，人造挖因子的机器。

**"Machine scales, human steers."**

## 直觉

量化研究的本质是一个 **hypothesis generation → backtesting → filtering → iteration** 的循环。这个循环目前由人类驱动，受限于三个瓶颈：

1. **文献带宽**：每年 factor mining 论文几百篇（学术+金工+券商+WorldQuant 社区），加上 arXiv 预印本、SSRN working paper、行业报告。没人能读完。大量因子是"重新发明轮子"或者"不知道隔壁方向已经做过了"。
2. **过拟合盲区**：数据窥探（data snooping）是 quant 最致命的问题。传统防御（deflated Sharpe、FDR、样本外检验）是被动的事后检查——就像只靠海关抽查来防走私。真正有效的防御是**对抗性攻击**：让一个专职的"因子杀手"来试图杀死每个候选因子，只有活下来的才放行。
3. **探索效率**：人工挖因子是串行的——想一个→测一个→改一个。探索空间受限于人的精力、记忆和先验偏见。人天然会被自己熟悉的因子类型（"我擅长量价"）和确认偏误（"我觉得这个逻辑应该对"）锁死。

这三个瓶颈恰好是 Agon 的 factory-loop 架构擅长解决的。把 Agon 的 Topic→Idea Factory→Proposal Factory→Experiment Factory→Paper Factory 流水线搬到量化领域，得到：

```
Topic (研究方向) → Idea Factory (因子假说生成+对抗筛选)
    → Proposal Factory (因子验证方案设计)
    → Experiment Factory (回测+过拟合审查)
    → Paper Factory (研究论文产出)
```

每一步都有人类审稿人（reviewer）和对抗性攻击者（kill-argument reviewer）在环——这恰好是 quant 最需要但传统工具链最缺的东西。

**这不是"又一个因子挖掘工具"。这是把整个量化研究的 workflow 本身 agent 化。**

## 行业全景：谁在做、做到了哪一步、缺口在哪

### 第一梯队：已经在生产的 Agent-Driven 系统

| 机构 | 系统 | 做法 | 公开程度 |
|------|------|------|---------|
| **Man Group** | AlphaGPT (2025.7 实盘) | 3-agent 流水线：Idea Person→Implementer→Evaluator。多轮自我修正，IC 从 0.58%→2.23%。硬约束：因子必须能被人话解释经济逻辑 | 半公开（Bloomberg + 白皮书） |
| **Bridgewater** | AIA Forecaster (2025 实盘) | 多 agent 自主搜索+辩论+supervisor 合成。$5B AIA Macro Fund。Brier Score 0.1076，统计上与人类超级预测员无差异 | 半公开（arXiv 2511.07678） |
| **Jump Trading** | Domain-Adapted Agents (已实盘) | LLM 微调后直接产出 live trading signals。多 agent 覆盖数千 instruments，研究"信息论收敛边界"来指导 agent 过程收敛。2026 年同时在 ICLR + ICML 演讲 | 极少（只讲架构方向，不讲细节） |
| **XTX Markets** | Self-Optimizing Agents（据报） | 150 人，日均 $250B 交易量。Agent 以 4-6 小时周期自主发现策略→仿真→上线，人工干预最小 | 几乎不公开 |

### 第二梯队：有明确 Agent 布局但还没全自动

| 机构 | 关键信号 |
|------|---------|
| **Two Sigma** | 2026.3 公开声明："LLM 把瓶颈从'需要更多想法'变成'需要更快评估想法'"——研究漏斗倒置。AI 定位为评估吞吐加速器而非 idea machine |
| **D.E. Shaw** | 内部 LLM Gateway + DocLab 密码学审计哈希链。每次模型调用可追溯。Agent 自主性受严格法律/合规约束 |
| **Citadel** | Jensen Huang 亲口说 Citadel Securities 工程师 100% 用 Cursor。AI 主用于基本面研究增强（解析 10-K/10-Q 隐藏风险）。Agent 计划据传在开发中 |
| **Optiver** | 上海新建 AI Engineering 团队（目标 10-15 人，做模型 substrate + evaluation pod）。Agent 已嵌入开发流程但**对自主交易执行非常谨慎**——"LLM 在序贯决策上 directionally correct but not proficient" |
| **Renaissance Technologies** | 极密。Medallion 自 1991 零亏损年，历史年化 ~66% (gross)。据传已深度整合 Palantir 大数据平台。是否用 LLM agent 未知——但以 Simons 传统，应该是最早试验的人之一 |

### 第三梯队：中国量化私募

| 机构 | 规模 | AI/Agent 信号 |
|------|------|-------------|
| **幻方** | 600亿+ | DeepSeek 反哺投研，最 aggressive。萤火二号万张 A100 |
| **九坤** | 500亿+ | 至知创新研究院，开源 IQuest-Coder 代码大模型 |
| **灵均** | 数百亿 | Alpha Capture + 产业链知识图谱，2025 收益 73.51% 登顶 |
| **明汯** | 800亿 | 400P FLOPS 算力，但**还没做 LLM agent**（你直接聊过） |
| **世纪前沿** | 百亿级 | AI 团队 100+ 人。据传抓了 20 个实习生做 agent 实验，养蛊最后只留一个 |
| **衍复** | 800亿+ | "四大金刚"之一，精选 alpha 因子 |
| **黑翼** | 500-600亿 | 自 2017 布局 AI，全流程 AI 化 |
| **宽德/佳期/启林** | 百亿-500亿 | ML 为核心，但 agent 方向无公开信息 |

### 第四梯队：开源/学术界的 Agent 因子挖掘

| 项目 | 来源 | 核心做法 | 成熟度 |
|------|------|---------|--------|
| **RD-Agent-Quant** | 微软 (NeurIPS 2025) | Multi-Agent + Multi-Armed Bandit 因子-模型联合优化。70% 更少因子、2× 年化收益、单次实验 <$10 | 最成熟 |
| **FactorMAD** | 清华/微软 (ICAIF 2025) | 双 Agent 辩论挖因子。LLM 直接写 Python 因子代码而非限定算子集 | 已开源 |
| **Alpha-GPT** | HKUST (EMNLP 2025) | 人机交互式 alpha 挖掘。WQ IQC top-10 / 41000+ 队伍 | 学术 |
| **EasyQuant/QuantGPT** | 社区 | Claude agent + WQ BRAIN 集成。Sharpe 1.6-2.1 | 社区 |
| **Robin** | 社区 (MIT) | 6-agent pipeline（Research→Debate→Implement→Validate→Strategy→Backtest） | 活跃开发 |

### 缺口在哪

所有人都把 AI agent 当**工具**用——单点 agent 生成因子、单点 agent 辩论、单点 agent 回测。**没有人把整个量化研究 workflow 本身变成一个自治系统。**

具体来说：
- **没人做 Deep Lit → Factor 的闭环**：Man Group 的 Idea Person 靠人工 prompt 给方向，不是从文献中自动提取研究前沿和未探索的因子逻辑
- **没人做 Kill-Argument 过拟合防御**：所有人都在谈过拟合是问题，但没人把对抗性攻击（"我专门负责杀死你的因子"）做成标准的 agent role。这恰好是 Agon 的独门绝技
- **没人做 Multi-Model Cross-Validation for Factor Quality**：如果 Claude、DeepSeek、GPT 三个 backend 独立跑，都"发现"了同一个因子，这是 signal 还是 noise？没人系统性地研究过
- **没人做 Factor Lifecycle Management**：因子会 decay（alpha decay），目前靠人监控和手动退役。agent 能不能自己追踪、预警、退役、搜索替代品？
- **没人做开源**：以上所有机构系统全是闭源黑箱。没有任何一个可以独立复现

## 系统设计核心问题（最高层级，不锁死方案）

这些是 Agon Alpha 需要回答的架构级问题——不是"挖什么因子"，而是"挖因子的机器该怎么造"：

### 1. Factory-Loop 怎么适配量化工作流？

Agon 的原始流水线是为学术研究（topic→idea→proposal→experiment→paper）设计的。量化研究有自己的阶段：

```
方向定义 → 因子假说 → 回测验证 → 过拟合审查 → 组合/实盘 → 研究文档
```

每个阶段怎么映射到 factory？每个 factory 的 producer 和 critic 分别是什么？多少个 agent roles？它们怎么 handoff？量化独有的阶段（比如过拟合审查、组合优化）需要新角色吗？

### 2. Adversarial Overfitting Defense 怎么设计？

这是 Agon Alpha 最核心的系统设计问题。Agon 的 kill-argument reviewer 在 academic research 场景下负责"找论文最薄弱的 claim 并试图击穿它"。在量化场景下，它应该做什么？

可能的方向（不锁死）：
- **时间鲁棒性攻击**：换时间段，因子还有效吗？
- **Universe 鲁棒性攻击**：换股票池/市场，因子还有效吗？
- **多重比较攻击**：你试了多少个变体才试出这一个？p-hacking 证据在哪？
- **伪因子对照**：随机打乱标签/收益率，这个因子比随机的好多少？
- **前视偏差攻击**：你的回测数据有没有用到未来信息？
- **交易成本攻击**：算上滑点和佣金，这个因子还赚钱吗？
- **容量攻击**：这个因子能承载多少资金？规模放大以后表现退化多少？

这些攻击能不能形式化成一个标准的 **Factor Defense Protocol**——因子必须通过全部攻击才放行？

### 3. Deep Literature Loop 怎么驱动因子发现？

Agon 的 deep lit loop 是 search→select→read→write wiki→expand→repeat。在量化场景下：

- 搜什么源？arXiv (q-fin), SSRN, J. Finance, RFS, JFE, J. Financial Economics, 券商金工报告, WorldQuant BRAIN 社区, QuantConnect 社区……
- 读完后怎么提取"可操作的因子逻辑"？不是摘要总结——是提取"这篇论文的因子公式是什么、经济直觉是什么、在什么市场/时间段上测的、IC/Sharpe 多少"
- 多篇文献能不能交叉碰撞出新因子？（"A 论文的因子逻辑 + B 论文的因子结构 → 一个没人试过的组合"）
- 文献驱动的假设生成 vs 数据驱动的信号搜索——两者的信息流怎么融合？

### 4. Multi-Agent Architecture 怎么设计？

Jump Trading 在 ICML 2026 上讨论了"什么时候 multi-agent with domain-focused subagents 超越 single context-rich frontier model"。这是工程问题也是科学问题：

- 几个 agent？什么分工？什么 communication protocol？
- Agent 之间是竞争（多个 agent 独立挖因子，最好的胜出）还是合作（分工协作，互相 critique）？
- 怎么防止 agent 之间的群体思维（groupthink）和 cascading errors？
- 每个 agent 配什么 model backend？什么时候该用一个更强的单模型 vs 多个便宜模型的 ensemble？

### 5. 怎么评价系统本身的好坏？

这不是"这个因子 Sharpe 多少"的问题——那是因子的评价。**系统**的评价是另一个层级：

- **新颖性**：系统发现的因子有多少是已知文献里没有的？（需要做 novelty check——对每个产出因子，搜文献看是否已被发表）
- **稳健性**：系统产出的因子在多大比例上能通过完整的过拟合防御协议？
- **效率**：单位时间/单位成本能产出多少通过防御的因子？
- **互补性**：multi-model 产出的因子之间是互补的还是冗余的？
- **人类对齐**：系统产出的因子能被人类 quant 理解和审计吗？还是变成了黑箱信号生成器？
- **实盘衰减**：系统产出的因子在实盘/paper trading 中的 alpha decay 速度是多少？和人类手动挖的比呢？

可不可以设计一个 **Agon Alpha Benchmark**——用 held-out 时间段/市场/因子库，测量系统"在前人未涉足的区域发现有效因子的能力"？

### 6. Human-in-the-Loop 的边界在哪？

"Machine scales, human steers"——人到底 steers 什么？

- 人定研究方向？（"这周探索期权波动率曲面" vs "这周探索供应链因子"）
- 人定风险预算？（"因子最大回撤 20% 硬止损"）
- 人做最终决策？（"系统产出 100 个因子，人挑 10 个上实盘"）
- 还是人只做例外处理？（"系统全自动，只有回撤超限或异常时才通知人"）

不同资产/频率/策略类型可能有不同的最优人机分工。能不能让系统**自适应**——根据因子复杂度、回测质量、市场环境自动决定哪些决策需要人类确认？

### 7. 系统通用性：一个架构，所有资产

这题的核心主张是 Agon 的 OmniDisciplinary 设计原则——核心 agent 领域无关，领域知识通过文献、context、refinery skills 注入。在量化场景下：

- 同一个 agent 架构能不能做股票因子、期货 CTA、期权波动率曲面、加密货币链上因子、宏观跨资产配置……？
- 不同资产需要不同的 refinery skills（比如期权需要 Greeks 和 vol surface 的领域知识），但核心 producer-critic loop 不变？
- 如果架构真的通用，怎么证明？是不是需要至少 2-3 个资产的 case study？

## 手头已有的东西

### Agon —— 成熟的生产级自主科研基础设施

| 组件 | 状态 | → Agon Alpha 角色 |
|------|------|-------------------|
| Deep Literature Loop (search→read→wiki→expand) | ✅ 400-2000 papers/topic | 系统性文献驱动因子发现 |
| Idea Factory (creator→refiner⇄reviewer) | ✅ 生产验证 | 因子假说的对抗性生成与筛选 |
| Experiment Factory (scientist→coder→auditor) | ✅ 444+ iterations | 因子回测 pipeline 自动化 |
| Kill-Argument Reviewer + Adjudicator | ✅ 生产验证 | **过拟合防御协议的核心引擎** |
| Multi-Model Collaboration (5+ backends) | ✅ 生产验证 | 跨模型因子一致性验证 |
| Audit System & Harness | ✅ 时间/成本/context 追踪 | 因子发现成本追踪 |
| Zero-Code Dispatcher | ✅ 1月连续无人干预 | 大规模并行因子探索 |
| Failure Taxonomy (20 modes, 4-axis) | ✅ 生产验证 | 量化版 failure mode 分类学 |
| Refinery Skill Injection (48 skills) | ✅ 生产验证 | Quant 领域 mindset skills |
| Open-Source | ✅ github.com/AutoResearch-Factory/Agon | 完全可复现 |

### 计算能力

AI/ML 全栈。GPU 集群（A100×10+ / RTX 8000×10+ 可用）。不差算力。

### 数据

公开市场数据 API 可覆盖 A 股/美股/港股/期货/加密货币/期权。另类数据（卫星、供应链、信用卡流水）可作为扩展方向。不需要 proprietary data 就能证明系统有效性。

## 开放问题（系统设计向，不限于此）

1. **Adversarial Overfitting Defense Protocol 能不能形式化？** 给定一个候选因子，系统自动运行 k 项攻击（时间鲁棒性、universe 鲁棒性、多重比较校正、伪因子对照、前视偏差、交易成本、容量……），全部通过才放行。这个 protocol 本身是不是一个独立的方法论贡献？

2. **Deep Lit → Factor Hypothesis 的链路怎么自动化？** 不是"读完论文输出摘要"——是从论文中提取可执行的因子公式和回测参数，多篇文献还能交叉碰撞出新组合。这本身是一个信息抽取+推理的 AI 问题。

3. **Multi-Model Consensus 是信号还是噪声？** 如果 3 个不同 backend 的 agent 各自独立运行，都"发现"了同一个因子——这是因为因子真的强，还是因为所有模型都在训练数据里见过类似的金融文本模式？怎么区分？

4. **Factor Lifecycle Automation**：因子从诞生→验证→实盘→衰减→退役，全生命周期能不能由 agent 自主管理？衰减预警用什么指标？退役阈值怎么定？退役后能不能自动搜索替代因子？

5. **Novelty Check at Scale**：系统产出 1000 个候选因子后，怎么自动判断哪些是真正新颖的、哪些是已知文献里已经有的？这需要 agent 做大规模的因子→文献 cross-reference。

6. **Benchmark Design for Research Systems**：怎么评价一个"自主研究系统"的好坏？不是评价它产出的某一个因子——是评价系统本身。需要什么 benchmark？held-out 时间段？held-out 因子库？和人类 quant 的对比实验？和 RD-Agent 的头对头对比？

7. **从回测到实盘的 Gap**：纯回测 paper 够不够？还是需要 paper trading 或小资金实盘？如果要实盘，最小可行验证是什么？（比如"系统产出 top-10 因子，$100K 实盘跑 3 个月，和回测 IC 的 rank correlation >0.7"？）

8. **通用性证明**：怎么证明 Agon Alpha 的架构是跨资产通用的？至少需要几个 case study（比如股票+期货+期权）才算 convincing？

9. **Human-Agent Collaboration Protocol**：人不挖因子了，但人做什么？怎么设计一个人机交互的频率和内容，使得人既不会成为瓶颈（micro-manage），也不会被完全 bypass（完全看不懂 agent 在干什么）？

10. **和 RD-Agent-Quant / FactorMAD 的根本区别**：如果 reviewer 说"这不就是 RD-Agent 换个 prompt 吗"，你怎么回应？Agon Alpha 的 architecture-level novelty 在哪——是 adversarial defense protocol？是 deep lit integration？是 multi-model consensus？是 lifecycle management？是 open-source reproducibility？还是所有上述之和？

## 大框

这是一个**最高层级的系统设计问题**——我们造的是"挖因子的机器"，不是某一个具体的因子。所以：

- ✅ 任何资产：股票（A股/美股/港股）、期货、期权、债券、加密货币、外汇……
- ✅ 任何频率：tick → 日内 → 日频 → 周频 → 月频
- ✅ 任何因子类型：量价、基本面、另类数据、文本/NLP、宏观、产业链、波动率曲面……
- ✅ 任何方法：传统线性、ML、DL（Transformer/GNN/LSTM）、RL、LLM agent、遗传规划、符号回归……
- ✅ 任何量化子问题：因子挖掘、因子组合、因子择时、组合优化、风险建模、交易执行……
- ✅ 期权很自然地在这个框架内——vol surface modeling、Greeks 因子、skew/term structure、volatility risk premium……全部是 factor mining 的特例
- ✅ 纯回测可以，paper trading 更好，小资金实盘最佳——但系统设计不应依赖于能否实盘
- ✅ 可以和 Qlib/RD-Agent 整合或对比
- ✅ 可以交叉到 AutoML、自动 forecasting、金融 NLP、知识图谱、因果推断
- ❌ 不要锁死任何一个资产/频率/方法——通用性是核心主张
- ❌ 不要做成"又一个 LSTM/Transformer 预测股价"——那不是在造系统
- ❌ 不要做成纯 benchmark survey——那是诊断工具，不是研究系统
- ❌ 不要让具体的因子方向（"做期权 vol 因子！"）绑架系统设计——系统在先，具体方向在后

## 起点文献

### 我们的基础设施（必读，写死）
- **Sun, Ren, Yi, Guo, Zhang, Du, Yang. "Agon: An Autonomous Large-Scale Omnidisciplinary Research System Built on Prompt Economy." arXiv:2606.24177, 2026.** — Agon Alpha 的 infrastructure base。

### Agent 驱动的因子挖掘（直接竞品/垫脚石）
- **FactorMAD** (Duan, Zhang, Li; Tsinghua/Microsoft). "A Multi-Agent Debate Framework Based on LLMs for Interpretable Stock Alpha Factor Mining." ICAIF 2025.
- **RD-Agent-Quant** (Microsoft). "A Multi-Agent Framework for Data-Centric Factors and Model Joint Optimization." NeurIPS 2025. arXiv:2505.15155.
- **Alpha-GPT** (HKUST). "Human-AI Interactive Alpha Mining for Quantitative Investment." EMNLP 2025.

### 行业 Agent 系统（非学术但必读）
- **Man Group. "What AI Can (and Can't Yet) Do for Alpha."** Nov 2025.
- **Man Group. "A Trend Following Deep Dive: AlphaTrend and Agentic Research Workflows."** Feb 2026.
- **Bridgewater. "AIA Forecaster."** arXiv:2511.07678.
- **Jump Trading. "Domain-Adapted Agents for Quantitative Research at Scale."** ICLR 2026 Expo Talk.
- **Jump Trading. "Multi-Agent System Design and Evaluation for Quantitative Finance."** ICML 2026 Expo Talk.

### 量化经典（deep lit 必过的基础设施）
- Fama & French (1993, 2015). 三因子/五因子模型. JFE.
- Hou, Xue & Zhang (2015). q-factor model. RFS.
- Harvey, Liu & Zhu (2016). …and the cross-section of expected returns. RFS. — 多重比较/数据窥探的经典
- Gu, Kelly & Xiu (2020). Empirical asset pricing via machine learning. RFS. — ML 量化的标杆
- Kozak, Nagel & Santosh (2020). Shrinking the cross-section. JFE.
- Giglio, Kelly & Xiu (2022). Factor forests.
- Lopez de Prado. "Advances in Financial Machine Learning." Wiley, 2018. — 量化 ML 的标准参考
- DeMiguel, Garlappi & Uppal (2009). Optimal versus naive diversification. RFS.

### LLM + Finance
- Lopez-Lira & Tang (2023). Can ChatGPT forecast stock price movements?
- FinGPT (Yang et al., 2023).
- BloombergGPT (Wu et al., 2023). arXiv:2303.17564.

### 开源量化平台（可能整合或对比）
- Microsoft Qlib: AI-oriented quant investment platform
- Qlib RD-Agent: LLM-driven Auto Quant Factory
