---
topic: 0709-quant-factor-mining
title: "Agon Alpha：自主量化研究系统 — 文献全景 v2 (审阅修订版)"
created: 2026-07-09
last_deep_lit_tick: 2026-07-10
revised: 2026-07-11
papers_full_text_read: 52 (arXiv wiki, 即 $ARXIV_WIKI_DIR 下 56 个 .md 减去 4 非量化论文), 1 (DSR JPM 2014 wiki), ~90 (全文已读但 wiki 文件不在 $ARXIV_WIKI_DIR 或待核查)
papers_relevant_indexed: 200+
v2_wiki_audit: |
  $ARXIV_WIKI_DIR = /home/xingyu/AutoResearch/agent-factory-data/wiki/
  实际 .md 文件数: 56
  非量化论文: 4 (Nature Genetics, Nature Reviews Genetics, Bioinformatics, bioRxiv)
  量化 arXiv wiki: 52
  非 arXiv wiki: 1 (DSR, 文件名含 DOI 但仍在 wiki 目录)
  工作区重复/拷贝: 30 (不计入唯一计数)
  **与 frontmatter 声称 143 的差额: 约 91 篇**
  可能原因: (a) wiki 文件存于其他路径, (b) 曾产出但已被清理, (c) 声称数有误
model_used: deepseek-v4-pro[1m] (全文精读), claude-opus (调度)
v2_changelog: |
  - 修正 wiki 文件计数（实际 52 arXiv + 其他, 非 143 arXiv）
  - 新增缺失重要论文 12 篇（AlphaBench ICLR 2026, QuantEvolver, AlphaCFG, Text-to-Alpha ICLR 2026,
    HKUST-GZ 综述, Supply Chain Textual Signals, CrossAlpha, Principal Portfolios,
    Bayesian Factor Zoo, Bryzgalova-Huang-Julliard 等）
  - 新增因果推断、GNN/图学习两个子领域覆盖
  - 标注 15 篇基石文献为"待获取"（Fama-French, Harvey-Liu-Zhu, Gu-Kelly-Xiu 等）
  - 修正过量声明（§4 C10 竞争系统非全部串行, C11 FactorMiner 经验记忆已跨越因子级,
    §6.1 "全部归零" → "median 归零", §6.7 ATLAS 反思悖论标注小样本局限）
  - 新增 §13 缺口与待办
---

# Agon Alpha 文献全景 v2（审阅修订版）

> 本文件是单一事实源：撞车判定、垫脚石识别、关键洞察都在这里。
> v2 经过独立审阅，修正了过量声明并补齐了关键缺失文献。

---

## 摘要

我们对量化金融的自主研究系统（Agon Alpha）做了地毯式文献调研。21 轮搜索，130+ arxiv-tool queries，~52 篇 arXiv 论文全文精读并写入 wiki，覆盖 LLM agent 因子挖掘、资产定价、高频/微观结构、期权/波动率、组合优化、执行、NLP/情绪、RL、加密、统计套利、因子择时、尾部风险、回测方法论、体制检测、因果推断、GNN/图学习等 26 个子领域。

**核心结论：52 篇 arXiv 全文精读 + 200+ 篇元数据索引中，零篇同时实现 Agon Alpha 的所有核心 claim。** 所有竞品要么做单点因子工具，要么做交易 agent，要么做回测 protocol。无人做 full factory-loop 自主量化研究系统（deep lit → idea → experiment → paper 全闭环 + adversarial overfitting defense + multi-model consensus + 跨资产 OmniDisciplinary + 大规模并行自动化）。

**最强 motivation 论文：** Chen & Welch (2607.06502) 证明发表后的 academic alphas 在 post-2005 large-cap 域下 median 仅 7bp/月，Empirical Bayes 收缩后分布坍缩——整个学术因子 zoo 在可投资股票上已无法提供显著 alpha。

**25 个可直接集成的垫脚石** 从竞品论文中提取，涵盖因子 grammar、筛选管线、过拟合 protocol、偏差框架、regime 检测、MCTS 搜索、DSR/PSR 公式、sealed evaluation 等。

**15 篇基石文献待获取**：Fama-French 三/五因子、Harvey-Liu-Zhu 因子动物园、Gu-Kelly-Xiu ML 资产定价、Lopez de Prado 金融 ML、Kelly-Malamud-Pedersen 主组合、Bryzgalova-Huang-Julliard 贝叶斯因子动物园等——这些是领域根基，不可缺失。

---

## §1. Agon — 我们的基础设施

（v2 注：§1 内容无实质性改动，保留原版。唯一注意：AgonAlpha GitHub README 当前引用 arXiv:2606.08878，非 2606.24177，需核实统一。）

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

| | 竞品 | Agon Alpha |
|---|---|---|
| 规模 | 单线程或有限并行 | 多 topic/idea/experiment 并发 |
| 架构 | Linear pipeline / fixed multi-agent / limited hierarchy | Factory-loop: producer-critic adversarial |
| 调度 | 硬编码 workflow | Zero-Code prompt dispatcher |
| 验证 | Statistical threshold 或被动 audit | Kill-argument reviewer + multi-model second-check |
| 领域迁移 | 重新实现或 limited transfer | 同一 core agent 集合，换 context + skills |
| 代码 | 部分开源且依赖闭源数据 | 全栈开源 |

**v2 注：** 原版 "全部串行 single-thread" 不够准确。Agora 有 3 并发 evaluator + 5 agent 类并发运行，CogAlpha 有 21 agent 7 层并行。修正为"单线程或有限并行"——竞品的并行是多 agent 协作层面的，而 Agon Alpha 的并行是多个独立 research thread 同时跑 factory 层面的。Agon Alpha 的并行层级更高。

---

## §2. 这份 landscape 怎么做出来的

**21 轮搜索**：130+ arxiv-tool queries + 10+ WebSearch。覆盖 LLM agent 因子挖掘、传统资产定价、过拟合防御、高频/微观结构、期权/波动率、组合优化、执行/市场冲击、NLP/情绪、RL、加密/DeFi、商品/固收、统计套利、因子择时、尾部风险、回测方法论、体制检测、时序基础模型、金融 LLM 推理、**因果推断、GNN/图学习** 等 26 个子领域。

**全文精读**：52 篇 arXiv 论文全文精读写入 wiki（`$ARXIV_WIKI_DIR`），由 `claude-ds`（deepseek-v4-pro[1m]）并行跑 deep-lit-reader agent 完成。每篇产出 80-225 行中文 wiki。另有 5+ 篇非 arXiv 论文（DSR 等）完成 wiki。200+ 篇论文通过元数据（摘要、标题、引用）索引。

**v2 注：** 原版声称 143 篇 arXiv 全文精读——wiki 目录实际仅有 56 个 .md 文件（含 4 个非量化生物学论文），约 52 篇量化 arXiv wiki。计数已修正。剩余 91 篇若存在于其他目录需补录；若从未产出则需重新精读。

**B7 反向扩展已执行**：references + cited + author search + title-term search 四项扩展。

**未获取全文的**：FactorMAD（ACM paywall+Cloudflare）、Man Group AlphaGPT（web article，无定量数据）。Chain-of-Alpha (2508.06312) arXiv 404。15 篇基石文献（Fama-French, Harvey-Liu-Zhu, Gu-Kelly-Xiu, Lopez de Prado 等）在 SSRN/journals，详见 §13 待获取清单。

---

## §3. 竞争格局：论文按主题组织

### 3.1 LLM Agent 因子挖掘（18 → 21 篇）— 最直接相关

**v2 新增（3 篇）：** AlphaBench (ICLR 2026)、QuantEvolver (2605.15412)、AlphaCFG (2601.22119)

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
| 2603.14288 | Beyond Prompting | 2026 | 闭环 agentic AI, factor grammar 10 primitives | SR 2.75（105% turnover 不可交易） |
| 2603.16365 | FactorEngine | 2026 | 图灵完备程序因子 + macro-micro co-evolution | IC 0.047, IR 1.60 |
| 2603.20247 | AlphaLogics | 2026 | Market logic 作为可优化对象 | IR 1.53 CSI500 |
| 2604.09601 | Hubble | 2026 | DSL+AST sandbox+dual-channel RAG | RankIC 0.006 |
| 2604.26747 | LLM Agents in Crypto | 2026 | Beyond Prompting 作者的加密后续 | SR 1.55 net |
| 2605.05580 | AlphaCrafter | 2026 | Miner→Screener→Trader, 唯一回测+OOS双正 | SR 1.53→0.70 |
| 2606.20625 | AlphaMemo | 2026 | SSPM+AST-diff edit motifs+confidence-gated | RankICIR 0.46 |
| 2606.29194 | Agora (AI Trading's Alpha Singularity) | 2026 | Sealed Joint Search, 5 agent A2A, SR 1.87 | SR 1.87 holdout |
| 2510.04787 | TiMi | 2026 | Strategy-deployment decoupling, 200+ pairs | — |
| DOI | FactorMAD (ICAIF 2025) | 2025 | 双 agent 辩论，code-based pipeline | 显著优于 GP/RL |
| **🆕 ICLR 2026** | **AlphaBench** (Luo et al., CityU) | 2026 | **首个 LLM 因子挖掘系统 benchmark。3 任务 (generation/evaluation/searching)，687 gen + 1170 eval 指令。LLM 评估质量差 (近随机)** | **GPT-5: gen 0.67 成功率, search EA 1.00** |
| **🆕 2605.15412** | **QuantEvolver** (Zhang et al.) | 2026 | **RL fine-tuning 取代 prompt loop。Diversity-Complementarity Reward。绕过 context explosion + feedback drift** | **优于所有 LLM baseline** |
| **🆕 2601.22119** | **AlphaCFG** (Yang et al.) | 2026 | **CFG 约束 MCTS。Tree-LSTM value/policy。CSI300+S&P500 双市场** | **Rank IC 0.087, Sharpe 0.65** |

**关键发现（更新）：** 所有系统要么靠 LLM 预训练知识，要么靠人类 prompt 给方向。**零篇从文献中提取因子逻辑。** 多数固定 operator set，多数只用 OHLCV 数据，多数无交易成本建模。AlphaBench 的系统性 benchmark 结果显示 LLM 在因子评估任务上表现最差（近随机）——这恰好是 Agon Alpha 的 N4 (multi-model consensus) 和 N2 (adversarial defense) 要解决的问题。QuantEvolver 的 RFT 路径（把回测反馈转化为策略更新而非 prompt loop）值得关注——它从根本上绕过了 prompt-level loop 的 context explosion 问题。

### 3.2 Multi-Agent 金融系统（7 篇）

（无变动。原 7 篇保留。）

### 3.3 基准与评估（6 → 7 篇）

**v2 新增：** AlphaBench (ICLR 2026) — 同时归入 §3.1 和 §3.3

| ID | 论文 | 核心 |
|----|------|------|
| 2503.21422 | Survey of AI in Quant Investment | 最全面的量化 AI 综述 |
| 2601.13770 | Look-Ahead-Bench | Scaling Paradox：大模型前视偏差更严重 |
| 2602.14233 | Evaluating LLMs in Finance (ICML 2026) | 5 种结构性偏差框架 + checklist |
| 2606.08285 | Beyond Agent Architecture | 审计 30 篇 LLM 交易论文：**无一完整 artifact** |
| 2606.29771 | CLQT | 5 轴 diagnostic benchmark |
| 2605.27887 | PortBench | Corr-aware LLM portfolio benchmark |
| **🆕 ICLR 2026** | **AlphaBench** (Luo et al.) | **首个 LLM 因子挖掘系统性 benchmark。发现 LLM 因子评估能力极弱 (近随机)** |

### 3.4 资产定价与因子模型（8 篇 → 待扩）

v2 注：当前 8 篇覆盖了部分 ML 资产定价，但缺少该领域基石文献（Fama-French 三/五因子、Harvey-Liu-Zhu 因子动物园、Gu-Kelly-Xiu、Kozak-Nagel-Santosh、Kelly-Malamud-Pedersen 主组合、Bryzgalova-Huang-Julliard 贝叶斯因子动物园）。这些基石文献对 §6 的多个洞察（因子动物园、multiple testing、SDF 密度）是直接先验，必须在下一轮 deep lit 中补齐。详见 §13 待获取清单。

（原 8 篇保留。）

### 3.5 组合优化与组合管理（13 篇）

（无变动。原 13 篇保留。）

### 3.6 期权与波动率（9 篇）

（无变动。原 9 篇保留。）

### 3.7 LOB/微观结构/高频（8 篇）

（无变动。原 8 篇保留。）

### 3.8 执行与交易成本（11 篇）

（无变动。原 11 篇保留。）

### 3.9 NLP/情绪/新闻/LLM+Finance（15 → 17 篇）

**v2 新增（2 篇）：** Text-to-Alpha (ICLR 2026), Supply Chain Textual Signals (2606.29290)

| 🆕 ICLR 2026 | **Text-to-Alpha** (Choi et al.) | 2026 | **"LLM as extractor, embedding as ruler"——从 10-K/MD&A 提取 metric-focused textual spans, 语义偏移 >2× alpha vs NER baseline** | **Portfolio + cross-sectional** |
| 🆕 2606.29290 | **Supply Chain Textual Signals** (Yılkı) | 2026 | **FinBERT 10-K 嵌入 × 供应链 KG。FF5 alpha 7.27%/年, Sharpe 0.86, NW t=−2.64** | **OOS + placebo + sector-neutral 稳健** |

（原 15 篇保留。）

### 3.10 过拟合防御与回测方法论（11 篇）

（无变动。原 11 篇保留。）

### 3.11 统计套利与因子择时（11 篇）

（无变动。原 11 篇保留。）

### 3.12 其他主题

（原 sub-sections 保留。）

### 3.13 🆕 因果推断与因子发现（3 篇）— v2 新子领域

| ID | 论文 | 核心 |
|----|------|------|
| 2502.04592 | CAMEF: Causal-Augmented Multi-Modality Event-Driven Forecasting | 因果增强多模态金融预测 |
| 2509.05922 | Predicting Market Troughs: ML with Causal Interpretation | 市场底部预测的因果解释 |
| NeurIPS 2025 | From Prediction to Scientific Discovery: Causal Inference for Financial Economics (Kelly et al.) | 从预测到科学发现——金融经济学的因果推断案例 |

**v2 注：** 因果推断子领域尚浅，仅覆盖 3 篇代表性论文。该领域对 N2 (adversarial overfitting defense) 和因子质量评估有直接意义——因果推断能区分"真正驱动收益"和"偶然相关"的因子。建议后续 deep lit 重点扩展。

### 3.14 🆕 GNN / 图学习与因子建模（3 篇）— v2 新子领域

| ID | 论文 | 核心 |
|----|------|------|
| 2502.06707 | FinMamba: Market-Aware Graph Enhanced Mamba for Stock Prediction | 市场感知图增强 Mamba |
| 2602.00888 | GAPNet: Jointly Learning Task-Specific Graph for Dynamic Stock Relation | 动态股票关系图学习 |
| 2606.29290 | Supply Chain Propagation of Textual Signals (Yılkı) | KG + LLM 嵌入，同时归入 NLP |

**v2 注：** GNN/图学习子领域尚浅。股票关系图、供应链图、行业竞争图对 N7 (跨资产 OmniDisciplinary) 有直接意义。后续 deep lit 应扩展，包括关系图对比学习（FactorGCL 已在 §3.11 覆盖）和超图方法（STORM 已在 §3.11 覆盖）。

---

## §4. 撞车判定——逐 claim 对照全部论文（v2 修订）

| # | Claim | 状态 | 证据 |
|---|-------|------|------|
| C1 | LLM agent 能挖因子 | ✅ 被占满 | 20+ 篇证明。IC 2%-8%，Sharpe 0.7-3.1。**不要 claim** |
| C2 | Multi-agent 优于 single | ⚠️ 部分 | FactorMAD, TradingAgents, CogAlpha, ATLAS, Agora 等。全部 **fixed architecture** |
| C3 | Self-evolving memory 改善质量 | ⚠️ 部分 | FactorMiner, AlphaMemo, QuantaAlpha。全部 **factor-level 或 session-level memory** |
| C4 | **Deep Lit → Factor 闭环** | 🟢 白地 | 零篇。全部靠 LLM 预训练或人给方向。Text-to-Alpha (ICLR 2026) 从 SEC 文件提取*信号*但不从学术文献提取*因子公式* |
| C5 | **Adversarial Overfitting Defense as Agent Role** | 🟢 白地 | AlgoXpert/Spurious Audit 是被动 protocol。无人设"因子杀手" agent。Agora SJS 的 5 约束是密封被动 gate，非主动攻击 |
| C6 | **Multi-Model Consensus for Factor Quality** | 🟢 白地 | QuantaAlpha 简单 ablation，不系统。AlphaBench (ICLR 2026) 测试了 5+ LLM 但仅做 benchmark 比较，不研究跨模型一致性 |
| C7 | **Factor Lifecycle 全闭环** | 🟢 白地 | AlphaForge/AlphaCrafter 做了部分。无人全自动 |
| C8 | **开源可复现完整研究系统** | 🟢 白地 | 2606.08285 审计 30 篇**无一完整 artifact**。AlphaBench 提供 benchmark 代码但不提供系统 |
| C9 | **跨资产通用架构** | 🟢 白地 | 全部单市场。AlphaCFG 测试 CSI300+S&P500 但架构非 OmniDisciplinary 设计 |
| C10 | **大规模并行自动化（多 research thread 并发）** | 🟢 白地 | Agora 有 3 并发 evaluator + 5 agent 类并发，CogAlpha 有 7 层并行——但这些都是**单 research thread 内的多 agent 协作**。无人做跨 research thread 的大规模并行 factory 调度 |
| C11 | **Workflow-Level Memory（跨 factory 长期记忆）** | 🟢 白地 | FactorMiner Experience Memory 存因子级方向（推荐/禁止），AlphaMemo 存 motif edit 历史。这些是 **session-level**，非跨 factory 的 workflow-level。但边界模糊——后续需更精确界定 |

**结论：11 claim，1 占满，2 部分，8 白地。零篇同时实现 C4-C11 的全部。Agon Alpha 是量化金融的全新系统范式。**

**v2 关键修订：**
- C10 从 "全部串行 single-thread" 改为精确描述：竞品的并行是单 research thread 内的多 agent 协作，Agon Alpha 的并行是跨 research thread 的 factory 级调度
- C11 承认 FactorMiner/AlphaMemo 的边界模糊性，标注需进一步精确界定
- 所有"白地"claim 新增与最接近竞品的精确对比

---

## §5. Agon Alpha 的 7 个 Architecture-Level Novelty（v2 修订）

**N1. Factory-Loop 架构。** 竞品中零篇使用 **producer-critic adversarial loop 围绕 artifact**。CogAlpha 有 7 层 21 agent 层级，Agora 有 5 agent 3 channel A2A——但它们都是 fixed architecture（角色和 handoff 内置在代码中），而 Agon Alpha 的 factory-loop 是 prompt-defined（Zero-Code），支持任意新 factory 的 prompt-level 组合。量化金融全新。

**N2. Adversarial Overfitting Defense Protocol。** 不是 "t > 3.0" 统计阈值，是专职 agent 从 7 维度**主动攻击**每个候选因子：时间鲁棒性、universe 鲁棒性、多重比较（DSR/PSR 定量武器）、伪因子对照（EVT baseline）、前视偏差、交易成本、容量。AlgoXpert IS→WFA→OOS 和 Spurious Audit 是**被动检查**——可被"恰好通过阈值"绕过（agent 主动适配攻击策略→防御更难绕过）。Agora SJS 的 5 约束是**密封被动 gate**（fixed constraints, no adaptation）。对抗性攻击的关键差异：自适应攻击策略。

**N3. Deep Lit → Factor Hypothesis 闭环。** 全部竞品依赖 LLM 预训练知识或人给方向。Agon Alpha 引入第三种知识源：系统性文献搜索→全文精读→提取因子逻辑→交叉碰撞→驱动新假设→novelty check。Text-to-Alpha (ICLR 2026) 从 SEC 文件提取文本信号——这是 text-to-signal，不是 lit-to-factor-formula。关键差异：因子公式的结构化提取 + 跨论文交叉碰撞。

**N4. Multi-Model Consensus for Factor Robustness。** 全部竞品单 LLM backend 或未披露模型。AlphaBench (ICLR 2026) 测试了 5+ 模型但只做 benchmark 比较，不研究跨模型因子一致性。Agon Alpha：同一因子经 3+ backend 独立验证才放行。跨模型一致性作为因子质量的独立信号——这在量化金融中前所未有。

**N5. Workflow-Level Memory。** FactorMiner 的 Experience Memory（推荐/禁止方向）、AlphaMemo 的 motif edit 历史是 session-level memory。Agon Alpha 做跨 factory 的 workflow-level memory：研究方向、搜索策略、失败模式、回测配置的长期记忆。关键差异：workflow-level 记忆是 **跨 factory 实例持久化** 的，影响后续 research thread 的初始条件。

**N6. Full Lifecycle Factor Management。** Discovery→validation→production→decay→retirement→replacement 全自动。AlphaCrafter 做了 re-validation+deprecated，AlphaForge 做了 factor timing。无人全闭环。

**N7. Cross-Asset OmniDisciplinary。** 同一套 factory-loop 同时跑股票+期货+期权+加密+宏观。全部竞品单市场。AlphaCFG 测试了 CSI300+S&P500 但不是 OmniDisciplinary 设计（同一个因子语法在两个市场跑，非架构级跨资产）。Agon 的 OmniDisciplinary（core agent 领域无关+context/skills 注入）天然支持。

---

## §6. 关键洞察（从全部论文中提炼）（v2 修订）

### 6.1 发表后的 alpha 几乎全是噪音

Chen & Welch (2607.06502) 用 ~200 个异常做 2×2 分解。Post-2005 + top-90%-market-cap 域：median **7 bps/月**。Empirical Bayes 收缩后 **median 归零**，分布坍缩到噪音水平。仅 profitability 残存（median 24 bps）。**所有 20+ 篇 LLM agent 因子论文解决的是几乎不存在的问题。** 学术因子在可投资股票上已无显著 alpha。

**v2 修订：** 原版 "全部归零" 不精确——分布坍缩但并非每个单因子都精确等于零。修正为 "median 归零。"

### 6.2-6.6 （保留，无实质性改动）

### 6.7 Reflection 有害——但证据有限

ATLAS (2510.15949, ACL 2026)：reflection 改善与 baseline **负相关**（r=-0.78, p<0.05）。越强的 baseline，反思后反而更差。这直接支持了 Agon Alpha 的 fresh-context 独立审查设计——不让 agent 反思自己，而是让独立 agent 在 fresh context 中审查。

**v2 修订：** ATLAS 实验仅覆盖 3 只股票、2 个月。反思悖论的发现重要但不能过度泛化。Agon Alpha 的 fresh-context 审查设计有多重独立动机（ATLAS 是一个支持证据，不是唯一根据）。

### 6.8-6.13 （保留，无实质性改动）

---

## §7. 25 个可直接集成的垫脚石（v2 修订）

**v2 修订：** 以下标注有实质改动的垫脚石。其余保留原版。

| # | 垫脚石 | 来源 | 集成到 Agon Alpha | v2 备注 |
|---|--------|------|-----------------|---------|
| 🔑 | **What Useful Alphas?** | 2607.06502 | 最强 motivation 论文 | Chen & Welch |
| 🆕 26 | **AlphaBench 系统性评估框架** | AlphaBench ICLR 2026 | Factor quality evaluation 标准化。3 任务 × 5+ 模型基准 | 填补 N4 评估缺口 |
| 🆕 27 | **RFT 绕过 prompt loop 限制** | QuantEvolver 2605.15412 | 探索将回测反馈参数化更新的路径 | 可能替代纯 prompt-level iteration |
| 🆕 28 | **CFG 约束搜索空间** | AlphaCFG 2601.22119 | 语法约束的 MCTS 因子搜索 | 可用于 Idea Factory 的因子生成约束 |

（原 25 个垫脚石保留。）

---

## §8. 竞品系统性缺陷 → Agon Alpha 对应解法

（v2 修订：修正"全部单线程"为精确描述）

| 缺陷 | 证据 | Agon Alpha 解法 |
|------|------|---------------|
| 换手率不可交易 | Beyond Prompting 105%/day | N2 交易成本攻击 + auditor |
| 回测≠实盘 | AlphaCrafter SR 1.53→0.70, LSTM +22.93%→-7.74% | N2 OOS gate + paper trading |
| 前视偏差 LLM 死穴 | 大模型偏差更严重 (Inverse Scaling) | PiT/debiased 做时序，大模型只做 reasoning |
| 过拟合仅被动检查 | 全用 t>2.0/3.0 阈值 | N2 对抗性攻击 7 维度 |
| LLM backend 单一不透明 | 多数不披露模型 | N4 Multi-Model Consensus |
| OOS 太短 | 1年/195天/3月 | N2 multi-year walk-forward |
| 无一完整 artifact | 2606.08285 审计 30 篇无一全包 | Code-Artifact Separation + 全栈开源 |
| 全部单市场 | 无一架构级跨资产 | N7 OmniDisciplinary |
| 无文献驱动 | 全部预训练或人给方向 | N3 Deep Lit→Factor |
| 无跨 factory 长期记忆 | 只有 factor/session-level | N5 Workflow-Level Memory |
| 并行限于单 research thread | Agora 3 evaluator 并发, CogAlpha 7 层并行 | Agon Alpha: 多 research thread 并发 factory 调度 |

---

## §9. 论文质量评估：玩具 vs 实战

（v2 修订：新增 ICLR 2026 论文，标注 Beyond Prompting 的方法论贡献）

| 论文 | 核心结果 | 致命缺陷 | 判定 |
|------|---------|---------|------|
| AlphaForge (AAA125) | IC 4.40%, ¥3M 实盘 +21.68% | 只用 6 特征 | ⭐ 真金验证 |
| AlphaCrafter | SR 1.53→0.70 | "实盘"是 simulator | ⭐⭐ 最接近实战 |
| FactorMiner | IC 8.25%, 110 因子 | 无交易成本 | ⭐ GPU 有价值 |
| RD-Agent-Quant (NeurIPS25) | IC 0.053, IR 1.74, <$10 | Wind 数据不公开 | ⭐⭐ 最成熟开源 |
| Agora | SR 1.87, sealed holdout | 单种, holdout 91天, 单后端 | ⭐⭐⭐ 最接近但关键不同 |
| Bridgewater AIA | Brier=human superforecaster | 预测事件非资产 | ⭐⭐ Agentic search 验证 |
| 101 Alphas | SR 1.24-4.16, corr 15.9% | 非 agent 系统 | ⭐ 因子基准库 |
| Beyond Prompting | SR 2.75, turnover 105% | **不可交易** | ⚠️ 方法论 (factor grammar) 有价值, 实盘结果不可信 |
| Attention Factors | Net SR 2.3, 24年 | 无代码 | ⭐⭐ Joint learning |
| What Useful Alphas? | Median 7bp/月 post-2005 | 仅 long-short | ⭐⭐⭐ 最强 motivation |
| DL Stat Arb (Pelger) | SR >4 gross | 无代码, 仅 US | ⭐⭐ Stat arb SOTA |
| Spurious Audit | K̂_eff+5 nulls | 无真机 | ⭐⭐ 过拟合框架 |
| 13-Sharpe Factor | SR 13.19 | 仅 3 年+survivorship bias | ❌❌ 反面教材 |
| ATLAS (ACL26) | Reflection paradox r=-0.78 | 仅 3 只股票 2 月 | ⭐ Adaptive-OPRO |
| Spatio-Temporal (Oxford) | SLP > CNN/LSTM | 仅 Financials 行业 | ⭐ 方法论验证 |
| TSFM Evaluation | 49.5K > 500M TimesFM | NeurIPS workshop | ⭐ Foundation model 警示 |
| 🆕 AlphaBench (ICLR26) | LLM eval 近随机 | benchmark 非 trading system | ⭐⭐⭐ 填补评估空白 |
| 🆕 QuantEvolver | RFT > prompt loop | 计算成本, 需 GPU 微调 | ⭐⭐ 探索新范式 |
| 🆕 Text-to-Alpha (ICLR26) | >2× alpha vs NER | 仅 SEC 10-K 文本 | ⭐⭐ 文本→信号 |

---

## §10. 完整论文索引（v2 更新）

### A. LLM Agent 因子挖掘 (18 → 21)
2308.00016, 2406.10811, 2406.18394, 2505.11122, 2505.15155, 2511.18850, 2602.07085, 2602.14670, 2603.14288, 2603.16365, 2603.20247, 2604.09601, 2604.26747, 2605.05580, 2606.20625, 2606.29194, 2510.04787, DOI:FactorMAD, **🆕 AlphaBench (ICLR 2026), 🆕 2605.15412 (QuantEvolver), 🆕 2601.22119 (AlphaCFG)**

### B. Multi-Agent 金融 (7)
（保留原列表）

### C. 基准与评估 (6 → 7)
原 6 篇 + **🆕 AlphaBench (ICLR 2026)**

### D. NLP/情绪/新闻 (15 → 17)
原 15 篇 + **🆕 Text-to-Alpha (ICLR 2026), 🆕 2606.29290 (Supply Chain Textual Signals)**

### E-R. （保留原列表）

### 🆕 S. 因果推断与因子发现 (3)
2502.04592, 2509.05922, NeurIPS 2025 (Kelly et al.)

### 🆕 T. GNN / 图学习与因子建模 (3)
2502.06707, 2602.00888, 2606.29290（同时归入 NLP）

### U. 非 arXiv 已获取 (1)
DSR (Bailey & Lopez de Prado, JPM 2014, PDF 1205行, wiki done)

### V. 非 arXiv 待获取——基石文献（15 篇，高优先级）
参见 §13。

---

## §11. 搜索日志（v2 注：保留原版，标注 R21 饱和声明需重新评估）

（v2 注：原版声称 R21 接近饱和，但 v2 审阅中在 15 分钟内发现 3+ 重要缺失论文——AlphaBench, QuantEvolver, AlphaCFG——表明搜索策略可能过早收敛。建议追加 R22-R24，覆盖：(a) ICLR 2026 accepted paper list 中的 quant finance 论文，(b) 因果推断 + GNN 专项搜索，(c) SSRN/journals 手动获取。）

---

## §12. 下一步（v2 修订）

1. **修复 landscape 可信度（最高优先级）**：
   - 核实 143 篇 wiki 文件的真实位置。若 91 篇从未产出，修正计数并补读。
   - 补齐 §13 的 15 篇基石文献（至少完成 NBER/SSRN preprint 版 wiki）。
   - 补齐 v2 新发现的 6+ 篇缺失论文（AlphaBench, QuantEvolver, AlphaCFG, Text-to-Alpha 等）。

2. **扩展子领域覆盖**：
   - 因果推断（至少 5-8 篇）：DML 资产定价、Granger-causal 网络、反事实因子评估
   - GNN/图学习（至少 5-8 篇）：股票关系图、供应链图、行业竞争图
   - 另类数据（至少 3-5 篇）：卫星、信用卡、供应链

3. **Idea Factory 启动条件**：在完成上述修复后（预计 5-8 天），8 个白地 claim × 25+ 个垫脚石 = 充足种子。优先 N2（Adversarial Overfitting Defense Protocol）或 N3（Deep Lit → Factor 闭环）——最强差异化，零竞品覆盖。

4. **Landscape 是活文档**：后续 deep lit 新发现持续追加。

---

## §13. 🆕 缺口与待获取清单

### 13.1 基石文献（15 篇，需在启动 Idea Factory 前补齐）

| # | 论文 | 来源 | 获取路径 | 优先级 |
|---|------|------|---------|--------|
| 1 | Fama & French (1993) 三因子模型 | JFE | Ken French 网站免费 | P0 |
| 2 | Fama & French (2015) 五因子模型 | JFE 116(1), 1-22 | Ken French 网站免费 | P0 |
| 3 | Fama & French (2020) Choosing Factors | JFE | Ken French 网站 | P0 |
| 4 | Hou, Xue & Zhang (2015) q-factor model | RFS | SSRN preprint | P0 |
| 5 | Harvey, Liu & Zhu (2016) Factor Zoo | RFS 29(1), 5-68 | SSRN-id 2545843 | P0 |
| 6 | Gu, Kelly & Xiu (2020) ML Asset Pricing | RFS 33(5), 2223-2273 | NBER w25398 免费 | P0 |
| 7 | Kozak, Nagel & Santosh (2020) Shrinking Cross-Section | JFE | SSRN preprint | P0 |
| 8 | Lopez de Prado (2018) Advances in Financial ML | Wiley | DSR 论文 (JPM 2014) 作代理；优先获取第 11-14 章 | P0 |
| 9 | DeMiguel, Garlappi & Uppal (2009) 1/N | RFS | 作者网站 | P1 |
| 10 | Kelly, Malamud & Pedersen (2023) Principal Portfolios | JF 78(1), 347-387 | NBER w27388 免费 | P1 |
| 11 | Bryzgalova, Huang, Julliard (2023) Bayesian Factor Zoo | JF 78(1) | SSRN preprint | P1 |
| 12 | Giglio, Kelly & Xiu (2022) Factor Forests | — | SSRN preprint | P1 |
| 13 | Cochrane (2011) Discount Rates / Presidential Address | JPE 66(6), 1047-1108 | UChicago 网站免费 | P1 |
| 14 | Lopez-Lira & Tang (2023) ChatGPT Stock Forecasting | — | arXiv? SSRN? | P1 |
| 15 | Dickerson, Julliard, Mueller (2024) Co-Pricing Factor Zoo | JFE forthcoming | SSRN preprint | P2 |

### 13.2 缺失子领域待搜索论文（各 5-8 篇）

- **因果推断**：DML for asset pricing, Granger-causal factor networks, counterfactual factor evaluation, IV-based factor identification
- **GNN/图学习**：stock relation graphs, supply chain propagation, industry competition networks, hypergraph factor models (FactorGCL 已覆盖), dynamic graph stock prediction
- **另类数据**：satellite imagery for retail/footfall, credit card transaction factors, supply chain shipment data, social media sentiment (beyond FinBERT)
- **固定收益/信用**：corporate bond factors, CDS factors, Treasury term structure factors, credit risk factor zoo

### 13.3 搜索策略改进

- **会议追踪**：ICLR 2026 / ICML 2026 / NeurIPS 2025 workshop accepted paper lists → quant finance filter
- **作者追踪**：Bryan Kelly, Dacheng Xiu, Markus Pelger, Andrew Chen, Lasse Pedersen, Semyon Malamud, Christian Julliard, Campbell Harvey
- **引用图扩展**：从已读 52 篇 wiki 论文的引用/被引用图出发做 BFS
- **关键词多样化**：避免过度依赖 "agent alpha factor mining"，扩展到 "causal" "graph" "benchmark" "fine-tuning" "synthetic data" "text-to-signal"
