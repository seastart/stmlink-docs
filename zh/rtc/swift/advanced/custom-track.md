---
title: "自定义推流"
description: "使用自定义音视频轨道、视频处理器和音频处理器扩展 Swift SDK 的采集能力"
---

### 概述

当内置的麦克风、摄像头、屏幕共享采集不能满足需求时，Swift SDK 提供了两条扩展路径：

+ 自定义音视频轨道：由业务层自己提供音频或视频帧
+ 媒体处理器：在 SDK 已采集到的音视频帧上做处理

常见场景包括：

+ 用外部渲染引擎生成视频帧后推流
+ 把本地 PCM 音频、BGM 或 TTS 数据送入频道
+ 做美颜、虚拟背景、水印或 AI 视频处理
+ 对采集侧音频做变声、降噪或增强

---

### 自定义视频轨道

创建自定义视频轨道：

```swift
let customVideoTrack = srtc.createLocalCustomVideoTrack(desc: "canvas")
try await channel.publishLocalTrack(customVideoTrack)
```

后续由业务层持续调用 `pushFrame(...)` 送入视频帧：

```swift
customVideoTrack.pushFrame(pixelBuffer)
```

这里的关键点是：

+ 不需要 `startCapture()`
+ SDK 不负责帮你生成帧
+ 你需要自己保证持续产出 `CVPixelBuffer`

适合：

+ Metal / SceneKit / Unity / 游戏引擎画面推流
+ 自定义合成画面
+ AI 生成帧或图像处理后的输出

---

### 自定义音频轨道

创建自定义音频轨道：

```swift
let customAudioTrack = srtc.createLocalCustomAudioTrack(desc: "bgm")
try await channel.publishLocalTrack(customAudioTrack)
```

然后持续注入 PCM 数据：

```swift
customAudioTrack.pushAudioBuffer(pcmBuffer)
```

这类轨道同样不需要 `startCapture()`，因为音频来源不是 SDK 内部采集器，而是你自己准备好的 `AVAudioPCMBuffer`。

适合：

+ 播放背景音乐并推送到频道
+ 把本地文件解码后的 PCM 数据送进 RTC
+ 语音合成、语音克隆、外部 DSP 引擎输出

---

### 最小流程总结

无论是自定义音频还是自定义视频，整体模型都是一样的：

```swift
let track = srtc.createLocalCustomVideoTrack(desc: "custom")
try await channel.publishLocalTrack(track)

// 之后由业务层持续送帧
track.pushFrame(pixelBuffer)
```

也就是说，SDK 管的是“发布和传输”，你管的是“媒体数据生产”。

---

### 视频处理器链

如果你的需求不是“自己产出新视频帧”，而是“处理已有采集帧”，更适合使用 `videoProcessors`：

```swift
final class PassThroughProcessor: VideoProcessor {
    func processVideoFrame(_ frame: VideoFrame) -> VideoFrame? {
        // 这里可以替换 pixelBuffer、加滤镜、打水印
        return frame
    }
}

let cameraTrack = srtc.createLocalCameraTrack(preset: .h720p)
cameraTrack.videoProcessors = [PassThroughProcessor()]
try await cameraTrack.startCapture()
try await channel.publishLocalTrack(cameraTrack)
```

处理器按数组顺序串行执行：

+ 返回新的 `VideoFrame`，继续流转
+ 返回 `nil`，这一帧会被丢弃

这更适合：

+ 美颜
+ 虚拟背景
+ 视频水印
+ AI 分割或视觉增强

---

### 音频处理器

音频处理器挂在 `SRTC` 主入口上，而不是某一个单独轨道上：

```swift
final class MyAudioProcessor: NSObject, AudioProcessor {
    func audioProcessingInitialize(sampleRate sampleRateHz: Int, channels: Int) {}

    func audioProcessingProcess(audioBuffer: AudioBuffer) {
        // 可原地修改 Float 采样值
    }

    func audioProcessingRelease() {}
}

srtc.audioCaptureProcessor = MyAudioProcessor()
```

需要注意：

+ `audioCaptureProcessor` 是采集后处理
+ `audioRenderProcessor` 是远端播放前处理
+ 这是全局能力，不是 per-track 能力

因此如果你的需求是“只对某一路麦克风做局部处理”，就要先确认这种全局模型是否符合你的业务预期。

---

### 如果只是想观察远端音频数据

那就不要用 `AudioProcessor`，而应该用 `AudioRenderer`：

```swift
final class MyTranscriber: AudioRenderer {
    func render(pcmBuffer: AVAudioPCMBuffer) {
        // 将 PCM 数据送去做转写或录制
    }
}

let renderer = MyTranscriber()
remoteAudioTrack.add(audioRenderer: renderer)
```

两者区别很明确：

+ `AudioProcessor`：可修改音频
+ `AudioRenderer`：只观察，不修改

---

### 选择建议

如果你的目标是：

+ 自己生成音视频数据并推流：用自定义 Track
+ 处理 SDK 已采集到的本地视频：用 `videoProcessors`
+ 处理采集侧或播放侧音频：用 `audioCaptureProcessor` / `audioRenderProcessor`
+ 读取远端 PCM 做分析或转写：用 `AudioRenderer`

不要把这几种机制混在一起理解。它们解决的是四类不同问题。
