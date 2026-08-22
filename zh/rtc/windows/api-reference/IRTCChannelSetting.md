---
title: "IRTCChannelSetting"
description: "单个频道的各项运行参数读取与设置，含默认值和生效时机"
---

## 函数说明
频道配置接口，通过 [IRTCChannel::getSetting](./IRTCChannel.md#获取配置信息对象) 获取，
**一个频道一份**。旧版名为 `IRTCSetting`，挂在 `IRTCEngine` 上。

配置要在 `createChannel` 之后、`join()` 之前设置 —— 下表标「入会前设置」的项是在 `join()`/开流阶段读取的，
`join()` 之后再改不生效。

## 配置项

| 参数 | 默认 | 说明 | 备注 |
| --- | --- | --- | --- |
| stream_model | 3 | 流媒体模式 [查看](../enums.md#流媒体类型 StreamModelEnum) | 入会前设置，join() 时读取决定使用哪套流媒体实现 |
| stat_interval | 0 | 上下行回调时间间隔（毫秒） | 会中可以随意设置，统计线程每轮重读 |
| speaker_interval | 0 | 音柱信息回调时间间隔（毫秒） | 会中可以随意设置，统计线程每轮重读 |
| enable_audio_record | 0 | 使能本地录音 | 入会前设置 |
| mcu_track | 1 | MCU 轨道设置 | 入会前设置 |
| den_model | 2 | 音频降噪设置（0：声学，1:AI，2:AI+ 声学，3：关闭） | 会中可以随意设置，立即下发到本频道 |
| simple | 0 | 简单模式 | 入会前设置 |
| opus | 0 | OPUS 编码使能 | 入会前设置；每次推送音频轨道时也会读 |
| limit_speed | 0 | 限速设置 | 会中可以随意设置，立即下发到本频道 |

> `sdk_log_path` 和 `enable_stream_log` 已从本接口**移除**，改为 `RTCEngine_Init` 的
> [RTCEngineOptions](../types.md#引擎初始化参数（RTCEngineOptions）) 参数 —— 它们在引擎初始化阶段就被消费，
> 那时还没有任何频道对象。

## 函数方法

每个配置项都有对应的 `set_<参数名>` 和 `get_<参数名>` 方法：

```cpp
// 示例
virtual StatusCode set_stream_model(int v) = 0;
virtual int get_stream_model() = 0;

virtual StatusCode set_den_model(int v) = 0;
virtual int get_den_model() = 0;

// ... 其他配置项类似
```