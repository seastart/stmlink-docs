---
title: "音频路由（iOS）"
description: "iOS 上用 AudioRouteSession 控制声音从扬声器还是听筒出，理解持久/临时两层设置、外设为何不可主动切换，以及入会即申请麦克风权限的原因"
---

### 概述

iOS 上「声音从哪出」由 `AudioRouteSession.shared` 管理。它只在 iOS 存在——macOS 是独立的输入 / 输出硬件设备模型，走 [设备管理](/zh/rtc/swift/advanced/device-management) 的 `setOutputDevice(_:)`。

这套 API 的设计基准是主流 RTC SDK（声网 Agora、腾讯 TRTC、LiveKit）的通行做法，有三条需要先理解的原则，否则很容易写出「设置了但没生效」的代码。

---

### 原则一：只能切扬声器和听筒

`AudioRouteTarget` 只有两个值：

```swift
public enum AudioRouteTarget {
    case speaker    // 扬声器（免提）
    case earpiece   // 听筒
}
```

**SDK 不提供「切换到蓝牙耳机 / 有线耳机」的 API。** 这不是功能缺失，而是 iOS 平台限制：系统没有可靠手段让 App 指定某个具体外设（无法在多个已连接设备中选择，A2DP 与 HFP 之间的切换也由系统按会话类别决定）。Agora、TRTC、LiveKit 同样都没有这类接口。

外接设备的行为是：

+ **插入时系统自动切过去**，多个设备同时连接时取最后连接的那个
+ **拔出时** SDK 会回落到你设置的路由
+ 需要让用户主动选择蓝牙 / AirPlay 时，用系统提供的 `AVRoutePickerView`

<Warning>
当前正在使用蓝牙或有线耳机时，`setAudioRoute(.speaker)` **不会生效**，音频仍然从外设输出。iOS 不允许把输出从外设抢回内置扬声器。这与 Agora 等 SDK 的行为一致，SDK 不会因此抛错，只会记录日志。请通过 `currentRoute` 判断实际结果，不要假设调用成功就已切换。
</Warning>

---

### 原则二：持久设置与临时设置分两层

| 层 | API | 生效时机 | 说明 |
| :--- | :--- | :--- | :--- |
| 持久 | `defaultAudioRoute` | 入会前设定，长期有效 | 相当于 Agora 的 `setDefaultAudioRouteToSpeakerphone` |
| 临时 | `setAudioRoute(_:)` | 入会后调用 | 相当于 Agora 的 `setEnableSpeakerphone` |

优先级是 **临时 > 持久**。外设拔出后，SDK 按这个优先级回落。

#### 持久设置：入会前定好默认行为

```swift
// 语音通话场景：默认走听筒
AudioRouteSession.shared.defaultAudioRoute = .earpiece

// 视频会议场景：默认走免提
AudioRouteSession.shared.defaultAudioRoute = .speaker
```

<Tip>
如果没有「通话中让用户临时切换」的需求，**只用这一个就够了**。设置一次，之后插拔耳机的回落都会遵循它。
</Tip>

#### 临时设置：通话中切换

```swift
// 用户点了免提按钮
AudioRouteSession.shared.setAudioRoute(.speaker)

// 用户点了听筒
AudioRouteSession.shared.setAudioRoute(.earpiece)

// 放弃临时选择，回到 defaultAudioRoute
AudioRouteSession.shared.clearAudioRouteOverride()
```

临时设置会被系统行为冲掉（插拔外设、系统通话等），这是设计如此，不是 bug。

---

### 原则三：入会即建立音频通道

**加入频道时 SDK 就会建立通话音频通道并保持到离会**，无论你有没有开麦。开不开麦只决定「推不推流」，不影响底层音频采集是否运行。

这带来两个必须提前告知产品和用户的结果：

<Warning>
**加入频道时会申请麦克风权限**，即使用户只打算旁听。请确保 `Info.plist` 含 `NSMicrophoneUsageDescription`，否则 App 会崩溃。

**加入频道期间 iOS 状态栏会显示橙色麦克风指示点。** 音频采集确实在运行，这与 Zoom、腾讯会议等会议类 App 的表现一致，不是 SDK 在偷偷录音。
</Warning>

为什么必须这样做？因为 iOS 上音频会话不处于 VoIP 通话模式时，**路由控制整体不可靠**——听筒输出只在 `.playAndRecord` 会话类别下存在，而按需临时升级类别经真机验证是切不过去的。腾讯 TRTC 文档记录了同一现象：不开麦时走媒体通道，此时无法设置外放或听筒。

如果用户拒绝了麦克风权限，SDK 会降级到只播放模式：**仍然可以听到对方**，但听筒路由不可用，只能外放。

建议在 `Info.plist` 中同时声明后台音频能力，避免切到后台时音频被系统挂起：

```xml
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

---

### 查询当前状态

`currentRoute` 是**只读的五态**类型，包含 SDK 无法主动切换但需要如实上报的外设：

```swift
let session = AudioRouteSession.shared

session.currentRoute           // .speaker / .receiver / .bluetooth / .headset / .unknown
session.currentRoute.isExternal // 是否走在蓝牙或有线耳机上
session.effectiveRouteTarget   // 当前生效目标 = 临时覆盖 ?? 持久默认
session.routeOverride          // 临时覆盖，nil 表示没有
session.isBluetoothAvailable   // 蓝牙耳机是否在位
session.isHeadsetAvailable     // 有线耳机是否在位
session.isEngaged              // 音频通道是否已建立（入会中 / 采集中）
```

<Note>
注意区分 `currentRoute`（**实际**从哪出声，五态）和 `effectiveRouteTarget`（你**要求**的目标，两态）。插着耳机时前者是 `.bluetooth`，后者可能仍是 `.speaker`——这不是矛盾，是外设优先。UI 应该展示 `currentRoute`。
</Note>

---

### 监听路由变化

```swift
final class RouteObserver: AudioRouteSessionDelegate {
    init() {
        AudioRouteSession.shared.delegates.add(delegate: self)
    }

    func audioRouteSession(
        _ session: AudioRouteSession,
        didChangeRoute route: AudioRoute,
        from previousRoute: AudioRoute,
        reason: AVAudioSession.RouteChangeReason
    ) {
        // 已在主线程回调，可直接更新 UI
        print("路由变化：\(previousRoute.displayName) → \(route.displayName)")
    }

    func audioRouteSessionWasInterrupted(_ session: AudioRouteSession) {
        // 来电 / Siri / 其他 App 抢占
    }

    func audioRouteSessionDidRecoverFromInterruption(_ session: AudioRouteSession) {
        // 中断真正恢复后才触发（可能延后，见下）
    }

    func audioRouteSession(_ session: AudioRouteSession, didChangeCallState callState: AudioCallState) {
        // 系统通话状态：.incoming / .connected / .disconnected 等
    }
}
```

所有回调都在主线程执行，协议提供了默认空实现，只实现你关心的即可。

`reason` 参数值得关注，它区分了变化来源：`.oldDeviceUnavailable` 是拔出，`.newDeviceAvailable` 是插入，`.override` 是 App 主动覆盖。排查路由问题时这一项往往比结果本身更有价值。

---

### 中断与系统来电

SDK 通过 CallKit 感知系统通话状态，中断恢复不是一次性的：

+ 音频中断结束时，如果系统电话还没真正挂断，**不会**立即恢复——此时重激活音频会话必定失败
+ 恢复条件是「系统通话已结束」且「App 在前台」，不满足则保留待恢复状态
+ 会在回到前台时、以及通话结束若干秒后自动重试
+ 真正恢复成功后才触发 `audioRouteSessionDidRecoverFromInterruption`

业务层通常不需要自己处理这套时序，在恢复回调里刷新 UI 即可。

---

### 与 DeviceManager 的关系

`DeviceManager` 上的 iOS 音频方法是这套 API 的薄封装，语义对齐 Agora 的 `setEnableSpeakerphone`：

```swift
try DeviceManager.shared.setSpeakerOutputPreferred(true)   // 等价于 setAudioRoute(.speaker)
try DeviceManager.shared.setSpeakerOutputPreferred(false)  // 等价于 setAudioRoute(.earpiece)
DeviceManager.shared.isSpeakerOutputPreferred              // 当前是否走外放
```

<Note>
`DeviceManager.audioInputs()` 和 `setAudioInputDevice(_:)` 是**输入端口**层面的低阶接口，与「声音从哪出」是两件事，且不参与本文的回落策略。控制输出走向请使用 `AudioRouteSession`。
</Note>

---

### 完整示例

```swift
import SRTC

final class CallAudioController: AudioRouteSessionDelegate {
    private let session = AudioRouteSession.shared

    /// 入会前调用：定好默认行为
    func prepare(isVideoCall: Bool) {
        session.defaultAudioRoute = isVideoCall ? .speaker : .earpiece
        session.delegates.add(delegate: self)
    }

    /// 免提按钮
    func toggleSpeaker() {
        let next: AudioRouteTarget = session.currentRoute == .speaker ? .earpiece : .speaker
        session.setAudioRoute(next)

        // 外设在用时切换不会生效，据此给用户提示
        if session.currentRoute.isExternal {
            showToast("当前使用\(session.currentRoute.displayName)，请在系统控制中心切换")
        }
    }

    func audioRouteSession(
        _ session: AudioRouteSession,
        didChangeRoute route: AudioRoute,
        from previousRoute: AudioRoute,
        reason: AVAudioSession.RouteChangeReason
    ) {
        updateSpeakerButton(isOn: route == .speaker, isEnabled: !route.isExternal)
    }
}
```

---

### 常见问题

**切换没有生效**

按顺序排查：

1. 当前是否走在外设上（`currentRoute.isExternal`）——这种情况下切扬声器本就无效
2. 是否已入会或已开始采集（`isEngaged`）——未建立音频通道时设置只会被记录，等通道建立后套用
3. 麦克风权限是否被拒——被拒时会话降级，听筒不可用

**为什么不开麦也要麦克风权限**

见「原则三」。听筒输出只在可录音的会话类别下存在，这是 iOS 平台限制。

**入会后状态栏出现橙色圆点**

正常现象，音频采集确实在运行，与其他会议类 App 一致。

**模拟器上路由切换无效**

模拟器没有听筒和蓝牙路由，`availableInputs` 也不真实。**音频路由必须在真机上验证。**
