---
title: "音频路由（iOS）"
description: "会议中控制声音从扬声器还是听筒出：持久默认与临时切换两层、外设为什么不能主动切、以及入会即申请麦克风权限的原因"
---

### 概述

iOS 上「声音从哪出」由 `SMeetingEngine` 上的一组音频路由接口控制，仅 iOS 可用 —— macOS 是独立的输入 / 输出硬件设备模型，走 [设备管理](/zh/meeting/swift/advanced/device-management) 的 `setAudioOutput(deviceId:)`。

这套接口是底层 SRTC `AudioRouteSession` 的薄封装，不做二次状态缓存，因此会议层与底层不会出现两份漂移的状态。设计基准是主流 RTC SDK（声网 Agora、腾讯 TRTC、LiveKit）的通行做法，有三条需要先理解的原则，否则很容易写出「设置了但没生效」的代码。

底层机制的完整说明见 [SRTC · 音频路由](/zh/rtc/swift/advanced/audio-routing)，本页只讲会议层怎么用。

---

### 原则一：只能切扬声器和听筒

`AudioRouteTarget` 只有两个值 —— `.speaker`（扬声器 / 免提）和 `.earpiece`（听筒）。

**SDK 不提供「切换到蓝牙耳机 / 有线耳机」的接口。** 这不是功能缺失，而是 iOS 平台限制：系统没有可靠手段让 App 指定某个具体外设。Agora、TRTC、LiveKit 同样都没有这类接口。

外接设备的行为是：插入时系统自动切过去，拔出时 SDK 回落到你设置的路由；需要让用户主动选蓝牙 / AirPlay 时，用系统提供的 `AVRoutePickerView`。

<Warning>
正在使用蓝牙或有线耳机时，`setAudioRoute(.speaker)` **不会生效**，音频仍然从外设输出。iOS 不允许把输出从外设抢回内置扬声器，SDK 不会因此抛错，只会记录日志。请用 `currentAudioRoute` 判断实际结果，不要假设调用成功就已切换；`isExternalAudioRouteActive` 为 `true` 时应把「切外放」按钮置灰。
</Warning>

---

### 原则二：持久设置与临时设置分两层

| 层 | 接口 | 生效时机 | 对应 Agora 接口 |
| :--- | :--- | :--- | :--- |
| 持久 | `defaultAudioRoute` | 入会前设定，长期有效 | `setDefaultAudioRouteToSpeakerphone` |
| 临时 | `setAudioRoute(_:)` | 入会后调用 | `setEnableSpeakerphone` |

优先级是 **临时 > 持久**。外设拔出后，SDK 按这个优先级回落。

```swift
// 入会前：会议场景默认走免提
meeting.defaultAudioRoute = .speaker

// 会中：用户点了听筒按钮
meeting.setAudioRoute(.earpiece)

// 放弃临时选择，回到 defaultAudioRoute
meeting.clearAudioRouteOverride()
```

<Tip>
如果没有「会中让用户临时切换」的需求，**只用 `defaultAudioRoute` 就够了**。它落在 `AVAudioSession` 的 category option 上，是 Apple 表达「默认外放」的正规方式，比激活后再覆盖一次可靠得多。
</Tip>

临时设置会被系统行为冲掉（插拔外设、系统通话等），这是设计如此，不是 bug。

---

### 原则三：入会即建立通话音频通道

**加入会议时 SDK 就会建立通话音频通道并保持到离会**，无论你有没有开麦。开不开麦只决定「推不推流」，不影响底层音频采集是否运行。

<Warning>
**入会时会申请麦克风权限**，即使成员只打算旁听。请确保 `Info.plist` 含 `NSMicrophoneUsageDescription`，否则 App 会崩溃。

**入会期间 iOS 状态栏会显示橙色麦克风指示点。** 音频采集确实在运行，这与 Zoom、腾讯会议等会议类 App 的表现一致，不是 SDK 在偷偷录音。
</Warning>

为什么必须这样做？iOS 上听筒输出只存在于可录音的会话类别（`.playAndRecord`）下，而「平时只播放、要听筒时再临时升级」经真机验证是切不过去的 —— 通话通道常驻是路由可控的前提。

如果用户拒绝了麦克风权限，SDK 会降级到只播放模式：**仍然可以听到其他成员**，但听筒路由不可用，只能外放。

建议在 `Info.plist` 中同时声明后台音频能力，避免切到后台时音频被系统挂起：

```xml
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

---

### 查询当前状态

```swift
meeting.currentAudioRoute           // 系统实际路由（五态，含蓝牙 / 有线）
meeting.effectiveAudioRouteTarget   // 当前生效目标 = 临时覆盖 ?? 持久默认（两态）
meeting.audioRouteOverride          // 临时覆盖，nil 表示没有
meeting.isExternalAudioRouteActive  // 是否走在蓝牙或有线耳机上
meeting.isAudioSessionActive        // 通话音频通道是否已建立（入会后应为 true）
meeting.audioCallState              // 系统通话状态（CallKit 观察结果）
meeting.availableAudioRoutes()      // 系统音频端口快照，诊断 / 展示用
```

<Note>
注意区分 `currentAudioRoute`（**实际**从哪出声，五态）和 `effectiveAudioRouteTarget`（你**要求**的目标，两态）。插着耳机时前者是 `.bluetooth`，后者可能仍是 `.speaker` —— 这不是矛盾，是外设优先。UI 上要展示给用户的是 `currentAudioRoute`。

`availableAudioRoutes()` 返回的是端口快照，**不是可供用户选择的列表** —— 可控目标只有听筒和外放两个。
</Note>

---

### 监听路由变化

```swift
extension MeetingController: SMeetingDelegate {

    func meeting(_ meeting: SMeetingEngine, audioRouteDidChange data: AudioRouteChangeEventData) {
        // 已在主线程回调，可直接更新 UI
        updateSpeakerButton(
            isOn: data.route == .speaker,
            isEnabled: !meeting.isExternalAudioRouteActive
        )
    }

    func meetingAudioRouteDidRecoverFromInterruption(_ meeting: SMeetingEngine) {
        // 来电 / Siri 中断真正恢复后触发一次，刷新 UI 即可
    }
}
```

`AudioRouteChangeEventData` 带 `route`（变化后）、`previousRoute`（变化前）和 `reason`（系统给出的原因：`.oldDeviceUnavailable` 是拔出、`.newDeviceAvailable` 是插入、`.override` 是 App 主动覆盖）。排查路由问题时 `reason` 往往比结果本身更有价值。

音频路由事件**不依赖会议状态**，SDK 实例创建后就开始上报，入会前的设备检测页面也能用。

<Note>
中断恢复不是一次性的：音频中断结束时如果系统电话还没真正挂断，重激活必定失败。SDK 会等到「系统通话已结束」且「App 在前台」再重试，真正恢复成功后才触发 `meetingAudioRouteDidRecoverFromInterruption`。业务层不需要自己处理这套时序。
</Note>

---

### 与 setSpeakerOutputEnabled 的关系

[设备管理](/zh/meeting/swift/advanced/device-management) 里的 `setSpeakerOutputEnabled(_:)` 与本页的 `setAudioRoute(_:)` 是**同一机制的两种写法**，都落在系统的 `overrideOutputAudioPort` 上：

```swift
try meeting.setSpeakerOutputEnabled(true)   // 等价于 setAudioRoute(.speaker)
try meeting.setSpeakerOutputEnabled(false)  // 等价于 setAudioRoute(.earpiece)
```

要表达「长期默认外放」请用 `defaultAudioRoute`。不要在这两套之外自己再造第三套状态。

---

### 常见问题

**切换没有生效**

按顺序排查：

1. 当前是否走在外设上（`isExternalAudioRouteActive`）—— 这种情况下切扬声器本就无效
2. 是否已入会（`isAudioSessionActive`）—— 音频通道未建立时设置只会被记录，等通道建立后套用
3. 麦克风权限是否被拒 —— 被拒时会话降级，听筒不可用

**为什么不开麦也要麦克风权限**

见「原则三」。听筒输出只在可录音的会话类别下存在，这是 iOS 平台限制。

**模拟器上路由切换无效**

模拟器没有听筒和蓝牙路由，端口列表也不真实。**音频路由必须在真机上验证。**

---

### 相关页面

+ [设备管理](/zh/meeting/swift/advanced/device-management)
+ [媒体控制](/zh/meeting/swift/advanced/media-control)
+ [SRTC · 音频路由](/zh/rtc/swift/advanced/audio-routing)
