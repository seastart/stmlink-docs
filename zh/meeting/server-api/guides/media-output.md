---
title: "媒体输出接入指南"
description: "把会议里的画面和声音送出去：HTTP-FLV / RTSP 拉流地址与 RTMP / RTMPS 推流任务。画面取合成画面或任意一人、声音取会议混音或任意一人，可自由组合；含合流任务依赖、协议限制、推流状态与告警、旧接口迁移"
---

本页讲会议层媒体输出的整体玩法。单个接口的参数与返回结构见[媒体输出](/zh/meeting/server-api/stream)。

<Note>会议层的媒体输出是对 SRTC 同名接口的透传，能力、协议限制和错误码与 SRTC 完全一致，详细说明见 SRTC 的[媒体输出接入指南](/zh/rtc/server-api/guides/media-output)。本页只讲会议层的差异和常用做法。</Note>

## 一套来源，两种输出

| 输出 | 接口 | 协议 | 适合 |
| --- | --- | --- | --- |
| 拉流 | [申请拉流地址](/zh/meeting/server-api/stream) | HTTP-FLV、RTSP | 网页播放器、业务系统、NVR / 监控平台自己来拉 |
| 推流 | [开始推流](/zh/meeting/server-api/stream#开始推流) | RTMP、RTMPS | 推到视频号、抖音、自建 CDN 等直播平台 |

画面和声音各自选来源，拉流推流通用：

| 参数 | 取值 | 说明 |
| --- | --- | --- |
| `video` | `mcu` / `user` / `none`，必填 | `mcu` 会议合成画面；`user` 某个人的画面（配 `video_uid`，填会中用户 ID）；`none` 不要画面 |
| `video_desc` | 轨道描述 | 这个人同时发布多路视频（如摄像头和屏幕共享）时指定其中一路，不传取先到的那一路 |
| `audio` | `auto`（默认）/ `mix` / `user` / `none` | `auto` 跟随画面：合成画面配会议混音、单人画面配本人声音，不要画面时不能用；`mix` 会议混音；`user` 某个人的声音（配 `audio_uid`） |
| `audio_desc` | 轨道描述 | 这个人发布多路音频时指定其中一路，不传取第一路 |

`video` 和 `audio` 不能同时是 `none`；画面和声音可以来自不同的人，例如「主讲人画面 + 会议混音」即 `video=user`、`video_uid=主讲人`、`audio=mix`。

## 与 SRTC 的差异

+ 用 `meeting_id` 指定会议，代替 SRTC 的 `channel`
+ `video_uid` / `audio_uid` 填会中用户 ID
+ **停止推流要同时传 `meeting_id` 和 `push_id`**，推流不属于这场会议时返回 `1074`
+ 开始推流要求会议进行中（有人在会）；会议结束、所有人离开后其下全部推流自动停止
+ 申请拉流地址、开始推流时 `meeting_id` 对应的会议不存在返回 `2101`

## 合成画面和混音依赖合流任务

用到合成画面（`video=mcu`）或会议混音时，会议须有**进行中的合流任务**（`task_type` 含 `2`）：

+ **合成模式的会议**进会后服务端自动起合流任务，可以直接用
+ **普通会议**要先[开始录制任务](/zh/meeting/server-api/mcu)，`task_type` 带 `2`（如 `2` 只合流、`3` 录像+合流）。画面布局在那里配，见[云录制与合流接入指南](/zh/meeting/server-api/guides/recording)

没有合流任务时，拉流直接返回 `1073`；推流允许先建，状态停在 `waiting`，合流任务起来后自动开推。
只用单人画面和单人声音时不依赖合流任务。

## 拉流与推流的要点

+ **HTTP-FLV** 视频只支持 H264、不转码（发布端用 VP8 时拉不到画面；合成画面恒为 H264），音频转成 AAC
+ **RTSP** 视频原样直通（H264 / H265 / VP8），音频默认转 AAC，`rtsp_audio=opus` 可原样直通；只支持 RTSP over TCP
+ 拉流地址自带签名，默认 24 小时有效，有人来拉才订阅、没人拉不占资源，不需要停止
+ **推流**一个会议可以同时推多路；同一会议对同一推流地址重复开始返回已有的 `push_id`（来源变了按新来源更新）
+ 推流状态 `waiting` / `connecting` / `publishing` / `retrying` / `stopped`，用[推流任务列表](/zh/meeting/server-api/stream#推流任务列表)查
+ 纯音频（`video=none`）有局限：HTTP-FLV 断档不补静音；很多直播平台不接纯音频推流

## 推流失败告警

推流持续失败（一直重试约 90 秒）时，经 [`mcu_alarm` 回调](/zh/meeting/server-api/guides/callbacks)通知：
**`task_type` 为 `0` 表示推流告警，此时 `task_id` 是 `push_id`**，不是录制任务，不要拿去调 `mcu/*` 接口。
告警不代表推流已停止，以推流列表的 `status` 为准。

## 从旧用法迁移

旧的直播接口与用法已删除，没有兼容期，请把调用方改到新接口：

| 旧用法 | 新用法 |
| --- | --- |
| `mcu/start` 的 `layout_data.push_url` / `push_audio*` | 已删除。改用 `stream/push/start`，`video=mcu`，`audio` 等同原 `push_audio`；停推用 `stream/push/stop` |
| `task_type` 含 `8`（直播流） | 改成 `2`（合流），如 `9` → `3`；传含 `8` 的值会报错（`mcu/start`、`mcu/stop` 都是） |
| `mcu/live-url` | 已删除。改用 `stream/pull-url`（`protocol=flv`、`video=mcu`），返回 `url` 与 `expire_at`；没有进行中的合流任务时返回错误码 `1073`（原来是成功、`data` 为 `null`） |
