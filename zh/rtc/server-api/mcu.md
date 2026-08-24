---
title: "云录制与直播"
description: "整场云端录制、点播地址与直播推流；按说话人分轨的录音是另一套接口，见「语音录制」"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 rtc-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 获取默认录制配置

`POST /server/v1/mcu/record-config`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

查询应用当前的默认录制配置（布局、水印、成员名标签位置）。无请求参数，
配置是应用维度的，由鉴权得到的应用身份决定。

启动任务时不传 layout_data 就用这套配置 —— 把统一的水印、标签、布局策略配在这里，
就不必每次启动任务都重复传。

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
  水印类型 0默认,1无,2单排,3多排
</ResponseField>

<ResponseField name="window_tag_type" type="string">
  窗口标签位置 字母或组合:L左,R右,T上,B下,空表示不启用标签
</ResponseField>

<ResponseField name="created_at" type="integer">
  配置创建时间，秒级时间戳
  示例：`1718194666`
</ResponseField>

<ResponseField name="updated_at" type="integer">
  配置最后变更时间，秒级时间戳
  示例：`1718194705`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "app_id": "",
    "created_at": 1718194666,
    "layout": "",
    "updated_at": 1718194705,
    "watermark_type": 0,
    "window_tag_type": ""
  }
}
```

---

## 更新默认录制配置

`POST /server/v1/mcu/save-record-config`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

更新应用的默认录制配置。三个字段都可选，只传要改的。
改动只影响之后启动的新任务，进行中的任务不受影响。

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

## 录像任务列表

`POST /server/v1/mcu/list-task`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

分页查询录像任务列表。一次录制 = 一个任务，任务下可能有多个录像文件
（超过分片时长会滚动切段，中途中断续录也会另起一段）。

本接口只返回任务本身，要拿可播放的文件请用「录像任务详情」（内联全部文件与地址）
或「录像文件列表」。用 task_status 区分进行中与已结束，record_count 是已产出的文件数。

**请求参数**

<ParamField body="channel" type="string">
  频道，空表示不限（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="room_no" type="string">
  外部会议号，空表示不限（最大长度 50）
  示例：`818595664`
</ParamField>

<ParamField body="task_status" type="integer">
  任务状态，不传表示不限：0 待开始 1 进行中 2 待结束 3 异常结束 4 正常结束
  示例：`4`
</ParamField>

<ParamField body="title" type="string">
  录像标题，模糊匹配；空表示不限（最大长度 100）
  示例：`周会`
</ParamField>

<ParamField body="tag" type="string">
  标签，模糊匹配；空表示不限（最大长度 50）
  示例：`研发`
</ParamField>

<ParamField body="begin_at" type="integer">
  起始时间，秒级时间戳，按任务创建时间过滤；0 表示不限
  示例：`1718194666`
</ParamField>

<ParamField body="end_at" type="integer">
  终止时间，秒级时间戳；0 表示不限
  示例：`1718799878`
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
  "channel": "fire",
  "end_at": 1718799878,
  "page": 1,
  "per-page": 10,
  "room_no": "818595664",
  "tag": "研发",
  "task_status": 4,
  "title": "周会"
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

<ResponseField name="task_type" type="integer">
  任务类型 1录像 2合流 4录音 8直播流, 按位组合
</ResponseField>

<ResponseField name="task_status" type="integer">
  0待开始 1进行中 2待结束 3异常结束 4正常结束
</ResponseField>

<ResponseField name="err_desc" type="string">
  错误描述
</ResponseField>

<ResponseField name="began_at" type="integer">
  录制开始时间，秒级时间戳，0表示底层任务还没跑起来
  示例：`1718194666`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  录制结束时间，秒级时间戳，0表示未结束
  示例：`1718216393`
</ResponseField>

<ResponseField name="record_count" type="integer">
  录像文件数。一次录制超过分片时长(默认1小时)或中途中断续录都会多出文件
</ResponseField>

<ResponseField name="total_duration" type="integer">
  全部录像文件的总时长(秒)
  示例：`21727`
</ResponseField>

<ResponseField name="total_size" type="integer">
  全部录像文件的总字节
</ResponseField>

<ResponseField name="tags" type="string">
  录像标签 逗号隔开
</ResponseField>

<ResponseField name="records" type="array<object>">
  录像文件列表，仅任务详情返回；列表接口为null
  <Expandable title="元素字段">
    <ResponseField name="record_id" type="string">
      录像文件ID，取播放地址时用
    </ResponseField>

    <ResponseField name="task_id" type="string">
      所属录像任务ID
    </ResponseField>

    <ResponseField name="channel" type="string">
      频道
    </ResponseField>

    <ResponseField name="seq" type="integer">
      分片序号，从1开始，按它排序即播放顺序
    </ResponseField>

    <ResponseField name="vod_size" type="integer">
      录像大小(字节)
    </ResponseField>

    <ResponseField name="duration" type="integer">
      本片时长(秒)
      示例：`3600`
    </ResponseField>

    <ResponseField name="began_at" type="integer">
      本片开始时间，秒级时间戳，用于与业务侧的时间线对齐
      示例：`1718194666`
    </ResponseField>

    <ResponseField name="ended_at" type="integer">
      本片结束时间，秒级时间戳
      示例：`1718198266`
    </ResponseField>

    <ResponseField name="offset_ms" type="integer">
      相对任务开始的偏移(毫秒)，做多片连播的进度轴用这个
      示例：`7200000`
    </ResponseField>

    <ResponseField name="reason" type="integer">
      分片原因 0未知 1按时长切段 2中断后续录(与上一片间有空洞) 3任务结束收尾
    </ResponseField>

    <ResponseField name="width" type="integer">
      视频宽
      示例：`1280`
    </ResponseField>

    <ResponseField name="height" type="integer">
      视频高
      示例：`720`
    </ResponseField>

    <ResponseField name="fps" type="integer">
      帧率
      示例：`15`
    </ResponseField>

    <ResponseField name="codec" type="string">
      视频编码
      示例：`h264`
    </ResponseField>

    <ResponseField name="bitrate" type="integer">
      码率(bps)
    </ResponseField>

    <ResponseField name="is_done" type="boolean">
      是否已上传完成。false表示还在录制或上传中，取不到播放地址
    </ResponseField>

    <ResponseField name="addr" type="string">
      预签名播放地址，有效期2小时；仅任务详情返回，列表接口为空
    </ResponseField>

    <ResponseField name="created_at" type="integer">
      记录创建时间，秒级时间戳
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="created_at" type="integer">
  任务创建时间，秒级时间戳
  示例：`1718194666`
</ResponseField>

<ResponseField name="updated_at" type="integer">
  任务最后变更时间，秒级时间戳
  示例：`1718194705`
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
      "began_at": 1718194666,
      "channel": "",
      "created_at": 1718194666,
      "ended_at": 1718216393,
      "err_desc": "",
      "op_name": "",
      "op_uid": "",
      "record_count": 0,
      "records": [
        {
          "addr": "",
          "began_at": 1718194666,
          "bitrate": 0,
          "channel": "",
          "codec": "h264",
          "created_at": 0,
          "duration": 3600,
          "ended_at": 1718198266,
          "fps": 15,
          "height": 720,
          "is_done": false,
          "offset_ms": 7200000,
          "reason": 0,
          "record_id": "",
          "seq": 0,
          "task_id": "",
          "vod_size": 0,
          "width": 1280
        }
      ],
      "room_no": "",
      "tags": "",
      "task_id": "",
      "task_status": 0,
      "task_type": 0,
      "title": "",
      "total_duration": 21727,
      "total_size": 0,
      "updated_at": 1718194705
    }
  ]
}
```

---

## 录像任务详情

`POST /server/v1/mcu/detail`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

查询一次录制任务的详情：任务类型、状态、起止时间、总时长，以及**本次录制的全部录像文件**
（records 数组，含每个文件的播放地址、时长、起止时间与分片序号）。

一次录制会产出多个文件：超过分片时长（默认 1 小时）会滚动切段，录制中途中断后被续上
也会另起一段。要播完整场就按 records 里的 seq 顺序依次播放。

有 task_id 时按任务查；只传 channel 则取该频道最近一次的录像。
用 task_status 判断任务跑到哪一步了（0 待开始 1 进行中 2 待结束 3 异常结束 4 正常结束）。

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
  是否返回内网播放地址，适合纯内网部署或专线接入；默认返回外网地址
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

<ResponseField name="task_type" type="integer">
  任务类型 1录像 2合流 4录音 8直播流, 按位组合
</ResponseField>

<ResponseField name="task_status" type="integer">
  0待开始 1进行中 2待结束 3异常结束 4正常结束
</ResponseField>

<ResponseField name="err_desc" type="string">
  错误描述
</ResponseField>

<ResponseField name="began_at" type="integer">
  录制开始时间，秒级时间戳，0表示底层任务还没跑起来
  示例：`1718194666`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  录制结束时间，秒级时间戳，0表示未结束
  示例：`1718216393`
</ResponseField>

<ResponseField name="record_count" type="integer">
  录像文件数。一次录制超过分片时长(默认1小时)或中途中断续录都会多出文件
</ResponseField>

<ResponseField name="total_duration" type="integer">
  全部录像文件的总时长(秒)
  示例：`21727`
</ResponseField>

<ResponseField name="total_size" type="integer">
  全部录像文件的总字节
</ResponseField>

<ResponseField name="tags" type="string">
  录像标签 逗号隔开
</ResponseField>

<ResponseField name="records" type="array<object>">
  录像文件列表，仅任务详情返回；列表接口为null
  <Expandable title="元素字段">
    <ResponseField name="record_id" type="string">
      录像文件ID，取播放地址时用
    </ResponseField>

    <ResponseField name="task_id" type="string">
      所属录像任务ID
    </ResponseField>

    <ResponseField name="channel" type="string">
      频道
    </ResponseField>

    <ResponseField name="seq" type="integer">
      分片序号，从1开始，按它排序即播放顺序
    </ResponseField>

    <ResponseField name="vod_size" type="integer">
      录像大小(字节)
    </ResponseField>

    <ResponseField name="duration" type="integer">
      本片时长(秒)
      示例：`3600`
    </ResponseField>

    <ResponseField name="began_at" type="integer">
      本片开始时间，秒级时间戳，用于与业务侧的时间线对齐
      示例：`1718194666`
    </ResponseField>

    <ResponseField name="ended_at" type="integer">
      本片结束时间，秒级时间戳
      示例：`1718198266`
    </ResponseField>

    <ResponseField name="offset_ms" type="integer">
      相对任务开始的偏移(毫秒)，做多片连播的进度轴用这个
      示例：`7200000`
    </ResponseField>

    <ResponseField name="reason" type="integer">
      分片原因 0未知 1按时长切段 2中断后续录(与上一片间有空洞) 3任务结束收尾
    </ResponseField>

    <ResponseField name="width" type="integer">
      视频宽
      示例：`1280`
    </ResponseField>

    <ResponseField name="height" type="integer">
      视频高
      示例：`720`
    </ResponseField>

    <ResponseField name="fps" type="integer">
      帧率
      示例：`15`
    </ResponseField>

    <ResponseField name="codec" type="string">
      视频编码
      示例：`h264`
    </ResponseField>

    <ResponseField name="bitrate" type="integer">
      码率(bps)
    </ResponseField>

    <ResponseField name="is_done" type="boolean">
      是否已上传完成。false表示还在录制或上传中，取不到播放地址
    </ResponseField>

    <ResponseField name="addr" type="string">
      预签名播放地址，有效期2小时；仅任务详情返回，列表接口为空
    </ResponseField>

    <ResponseField name="created_at" type="integer">
      记录创建时间，秒级时间戳
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="created_at" type="integer">
  任务创建时间，秒级时间戳
  示例：`1718194666`
</ResponseField>

<ResponseField name="updated_at" type="integer">
  任务最后变更时间，秒级时间戳
  示例：`1718194705`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "began_at": 1718194666,
    "channel": "",
    "created_at": 1718194666,
    "ended_at": 1718216393,
    "err_desc": "",
    "op_name": "",
    "op_uid": "",
    "record_count": 0,
    "records": [
      {
        "addr": "",
        "began_at": 1718194666,
        "bitrate": 0,
        "channel": "",
        "codec": "h264",
        "created_at": 0,
        "duration": 3600,
        "ended_at": 1718198266,
        "fps": 15,
        "height": 720,
        "is_done": false,
        "offset_ms": 7200000,
        "reason": 0,
        "record_id": "",
        "seq": 0,
        "task_id": "",
        "vod_size": 0,
        "width": 1280
      }
    ],
    "room_no": "",
    "tags": "",
    "task_id": "",
    "task_status": 0,
    "task_type": 0,
    "title": "",
    "total_duration": 21727,
    "total_size": 0,
    "updated_at": 1718194705
  }
}
```

---

## 录像文件列表

`POST /server/v1/mcu/list-record`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

分页查询录像文件，一条就是一次录制产出的一个文件（分片）。

按 seq 升序即为播放顺序；offset_ms 是相对任务开始的偏移，做多片连播的进度轴用它。
reason=2 表示这一片与上一片之间存在时间空洞（录制曾中断后续录），连播时要留意。

拿到列表后用「批量获取录像文件播放地址」一次性取回本页地址，比逐条取快得多。

**请求参数**

<ParamField body="task_id" type="string">
  录像任务ID，只看某一次录制的文件时传；空表示不限
  示例：`sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  频道，空表示不限（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
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
  "channel": "fire",
  "page": 1,
  "per-page": 10,
  "task_id": "sxjgwy"
}
```

**响应参数**

<ResponseField name="record_id" type="string">
  录像文件ID，取播放地址时用
</ResponseField>

<ResponseField name="task_id" type="string">
  所属录像任务ID
</ResponseField>

<ResponseField name="channel" type="string">
  频道
</ResponseField>

<ResponseField name="seq" type="integer">
  分片序号，从1开始，按它排序即播放顺序
</ResponseField>

<ResponseField name="vod_size" type="integer">
  录像大小(字节)
</ResponseField>

<ResponseField name="duration" type="integer">
  本片时长(秒)
  示例：`3600`
</ResponseField>

<ResponseField name="began_at" type="integer">
  本片开始时间，秒级时间戳，用于与业务侧的时间线对齐
  示例：`1718194666`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  本片结束时间，秒级时间戳
  示例：`1718198266`
</ResponseField>

<ResponseField name="offset_ms" type="integer">
  相对任务开始的偏移(毫秒)，做多片连播的进度轴用这个
  示例：`7200000`
</ResponseField>

<ResponseField name="reason" type="integer">
  分片原因 0未知 1按时长切段 2中断后续录(与上一片间有空洞) 3任务结束收尾
</ResponseField>

<ResponseField name="width" type="integer">
  视频宽
  示例：`1280`
</ResponseField>

<ResponseField name="height" type="integer">
  视频高
  示例：`720`
</ResponseField>

<ResponseField name="fps" type="integer">
  帧率
  示例：`15`
</ResponseField>

<ResponseField name="codec" type="string">
  视频编码
  示例：`h264`
</ResponseField>

<ResponseField name="bitrate" type="integer">
  码率(bps)
</ResponseField>

<ResponseField name="is_done" type="boolean">
  是否已上传完成。false表示还在录制或上传中，取不到播放地址
</ResponseField>

<ResponseField name="addr" type="string">
  预签名播放地址，有效期2小时；仅任务详情返回，列表接口为空
</ResponseField>

<ResponseField name="created_at" type="integer">
  记录创建时间，秒级时间戳
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
      "addr": "",
      "began_at": 1718194666,
      "bitrate": 0,
      "channel": "",
      "codec": "h264",
      "created_at": 0,
      "duration": 3600,
      "ended_at": 1718198266,
      "fps": 15,
      "height": 720,
      "is_done": false,
      "offset_ms": 7200000,
      "reason": 0,
      "record_id": "",
      "seq": 0,
      "task_id": "",
      "vod_size": 0,
      "width": 1280
    }
  ]
}
```

---

## 获取单个录像文件的播放地址

`POST /server/v1/mcu/vod-url`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

获取单个录像文件的回放地址。文件必须已上传完成，正在录制或上传中的取不到地址。
地址有有效期（2 小时），不要长期缓存或存进业务库，每次播放前重新获取。

**请求参数**

<ParamField body="record_id" type="string" required>
  录像文件ID，取自任务详情或录像文件列表
  示例：`rc3p9w`
</ParamField>

<ParamField body="is_lan" type="boolean">
  是否返回内网地址，适合纯内网部署或专线接入；默认返回外网地址
</ParamField>


请求示例：

```json
{
  "is_lan": false,
  "record_id": "rc3p9w"
}
```

**响应参数**

<ResponseField name="record_id" type="string">
  录像文件ID
</ResponseField>

<ResponseField name="addr" type="string">
  预签名播放地址，有效期2小时
</ResponseField>

<ResponseField name="size" type="integer">
  录像大小(字节)
</ResponseField>

<ResponseField name="duration" type="integer">
  本片时长(秒)
</ResponseField>

<ResponseField name="began_at" type="integer">
  本片开始时间，秒级时间戳
</ResponseField>

<ResponseField name="offset_ms" type="integer">
  相对任务开始的偏移(毫秒)
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "addr": "",
    "began_at": 0,
    "duration": 0,
    "offset_ms": 0,
    "record_id": "",
    "size": 0
  }
}
```

---

## 批量获取录像文件播放地址

`POST /server/v1/mcu/vod-url/batch`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

批量获取录像文件的回放地址，一次最多 50 个，适合整场连播时一次性取全。

单个文件签发失败（如已被清理）时该条 addr 为空，不影响其余条目。

**请求参数**

<ParamField body="record_ids" type="array<string>" required>
  录像文件ID列表，单次最多 50 个（最大长度 50）
  示例：`["rc3p9w","rc3p9x"]`
</ParamField>

<ParamField body="is_lan" type="boolean">
  是否返回内网地址，适合纯内网部署或专线接入；默认返回外网地址
</ParamField>


请求示例：

```json
{
  "is_lan": false,
  "record_ids": [
    "rc3p9w",
    "rc3p9x"
  ]
}
```

**响应参数**

<ResponseField name="record_id" type="string">
  录像文件ID
</ResponseField>

<ResponseField name="addr" type="string">
  预签名播放地址，有效期2小时
</ResponseField>

<ResponseField name="size" type="integer">
  录像大小(字节)
</ResponseField>

<ResponseField name="duration" type="integer">
  本片时长(秒)
</ResponseField>

<ResponseField name="began_at" type="integer">
  本片开始时间，秒级时间戳
</ResponseField>

<ResponseField name="offset_ms" type="integer">
  相对任务开始的偏移(毫秒)
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "addr": "",
      "began_at": 0,
      "duration": 0,
      "offset_ms": 0,
      "record_id": "",
      "size": 0
    }
  ]
}
```

---

## 删除录像任务

`POST /server/v1/mcu/del-task`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

删除录像任务，其下全部录像文件一并删除，删除后不再出现在列表与详情中。

只传 channel 不传 task_id 时，该频道下**所有**含录像的任务会被一起删掉，
要删指定的一次录制请传 task_id。

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
  是否返回内网播放地址，适合纯内网部署或专线接入；默认返回外网地址
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

`data` 为 null

响应示例：

```json
{
  "code": 0,
  "data": null
}
```

---

## 删除单个录像文件

`POST /server/v1/mcu/del-record`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

删除单个录像文件，同一次录制的其他文件不受影响。

**请求参数**

<ParamField body="record_id" type="string" required>
  录像文件ID
  示例：`rc3p9w`
</ParamField>


请求示例：

```json
{
  "record_id": "rc3p9w"
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

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

启动服务端的录制、合流或直播任务。同一频道对同一类型只有一个进行中的任务：
重复调用不新建，而是按传入参数更新已有任务。

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

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

停止进行中的录制/合流/直播任务。录像文件在任务停止后才完成转码，随后才能取到播放地址。
频道销毁时进行中的任务会自动停止，不必先手动调用。

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

## 修改录像任务的标题与标签

`POST /server/v1/mcu/update-task`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

修改录像任务的标题与标签，用于归档整理，不影响录像文件本身。
标题与标签都可以用录像任务列表的 search 检索到。

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

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

获取直播拉流地址，一次返回 rtmp / flv / hls 三种协议，按你的播放端选用。

与录像回放不同，直播地址在任务**进行中**就能取到 —— 前提是启动任务时
task_type 带了直播位（8）。地址有有效期，不要长期缓存。

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
  是否返回内网播放地址，适合纯内网部署或专线接入；默认返回外网地址
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

<ResponseField name="rtmp" type="string">
  RTMP 拉流地址，延迟最低，适合需要低延迟的播放端
</ResponseField>

<ResponseField name="flv" type="string">
  HTTP-FLV 拉流地址，Web 端常用
</ResponseField>

<ResponseField name="hls" type="string">
  HLS(m3u8) 拉流地址，兼容性最好，延迟相对高
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

