---
title: "IM 消息"
description: "会议外的即时消息与设备在线管理"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 获取IM令牌

`POST /server/v1/im/grant`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

获取 IM 连接凭证。IM 是频道之外的消息通道 —— 用户不在任何频道里也能收发，
适合做会议邀请通知、来电呼叫、离线提醒这类场景。

典型时序：用户登录你的业务后，业务后端调本接口拿 token → 下发给客户端 →
客户端用它连接 IM。之后就能通过「发送IM消息」推送给他，或收到他的上下线回调
（im_connect / im_disconnect）。

同一个 uid 可以在多个设备上同时连接，每个连接有独立的 sid —— 所以"给某人发消息"
和"给某台设备发消息"是两件事，见「发送IM消息」。

**请求参数**

<ParamField body="uid" type="string" required>
  第三方用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）（最大长度 100）
  示例：`1001`
</ParamField>

<ParamField body="net" type="string">
  线路，取值是中文线路名，由部署的网络配置决定；留空则由服务端选择
  示例：`内网`
</ParamField>

<ParamField body="sg" type="string">
  服务分组
</ParamField>


请求示例：

```json
{
  "net": "内网",
  "sg": "",
  "uid": "1001"
}
```

**响应参数**

<ResponseField name="sid" type="string">
  本次 IM 会话 ID，同一 uid 多端连接各有独立的 sid
</ResponseField>

<ResponseField name="token" type="string">
  IM 连接凭证，下发给客户端用于建立 IM 长连接
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

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

通过 IM 通道给指定用户或设备推消息，接收方不需要在任何频道里。

收件人二选一：ruids 按用户发，该用户所有在线设备都会收到；rsids 按会话发，
只发给特定设备。rsids 有值时 ruids 会被忽略，两者不叠加。

消息不做持久化存储：important 只保证断线重连期间的补发，不是离线消息队列。
接收方长时间离线的消息需要你自己的业务侧兜底。

**请求参数**

<ParamField body="action" type="string" required>
  消息命令，由你自定义，客户端按它分发处理
  示例：`meeting_invite`
</ParamField>

<ParamField body="content" type="any">
  消息体，任意 JSON，结构由你定
  示例：`&#123;"meeting_no": "818595664", "title": "项目周会"&#125;`
</ParamField>

<ParamField body="uid" type="string">
  发送者用户ID，用于客户端展示"谁发来的"；服务端下发的系统消息可留空（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>

<ParamField body="sid" type="string">
  发送者会话ID
</ParamField>

<ParamField body="name" type="string">
  发送者名称
  示例：`张三`
</ParamField>

<ParamField body="ruids" type="array<string>">
  接收者用户ID列表(当Rsids有数据时,忽略此字段)
  示例：`["1002","1003"]`
</ParamField>

<ParamField body="rsids" type="array<string>">
  接收者SessionID列表，按设备精确投递
</ParamField>

<ParamField body="important" type="boolean">
  是否重要，重要消息在断线重连后会重发确保收到。邀请、呼叫这类不能丢的消息应开启，普通状态同步不必
</ParamField>


请求示例：

```json
{
  "action": "meeting_invite",
  "content": "{\"meeting_no\": \"818595664\", \"title\": \"项目周会\"}",
  "important": false,
  "name": "张三",
  "rsids": [
    ""
  ],
  "ruids": [
    "1002",
    "1003"
  ],
  "sid": "",
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

## 强制下线IM设备

`POST /server/v1/im/kick-device`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

强制断开指定用户或设备的 IM 连接，常用于账号在别处登录时踢掉旧设备。
被踢设备会收到通知并触发 im_disconnect 回调。

只断开 IM 连接，不影响该用户已在进行的频道通话；也不阻止对方重新连接 ——
需要禁止重连请在你的业务侧停止发放 IM 令牌。

**请求参数**

<ParamField body="uid" type="string">
  操作者用户ID，用于审计（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>

<ParamField body="ruids" type="array<string>">
  被踢者用户ID列表，按用户踢会踢掉其全部设备(当Rsids有数据时,忽略此字段)
  示例：`["1002"]`
</ParamField>

<ParamField body="rsids" type="array<string>">
  被踢者SessionID列表，按会话踢只踢特定设备
</ParamField>


请求示例：

```json
{
  "rsids": [
    ""
  ],
  "ruids": [
    "1002"
  ],
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

## 获取用户所有在线设备

`POST /server/v1/im/user-device-list`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

批量查询用户当前的 IM 在线设备，用于判断"这个人现在能不能收到推送"、
或展示多端在线状态。

响应的 data 是「用户ID → 设备列表」的映射，不在线的用户不会出现在结果里。
每台设备有独立的 sid 与 device_type，可以用它按设备精确发消息或踢线。

**请求参数**

<ParamField body="uids" type="array<string>" required>
  用户ID列表
  示例：`["1001","1002"]`
</ParamField>


请求示例：

```json
{
  "uids": [
    "1001",
    "1002"
  ]
}
```

**响应参数**

<ResponseField name="<键>" type="array<object>">
  键为动态值，见上方说明
  <Expandable title="元素字段">
    <ResponseField name="uid" type="string">
      用户ID
    </ResponseField>

    <ResponseField name="sid" type="string">
      会话ID
    </ResponseField>

    <ResponseField name="device_type" type="integer">
      设备类型
    </ResponseField>

    <ResponseField name="device_id" type="string">
      设备唯一id
    </ResponseField>

  </Expandable>
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {}
}
```

---

