---
title: "会议录制与直播"
description: "整场会议的云端录制、点播地址与直播推流"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 meeting-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 获取录制配置

`POST /server/v1/mcu/record-config`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

全局默认录像配置信息

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
  配置创建时间(时间戳)
</ResponseField>

<ResponseField name="updated_at" type="integer">
  配置更新时间(时间戳)
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

## 保存录制配置

`POST /server/v1/mcu/save-record-config`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

全局默认录像配置更新

**请求参数**

<ParamField body="layout" type="string">
  布局类型 auto,full,grids_2,grids_4,...
</ParamField>

<ParamField body="watermark_type" type="integer">
  水印类型 1无,2单排,3多排
</ParamField>

<ParamField body="window_tag_type" type="string">
  窗口标签位置 字母或组合:L左,R右,T上,B下,空表示不启用标签
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

## 录像列表

`POST /server/v1/mcu/list-record`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="begin_at" type="integer">
  开始时间
</ParamField>

<ParamField body="end_at" type="integer">
  结束时间
</ParamField>

<ParamField body="search" type="array<string>">
  附加筛选条件，格式 字段:操作符:值（如 title:like:周会）；room_no/meeting_id 已自动转成条件，不用重复传
</ParamField>

<ParamField body="sort" type="string">
  排序字段，逗号分隔，前缀 - 表示倒序，如 -created_at
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
  "end_at": 0,
  "meeting_id": "",
  "page": 1,
  "per-page": 10,
  "room_no": "",
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

<ResponseField name="mp4_key" type="string">
  转码文件key
</ResponseField>

<ResponseField name="mp4_size" type="integer">
  转码大小(字节)
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
  任务创建时间(时间戳)
</ResponseField>

<ResponseField name="updated_at" type="integer">
  任务更新时间(时间戳)
</ResponseField>

<ResponseField name="now" type="integer">
  当前时间, 用于前端本地时间不准时辅助计算录制时长
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
      "mp4_key": "",
      "mp4_size": 0,
      "now": 0,
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

## 单个录像的点播地址

`POST /server/v1/mcu/vod-url`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

获取录像地址(单个)

**请求参数**

<ParamField body="task_id" type="string">
  任务ID
</ParamField>

<ParamField body="meeting_id" type="string">
  频道(无TaskId时必填)
</ParamField>

<ParamField body="is_lan" type="boolean">
  是否局域网
</ParamField>


请求示例：

```json
{
  "is_lan": false,
  "meeting_id": "",
  "task_id": ""
}
```

**响应参数**

<ResponseField name="<键>" type="string">
  键为动态值，见上方说明
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {}
}
```

---

## 一场会议全部录像的点播地址

`POST /server/v1/mcu/vods-url`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

获取录像地址(多个)

**请求参数**

<ParamField body="meeting_id" type="string">
  会议ID(无RoomNo时必填)
</ParamField>

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="type" type="string">
  类型, 可选值: "", "mp4"
</ParamField>

<ParamField body="is_lan" type="boolean">
  是否局域网
</ParamField>


请求示例：

```json
{
  "is_lan": false,
  "meeting_id": "",
  "room_no": "",
  "type": ""
}
```

**响应参数**

<ResponseField name="url" type="string">
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
  "data": [
    {
      "mcu_at": 0,
      "mcu_dur": 0,
      "size": 0,
      "url": ""
    }
  ]
}
```

---

## 直播流地址

`POST /server/v1/mcu/live-url`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

获取直播地址

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": ""
}
```

**响应参数**

<ResponseField name="rtmp" type="string">
  RTMP 拉流地址
</ResponseField>

<ResponseField name="flv" type="string">
  HTTP-FLV 拉流地址
</ResponseField>

<ResponseField name="hls" type="string">
  HLS 拉流地址
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

## 删除录像

`POST /server/v1/mcu/del-record`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

**请求参数**

<ParamField body="task_id" type="string" required>
  任务ID
</ParamField>


请求示例：

```json
{
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

## 开始 / 更新录制任务

`POST /server/v1/mcu/start`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

开始录制任务

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="task_type" type="integer" required>
  任务类型，按位组合：1录像、2合流、4录音、8直播流；如 3 表示录像+合流，9 表示录像+直播
  示例：`9`
</ParamField>

<ParamField body="title" type="string">
  录制任务标题
</ParamField>

<ParamField body="op_uid" type="string">
  任务发起人ID
</ParamField>

<ParamField body="op_name" type="string">
  任务发起人名称
</ParamField>

<ParamField body="tags" type="string">
  录像标签,逗号分隔
</ParamField>

<ParamField body="layout_data" type="object" required>
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

  </Expandable>
</ParamField>


请求示例：

```json
{
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
  "meeting_id": "",
  "op_name": "",
  "op_uid": "",
  "room_no": "",
  "tags": "",
  "task_type": 9,
  "title": ""
}
```

**响应参数**

<ResponseField name="<键>" type="string">
  键为动态值，见上方说明
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {}
}
```

---

## 结束录制任务

`POST /server/v1/mcu/stop`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="task_type" type="integer">
  任务类型(选填)。不传表示停掉该会议所有类型的任务；传了则只停指定类型，取值同启动接口
  示例：`1`
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "task_type": 1
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

