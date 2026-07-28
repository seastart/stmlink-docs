---
title: "录制与直播"
description: "云端录制、点播地址与直播推流"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## Mcu.RecordConfig

`POST /server/v1/mcu/record-config`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

无

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data.app_id | string | 应用ID |
| data.layout | string | 布局类型 auto,full,grids_2,grids_4,... |
| data.watermark_type | integer | 水印类型 1无,2单排,3多排 |
| data.window_tag_type | string | 窗口标签位置 字母或组合:L左,R右,T上,B下,空表示不启用标签 |
| data.created_at | integer |  |
| data.updated_at | integer |  |

响应示例：

```json
{
  "code": 0,
  "data": {
    "app_id": "",
    "created_at": 0,
    "layout": "",
    "updated_at": 0,
    "watermark_type": 0,
    "window_tag_type": ""
  }
}
```

---

## Mcu.SaveRecordConfig

`POST /server/v1/mcu/save-record-config`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| layout | string | 否 | 布局类型 auto,full,grids_2,grids_4,... |
| watermark_type | integer | 否 | 水印类型 1无,2单排,3多排 |
| window_tag_type | string | 否 | 窗口标签位置 字母或组合:L左,R右,T上,B下,空表示不启用标签（最大长度 2） |

请求示例：

```json
{
  "layout": "",
  "watermark_type": 0,
  "window_tag_type": ""
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

## Mcu.ListRecord

`POST /server/v1/mcu/list-record`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| begin_at | integer | 否 |  |
| end_at | integer | 否 |  |
| search | array | 否 | 通用搜索 |
| sort | string | 否 | 排序（可排序字段：created_at） |
| page | integer | 否 | 页数，从1开始 |
| per-page | integer | 否 | 每页数据量 |

请求示例：

```json
{
  "begin_at": 0,
  "end_at": 0,
  "page": 0,
  "per-page": 0,
  "search": [
    ""
  ],
  "sort": ""
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data[].task_id | string | 任务ID |
| data[].op_uid | string | 任务发起人ID |
| data[].op_name | string | 任务发起人名 |
| data[].channel | string | 频道 |
| data[].title | string | 频道标题 |
| data[].room_no | string | 外部会议号 |
| data[].task_status | integer | 0待开始 1进行中 2待结束 3异常结束 4正常结束 |
| data[].err_desc | string | 错误描述 |
| data[].vod_key | string | 录像文件key |
| data[].vod_size | integer | 录像大小(字节) |
| data[].mcu_at | integer | MCU开始时间 |
| data[].mcu_dur | integer | Mcu时长(秒) |
| data[].tags | string | 录像标签 逗号隔开 |
| data[].created_at | integer |  |
| data[].updated_at | integer |  |

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
      "channel": "",
      "created_at": 0,
      "err_desc": "",
      "mcu_at": 0,
      "mcu_dur": 0,
      "op_name": "",
      "op_uid": "",
      "room_no": "",
      "tags": "",
      "task_id": "",
      "task_status": 0,
      "title": "",
      "updated_at": 0,
      "vod_key": "",
      "vod_size": 0
    }
  ]
}
```

---

## Mcu.VodUrl

`POST /server/v1/mcu/vod-url`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| task_id | string | 否 | 任务ID |
| channel | string | 否 | 频道(无TaskId时必填) |
| is_lan | boolean | 否 | 是否局域网 |

请求示例：

```json
{
  "channel": "",
  "is_lan": false,
  "task_id": ""
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data.addr | string | 录像地址 |
| data.size | integer | 录像大小(字节) |
| data.mcu_at | integer | MCU开始时间 |
| data.mcu_dur | integer | Mcu时长(秒) |

响应示例：

```json
{
  "code": 0,
  "data": {
    "addr": "",
    "mcu_at": 0,
    "mcu_dur": 0,
    "size": 0
  }
}
```

---

## Mcu.DelRecord

`POST /server/v1/mcu/del-record`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| task_id | string | 否 | 任务ID |
| channel | string | 否 | 频道(无TaskId时必填) |

请求示例：

```json
{
  "channel": "",
  "task_id": ""
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

## Mcu.Start

`POST /server/v1/mcu/start`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| task_type | integer | 是 | 1录像模式 2合流模式 3混合模式 |
| op_uid | string | 否 | 任务发起人ID |
| op_name | string | 否 | 任务发起人名（最大长度 100） |
| channel | string | 是 | 频道（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -） |
| title | string | 是 | 频道标题 |
| room_no | string | 否 | 外部会议号（最大长度 50） |
| tags | string | 否 | 录像标签,逗号分隔 |
| layout_data | object | 否 | 布局数据 |
| layout_data.layout | string | 是 | 布局类型 |
| layout_data.watermark | object | 否 | 水印 |
| layout_data.watermark.type | integer | 否 | 类型 0默认, 1无, 2单排, 3多排 |
| layout_data.watermark.text | string | 否 | 指定内容, 空表示自动(会议标题) |
| layout_data.watermark.size | integer | 否 | 字体大小, 0表示默认值 |
| layout_data.watermark.color | string | 否 | 字体颜色, 空表示默认值 |
| layout_data.watermark.ol_color | string | 否 | 轮廓颜色, 空表示默认值 |
| layout_data.watermark.ol_width | integer | 否 | 轮廓线宽, 0表示默认值 |
| layout_data.nobody_text | string | 否 | 会中无人时显示的文本, 空表示无人时停止录制 |
| layout_data.tag | object | 否 | 默认标签 |
| layout_data.tag.type | string | 否 | 类型, 字母或组合: L左, R右, T上, B下 |
| layout_data.tag.text | string | 否 | 指定内容, 空表示自动(会中名称) |
| layout_data.tag.size | integer | 否 | 字体大小, 0表示默认 |
| layout_data.tag.color | string | 否 | 字体颜色, 空表示默认 |
| layout_data.tag.bg_color | string | 否 | 背景颜色, 空表示默认 |
| layout_data.polling_dur | integer | 否 | 轮询时长(秒) 0不轮询 |
| layout_data.div_list | array | 否 | 逻辑块列表 |
| layout_data.div_list[].cells | array | 否 | 宫格列表, 空表示剩余格子共用此处的用户 |
| layout_data.div_list[].cells[].idx | integer | 否 | 格子序号, 排序规则按HTML中&lt;td&gt;标签的顺序 |
| layout_data.div_list[].cells[].bind_share | boolean | 否 | 是否优化绑定频道内的共享流 |
| layout_data.div_list[].cells[].tag | object | 否 | 标签 |
| layout_data.div_list[].cells[].tag.type | string | 否 | 类型, 字母或组合: L左, R右, T上, B下 |
| layout_data.div_list[].cells[].tag.text | string | 否 | 指定内容, 空表示自动(会中名称) |
| layout_data.div_list[].cells[].tag.size | integer | 否 | 字体大小, 0表示默认 |
| layout_data.div_list[].cells[].tag.color | string | 否 | 字体颜色, 空表示默认 |
| layout_data.div_list[].cells[].tag.bg_color | string | 否 | 背景颜色, 空表示默认 |
| layout_data.div_list[].uids | array | 否 | 用户ID列表, 空表示大轮询在线剩余用户, 多个表示小轮询 |
| layout_data.names | object | 否 | 用户名称表, 与McuDiv.Uids对应(不必需) |

请求示例：

```json
{
  "channel": "",
  "layout_data": {
    "div_list": [
      {
        "cells": [
          {
            "bind_share": false,
            "idx": 0,
            "tag": {
              "bg_color": "",
              "color": "",
              "size": 0,
              "text": "",
              "type": ""
            }
          }
        ],
        "uids": [
          ""
        ]
      }
    ],
    "layout": "",
    "names": {},
    "nobody_text": "",
    "polling_dur": 0,
    "tag": {
      "bg_color": "",
      "color": "",
      "size": 0,
      "text": "",
      "type": ""
    },
    "watermark": {
      "color": "",
      "ol_color": "",
      "ol_width": 0,
      "size": 0,
      "text": "",
      "type": 0
    }
  },
  "op_name": "",
  "op_uid": "",
  "room_no": "",
  "tags": "",
  "task_type": 0,
  "title": ""
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

## Mcu.Stop

`POST /server/v1/mcu/stop`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| task_id | string | 否 | 任务ID |
| channel | string | 否 | 频道(无TaskId时必填) |
| task_type | integer | 否 | 任务类型(选填) |

请求示例：

```json
{
  "channel": "",
  "task_id": "",
  "task_type": 0
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

## Mcu.RecordDetail

`POST /server/v1/mcu/record-detail`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| task_id | string | 否 | 任务ID |
| channel | string | 否 | 频道(无TaskId时必填) |

请求示例：

```json
{
  "channel": "",
  "task_id": ""
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data.task_id | string | 任务ID |
| data.op_uid | string | 任务发起人ID |
| data.op_name | string | 任务发起人名 |
| data.channel | string | 频道 |
| data.title | string | 频道标题 |
| data.room_no | string | 外部会议号 |
| data.task_status | integer | 0待开始 1进行中 2待结束 3异常结束 4正常结束 |
| data.err_desc | string | 错误描述 |
| data.vod_key | string | 录像文件key |
| data.vod_size | integer | 录像大小(字节) |
| data.mcu_at | integer | MCU开始时间 |
| data.mcu_dur | integer | Mcu时长(秒) |
| data.tags | string | 录像标签 逗号隔开 |
| data.created_at | integer |  |
| data.updated_at | integer |  |

响应示例：

```json
{
  "code": 0,
  "data": {
    "channel": "",
    "created_at": 0,
    "err_desc": "",
    "mcu_at": 0,
    "mcu_dur": 0,
    "op_name": "",
    "op_uid": "",
    "room_no": "",
    "tags": "",
    "task_id": "",
    "task_status": 0,
    "title": "",
    "updated_at": 0,
    "vod_key": "",
    "vod_size": 0
  }
}
```

---

## Mcu.UpdateRecord

`POST /server/v1/mcu/update-record`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| task_id | string | 是 | 任务ID |
| title | string | 否 | 最大长度 100 |
| tags | array | 否 | 最大长度 10 |

请求示例：

```json
{
  "tags": [
    ""
  ],
  "task_id": "",
  "title": ""
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

## Mcu.LiveUrl

`POST /server/v1/mcu/live-url`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| task_id | string | 否 | 任务ID |
| channel | string | 否 | 频道(无TaskId时必填) |

请求示例：

```json
{
  "channel": "",
  "task_id": ""
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data.rtmp | string |  |
| data.flv | string |  |
| data.hls | string |  |

响应示例：

```json
{
  "code": 0,
  "data": {
    "flv": "",
    "hls": "",
    "rtmp": ""
  }
}
```

---

