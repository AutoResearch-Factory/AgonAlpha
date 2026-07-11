# WorldQuant BRAIN API 使用手册

本文记录如何不用浏览器, 通过 Python 调用 WorldQuant BRAIN API.
BRAIN API 并不是公开, 稳定版本的通用 API, 接口和权限都可能变化, 应以官方文档为准.

## 接口总览

| 方法 | 路径 | 说明 | 成功状态 |
|---|---|---|---|
| `POST` | `/authentication` | 创建认证会话 | `201` |
| `GET` | `/operators` | 获取操作符列表 | `200` |
| `GET` | `/data-fields` | 获取或搜索数据字段 | `200` |
| `OPTIONS` | `/simulations` | 获取回测参数定义和可选值 | `200` |
| `POST` | `/simulations` | 创建回测 | `201` |
| `GET` | `/simulations/<simulation_id>` | 查询回测状态 | `200` |
| `DELETE` | `/simulations/<simulation_id>` | 取消回测 | `204` |
| `GET` | `/users/self/alphas` | 获取 Alpha 列表 | `200` |
| `GET` | `/alphas/<alpha_id>` | 获取 Alpha 详情 | `200` |
| `GET` | `/alphas/<alpha_id>/check` | 获取提交检查 | `200` |
| `GET` | `/alphas/<alpha_id>/correlations/self` | 获取自相关结果 | `200` |
| `POST` | `/alphas/<alpha_id>/submit` | 提交 Alpha | - |

## 基础地址

基础地址: `https://api.worldquantbrain.com`. 除非另有说明, 请求体和响应体均使用 JSON.

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

### 获取提交检查

请求: `GET /alphas/<alpha_id>/check` | 成功响应: `HTTP 200 OK`

响应体: `{"is": {"checks": [{"name": "<name>", "result": "<result>", "limit": <value>, "value": <value>}]}}`

### 获取自相关结果

请求: `GET /alphas/<alpha_id>/correlations/self` | 成功响应: `HTTP 200 OK`

首次请求可能只返回 `Retry-After`. 计算完成后响应包含 `schema`, `records`, `min`, `max`. `records` 中的主要字段为 `id`, `correlation`, `sharpe`, `returns`, `turnover`, `fitness`, `margin`.

### 提交 Alpha

请求: `POST /alphas/<alpha_id>/submit`

请求体为空. 提交前先读取 `/alphas/<alpha_id>/check` 并确认各项检查结果.
