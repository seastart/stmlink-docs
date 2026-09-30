---
title: "Settings"
description: "Setting items of the SMeeting Windows SDK: engine-level ISMeetingSetting (log path, stream log) read at login, and meeting-level ISMeetingChannelSetting with the getter/setter of each item and when it takes effect (at enter() or any time)."
---

Settings are split into **engine-level** `ISMeetingSetting` and **meeting-level** `ISMeetingChannelSetting`.

---

## ISMeetingSetting (engine level)

Obtained through `ISMeetingEngine::getSetting()`. These two items are read when `login()` initializes the underlying SRTC engine; changing them afterward has no effect.

| Setting | Setter | Getter | Type |
| --- | --- | --- | --- |
| SDK log path | set_sdk_log_path | get_sdk_log_path | std::string |
| Enable stream logs | set_enable_stream_log | get_enable_stream_log | int |

---

## ISMeetingChannelSetting (meeting level)

Obtained through `ISMeetingChannel::getSetting()`. Configure it after `createChannel()` and before `enter()`.

| Setting | Setter | Getter | Type | Takes effect |
| --- | --- | --- | --- | --- |
| Streaming mode | set_stream_model | get_stream_model | int | At `enter()` (read when `enter()` internally joins the underlying SRTC channel) |
| MCU track | set_mcu_track | get_mcu_track | int | At `enter()` (read when `enter()` internally joins the underlying SRTC channel) |
| Enable audio recording | set_enable_audio_record | get_enable_audio_record | int | At `enter()` (read when `enter()` internally joins the underlying SRTC channel) |
| Display name for entering the meeting | set_room_name | get_room_name | std::string | At enter() |
| Avatar for entering the meeting | set_room_avatar | get_room_avatar | std::string | At enter() |
| Streaming vendor | set_stream_vendor | get_stream_vendor | std::string | At enter() |
| Statistics interval | set_stat_interval | get_stat_interval | int | Can be changed any time |
| Speaker interval | set_speaker_interval | get_speaker_interval | int | Can be changed any time |
| Noise suppression mode | set_den_model | get_den_model | int | Can be changed any time |
| Speed limit | set_limit_speed | get_limit_speed | int | Can be changed any time |

> `stream_model` / `mcu_track` / `enable_audio_record` / `room_name` / `room_avatar` / `stream_vendor` are read at `enter()`, and changing them afterward has no effect; `den_model` / `limit_speed` / `stat_interval` / `speaker_interval` can be changed any time and are applied immediately.
