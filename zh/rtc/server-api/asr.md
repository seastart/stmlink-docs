---
title: "语音转写"
description: "ASR 语音识别的启停与结果回调"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 启动语音识别

`POST /server/v1/asr/start`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

对频道启动实时语音识别，把会中的说话内容转写成文字，用于会议纪要、字幕、检索。

+ 同一频道重复调用不会重复启动
+ 识别的是频道内所有开麦成员的音频，结果里带 uid 与 name 标明说话人
+ 转写结果通过「语音识别句子列表」按频道查询

启动后会持续产生费用，频道销毁时自动停止；也可以用「停止语音识别」提前结束。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名
  示例：`fire`
</ParamField>


请求示例：

```json
{
  "channel": "fire"
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

## 停止语音识别

`POST /server/v1/asr/stop`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

停止频道的语音识别。已产生的转写结果不会被删除，仍可用「语音识别句子列表」查询。

频道销毁时会自动停止，不必先手动调用。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名
  示例：`fire`
</ParamField>


请求示例：

```json
{
  "channel": "fire"
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

## 语音识别句子列表

`POST /server/v1/asr/list-sentence`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

分页查询频道的语音转写结果，每条是一句话，带说话人与时间。

+ 按 created_at 顺序取即可还原完整对话，是生成会议纪要的数据源
+ 频道销毁后结果仍然保留，可事后查询

一句话的切分由识别引擎按语音停顿决定，不保证与"一个完整语义单元"对应 ——
做纪要摘要时建议把连续多句合并后再交给模型处理。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名
  示例：`fire`
</ParamField>

<ParamField body="sort" type="string">
  排序
</ParamField>

<ParamField body="search" type="array<string>">
  通用搜索，可按转写内容检索
</ParamField>

<ParamField body="page" type="integer">
  页数，从1开始
  示例：`1`
</ParamField>

<ParamField body="per-page" type="integer">
  每页数据量
  示例：`10`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "page": 1,
  "per-page": 10,
  "search": [
    ""
  ],
  "sort": ""
}
```

**响应参数**

<ResponseField name="channel" type="string">
  频道名
  示例：`fire`
</ResponseField>

<ResponseField name="uid" type="string">
  说话人的用户ID
  示例：`1001`
</ResponseField>

<ResponseField name="name" type="string">
  说话人的会中昵称
  示例：`张三`
</ResponseField>

<ResponseField name="sentence" type="string">
  转写出的一句话文本
  示例：`我们下周把这个方案定下来`
</ResponseField>

<ResponseField name="created_at" type="integer">
  该句话的产生时间，秒级时间戳
  示例：`1718250918`
</ResponseField>


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
      "channel": "fire",
      "created_at": 1718250918,
      "name": "张三",
      "sentence": "我们下周把这个方案定下来",
      "uid": "1001"
    }
  ]
}
```

---

