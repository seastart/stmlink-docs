---
title: "语音转写"
description: "ASR 语音识别的启停与结果回调"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 rtc-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 启动语音识别

`POST /server/v1/asr/start`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

对频道启动实时语音识别，把会中的说话内容转写成文字，用于会议纪要、字幕、检索。

+ 同一频道重复调用不会重复启动，返回的仍是进行中的那一场
+ 识别的是频道内所有开麦成员的音频，结果里带 uid 与 name 标明说话人
+ 每次启动到停止（或频道销毁）是一个识别场次，转写结果与会议纪要都按场次归档
+ 转写结果通过「语音识别句子列表」按场次或频道查询

启动后会持续产生费用，频道销毁时自动停止；也可以用「停止语音识别」提前结束。
应用开启了自动纪要时，场次结束后会生成会议纪要，完成后发频道消息 ai_summary_ready；
传了 translate_lang（或应用开启了实时翻译）时，每句定稿后的译文通过频道消息 asr_trans 下发。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名
  示例：`fire`
</ParamField>

<ParamField body="translate_lang" type="string">
  实时翻译目标语言，传了则本场每句定稿后自动翻译，译文通过频道消息 asr_trans 下发；不传按应用设置（最大长度 16）
  示例：`en`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "translate_lang": "en"
}
```

**响应参数**

<ResponseField name="session_id" type="string">
  识别场次ID，查句子、取会议纪要都用它
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "session_id": ""
  }
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

## 语音识别场次列表

`POST /server/v1/asr/list-session`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

分页查询应用的语音识别场次，每次启动到停止（或频道销毁）为一场，带会议纪要状态。

频道名会被复用（同一个会议室天天开会），按场次区分每一场会议的转写与纪要。

**请求参数**

<ParamField body="channel" type="string">
  频道名，不传表示全部频道（最大长度 100）
  示例：`fire`
</ParamField>

<ParamField body="begin_at" type="integer">
  起始时间（按场次开始时间过滤），秒级时间戳，0 表示不限
</ParamField>

<ParamField body="end_at" type="integer">
  截止时间，秒级时间戳，0 表示不限
</ParamField>

<ParamField body="sort" type="string">
  排序，默认按开始时间倒序（可排序字段：started_at、sentence_count）
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
  "begin_at": 0,
  "channel": "fire",
  "end_at": 0,
  "page": 1,
  "per-page": 10,
  "sort": ""
}
```

**响应参数**

<ResponseField name="session_id" type="string">
  识别场次ID
</ResponseField>

<ResponseField name="channel" type="string">
  频道名
  示例：`fire`
</ResponseField>

<ResponseField name="started_at" type="integer">
  识别开始时间，秒级时间戳
  示例：`1718250918`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  识别结束时间，秒级时间戳，0 表示识别中
</ResponseField>

<ResponseField name="status" type="integer">
  场次状态 1识别中,2已结束
</ResponseField>

<ResponseField name="sentence_count" type="integer">
  已转写的句子数
</ResponseField>

<ResponseField name="summary_status" type="integer">
  纪要状态 -1未生成,0排队,1生成中,2完成,3失败
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
      "ended_at": 0,
      "sentence_count": 0,
      "session_id": "",
      "started_at": 1718250918,
      "status": 0,
      "summary_status": 0
    }
  ]
}
```

---

## 语音识别句子列表

`POST /server/v1/asr/list-sentence`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

分页查询频道的语音转写结果，每条是一句话，带说话人与时间。

+ 按 created_at 顺序取即可还原完整对话，是生成会议纪要的数据源
+ 传 session_id 只取某一场识别的句子，begin_ms / end_ms 是句子相对该场开始的毫秒，可直接做字幕时间轴
+ 频道销毁后结果仍然保留，可事后查询

一句话的切分由识别引擎按语音停顿决定，不保证与"一个完整语义单元"对应 ——
做纪要摘要时建议把连续多句合并后再交给模型处理。

**请求参数**

<ParamField body="channel" type="string">
  频道名，不传 session_id 时必填
  示例：`fire`
</ParamField>

<ParamField body="session_id" type="string">
  识别场次ID，传了只返回该场次的句子
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
  "session_id": "",
  "sort": ""
}
```

**响应参数**

<ResponseField name="sentence_id" type="string">
  句子ID，与频道消息 asr_trans 里的 sentence_id 对应
</ResponseField>

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

<ResponseField name="session_id" type="string">
  所属识别场次ID，早期数据为空
</ResponseField>

<ResponseField name="begin_ms" type="integer">
  句首时刻，相对场次开始的毫秒
  示例：`65200`
</ResponseField>

<ResponseField name="end_ms" type="integer">
  句尾时刻，相对场次开始的毫秒
  示例：`68900`
</ResponseField>

<ResponseField name="trans_text" type="string">
  译文，未开启翻译时为空
</ResponseField>

<ResponseField name="trans_lang" type="string">
  译文语言，如 en
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
      "begin_ms": 65200,
      "channel": "fire",
      "created_at": 1718250918,
      "end_ms": 68900,
      "name": "张三",
      "sentence": "我们下周把这个方案定下来",
      "sentence_id": "",
      "session_id": "",
      "trans_lang": "",
      "trans_text": "",
      "uid": "1001"
    }
  ]
}
```

---

