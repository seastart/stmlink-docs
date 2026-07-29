---
title: "录制与直播"
description: "云端录制、点播地址与直播推流"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 获取默认录制配置

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

## 更新默认录制配置

`POST /server/v1/mcu/save-record-config`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

更新应用的默认录制配置。三个字段都可选，只传要改的。 改动只影响之后启动的新任务，进行中的任务不受影响。

**请求参数**

<ParamField body="layout" type="string">
  布局类型: auto自动 full全屏 right_4右侧小窗 top_4顶部小窗 br_7下L型 tl_7上L型 tb_8左右布局, 以及等分宫格 grids_N (N 取 2,3,4,5,6,8,9,12,16,20,25)
  示例：`auto`
</ParamField>

<ParamField body="watermark_type" type="integer">
  水印类型 0默认,1无,2单排,3多排
  示例：`1`
</ParamField>

<ParamField body="window_tag_type" type="string">
  每个画面上成员名标签的位置，字母或组合:L左,R右,T上,B下（如 LB 左下）；空表示不显示标签（最大长度 2）
  示例：`L`
</ParamField>


请求示例：

```json
{
  "layout": "auto",
  "watermark_type": 1,
  "window_tag_type": "L"
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

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

分页查询录像列表。只有已完成的任务才有可播放的录像文件， 用响应里的 task_status 区分进行中与已结束。

**请求参数**

<ParamField body="begin_at" type="integer">
  起始时间，秒级时间戳，按任务创建时间过滤；0 表示不限
  示例：`1718194666`
</ParamField>

<ParamField body="end_at" type="integer">
  终止时间，秒级时间戳；0 表示不限
  示例：`1718799878`
</ParamField>

<ParamField body="search" type="array<string>">
  通用搜索
</ParamField>

<ParamField body="sort" type="string">
  排序（可排序字段：created_at）
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
  "begin_at": 1718194666,
  "end_at": 1718799878,
  "page": 1,
  "per-page": 10,
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

## 获取录像播放地址

`POST /server/v1/mcu/vod-url`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

获取录像回放地址。任务必须已停止且转码完成，进行中的任务取不到地址。 地址有有效期，不要长期缓存或存进业务库，每次播放前重新获取。

**请求参数**

<ParamField body="task_id" type="string">
  任务ID
  示例：`sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)；只传频道则取该频道最近一次的录像
  示例：`fire`
</ParamField>

<ParamField body="is_lan" type="boolean">
  是否返回内网地址，适合纯内网部署或专线接入；默认返回外网地址
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "is_lan": false,
  "task_id": "sxjgwy"
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

## 删除录像

`POST /server/v1/mcu/del-record`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

按任务或频道定位一次录制任务：有 task_id 时按任务，只传 channel 则取该频道 进行中的任务（或最近一次录像，取决于具体接口）。

**请求参数**

<ParamField body="task_id" type="string">
  任务ID
  示例：`sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)
  示例：`fire`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "task_id": "sxjgwy"
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

## 启动录制/合流/直播任务

`POST /server/v1/mcu/start`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

启动服务端的录制、合流或直播任务。同一频道对同一类型只有一个进行中的任务： 重复调用不新建，而是按传入参数更新已有任务。

**请求参数**

<ParamField body="task_type" type="integer" required>
  任务类型，按位组合：1录像、2合流、4录音、8直播流；如 3 表示录像+合流，9 表示录像+直播
  示例：`9`
</ParamField>

<ParamField body="op_uid" type="string">
  任务发起人ID
  示例：`1001`
</ParamField>

<ParamField body="op_name" type="string">
  任务发起人名（最大长度 100）
  示例：`张三`
</ParamField>

<ParamField body="channel" type="string" required>
  频道（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="title" type="string" required>
  频道标题。会成为录像标题，也是水印的默认内容（watermark.text 留空时）
  示例：`项目周会 2024-06-12`
</ParamField>

<ParamField body="room_no" type="string">
  外部会议号。你自己业务的会议号，仅用于回查，RTC 侧不校验（最大长度 50）
  示例：`818595664`
</ParamField>

<ParamField body="tags" type="string">
  录像标签，逗号分隔（注意：修改录像接口的 tags 是数组）
  示例：`周会,研发`
</ParamField>

<ParamField body="layout_data" type="object">
  布局数据。不传时使用应用的默认录制配置（见获取默认录制配置）
  <Expandable title="字段">
    <ParamField body="layout" type="string" required>
      布局类型: auto自动 full全屏 right_4右侧小窗 top_4顶部小窗 br_7下L型 tl_7上L型 tb_8左右布局, 以及等分宫格 grids_N (N 取 2,3,4,5,6,8,9,12,16,20,25)
      示例：`auto`
    </ParamField>

    <ParamField body="watermark" type="object">
      水印
      <Expandable title="字段">
        <ParamField body="type" type="integer">
          类型 0默认, 1无, 2单排, 3多排
          示例：`1`
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
          示例：`L`
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
  "channel": "fire",
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
              "type": "L"
            }
          }
        ],
        "uids": [
          ""
        ]
      }
    ],
    "layout": "auto",
    "names": {},
    "nobody_text": "",
    "polling_dur": 0,
    "tag": {
      "bg_color": "",
      "color": "",
      "size": 0,
      "text": "",
      "type": "L"
    },
    "watermark": {
      "color": "",
      "ol_color": "",
      "ol_width": 0,
      "size": 0,
      "text": "",
      "type": 1
    }
  },
  "op_name": "张三",
  "op_uid": "1001",
  "room_no": "818595664",
  "tags": "周会,研发",
  "task_type": 9,
  "title": "项目周会 2024-06-12"
}
```

**响应参数**

<ResponseField name="task_id" type="string">
  本次任务的 ID，停止任务、查询详情、取播放地址都用它
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "task_id": ""
  }
}
```

---

## 停止录制/合流/直播任务

`POST /server/v1/mcu/stop`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

停止进行中的录制/合流/直播任务。录像文件在任务停止后才完成转码，随后才能取到播放地址。 频道销毁时进行中的任务会自动停止，不必先手动调用。

**请求参数**

<ParamField body="task_id" type="string">
  任务ID
  示例：`sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)
  示例：`fire`
</ParamField>

<ParamField body="task_type" type="integer">
  任务类型(选填)。不传表示停掉该频道所有类型的任务；传了则只停指定类型，取值同启动接口
  示例：`1`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "task_id": "sxjgwy",
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

## 录像详情

`POST /server/v1/mcu/record-detail`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

按任务或频道定位一次录制任务：有 task_id 时按任务，只传 channel 则取该频道 进行中的任务（或最近一次录像，取决于具体接口）。

**请求参数**

<ParamField body="task_id" type="string">
  任务ID
  示例：`sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)
  示例：`fire`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "task_id": "sxjgwy"
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

## 修改录像标题与标签

`POST /server/v1/mcu/update-record`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

修改录像的标题与标签，用于归档整理，不影响录像文件本身。 标题与标签都可以用录像列表的 search 检索到。 注意: 不接受调用方传入 app_id，应用维度一律取鉴权得到的 app_id，避免改到其他租户的录像

**请求参数**

<ParamField body="task_id" type="string" required>
  任务ID
  示例：`sxjgwy`
</ParamField>

<ParamField body="title" type="string">
  录像标题，不传表示不改（最大长度 100）
  示例：`项目周会（已归档）`
</ParamField>

<ParamField body="tags" type="array<string>">
  标签，最多 10 个，整体替换而非追加 —— 要保留的标签需一并传入（最大长度 10）
  示例：`["周会","研发"]`
</ParamField>


请求示例：

```json
{
  "tags": [
    "周会",
    "研发"
  ],
  "task_id": "sxjgwy",
  "title": "项目周会（已归档）"
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

## 获取直播拉流地址

`POST /server/v1/mcu/live-url`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

按任务或频道定位一次录制任务：有 task_id 时按任务，只传 channel 则取该频道 进行中的任务（或最近一次录像，取决于具体接口）。

**请求参数**

<ParamField body="task_id" type="string">
  任务ID
  示例：`sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)
  示例：`fire`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "task_id": "sxjgwy"
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

