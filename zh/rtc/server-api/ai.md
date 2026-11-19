---
title: "会议纪要"
description: "按语音识别场次生成与获取会议纪要（大模型生成，Markdown）；识别的启停与场次列表见「语音转写」"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 rtc-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 获取会议纪要

`POST /server/v1/ai/summary/get`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

获取一场语音识别的会议纪要（Markdown）。

+ 应用开启自动纪要时，场次结束后自动生成；也可以调「生成会议纪要」手动生成
+ 生成是异步的，status 为 0/1 时稍后再取；完成或最终失败时频道内会收到自定义消息 ai_summary_ready
+ 大模型由平台运营方在后台配置，未配置时纪要不会生成

**请求参数**

<ParamField body="session_id" type="string" required>
  识别场次ID，来自启动语音识别的返回或场次列表
</ParamField>


请求示例：

```json
{
  "session_id": ""
}
```

**响应参数**

<ResponseField name="summary_id" type="string">
  纪要ID
</ResponseField>

<ResponseField name="session_id" type="string">
  识别场次ID
</ResponseField>

<ResponseField name="channel" type="string">
  频道名
  示例：`fire`
</ResponseField>

<ResponseField name="template_id" type="string">
  生成所用模板ID
</ResponseField>

<ResponseField name="status" type="integer">
  纪要状态 0排队,1生成中,2完成,3失败
</ResponseField>

<ResponseField name="content" type="string">
  纪要正文，Markdown 格式；重新生成失败时保留上一次成功的内容
</ResponseField>

<ResponseField name="model" type="string">
  生成所用的模型名
</ResponseField>

<ResponseField name="prompt_tokens" type="integer">
  输入 token 数
</ResponseField>

<ResponseField name="completion_tokens" type="integer">
  输出 token 数
</ResponseField>

<ResponseField name="error" type="string">
  失败原因(仅失败时)
</ResponseField>

<ResponseField name="finished_at" type="integer">
  最近一次生成结束时间，秒级时间戳
</ResponseField>

<ResponseField name="created_at" type="integer">
  创建时间，秒级时间戳
</ResponseField>

<ResponseField name="updated_at" type="integer">
  最后变更时间，秒级时间戳
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "channel": "fire",
    "completion_tokens": 0,
    "content": "",
    "created_at": 0,
    "error": "",
    "finished_at": 0,
    "model": "",
    "prompt_tokens": 0,
    "session_id": "",
    "status": 0,
    "summary_id": "",
    "template_id": "",
    "updated_at": 0
  }
}
```

---

## 生成会议纪要

`POST /server/v1/ai/summary/generate`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

为一场语音识别（重新）生成会议纪要，异步执行，立即返回排队中的纪要。

+ 可换模板重新生成；新结果出来前，上一次成功的纪要正文仍保留
+ 同一场次正在生成时再次调用会报错，等完成后再调
+ 完成或最终失败时频道内会收到自定义消息 ai_summary_ready，也可轮询「获取会议纪要」

**请求参数**

<ParamField body="session_id" type="string" required>
  识别场次ID
</ParamField>

<ParamField body="template_id" type="string">
  纪要模板ID，不传按应用设置的模板，应用未设置则用默认模板
</ParamField>


请求示例：

```json
{
  "session_id": "",
  "template_id": ""
}
```

**响应参数**

<ResponseField name="summary_id" type="string">
  纪要ID
</ResponseField>

<ResponseField name="session_id" type="string">
  识别场次ID
</ResponseField>

<ResponseField name="channel" type="string">
  频道名
  示例：`fire`
</ResponseField>

<ResponseField name="template_id" type="string">
  生成所用模板ID
</ResponseField>

<ResponseField name="status" type="integer">
  纪要状态 0排队,1生成中,2完成,3失败
</ResponseField>

<ResponseField name="content" type="string">
  纪要正文，Markdown 格式；重新生成失败时保留上一次成功的内容
</ResponseField>

<ResponseField name="model" type="string">
  生成所用的模型名
</ResponseField>

<ResponseField name="prompt_tokens" type="integer">
  输入 token 数
</ResponseField>

<ResponseField name="completion_tokens" type="integer">
  输出 token 数
</ResponseField>

<ResponseField name="error" type="string">
  失败原因(仅失败时)
</ResponseField>

<ResponseField name="finished_at" type="integer">
  最近一次生成结束时间，秒级时间戳
</ResponseField>

<ResponseField name="created_at" type="integer">
  创建时间，秒级时间戳
</ResponseField>

<ResponseField name="updated_at" type="integer">
  最后变更时间，秒级时间戳
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "channel": "fire",
    "completion_tokens": 0,
    "content": "",
    "created_at": 0,
    "error": "",
    "finished_at": 0,
    "model": "",
    "prompt_tokens": 0,
    "session_id": "",
    "status": 0,
    "summary_id": "",
    "template_id": "",
    "updated_at": 0
  }
}
```

---

