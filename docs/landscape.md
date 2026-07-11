---
topic: 0709-quant-factor-mining
title: "Agon Alpha：自主量化研究系统 — 文献全景"
created: 2026-07-09
last_deep_lit_tick: 2026-07-10
papers_full_text_read: 143
papers_relevant_indexed: 200+
model_used: deepseek-v4-pro[1m] (全文精读), claude-opus (调度)
---

# Agon Alpha 文献全景：143 篇全文精读

> 143 篇完整笔记在 `$ARXIV_WIKI_DIR/<arxiv_id>.md`。
> 本文件是单一事实源：撞车判定、垫脚石识别、关键洞察都在这里。

---

## 摘要

我们对量化金融的自主研究系统（Agon Alpha）做了地毯式文献调研。21 轮搜索，130+ arxiv-tool queries，143 篇全文精读，覆盖 LLM agent 因子挖掘、资产定价、高频/微观结构、期权/波动率、组合优化、执行、NLP/情绪、RL、加密、统计套利、因子择时、尾部风险、回测方法论、体制检测等 24 个子领域。

**核心结论：143 篇中零篇撞车 Agon Alpha 的核心 claim。** 所有竞品要么做单点因子工具，要么做交易 agent，要么做回测 protocol。无人做 full factory-loop 自主量化研究系统（deep lit → idea → experiment → paper 全闭环 + adversarial overfitting defense + multi-model consensus + 跨资产 OmniDisciplinary + 大规模并行自动化）。

**最强 motivation 论文：** Chen & Welch (2607.06502) 证明发表后的 academic alphas 在 post-2005 large-cap 域下 median 仅 7bp/月，Empirical Bayes 收缩后全部归零——整个学术因子 zoo 在可投资股票上已经 dead。

**25 个可直接集成的垫脚石** 从竞品论文中提取，涵盖因子 grammar、筛选管线、过拟合 protocol、偏差框架、regime 检测、MCTS 搜索、DSR/PSR 公式、sealed evaluation 等。

---

## §1. Agon — 我们的基础设施

Agon (arXiv:2606.24177) 是 Agon Alpha 的 infrastructure base。以下来自论文 tex 源文件，非二手 wiki。

### 1.1 六大设计原则

| 原则 | 含义 |
|------|------|
| Prompt Economy | ROI = Σv_i/(m+αn)。Loop 最大化 ROI。每个 loop 是 producer-critic adversarial pair 围绕 artifact |
| Future-Facing | Prompt 只描述稳定结构，不固化当前模型弱点 |
| Minimal Prompts | 18 roles, 230.6 KiB（vs AI Scientist v2 ~110/302, ARIS 79/1157） |
| OmniDisciplinary | 核心 agent 领域无关。领域知识通过文献/context/refinery skills 注入 |
| Massive Parallelism | 同一套 role prompts 同时实例化在多个 research thread。Factory 异步运行 |
| Zero-Code | Prompt, not Code。调度为 prompt dispatcher。1 月连续无人干预已验证 |

### 1.2 Factory-Loop 架构

```
Topic → Idea Factory → Proposal Factory → Experiment Factory → Paper Factory
         ↑                ↑                    ↑                   ↑
         └── Deep Literature Loop (wiki + landscape) ──────────────┘
```

每个 factory = producer-critic adversarial loop。Critic 在 fresh context 独立工作。Artifact 经受住攻击后才 advance。

**关键组件：**
- Multi-Model Collaboration：每个 role 可配不同 backend（Claude Code, Codex, DeepSeek, Kimi, GLM）。关键步骤 second-model check
- Refinery Skill Injection：从 ARIS/Sibyl 蒸馏 48 mindset skills。优先级 user > agent factory > refinery skills
- Code-Artifact Separation：框架与 artifact 分离。Inter-agent handoff 通过 artifact 中介
- Audit System：追踪每次调用的时间、成本、context、工具使用
- Kill-Argument Reviewer + Adjudicator：防止 paper monster
- Zero-Code Dispatcher：1 月连续无人干预已验证

### 1.3 Failure Taxonomy

20 failure modes，4-axis：Severity（Waste/Invalid evidence/Direction collapse）、Fixability（Prompt/Loop/Loop+Human/Human）、Visibility（Visible/Partially visible/Invisible）、Capability Locus（Perception/Reasoning/Execution/Motivation）。

核心洞察：**visibility--fixability line 是自主研究的能力边界。** Invisible + Not Fixable 象限（anomaly blindness, plausible false attribution, scientific taste, obedient refinement, exploration refusal）只有人类科学家能跨过。

### 1.4 部署记录

1000+ loop iterations，10+ 领域，0 行人类手写实验代码，同一架构跨领域零修改迁移，全栈开源（github.com/AutoResearch-Factory/Agon）。

### 1.5 Agon Alpha = Agon × 量化金融

Agon Alpha 是把 Agon 的 factory-loop 架构搬到量化金融领域。关键差异不在 feature level（"我们有 deep lit 他们没有"），而在**系统层级**：

| | 143 篇竞品 | Agon Alpha |
|---|---|---|
| 规模 | 单线程，单次实验 | 多 topic/idea/experiment 并发 |
| 架构 | Linear pipeline 或 fixed multi-agent | Factory-loop: producer-critic adversarial |
| 调度 | 硬编码 workflow | Zero-Code prompt dispatcher |
| 验证 | Statistical threshold 或被动 audit | Kill-argument reviewer + multi-model second-check |
| 领域迁移 | 重新实现或 limited transfer | 同一 core agent 集合，换 context + skills |
| 代码 | 部分开源且依赖闭源数据 | 全栈开源 |

---

## §2. 这份 landscape 怎么做出来的

**21 轮搜索**：130+ arxiv-tool queries + 10+ WebSearch。覆盖 LLM agent 因子挖掘、传统资产定价、过拟合防御、高频/微观结构、期权/波动率、组合优化、执行/市场冲击、NLP/情绪、RL、加密/DeFi、商品/固收、统计套利、因子择时、尾部风险、回测方法论、体制检测、时序基础模型、金融 LLM 推理等 24 个子领域。

**143 篇全文精读**：全部由 `claude-ds`（deepseek-v4-pro[1m]）并行跑 deep-lit-reader agent 完成。每篇产出 80-225 行中文 wiki，写入 `$ARXIV_WIKI_DIR`。

**B7 反向扩展已执行**：references + cited + author search + title-term search 四项扩展。

**未获取全文的**：FactorMAD（ACM paywall+Cloudflare）、Man Group AlphaGPT（web article，无定量数据）。Chain-of-Alpha (2508.06312) arXiv 404。10 篇 FX/ESG/因子经典论文在 SSRN/journals（SSRN Cloudflare 阻拦，RFS/JFE/JF paywall），已从元数据列入。

---

## §3. 竞争格局：143 篇论文按主题组织

### 3.1 LLM Agent 因子挖掘（18 篇）— 最直接相关

这是 2025-2026 年爆发的新领域。核心范式：用 LLM agent 替代遗传规划/强化学习来生成 alpha 因子公式。

| ID | 论文 | 年份 | 核心贡献 | IC/Sharpe |
|----|------|------|---------|-----------|
| 2308.00016 | Alpha-GPT | 2023 | 人机交互 alpha 挖掘，WQ IQC top-10 | — |
| 2406.10811 | LLMFactor | 2024 | LLM prompt-only 生成因子 | — |
| 2406.18394 | AlphaForge (AAAI 2025) | 2024 | Generator-Predictor NN + dynamic combination | IC 4.40%, ¥3M 实盘 +21.68% |
| 2505.11122 | Alpha Jungle | 2025 | LLM+MCTS，UCT-guided+Frequent Subtree Avoidance | IC 0.042-0.080 |
| 2505.15155 | RD-Agent-Quant (NeurIPS 2025) | 2025 | Co-STEER + MAB scheduler，<$10 cost | IC 0.053, IR 1.74 |
| 2511.18850 | CogAlpha | 2025 | 7-level 21-agent hierarchy + Thinking Evolution | IC 0.059 |
| 2602.07085 | QuantaAlpha | 2026 | Trajectory-level mutation/crossover | IC 0.047 |
| 2602.14670 | FactorMiner | 2026 | Ralph Loop + experience memory, 110 factors, GPU加速 | IC 8.25% CSI500 |
| 2603.14288 | Beyond Prompting | 2026 | 闭环 agentic AI, 但 turnover 105% | SR 2.75 组合 |
| 2603.16365 | FactorEngine | 2026 | 图灵完备程序因子 + macro-micro co-evolution | IC 0.047, IR 1.60 |
| 2603.20247 | AlphaLogics | 2026 | Market logic 作为可优化对象 | IR 1.53 CSI500 |
| 2604.09601 | Hubble | 2026 | DSL+AST sandbox+dual-channel RAG | RankIC 0.006 |
| 2604.26747 | LLM Agents in Crypto | 2026 | Beyond Prompting 作者的加密后续 | SR 1.55 net |
| 2605.05580 | AlphaCrafter | 2026 | Miner→Screener→Trader, 唯一回测+OOS双正 | SR 1.53→0.70 |
| 2606.20625 | AlphaMemo | 2026 | SSPM+AST-diff edit motifs+confidence-gated | RankICIR 0.46 |
| 2606.29194 | Agora | 2026 | Sealed Joint Search, 5 agent A2A, SR 1.87 | SR 1.87 holdout |
| 2510.04787 | TiMi | 2026 | Strategy-deployment decoupling, 200+ pairs | — |
| DOI | FactorMAD (ICAIF 2025) | 2025 | 双 agent 辩论，code-based pipeline | 显著优于 GP/RL |

**关键发现：** 所有系统要么靠 LLM 预训练知识，要么靠人类 prompt 给方向。**零篇从文献中提取因子逻辑。** 多数固定 operator set，多数只用 OHLCV 数据，多数无交易成本建模。最成熟的 RD-Agent-Quant 依赖不公开的 Wind 数据。Agora 是最接近我们的系统但要区分——单线程、单模型、被动 sealed evaluator（非主动 kill-argument attacker）。

### 3.2 Multi-Agent 金融系统（7 篇）

| ID | 论文 | 核心 |
|----|------|------|
| 2407.06567 | FinCon | LLM multi-agent + verbal RL |
| 2412.20138 | TradingAgents | 5-team hierarchy, Bull vs Bear 辩论 |
| 2508.00554 | ContestTrade | Internal contest mechanism |
| 2510.15949 | ATLAS (ACL 2026) | Adaptive-OPRO prompt optimization, reflection paradox |
| 2602.23330 | Expert Investment Teams | Fine-grained task decomposition |
| 2604.18500 | QRAFTI | MCP 工具化 + reflection planning |
| 2605.12532 | AgenticAITA | Training-free deliberative loop + safety layer |

### 3.3 基准与评估（6 篇）

| ID | 论文 | 核心 |
|----|------|------|
| 2503.21422 | Survey of AI in Quant Investment | 最全面的量化 AI 综述 |
| 2601.13770 | Look-Ahead-Bench | Scaling Paradox：大模型前视偏差更严重 |
| 2602.14233 | Evaluating LLMs in Finance (ICML 2026) | 5 种结构性偏差框架 + checklist |
| 2606.08285 | Beyond Agent Architecture | 审计 30 篇 LLM 交易论文：**无一完整 artifact** |
| 2606.29771 | CLQT | 5 轴 diagnostic benchmark |
| 2605.27887 | PortBench | Corr-aware LLM portfolio benchmark |

### 3.4 资产定价与因子模型（8 篇）

| ID | 论文 | 核心 |
|----|------|------|
| 2206.10014 | Deep PLS for Empirical Asset Pricing | Deep PLS SDF estimation |
| 2301.09173 | Labor Income Risk and Cross-Section | Labor factor |
| 2402.06635 | Large and Deep Factor Models | 大规模深度因子模型 |
| 2403.06779 | From Factor Models to Deep Learning (Survey) | ML 重塑资产定价综述 |
| 2404.14137 | Asymmetric CAPM | 非对称 CAPM |
| 2411.19444 | CAPM with Size Factor | 改进 CAPM |
| 2512.16251 | Consensus-Bottleneck Asset Pricing | 可解释 DL 资产定价 |
| 2604.04430 | The Co-Pricing Factor Zoo | 共定价因子 |

### 3.5 组合优化与组合管理（13 篇）

| ID | 论文 | 核心 |
|----|------|------|
| 2402.16609 | Transformer+RL+Black-Litterman | 组合优化 |
| 2403.07916 | Industry-grade Deep RL Portfolio | 工业级 RL 组合 |
| 2403.16667 | Deep RL and Mean-Variance | 负责任组合优化 |
| 2405.01604 | Portfolio Management using Deep RL | RL 组合管理 |
| 2409.08426 | Deep RL Framework for Portfolio | RL 组合框架 |
| 2507.05994 | Generalized Kelly Criterion | 广义 Kelly 最优增长 |
| 2602.17098 | Deep RL for Optimal Portfolio Allocation | RL vs MVO 对比 |
| 2605.28853 | Financially Guided Deep Portfolio | AttentionLSTM SR 0.29 |
| 2605.01384 | SBCA: Cross-Modal BERT Actor-Critic | 跨模态组合优化 |
| 2605.17307 | Deep RL Diversified Portfolio (SAC) | LSTM vs Transformer encoder |
| 2605.09310 | Beyond ESG Scores | 动态约束组合优化 |
| 2606.08283 | Macro Economists ETF | LLM multi-agent 商品 ETF |
| 2510.14264 | AlphaQuanter | Tool-augmented agentic RL |

### 3.6 期权与波动率（9 篇）

| ID | 论文 | 核心 |
|----|------|------|
| 2405.06774 | Hedging American Put Options with Deep RL | RL 期权对冲 |
| 2406.11520 | Operator Deep Smoothing for IV | IV 曲面算子平滑 |
| 2504.06208 | Deep Hedging with Options Using IV Surface | IV 曲面深度对冲 |
| 2509.08096 | Joint Calibration of Vol Surface | 联合校准 |
| 2512.12420 | Deep Hedging with RL | RL 期权风险管理 |
| 2603.06587 | Autonomous AI Agents for Option Hedging | 缺口感知 RL 对冲 |
| 2604.02743 | Options-Driven Rough Vol Forecasting | Rough Heston + DL surrogate |
| 2606.16961 | ConvVAE for Crypto Vol Surfaces | 加密波动率曲面 |
| 2512.21798 | Deep Generative Models for Synthetic Data | 合成金融数据 |

### 3.7 LOB/微观结构/高频（8 篇）

| ID | 论文 | 核心 |
|----|------|------|
| 2403.09267 | Deep LOB Forecasting: Microstructural Guide | LOB 预测指南 |
| 2405.18938 | HLOB: Information Persistence in LOB | LOB 信息持续性 |
| 2406.19396 | SimLOB: Learning LOB Representations | LOB 表示学习 |
| 2506.07711 | Square-root Impact, Order Imbalance & Vol | 市场冲击 |
| 2508.06788 | Returns and Order Flow Imbalances | 订单流日内动态 |
| 2511.20606 | LOB Dynamics in Matching Markets | LOB 动态 |
| 2512.15720 | Hidden Order in Trades Predicts Price | 隐藏订单预测 |
| 2603.20456 | Neural HMM for HFT Order Flow | HFT 订单流 HMM |

### 3.8 执行与交易成本（11 篇）

| ID | 论文 | 核心 |
|----|------|------|
| 2402.12049 | RL Optimal Execution with Time-Varying Liquidity | RL 最优执行 |
| 2408.11773 | Deviations from Nash in Execution Game | 双 agent 执行博弈 |
| 2410.13493 | Deep RL for Online Optimal Execution | 在线执行 |
| 2506.05755 | FlowOE: RL Optimal Execution under Heston | Heston 下执行 |
| 2510.22206 | Market Simulation RL Execution | 市场仿真 RL 执行 |
| 2511.07434 | RL-Exec: Impact-Aware Liquidation | BTC-USD 胜过 TWAP/VWAP |
| 2603.29086 | Realistic Market Impact Modeling for RL | 真实市场冲击 |
| 2605.20348 | Memory-Induced Supra-Competitive RL Exec | DDQN 执行博弈 |
| 2207.11152 | Learn Continuously, Act Discretely (HALOP) | 混合动作空间 RL |
| 2502.07868 | Minimal Shortfall RL Liquidation | RL 最小化执行缺口 |
| 2012.12620 | Hierarchical RL Portfolio + Execution | 分层 RL 组合+执行 |

### 3.9 NLP/情绪/新闻/LLM+Finance（15 篇）

| ID | 论文 | 核心 |
|----|------|------|
| 2407.03689 | Text2TimeSeries | LLM 事件驱动时序 |
| 2407.16150 | FinBERT-LSTM News Sentiment | 情绪预测 |
| 2407.18103 | Fine-Tuning LLMs for Stock Return | LLM 微调预测 |
| 2410.01987 | Financial Sentiment LLMs and FinBERT | 情绪分析 |
| 2410.19025 | LLMs for Financial Time-series | LLM 时序预测 |
| 2411.00856 | AI in Investment Analysis: LLM Equity Ratings | LLM 股票评级 |
| 2412.03527 | FANAL: Financial News Alerting | 新闻预警 |
| 2412.19245 | Sentiment Trading with LLMs | LLM 情绪交易 |
| 2503.03612 | LLMs in Finance: Financial Sentiment | 金融情绪定义 |
| 2505.16136 | Interpretable ML for Macro Alpha | 宏观情绪 |
| 2604.17327 | Signal or Noise in Multi-Agent LLM | MarketSenseAI, +2.18%/月 |
| 2606.27446 | Causal Multilingual Financial QA | 因果金融 QA |
| 2409.17581 | SEC 10-K Analysis Using LLMs | SEC 文件 LLM 分析 |
| 2510.23464 | LLM Stance Detection on SEC Filings | SEC 立场检测 |
| 2105.12825 | Trade the Event: Corporate Events | 事件驱动交易 |

### 3.10 过拟合防御与回测方法论（11 篇）

| ID | 论文 | 核心 |
|----|------|------|
| 1905.08042 | Testing Sharpe Ratio: Luck or Skill? | SR 显著性检验 |
| 1911.04090 | A Post Hoc Test on the Sharpe Ratio | SR 事后检验 |
| 1905.04569 | Impact is not just volatility | 市场冲击 ≠ 波动率 |
| 2001.04185 | Zooming In on Equity Factor Crowding | Momentum 拥挤 1-2% 订单流 |
| 2502.04284 | Alpha Decay + TC Multi-period Optimal Trading | 衰减+成本 MDP |
| 2512.05900 | Finite Sample Bias in Time Series CV | 时序 CV 偏差 |
| 2602.00080 | GT-Score: 98% generalization improvement | 过拟合防御目标函数 |
| 2603.09219 | AlgoXpert: IS→WFA→OOS Protocol | 三阶段过拟合防御 |
| 2604.15531 | Spurious Predictability in Financial ML | Falsification audit, K̂_eff |
| 2512.12924 | Rigorous WFV Framework | 34 rolling windows, honest null |
| DSR | Bailey & Lopez de Prado DSR (JPM 2014) | **N2 多重比较攻击的定量武器** |

### 3.11 统计套利与因子择时（11 篇）

| ID | 论文 | 核心 |
|----|------|------|
| 2106.04028 | Deep Learning Statistical Arbitrage (Pelger) | CNN+Transformer, SR >4 gross |
| 2406.15612 | EVT-based RL for Tail Risk | 极值理论 RL |
| 2510.11616 | Attention Factors (Pelger) | Net SR 2.3, weak factors matter |
| 2512.02037 | Stat Arb in Polish Equities Using DL | LSTM+OU |
| 2302.10175 | Spatio-Temporal Momentum (Oxford-Man) | SLP > CNN/LSTM |
| 2404.18017 | DL for Factor Timing | NN 预测因子溢价 |
| 2410.14841 | Dynamic Factor Allocation Regime-Switching | IR 0.05→0.5 |
| 2412.09468 | STORM: Dual VQ-VAE Factor Model (WWW 2025) | 因子多样性+选择 |
| 2502.05218 | FactorGCL (AAAI 2025) | 超图+对比学习，Duan(FactorMAD同组) |
| 2508.14656 | DL Short Term Equity Trend: Behavior-Driven | 行为金融+ML |
| 2511.12490 | 13-Sharpe OOS Factor | ❌❌ 过拟合红旗教科书 |

### 3.12 其他主题（31 篇）

**RL/自适应（6 篇）**：2407.16376, 2412.08435, 2507.02910, 2512.04697, 2603.10299, 2410.14841

**尾部风险（4 篇）**：2308.00065, 2606.04576, 2606.26625, 2603.29086

**加密/DeFi/另类（11 篇）**：1601.00991, 2402.04775, 2407.03781, 2409.15320, 2412.13172, 2502.19615, 2503.00603, 2503.12648, 2504.13598, 2603.29751, 2604.24366

**商品/固收/宏观（7 篇）**：2412.05889, 2504.13521, 2505.15296, 2512.19484, 2602.20856, 2604.25403, 2605.24490

**体制检测（4 篇）**：2404.03319, 2510.03236, 2604.04963, 2512.12924

**时序基础模型/量化基础设施（6 篇）**：2510.00742, 2410.11674, 2310.08278, 2603.21330, 2011.09607, 2305.01505, 2403.15062

**通用自主发现（2 篇）**：2606.13662, 2511.07678

**非 arXiv（5 篇）**：DSR (JPM 2014, wiki done)、Man Group AlphaGPT (2025.11)、FX 因子 (SSRN, 6 篇)、ESG 因子 (SSRN, 6 篇)、传统经典 (JFE/RFS/JF paywall, 5 篇)

---

## §4. 撞车判定——逐 claim 对照 143 篇

| # | Claim | 状态 | 证据 |
|---|-------|------|------|
| C1 | LLM agent 能挖因子 | ✅ 被占满 | 20+ 篇证明。IC 2%-8%，Sharpe 0.7-3.1。**不要 claim** |
| C2 | Multi-agent 优于 single | ⚠️ 部分 | FactorMAD, TradingAgents, CogAlpha, ATLAS, Agora 等。全部 **fixed architecture** |
| C3 | Self-evolving memory 改善质量 | ⚠️ 部分 | FactorMiner, AlphaMemo, QuantaAlpha。全部 **factor-level memory** |
| C4 | **Deep Lit → Factor 闭环** | 🟢 白地 | 零篇。全部靠 LLM 预训练或人给方向 |
| C5 | **Adversarial Overfitting Defense as Agent Role** | 🟢 白地 | AlgoXpert/Spurious Audit 是被动 protocol。无人设"因子杀手" agent |
| C6 | **Multi-Model Consensus for Factor Quality** | 🟢 白地 | QuantaAlpha 简单 ablation，不系统 |
| C7 | **Factor Lifecycle 全闭环** | 🟢 白地 | AlphaForge/AlphaCrafter 做了部分。无人全自动 |
| C8 | **开源可复现完整研究系统** | 🟢 白地 | 2606.08285 审计 30 篇**无一完整 artifact** |
| C9 | **跨资产通用架构** | 🟢 白地 | 全部单市场 |
| C10 | **大规模并行自动化** | 🟢 白地 | 全部串行 single-thread |
| C11 | **Workflow-Level Memory** | 🟢 白地 | 全部 factor-level |

**结论：11 claim，1 占满，2 部分，8 白地。零撞车核心。Agon Alpha 是量化金融的全新系统范式。**

---

## §5. Agon Alpha 的 7 个 Architecture-Level Novelty

**N1. Factory-Loop 架构。** 143 篇中零篇使用 producer-critic adversarial loop 围绕 artifact。所有架构归为 single agent loop / fixed multi-agent pipeline / evolutionary loop 三种。量化金融全新。

**N2. Adversarial Overfitting Defense Protocol。** 不是 "t > 3.0" 统计阈值，是专职 agent 从 7 维度主动攻击每个候选因子：时间鲁棒性、universe 鲁棒性、多重比较（DSR/PSR 定量武器）、伪因子对照（EVT baseline）、前视偏差、交易成本、容量。AlgoXpert IS→WFA→OOS 和 Spurious Audit 是被动检查——可被"恰好通过阈值"绕过。对抗性攻击不能。

**N3. Deep Lit → Factor Hypothesis 闭环。** 143 篇零篇。全部依赖 LLM 预训练知识或人给方向。Agon Alpha 引入第三种知识源：系统性文献搜索→全文精读→提取因子逻辑→交叉碰撞→驱动新假设→novelty check（"这个因子 2019 年 JFE 发过了"）。

**N4. Multi-Model Consensus for Factor Robustness。** 143 篇全部单 LLM backend（多数不披露是哪个模型）。Agon Alpha：同一因子经 3+ backend 独立验证才放行。跨模型一致性作为因子质量的独立信号。

**N5. Workflow-Level Memory。** FactorMiner/AlphaMemo 做 factor-level memory（这个因子公式的哪个 edit 有效/失败）。Agon Alpha 做跨 factory 的 workflow-level memory：研究方向、搜索策略、失败模式、回测配置的长期记忆。

**N6. Full Lifecycle Factor Management。** Discovery→validation→production→decay→retirement→replacement 全自动。AlphaCrafter 做了 re-validation+deprecated，AlphaForge 做了 factor timing。无人全闭环。

**N7. Cross-Asset OmniDisciplinary。** 同一套 factory-loop 同时跑股票+期货+期权+加密+宏观。143 篇全部单市场。Agon 的 OmniDisciplinary（core agent 领域无关+context/skills 注入）天然支持。

---

## §6. 关键洞察（从 143 篇中提炼）

### 6.1 发表后的 alpha 是垃圾
Chen & Welch (2607.06502) 用 ~200 个异常做 2×2 分解。Post-2005 + top-90%-market-cap 域：median **7 bps/月**。Var(t)=1.09——全是噪音。Empirical Bayes 收缩后全部归零。仅 profitability 残存（median 24 bps）。**所有 20+ 篇 LLM agent 因子论文解决的是不存在的问题。**

### 6.2 因子拥挤可测，动量已饱和
Volpati et al. (2001.04185)：动量解释 1-2% 订单流，2012 年以来拥挤急剧上升。反直觉：trade imbalance 与动量信号**负相关**——交易者主要用 limit order。Kakushadze (1601.00991)：P~σ^0.76（R²=0.734），turnover 对收益不显著。

### 6.3 弱因子驱动套利，强因子不
Epstein/Pelger (2510.11616)：100 factor SR 4.52 > 30 factor 3.97 > 8 factor 3.35。**过去收益特征（非基本面）主导信号。** Attention mechanism 天然聚类为行业，无显式标签。Net SR 2.3 after TC。

### 6.4 最简单模型常胜复杂模型
Tan, Roberts & Zohren (2302.10175)：**单隐层 SLP 全面胜 CNN/LSTM。** 只用 5 天历史+L1 正则化。CNN/LSTM 不仅无提升，反而过拟合。Karaouli et al. (2510.00742)：**49.5K 参数 SAMFormer > 500M TimesFM。** TimesFM fine-tune 越久越差（catastrophic forgetting）。

### 6.5 Agentic search 是第一要素
Bridgewater AIA (2511.07678)：agentic vs non-agentic search **3.6×** Brier 差异。简单均值 ensemble > LLM 合成。5→10 agent 显著改善，往上递减。**这直接验证了 Deep Lit Loop 的核心价值。**

### 6.6 非线性制造虚假正交性
Nikolopoulos (2604.15531)：即使原始 K̂_eff=1.24（高度相关），门限化后暴增到 **3.34**。"Spurious orthogonality"——非线性信号提取改变了相关性结构。Kill-argument reviewer 必须专门检测此效应。

### 6.7 Reflection 有害
ATLAS (2510.15949, ACL 2026)：reflection 改善与 baseline **负相关**（r=-0.78, p<0.05）。越强的 baseline，反思后反而更差。Agon Alpha 必须用 fresh-context 独立审查，不让 agent 反思自己。

### 6.8 进化是涌现的，不是设计的
Agora (2606.29194)：8 个技能库中只有 metric 库发生了进化（2/8）。两个 accepted metrics 是跨轮涌现的，不是单个 agent 创造的。SJS 的 5 约束是被动 gate——这正是 Agon Alpha 主动 kill-argument 的差异化机会。

### 6.9 13-Sharpe 因子是过拟合红旗
Singha (2511.12490)：单作者、survivorship bias、仅 3 年 OOS、42% daily turnover、kill-switch 从未触发。教科书级的 anomaly blindness + plausible false attribution。

### 6.10 回测≠实盘，差距巨大
AlphaCrafter 回测 SR 1.53→"实盘" 0.70。LSTM 回测 AR +22.93%→"实盘" -7.74%。**腰斩是普遍规律。** 2606.08285 审计 30 篇 LLM 交易论文：**无一提供完整 artifact。**

### 6.11 换手率是最大红旗
Beyond Prompting 声称 SR 2.75 但 **105% daily turnover**——在实战中不可交易。Chen & Welch 指出算上交易成本后所有 alpha 归零。任何不报告 turnover 的论文不可信。

### 6.12 前视偏差是 LLM 死穴，且大模型更严重
Look-Ahead-Bench (2601.13770)：Llama 70B alpha decay -15pp, DeepSeek 3.2 **-22pp**。**Inverse Scaling：模型越大，记忆越强，前视偏差越严重。** PiT 模型展现正常正 scaling。

### 6.13 DSR/PSR 是 N2 的定量武器
Bailey & Lopez de Prado (JPM 2014)：DSR = PSR(E[max{ŜR}])。用极值理论估计 N 次独立试验下期望最大 SR。DSR > 0.95 意味着即使在 N 重比较后仍然显著。MinBTL 给出最小回测长度需求。

---

## §7. 25 个可直接集成的垫脚石

| # | 垫脚石 | 来源 | 集成到 Agon Alpha |
|---|--------|------|-----------------|
| 1 | Factor grammar: 10 primitives + formula/econ 联合生成 | 2603.14288 | Idea Factory 生成约束层 |
| 2 | 四级筛选: IC→correlation→replacement→dedup→full | 2602.14670 | Experiment Factory screening |
| 3 | IS→WFA→OOS: stable region+cliff veto+purge gap | 2603.09219 | Defense Protocol 基础 |
| 4 | 五种偏差框架: look-ahead/survivorship/narrative/objective/cost | 2602.14233 | 每个 factory 内置 bias checklist |
| 5 | Periodic re-validation + decay tracking + deprecated | 2605.05580 | Lifecycle monitoring |
| 6 | Regime-aware selection: 9 维 + suitability scoring | 2605.05580 | Screener agent |
| 7 | Dual-channel RAG: positive(欠覆盖)+negative(拥挤) | 2604.09601 | Deep Lit guided search |
| 8 | Experience memory: recommended + forbidden directions | 2602.14670 | Workflow Memory template |
| 9 | MCP 工具协议: winsorization/quantile/rolling/portfolio | 2604.18500 | Coder tool interface |
| 10 | Environment engineering: Docker+Git+time/cost+UI | 2606.13662 | Infrastructure layer |
| 11 | Co-STEER: DAG+(task,code,feedback) triple KB | 2505.15155 | Coder agent |
| 12 | MCTS: UCT+5维backtesting+Frequent Subtree Avoidance | 2505.11122 | Hypothesis search |
| 13 | Scaling Paradox: 大模型推理, PiT/debiased 做时序 | 2601.13770 | Model 选择策略 |
| 14 | Reproducibility audit 6 维 | 2606.08285 | Release checklist |
| 15 | Likelihood-Impact 矩阵 | 2606.24177 | Idea reviewer |
| 16 | **DSR/PSR 公式 + MinBTL** | DSR JPM 2014 | N2 多重比较攻击定量武器 |
| 17 | Factor crowding: trade imbalance 测量 | 2001.04185 | N2 容量攻击实证基础 |
| 18 | Alpha decay+TC 联合 MDP | 2502.04284 | N6 退役决策理论 |
| 19 | Factor timing via CNN/TV-PR | 2404.18017, 2410.14841 | N6 re-validation 自适应 |
| 20 | EVT-based RL: POT policy gradients | 2406.15612 | N2 伪因子对照统计基础 |
| 🔑 | **What Useful Alphas?** | 2607.06502 | 最强 motivation 论文 |
| 21 | Sealed Joint Search: 5 约束防 leakage | 2606.29194 | Evaluation 密封协议 |
| 22 | Agentic search 3.6× 验证 | 2511.07678 | Deep Lit 有效性验证 |
| 23 | Falsification Audit: K̂_eff + 5 nulls | 2604.15531 | N2 过拟合检测框架 |
| 24 | GT-Score: 98% generalization | 2602.00080 | N2 scoring 函数 |
| 25 | 101 Alphas: SR 1.24-4.16, corr 15.9% | 1601.00991 | Factor baseline + diversity 金标准 |

---

## §8. 竞品系统性缺陷 → Agon Alpha 对应解法

| 缺陷 | 证据 | Agon Alpha 解法 |
|------|------|---------------|
| 换手率不可交易 | Beyond Prompting 105%/day | N2 交易成本攻击 + auditor |
| 回测≠实盘 | AlphaCrafter SR 1.53→0.70, LSTM +22.93%→-7.74% | N2 OOS gate + paper trading |
| 前视偏差 LLM 死穴 | 大模型偏差更严重 (Inverse Scaling) | PiT/debiased 做时序，大模型只做 reasoning |
| 过拟合仅被动检查 | 全用 t>2.0/3.0 阈值 | N2 对抗性攻击 7 维度 |
| LLM backend 单一不透明 | 多数不披露模型 | N4 Multi-Model Consensus |
| OOS 太短 | 1年/195天/3月 | N2 multi-year walk-forward |
| 无一完整 artifact | 2606.08285 审计 30 篇无一全包 | Code-Artifact Separation + 全栈开源 |
| 全部单市场 | 143 篇无一架构级跨资产 | N7 OmniDisciplinary |
| 无文献驱动 | 全部预训练或人给方向 | N3 Deep Lit→Factor |
| 无 workflow memory | 只有 factor-level | N5 Workflow-Level Memory |

---

## §9. 论文质量评估：玩具 vs 实战

| 论文 | 核心结果 | 致命缺陷 | 判定 |
|------|---------|---------|------|
| AlphaForge (AAA125) | IC 4.40%, ¥3M 实盘 +21.68% | 只用 6 特征 | ⭐ 真金验证 |
| AlphaCrafter | SR 1.53→0.70 | "实盘"是 simulator | ⭐⭐ 最接近实战 |
| FactorMiner | IC 8.25%, 110 因子 | 无交易成本 | ⭐ GPU 有价值 |
| RD-Agent-Quant (NeurIPS25) | IC 0.053, IR 1.74, <$10 | Wind 数据不公开 | ⭐⭐ 最成熟开源 |
| Agora | SR 1.87, sealed holdout | 单线程, holdout 91天 | ⭐⭐⭐ 最接近但关键不同 |
| Bridgewater AIA | Brier=human superforecaster | 预测事件非资产 | ⭐⭐ Agentic search 验证 |
| 101 Alphas | SR 1.24-4.16, corr 15.9% | 非 agent 系统 | ⭐ 因子基准库 |
| Beyond Prompting | SR 2.75, turnover 105% | **不可交易** | ❌ |
| Attention Factors | Net SR 2.3, 24年 | 无代码 | ⭐⭐ Joint learning |
| What Useful Alphas? | Median 7bp/月 post-2005 | 仅 long-short | ⭐⭐⭐ 最强 motivation |
| DL Stat Arb (Pelger) | SR >4 gross | 无代码, 仅 US | ⭐⭐ Stat arb SOTA |
| Spurious Audit | K̂_eff+5 nulls | 无真机 | ⭐⭐ 过拟合框架 |
| 13-Sharpe Factor | SR 13.19 | 仅 3 年+survivorship bias | ❌❌ 反面教材 |
| ATLAS (ACL26) | Reflection paradox r=-0.78 | 仅 3 只股票 2 月 | ⭐ Adaptive-OPRO |
| Spatio-Temporal (Oxford) | SLP > CNN/LSTM | 仅 Financials 行业 | ⭐ 方法论验证 |
| TSFM Evaluation | 49.5K > 500M TimesFM | NeurIPS workshop | ⭐ Foundation model 警示 |

---

## §10. 完整论文索引（143 篇，一篇不漏）

### A. LLM Agent 因子挖掘 (18)
2308.00016, 2406.10811, 2406.18394, 2505.11122, 2505.15155, 2511.18850, 2602.07085, 2602.14670, 2603.14288, 2603.16365, 2603.20247, 2604.09601, 2604.26747, 2605.05580, 2606.20625, 2606.29194, 2510.04787, DOI:FactorMAD

### B. Multi-Agent 金融 (7)
2407.06567, 2412.20138, 2508.00554, 2510.15949, 2602.23330, 2604.18500, 2605.12532

### C. 基准与评估 (6)
2503.21422, 2601.13770, 2602.14233, 2606.08285, 2606.29771, 2605.27887

### D. 资产定价 (8)
2206.10014, 2301.09173, 2402.06635, 2403.06779, 2404.14137, 2411.19444, 2512.16251, 2604.04430

### E. 组合优化 (8)
2402.16609, 2403.07916, 2403.16667, 2405.01604, 2409.08426, 2507.05994, 2602.17098, 2605.28853

### F. 组合管理 RL/LLM (5)
2605.01384, 2605.17307, 2605.09310, 2606.08283, 2510.14264

### G. 期权与波动率 (9)
2405.06774, 2406.11520, 2504.06208, 2509.08096, 2512.12420, 2603.06587, 2604.02743, 2606.16961, 2512.21798

### H. LOB/微观结构 (8)
2403.09267, 2405.18938, 2406.19396, 2506.07711, 2508.06788, 2511.20606, 2512.15720, 2603.20456

### I. 执行与交易成本 (11)
2402.12049, 2408.11773, 2410.13493, 2506.05755, 2510.22206, 2511.07434, 2603.29086, 2605.20348, 2207.11152, 2502.07868, 2012.12620

### J. NLP/情绪/新闻 (15)
2407.03689, 2407.16150, 2407.18103, 2410.01987, 2410.19025, 2411.00856, 2412.03527, 2412.19245, 2503.03612, 2505.16136, 2604.17327, 2606.27446, 2409.17581, 2510.23464, 2105.12825

### K. 过拟合防御与回测 (11)
1905.08042, 1911.04090, 1905.04569, 2001.04185, 2502.04284, 2512.05900, 2602.00080, 2603.09219, 2604.15531, 2512.12924, DSR

### L. 统计套利与因子择时 (11)
2106.04028, 2406.15612, 2510.11616, 2512.02037, 2302.10175, 2404.18017, 2410.14841, 2412.09468, 2502.05218, 2508.14656, 2511.12490

### M. RL/自适应 (6)
2407.16376, 2412.08435, 2507.02910, 2512.04697, 2603.10299, 2410.14841

### N. 尾部风险 (4)
2308.00065, 2606.04576, 2606.26625, 2603.29086

### O. 加密/DeFi/另类 (11)
1601.00991, 2402.04775, 2407.03781, 2409.15320, 2412.13172, 2502.19615, 2503.00603, 2503.12648, 2504.13598, 2603.29751, 2604.24366

### P. 商品/固收/宏观 (7)
2412.05889, 2504.13521, 2505.15296, 2512.19484, 2602.20856, 2604.25403, 2605.24490

### Q. 体制检测 (4)
2404.03319, 2510.03236, 2604.04963, 2512.12924

### R. 时序基础模型/量化基础设施 (6)
2510.00742, 2410.11674, 2310.08278, 2603.21330, 2011.09607, 2305.01505, 2403.15062

### S. 通用自主发现 (2)
2606.13662, 2511.07678

### T. 非 arXiv 已获取 (1)
DSR (Bailey & Lopez de Prado, JPM 2014, PDF 1205行, wiki done)

### U. 非 arXiv 未获取（结构性障碍）
FX 因子 (SSRN, 6篇)、ESG/气候因子 (SSRN, 6篇)、传统经典 (JFE/RFS/JF paywall, 5篇)、Man Group AlphaGPT

---

## §11. 搜索日志

| Round | Queries | 选中 | 累计 | 关键发现 |
|-------|---------|------|------|---------|
| R1-R3 | 28 | 19 | 19 | LLM agent 因子挖掘核心群 |
| R4-R6 | 38 | 22 | 41 | 扩展到执行、NLP、波动率 |
| R7-R9 | 30 | 26 | 67 | 组合优化、尾部风险、加密 |
| R10-R12 | 20 | 19 | 86 | 资产定价、回测方法论 |
| R13-R15 | 25 | 33 | 119 | 过拟合防御、统计套利、因子择时 |
| R16-R19 | 30 | 18 | 137 | 体制检测、时序FM、多agent交易 |
| R20-R21 | 28 | 6 | 143 | 量化基础设施、金融LLM推理 |
| **总计** | **199** | **143** | **143** | 24 子领域覆盖 |

---

## §12. 下一步

1. **Deep lit**：arXiv 已接近饱和（R21 的 24 维度搜索返回几乎全是非金融噪音）。非 arXiv 文献（SSRN/journals）存在结构性障碍（Cloudflare/paywall），需手动逐个绕过或接受元数据引用。

2. **Idea Factory 可启动**：8 个白地 claim × 25 个垫脚石 = 充足种子。优先 N2（Adversarial Overfitting Defense Protocol）或 N3（Deep Lit → Factor Hypothesis 闭环）——最强差异化，零竞品覆盖。

3. **Landscape 是活文档**：后续 deep lit 新发现持续追加到 §3 对应主题和 §10 索引。
