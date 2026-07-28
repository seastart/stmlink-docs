---
title: "语音转写"
description: "ASR 语音识别的启停与结果回调"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## ASR语音识别启停回调

`POST /server/v1/asr/start`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| AppId | string | 否 |  |
| channel | string | 是 |  |

请求示例：

```json
{
  "AppId": "",
  "channel": ""
}
```

**响应参数**

`data` 为 null

响应示例：

```json
{
  "code": 0,
  "data": null
}
```

---

## ASR语音识别推送结果

`POST /server/v1/asr/stop`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| AppId | string | 否 |  |
| channel | string | 是 |  |

请求示例：

```json
{
  "AppId": "",
  "channel": ""
}
```

**响应参数**

`data` 为 null

响应示例：

```json
{
  "code": 0,
  "data": null
}
```

---

## ASR语音识别句子列表

`POST /server/v1/asr/list-sentence`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| AppId | string | 否 |  |
| channel | string | 是 |  |
| sort | string | 否 |  |
| search | array | 否 |  |
| page | integer | 否 | 页数，从1开始 |
| per-page | integer | 否 | 每页数据量 |

请求示例：

```json
{
  "AppId": "",
  "channel": "",
  "page": 0,
  "per-page": 0,
  "search": [
    ""
  ],
  "sort": ""
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data[].channel | string |  |
| data[].uid | string |  |
| data[].name | string |  |
| data[].sentence | string | 句子 |
| data[].created_at | integer | 创建时间 |

响应示例：

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "channel": "",
      "created_at": 0,
      "name": "",
      "sentence": "",
      "uid": ""
    }
  ]
}
```

---

