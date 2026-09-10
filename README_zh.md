# AgonAlpha

[English](README.md) | 中文

AgonAlpha ([论文](https://arxiv.org/abs/2608.11250)) 是一个面向可复现量化 alpha 发现的 agentic 框架. 它搜索的对象是完整的科研产物 —— 假设, 可执行表达式, 评测证据, 理由和评审状态 —— 同时由一个蒙特卡洛树搜索 (MCTS) 调度器在候选谱系之间分配算力.

本仓库提供编排层. 数据, 凭证, evaluator 集成, 生成出的候选以及评测结果都留在本地, 不纳入版本控制.

## 工作方式

每条搜索流水线有两个角色:

1. **alpha proposer** 生成或改进候选, 用用户自备的本地 evaluator 评测, 并记录一份可复现的报告.
2. **alpha reviewer** 独立核查报告及其证据, 必要时重跑评测, 并给出调度器所使用的已验证 Fitness.

调度器结合了基于分位数的 reward, upper-confidence-bound 选择, progressive widening 和访问回传. 候选报告是不可变的谱系记录: 一个新候选只能看到它所选祖先路径上的报告.

## 仓库结构

```text
agents/                         proposer 和对抗性 reviewer 的 prompt
commands/alpha-mcts.md          搜索编排命令
references/project_manual.md    候选产物格式
references/dispatch_manual.md   受支持的子 agent 启动流程
references/evaluator.example.md 本地 evaluator 契约模板
scripts/mcts.py                 确定性 MCTS 调度器
scripts/tests/test_mcts.py      调度器测试
settings.example.toml           模型路由与并发配置示例
```

## 环境要求

- Python 3.10 或更新版本
- `pytest`, 用于运行测试
- 支持本地 plugin 的 Claude Code
- 至少一个按 `references/dispatch_manual.md` 配置好的 agent CLI
- 一个能返回有限数值 Fitness 的本地评测系统

## 安装

Clone 仓库并创建本地配置文件:

```bash
git clone https://github.com/AutoResearch-Factory/AgonAlpha.git
cd AgonAlpha
cp settings.example.toml settings.toml
cp references/evaluator.example.md references/evaluator.md
```

编辑 `settings.toml` 选择并发度和 agent 后端. 然后在 `references/evaluator.md` 里补全可用数据, 候选语法, 可执行的评测接口, Fitness 定义, 接受条件和授权边界. 这两个文件都被 Git 忽略.

运行调度器测试:

```bash
python -m pytest scripts/tests
```

## 用法

以 plugin 方式加载本仓库启动 Claude Code:

```bash
claude --plugin-dir .
```

在交互会话里, 请求跑完一条或多条候选流水线:

```text
/alpha-mcts 1
```

把 `1` 换成要跑完的流水线数量. 该命令会在需要时初始化 `alphas/state.json`, 保持最多 `parallelism` 条流水线同时活跃, 并把每个候选写到 `alphas/<candidate-id>/` 下. 整个 `alphas/` workspace 都被忽略, 因此表达式, 证据和结果不会被误提交.

MCTS 调度器也可以直接调用:

```bash
python scripts/mcts.py init
python scripts/mcts.py next
python scripts/mcts.py update --candidate-id 0001 --score 1.25
```

## 安全与可复现

- 凭证放在环境变量或本地密钥存储里; 绝不要把值写进 `references/evaluator.md`.
- 把原始评测输入和输出保存在候选工作目录内, 这样 reviewer 才能复现分数.
- 不要提交生成的 alpha 表达式, 专有数据集, 非公开的平台文档或评测产物.
- 除非本地 evaluator 契约里明确授权, 否则一律视对外提交, 发布和部署为禁用.

## 引用

如果 AgonAlpha 对你的研究有帮助, 请引用:

> W. Ye, Y. Sun, X. Ren, S. Yu, C. Yi, and H. Yang, “AgonAlpha: Autonomous Alpha Discovery via Prompt Economy and Scalable Agentic Search,” arXiv:2608.11250, 2026. [https://arxiv.org/abs/2608.11250](https://arxiv.org/abs/2608.11250)

```bibtex
@article{ye2026agonalpha,
  title   = {AgonAlpha: Autonomous Alpha Discovery via Prompt Economy and Scalable Agentic Search},
  author  = {Ye, Weicheng and Sun, Youran and Ren, Xingyu and Yu, Shunyao and Yi, Chugang and Yang, Haizhao},
  journal = {arXiv preprint arXiv:2608.11250},
  year    = {2026}
}
```
