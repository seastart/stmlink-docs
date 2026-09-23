---
title: "虚拟背景"
description: "iOS SMeeting 会议 SDK 的虚拟背景：人像分割后做背景虚化或背景替换，不需要授权密钥；本页交代它为什么是设备级配置、切换摄像头与断线重连后不用自己补，以及低端机保帧率的两个参数"
---

虚拟背景在摄像头采集链路上做人像分割，把人像之外的区域替换成虚化或指定图片。它是自研组件，装载不需要授权密钥。

<Note>
接口挂在全局单例 `MeetingKit` 上，不在 `MeetingKitRoom` 上——虚拟背景作用于进程内唯一的共享摄像头采集链路，**属设备级配置，设置会同时作用于全部房间**。同时加入多个房间时，不存在「只给某一个房间开虚拟背景」的用法。

会中切换摄像头（`switchCamera`）与断线重连都会重建采集链路，SDK 会自动把当前配置整体重放一遍，**业务层不需要在这些时机自己补**。
</Note>

<Warning>
`2.1.0` 起最低系统要求为 **iOS 16.0**。虚拟背景依赖 `onnxruntime`，使用 CocoaPods 集成时由 `RTCEngineKit` 的 podspec 传递引入，`Podfile` 中不需要显式声明，详见 [快速开始](/zh/meeting/ios/quickstart)。
</Warning>

### step 1：**装载虚拟背景组件**

建议在需要用到虚拟背景前装载，例如进入会议页面时。`modelPath` 传 `nil` 使用 SDK 内置的人像分割模型。

```objectivec
/// 装载虚拟背景组件
/// @param modelPath 人像分割模型文件路径，传 nil 使用内置模型
SEAError error = [[MeetingKit sharedInstance] installVirtualBackground:nil];
```

返回值说明：

| **返回值** | **说明** |
| --- | --- |
| SEAErrorOK | 装载成功 |
| SEAErrorConflict | 组件已装载，本次指令被丢弃 |
| SEAErrorNotFound | 模型文件不存在，检查 `modelPath` |
| SEAErrorSystemError | 推理会话创建失败，属于运行环境问题 |

### step 2：**设置背景效果**

背景虚化与背景替换**互斥，后调用的生效**。两个接口在装载前调用也会被记住，装载完成后自动生效，因此不必关心与 `installVirtualBackground:` 的先后顺序。

```objectivec
/// 设置背景虚化
/// @param level 虚化等级，取值范围 1-10，默认 5（超出范围会被收敛到边界值）
[[MeetingKit sharedInstance] setVirtualBackgroundBlur:5];

/// 设置背景替换
/// @param image 背景图片，按 cover 裁剪不拉伸；传 nil 表示取消替换回到虚化
[[MeetingKit sharedInstance] setVirtualBackgroundImage:[UIImage imageNamed:@"background"]];
```

### step 3：**开启或关闭虚拟背景**

装载后默认**不开启**，需要显式打开。关闭后是零开销直通，不再跑推理。

```objectivec
/// 虚拟背景功能开关
/// @param enabled YES-开启 NO-关闭
[[MeetingKit sharedInstance] enabledVirtualBackground:YES];

/// 获取虚拟背景开启状态
BOOL enabled = [[MeetingKit sharedInstance] isVirtualBackgroundEnabled];
```

组件未装载时调用开关会返回 `SEAErrorConflict`。关闭时会清掉帧间状态，下次开启从首帧重新收敛，不会闪出过期蒙版。

### step 4：**低端机保帧率（可选）**

默认每帧都跑一次人像分割。低端机上可以调大推理间隔，用蒙版复用换帧率；此时再按需打开蒙版对齐消除拖影。

```objectivec
/// 设置分割推理间隔
/// @param interval 分割每 N 帧跑一次（合成仍每帧跑），默认 1
[[MeetingKit sharedInstance] setVirtualBackgroundInferenceInterval:2];

/// 设置蒙版对齐
/// @param enabled YES-开启 NO-关闭，默认 NO
[[MeetingKit sharedInstance] setVirtualBackgroundMaskSync:YES];
```

| **参数** | **默认值** | **说明** |
| --- | :---: | --- |
| inferenceInterval | `1` | 每 N 帧跑一次分割，小于 1 按 1 处理。调大可降低推理开销，代价是快速运动时蒙版跟随变慢 |
| maskSync | `NO` | 开启后非推理帧不重新合成，画面与蒙版永远同一时刻，消除挥手时的错位拖影，代价是画面更新率降到蒙版率 |

<Note>
`inferenceInterval` 为 `1` 时，`setVirtualBackgroundMaskSync:` 开与不开没有任何区别——它只在调大推理间隔后才起作用。
</Note>

### step 5：**卸载虚拟背景组件**

不再使用时卸载，释放推理会话与相关缓冲。

```objectivec
/// 卸载虚拟背景组件
[[MeetingKit sharedInstance] uninstallVirtualBackground];
```

### 本地预览与推流的一致性

虚拟背景开启时，本地预览显示的就是处理后的画面，与对端看到的是同一份数据；关闭后本地预览回到摄像头原始画面。完整签名与参数见 [MeetingKit](/zh/meeting/ios/api-reference/MeetingKit#虚拟背景接口)。
