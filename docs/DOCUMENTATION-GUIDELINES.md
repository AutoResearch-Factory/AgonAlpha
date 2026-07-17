# 文档组织、索引与可发现性原则

## 目标

文档以 [`docs/INDEX.md`](INDEX.md) 为统一入口。一个不了解项目的新同事或 Agent，应当能从该入口快速知道有哪些资料，并通过尽可能少的索引跳转找到需要阅读的文件。

本原则适用于 `docs/**` 中面向人或 Agent 使用的文档。图片、原始下载文件和明确的整理辅助文件采用下文所列的例外规则。

## 强制规则

### 1. 统一入口与 INDEX 连通性

- `docs/INDEX.md` 是最外层且唯一的起点。
- 每个适用文件都必须被 `docs/INDEX.md` 或由它连接的下级 `INDEX.md` **明确链接且只登记一次**；仅链接目录不能替代文件级索引。
- 每个下级 `INDEX.md` 自身也必须能从 `docs/INDEX.md` 找到。
- 同一 section 中只要存在下级 `INDEX.md`，它的链接就必须放在该 section 的最开始；该 section 的普通文件统一由下级 `INDEX.md` 登记，不在根索引重复列出。
- 不允许存在从最外层索引出发找不到的适用文件，即“孤儿文件”。
- 承担目录导航功能的 Markdown 应命名为 `INDEX.md`，使其用途一目了然。

### 2. 每个 INDEX 条目必须有一句话描述

- 每个文件在 INDEX 中的条目都必须包含链接、文件名或标题，以及紧随其后的一句话 description；不能只列名字。
- description 只应客观说明文件是什么以及实际包含什么，可以注明内容范围、条目数量、数据结构或来源，不能只是换一种说法重复标题。
- description 不得包含阅读顺序、使用方法、操作建议、推荐场景或“适合……”“用于……”之类的指导性表述。
- 列表条目可以使用 `- [标题](path) - description` 格式；表格条目必须有单独的 `Description` 列。
- description 应简洁、具体，并足以让不了解该文件的人或 Agent 在不打开文件的情况下知道其主要内容。

### 3. INDEX 层级最多为 2

INDEX 层级是从 `docs/INDEX.md` 出发，为知道某文件而必须查看的最少索引数：

- 第一层：查看 `docs/INDEX.md` 就能知道的文件；`docs/INDEX.md` 自身也按第一层计。
- 第二层：还需要再查看一个由根索引链接的下级 `INDEX.md` 才能知道的文件。
- 所有适用文件都不得深于第二层。

例如，根索引直接链接 `docs/tutorials/INDEX.md`，而后者链接 `docs/tutorials/19-alpha-examples.md`；该教程的 INDEX 层级为第二层。

### 4. Folder 层级最多为 3

Folder 层级按文件相对于 `docs/` 的路径组成部分数量计算：

- 第一层：`docs/INDEX.md`
- 第二层：`docs/tutorials/INDEX.md`
- 第三层：例如 `docs/tutorials/topic/example.md`

所有适用文件都不得深于第三层。

### 5. 能浅则浅

满足内容组织清晰的前提下，应同时降低 INDEX 层级和 Folder 层级。达到上限只是合规，不代表已经达到最佳可用性。

能够通过 `INDEX.md` 的 section 和清晰文件名表达的分类，不应再增加中间目录。当前面向阅读的文件均应尽量放在 `docs/<section>/`，避免形成 `docs/<section>/<category>/`。

### 6. 避免无意重复

- 同一文件原则上只在所属的一个 INDEX 中登记。
- 对 Alpha 挖掘非常重要、需要在统一入口强调的文件，可以同时在 `docs/INDEX.md` 和所属的下级 `INDEX.md` 各登记一次，最多出现两次。
- 上述例外必须是有意的重点强调，不得由格式副本、抓取产物或随意铺开链接造成。
- 多个文件包含相同或实质相同的信息时，INDEX 只保留其中信息最完整且便于机器读取的一份。
- 文件格式本身不决定取舍；应比较实际内容、信息完整性和机器可读性。

当前明确允许在根 INDEX 和所属下级 INDEX 中重复登记的重点文件如下：

- `docs/data/fields.json`
- `docs/data/categories.json`
- `docs/factor-research/faqs.md`
- `docs/factor-research/recommended-reading.md`
- `docs/factor-research/research-papers.json`
- `docs/tutorials/alpha-examples-bronze-users.md`
- `docs/tutorials/alpha-examples-silver-users.md`

### 7. 删除与 Alpha 无关的信息

- INDEX 只收录直接服务于 Alpha 挖掘、WorldQuant 接口、数据、操作符、回测、评估和研究方法的内容。
- 下载与爬取过程中的辅助文件、调试信息、访问状态、搜索中间结果及其他无关内容不得出现在 INDEX 中。
- 此处的“删除”是指删除 INDEX 条目；除非另有明确要求，不删除实际文件。

### 8. 图片必须被正文引用

- 每个图片文件必须至少被一个 Markdown 文件引用。
- 图片不要求出现在 INDEX 中，也不参与适用文件的 INDEX 连通性和 Folder 层级检查。
- 不得保留没有正文引用的孤立图片。

## 例外与检查范围

原始下载文件和整理辅助文件不是给新同事直接阅读的资料，因此不要求 INDEX 连通，不受上述层级上限约束，也不参与适用文件的完整性检查。

原始下载文件和其他辅助内容不应出现在根 INDEX 或下级 INDEX 中。图片只需由 Markdown 正文引用，不应为了凑齐目录而在 INDEX 中单独登记。

当前排除项如下：

1. 所有图片文件，包括 `docs/tutorials/images/**`。
2. 任一路径中的 `raw/` 目录；当前为 `docs/tutorials/raw/**`。
3. 下载清单及抓取诊断：
   - `docs/manifest.json`
   - `docs/api/official-api-search.json`
   - `docs/api/official-page-status.json`
4. 原始下载或重复格式副本：
   - `docs/data/datasets.json`
   - `docs/data/fields.md`
   - `docs/data/fields.csv`
   - `docs/data/fields.jsonl`
   - `docs/syntax/operators.json`
   - `docs/factor-research/video-courses.json`
   - `docs/tutorials/catalog.json`
5. 搜索过程产物：
   - `docs/factor-research/search-catalog.json`
   - `docs/factor-research/search-results.json`

API Schema、`docs/data/fields.json`、14 个数据集详情 JSON（例如 `docs/data/analyst4.json`）、`docs/data/categories.json` 和 `docs/factor-research/research-papers.json` 有直接使用价值，当前纳入规则检查。

若文件用途发生变化，或新增其他辅助文件，应明确更新本节后再重新检查，不能仅凭扩展名临时排除。

## 合规检查

文档组织不再计算字符加权分或平均层级分。每次修改文档结构后，应逐项检查以下离散条件：

- 所有适用文件均可从 `docs/INDEX.md` 到达。
- 除明确用作重点强调的文件可在根 INDEX 和所属下级 INDEX 各登记一次外，不存在无意重复登记。
- 每个 INDEX 条目都有符合要求的一句话 description。
- 排除项没有出现在任何 INDEX 中。
- 不存在损坏的本地链接。
- INDEX 最大层级不超过 2。
- Folder 最大层级不超过 3，并遵守“能浅则浅”的原则。
- 每张图片至少被一个 Markdown 正文引用。

任一条件不满足即视为不合规；不得用其他条件的较好结果抵消。
