---
title: "语音录制"
description: "按说话人分轨的旁路录音：按一次讲话切段，段级查询与播放；整场混音录制见「云录制与直播」"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 rtc-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 开始语音录制

`POST /server/v1/talkrec/start`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

对频道开启语音录制。服务端以观众身份入会旁路录制，按说话人分轨、由媒体帧自动分段，
把音频切成「一次讲话 = 一段录音」，每段单独成文件、带讲话人与起止时间。

+ 频道需已开启，未开启返回「频道未开启」
+ 同一频道同时只跑一路录音：重复调用返回已有任务的 task_id，不会重复入会
+ 客户端无需改造：分段由服务端按语音/静音自动判定，不依赖客户端上报任何状态

启动是异步的：接口返回只表示已受理，录音网关入会成功后任务才转为进行中。
用「语音录制任务详情」的 task_status 观察，或接 `talkrec_task` 事件回调。

**请求参数**

<ParamField body="channel" type="string" required>
  频道（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="title" type="string">
  频道标题，仅用于列表与后台展示（最大长度 100）
  示例：`三号线抢修对讲`
</ParamField>

<ParamField body="op_uid" type="string">
  任务发起人ID。你自己业务的用户ID，仅用于回查，RTC 侧不校验（最大长度 100）
  示例：`1001`
</ParamField>

<ParamField body="op_name" type="string">
  任务发起人名（最大长度 100）
  示例：`张三`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "op_name": "张三",
  "op_uid": "1001",
  "title": "三号线抢修对讲"
}
```

**响应参数**

<ResponseField name="task_id" type="string">
  本次录音任务的 ID，停止任务、查询详情、按任务筛录音段都用它
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

## 停止语音录制

`POST /server/v1/talkrec/stop`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

停止语音录制。停止时服务端会把所有还没结束的讲话闭合成完整录音段，
因此最后几段可能在本接口返回后才出现在录音段列表里。

已产生的录音段不会被删除，仍可查询与播放。

**请求参数**

<ParamField body="task_id" type="string">
  任务ID
  示例：`sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
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

## 语音录制任务详情

`POST /server/v1/talkrec/detail`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

查询一路语音录制任务的详情：状态、起止时间，以及已产出的录音段数与总大小。

有 task_id 时按任务查；只传 channel 则优先返回该频道未结束的那一路，
都结束了则返回最近一路；该频道从未录过音时 `data` 为 null。

用 task_status 判断任务跑到哪一步了（0 待开始 1 进行中 3 异常结束 4 正常结束），
异常时 err_desc 是原因。

**请求参数**

<ParamField body="task_id" type="string">
  任务ID
  示例：`sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  频道(无TaskId时必填)（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
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

<ResponseField name="channel" type="string">
  频道
  示例：`fire`
</ResponseField>

<ResponseField name="title" type="string">
  频道标题
</ResponseField>

<ResponseField name="op_uid" type="string">
  任务发起人ID
</ResponseField>

<ResponseField name="op_name" type="string">
  任务发起人名
</ResponseField>

<ResponseField name="task_status" type="integer">
  任务状态 0待开始 1进行中 3异常结束 4正常结束
</ResponseField>

<ResponseField name="err_desc" type="string">
  错误描述
</ResponseField>

<ResponseField name="began_at" type="integer">
  任务开始时间，秒级时间戳
  示例：`1718194666`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  任务结束时间，秒级时间戳，0表示未结束
</ResponseField>

<ResponseField name="seg_count" type="integer">
  已产出的录音段数
</ResponseField>

<ResponseField name="total_size" type="integer">
  录音总字节
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
    "channel": "fire",
    "created_at": 1718194666,
    "ended_at": 0,
    "err_desc": "",
    "op_name": "",
    "op_uid": "",
    "seg_count": 0,
    "task_id": "",
    "task_status": 0,
    "title": "",
    "total_size": 0,
    "updated_at": 1718194705
  }
}
```

---

## 语音录制段列表

`POST /server/v1/talkrec/list-record`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

分页查询录音段，一条就是一次讲话。

对讲场景单段通常只有几秒，一个活跃频道一天可以产生上万段，
**务必带上 task_id 或 channel 缩小范围**，不要不加条件地全量翻页。

拿到列表后用「批量获取语音录制段播放地址」一次性取回本页的播放地址，
比逐条取快得多；单页控制在 50 条以内正好是批量接口的上限。

**请求参数**

<ParamField body="task_id" type="string">
  录音任务ID，只看某一路录音的段时传；空表示不限
  示例：`sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  频道，空表示不限（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="uid" type="string">
  讲话人ID，空表示不限（最大长度 100）
  示例：`1001`
</ParamField>

<ParamField body="begin_at" type="integer">
  起始时间，秒级时间戳，按讲话开始时间过滤；0 表示不限
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
  排序（可排序字段：began_at、duration_ms、vod_size）
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
  "search": [
    ""
  ],
  "sort": "",
  "task_id": "sxjgwy",
  "uid": "1001"
}
```

**响应参数**

<ResponseField name="record_id" type="string">
  录音段ID，取播放地址时用
</ResponseField>

<ResponseField name="task_id" type="string">
  所属录音任务ID
</ResponseField>

<ResponseField name="channel" type="string">
  频道
  示例：`fire`
</ResponseField>

<ResponseField name="uid" type="string">
  讲话人ID
  示例：`1001`
</ResponseField>

<ResponseField name="name" type="string">
  讲话人会中昵称
  示例：`张三`
</ResponseField>

<ResponseField name="vod_size" type="integer">
  录音大小(字节)
</ResponseField>

<ResponseField name="duration_ms" type="integer">
  录音时长(毫秒)
  示例：`5200`
</ResponseField>

<ResponseField name="began_at" type="integer">
  讲话开始时间，秒级时间戳
  示例：`1718194666`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  讲话结束时间，秒级时间戳
  示例：`1718194671`
</ResponseField>

<ResponseField name="codec" type="string">
  音频编码
  示例：`opus`
</ResponseField>

<ResponseField name="sample_rate" type="integer">
  采样率
  示例：`48000`
</ResponseField>

<ResponseField name="end_reason" type="integer">
  闭段原因 0未知 1正常松手 2超时切段 3用户离开 4任务停止 5空闲兜底
</ResponseField>

<ResponseField name="created_at" type="integer">
  记录创建时间，秒级时间戳
  示例：`1718194672`
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
      "channel": "fire",
      "codec": "opus",
      "created_at": 1718194672,
      "duration_ms": 5200,
      "end_reason": 0,
      "ended_at": 1718194671,
      "name": "张三",
      "record_id": "",
      "sample_rate": 48000,
      "task_id": "",
      "uid": "1001",
      "vod_size": 0
    }
  ]
}
```

---

## 获取语音录制段播放地址

`POST /server/v1/talkrec/vod-url`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

获取单个录音段的播放地址，可直接用 `<audio>` 播放（Opus/Ogg 格式）。

地址有有效期（2 小时），不要长期缓存或存进业务库，每次播放前重新获取。

**请求参数**

<ParamField body="record_id" type="string" required>
  录音段ID，取自录音段列表
  示例：`sxjgwy`
</ParamField>

<ParamField body="is_lan" type="boolean">
  是否返回内网地址，适合纯内网部署或专线接入；默认返回外网地址
</ParamField>


请求示例：

```json
{
  "is_lan": false,
  "record_id": "sxjgwy"
}
```

**响应参数**

<ResponseField name="record_id" type="string">
  录音段ID
</ResponseField>

<ResponseField name="addr" type="string">
  预签名播放地址，有效期2小时
</ResponseField>

<ResponseField name="vod_size" type="integer">
  录音大小(字节)
</ResponseField>

<ResponseField name="duration_ms" type="integer">
  录音时长(毫秒)
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "addr": "",
    "duration_ms": 0,
    "record_id": "",
    "vod_size": 0
  }
}
```

---

## 批量获取语音录制段播放地址

`POST /server/v1/talkrec/vod-url/batch`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

批量获取录音段播放地址，供录音段列表一次性取回本页所有地址。单次最多 50 个 ID。

与单条接口的差别：这里不会因为其中一条取不到就整体失败 —— 取不到的那条
`addr` 为空字符串（如文件已被清理），其余照常返回。

**请求参数**

<ParamField body="record_ids" type="array<string>" required>
  录音段ID列表，单次最多 50 个（最大长度 50）
  示例：`["sxjgwy","sxjgwz"]`
</ParamField>

<ParamField body="is_lan" type="boolean">
  是否返回内网地址，适合纯内网部署或专线接入；默认返回外网地址
</ParamField>


请求示例：

```json
{
  "is_lan": false,
  "record_ids": [
    "sxjgwy",
    "sxjgwz"
  ]
}
```

**响应参数**

<ResponseField name="record_id" type="string">
  录音段ID
</ResponseField>

<ResponseField name="addr" type="string">
  预签名播放地址，有效期2小时
</ResponseField>

<ResponseField name="vod_size" type="integer">
  录音大小(字节)
</ResponseField>

<ResponseField name="duration_ms" type="integer">
  录音时长(毫秒)
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "addr": "",
      "duration_ms": 0,
      "record_id": "",
      "vod_size": 0
    }
  ]
}
```

---

## 删除语音录制段

`POST /server/v1/talkrec/del-record`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

删除录音段，删除后不再出现在录音段列表中，播放地址也取不到了。
录音文件本身由服务端的定时任务异步回收，不影响本接口的返回。

**请求参数**

<ParamField body="record_id" type="string" required>
  录音段ID，取自录音段列表
  示例：`sxjgwy`
</ParamField>


请求示例：

```json
{
  "record_id": "sxjgwy"
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

