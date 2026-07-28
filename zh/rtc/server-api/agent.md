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

| 参数名 | 类型 | 说明 |
| --- | --- | --- |

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

| 参数名 | 类型 | 说明 |
| --- | --- | --- |

响应示例：

```json
{
  "code": 0,
  "data": null
}
```

---

## 国标GB28181设备的通道操作

`POST /server/v1/agent/set-gb28181-subject`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| id | string | 是 | 设备id（最大长度 64） |
| subject | string | 是 | 通道编号（最大长度 20） |
| name | string | 是 | 通道名称（最大长度 100） |

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

## Agent.DelGb28181Subject

`POST /server/v1/agent/del-gb28181-subject`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| id | string | 是 | 设备id（最大长度 64） |
| subject | string | 是 | 通道编号（最大长度 20） |

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

## Agent.GenGb28181Subject

`POST /server/v1/agent/gen-gb28181-subject`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| id | string | 是 | 设备id（最大长度 64） |

请求示例：

```json
{
  "id": ""
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |

响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## Agent.GenGb28181SipNo

`POST /server/v1/agent/gen-gb28181-sip-no`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

无

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |

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

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data[].id | string | gw id |
| data[].types | array | 代理类型 |
| data[].heartbeat_at | integer | 上次心跳时间 |
| data[].host | string | api接口，用于rtc调设备网关 |

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

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data[].id | string | gw id |
| data[].types | array | 代理类型 |
| data[].heartbeat_at | integer | 上次心跳时间 |
| data[].host | string | api接口，用于rtc调设备网关 |
| data[].info | any | 网关的平台信息 |

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

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| gw | string | 是 | 网关 |
| api | string | 是 |  |
| params | object | 否 |  |

请求示例：

```json
{
  "api": "",
  "gw": "",
  "params": {}
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |

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

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| id | string | 是 | 设备id（最大长度 64） |

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

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| id | string | 是 | 设备id（最大长度 64） |

请求示例：

```json
{
  "id": ""
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data.id | string | agent id |
| data.name | string | 代理名称 |
| data.type | integer | 代理类型 |
| data.status | integer | 在线状态 |
| data.heartbeat_at | integer | 上次心跳时间 |
| data.contact | string | 设备标识 |
| data.conn_params | object | 连接参数，已剔除机密项，见 NewAgent |
| data.gw | string | 设备网关 |
| data.remark | string | 备注 |

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

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| type | array | 是 | 代理类型 |
| keyword | string | 否 | 关键词（最大长度 100） |
| name | string | 否 | 显示名称（最大长度 100） |
| contact | string | 否 | 设备标识（最大长度 100） |
| page | integer | 否 | 页数，从1开始 |
| per-page | integer | 否 | 每页数据量 |

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

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data[].id | string | agent id |
| data[].name | string | 代理名称 |
| data[].type | integer | 代理类型 |
| data[].status | integer | 在线状态 |
| data[].heartbeat_at | integer | 上次心跳时间 |
| data[].contact | string | 设备标识 |
| data[].conn_params | object | 连接参数，已剔除机密项，见 NewAgent |
| data[].gw | string | 设备网关 |
| data[].remark | string | 备注 |

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

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| agents | array | 是 | 设备列表 |
| no | string | 是 | 目标房间号(如果是meeting层应用就是会议号，如果是rtc层应用就是频道名) |

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

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| uid | string | 否 | 设备会中用户ID，不传代表对全频道设备操作（仅支持大小写字母、数字、下划线 _ 与连字符 -） |
| channel | string | 是 | 频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -） |
| enabled | boolean | 否 | 是否启用 |
| op_uid | string | 否 | 主持人uid |

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

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| uid | string | 否 | 设备会中用户ID，不传代表对全频道设备操作（仅支持大小写字母、数字、下划线 _ 与连字符 -） |
| channel | string | 是 | 频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -） |
| enabled | boolean | 否 | 是否启用 |
| op_uid | string | 否 | 主持人uid |

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

