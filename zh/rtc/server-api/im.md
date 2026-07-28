---
title: "IM 消息"
description: "会议外的即时消息与设备在线管理"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 获取IM令牌

`POST /server/v1/im/grant`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="uid" type="string" required>
  第三方用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）（最大长度 100）
</ParamField>

<ParamField body="net" type="string">
  线路
</ParamField>

<ParamField body="sg" type="string">
  服务分组
</ParamField>


请求示例：

```json
{
  "net": "",
  "sg": "",
  "uid": ""
}
```

**响应参数**

<ResponseField name="sid" type="string">
</ResponseField>

<ResponseField name="token" type="string">
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "sid": "",
    "token": ""
  }
}
```

---

## 发送IM消息

`POST /server/v1/im/send-msg`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="action" type="string" required>
  消息命令
</ParamField>

<ParamField body="content" type="any">
  消息体
</ParamField>

<ParamField body="uid" type="string">
  发送者用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）
</ParamField>

<ParamField body="sid" type="string">
  发送者会话ID
</ParamField>

<ParamField body="name" type="string">
  发送者名称
</ParamField>

<ParamField body="ruids" type="array<string>">
  接收者用户ID列表(当Rsids有数据时,忽略此字段)
</ParamField>

<ParamField body="rsids" type="array<string>">
  接收者SessionID列表
</ParamField>

<ParamField body="important" type="boolean">
  是否重要，重要消息在断线重连后会重发确保收到
</ParamField>


请求示例：

```json
{
  "action": "",
  "content": null,
  "important": false,
  "name": "",
  "rsids": [
    ""
  ],
  "ruids": [
    ""
  ],
  "sid": "",
  "uid": ""
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

## 强制下线IM设备

`POST /server/v1/im/kick-device`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="uid" type="string">
  操作者用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）
</ParamField>

<ParamField body="ruids" type="array<string>">
  被踢者用户ID列表(当Rsids有数据时,忽略此字段)
</ParamField>

<ParamField body="rsids" type="array<string>">
  被踢者SessionID列表
</ParamField>


请求示例：

```json
{
  "rsids": [
    ""
  ],
  "ruids": [
    ""
  ],
  "uid": ""
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

## 获取用户所有在线设备

`POST /server/v1/im/user-device-list`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="uids" type="array<string>" required>
  用户ID列表
</ParamField>


请求示例：

```json
{
  "uids": [
    ""
  ]
}
```

**响应参数**


响应示例：

```json
{
  "code": 0,
  "data": {}
}
```

---

