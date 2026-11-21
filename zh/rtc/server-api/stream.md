---
title: "媒体输出"
description: "拉流地址（HTTP-FLV / RTSP）与推流任务（RTMP / RTMPS）：画面取合成画面或任意一人，声音取房间混音或任意一人，可自由组合"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 rtc-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 申请拉流地址

`POST /server/v1/stream/pull-url`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

申请频道内音视频的拉流地址（HTTP-FLV 或 RTSP）。画面与声音各自选来源：
画面取房间合成画面、某个用户的某路视频或不要；声音取房间混音、某个用户的某路音频或不要，默认跟随画面。
例如「主讲人画面 + 房间混音」即 video=user、video_uid=主讲人、audio=mix。

- 用到合成画面或房间混音时，频道内须有进行中的合流任务（mcu/start 的 task_type 含 2），否则返回错误码 1073
- flv：视频须为 H264（不转码，发布端使用 VP8 时拉不到画面，请让发布端使用 H264），音频转成 AAC
- rtsp：只支持 RTSP over TCP（拉流端需用 TCP 方式，如 ffplay 加 `-rtsp_transport tcp`）；视频原样直通（H264 或 VP8），
音频默认转成 AAC，传 rtsp_audio=opus 可原样直通 Opus、省去服务端转码
- 地址自带签名，有效期内可被多个拉流端反复拉取；过期后新的拉流请求会被拒绝，已在播放的不受影响
- 有人来拉时才订阅，最后一个拉流端断开后自动退订，不拉不占资源；无需调用停止接口
- 不校验频道是否开启、用户是否在线，地址可提前生成；拉流时来源还没发布，拉流端会收到 404，需重试
- 用户中途离开再回来，拉流不断，中间是一段空白

实际有效期以返回的 expire_at 为准（服务端配置的上限可能小于请求值）。

**请求参数**

<ParamField body="channel" type="string" required>
  频道（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="protocol" type="string" required>
  拉流协议：flv（HTTP-FLV）、rtsp（RTSP over TCP）
  示例：`flv`
</ParamField>

<ParamField body="video" type="string" required>
  画面来源：mcu 房间合成画面（频道内须有进行中的合流任务）、user 某个用户的画面（配 video_uid）、none 不要画面
  示例：`mcu`
</ParamField>

<ParamField body="video_uid" type="string">
  video 为 user 时必填：取哪个用户的画面（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>

<ParamField body="video_desc" type="string">
  video 为 user 时可选：该用户同时发布多路视频（如摄像头与屏幕共享）时指定其中一路（按轨道描述精确匹配），不传取先到的那一路（最大长度 50）
  示例：`camera`
</ParamField>

<ParamField body="audio" type="string">
  声音来源：auto 跟随画面（默认；合成画面配房间混音，单人画面配该用户本人的声音，不要画面时不能用 auto）、 mix 房间混音（频道内须有进行中的合流任务）、user 某个用户的声音（配 audio_uid）、none 不要声音。画面与声音不能都是 none
  示例：`auto`
</ParamField>

<ParamField body="audio_uid" type="string">
  audio 为 user 时必填：取哪个用户的声音（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1002`
</ParamField>

<ParamField body="audio_desc" type="string">
  该用户发布多路音频时指定其中一路（按轨道描述精确匹配），不传取第一路；audio 为 user 或 auto 跟随单人画面时生效（最大长度 50）
  示例：`mic`
</ParamField>

<ParamField body="expire" type="integer">
  地址有效期（秒），不传时默认 24 小时，最长一天
  示例：`86400`
</ParamField>

<ParamField body="rtsp_audio" type="string">
  RTSP 的音频编码，仅 protocol 为 rtsp 时生效：aac（默认，兼容 NVR、监控平台）、opus（原样直通，省服务端转码）
  示例：`aac`
</ParamField>


请求示例：

```json
{
  "audio": "auto",
  "audio_desc": "mic",
  "audio_uid": "1002",
  "channel": "fire",
  "expire": 86400,
  "protocol": "flv",
  "rtsp_audio": "aac",
  "video": "mcu",
  "video_desc": "camera",
  "video_uid": "1001"
}
```

**响应参数**

<ResponseField name="url" type="string">
  拉流地址，自带签名，有效期内可被多个拉流端反复拉取
  示例：`http://1.2.3.4:8080/f/eyJhcHBpZCI6....flv`
</ResponseField>

<ResponseField name="expire_at" type="integer">
  地址过期时间，秒级时间戳；过期后新的拉流请求会被拒绝，已在播放的不受影响
  示例：`1718198266`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "expire_at": 1718198266,
    "url": "http://1.2.3.4:8080/f/eyJhcHBpZCI6....flv"
  }
}
```

---

## 开始推流

`POST /server/v1/stream/push/start`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

开始推流：把频道内选定的画面与声音推到你的 RTMP 直播间（支持 rtmp:// 与 rtmps://），返回 push_id。
来源参数与申请拉流地址相同，一个频道可以同时有多路推流（如合成画面推视频号、某位嘉宾的单人画面推另一个平台）。

+ 频道须已开启；频道销毁时其下全部推流自动停止
+ 同一频道对同一推流地址重复调用不会另起一路：来源不变时直接返回已有的 push_id，来源变了则按新来源更新这一路
+ 来源暂时不存在（如合流任务还没开、要推的人还没发布）时推流处于 waiting，不算失败，来源出现后自动开推
+ 推流断线会自动重连；持续失败时经 MCU 告警回调（mcu_alarm）通知：task_type 为 0 表示这是推流告警，此时 task_id 是 push_id（与 MCU 任务 ID 格式相同但不是 MCU 任务，不要拿去调 mcu/detail 等 mcu/* 接口）
+ 推流状态用推流任务列表查；没有可用的推流服务时返回错误码 1072，推流地址不合格返回 1075，推流服务拒绝本次推流时返回 1076

**请求参数**

<ParamField body="channel" type="string" required>
  频道，须已开启（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="push_url" type="string" required>
  推流地址，支持 rtmp:// 与 rtmps://，须带推流码（如 rtmp://host/app/ 这类流名为空的地址会被拒绝）（最大长度 1024）
  示例：`rtmp://live.example.com/app/stream_key`
</ParamField>

<ParamField body="video" type="string" required>
  画面来源：mcu 房间合成画面（频道内须有进行中的合流任务）、user 某个用户的画面（配 video_uid）、none 不要画面
  示例：`mcu`
</ParamField>

<ParamField body="video_uid" type="string">
  video 为 user 时必填：取哪个用户的画面（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>

<ParamField body="video_desc" type="string">
  video 为 user 时可选：该用户同时发布多路视频（如摄像头与屏幕共享）时指定其中一路（按轨道描述精确匹配），不传取先到的那一路（最大长度 50）
  示例：`camera`
</ParamField>

<ParamField body="audio" type="string">
  声音来源：auto 跟随画面（默认；合成画面配房间混音，单人画面配该用户本人的声音，不要画面时不能用 auto）、 mix 房间混音（频道内须有进行中的合流任务）、user 某个用户的声音（配 audio_uid）、none 不要声音。画面与声音不能都是 none
  示例：`auto`
</ParamField>

<ParamField body="audio_uid" type="string">
  audio 为 user 时必填：取哪个用户的声音（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1002`
</ParamField>

<ParamField body="audio_desc" type="string">
  该用户发布多路音频时指定其中一路（按轨道描述精确匹配），不传取第一路；audio 为 user 或 auto 跟随单人画面时生效（最大长度 50）
  示例：`mic`
</ParamField>


请求示例：

```json
{
  "audio": "auto",
  "audio_desc": "mic",
  "audio_uid": "1002",
  "channel": "fire",
  "push_url": "rtmp://live.example.com/app/stream_key",
  "video": "mcu",
  "video_desc": "camera",
  "video_uid": "1001"
}
```

**响应参数**

<ResponseField name="push_id" type="string">
  推流任务ID，停止推流、查询推流状态都用它
  示例：`p7k2xq`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "push_id": "p7k2xq"
  }
}
```

---

## 停止推流

`POST /server/v1/stream/push/stop`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

停止推流。已停止的推流再次停止视为成功；push_id 不存在返回错误码 1074。

**请求参数**

<ParamField body="push_id" type="string" required>
  推流任务ID，取自开始推流的返回
  示例：`p7k2xq`
</ParamField>


请求示例：

```json
{
  "push_id": "p7k2xq"
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

## 推流任务列表

`POST /server/v1/stream/push/list`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

查询频道的推流任务：来源、脱敏后的推流地址、推流状态与最近一次错误，按创建时间倒序。
不传 push_id 时返回进行中的与最近一天内停止的推流。

状态 status：waiting 等待来源、connecting 正在连接直播平台、publishing 推流中、
retrying 推流失败正在重试（原因见 err）、stopped 已停止。

**请求参数**

<ParamField body="channel" type="string" required>
  频道（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="push_id" type="string">
  推流任务ID，只看某一路时传；不传返回该频道进行中的与最近一天内停止的推流
  示例：`p7k2xq`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "push_id": "p7k2xq"
}
```

**响应参数**

<ResponseField name="push_id" type="string">
  推流任务ID
  示例：`p7k2xq`
</ResponseField>

<ResponseField name="channel" type="string">
  频道
  示例：`fire`
</ResponseField>

<ResponseField name="video" type="string">
  画面来源：mcu 合成画面、user 某个用户、none 不要画面
  示例：`mcu`
</ResponseField>

<ResponseField name="video_uid" type="string">
  video 为 user 时取谁的画面
  示例：`1001`
</ResponseField>

<ResponseField name="video_desc" type="string">
  video 为 user 时该用户的哪路视频，空表示先到的那路
  示例：`camera`
</ResponseField>

<ResponseField name="audio" type="string">
  声音来源：auto 跟随画面、mix 房间混音、user 某个用户、none 不要声音
  示例：`auto`
</ResponseField>

<ResponseField name="audio_uid" type="string">
  audio 为 user 时取谁的声音
  示例：`1002`
</ResponseField>

<ResponseField name="audio_desc" type="string">
  该用户的哪路音频，空表示第一路
  示例：`mic`
</ResponseField>

<ResponseField name="push_url" type="string">
  推流地址，推流码已脱敏（只保留协议、服务器与第一段路径）
  示例：`rtmp://live.example.com/app/***`
</ResponseField>

<ResponseField name="status" type="string">
  推流状态：waiting 等待来源（如合成任务还没开、要推的人还没发布，来源出现后自动开推，不算失败）、 connecting 正在连接直播平台、publishing 推流中、retrying 推流失败正在重试（原因见 err）、stopped 已停止
  示例：`publishing`
</ResponseField>

<ResponseField name="err" type="string">
  最近一次错误，正常时为空
  示例：`connection refused`
</ResponseField>

<ResponseField name="created_at" type="integer">
  创建时间，秒级时间戳
  示例：`1718194666`
</ResponseField>

<ResponseField name="started_at" type="integer">
  开始推流时间（首次交给推流服务的时刻），秒级时间戳；0 表示还没开始
  示例：`1718194667`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  停止时间，秒级时间戳；0 表示未停止
  示例：`1718198266`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "audio": "auto",
      "audio_desc": "mic",
      "audio_uid": "1002",
      "channel": "fire",
      "created_at": 1718194666,
      "ended_at": 1718198266,
      "err": "connection refused",
      "push_id": "p7k2xq",
      "push_url": "rtmp://live.example.com/app/***",
      "started_at": 1718194667,
      "status": "publishing",
      "video": "mcu",
      "video_desc": "camera",
      "video_uid": "1001"
    }
  ]
}
```

---

