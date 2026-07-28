---
title: "IM 消息"
description: "会议外的即时消息与设备在线管理"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 获取IM令牌

`POST /server/v1/im/grant`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| uid | string | 是 | 第三方用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）（最大长度 100） |
| net | string | 否 | 线路 |
| sg | string | 否 | 服务分组 |

请求示例：

```json
{
  "net": "",
  "sg": "",
  "uid": ""
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data.sid | string |  |
| data.token | string |  |

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

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| action | string | 是 | 消息命令 |
| content | any | 否 | 消息体 |
| uid | string | 否 | 发送者用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -） |
| sid | string | 否 | 发送者会话ID |
| name | string | 否 | 发送者名称 |
| ruids | array | 否 | 接收者用户ID列表(当Rsids有数据时,忽略此字段) |
| rsids | array | 否 | 接收者SessionID列表 |
| important | boolean | 否 | 是否重要，重要消息在断线重连后会重发确保收到 |

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

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| uid | string | 否 | 操作者用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -） |
| ruids | array | 否 | 被踢者用户ID列表(当Rsids有数据时,忽略此字段) |
| rsids | array | 否 | 被踢者SessionID列表 |

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

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| uids | array | 是 | 用户ID列表 |

请求示例：

```json
{
  "uids": [
    ""
  ]
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |

响应示例：

```json
{
  "code": 0,
  "data": {}
}
```

---

