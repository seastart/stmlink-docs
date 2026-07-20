---
title: "网络质量"
description: "Android SRTC 音视频 SDK 流媒体网络质量监测与弱网处理指南"
---

SDK 提供三种获取网络质量的方式，从"被动感知变化"到"主动查询"，按需选择：

| 方式 | 接口 | 使用场景 |
|---|---|---|
| 订阅质量等级变化（推荐） | `RTCMediaEvent.onNetworkQualityChanged` | 网络状态灯、弱网提示；**仅在质量等级跨档变化时回调**，内置迟滞去抖 |
| 周期性质量快照 | `RTCMediaEvent.onMediaMetric` | 详细诊断面板；每约 5 秒下发一份完整 `MediaMetric.Metric` |
| 主动查询快照 | `RTCEngine.getMetric()` | 任意时刻主动拉取最近一次完整质量快照 |

`onNetworkQualityChanged` 与 `onMediaMetric` 通过 `RTCMediaEvent` 被动下发，业务层订阅即可、无需轮询；`getMetric()` 用于主动按需拉取。

`Metric` 各字段的完整数据字典见[媒体质量](/zh/rtc/android/media-quality)。

## 一、订阅质量等级变化（推荐）

大多数业务只需要"网络状态灯 + 弱网提示"，推荐优先使用 `onNetworkQualityChanged`。它**只在质量等级发生跨档变化时回调**（而非每个采样周期都回调），并已处理好弱网抖动：

- **非对称迟滞**：等级下降（变差）**立即**回调，便于及时响应；等级回升（变好）需连续多次采样**确认后**才回调，避免网络抖动导致状态灯频繁跳变。因此业务层无需自己再做时间去抖，直接响应回调即可。
- **分方向**：上行、下行各自独立判断与回调，一次回调只表示**一个方向**（`direction`）的变化。

继承 `RTCMediaSimpleEvent` 只重写关心的回调，再通过 `setRtcMediaEvent` 注册：

```kotlin
import cn.seastart.rtc.impl.RTCMediaSimpleEvent
import cn.seastart.rtc.info.NetworkQualityChange
import cn.seastart.rtc.info.QualityDirection
import cn.seastart.rtc.info.QualityTrend

rtcEngine.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
    override fun onNetworkQualityChanged(change: NetworkQualityChange) {
        // change.direction     : UPLINK / DOWNLINK，本次变化的方向
        // change.previousLevel : 变化前等级
        // change.currentLevel  : 变化后等级（excellent / good / poor / lost）
        // change.trend         : INITIAL(首次) / DEGRADED(变差) / RECOVERED(变好)
        // change.report        : 触发本次变化时的完整 QualityReport

        // 回调可能在非主线程，更新 UI 请切主线程
        runOnUiThread {
            when (change.direction) {
                QualityDirection.UPLINK -> updateUplinkIndicator(change.currentLevel)
                QualityDirection.DOWNLINK -> updateDownlinkIndicator(change.currentLevel)
            }
        }
    }
})
```

:::note
`onNetworkQualityChanged` 在信令通道的后台线程回调，更新 UI 前请切换到主线程（如 `runOnUiThread` / `View.post`）。
:::

`NetworkQualityChange` 结构：

```kotlin
/** 变化方向 */
enum class QualityDirection {
    /** 上行：本端到服务端 */
    UPLINK,
    /** 下行：服务端到本端 */
    DOWNLINK
}

/** 变化趋势 */
enum class QualityTrend {
    /** 首次观测到该方向的等级（无历史可比） */
    INITIAL,
    /** 等级下降，网络变差 */
    DEGRADED,
    /** 等级回升，网络变好 */
    RECOVERED
}

data class NetworkQualityChange(
    /** 本次变化的方向 */
    var direction: QualityDirection,
    /** 变化前的等级；首次(INITIAL)时为占位空值 */
    var previousLevel: String,
    /** 变化后的等级：excellent / good / poor / lost */
    var currentLevel: String,
    /** 变化趋势 */
    var trend: QualityTrend,
    /** 触发本次变化时的完整质量报告，含上下行明细 */
    var report: MediaMetric.QualityReport
)
```

## 二、周期性质量快照 `onMediaMetric`

需要详细诊断面板（每条轨道的码率、丢包、帧率等）时，订阅 `onMediaMetric`。SDK 入会后每约 **5 秒**下发一份完整的 `MediaMetric.Metric`：

```kotlin
import cn.seastart.rtc.impl.RTCMediaSimpleEvent
import cn.seastart.rtc.statistics.MediaMetric

rtcEngine.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
    override fun onMediaMetric(metric: MediaMetric.Metric) {
        // 连接质量评估（同 onNetworkQualityChanged 的数据源）
        metric.qualityReport?.let { report ->
            val up = report.uplink.level     // excellent / good / poor / lost
            val down = report.downlink.level
            renderDashboard(up, down)
        }
        // 网络总体统计
        val net = metric.networkStats
        // 轨道级统计
        val localVideos = metric.localVideos
        val remoteVideos = metric.remoteVideos
    }
})
```

:::note
`qualityReport` 由服务端计算并下发，首次入会后需等待服务端首个质量报告到达，在此之前可能为 `null`，示例中已用可空写法处理。
:::

## 三、主动查询 `getMetric`

在任意时刻主动拉取最近一次采集到的完整质量快照（含 `qualityReport`），适合"点开详情才计算"的诊断面板等按需场景：

```kotlin
val metric = rtcEngine.getMetric()
metric?.qualityReport?.let { report ->
    // report.uplink.level / report.downlink.level ...
}
```

:::note
返回线程安全副本，不会触发底层 `getStats`；采样周期约 5 秒，起播初期可能为 `null`。
:::

## 四、连接质量评估 `qualityReport`

三种方式拿到的连接质量都是同一份 `qualityReport`：服务端已综合丢包、RTT、抖动、码率等多维指标计算出等级与 MOS，业务层直接用即可，无需自己算。它区分**上行**(本端到服务端)与**下行**(服务端到本端)两个方向。

```kotlin
data class QualityReport(
    /** 服务端生成该质量报告的时间戳 */
    var timestamp: Long = 0L,
    /** 本端到服务端的上行质量 */
    var uplink: QualityStats = QualityStats(),
    /** 服务端到本端的下行质量 */
    var downlink: QualityStats = QualityStats()
)

data class QualityStats(
    /** 综合质量分数，0 ~ 100，越高越好 */
    var score: Double = 0.0,
    /** 质量等级：excellent / good / poor / lost */
    var level: String = "",
    /** 语音主观质量分估算，1.0 ~ 4.5，越高越好 */
    var mos: Double = 0.0,
    /** 丢包率，0 ~ 1 */
    var loss: Double = 0.0,
    /** 往返时延，单位毫秒 */
    var rtt: Double = 0.0,
    /** 抖动，单位毫秒 */
    var jitter: Double = 0.0,
    /** 本轮统计参与计算的包数 */
    var packets: Long = 0L,
    /** 平均码率，单位 kbps */
    var bitrate: Double = 0.0,
    /** 本窗口字节数 */
    var bytes: Long = 0L
)
```

`level` 取值说明：

| level | 含义 |
|---|---|
| `excellent` | 优秀，几乎无损 |
| `good` | 良好，轻微丢包或延迟 |
| `poor` | 较差，明显卡顿、丢包 |
| `lost` | 连接已丢失，媒体无法传输 |

> `onNetworkQualityChanged`、`onMediaMetric.qualityReport`、`getMetric().qualityReport` 三者数据源一致，均来自服务端下发的同一份质量报告；区别只在下发方式（变化触发 / 周期 / 主动拉取）。

除 `qualityReport` 外，`Metric` 还包含网络总体统计 `networkStats`、上下行聚合 `localUploadStats` / `remoteDownloadStats`、以及轨道级统计 `localAudios` / `localVideos` / `remoteAudios` / `remoteVideos`，完整字段见[媒体质量](/zh/rtc/android/media-quality)。

## 五、弱网处理

处理弱网先分清两件事：**方向**和**处置**。

+ 上行差是你发不出去，可以主动降级(关摄像头、取消发布视频)；下行差是你收不进来，多数由服务端自动优化，必要时可退订视频。所以要看 `uplink` / `downlink` 两个方向，而不是只看一侧。
+ 用 `onNetworkQualityChanged` 驱动即可——它已内置迟滞去抖，无需业务层再做时间去抖；若走 `onMediaMetric` 周期读取，则需自行去抖（见 5.1）。

### 5.1 展示网络状态

用质量等级映射一个状态灯即可，不要把丢包率、RTT 这类原始数据直接展示给终端用户：

| level | 状态灯 |
|---|---|
| `excellent` / `good` | 正常 |
| `poor` | 较差，画质可能下降 |
| `lost` | 连接中断，重连中 |

上行差和下行差的提示文案不同，需要区分。用 `onNetworkQualityChanged` 时，直接响应变化即可，无需自己去抖：

```kotlin
override fun onNetworkQualityChanged(change: NetworkQualityChange) {
    if (change.trend != QualityTrend.DEGRADED) return
    when (change.direction) {
        QualityDirection.UPLINK ->
            if (isBad(change.currentLevel)) showTip("您的网络不佳，对方可能看不清您")
        QualityDirection.DOWNLINK ->
            if (isBad(change.currentLevel)) showTip("网络不佳，正在优化画质")
    }
}

private fun isBad(level: String) = level == "poor" || level == "lost"
```

若改用周期性的 `onMediaMetric`，由于每约 5 秒回调一次，需自行做一次去抖，避免频繁打扰：

```kotlin
// 简单去抖：记录某方向进入 poor 的起始时间，持续超过阈值才提示
private var uplinkPoorSince = 0L

private fun checkUplink(level: String) {
    if (level == "poor" || level == "lost") {
        if (uplinkPoorSince == 0L) uplinkPoorSince = System.currentTimeMillis()
        if (System.currentTimeMillis() - uplinkPoorSince > 5000) {
            showTip("您的网络不佳，对方可能看不清您")
        }
    } else {
        uplinkPoorSince = 0L
    }
}
```

### 5.2 上行变差

当上行等级持续为 `poor` / `lost`，按从轻到重逐级降级：

**1. 关闭摄像头、只保留音频。** 音频码率低，弱网下几乎总能保住。停止摄像头采集即可显著降低上行占用，且保留发布通道，网络恢复后可随时重新采集：

```kotlin
// 弱网时：关闭摄像头采集，音频不受影响
localCameraTrack.stopCapture()

// 网络恢复后：重新开启采集
localCameraTrack.startCapture(object : RTCResultListener {
    override fun onSuccess() {}
    override fun onFail(code: Int) {}
})
```

**2. 彻底取消发布视频。** 比关摄像头更彻底，释放上行编码与发送资源：

```kotlin
rtcEngine.unPublishLocalVideo(localVideoTrack, object : RTCResultListener {
    override fun onSuccess() {}
    override fun onFail(code: Int) {}
})
```

关摄像头会改变通话形态，建议提示用户后再执行，不要静默操作——应急指挥、执法记录等场景尤其如此。

如需进一步定位上行受限的原因，可读取本地视频轨道的 `qualityLimitationReason`：

```kotlin
rtcEngine.getMetric()?.localVideos?.values?.forEach { stats ->
    when (stats.qualityLimitationReason) {
        "bandwidth" -> { /* 上行带宽不足：优先降码率 / 关摄像头 */ }
        "cpu"       -> { /* 设备编码跟不上：建议降分辨率 / 帧率 */ }
    }
}
```

### 5.3 下行变差

当下行等级持续为 `poor`：

**1. 先确认是不是对端的问题。** 本端有下行丢包(`downlink.loss` 明显 > 0)，才是你的接收链路差；若本端几乎无丢包、只是某人画面卡顿，通常是对方上行差，此时退订也无济于事，提示"对方网络不佳"即可。

**2. 发布方发大小流时，服务端自动切层。** 服务端会依据每个订阅者自身的下行带宽和丢包，自动把它切到合适的大 / 小流，订阅端无需手动切换（订阅时通过候选层列表告知服务端可切的层）。只发单流则无法自动降。

**3. 退订视频、只收音频。**

```kotlin
rtcEngine.unSubscribeRemoteTrack(uid, trackId)
```

**4. 多路会议**：只订阅当前说话人的视频，其余成员只收音频。当前说话人可通过 `onActiveSpeakersChanged` 获取：

```kotlin
override fun onActiveSpeakersChanged(speakers: List<ActiveSpeakerInfo>) {
    // speakers 为当前正在说话的用户列表，可据此决定订阅哪些人的视频
    speakers.forEach { it.uid; it.level }
}
```

### 5.4 连接断开与重连

连接状态相关的通知在 `RTCClientEvent` 中，通过 `setRtcClientEvent` 注册。SDK 会在网络中断时自动重连，业务层据此更新 UI 即可：

```kotlin
import cn.seastart.rtc.impl.RTCClientSimpleEvent

rtcEngine.setRtcClientEvent(object : RTCClientSimpleEvent() {
    override fun onReconnecting() {
        showReconnecting()   // 显示"正在重连"
    }
    override fun onReconnected() {
        hideReconnecting()   // 重连成功，恢复状态灯与此前主动关闭的摄像头 / 订阅
    }
    override fun onDisconnected(leaveReason: LeaveReason, statusCode: Int, message: String) {
        // 连接已断开
    }
})
```

### 5.5 速查表

| 信号 | 处置 |
|---|---|
| `uplink = poor / lost` | 关摄像头保音频 → 取消发布视频；提示"您的网络" |
| `uplink` 受限原因 `bandwidth` | 关摄像头 / 降码率 |
| `uplink` 受限原因 `cpu` | 降分辨率 / 帧率 |
| `downlink = poor`（本端有丢包） | 退订视频保音频 / 多路只留主讲 |
| `downlink = poor`（本端无丢包） | 提示"对方网络不佳" |
| `onReconnecting` | 显示"正在重连"，恢复后刷新状态 |

## 六、完整示例

把上面的做法串起来：用 `onNetworkQualityChanged` 驱动状态灯与分方向提示（内置迟滞，无需自行去抖），按需降级与恢复，并处理断线重连。

```kotlin
import cn.seastart.rtc.impl.RTCMediaSimpleEvent
import cn.seastart.rtc.impl.RTCClientSimpleEvent
import cn.seastart.rtc.info.NetworkQualityChange
import cn.seastart.rtc.info.QualityDirection
import cn.seastart.rtc.info.QualityTrend
import cn.seastart.rtc.track.LocalCameraTrack

class NetworkQualityHandler(
    private val rtcEngine: RTCEngine,
    private val cameraTrack: LocalCameraTrack,
    private val localVideoTrack: LocalVideoTrack
) {
    // 标记是否因弱网主动关了摄像头，用于网络恢复后自动开回
    private var cameraOffByNetwork = false

    fun attach() {
        rtcEngine.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
            override fun onNetworkQualityChanged(change: NetworkQualityChange) {
                runOnUiThread {
                    // 状态灯：按方向更新（一次回调只表示一个方向）
                    when (change.direction) {
                        QualityDirection.UPLINK -> updateUplinkIndicator(change.currentLevel)
                        QualityDirection.DOWNLINK -> updateDownlinkIndicator(change.currentLevel)
                    }

                    // 仅在"变差"时提示，分方向文案
                    if (change.trend == QualityTrend.DEGRADED && isBad(change.currentLevel)) {
                        when (change.direction) {
                            QualityDirection.UPLINK ->
                                showTip("您的网络不佳，可关闭摄像头以保证语音通话")
                            QualityDirection.DOWNLINK ->
                                showTip("网络不佳，正在优化画质")
                        }
                    }
                }
            }
        })

        rtcEngine.setRtcClientEvent(object : RTCClientSimpleEvent() {
            override fun onReconnecting() { showReconnecting() }
            override fun onReconnected() {
                hideReconnecting()
                // 重连成功且此前因弱网关过摄像头 → 自动开回
                if (cameraOffByNetwork) {
                    cameraTrack.startCapture(null)
                    cameraOffByNetwork = false
                }
            }
        })
    }

    // 用户确认后：关摄像头保音频
    fun downgradeToAudioOnly() {
        cameraTrack.stopCapture()
        cameraOffByNetwork = true
    }

    private fun isBad(level: String) = level == "poor" || level == "lost"
}
```

> 示例中 `stopCapture` / `startCapture` / `unPublishLocalVideo` / `unSubscribeRemoteTrack` 均为 SDK 现有方法。关摄像头这类改变通话形态的操作建议通过按钮交给用户确认，未静默执行；普通会议等场景可自行改为自动。
