---
title: "IRTCSetting"
description: "Windows SRTC 音视频 SDK IRTCSetting 配置接口参考"
---

## 函数说明
SDK 配置接口，提供各项参数的获取和设置方法。

## 配置项

| 参数 | 默认 | 说明 | 备注 |
| --- | --- | --- | --- |
| stream_model | 3 | 流媒体模式 [查看](../enums.md#流媒体类型 StreamModelEnum) | 入会前设置 |
| sdk_log_path | 空 | 日志目录 | 需在首次入会前设置 |
| stat_interval | 0 | 上下行回调时间间隔（毫秒） | 会中可以随意设置 |
| speaker_interval | 0 | 音柱信息回调时间间隔（毫秒） | 会中可以随意设置 |
| enable_stream_log | 0 | 使能流媒体日志 | 入会前设置 |
| enable_audio_record | 0 | 使能本地录音 | 入会前设置 |
| mcu_track | 1 | MCU 轨道设置 | 会中可以随意设置 |
| den_model | 2 | 音频降噪设置（0：声学，1:AI，2:AI+ 声学，3：关闭） | 会中可以随意设置 |
| simple | 0 | 简单模式 | 入会前设置 |
| opus | 0 | OPUS 编码使能 | 入会前设置 |
| limit_speed | 0 | 限速设置 | 入会前设置 |

## 函数方法

每个配置项都有对应的 `set_<参数名>` 和 `get_<参数名>` 方法：

```cpp
// 示例
virtual StatusCode set_stream_model(int v) = 0;
virtual int get_stream_model() = 0;

virtual StatusCode set_sdk_log_path(const char* v) = 0;
virtual const char* get_sdk_log_path() = 0;

// ... 其他配置项类似
```
