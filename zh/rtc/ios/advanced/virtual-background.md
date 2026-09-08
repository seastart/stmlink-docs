---
title: "虚拟背景"
description: "iOS SRTC 音视频 SDK 的虚拟背景：人像分割后做背景虚化或背景替换，不需要授权密钥；本页交代与美颜的先后顺序、低端机保帧率的两个参数，以及必须补上的 onnxruntime 依赖"
---

虚拟背景在摄像头采集链路上做人像分割，把人像之外的区域替换成虚化或指定图片。它是自研组件，**与美颜不同，装载不需要授权密钥**。

<Note>
虚拟背景与美颜作用于同一条共享摄像头采集链路，设置对全部频道实例同时生效。

两者同时开启时顺序固定为**美颜在前、虚拟背景在后**：人像分割的输入是美颜后的图，边缘才与最终画面一致。
</Note>

<Warning>
虚拟背景依赖 `onnxruntime`，SDK 内部只保留其未定义符号，由接入 App 在链接期解决。使用 CocoaPods 集成时依赖会自动带入，最低系统要求为 iOS 16.0，详见 [集成方式](/zh/rtc/ios/integration)。
</Warning>

### step 1：**装载虚拟背景组件**

建议在需要用到虚拟背景前装载，例如进入会议页面时。`modelPath` 传 `nil` 使用 SDK 内置的人像分割模型。

```objectivec
/// 装载虚拟背景组件
/// @param modelPath 人像分割模型文件路径，传 nil 使用内置模型
RTCEngineError error = [[RTCEngineKit sharedEngine] installVirtualBackground:nil];
```

返回值说明：

| **返回值** | **说明** |
| --- | --- |
| RTCEngineErrorOK | 装载成功 |
| RTCEngineErrorConflict | 组件已装载，本次指令被丢弃 |
| RTCEngineErrorNotFound | 模型文件不存在，检查 `modelPath` |
| RTCEngineErrorSystemError | 推理会话创建失败，属于运行环境问题 |

### step 2：**设置背景效果**

背景虚化与背景替换**互斥，后调用的生效**。两个接口在装载前调用也会被记住，装载完成后自动生效，因此不必关心与 `installVirtualBackground:` 的先后顺序。

```objectivec
/// 设置背景虚化
/// @param level 虚化等级，取值范围 1-10，默认 5（超出范围会被收敛到边界值）
[[RTCEngineKit sharedEngine] setVirtualBackgroundBlur:5];

/// 设置背景替换
/// @param image 背景图片，按 cover 裁剪不拉伸；传 nil 表示取消替换回到虚化
[[RTCEngineKit sharedEngine] setVirtualBackgroundImage:[UIImage imageNamed:@"background"]];
```

### step 3：**开启或关闭虚拟背景**

装载后默认**不开启**，需要显式打开。关闭后是零开销直通，不再跑推理。

```objectivec
/// 虚拟背景功能开关
/// @param enabled YES-开启 NO-关闭
[[RTCEngineKit sharedEngine] enabledVirtualBackground:YES];

/// 获取虚拟背景开启状态
BOOL enabled = [[RTCEngineKit sharedEngine] isVirtualBackgroundEnabled];
```

组件未装载时调用开关会返回 `RTCEngineErrorConflict`。关闭时会清掉帧间状态，下次开启从首帧重新收敛，不会闪出过期蒙版。

### step 4：**低端机保帧率（可选）**

默认每帧都跑一次人像分割。低端机上可以调大推理间隔，用蒙版复用换帧率；此时再按需打开蒙版对齐消除拖影。

```objectivec
/// 设置分割推理间隔
/// @param interval 分割每 N 帧跑一次（合成仍每帧跑），默认 1
[[RTCEngineKit sharedEngine] setVirtualBackgroundInferenceInterval:2];

/// 设置蒙版对齐
/// @param enabled YES-开启 NO-关闭，默认 NO
[[RTCEngineKit sharedEngine] setVirtualBackgroundMaskSync:YES];
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
[[RTCEngineKit sharedEngine] uninstallVirtualBackground];
```

引擎销毁时会自动卸载，无需重复调用。

### 与美颜同时使用

两者相互独立装载、独立开关，可以只开其中一个。同时开启时处理顺序固定为美颜在前、虚拟背景在后。

```objectivec
/// 美颜：需要授权密钥
[[RTCEngineKit sharedEngine] installRenderModule:g_auth_package authDataSize:sizeof(g_auth_package) logLevel:RTCEngineLogLevelError];
/// 虚拟背景：不需要授权密钥
[[RTCEngineKit sharedEngine] installVirtualBackground:nil];
[[RTCEngineKit sharedEngine] enabledVirtualBackground:YES];
```

美颜或虚拟背景任一开启时，本地预览显示的是处理后的画面；两者都关闭时本地预览回到摄像头原始画面。美颜相关接口见 [视频美颜](/zh/rtc/ios/advanced/beauty)。
