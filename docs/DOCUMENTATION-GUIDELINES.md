# 文档组织、索引与可发现性原则

## 目标

文档以 [`docs/INDEX.md`](INDEX.md) 为统一入口。一个不了解项目的新同事或 Agent，应当能从该入口快速知道有哪些资料，并通过尽可能少的索引跳转找到需要阅读的文件。

本原则适用于 `docs/**` 中面向人或 Agent 使用的文档。图片、原始下载文件和明确的整理辅助文件采用下文所列的例外规则。

## 强制规则

### 1. 统一入口与 INDEX 连通性

- `docs/INDEX.md` 是最外层且唯一的起点。
- 每个适用文件都必须被 `docs/INDEX.md` 或由它连接的下级 `INDEX.md` **明确链接**；仅链接目录不能替代文件级索引。
- 每个下级 `INDEX.md` 自身也必须能从 `docs/INDEX.md` 找到。
- 同一 section 中只要存在下级 `INDEX.md`，它的链接就必须放在该 section 的最开始，先提供导航入口，再列普通文件。
- 下级 `INDEX.md` 必须是其 section 的完整目录，而不是仅记录根索引尚未列出的增量内容；属于该 section 的文件即使已经在 `docs/INDEX.md` 中出现，也必须在下级 `INDEX.md` 中再次列出。
- 为了降低 INDEX 层级，重要文件可以同时出现在根索引和所属 section 的下级索引中；这种有意的重复是允许且推荐的。
- 不允许存在从最外层索引出发找不到的适用文件，即“孤儿文件”。
- 承担目录导航功能的 Markdown 应命名为 `INDEX.md`，使其用途一目了然。

### 2. INDEX 层级最多为 2

INDEX 层级是从 `docs/INDEX.md` 出发，为知道某文件而必须查看的最少索引数：

- 第一层：查看 `docs/INDEX.md` 就能知道的文件；`docs/INDEX.md` 自身也按第一层计。
- 第二层：还需要再查看一个由根索引链接的下级 `INDEX.md` 才能知道的文件。
- 所有适用文件都不得深于第二层。

例如，根索引直接链接 `docs/tutorials/INDEX.md`，而后者链接 `docs/tutorials/19-alpha-examples.md`；该教程的 INDEX 层级为第二层。

### 3. Folder 层级最多为 3

Folder 层级按文件相对于 `docs/` 的路径组成部分数量计算：

- 第一层：`docs/INDEX.md`
- 第二层：`docs/tutorials/INDEX.md`
- 第三层：例如 `docs/tutorials/topic/example.md`

所有适用文件都不得深于第三层。

### 4. 能浅则浅

满足内容组织清晰的前提下，应同时降低 INDEX 层级和 Folder 层级。达到上限只是合规，不代表已经达到最佳可用性。

能够通过 `INDEX.md` 的 section 和清晰文件名表达的分类，不应再增加中间目录。当前面向阅读的文件均应尽量放在 `docs/<section>/`，避免形成 `docs/<section>/<category>/`。

### 5. 图片必须被正文引用

- 每个图片文件必须至少被一个 Markdown 文件引用。
- 图片不要求出现在 INDEX 中，也不参与 INDEX 层级、Folder 层级和平均分计算。
- 不得保留没有正文引用的孤立图片。

## 例外与当前计分范围

原始下载文件和整理辅助文件不是给新同事直接阅读的资料，因此不要求 INDEX 连通，不受上述层级上限约束，也不参与平均分的分子或分母。

为了让 section 的非图片资产清单完整，下级 `INDEX.md` 仍应登记原始下载文件和其他辅助内容。图片只需由 Markdown 正文引用，不应为了凑齐目录而在 INDEX 中单独登记。

当前排除项如下：

1. 所有图片文件，包括 `docs/tutorials/images/**`。
2. 任一路径中的 `raw/` 目录；当前为 `docs/tutorials/raw/**`。
3. 下载清单及抓取诊断：
   - `docs/manifest.json`
   - `docs/api/official-api-search.json`
   - `docs/api/official-page-status.json`
4. 原始下载或机器可读副本：
   - `docs/data/datasets.json`
   - `docs/data/fields.csv`
   - `docs/data/fields.json`
   - `docs/data/fields.jsonl`
   - `docs/syntax/operators.json`
   - `docs/factor-research/video-courses.json`
   - `docs/tutorials/catalog.json`
5. 搜索过程产物：
   - `docs/factor-research/search-catalog.json`
   - `docs/factor-research/search-results.json`

API Schema、14 个数据集详情 JSON（例如 `docs/data/analyst4.json`）、`docs/data/categories.json` 和 `docs/factor-research/research-papers.json` 有直接使用价值，当前纳入规则检查和计分。

若文件用途发生变化，或新增其他辅助文件，应明确更新本节后再重新计算，不能仅凭扩展名临时排除。

## 平均分

### 出发点

假设新同事或 Agent 每多进入一层，继续查找并实际使用该文件的可能性都会减半。层级越浅，文件越可能被发现和使用。

### 单文件得分

层级为 `L` 的文件得分为：

```text
score(L) = 0.5 ** (L - 1)
```

因此第一层为 `1`，第二层为 `0.5`，第三层为 `0.25`，依此类推。

### 按字符数加权

设文件 `i` 的 UTF-8 文本解码后字符数为 `c_i`，层级为 `L_i`，则平均分为：

```text
average_score = Σ(c_i × 0.5 ** (L_i - 1)) / Σ(c_i)
```

- 字符数按 Unicode 字符数计算，包含空白和换行，不按文件字节数计算。
- INDEX 平均分使用 INDEX 层级作为 `L_i`。
- Folder 平均分使用 Folder 层级作为 `L_i`。
- 所有适用文件，包括各级 `INDEX.md` 和本文档，都参与计算。
- INDEX 不可达的适用文件仍保留在分母中，单文件得分按 `0` 计算，避免通过漏建索引虚增平均分。
- 排除项完全不进入分子和分母。
- 中间计算不提前舍入，最终平均分四舍五入保留小数点后两位。

平均分的理论最高值为 **1**，表示所有计分内容都处于第一层。分数越接近 1，整体内容越容易被发现。

## 当前结果

统计范围：`docs/**`；统计日期：2026-07-12。结果已包含本文档、索引整理和面向阅读文件的目录扁平化。

| 指标 | 当前值 | 理想值 |
|---|---:|---:|
| 纳入计分的文件数 | 117 | — |
| 纳入计分的总字符数 | 2,315,925 | — |
| INDEX 层级平均分 | 0.90 | 1 |
| Folder 层级平均分 | 0.50 | 1 |

层级分布：

| 维度 | 第一层 | 第二层 | 第三层 | 不可达或更深 |
|---|---:|---:|---:|---:|
| INDEX 文件数 | 16 | 101 | 不适用 | 0 |
| INDEX 字符数 | 1,847,933 | 467,992 | 不适用 | 0 |
| Folder 文件数 | 2 | 115 | 0 | 0 |
| Folder 字符数 | 5,001 | 2,310,924 | 0 | 0 |

当前完整性检查：

- INDEX 可达的适用文件：117 / 117。
- 图片被 Markdown 引用：64 / 64。
- INDEX 最大层级：2。
- Folder 最大层级：2。
