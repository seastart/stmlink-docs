---
title: "配置项"
description: "Windows SMeeting SDK 引擎级与会议级配置项 C++ 参考"
---

配置项分为**引擎级** `ISMeetingSetting` 和**会议级** `ISMeetingChannelSetting`。

---

## ISMeetingSetting（引擎级）

通过 `ISMeetingEngine::getSetting()` 获取。这两项在 `login()` 初始化 rtc 引擎时读取，之后修改无效。

| 配置项 | 设置方法 | 获取方法 | 类型 |
| --- | --- | --- | --- |
| SDK 日志路径 | set_sdk_log_path | get_sdk_log_path | std::string |
| 启用流日志 | set_enable_stream_log | get_enable_stream_log | int |

---

## ISMeetingChannelSetting（会议级）

通过 `ISMeetingChannel::getSetting()` 获取。在 `createChannel()` 之后、`enter()` 之前配置。

| 配置项 | 设置方法 | 获取方法 | 类型 | 生效时机 |
| --- | --- | --- | --- | --- |
| 流模式 | set_stream_model | get_stream_model | int | rtc join 时 |
| MCU 轨道 | set_mcu_track | get_mcu_track | int | rtc join 时 |
| 启用音频录制 | set_enable_audio_record | get_enable_audio_record | int | rtc join 时 |
| 入会昵称 | set_room_name | get_room_name | std::string | enter() 时 |
| 入会头像 | set_room_avatar | get_room_avatar | std::string | enter() 时 |
| 流厂商 | set_stream_vendor | get_stream_vendor | std::string | enter() 时 |
| 统计间隔 | set_stat_interval | get_stat_interval | int | 随时可改 |
| 发言者间隔 | set_speaker_interval | get_speaker_interval | int | 随时可改 |
| 降噪模式 | set_den_model | get_den_model | int | 随时可改 |
| 限速 | set_limit_speed | get_limit_speed | int | 随时可改 |

> `stream_model` / `mcu_track` / `enable_audio_record` / `room_name` / `room_avatar` / `stream_vendor` 在 `enter()` 时读取，之后改无效；`den_model` / `limit_speed` / `stat_interval` / `speaker_interval` 随时可改并立刻下发。
