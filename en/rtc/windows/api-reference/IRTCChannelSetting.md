---
title: "IRTCChannelSetting"
description: "API reference for IRTCChannelSetting, the Windows SRTC per-channel settings: each item's default value, meaning, and when it takes effect (before join() or at any time while in the channel), plus the set_/get_ accessor pattern. Read before calling join()."
---

## Description
The channel settings interface, obtained through [IRTCChannel::getSetting](/en/rtc/windows/api-reference/IRTCChannel#get-the-settings-object).
There is **one per channel**. In older versions it was called `IRTCSetting` and lived on `IRTCEngine`.

Set the configuration after `createChannel` and before `join()`—items marked "Set before joining" in the table below are read during `join()` / stream setup,
and changing them after `join()` has no effect.

## Settings

| Parameter | Default | Description | Notes |
| --- | --- | --- | --- |
| stream_model | 3 | Media streaming mode; see [StreamModelEnum](/en/rtc/windows/enums#media-streaming-mode-streammodelenum) | Set before joining; read at join() to decide which media streaming implementation to use |
| stat_interval | 0 | Interval of the uplink/downlink callbacks (milliseconds) | Can be changed at any time while in the channel; the statistics thread re-reads it every cycle |
| speaker_interval | 0 | Interval of the audio level callback (milliseconds) | Can be changed at any time while in the channel; the statistics thread re-reads it every cycle |
| enable_audio_record | 0 | Enables local audio recording | Set before joining |
| mcu_track | 1 | MCU track setting | Set before joining |
| den_model | 2 | Audio noise suppression (0: acoustic, 1: AI, 2: AI + acoustic, 3: off) | Can be changed at any time while in the channel; applied to this channel immediately |
| simple | 0 | Simple mode | Set before joining |
| opus | 0 | Enables Opus encoding | Set before joining; also read every time an audio track is published |
| limit_speed | 0 | Bandwidth limit setting | Can be changed at any time while in the channel; applied to this channel immediately |

> `sdk_log_path` and `enable_stream_log` have been **removed** from this interface and are now parameters in
> [RTCEngineOptions](/en/rtc/windows/types#engine-initialization-options-rtcengineoptions) for `RTCEngine_Init`—they're consumed while the engine initializes,
> before any channel object exists.

## Methods

Each setting has a corresponding `set_<parameter name>` and `get_<parameter name>` method:

```cpp
// Example
virtual StatusCode set_stream_model(int v) = 0;
virtual int get_stream_model() = 0;

virtual StatusCode set_den_model(int v) = 0;
virtual int get_den_model() = 0;

// ... other settings work the same way
```
