---
title: "虚拟背景"
description: "Swift SMeeting 会议 SDK 的虚拟背景：人像分割后做背景虚化或背景替换，不需要授权密钥；本页交代它为什么是设备级配置、切换摄像头与重新开摄像头后不用自己补、低端机保帧率的两个参数，以及 1.3.0 抬高系统要求的代价"
---

虚拟背景在摄像头采集链路上做人像分割，把人像之外的区域替换成虚化或指定图片。它是自研组件，装载**不需要授权密钥**。

<Note>
接口挂在 `SMeetingEngine` 上，但状态是**设备级**的：虚拟背景作用于进程内唯一的共享摄像头采集链路，设置会同时作用于全部会议与频道。同时加入多个房间时，不存在「只给某一个房间开虚拟背景」的用法。

会中**切换摄像头、关掉摄像头再打开、断线重连后都不需要自己补**——效果由采集链路每帧现取，轨道重建不会把它丢掉。
</Note>

<Warning>
`1.3.0` 起最低系统要求抬到 **iOS 16.0 / macOS 14.0**（此前为 iOS 13 / macOS 10.15）。低于此下限的工程解析不到 1.3.0 及以后的版本，详见 [集成方式](/zh/meeting/swift/integration)。

推理运行时 `onnxruntime` 已静态链入音视频层的 `SRTC.xcframework`，你不需要额外声明任何依赖；代价是 SDK 二进制增大约 29MB，**与你是否使用虚拟背景无关**。
</Warning>

---

### step 1：**装载虚拟背景组件**

建议在需要用到虚拟背景前装载，例如进入会议页面时。`modelPath` 传 `nil` 使用 SDK 内置的人像分割模型。

```swift
/// 装载会加载模型并建立推理会话，耗时百毫秒级 —— 不要在主线程或采集线程调
Task.detached(priority: .userInitiated) {
    do {
        try meeting.installVirtualBackground()       // modelPath 传 nil 用内置模型
    } catch {
        print("虚拟背景装载失败:", error.localizedDescription)
    }
}
```

抛出的错误（来自音视频层的 `SRTCError`）：

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
meeting.setVirtualBackgroundBlur(level: 5)

/// 设置背景替换，按 cover 裁剪不拉伸；传 nil 表示取消替换回到虚化
meeting.setVirtualBackgroundImage(SRTCNativeImage(named: "background"))
```

`SRTCNativeImage` 是平台原生图片类型的别名（iOS 上是 `UIImage`、macOS 上是 `NSImage`）。

---

### step 3：**开启或关闭虚拟背景**

装载后默认**不开启**，需要显式打开。关闭后是零开销直通，不再跑推理。

```swift
try meeting.enableVirtualBackground(true)

/// 查询开启状态
let enabled = meeting.isVirtualBackgroundEnabled
```

组件未装载时调用开关会抛 `virtualBackgroundNotInstalled`。关闭时会清掉帧间状态，下次开启从首帧重新收敛，不会闪出过期蒙版。

<Note>
虚拟背景是本地预处理，与会议状态无关：**入会前、入会后都能设**，也不受主持人静音/关摄像头等权限动作影响。摄像头没开时设置同样会被记住，开了摄像头就能看到效果。
</Note>

---

### step 4：**低端机保帧率（可选）**

默认每帧都跑一次人像分割。低端机上可以调大推理间隔，用蒙版复用换帧率；此时再按需打开蒙版对齐消除拖影。

```swift
/// 分割每 N 帧跑一次（合成仍每帧跑），默认 1
meeting.setVirtualBackgroundInferenceInterval(2)

/// 蒙版对齐，默认 false
meeting.setVirtualBackgroundMaskSync(true)
```

| **参数** | **默认值** | **说明** |
| --- | :---: | --- |
| `inferenceInterval` | `1` | 每 N 帧跑一次分割，小于 1 按 1 处理。调大可降低推理开销，代价是快速运动时蒙版跟随变慢 |
| `maskSync` | `false` | 开启后非推理帧不重新合成，画面与蒙版永远同一时刻，消除挥手时的错位拖影，代价是画面更新率降到蒙版率 |

<Note>
`inferenceInterval` 为 `1` 时，`setVirtualBackgroundMaskSync(_:)` 开与不开没有任何区别——它只在调大推理间隔后才起作用。
</Note>

---

### step 5：**卸载虚拟背景组件**

不再使用时卸载，释放推理会话与相关缓冲。已设置的效果参数不会被清掉，下次装载后仍然生效。

```swift
meeting.uninstallVirtualBackground()
```

---

### 出错时丢帧，不会闪出真实背景

分割失败或输出缓冲池被耗尽时，SDK **丢掉这一帧**，而不是把未处理的摄像头原始画面送出去——那会把真实背景闪给其它成员。代价是对端看到画面短暂卡顿。

丢帧计数与只读状态都在 `meeting.virtualBackground` 上（`droppedFrameCount`、`isInstalled`、`isEnabled`、`effect`、`blurLevel`），可用于把面板控件回填成 SDK 的真实状态：

```swift
print(meeting.virtualBackground.droppedFrameCount)
```

---

### 本地预览与推流的一致性

虚拟背景开启时，本地预览显示的就是处理后的画面，与其它成员看到的是同一份数据；关闭后本地预览回到摄像头原始画面。

更底层的用法（把虚拟背景挂到自定义视频轨道、自己接管采集时清帧间状态）见音视频层的 [虚拟背景](/zh/rtc/swift/advanced/virtual-background)。

---

### 相关页面

+ [集成方式](/zh/meeting/swift/integration) —— 系统要求与包体说明
+ [SMeetingEngine](/zh/meeting/swift/api-reference/SMeetingEngine#虚拟背景) —— 完整签名与参数
+ [音视频层的虚拟背景](/zh/rtc/swift/advanced/virtual-background) —— 诊断信息与自定义轨道用法
