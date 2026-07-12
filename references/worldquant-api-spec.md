# WorldQuant BRAIN API 使用手册

本文记录如何不用浏览器, 通过 Python 调用 WorldQuant BRAIN API.
BRAIN API 并不是公开, 稳定版本的通用 API, 接口和权限都可能变化, 应以官方文档为准.

## 基础地址

基础地址: `https://api.worldquantbrain.com`. 除非另有说明, 请求体和响应体均使用 JSON.

## 已验证接口

下表仅列出本文已经验证的接口, 不代表 BRAIN API 的完整路由集合.

| 路径 | 方法 | 说明 | 成功状态 | `${CLAUDE_PLUGIN_ROOT}/scripts/brain_client.py` 如何使用 |
|---|---|---|---|---|
| `/authentication` | `POST` | 创建认证会话 | `201` | 运行 `simulate` 时自动认证 |
| `/operators` | `GET` | 获取操作符列表 | `200` | |
| `/data-fields` | `GET` | 获取或搜索数据字段 | `200` | |
| `/simulations` | `OPTIONS` | 获取回测参数定义和可选值 | `200` | |
| `/simulations` | `POST` | 创建回测 | `201` | `simulate` 为每个尚未创建的候选提交回测 |
| `/simulations/<simulation_id>` | `GET` | 查询回测状态 | `200` | `simulate` 自动轮询至获得 Alpha ID 或失败 |
| `/simulations/<simulation_id>` | `DELETE` | 取消回测 | `204` | |
| `/alphas/<alpha_id>` | `GET` | 获取 Alpha 详情 | `200` | `simulate` 在回测完成后自动核验 Alpha |
| `/alphas/<alpha_id>/recordsets` | `GET` | 获取可用统计集 | `200` | |
| `/alphas/<alpha_id>/recordsets/yearly-stats` | `GET` | 获取按年统计 | `200` | |
| `/alphas/<alpha_id>/recordsets/daily-pnl` | `GET` | 获取每日 PnL | `200` | |
| `/alphas/<alpha_id>/check` | `GET` | 获取提交检查 | `200` | |
| `/alphas/<alpha_id>/correlations/self` | `GET` | 获取自相关结果 | `200` | |
| `/alphas/<alpha_id>` | `OPTIONS` | 获取 Alpha 属性定义 | `200` | |
| `/alphas/<alpha_id>` | `PATCH` | 更新 Alpha 属性 | `200` | `simulate` 会为通过核验的 Alpha 设置候选名称 |
| `/alphas/<alpha_id>/submit` | `POST` | 提交 Alpha | - | |
| `/users/self/alphas` | `GET` | 获取 Alpha 列表 | `200` | |

## 项目客户端：`${CLAUDE_PLUGIN_ROOT}/scripts/brain_client.py`

这是本项目用于批量创建并轮询 BRAIN simulation 的命令行客户端；它只覆盖高频使用场景（目前是回测），其他功能还需要你自己完成。

### 准备凭据和候选文件

默认从 `alphas/.env` 读取凭据。文件必须包含 `BRAIN_EMAIL` 和 `BRAIN_PASSWORD`；支持 `export KEY=value` 及带引号的值。可通过 `--env` 使用其他文件。

候选文件可以是 JSON 数组，或包含 `candidates` 数组的 JSON 对象。每个候选必须有 `name`、`settings` 与 `regular`（也接受 `expression`）。`name` 同时用作 artifact 目录名和 Alpha 名称，格式必须为 `{CANDIDATE_ID}-{LOOP_ID}-{SLUG}`：`CANDIDATE_ID` 是 run-dir 的末级目录名，`LOOP_ID` 从 1 开始递增，`SLUG` 是唯一、简洁的小写 kebab-case 描述。不要传 `slug` 或 `id`。客户端拒绝格式错误或重复的名称，以及重复 simulation payload。

```json
{
  "candidates": [
    {
      "name": "0001-1-usa-reversal-v1",
      "settings": {
        "instrumentType": "EQUITY",
        "region": "USA",
        "universe": "TOP3000",
        "delay": 1
      },
      "regular": "rank(reverse(returns))"
    }
  ]
}
```

### 运行

在 run-dir 运行：

```bash
cd <run-dir>
python ${CLAUDE_PLUGIN_ROOT}/scripts/brain_client.py --env ${CLAUDE_PLUGIN_ROOT}/alphas/.env simulate candidates.json \
  --run-dir . \
  --max-active 4 \
  --max-runtime 540
```

- `--run-dir` 必须解析为当前工作目录；先 `cd <run-dir>` 再传入 `--run-dir .`，避免命令写入其他目录。
- `--max-active` 默认 `4`，表示同时处于 BRAIN server-side simulation 中的最大候选数。
- `--max-runtime` 默认 `540` 秒，只限制本地调度进程的本次运行时间。
- simulation 创建后立即轮询一次。未完成时，下一次轮询等待 `max(Retry-After, 30 秒)`；服务端未提供 `Retry-After` 时同样等待 30 秒。

### Artifact 与恢复

每个候选写入 `<run-dir>/<name>/`。主要文件为 `candidate.json`、`payload.json`、`creation.json`、`status-latest.json`、`alpha-before-name.json`、`name-response.json`、`alpha.json`、`result.json` 或 `error.json`；批次汇总写入 `<run-dir>/summary.json`。JSON 写入先落在同目录的 `*.json.tmp`，再原子替换；凭据不会写入 artifact。

`max-runtime` 到期时，命令先写入 `summary.json` 再结束。本次已创建的 BRAIN simulation 不会被取消：用相同候选文件和同一 `--run-dir` 重跑，即会从 `creation.json` 中保存的 Location 继续轮询；已有 `result.json` 会复用，尚未创建的候选继续排队。已有 `error.json` 的候选视为终态失败，不自动重新提交。

完成 simulation 后，客户端会获取 Alpha 并核对 ID、表达式和 settings；同一批中同一 Alpha 只能被一个候选认领。只有确认返回 Alpha 不早于本次 simulation 请求且没有不同的现有名称时，客户端才会 `PATCH` 设置候选名称。

## 认证

### 创建会话

请求: `POST /authentication` | 认证头: `Authorization: Basic <base64(email:password)>` | 成功响应: `HTTP 201 Created`

响应会设置会话 Cookie. 后续请求必须携带该 Cookie.

## 操作符

### 获取操作符列表

请求: `GET /operators` | 成功响应: `HTTP 200 OK`

每个操作符包含 `name`, `category`, `scope`, `level`, `definition`, `description`, `documentation`.

## 数据字段

### 获取或搜索数据字段

请求: `GET /data-fields` | 成功响应: `HTTP 200 OK`

查询参数:

| 参数 | 类型 | 可选值或格式 |
|---|---|---|
| `instrumentType` | string | `EQUITY` |
| `region` | string | `USA` |
| `universe` | string | `TOP3000`, `TOP2000`, `TOP1000`, `TOP500`, `TOP200`, `TOPSP500` |
| `delay` | integer | `1` |
| `dataset.id` | string | 数据集 ID |
| `search` | string | 任意搜索字符串 |
| `limit` | integer | 正整数 |
| `offset` | integer | 非负整数 |

响应体:

```
{
  "count": <integer>,
  "results": [
    {
      "id": "<field_id>",
      "description": "<description>",
      "type": "<field_type>"
    }
  ]
}
```

每个数据字段还可能包含 `dataset`, `category`, `subcategory`, `region`, `universe`, `delay`, `coverage`, `dateCoverage`, `alphaCount`, `userCount`.

## 回测

### 获取参数定义

请求: `OPTIONS /simulations` | 成功响应: `HTTP 200 OK`

参数定义位于 `actions.POST`. 可选值可能随服务端配置变化, 创建回测前可通过该接口刷新.

### 创建回测

请求: `POST /simulations` | 内容类型: `application/json` | 成功响应: `HTTP 201 Created`

请求体:

```
{
  "type": "REGULAR",
  "settings": {
    "instrumentType": "EQUITY",
    "region": "USA",
    "universe": "TOP3000",
    "delay": 1,
    "decay": 4,
    "neutralization": "SUBINDUSTRY",
    "truncation": 0.08,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "language": "FASTEXPR",
    "visualization": false
  },
  "regular": "<fast_expression>"
}
```

设置字段:

| 字段 | 类型 | 可选值或格式 |
|---|---|---|
| `type` | string | `REGULAR` |
| `instrumentType` | string | `EQUITY` |
| `region` | string | `USA` |
| `universe` | string | `TOP3000`, `TOP2000`, `TOP1000`, `TOP500`, `TOP200`, `TOPSP500` |
| `delay` | integer | `1` |
| `decay` | integer | 整数 |
| `neutralization` | string | `NONE`, `MARKET`, `SECTOR`, `INDUSTRY`, `SUBINDUSTRY` |
| `truncation` | number | 浮点数 |
| `pasteurization` | string | `ON`, `OFF` |
| `unitHandling` | string | `VERIFY` |
| `nanHandling` | string | `ON`, `OFF` |
| `language` | string | `FASTEXPR` |
| `visualization` | boolean | `true`, `false` |
| `testPeriod` | string | 时间段字符串, 可省略 |
| `regular` | string | Fast Expression 表达式 |

状态地址: `Location: https://api.worldquantbrain.com/simulations/<simulation_id>`

### 查询回测状态

请求: `GET /simulations/<simulation_id>`

运行中的响应: `{"progress": <number>}`
如果响应包含 `Retry-After` 头, 下次轮询应等待指定的秒数.
完成响应: `{"progress": null, "alpha": "<alpha_id>"}`
失败响应: `{"status": "ERROR", "message": "<error_message>"}`

### 取消回测

请求: `DELETE /simulations/<simulation_id>`

## Alpha

### 获取 Alpha 列表

请求: `GET /users/self/alphas?limit=<limit>&offset=<offset>` | 成功响应: `HTTP 200 OK`

响应体包含 `count`, `next`, `previous`, `results`.

### 获取 Alpha 详情

请求: `GET /alphas/<alpha_id>` | 成功响应: `HTTP 200 OK`

响应体中的 `is` 字段包含样本内回测指标:

```
{
  "id": "<alpha_id>",
  "name": <string_or_null>,
  "is": {
    "sharpe": <number>,
    "fitness": <number>,
    "returns": <number>,
    "turnover": <number>,
    "drawdown": <number>,
    "margin": <number>
  }
}
```

`settings` 包含实际采用的回测设置. `regular.code` 包含表达式. `is.checks` 包含检查结果.

### 获取可用统计集

请求: `GET /alphas/<alpha_id>/recordsets` | 成功响应: `HTTP 200 OK`

响应体包含 `count`, `next`, `previous`, `results`. `results` 中每项包含统计集的 `name` 和 `title`. 当前已验证的统计集为 `pnl`, `sharpe`, `turnover`, `daily-pnl`, `yearly-stats`.

### 获取按年统计

请求: `GET /alphas/<alpha_id>/recordsets/yearly-stats` | 成功响应: `HTTP 200 OK`

响应体包含 `schema` 和 `records`. `records` 中每条记录都是数组, 字段顺序由 `schema.properties` 定义. 当前顺序为:

`year`, `pnl`, `bookSize`, `longCount`, `shortCount`, `turnover`, `sharpe`, `returns`, `drawdown`, `margin`, `fitness`, `stage`

`turnover`, `returns`, `drawdown` 和 `margin` 返回原始小数值, 展示时分别按照 `schema.properties` 中的 `percent` 或 `permyriad` 类型换算. `stage` 表示统计周期, 例如 `IS`.

### 获取每日 PnL

请求: `GET /alphas/<alpha_id>/recordsets/daily-pnl` | 成功响应: `HTTP 200 OK`

响应体包含 `schema` 和 `records`. 当前字段顺序为 `date`, `pnl`, 每条记录表示一个交易日的 PnL. 该接口可能暂时返回空的 `HTTP 200` 和 `Retry-After`, 应等待后重试.

### 获取 Alpha 属性定义

请求: `OPTIONS /alphas/<alpha_id>` | 成功响应: `HTTP 200 OK`

可编辑属性定义位于 `actions.PUT`. 当前允许 `GET`, `PUT`, `PATCH`, `HEAD`, `OPTIONS`.

### 更新 Alpha 属性

请求: `PATCH /alphas/<alpha_id>` | 内容类型: `application/json` | 成功响应: `HTTP 200 OK`

设置名称: `{"name": "<name>"}`

`POST /simulations` 不接受 `name`. 回测创建的 Alpha 默认 `name: null`, UI 显示为 `anonymous`; 获取 `<alpha_id>` 后必须单独设置名称.

### 获取提交检查

请求: `GET /alphas/<alpha_id>/check` | 成功响应: `HTTP 200 OK`

响应体: `{"is": {"checks": [{"name": "<name>", "result": "<result>", "limit": <value>, "value": <value>}]}}`

### 获取自相关结果

请求: `GET /alphas/<alpha_id>/correlations/self` | 成功响应: `HTTP 200 OK`

首次请求可能只返回 `Retry-After`. 计算完成后响应包含 `schema`, `records`, `min`, `max`. `records` 中的主要字段为 `id`, `correlation`, `sharpe`, `returns`, `turnover`, `fitness`, `margin`.

### 提交 Alpha

请求: `POST /alphas/<alpha_id>/submit`

请求体为空. 提交前先读取 `/alphas/<alpha_id>/check` 并确认各项检查结果.
