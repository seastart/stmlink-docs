---
title: "设备接入"
description: "SIP / H323 / GB28181 监控等设备的接入与会中操作"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 新增设备

`POST /server/v1/agent/create`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

把 SIP / H323 话机、国标监控、RTSP 流等外部设备登记到你的应用下，之后就能用
「邀请设备入会」把它拉进频道。返回的是设备 ID，请保存下来 —— 后续修改、删除、
查详情都用它。

请求体字段随 URL 查询参数 type 变化（每种接入方式的必填项不同），
六种接入方式各自要传什么，见「设备接入指南」。

**URL 查询参数**

<ParamField query="type" type="string" required>
  接入方式，取值见「设备接入指南」
</ParamField>

**请求参数**

请求体字段随上面的查询参数变化，见接口说明中指引的指南页。

**响应参数**

<ResponseField name="data" type="string">
  新增设备的 ID，后续修改、删除、查详情都用它
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 修改设备

`POST /server/v1/agent/update`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

修改已登记设备的连接信息或显示名称。请求体字段与「新增设备」相同（按 type 变化），
另需带上设备 id，见「设备接入指南」。

+ type 必须与设备原本的接入方式一致，不能借此把 SIP 设备改成 RTSP；要换接入方式请删除后重新登记
+ 改动会在设备下次连接时生效，正在会中的设备不受影响

**URL 查询参数**

<ParamField query="type" type="string" required>
  接入方式，必须与该设备登记时的一致
</ParamField>

**请求参数**

请求体字段随上面的查询参数变化，见接口说明中指引的指南页。

**响应参数**

<ResponseField name="data" type="string">
  被修改的设备 ID
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 设置国标设备的一个通道

`POST /server/v1/agent/set-gb28181-subject`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

给国标设备添加或更新一个通道（一台国标设备下可以有多个摄像头通道）。
通道编号已存在时是更新名称，不存在则新增。

也可以在「新增设备」时用 subjects 一次性批量传入。

**请求参数**

<ParamField body="id" type="string" required>
  设备id，来自「新增设备」的返回值或「设备列表」（最大长度 64）
  示例：`sw8kjx`
</ParamField>

<ParamField body="subject" type="string" required>
  通道编号，需与设备端的实际配置一致；可用「生成国标设备的通道编号」按规范自动生成（最大长度 20）
  示例：`50010700001320000001`
</ParamField>

<ParamField body="name" type="string" required>
  通道名称，会中用它区分同一台设备的不同画面（最大长度 100）
  示例：`嘉宾席`
</ParamField>


请求示例：

```json
{
  "id": "sw8kjx",
  "name": "嘉宾席",
  "subject": "50010700001320000001"
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

## 删除国标设备的一个通道

`POST /server/v1/agent/del-gb28181-subject`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

删除国标设备的一个通道。设备本身不受影响，只是该通道不再可被邀请入会。
正在会中的通道会先被移出频道。

**请求参数**

<ParamField body="id" type="string" required>
  设备id（最大长度 64）
  示例：`sw8kjx`
</ParamField>

<ParamField body="subject" type="string" required>
  通道编号（最大长度 20）
  示例：`50010700001320000001`
</ParamField>


请求示例：

```json
{
  "id": "sw8kjx",
  "subject": "50010700001320000001"
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

## 生成国标设备的通道编号

`POST /server/v1/agent/gen-gb28181-subject`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

按国标规范为指定设备生成一个尚未使用的通道编号，避免自己拼编号时格式出错
或与已有通道冲突。

生成的编号只是返回给你，不会自动登记 —— 拿到后仍需调「设置国标设备的一个通道」
并填上通道名称。

**请求参数**

<ParamField body="id" type="string" required>
  设备id（最大长度 64）
  示例：`sw8kjx`
</ParamField>


请求示例：

```json
{
  "id": "sw8kjx"
}
```

**响应参数**

<ResponseField name="data" type="string">
  生成的通道编号，尚未登记，需再调「设置国标设备的一个通道」
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 生成国标设备的 SIP 编号

`POST /server/v1/agent/gen-gb28181-sip-no`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

生成一个尚未使用的国标设备 SIP 编号，用于登记新的国标设备（type=gb28181 时的
sip_no）。无请求参数。

同样只是返回编号，不会自动创建设备。

**请求参数**

无

**响应参数**

<ResponseField name="data" type="string">
  生成的设备 SIP 编号，尚未创建设备
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 设备网关列表

`POST /server/v1/agent/list-gw`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

列出可用的设备网关。登记设备前先调它拿 gw 的取值。

设备网关是介于外部设备与 RTC 之间的转换层：SIP/H323/国标各有自己的信令协议，
由网关负责对接，并把媒体转成 RTC 能用的格式。不同网关支持的接入方式不同，
所以用 type 筛选，取值见「设备接入指南」。

**URL 查询参数**

<ParamField query="type" type="string" required>
  按接入方式筛选，只返回支持该方式的网关；取值见「设备接入指南」
</ParamField>

**请求参数**

无（参数全部通过 URL 查询串传递）

**响应参数**

<ResponseField name="id" type="string">
  gw id
</ResponseField>

<ResponseField name="types" type="array<integer>">
  代理类型
</ResponseField>

<ResponseField name="heartbeat_at" type="integer">
  上次心跳时间
</ResponseField>

<ResponseField name="host" type="string">
  api接口，用于rtc调设备网关
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "heartbeat_at": 0,
      "host": "",
      "id": "",
      "types": [
        0
      ]
    }
  ]
}
```

---

## 设备网关平台信息列表

`POST /server/v1/agent/list-gw-info`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

获取网关的平台侧信息，用于配置设备端。

典型用法是国标接入：国标摄像头需要在设备端填写"上级平台"的 SIP 编号、域、IP、
端口，这些值就从这里取，填进摄像头的国标配置页面，设备才能注册上来。

与「设备网关列表」的区别：那个是"我们有哪些网关"，这个是"要让设备连上某个网关，
设备端该怎么填"。

**URL 查询参数**

<ParamField query="type" type="string" required>
  接入方式，不同方式返回的平台信息字段不同；取值见「设备接入指南」
</ParamField>

**请求参数**

无（参数全部通过 URL 查询串传递）

**响应参数**

<ResponseField name="id" type="string">
  gw id
</ResponseField>

<ResponseField name="types" type="array<integer>">
  代理类型
</ResponseField>

<ResponseField name="heartbeat_at" type="integer">
  上次心跳时间
</ResponseField>

<ResponseField name="host" type="string">
  api接口，用于rtc调设备网关
</ResponseField>

<ResponseField name="info" type="any">
  网关的平台信息
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "heartbeat_at": 0,
      "host": "",
      "id": "",
      "info": null,
      "types": [
        0
      ]
    }
  ]
}
```

---

## 调用网关的api接口

`POST /server/v1/agent/call-gw-api`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

透传调用设备网关自身的 API，用于常规接口覆盖不到的排查与运维场景
（如查询网关内部状态、触发设备重连）。响应的 data 是网关原样返回的数据。

这是面向运维的低层接口：api 与 params 的取值取决于网关版本，没有稳定性承诺。
业务代码请不要依赖它，优先使用本组其它具名接口。

**请求参数**

<ParamField body="gw" type="string" required>
  网关，取值见「设备网关列表」
  示例：`devgw-1`
</ParamField>

<ParamField body="api" type="string" required>
  网关自身的接口路径
  示例：`/api/v1/status`
</ParamField>

<ParamField body="params" type="object">
  传给网关接口的参数
  示例：`{"device_id":"sw8kjx"}`
</ParamField>


请求示例：

```json
{
  "api": "/api/v1/status",
  "gw": "devgw-1",
  "params": {
    "device_id": "sw8kjx"
  }
}
```

**响应参数**

<ResponseField name="data" type="any">
  网关原样返回的数据（结构不固定）
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": null
}
```

---

## 删除设备

`POST /server/v1/agent/delete`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

删除已登记的设备。响应的 data 是被删除的设备 ID。

设备若正在会中，会先被移出频道。删除后同一台物理设备可以重新登记，
但会得到新的设备 ID。

**请求参数**

<ParamField body="id" type="string" required>
  设备id（最大长度 64）
  示例：`sw8kjx`
</ParamField>


请求示例：

```json
{
  "id": "sw8kjx"
}
```

**响应参数**

<ResponseField name="data" type="string">
  被删除的设备 ID
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 设备详情

`POST /server/v1/agent/detail`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

查询单个设备的详情，包含连接参数、所属网关、在线状态。
设备 id 来自「新增设备」的返回值，或「设备列表」。

**请求参数**

<ParamField body="id" type="string" required>
  设备id（最大长度 64）
  示例：`sw8kjx`
</ParamField>


请求示例：

```json
{
  "id": "sw8kjx"
}
```

**响应参数**

<ResponseField name="id" type="string">
  agent id
</ResponseField>

<ResponseField name="name" type="string">
  代理名称
</ResponseField>

<ResponseField name="type" type="integer">
  代理类型
</ResponseField>

<ResponseField name="status" type="integer">
  在线状态
</ResponseField>

<ResponseField name="heartbeat_at" type="integer">
  上次心跳时间
</ResponseField>

<ResponseField name="contact" type="string">
  设备标识
</ResponseField>

<ResponseField name="conn_params" type="object">
  连接参数，已剔除机密项，见 NewAgent
</ResponseField>

<ResponseField name="gw" type="string">
  设备网关
</ResponseField>

<ResponseField name="remark" type="string">
  备注
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "conn_params": {},
    "contact": "",
    "gw": "",
    "heartbeat_at": 0,
    "id": "",
    "name": "",
    "remark": "",
    "status": 0,
    "type": 0
  }
}
```

---

## 设备列表

`POST /server/v1/agent/list-invite`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

分页查询可邀请的设备列表，通常用于在你的界面上给用户挑设备。

国标设备的每个通道会各占一条。响应里的 contact（设备标识）就是「邀请设备入会」
要传的值。

**请求参数**

<ParamField body="type" type="array<integer>" required>
  代理类型，2 SIP、3 H323、4 GB28181监控、5 RTSP拉流
  示例：`2,4`
</ParamField>

<ParamField body="keyword" type="string">
  关键词，模糊匹配显示名与设备标识（最大长度 100）
  示例：`会议室`
</ParamField>

<ParamField body="name" type="string">
  显示名称，精确筛选（最大长度 100）
  示例：`嘉宾席摄像头`
</ParamField>

<ParamField body="contact" type="string">
  设备标识，精确筛选（最大长度 100）
  示例：`50010700001320000001`
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
  "contact": "50010700001320000001",
  "keyword": "会议室",
  "name": "嘉宾席摄像头",
  "page": 1,
  "per-page": 10,
  "type": "2,4"
}
```

**响应参数**

<ResponseField name="id" type="string">
  agent id
</ResponseField>

<ResponseField name="name" type="string">
  代理名称
</ResponseField>

<ResponseField name="type" type="integer">
  代理类型
</ResponseField>

<ResponseField name="status" type="integer">
  在线状态
</ResponseField>

<ResponseField name="heartbeat_at" type="integer">
  上次心跳时间
</ResponseField>

<ResponseField name="contact" type="string">
  设备标识
</ResponseField>

<ResponseField name="conn_params" type="object">
  连接参数，已剔除机密项，见 NewAgent
</ResponseField>

<ResponseField name="gw" type="string">
  设备网关
</ResponseField>

<ResponseField name="remark" type="string">
  备注
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
      "conn_params": {},
      "contact": "",
      "gw": "",
      "heartbeat_at": 0,
      "id": "",
      "name": "",
      "remark": "",
      "status": 0,
      "type": 0
    }
  ]
}
```

---

## 邀请设备入会

`POST /server/v1/agent/invite`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

把设备拉进频道，可以一次邀请多台。设备的 type 与 contact 从「设备列表」取。

设备入会是异步的：本接口返回成功只表示邀请已下发，设备实际上线要等 user_join
回调（设备的 uid 带 _agent_ 前缀）。邀请一个已在该频道的设备不会重复拉入。

设备接受邀请前会触发 agent_join 回调。若你订阅了该事件，需要按要求返回 sid，
否则设备无法入会 —— 详见「回调事件接入指南」。

**请求参数**

<ParamField body="agents" type="array<any>" required>
  设备列表
</ParamField>

<ParamField body="no" type="string" required>
  目标房间号(如果是meeting层应用就是会议号，如果是rtc层应用就是频道名)
  示例：`fire`
</ParamField>


请求示例：

```json
{
  "agents": [
    null
  ],
  "no": "fire"
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

## 开关设备视频

`POST /server/v1/agent/set-camera-enabled`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

开关设备的摄像头。设备不像普通客户端那样能自己操作，只能由服务端下发。

若你订阅了 agent_operate 回调，本次操作会先征询你的业务后端，返回非 0 表示拒绝；
不订阅则默认允许。

**请求参数**

<ParamField body="uid" type="string">
  设备会中用户ID，不传代表对全频道设备操作。带 _agent_ 前缀，从「在线/离线成员列表」或 user_join 回调拿（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`_agent_co63jg6g54hu3b0xhtie`
</ParamField>

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="enabled" type="boolean">
  是否启用
</ParamField>

<ParamField body="op_uid" type="string">
  主持人uid，用于审计
  示例：`1001`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "enabled": false,
  "op_uid": "1001",
  "uid": "_agent_co63jg6g54hu3b0xhtie"
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

## 开关设备音频

`POST /server/v1/agent/set-mic-enabled`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

开关设备的麦克风，语义与「开关设备视频」一致。

**请求参数**

<ParamField body="uid" type="string">
  设备会中用户ID，不传代表对全频道设备操作。带 _agent_ 前缀（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`_agent_co63jg6g54hu3b0xhtie`
</ParamField>

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="enabled" type="boolean">
  是否启用
</ParamField>

<ParamField body="op_uid" type="string">
  主持人uid，用于审计
  示例：`1001`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "enabled": false,
  "op_uid": "1001",
  "uid": "_agent_co63jg6g54hu3b0xhtie"
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

