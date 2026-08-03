---
title: "自定义推流"
description: "Android SRTC 音视频 SDK 通过 LocalCustomVideoTrack 把外部画面（白板、画布、播放器、第三方采集源）作为视频流发布到频道"
---

当内置的摄像头、屏幕共享采集不能满足需求时，可以用 `LocalCustomVideoTrack` 把**业务侧自己生成的画面**发布到频道。分工是固定的：

- **你负责产出帧**：持续提供**未编码**的原始 YUV（I420）数据，无需自行编码。
- **SDK 负责编码与传输**：按预设参数编码、发布，远端像普通视频流一样订阅播放。

典型场景：

- 白板 / 画布 / 自绘内容推流
- 本地播放器解码后的画面转推
- 第三方 SDK（美颜、AR、AI 生成）处理后的输出
- 非标准采集设备（外接采集卡、USB 设备）的帧数据

> ⚠️ **引擎限制**：自定义帧输入仅在风远（`StreamVendor.FY`）与网宿（`StreamVendor.WS`）流媒体引擎下生效。网仕（`StreamVendor.OOK`）引擎下 `inputData` 不产生任何效果，帧被直接丢弃且**没有错误回调**。引擎由服务端下发决定，接入前请先与服务端确认当前频道使用的引擎。

## 1. 整体流程

```text
入会成功（onJoinSucceed）
   ↓
getLocalCustomVideoTrack(preOpt)     选预设，拿轨道
   ↓
publishLocalVideo(track, ...)        发布轨道，等 onSuccess
   ↓
inputData(...)  ← 循环送帧            业务侧持续产帧
   ↓
unPublishLocalVideo(track, ...)      停止推流
```

三个必须遵守的顺序约束：

1. **入会之后**才能发布（未入会 `publishLocalVideo` 回调 `onFail(102202)`，频道未启动）。
2. **发布成功之后**才能送帧。轨道未发布时 `inputData` 会被静默丢弃，没有任何提示 —— 这是最常见的“远端看不到画面”的原因。
3. **观众身份不能发布**（`onFail(102207)`）。可先用 `rtcEngine.isAudience()` 判断。

## 2. 选择预设

预设决定编码分辨率、帧率、码率以及轨道描述（`desc`），完整字段见 [自定义视频流预设](/zh/rtc/android/presets/custom-video)。

```kotlin
// 默认预设：1080p / 10fps / 1Mbps，轨道描述 "custom"
val preOpt = PreOptionCustomVideo.def

// 以屏幕共享的轨道描述发布外部画面（远端按"共享"处理），轨道描述 "screen"
val sharePreOpt = PreOptionCustomVideo.screen
```

需要自定义参数时直接构造。**采集与推送两侧的分辨率保持一致**，可以避免 SDK 做额外缩放：

```kotlin
val preOpt = PreOptionCustomVideo(
    capture = CustomVideoCaptureOptions(
        width = 1280,
        height = 720,
        maxFps = 15,
        maxBitrate = 1200 * 1024
    ),
    publish = VideoPublishOptions(
        desc = TrackDesc.TRACK_CUSTOM.value,
        codec = CodecType.H264,
        maxBitrate = 1200 * 1024,
        width = 1280,
        height = 720,
        maxFps = 15,
        props = null,
        simulcasts = null      // 自定义视频不使用联播
    )
)
```

选参数的建议：

- **静态内容为主（白板、文档、PPT）**：帧率取 5～10 fps 就够，分辨率优先（文字清晰度靠分辨率而不是帧率）。
- **动态内容（视频转推、游戏画面）**：帧率取 15～25 fps，同时把码率相应提高，否则运动画面会明显发糊。
- 宽高必须是**偶数**（I420 的色度平面按 `width/2 × height/2` 计算）。

## 3. 获取轨道并发布

```kotlin
private var customTrack: LocalCustomVideoTrack? = null

private fun startCustomPush() {
    if (rtcEngine.isAudience()) {
        // 观众身份不能发流
        return
    }

    val track = rtcEngine.getLocalCustomVideoTrack(preOpt)
    customTrack = track

    rtcEngine.publishLocalVideo(track, null, object : RTCResultListener {
        override fun onSuccess() {
            // 发布成功后才开始送帧
            startFrameLoop(track)
        }

        override fun onFail(code: Int) {
            // 102202：频道未启动（尚未入会）
            // 102207：观众禁止发流
            // 其他错误码参见错误码文档
        }
    })
}
```

关于轨道实例，有两点需要注意：

- **它在 SDK 内部按单例缓存**。重复调用 `getLocalCustomVideoTrack(preOpt)` 返回同一个对象，并用新传入的 `preOpt` 覆盖旧值。因此不要用两套 `desc` 交替送帧来模拟“两路自定义流”，同一时刻只应有一套生效的预设。
- 若在发布时通过 `PublishCustomOptions(desc = ...)` 覆盖了 `desc`，SDK 会把它写回 `preOpt.publish.desc`，`inputData` 自动按最新的 `desc` 定位轨道，业务侧无需额外处理。

```kotlin
// 用 PublishCustomOptions 覆盖轨道描述的写法
rtcEngine.publishLocalVideo(
    track,
    PublishCustomOptions(TrackDesc.TRACK_SHARE.value, null, null),
    listener
)
```

## 4. 准备帧数据（关键）

`inputData` 只接受**紧凑排布的 I420**。这一节的约定不满足，表现就是远端花屏、错位或绿边。

### 4.1 内存布局

```text
byteArray 长度 = width * height * 3 / 2

┌────────────────────────────┐  offset 0
│ Y 平面   width * height     │
├────────────────────────────┤  offset = width*height
│ U 平面   (width/2)*(height/2)│
├────────────────────────────┤  offset = width*height*5/4
│ V 平面   (width/2)*(height/2)│
└────────────────────────────┘
```

三段必须**连续、无空洞**，并且 `stride` 参数按紧凑值传：

```kotlin
strideY = width
strideU = width / 2
strideV = width / 2
```

> ⚠️ SDK 当前按紧凑布局计算平面偏移，传入带 padding 的行跨度**不会**被用于寻址。若上游数据每行带 padding（如 Camera2 的 `rowStride > width`），必须先按有效像素逐行拷贝成紧凑数组，再送入。

数据长度不足时，SDK 会在送编码前抛出 `IllegalArgumentException("Invalid I420 size: ...")`，可据此快速定位布局问题。

### 4.2 从 Bitmap / Canvas 生成 I420

白板、自绘内容通常先画到 `Bitmap`（`ARGB_8888`），再转 I420：

```kotlin
/**
 * ARGB_8888 → 紧凑 I420（BT.601 limited range）
 * argb：Bitmap.getPixels 取出的像素；width / height 必须为偶数
 * out：复用的输出数组，长度 >= width * height * 3 / 2
 */
fun argbToI420(argb: IntArray, width: Int, height: Int, out: ByteArray) {
    val frameSize = width * height
    var yIndex = 0
    var uIndex = frameSize
    var vIndex = frameSize + frameSize / 4

    for (y in 0 until height) {
        for (x in 0 until width) {
            val color = argb[yIndex]
            val r = (color shr 16) and 0xFF
            val g = (color shr 8) and 0xFF
            val b = color and 0xFF

            val yy = ((66 * r + 129 * g + 25 * b + 128) shr 8) + 16
            out[yIndex] = yy.coerceIn(16, 235).toByte()

            // 色度按 2x2 取样，只在偶数行、偶数列写入
            if (y and 1 == 0 && x and 1 == 0) {
                val u = ((-38 * r - 74 * g + 112 * b + 128) shr 8) + 128
                val v = ((112 * r - 94 * g - 18 * b + 128) shr 8) + 128
                out[uIndex++] = u.coerceIn(16, 240).toByte()
                out[vIndex++] = v.coerceIn(16, 240).toByte()
            }
            yIndex++
        }
    }
}
```

调用方式：

```kotlin
private val pixels = IntArray(width * height)
private val i420 = ByteArray(width * height * 3 / 2)

bitmap.getPixels(pixels, 0, width, 0, 0, width, height)
argbToI420(pixels, width, height, i420)
```

> 上面是纯 Kotlin 实现，便于理解与自测，但 1080p 逐像素循环在中低端机上开销明显。生产环境建议改用 **libyuv**（`ARGBToI420`）或 GPU 方案；也可以先降到 720p 再推流。SDK 内部虽然集成了 libyuv，但未对外暴露转换接口，需要业务侧自行引入。

### 4.3 从 YUV_420_888 生成 I420

若数据来自 `ImageReader` / 第三方采集（`YUV_420_888`），需要处理三件事再送入：

- `rowStride` 可能大于 `width` → 逐行按 `width` 拷贝，去掉行尾 padding。
- `pixelStride` 可能为 2（半平面 NV12/NV21 形态）→ 按步长抽取，拆成独立的 U、V 平面。
- U、V 顺序必须是 **I420（先 U 后 V）**，NV21 的 VU 顺序需要交换。

这部分同样推荐直接用 libyuv 的 `Android420ToI420`，自己写循环容易在 stride/pixelStride 组合上出错。

## 5. 持续送帧

```kotlin
customTrack?.inputData(
    yuv = i420,
    width = width,
    height = height,
    strideY = width,
    strideU = width / 2,
    strideV = width / 2,
    rotation = 0,
    stamp = System.nanoTime()
)
```

参数要点：

| 参数 | 要求 |
| --- | --- |
| `rotation` | 只取 `0` / `90` / `180` / `270`。它是**帧元数据**，不会改变 `yuv` 里的像素排布，由编码与远端渲染侧完成旋转。画面本身已经是正向时传 `0`。 |
| `stamp` | 单位**纳秒**，与 Camera2 的 `timestampNs` 同一口径，直接用 `System.nanoTime()` 即可。必须**单调递增**，时间戳回退或跳变会导致远端卡顿、码率控制异常。 |

线程与节奏：

- **不要在主线程送帧**。`inputData` 是同步调用，内部会做拷贝、必要的对齐缩放并提交编码，1080p 下单帧耗时不可忽略。建议用一条独立的 `HandlerThread`。
- **按预设帧率节流**。超过 `maxFps` 的高频送帧不会提升画质，只会白白增加 CPU 与内存带宽开销。
- **静态画面也要持续送帧**。停止送帧远端会停在最后一帧；若画面长时间不变，可按最低帧率（如 1～2 fps）继续送同一帧以维持流的活性。
- **复用输出数组**。`inputData` 返回后内部已完成数据拷贝，业务侧可立即复用同一个 `ByteArray`，避免每帧新建对象造成 GC 抖动。

## 6. 停止与清理

```kotlin
private fun stopCustomPush() {
    stopFrameLoop()                              // 先停止送帧
    customTrack?.let {
        rtcEngine.unPublishLocalVideo(it, null)  // 再取消发布
    }
    customTrack = null
}
```

- **先停送帧、再取消发布**，顺序反了会有若干帧被丢弃（无害，但日志里会有无效调用）。
- 与摄像头一致，快速连续 `publish` / `unPublish` 时，中间被合并的调用可能不回调，请以最后一次调用的回调或最终状态为准。
- `leave()` 会释放流媒体引擎，轨道实例仍在但发布状态已失效，**重新入会后必须重新 `publishLocalVideo`**。
- `releaseSDK()` 还会清空本地轨道缓存，之后需重新 `getLocalCustomVideoTrack`。

> **本地预览**：`LocalCustomVideoTrack` 继承了 `addPlayView` 等渲染方法，但 SDK **不会**把 `inputData` 送入的帧回显到这些控件上（本地回显只对摄像头轨道生效）。自定义推流的本地预览请直接显示你自己的数据源（如白板 View 本身），不需要给本轨道添加渲染控件。

## 7. 完整示例

一个把 `Bitmap` 按固定帧率推流的最小封装：

```kotlin
class CustomVideoPusher(
    private val rtcEngine: RTCEngine,
    private val width: Int = 1280,
    private val height: Int = 720,
    private val fps: Int = 10
) {
    private val preOpt = PreOptionCustomVideo(
        capture = CustomVideoCaptureOptions(width, height, fps, 1200 * 1024),
        publish = VideoPublishOptions(
            desc = TrackDesc.TRACK_CUSTOM.value,
            codec = CodecType.H264,
            maxBitrate = 1200 * 1024,
            width = width,
            height = height,
            maxFps = fps,
            props = null,
            simulcasts = null
        )
    )

    private val pixels = IntArray(width * height)
    private val i420 = ByteArray(width * height * 3 / 2)

    private var track: LocalCustomVideoTrack? = null
    private var thread: HandlerThread? = null
    private var handler: Handler? = null
    private var running = false

    /** 帧源：由业务实现，返回当前要推送的画面 */
    var frameProvider: (() -> Bitmap?)? = null

    fun start() {
        if (rtcEngine.isAudience()) return

        val customTrack = rtcEngine.getLocalCustomVideoTrack(preOpt)
        track = customTrack

        rtcEngine.publishLocalVideo(customTrack, null, object : RTCResultListener {
            override fun onSuccess() = startLoop()
            override fun onFail(code: Int) {
                // 102202 未入会 / 102207 观众身份 / 其他
            }
        })
    }

    private fun startLoop() {
        if (running) return
        running = true
        thread = HandlerThread("custom-video-pusher").apply { start() }
        handler = Handler(thread!!.looper)
        handler?.post(pushTask)
    }

    private val pushTask = object : Runnable {
        override fun run() {
            if (!running) return
            val startAt = SystemClock.elapsedRealtime()

            frameProvider?.invoke()?.let { bitmap ->
                if (bitmap.width == width && bitmap.height == height) {
                    bitmap.getPixels(pixels, 0, width, 0, 0, width, height)
                    argbToI420(pixels, width, height, i420)
                    track?.inputData(
                        yuv = i420,
                        width = width,
                        height = height,
                        strideY = width,
                        strideU = width / 2,
                        strideV = width / 2,
                        rotation = 0,
                        stamp = System.nanoTime()
                    )
                }
            }

            // 按目标帧率节流，扣除本帧实际耗时
            val cost = SystemClock.elapsedRealtime() - startAt
            val delay = (1000L / fps - cost).coerceAtLeast(0L)
            handler?.postDelayed(this, delay)
        }
    }

    fun stop() {
        running = false
        handler?.removeCallbacksAndMessages(null)
        thread?.quitSafely()
        thread = null
        handler = null

        track?.let { rtcEngine.unPublishLocalVideo(it, null) }
        track = null
    }
}
```

使用：

```kotlin
val pusher = CustomVideoPusher(rtcEngine)
pusher.frameProvider = { whiteboardView.snapshotBitmap() }   // 业务侧提供画面

// 入会成功后开始
pusher.start()

// 结束推流 / 离会前
pusher.stop()
```

## 8. 排查对照表

| 现象 | 常见原因 |
| --- | --- |
| 远端完全看不到画面 | 未发布就送帧；`publishLocalVideo` 失败未处理（观众身份 / 未入会）；当前是 OOK 引擎，帧被丢弃 |
| 远端画面停在某一帧 | 送帧循环被中断（线程退出、异常吞掉）；`leave()` 后重新入会但没有重新发布 |
| 画面花屏、斜向错位 | `stride` 传了带 padding 的值；U / V 平面顺序颠倒（NV21 未换序）；数组长度与 `width × height` 不匹配 |
| 画面颜色异常（偏紫 / 偏绿） | U、V 平面写反；转换用了错误的色彩范围（full range 与 limited range 混用） |
| 画面右侧或底部有绿边 | 上游数据带行 padding 未去除；宽高传了奇数 |
| 画面方向不对 | `rotation` 与实际像素排布不匹配 —— 像素已经旋转过就传 `0`，不要重复旋转 |
| 远端卡顿、码率忽高忽低 | `stamp` 非单调递增或单位不是纳秒；送帧节奏抖动过大 |
| 本地 CPU 占用高、发热 | 在主线程送帧；送帧频率超过 `maxFps`；用纯 Java/Kotlin 循环做 1080p 色彩转换 |
| 本地预览看不到 | 预期行为，SDK 不回显自定义帧，需业务侧自绘 |

## 相关文档

- [LocalCustomVideoTrack](/zh/rtc/android/api-reference/LocalCustomVideoTrack)：接口与参数完整定义
- [自定义视频流预设](/zh/rtc/android/presets/custom-video)：`PreOptionCustomVideo` 字段与内置预设
- [RTCEngine](/zh/rtc/android/api-reference/RTCEngine)：`getLocalCustomVideoTrack` / `publishLocalVideo` / `unPublishLocalVideo`
- [快速开始](/zh/rtc/android/quickstart)：入会、发布、订阅的最小主线流程
