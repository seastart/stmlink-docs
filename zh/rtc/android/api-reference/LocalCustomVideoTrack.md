---
title: "LocalCustomVideoTrack"
description: "Android SRTC 音视频 SDK LocalCustomVideoTrack 接口参考"
---

## 说明

`LocalCustomVideoTrack` 用于向已发布的轨道推送外部**原始 YUV 视频帧**（如白板、画布、播放器画面、第三方采集源），通过 [`RTCEngine.getLocalCustomVideoTrack`](/zh/rtc/android/api-reference/RTCEngine) 获取。它继承自 `LocalVideoTrack`，可直接作为 `publishLocalVideo` / `unPublishLocalVideo` 的输入轨道。

与 [`CustomVideoTrack`](/zh/rtc/android/api-reference/CustomVideoTrack) 的区别（两者是不同的类，方法同名但语义不同，切勿混用）：

| 对比项 | LocalCustomVideoTrack | CustomVideoTrack |
| --- | --- | --- |
| 输入数据 | 原始 YUV（I420）未编码帧 | 已编码码流（H264/H265） |
| 获取方式 | `getLocalCustomVideoTrack(preOpt)` | `getCustomVideoTrack()` |
| 开始/停止推流 | `publishLocalVideo` / `unPublishLocalVideo` | `startCustomVideo` / `stopCustomVideo` |
| 送帧方法 | `inputData(yuv, width, height, strideY, strideU, strideV, rotation, stamp)` | `inputData(stamp, data, angle)` |
| 编码 | 由 SDK 完成（按预设参数） | 由业务侧自行完成 |

> ⚠️ **引擎限制**：本轨道的帧输入仅在风远（`StreamVendor.FY`）与网宿（`StreamVendor.WS`）流媒体引擎下生效；网仕（`StreamVendor.OOK`）引擎下调用 `inputData` 不会产生任何效果，帧被直接丢弃，也不会有错误回调。引擎由服务端下发决定，枚举值参见 [枚举定义](/zh/rtc/android/enums)。

## 属性

### preOpt
```kotlin
var preOpt: PreOptionCustomVideo
```
说明：当前轨道使用的自定义视频预设（采集参数 + 推送参数），参见 [自定义视频流预设](/zh/rtc/android/presets/custom-video)。

- `preOpt.publish.desc` 决定该轨道的轨道描述，`inputData` 也依据它定位目标轨道。
- 轨道实例在 SDK 内部按单例缓存：重复调用 `getLocalCustomVideoTrack(preOpt)` 返回同一实例，并把传入的 `preOpt` 覆盖到该实例上。若需要同时区分“自定义流”和“共享流”，应在切换预设后重新发布，不要在同一时刻按两套 `desc` 交替送帧。

## LocalCustomVideoTrack 自身方法

### inputData(yuv, width, height, strideY, strideU, strideV, rotation, stamp)
```kotlin
fun inputData(
    yuv: ByteArray, width: Int, height: Int,
    strideY: Int, strideU: Int, strideV: Int,
    rotation: Int, stamp: Long
)
```
方法说明：向已发布的自定义视频轨道推送一帧原始 YUV 数据。内部按 `preOpt.publish.desc` 查找已发布轨道并送入编码流水线；轨道尚未发布（或引擎不支持）时该帧被静默丢弃。  
参数说明：

| 参数名 | 数据类型 | 说明 |
| --- | --- | --- |
| yuv | `ByteArray` | 紧凑排布的 I420 数据，长度至少 `width * height * 3 / 2`。 |
| width | `Int` | 帧宽度，需为偶数。 |
| height | `Int` | 帧高度，需为偶数。 |
| strideY | `Int` | Y 平面行跨度，传 `width`。 |
| strideU | `Int` | U 平面行跨度，传 `width / 2`。 |
| strideV | `Int` | V 平面行跨度，传 `width / 2`。 |
| rotation | `Int` | 帧旋转角度，取 `0` / `90` / `180` / `270`，作为帧元数据交由编码与渲染侧处理。 |
| stamp | `Long` | 帧时间戳，单位**纳秒**（与 Camera2 的 `timestampNs` 同一口径）。 |

返回值说明：无（`Unit`）。

#### 帧数据格式要求

- **必须是紧凑 I420**：`Y` 平面 `width * height` 字节，紧接 `U` 平面 `(width/2) * (height/2)` 字节，再接同样大小的 `V` 平面，三段连续无空洞。
- **`stride` 必须与紧凑布局一致**（`width`、`width/2`、`width/2`）。SDK 当前按紧凑布局计算平面偏移，传入带 padding 的行跨度会导致画面错位/花屏。若上游数据带 padding（如 Camera2 的 `rowStride > width`），请先按有效像素拷贝成紧凑数组再送入。
- 长度不足会在送编码前抛出 `IllegalArgumentException`（`Invalid I420 size`）。
- 分辨率无需自行对齐编码器：SDK 会按设备编码器要求做对齐缩放；但 `width`/`height` 必须为偶数。
- 送帧节奏由业务侧控制，帧率与码率上限由 `preOpt` 决定，超出预设帧率的高频送帧只会增加无谓开销。

## 继承自 VideoTrack 的渲染方法

`addPlayView` / `replacePlayView` / `removePlayView` / `removeAllPlayView` 由基类 `VideoTrack` 提供，签名与 [`LocalScreenTrack`](/zh/rtc/android/api-reference/LocalScreenTrack) 一致。

> **注意**：SDK **不会**把 `inputData` 送入的帧回显到这些渲染控件上（本地回显仅对摄像头轨道生效）。自定义视频的本地预览请由业务侧自行绘制数据源，无需给本轨道添加渲染控件。

## 典型接入流程

```kotlin
// 1. 获取轨道（可自定义预设，默认 PreOptionCustomVideo.def）
val customTrack = rtcEngine.getLocalCustomVideoTrack(PreOptionCustomVideo.def)

// 2. 发布轨道；发布成功后才能送帧
rtcEngine.publishLocalVideo(customTrack, null, object : RTCResultListener {
    override fun onSuccess() {
        // 3. 按业务节奏持续送帧（此处示意单帧）
        customTrack.inputData(
            yuv = i420Bytes,          // 紧凑 I420
            width = 1920,
            height = 1080,
            strideY = 1920,
            strideU = 960,
            strideV = 960,
            rotation = 0,
            stamp = System.nanoTime()
        )
    }

    override fun onFail(code: Int) {
        // 错误码参见错误码文档
    }
})

// 4. 结束推送
rtcEngine.unPublishLocalVideo(customTrack, null)
```

如需以屏幕共享的轨道描述（`TRACK_SHARE`）发布外部画面，改用 `PreOptionCustomVideo.screen`，或在发布时通过 `PublishCustomOptions(desc = ...)` 覆盖 `desc`：

```kotlin
val shareTrack = rtcEngine.getLocalCustomVideoTrack(PreOptionCustomVideo.screen)
rtcEngine.publishLocalVideo(shareTrack, null, null)
```

## 注意事项

- **先发布、后送帧**：`publishLocalVideo` 成功回调之后再调用 `inputData`，否则帧会被丢弃且无任何提示。
- **`desc` 要一致**：若发布时用 `PublishCustomOptions` 覆盖了 `desc`，SDK 会同步写回 `preOpt.publish.desc`，`inputData` 仍按最新的 `desc` 定位轨道；不要在业务侧另存一份旧 `desc` 做判断。
- **发布/取消发布的回调合并**：与摄像头一致，快速连续 `publish`/`unpublish` 时中间被合并的调用可能不回调，以最后一次调用的回调或最终状态为准。
- **离会后需重新发布**：`leave()` 会释放流媒体引擎，轨道实例仍在但发布状态已失效，重新入会后必须重新 `publishLocalVideo` 才能继续送帧；`releaseSDK()` 还会清空本地轨道缓存，之后需重新调用 `getLocalCustomVideoTrack`。
- **复用输入数组**：`inputData` 内部会把数据拷贝进编码缓冲，调用返回后业务侧可立即复用该 `ByteArray`，建议自行做缓冲池以降低 GC 压力。
