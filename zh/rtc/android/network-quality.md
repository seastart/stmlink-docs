---
title: "网络质量"
description: "区分 FY 服务端质量报告、本地网络与播放体验快照，以及按需查询的逐轨详细统计。"
---

SDK 提供三种相互独立的质量信息。所有回调都带 `channel`，多频道应用应按频道保存结果。公开监测类型位于 `cn.seastart.rtc.monitoring.api`。

| 信息 | 入口 | 用途 |
| --- | --- | --- |
| FY 服务端网络质量 | `RTCMediaEvent.onNetworkQualityChanged(channel, change)` | FY 服务端每份报告分别交付上、下行事件；WS 不提供该服务端报告。 |
| 本地网络与播放体验 | `RTCMediaEvent.onLocalQualitySnapshot(channel, snapshot)` | 每频道在采样完成后约 2 秒交付一次本地上下行网络质量和逐轨下行播放体验。 |
| 详细媒体统计 | `RTCEngine.getMetric()` / `RTCChannel.getMetric()` | 按需查询默认频道或指定频道最近一次完成采样的原始统计。 |

本地快照与 FY 服务端报告有不同的数据来源和等级，不应混用。详细模型及数值单位见 [媒体质量](/zh/rtc/android/media-quality)。

## 监听本地周期快照

```kotlin
import cn.seastart.rtc.impl.RTCMediaSimpleEvent
import cn.seastart.rtc.monitoring.api.LocalQualitySnapshot

rtcEngine.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
    override fun onLocalQualitySnapshot(channel: String, snapshot: LocalQualitySnapshot) {
        val uplink = snapshot.networkQuality.uplink.level
        val downlink = snapshot.networkQuality.downlink.level
        val affectedTracks = snapshot.networkQuality.remoteTracks
        val videoPlayback = snapshot.mediaPlaybackExperience.videoTracks
        // 根据 channel 分发到对应页面；更新 UI 前切换到主线程。
    }
})
```

`snapshot.timestamp`、`snapshot.networkQuality.timestamp` 与 `snapshot.mediaPlaybackExperience.timestamp` 相同，单位为毫秒。间隔从采集及交付完成后开始计算，因此不是严格每 2 秒一次。没有有效样本时，网络或播放等级可能为 `UNKNOWN`，可空指标为 `null`。`NetworkQuality` 分别提供方向概览和逐轨结果；播放体验只评估本地接收的音视频连续性。网络差不必然等于播放卡顿，播放平滑也不表示画质清晰。

网络等级为 `UNKNOWN`、`EXCELLENT`、`GOOD`、`POOR`、`BAD`、`LOST`。`LOST` 只表示预期传输轨道的 ICE 进入 `FAILED`；主动关闭返回 `UNKNOWN`。视频播放等级为 `UNKNOWN`、`SMOOTH`、`DEGRADED`、`FROZEN`；音频为 `UNKNOWN`、`CLEAR`、`DEGRADED`、`INTERRUPTED`。逐轨网络分数 `score` 为 0～100，无法评分时为 `null`，不代表播放体验分。

## 按需查询详细统计

```kotlin
import cn.seastart.rtc.monitoring.api.MediaMetric

val metric: MediaMetric? = rtcEngine.getMetric() // 默认频道
val otherMetric: MediaMetric? = rtcChannel.getMetric() // 指定频道
metric?.let { sample ->
    val channel = sample.channel
    val sampledAtMs = sample.sampleTimestampMs
    val localVideos = sample.localVideos
    val remoteVideos = sample.remoteVideos
    val serverReport = sample.qualityReport // FY 可用；WS 为 null
}
```

查询返回最近一次**完成**的采样，不会额外触发 WebRTC `getStats()`，也不会推进网络或播放评估窗口。尚无可用采样或监测失效时返回 `null`；同一帧重复查询会得到独立副本。`sampleTimestampMs` 是采样完成时间；若快照回调后已有新采样，随后查询到的时间戳可能不同。组合两类结果时先核对 `channel` 和时间戳。逐轨 `timestamp` 来自 RTCStats，与顶层墙钟时间不同。

详细码率单位是 bps，RTT 和 jitter 为 ms，丢包率为 0～1；包数、字节数和帧数是累计量。`null` 表示不可得，真实测到的零保留为 `0`。无轨道时部分方向合计为 `0`，不能据此推断某条轨道有零值。

## FY 服务端报告

```kotlin
import cn.seastart.rtc.monitoring.api.NetworkQualityChange

override fun onNetworkQualityChanged(channel: String, change: NetworkQualityChange) {
    val direction = change.direction // UPLINK 或 DOWNLINK
    val level = change.currentLevel // excellent / good / poor / lost
    val trend = change.trend // INITIAL / DEGRADED / RECOVERED / STABLE
    val report = change.report // ServerQualityReport
}
```

每份 FY 报告会为上、下行各回调一次，即使等级未变也会以 `STABLE` 交付；SDK 不做业务去抖。`report` 同时包含两个方向的服务端统计。`getMetric().qualityReport` 也是 FY 的最近服务端报告，但它在该采样帧首次组装详细统计时读取，不能假设与某次服务端回调严格同步。WS 的 `qualityReport` 为 `null`。回调在 SDK 后台线程执行，更新 UI 前切到主线程。

## 处理弱网

先按频道、方向及轨道判断影响范围。可以用方向等级驱动状态展示，再用 `remoteTracks`、`localTracks` 和播放列表定位受影响的轨道。提示或自动降级应由应用按业务场景设置持续时间与恢复条件；不要把一次 `POOR` 或 `BAD` 直接当作必须停止视频的信号。连接状态变化另见 [`RTCClientEvent`](/zh/rtc/android/api-reference/RTCClientEvent)。
