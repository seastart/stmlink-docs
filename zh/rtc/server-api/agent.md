---
title: "设备接入"
description: "SIP / H323 / GB28181 监控等设备的接入与会中操作"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 新增设备

`POST /server/v1/agent/create`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

无

**响应参数**


响应示例：

```json
{
  "code": 0,
  "data": null
}
```

---

## 修改设备

`POST /server/v1/agent/update`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

无

**响应参数**


响应示例：

```json
{
  "code": 0,
  "data": null
}
```

---

## 设置国标设备的一个通道

`POST /server/v1/agent/set-gb28181-subject`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="id" type="string" required>
  设备id（最大长度 64）
</ParamField>

<ParamField body="subject" type="string" required>
  通道编号（最大长度 20）
</ParamField>

<ParamField body="name" type="string" required>
  通道名称（最大长度 100）
</ParamField>


请求示例：

```json
{
  "id": "",
  "name": "",
  "subject": ""
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

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="id" type="string" required>
  设备id（最大长度 64）
</ParamField>

<ParamField body="subject" type="string" required>
  通道编号（最大长度 20）
</ParamField>


请求示例：

```json
{
  "id": "",
  "subject": ""
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

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="id" type="string" required>
  设备id（最大长度 64）
</ParamField>


请求示例：

```json
{
  "id": ""
}
```

**响应参数**


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

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

无

**响应参数**


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

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

无

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

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

无

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

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="gw" type="string" required>
  网关
</ParamField>

<ParamField body="api" type="string" required>
</ParamField>

<ParamField body="params" type="object">
</ParamField>


请求示例：

```json
{
  "api": "",
  "gw": "",
  "params": {}
}
```

**响应参数**


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

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="id" type="string" required>
  设备id（最大长度 64）
</ParamField>


请求示例：

```json
{
  "id": ""
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

## 设备详情

`POST /server/v1/agent/detail`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="id" type="string" required>
  设备id（最大长度 64）
</ParamField>


请求示例：

```json
{
  "id": ""
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

## 路由名保留 list-invite 是为了不动已有调用方（live/meeting 后端、各端 demo）

`POST /server/v1/agent/list-invite`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="type" type="array<integer>" required>
  代理类型
</ParamField>

<ParamField body="keyword" type="string">
  关键词（最大长度 100）
</ParamField>

<ParamField body="name" type="string">
  显示名称（最大长度 100）
</ParamField>

<ParamField body="contact" type="string">
  设备标识（最大长度 100）
</ParamField>

<ParamField body="page" type="integer">
  页数，从1开始
</ParamField>

<ParamField body="per-page" type="integer">
  每页数据量
</ParamField>


请求示例：

```json
{
  "contact": "",
  "keyword": "",
  "name": "",
  "page": 0,
  "per-page": 0,
  "type": [
    0
  ]
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

## 邀请设备入会，最终由应用层封装接口在应用层界面呈现

`POST /server/v1/agent/invite`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="agents" type="array<any>" required>
  设备列表
</ParamField>

<ParamField body="no" type="string" required>
  目标房间号(如果是meeting层应用就是会议号，如果是rtc层应用就是频道名)
</ParamField>


请求示例：

```json
{
  "agents": [
    null
  ],
  "no": ""
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

## 开关设备视频，应用层后端检测到是操作设备时内部调用

`POST /server/v1/agent/set-camera-enabled`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="uid" type="string">
  设备会中用户ID，不传代表对全频道设备操作（仅支持大小写字母、数字、下划线 _ 与连字符 -）
</ParamField>

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
</ParamField>

<ParamField body="enabled" type="boolean">
  是否启用
</ParamField>

<ParamField body="op_uid" type="string">
  主持人uid
</ParamField>


请求示例：

```json
{
  "channel": "",
  "enabled": false,
  "op_uid": "",
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

## 开关设备音频，应用层后端检测到是操作设备时内部调用

`POST /server/v1/agent/set-mic-enabled`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="uid" type="string">
  设备会中用户ID，不传代表对全频道设备操作（仅支持大小写字母、数字、下划线 _ 与连字符 -）
</ParamField>

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
</ParamField>

<ParamField body="enabled" type="boolean">
  是否启用
</ParamField>

<ParamField body="op_uid" type="string">
  主持人uid
</ParamField>


请求示例：

```json
{
  "channel": "",
  "enabled": false,
  "op_uid": "",
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

