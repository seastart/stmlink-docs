---
title: "媒体质量"
description: "通过 SMeeting Android 的本地质量快照、按需详细统计和 FY 服务端报告观察当前会议的音视频质量"
---

SMeeting 2.0.41 使用 SRTC 2.0.38 的 `cn.seastart.rtc.monitoring.api` 监测模型。旧版 `cn.seastart.rtc.statistics.MediaMetric` 的嵌套类型和 `onMediaMetric()` 已移除；完整字段与数值单位见 [SRTC 媒体质量](/zh/rtc/android/media-quality)。

## 获取质量数据

| 入口 | 数据 | 使用时机 |
| --- | --- | --- |
| `MeetingMediaEvent.onLocalQualitySnapshot(snapshot)` | `LocalQualitySnapshot`，同次采样的本地上下行网络质量和远端音视频播放体验 | 周期展示网络与播放质量；回调保持 RTC 统计线程，更新 UI 前应切换线程 |
| `MeetingEngine.getMetric()` | 当前会议频道最近一次完成采样的 `MediaMetric?` 详细统计副本 | 按需读取轨道码率、帧率、丢包与网络数据；不会即时触发底层统计采集 |
| `MeetingMediaEvent.onNetworkQualityChanged(change)` | FY 服务端的 `NetworkQualityChange` | 处理服务端上、下行质量档位；与本地快照独立，WS 不产生此类 FY 报告 |

`getMetric()` 在无活动会议、尚未完成采样或媒体连接失效时返回 `null`。`onLocalQualitySnapshot()` 在采样完成后约每 2 秒交付一次；详细统计只在需要时查询。

```kotlin
import cn.seastart.meeting.event.MeetingMediaSimpleEvent
import cn.seastart.rtc.monitoring.api.LocalQualitySnapshot
import cn.seastart.rtc.monitoring.api.MediaMetric
import cn.seastart.rtc.monitoring.api.NetworkQualityChange

meetingEngine.mediaEvent = object : MeetingMediaSimpleEvent() {
    override fun onLocalQualitySnapshot(snapshot: LocalQualitySnapshot) {
        val downlinkLevel = snapshot.networkQuality.downlink.level
        // 回调在 RTC 统计线程；如需显示 downlinkLevel，先切换到主线程。
    }

    override fun onNetworkQualityChanged(change: NetworkQualityChange) {
        // FY 服务端质量报告；弱网提示由应用自行去抖。
    }
}

val metric: MediaMetric? = meetingEngine.getMetric()
```

## 本地质量快照

`LocalQualitySnapshot` 包含同一轮采样的 `timestamp: Long`、`networkQuality: NetworkQuality` 和 `mediaPlaybackExperience: MediaPlaybackExperience`。网络质量按上、下行及用户轨道提供档位、丢包率、码率、RTT 和抖动；播放体验按远端视频、音频轨道提供流畅度或中断信息。快照不包含逐轨原始计数；字段和档位见 [SRTC 媒体质量](/zh/rtc/android/media-quality)。

## 详细统计

`getMetric()` 返回的顶层 `MediaMetric` 包含 `channel`、`sampleTimestampMs`、本地音视频发送轨道 `localAudios` / `localVideos`、远端接收轨道 `remoteAudios` / `remoteVideos`、汇总 `localUploadStats` / `remoteDownloadStats`、`networkStats`，以及可空的 FY 服务端 `qualityReport`。逐轨映射使用 `UserTrackDesc` 作为键；码率单位是 bps，丢包率为 0～1 的比例。详细字段与单位见 [SRTC 媒体质量](/zh/rtc/android/media-quality)。

## FY 服务端质量报告

`onNetworkQualityChanged()` 每收到一份 FY 服务端报告就为上、下行各回调一次，不做去抖；等级未变化时 `trend` 为 `STABLE`。它与本地 `LocalQualitySnapshot` 的评估相互独立。方向、档位和趋势枚举见 [SRTC 枚举类型](/zh/rtc/android/enums)，弱网处理建议见 [SRTC 网络质量](/zh/rtc/android/network-quality)。
