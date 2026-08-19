---
title: "屏幕共享"
description: "SRTC Swift SDK 在 macOS 与 iOS 上的屏幕共享接入方式与平台差异"
---

### 平台差异

| 平台 | 支持情况 | 说明 |
| --- | --- | --- |
| macOS 12.3+ | 显示器 / 窗口共享 | 基于 `ScreenCaptureKit`，业务侧先让用户选源 |
| iOS 应用内采集 | 只能采到本 App 的画面 | 默认方式，零额外集成 |
| iOS 全屏采集 | 能采整个系统屏幕 | 需集成 Broadcast Upload Extension，见下 |
| macOS 系统音频 | 支持 | 传 `audioPreset` 即可 |
| iOS 系统音频 | 不支持 | 两种采集方式都不支持，SDK 会忽略屏幕音频采集选项 |

iOS 上的两种采集方式由 `createLocalScreenTrack(mode:)` 选择，默认 `.inApp`：

```swift
// 应用内采集：只有本 App 的画面，切到其它 App 后对端看到的画面会停住
let track = srtc.createLocalScreenTrack(preset: .h1080p)

// 全屏采集：整个系统屏幕，切到任何 App 都继续共享
let track = srtc.createLocalScreenTrack(
    preset: .h720p,
    mode: .broadcast(appGroup: "group.your.app.group")
)
```

---

### 基本用法

#### 默认创建屏幕共享轨道

```swift
let screenTrack = srtc.createLocalScreenTrack(preset: .h1080p)
try await screenTrack.startCapture()
try await channel.publishLocalTrack(screenTrack)
```

如果你不需要系统音频，这是最直接的接法。

---

### macOS：选择显示器或窗口

macOS 下，业务层需要先枚举采集源，再把用户选中的源传给 SDK：

```swift
import SRTC

@available(macOS 12.3, *)
func startScreenShare(srtc: SRTCEngine, channel: Channel) async throws {
    let displays = try await ScreenCaptureSources.availableDisplays()
    let windows = try await ScreenCaptureSources.availableWindows()

    // 业务层自行展示选择 UI，这里以第一块显示器为例
    let selectedSource = displays.first

    let screenTrack = srtc.createLocalScreenTrack(
        source: selectedSource,
        preset: .h1080p
    )
    try await screenTrack.startCapture()
    try await channel.publishLocalTrack(screenTrack)
}
```

这里要注意一个设计边界：

+ SDK 负责“发现可共享的源”和“实际开始采集”
+ 业务层负责“如何把显示器 / 窗口列表展示给用户”

这样做的好处是 SDK 不绑定任何特定 UI 方案，SwiftUI、AppKit、TCA、MVVM 都能接入。

---

### macOS：同时采集系统音频

如果你要在屏幕共享时一起发送系统音频，可以传入 `audioPreset`：

```swift
let screenTrack = srtc.createLocalScreenTrack(
    source: selectedSource,
    preset: .h1080p,
    audioPreset: .default
)

try await screenTrack.startCapture()
try await channel.publishLocalTrack(screenTrack)
```

发布 `LocalScreenTrack` 时，如果它内部存在 `audioTrack`，SDK 会自动把屏幕音频一并走音频混音链路发送出去。

---

### iOS：应用内屏幕采集

iOS 下不需要传入 `source`：

```swift
let screenTrack = srtc.createLocalScreenTrack(preset: .h1080p)
try await screenTrack.startCapture()
try await channel.publishLocalTrack(screenTrack)
```

需要明确的是：

+ 这里是应用内采集模型，不是桌面级窗口选择模型
+ 用户切到别的 App 后就采不到内容了，对端画面会停住
+ 即便传入 `audioPreset`，iOS 也不会采集系统音频

---

### iOS：全屏采集（Broadcast Extension）

要采整个系统屏幕，iOS 只提供一条路：ReplayKit 的 **Broadcast Upload Extension**。
采集发生在系统拉起的独立扩展进程里，SDK 负责把帧跨进程送回 App 再编码发送，
业务侧要做的是把扩展 target 建起来。

#### 一、建扩展 target

Xcode **File → New → Target → Broadcast Upload Extension**，取消勾选 “Include UI Extension”。
给这个 target 加依赖 `SRTCBroadcastKit`（**不要**加 `SRTC`），把模板生成的 `SampleHandler`
整个替换成：

```swift
import SRTCBroadcastKit

class SampleHandler: SRTCBroadcastSampleHandler {}
```

采集、缩放、跨进程传输都在基类里，正常情况下不需要重写任何方法。

<Warning>
扩展 target 只能链接 `SRTCBroadcastKit`。扩展进程的内存上限是 **50MB**，链上包含 WebRTC 的
`SRTC` 会让系统在采集过程中把扩展杀掉。反过来，`SRTCBroadcastKit` 也不要加到 App target
上——App 侧的 `SRTC` 里已经含有同一份代码。
</Warning>

#### 二、配 App Group

App 与扩展需要一个共同的 App Group 来交换采集参数、并让跨进程通道落脚（App Group 需先在
Apple 开发者后台注册，两个 Bundle ID 的描述文件都要带上这个能力）：

1. App target 与扩展 target 都开启 **App Groups** 能力，勾选同一个 group；
2. 在**扩展**的 Info.plist 里写上它：

```xml
<key>SRTCAppGroupIdentifier</key>
<string>group.your.app.group</string>
```

#### 三、创建轨道并开始监听

```swift
let screenTrack = srtc.createLocalScreenTrack(
    preset: .h720p,
    mode: .broadcast(appGroup: "group.your.app.group")
)
screenTrack.delegates.add(delegate: self)

try await screenTrack.startCapture()               // 只是开始监听，此时还没有画面
try await channel.publishLocalTrack(screenTrack)
```

<Note>
`startCapture()` 成功**不代表已经有画面**，它只表示 SDK 已就绪、在等扩展连上来。
用户什么时候发起广播不由 App 决定，所以监听必须提前开着。
</Note>

#### 四、让用户发起广播

全屏采集只能由用户从系统 UI 发起，App 无法代替用户点。SDK 封装了系统选择器：

```swift
import SRTC
import SwiftUI

struct ShareButton: View {
    var body: some View {
        SRTCBroadcastPicker(
            preferredExtension: "com.your.app.broadcast",   // 扩展的 Bundle ID
            title: "开始共享"
        )
        .frame(width: 64, height: 32)
    }
}
```

UIKit 用 `SRTCBroadcastPickerView`。用户点击后会看到系统的广播选择面板，选中你的扩展并点
“开始直播”，画面才真正开始传输。

#### 五、监听真正的开始与结束

用户可能从系统胶囊（屏幕顶部的红色计时器）直接停止共享，这个动作发生在 App 之外，
必须靠事件感知：

```swift
extension MyState: TrackDelegate {
    func screenBroadcastDidStart(_ track: Track) {
        // 扩展已连上，画面开始传输 —— 这才是"共享中"
    }

    func screenBroadcastDidFinish(_ track: Track, reason: String) {
        // 用户点了系统胶囊、或广播被系统中断。监听仍然保留，用户可以再次发起
    }
}
```

两个状态要分清：

| 属性 / 事件 | 含义 |
| --- | --- |
| `track.isCapturing` | 监听已就绪（`startCapture()` 成功后为 `true`） |
| `track.isBroadcastActive` | 扩展正在推流，**对端能看到画面** |
| `screenBroadcastDidStart` | 从"等待"进入"共享中" |
| `screenBroadcastDidFinish` | 用户或系统结束了广播 |

展示"共享中"这类 UI 状态时应该看 `isBroadcastActive`。

---

### 停止共享

```swift
try await channel.unpublishLocalTrack(screenTrack)
try await screenTrack.stopCapture()
```

建议遵循“先取消发布，再停止采集”的顺序，这样频道侧状态和本地硬件状态更一致。

iOS 全屏采集下还有一点：ReplayKit 规定**只有扩展自己能结束广播**，宿主 App 只能发出请求。
`stopCapture()` 会通知扩展结束，扩展随后自行退出、系统胶囊消失——所以从调用到胶囊消失之间
会有很短的延迟，这是平台行为，不是调用没生效。

---

### 常见问题

#### 为什么 macOS 必须先让用户选源？

因为桌面采集的本质是“用户授权共享哪一块屏幕或哪一个窗口”，SDK 无法替用户做出这个选择。

#### 为什么 iOS 不支持系统音频？

这是平台能力边界，不是 SDK 层面的简单开关。Swift SDK 在 iOS 上会明确忽略屏幕音频配置，而不是制造一个看起来支持、实际无效的接口。

#### 全屏共享在模拟器上不出画面？

全屏采集依赖真实签名与 App Group，**模拟器跑不通，必须真机**。模拟器上只能验证工程能编过。

#### 扩展的日志去哪看？

扩展是独立进程，日志不会出现在 Xcode 主 App 的控制台。用 **Console.app** 连上设备，
按 subsystem `com.srtc.broadcast` 过滤。常见两条：

+ “请先在 App 内开启屏幕共享，再从系统菜单开始广播”——用户先点了系统胶囊，App 侧还没
  `startCapture()`，扩展连不上宿主就会主动结束；
+ “未配置 App Group”——扩展 Info.plist 里的 `SRTCAppGroupIdentifier` 漏了或拼错。

#### 全屏共享时画面偶尔跳帧？

屏幕帧在宿主侧走固定容量的缓冲池，编码来不及时会合并掉中间帧、只保留最新一帧，
这是有意的保护（否则内存会无上限增长）。SDK 会周期性输出 `received / delivered /
coalesced / footprint` 的汇总日志，`coalesced` 持续增长说明当前分辨率/帧率对设备偏高，
可以换用更低的 `ScreenPreset`。
