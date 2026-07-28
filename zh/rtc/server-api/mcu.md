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

<ResponseField name="app_id" type="string">
  应用ID
</ResponseField>

<ResponseField name="layout" type="string">
  布局类型 auto,full,grids_2,grids_4,...
</ResponseField>

<ResponseField name="watermark_type" type="integer">
  水印类型 1无,2单排,3多排
</ResponseField>

<ResponseField name="window_tag_type" type="string">
  窗口标签位置 字母或组合:L左,R右,T上,B下,空表示不启用标签
</ResponseField>

<ResponseField name="created_at" type="integer">
</ResponseField>

<ResponseField name="updated_at" type="integer">
</ResponseField>


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

<ParamField body="layout" type="string">
  布局类型 auto,full,grids_2,grids_4,...
</ParamField>

<ParamField body="watermark_type" type="integer">
  水印类型 1无,2单排,3多排
</ParamField>

<ParamField body="window_tag_type" type="string">
  窗口标签位置 字母或组合:L左,R右,T上,B下,空表示不启用标签（最大长度 2）
</ParamField>


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

<ParamField body="begin_at" type="integer">
</ParamField>

<ParamField body="end_at" type="integer">
</ParamField>

<ParamField body="search" type="array<string>">
  通用搜索
</ParamField>

<ParamField body="sort" type="string">
  排序（可排序字段：created_at）
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

<ResponseField name="task_id" type="string">
  任务ID
</ResponseField>

<ResponseField name="op_uid" type="string">
  任务发起人ID
</ResponseField>

<ResponseField name="op_name" type="string">
  任务发起人名
</ResponseField>

<ResponseField name="channel" type="string">
  频道
</ResponseField>

<ResponseField name="title" type="string">
  频道标题
</ResponseField>

<ResponseField name="room_no" type="string">
  外部会议号
</ResponseField>

<ResponseField name="task_status" type="integer">
  0待开始 1进行中 2待结束 3异常结束 4正常结束
</ResponseField>

<ResponseField name="err_desc" type="string">
  错误描述
</ResponseField>

<ResponseField name="vod_key" type="string">
  录像文件key
</ResponseField>

<ResponseField name="vod_size" type="integer">
  录像大小(字节)
</ResponseField>

<ResponseField name="mcu_at" type="integer">
  MCU开始时间
</ResponseField>

<ResponseField name="mcu_dur" type="integer">
  Mcu时长(秒)
</ResponseField>

<ResponseField name="tags" type="string">
  录像标签 逗号隔开
</ResponseField>

<ResponseField name="created_at" type="integer">
</ResponseField>

<ResponseField name="updated_at" type="integer">
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

<ParamField body="task_id" type="string">
  任务ID
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)
</ParamField>

<ParamField body="is_lan" type="boolean">
  是否局域网
</ParamField>


请求示例：

```json
{
  "channel": "",
  "is_lan": false,
  "task_id": ""
}
```

**响应参数**

<ResponseField name="addr" type="string">
  录像地址
</ResponseField>

<ResponseField name="size" type="integer">
  录像大小(字节)
</ResponseField>

<ResponseField name="mcu_at" type="integer">
  MCU开始时间
</ResponseField>

<ResponseField name="mcu_dur" type="integer">
  Mcu时长(秒)
</ResponseField>


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

<ParamField body="task_id" type="string">
  任务ID
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)
</ParamField>


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

<ParamField body="task_type" type="integer" required>
  1录像模式 2合流模式 3混合模式
</ParamField>

<ParamField body="op_uid" type="string">
  任务发起人ID
</ParamField>

<ParamField body="op_name" type="string">
  任务发起人名（最大长度 100）
</ParamField>

<ParamField body="channel" type="string" required>
  频道（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
</ParamField>

<ParamField body="title" type="string" required>
  频道标题
</ParamField>

<ParamField body="room_no" type="string">
  外部会议号（最大长度 50）
</ParamField>

<ParamField body="tags" type="string">
  录像标签,逗号分隔
</ParamField>

<ParamField body="layout_data" type="object">
  布局数据
  <Expandable title="字段">
    <ParamField body="layout" type="string" required>
      布局类型
    </ParamField>

    <ParamField body="watermark" type="object">
      水印
      <Expandable title="字段">
        <ParamField body="type" type="integer">
          类型 0默认, 1无, 2单排, 3多排
        </ParamField>

        <ParamField body="text" type="string">
          指定内容, 空表示自动(会议标题)
        </ParamField>

        <ParamField body="size" type="integer">
          字体大小, 0表示默认值
        </ParamField>

        <ParamField body="color" type="string">
          字体颜色, 空表示默认值
        </ParamField>

        <ParamField body="ol_color" type="string">
          轮廓颜色, 空表示默认值
        </ParamField>

        <ParamField body="ol_width" type="integer">
          轮廓线宽, 0表示默认值
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="nobody_text" type="string">
      会中无人时显示的文本, 空表示无人时停止录制
    </ParamField>

    <ParamField body="tag" type="object">
      默认标签
      <Expandable title="字段">
        <ParamField body="type" type="string">
          类型, 字母或组合: L左, R右, T上, B下
        </ParamField>

        <ParamField body="text" type="string">
          指定内容, 空表示自动(会中名称)
        </ParamField>

        <ParamField body="size" type="integer">
          字体大小, 0表示默认
        </ParamField>

        <ParamField body="color" type="string">
          字体颜色, 空表示默认
        </ParamField>

        <ParamField body="bg_color" type="string">
          背景颜色, 空表示默认
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="polling_dur" type="integer">
      轮询时长(秒) 0不轮询
    </ParamField>

    <ParamField body="div_list" type="array<object>">
      逻辑块列表
      <Expandable title="元素字段">
        <ParamField body="cells" type="array<object>">
          宫格列表, 空表示剩余格子共用此处的用户
        </ParamField>

        <ParamField body="uids" type="array<string>">
          用户ID列表, 空表示大轮询在线剩余用户, 多个表示小轮询
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="names" type="object">
      用户名称表, 与McuDiv.Uids对应(不必需)
    </ParamField>

  </Expandable>
</ParamField>


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

<ParamField body="task_id" type="string">
  任务ID
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)
</ParamField>

<ParamField body="task_type" type="integer">
  任务类型(选填)
</ParamField>


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

<ParamField body="task_id" type="string">
  任务ID
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)
</ParamField>


请求示例：

```json
{
  "channel": "",
  "task_id": ""
}
```

**响应参数**

<ResponseField name="task_id" type="string">
  任务ID
</ResponseField>

<ResponseField name="op_uid" type="string">
  任务发起人ID
</ResponseField>

<ResponseField name="op_name" type="string">
  任务发起人名
</ResponseField>

<ResponseField name="channel" type="string">
  频道
</ResponseField>

<ResponseField name="title" type="string">
  频道标题
</ResponseField>

<ResponseField name="room_no" type="string">
  外部会议号
</ResponseField>

<ResponseField name="task_status" type="integer">
  0待开始 1进行中 2待结束 3异常结束 4正常结束
</ResponseField>

<ResponseField name="err_desc" type="string">
  错误描述
</ResponseField>

<ResponseField name="vod_key" type="string">
  录像文件key
</ResponseField>

<ResponseField name="vod_size" type="integer">
  录像大小(字节)
</ResponseField>

<ResponseField name="mcu_at" type="integer">
  MCU开始时间
</ResponseField>

<ResponseField name="mcu_dur" type="integer">
  Mcu时长(秒)
</ResponseField>

<ResponseField name="tags" type="string">
  录像标签 逗号隔开
</ResponseField>

<ResponseField name="created_at" type="integer">
</ResponseField>

<ResponseField name="updated_at" type="integer">
</ResponseField>


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

<ParamField body="task_id" type="string" required>
  任务ID
</ParamField>

<ParamField body="title" type="string">
  最大长度 100
</ParamField>

<ParamField body="tags" type="array<string>">
  最大长度 10
</ParamField>


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

<ParamField body="task_id" type="string">
  任务ID
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)
</ParamField>


请求示例：

```json
{
  "channel": "",
  "task_id": ""
}
```

**响应参数**

<ResponseField name="rtmp" type="string">
</ResponseField>

<ResponseField name="flv" type="string">
</ResponseField>

<ResponseField name="hls" type="string">
</ResponseField>


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

