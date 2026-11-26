---
title: "同声传译"
description: "会中同声传译的开关与成员语言：每句定稿后翻译成在会成员的语言并合成语音，随频道消息 asr_trans 下发；依附在「语音转写」上"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 rtc-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 开启同声传译

`POST /server/v1/interp/start`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

开启频道的同声传译：每句话定稿后翻译成在会成员的各种语言、合成语音，通过频道消息 asr_trans 下发（带 audio_url）。

+ 依附在语音识别上：频道还没开语音识别时会自动开启，返回的 session_id 与「启动语音识别」一致
+ 成员用「设置同传语言」设自己的语言，没设的按中文；每句只翻译成「在会成员的语言 − 说话人的语言」
+ 开启后发频道消息 interp_enabled（enabled=true，duck_volume 为播译音时说话人原声的音量），频道属性 props 里的
interp_enabled / interp_duck_volume 同步更新，后入会的成员从频道属性取当前状态
+ 重复调用幂等，可用于会中更换 AI 方案；停止语音识别时同传随之关闭

需要应用的 AI 方案配了大模型，否则报「大模型未配置或未启用」；方案没配语音合成时只下发译文、没有 audio_url。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名
  示例：`fire`
</ParamField>

<ParamField body="profile" type="string">
  AI 方案名（运营后台「AI 服务与方案」里配置），不传按应用 AI 设置的方案，再没有用默认方案（最大长度 64）
  示例：`default`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "profile": "default"
}
```

**响应参数**

<ResponseField name="session_id" type="string">
  识别场次ID（同传依附在转写场次上）
</ResponseField>

<ResponseField name="duck_volume" type="number">
  播译音时说话人原声压到的音量（0~1，0=静音），来自 AI 方案
  示例：`0.2`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "duck_volume": 0.2,
    "session_id": ""
  }
}
```

---

## 关闭同声传译

`POST /server/v1/interp/stop`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

关闭频道的同声传译，语音识别照常进行（译文回到按应用设置的单语言实时翻译）。没开启时也返回成功。

关闭后发频道消息 interp_enabled（enabled=false）。

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

## 设置成员的同传语言

`POST /server/v1/interp/set-lang`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

设置成员的同传语言（「我的语言」）：决定他说话时用哪种语言识别，以及别人的话要翻译成哪种语言给他听。

+ 频道开启后即可设置，同传没开也会记住，开启时生效；频道销毁后清除
+ 设置后发频道消息 interp_lang（uid、lang），各端据此判断播不播某条译音
+ 正在识别时立即切换该成员的识别语言，切换前说的最后一句照常输出
+ 中英夹杂说话的成员建议设中文

**请求参数**

<ParamField body="channel" type="string" required>
  频道名
  示例：`fire`
</ParamField>

<ParamField body="uid" type="string" required>
  成员的用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>

<ParamField body="lang" type="string">
  语言码（zh / en 等，zh-CN 这类带地区的按 zh 处理），空=恢复默认语言（最大长度 16）
  示例：`en`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "lang": "en",
  "uid": "1001"
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

## 查询频道同传状态与成员语言

`POST /server/v1/interp/langs`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

查询频道的同传状态与成员语言表，入会时取一次全量，之后按频道消息 interp_enabled / interp_lang 增量更新。

langs 只含设过语言的成员，没设的按 default_lang。

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

<ResponseField name="enabled" type="boolean">
  同声传译是否开启
</ResponseField>

<ResponseField name="duck_volume" type="number">
  播译音时说话人原声压到的音量（0~1），未开启时为 0
</ResponseField>

<ResponseField name="default_lang" type="string">
  没设语言的成员按此语言算
  示例：`zh`
</ResponseField>

<ResponseField name="langs" type="object">
  设过语言的成员：uid → 语言
  示例：`{"1001":"en"}`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "default_lang": "zh",
    "duck_volume": 0,
    "enabled": false,
    "langs": {
      "1001": "en"
    }
  }
}
```

---

