---
title: "虚拟背景"
description: "Swift SRTC 音视频 SDK 的虚拟背景：人像分割后做背景虚化或背景替换，不需要授权密钥；本页交代它为什么开一次就作用于全部摄像头轨道、切摄像头不用自己补、低端机保帧率的两个参数，以及 1.4.0 抬高的系统要求"
---

虚拟背景在摄像头采集链路上做人像分割，把人像之外的区域替换成虚化或指定图片。它是自研组件，装载**不需要授权密钥**。

<Note>
接口挂在 `SRTCEngine` 上，但状态是**整机一份**（内部是 `SRTCVirtualBackground.shared`）：一个推理会话几十 MB、装载上百毫秒，多个引擎实例、多个频道共用同一份配置。不存在「只给某一个频道开虚拟背景」的用法。

开启后**自动作用于所有摄像头轨道**，包括开启之后才新建的那些（`createLocalCameraTrack` 会自动带上）。你不需要往 `videoProcessors` 里挂任何东西。

**切前后摄像头、切换摄像头设备后不用做任何事**：SDK 内部会清掉帧间状态并继续生效。
</Note>

<Warning>
`1.4.0` 起最低系统要求抬到 **iOS 16.0 / macOS 14.0**（此前为 iOS 13 / macOS 10.15）。低于此下限的工程解析不到 1.4.0 及以后的版本，详见 [集成方式](/zh/rtc/swift/integration)。

推理运行时 `onnxruntime` 已**静态链入** `SRTC.xcframework`，你不需要额外声明任何依赖、也不需要 embed 任何东西。
</Warning>

---

### step 1：**装载虚拟背景组件**

建议在需要用到虚拟背景前装载，例如进入会议页面时。`modelPath` 传 `nil` 使用 SDK 内置的人像分割模型。

```swift
/// 装载会加载模型并建立推理会话，耗时百毫秒级 —— 不要在主线程或采集线程调
Task.detached(priority: .userInitiated) {
    do {
        try srtc.installVirtualBackground()          // modelPath 传 nil 用内置模型
    } catch {
        print("虚拟背景装载失败:", error.localizedDescription)
    }
}
```

抛出的错误：

| **错误** | **说明** |
| --- | --- |
| `virtualBackgroundAlreadyInstalled` | 组件已装载，本次指令被丢弃 |
| `virtualBackgroundModelNotFound(String)` | 模型文件不存在，检查 `modelPath` |
| `virtualBackgroundSessionFailed(String)` | 推理会话创建失败，属于运行环境问题 |

---

### step 2：**设置背景效果**

背景虚化与背景替换**互斥，后调用的生效**。两个接口在装载前调用也会被记住，装载完成后自动生效，因此不必关心与 `installVirtualBackground()` 的先后顺序。

```swift
/// 设置背景虚化，level 取值 1~10，默认 5（超出范围会被收敛到边界值）
srtc.setVirtualBackgroundBlur(level: 5)

/// 设置背景替换，按 cover 裁剪不拉伸；传 nil 表示取消替换回到虚化
srtc.setVirtualBackgroundImage(SRTCNativeImage(named: "background"))
```

`SRTCNativeImage` 是平台原生图片类型的别名（iOS 上是 `UIImage`、macOS 上是 `NSImage`），另有一个接收 `CGImage` 的重载。

---

### step 3：**开启或关闭虚拟背景**

装载后默认**不开启**，需要显式打开。关闭后是零开销直通：采集链路根本不会调到处理器，不跑推理也不做合成。

```swift
try srtc.enableVirtualBackground(true)

/// 查询开启状态
let enabled = srtc.isVirtualBackgroundEnabled
```

组件未装载时调用开关会抛 `virtualBackgroundNotInstalled`。关闭时会清掉帧间状态，下次开启从首帧重新收敛，不会闪出过期蒙版。

---

### step 4：**低端机保帧率（可选）**

默认每帧都跑一次人像分割。低端机上可以调大推理间隔，用蒙版复用换帧率；此时再按需打开蒙版对齐消除拖影。

```swift
/// 分割每 N 帧跑一次（合成仍每帧跑），默认 1
srtc.setVirtualBackgroundInferenceInterval(2)

/// 蒙版对齐，默认 false
srtc.setVirtualBackgroundMaskSync(true)
```

| **参数** | **默认值** | **说明** |
| --- | :---: | --- |
| `inferenceInterval` | `1` | 每 N 帧跑一次分割，小于 1 按 1 处理。调大可降低推理开销，代价是快速运动时蒙版跟随变慢 |
| `maskSync` | `false` | 开启后非推理帧不重新合成，画面与蒙版永远同一时刻，消除挥手时的错位拖影，代价是画面更新率降到蒙版率 |

<Note>
`inferenceInterval` 为 `1` 时，`setVirtualBackgroundMaskSync(_:)` 开与不开没有任何区别——那时每帧都拿当前帧推理并当场合成，本来就是对齐的。它只在调大推理间隔后才起作用。
</Note>

帧率不稳时按帧数节流管不住实际推理频率，可以改按时间节流（`inferenceIntervalMs`，两者同时生效）：

```swift
srtc.virtualBackground.inferenceIntervalMs = 66   // 推理最快 ~15 次/秒
```

---

### step 5：**卸载虚拟背景组件**

不再使用时卸载，释放推理会话与相关缓冲。已设置的效果参数不会被清掉，下次装载后仍然生效。

```swift
srtc.uninstallVirtualBackground()
```

---

### 出错时丢帧，不会闪出真实背景

分割失败或输出缓冲池被耗尽时，SDK **丢掉这一帧**，而不是把未处理的摄像头原始画面送出去——那会把真实背景闪给对端，对虚拟背景来说是隐私事故。代价是对端看到画面短暂卡顿。

丢帧计数可以直接读，持续增长说明分割一直失败、或者你的处理器链下游在跨帧扣留输出缓冲：

```swift
print(srtc.virtualBackground.droppedFrameCount)
```

`srtc.virtualBackground` 还提供 `isInstalled`、`isEnabled`、`effect`、`blurLevel` 等只读状态，用于把 UI 与 SDK 的真实状态对齐（例如面板重新打开时回填控件）。

---

### 屏幕共享与自定义视频轨道

虚拟背景只自动作用于摄像头轨道。屏幕共享、自定义视频轨道默认**不过**虚拟背景——要给它们加效果，把这个实例手动放进那条轨道的 `videoProcessors` 即可（它本身就是一个 `VideoProcessor`）：

```swift
customTrack.videoProcessors = [srtc.virtualBackground]
```

自己接管采集（`LocalVideoTrack` + 自定义采集器）时，采集链路重建后需要手动清一次帧间状态，否则时域平滑仍压着旧画面的蒙版：

```swift
srtc.virtualBackground.reset()      // 只清帧间状态，配置不受影响
```

摄像头轨道不需要这一步，SDK 在设备切换里已经调过了。

---

### 本地预览与推流的一致性

虚拟背景开启时，本地预览显示的就是处理后的画面，与对端看到的是同一份数据（预览走 `track.addRenderer()`，渲染的是处理器之后的帧）；关闭后本地预览回到摄像头原始画面。

---

### 性能开销

人像分割固定走 CPU 推理，不启用 CoreML：模型只有 256×256，算子无法被 CoreML 完整承接，每帧在 CPU 与 CoreML 之间反复搬运数据的开销超过省下的算力，实测是负优化。

算法实现与 Objective-C 版同源（同一份人像分割 + 蒙版后处理），单帧耗时量级可参考 [iOS SDK 的虚拟背景](/zh/rtc/ios/advanced/virtual-background#性能开销)实测数据。真机上先按默认参数（每帧分割）测一轮，超出帧预算再按 step 4 调大推理间隔。

---

### 相关页面

+ [集成方式](/zh/rtc/swift/integration) —— 系统要求与集成步骤
+ [错误码](/zh/rtc/swift/error-codes) —— `SRTCError` 的虚拟背景相关取值
+ [自定义推流](/zh/rtc/swift/advanced/custom-track) —— 自己接管采集时的处理器链
