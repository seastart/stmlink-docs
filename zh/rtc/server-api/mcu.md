---
title: "录制与直播"
description: "云端录制、点播地址与直播推流"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 获取默认录制配置

`POST /server/v1/mcu/record-config`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

查询你这个应用的**默认录制配置**。无请求参数。

「启动录制/合流/直播任务」不传 `layout_data` 时就用这份配置，所以适合把统一的水印、标签、布局策略配在这里，避免每次启动任务都重复传。

**请求参数**

无

**响应参数**

<ResponseField name="app_id" type="string">
  应用ID
  示例：`68b3ft51smhz0x5glscw9whm78bw57uu`
</ResponseField>

<ResponseField name="layout" type="string">
  布局类型 auto,full,grids_2,grids_4,...
  示例：`auto`
</ResponseField>

<ResponseField name="watermark_type" type="integer">
  水印类型 1无,2单排,3多排
  示例：`1`
</ResponseField>

<ResponseField name="window_tag_type" type="string">
  窗口标签位置 字母或组合:L左,R右,T上,B下,空表示不启用标签
  示例：`L`
</ResponseField>

<ResponseField name="created_at" type="integer">
  示例：`1718250917`
</ResponseField>

<ResponseField name="updated_at" type="integer">
  示例：`1718250921`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
    "created_at": 1718250917,
    "layout": "auto",
    "updated_at": 1718250921,
    "watermark_type": 1,
    "window_tag_type": "L"
  }
}
```

---

## 更新默认录制配置

`POST /server/v1/mcu/save-record-config`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

全局默认录像配置更新

更新应用的默认录制配置。三个字段都是可选的，只传要改的即可。

+ `layout` 取值同「启动录制/合流/直播任务」
+ `watermark_type`：`1` 无水印、`2` 单排、`3` 多排（`0` 表示沿用系统默认）
+ `window_tag_type` 是每个画面上的成员名标签位置，用字母组合表示：`L` 左、`R` 右、`T` 上、`B` 下，可组合如 `LB` 表示左下；**留空表示不显示标签**

改动只影响之后启动的新任务，进行中的任务不受影响。

**请求参数**

<ParamField body="layout" type="string">
  布局类型: auto自动 full全屏 right_4右侧小窗 top_4顶部小窗 br_7下L型 tl_7上L型 tb_8左右布局, 以及等分宫格 grids_N (N 取 2,3,4,5,6,8,9,12,16,20,25)
  示例：`auto`
</ParamField>

<ParamField body="watermark_type" type="integer">
  水印类型 1无,2单排,3多排
  示例：`1`
</ParamField>

<ParamField body="window_tag_type" type="string">
  窗口标签位置 字母或组合:L左,R右,T上,B下,空表示不启用标签（最大长度 2）
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

分页查询录像列表。

+ `begin_at` / `end_at` 为秒级时间戳，按任务创建时间过滤，传 `0` 表示不限
+ `search` 支持按 `channel`、`task_status`、`room_no`、`op_name`、`title`、`tags` 检索
+ `sort` 支持 `created_at`，前缀 `-` 表示倒序（最新在前）

只有**已完成**的任务才有可播放的录像文件；`task_status` 用于区分进行中与已结束（见响应字段说明）。

**请求参数**

<ParamField body="begin_at" type="integer">
  示例：`1718194666`
</ParamField>

<ParamField body="end_at" type="integer">
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
  示例：`sxjgwy`
</ResponseField>

<ResponseField name="op_uid" type="string">
  任务发起人ID
  示例：`1001`
</ResponseField>

<ResponseField name="op_name" type="string">
  任务发起人名
  示例：`张三`
</ResponseField>

<ResponseField name="channel" type="string">
  频道
  示例：`fire`
</ResponseField>

<ResponseField name="title" type="string">
  频道标题
  示例：`项目周会 2024-06-12`
</ResponseField>

<ResponseField name="room_no" type="string">
  外部会议号
  示例：`818595664`
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
      "channel": "fire",
      "created_at": 0,
      "err_desc": "",
      "mcu_at": 0,
      "mcu_dur": 0,
      "op_name": "张三",
      "op_uid": "1001",
      "room_no": "818595664",
      "tags": "",
      "task_id": "sxjgwy",
      "task_status": 0,
      "title": "项目周会 2024-06-12",
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

获取录像地址

获取录像的回放地址。任务必须**已停止且转码完成**，进行中的任务取不到地址。

+ 有 `task_id` 时按任务取；只传 `channel` 则取该频道最近一次的录像
+ `is_lan` 为 true 时返回内网地址，适合纯内网部署或专线接入的场景；默认返回外网地址

地址有有效期，**不要长期缓存或直接存进你的业务库**，每次播放前重新获取。

**请求参数**

<ParamField body="task_id" type="string">
  任务ID
  示例：`sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)
  示例：`fire`
</ParamField>

<ParamField body="is_lan" type="boolean">
  是否局域网
  示例：`false`
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

MCU录像任务

删除录像。**文件会被真正删除，不可恢复**，请在你的业务侧做好确认。

有 `task_id` 时按任务删；只传 `channel` 则删该频道最近一次的录像。进行中的任务不能删，需先停止。

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

MCU任务开始或更新

启动服务端的录制、合流或直播任务。**同一频道对同一类型只会有一个进行中的任务**——重复调用不会新建，而是按传入参数更新已有任务（所以本接口既是"开始"也是"更新"）。

### task_type 是按位组合的

这是最容易搞错的地方。四个独立能力各占一位，想同时要哪几个就相加：

| 值 | 能力 | 产物 |
| --- | --- | --- |
| 1 | 录像 | 录像文件，用「获取录像播放地址」取回放 |
| 2 | 合流 | 把多路流混成一路（旁路推流、给不支持多流的下游用） |
| 4 | 录音 | 纯音频文件 |
| 8 | 直播流 | 直播拉流地址，用「获取直播拉流地址」取 |

所以 `3` = 录像+合流，`9` = 录像+直播（示例里用的就是 9），`15` = 四种全开。**不要把 3 理解成"混合模式"这一种独立类型**。

### 布局

`layout_data.layout` 决定画面怎么排。`auto` 会按人数自动选宫格，绝大多数场景够用；需要固定画面时才指定具体布局：

| 取值 | 说明 |
| --- | --- |
| `auto` | 自动，按在线人数选宫格 |
| `full` | 全屏单画面 |
| `grids_N` | 等分宫格，N 取 2、3、4、5、6、8、9、12、16、20、25（`grids_3` 是品字形）|
| `right_4` / `top_4` | 主画面 + 右侧/顶部小窗 |
| `br_7` / `tl_7` | 下 L 型 / 上 L 型 |
| `tb_8` | 左右布局 |

不传 `layout_data` 时用应用的默认录制配置（见「获取默认录制配置」）。

### 指定谁出现在哪个格子

`layout_data.div_list` 用来把特定用户钉到特定格子，不指定就按加入顺序自动填充：

+ `cells[].idx` 是格子序号，顺序等同 HTML 表格里 `<td>` 的排列（从左到右、从上到下）
+ `uids` 留空表示"剩余在线用户轮流出现在这些格子里"（大轮询）；填多个则是这几个人在这些格子里轮询（小轮询）
+ `polling_dur` 是轮询间隔秒数，`0` 表示不轮询
+ `cells[].bind_share` 为 true 时该格子优先绑定频道内的共享屏幕流

### 注意

+ 频道里没人时的行为由 `layout_data.nobody_text` 决定：留空表示**暂停录制**，填了文本则继续录制并显示该文本
+ `title` 会成为录像的标题，也是水印的默认内容（`watermark.text` 留空时）
+ `room_no` 是你自己业务的会议号，仅用于回查，RTC 侧不做校验

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
  频道标题
  示例：`项目周会 2024-06-12`
</ParamField>

<ParamField body="room_no" type="string">
  外部会议号（最大长度 50）
  示例：`818595664`
</ParamField>

<ParamField body="tags" type="string">
  录像标签,逗号分隔
  示例：`周会,研发`
</ParamField>

<ParamField body="layout_data" type="object">
  布局数据
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
      示例：`0`
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
              "type": ""
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
  示例：`sxjgwy`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "task_id": "sxjgwy"
  }
}
```

---

## 停止录制/合流/直播任务

`POST /server/v1/mcu/stop`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

MCU任务停止

停止进行中的录制/合流/直播任务。

+ 有 `task_id` 时按任务停；只传 `channel` 则停该频道进行中的任务
+ `task_type` 选填：不传表示停掉该频道所有类型的任务，传了则只停指定类型（按位组合，同「启动」接口）

录像文件在任务停止后才完成转码，随后才能取到播放地址。频道销毁时进行中的任务会自动停止，不必先手动调用本接口。

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
  任务类型(选填)
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

MCU录像任务

查询单个录制任务的详情，包含任务状态、时长、文件信息。

有 `task_id` 时按任务查；只传 `channel` 则查该频道**进行中**的任务——这是判断"某个频道现在是否正在录制"的常用方式。

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
  示例：`sxjgwy`
</ResponseField>

<ResponseField name="op_uid" type="string">
  任务发起人ID
</ResponseField>

<ResponseField name="op_name" type="string">
  任务发起人名
</ResponseField>

<ResponseField name="channel" type="string">
  频道
  示例：`fire`
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
    "channel": "fire",
    "created_at": 0,
    "err_desc": "",
    "mcu_at": 0,
    "mcu_dur": 0,
    "op_name": "",
    "op_uid": "",
    "room_no": "",
    "tags": "",
    "task_id": "sxjgwy",
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

修改录像 注意: 不接受调用方传入 app_id，应用维度一律取鉴权得到的 app_id，避免改到其他租户的录像

修改录像的标题与标签，用于归档整理。不影响录像文件本身。

+ `title` 和 `tags` 都是可选的，只传要改的
+ `tags` 最多 10 个，整体替换而非追加——需要保留的标签要一并传入

标题与标签都可以用「录像列表」的 `search` 检索到。

**请求参数**

<ParamField body="task_id" type="string" required>
  任务ID
  示例：`sxjgwy`
</ParamField>

<ParamField body="title" type="string">
  最大长度 100
  示例：`项目周会 2024-06-12（已归档）`
</ParamField>

<ParamField body="tags" type="array<string>">
  最大长度 10
  示例：`["周会","研发","已归档"]`
</ParamField>


请求示例：

```json
{
  "tags": [
    "周会",
    "研发",
    "已归档"
  ],
  "task_id": "sxjgwy",
  "title": "项目周会 2024-06-12（已归档）"
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

MCU录像任务

获取直播拉流地址。需要启动任务时 `task_type` 带上 `8`（直播流）这一位，否则没有直播流可拉。

与录像地址不同，直播地址在**任务进行中**就能取到——这正是它的用途：把会议画面分发给不参与互动的观众。

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

