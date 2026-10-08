---
title: "错误码"
description: "iOS SRTC 音视频 SDK 错误码枚举与处理说明"
---

<Note>
自 **3.2.0** 起错误码按[跨端统一码表](/zh/rtc/error-codes)重排为「iOS 前缀 `103` + 低 3 位」，枚举名保留、取值改变，需用新版头文件重新编译。下表「3.1.2 及以前」列为旧取值，完整说明见[更新日志](/zh/rtc/ios/changelog)。
</Note>

### 错误码规则

+ `0`：成功
+ `103000`–`103999`：SDK 本地错误，完整码 = `103` + 统一码表低 3 位，如 `103006` = `103` + `006`（连接失败）。低 3 位与其它端同义
+ `1000`–`99999`：后端业务码，SDK 原样透传，不加前缀，含义见[服务端 API 错误码](/zh/rtc/server-api/error-codes)

`engineChannel:onDisconnected:errCode:errMsg:` 与 `onImDisconnected:errCode:errMsg:` 的 `errCode` 同样遵循以上规则。只返回错误码的接口遇到后端业务码时，可立即读取 [RTCEngineKit.lastServerErrorMessage](/zh/rtc/ios/api-reference/RTCEngineKit#lastservererrormessage) 拿到服务端文案（`3.2.1` 起，语言随 [RTCEngineKit.language](/zh/rtc/ios/api-reference/RTCEngineKit#language)）。**请按错误码判断，不要依赖错误文案**：`errMsg` 来自后端，仅供日志。

### RTCEngineError
错误码

| **枚举名** | **枚举值** | **3.1.2 及以前** | **说明** |
| --- | :---: | :---: | --- |
| RTCEngineErrorOK | `0` | `0` | 无错误 |
| **连接与信令** | | | |
| RTCEngineErrorNotJoinedChannel | `103001` | `103002` | 未加入频道 |
| RTCEngineErrorStreamNotFound | `103003` | `103004` | 码流不存在 |
| RTCEngineErrorSdkTokenInvalid | `103004` | `100008` | 令牌不合法 |
| RTCEngineErrorConflict | `103005` | `100007` | 重复操作冲突，如重复加入频道 |
| RTCEngineErrorNetError | `103006` | `100009` | 网络错误（含 HTTP 非 200） |
| RTCEngineErrorTimeout | `103007` | `100005` | 连接或请求超时 |
| RTCEngineErrorProtocolParsingError | `103011` | `100004` | 协议解析错误 |
| RTCEngineErrorMediaNetError | `103012` | `100010` | 媒体网络错误 |
| **状态与通用** | | | |
| RTCEngineErrorNotInitialized | `103024` | `100002` | 未初始化，或当前状态不允许该操作（如未开启采集时调用 `switchCamera`） |
| RTCEngineErrorMediaNotInitialized | `103024` | `100003` | 已废弃（deprecated），与 `RTCEngineErrorNotInitialized` 同值，`switch` 中不要同时写两者 |
| RTCEngineErrorSystemError | `103025` | `100001` | 系统内部错误 |
| RTCEngineErrorUserCancelled | `103026` | `100012` | 用户取消了 |
| RTCEngineErrorInvalidArgs | `103031` | `100006` | 参数错误，如自定义流传入 `0`~`2` 号轨道 |
| **虚拟背景** | | | |
| RTCEngineErrorVirtualBackgroundAlreadyInstalled | `103027` | 新增 | 虚拟背景组件已装载 |
| RTCEngineErrorVirtualBackgroundNotInstalled | `103028` | 新增 | 虚拟背景组件未装载 |
| RTCEngineErrorVirtualBackgroundModelNotFound | `103029` | 新增 | 人像分割模型文件不存在或无效 |
| RTCEngineErrorVirtualBackgroundSessionFailed | `103030` | 新增 | 推理会话创建失败 |
| **权限与设备** | | | |
| RTCEngineErrorDeviceNoAuthorized | `103042` | `103001` | 设备访问无权限。保留定义，**SDK 不再返回**，请改用下方摄像头 / 麦克风两个码 |
| RTCEngineErrorForbidden | `103043` | `103003` | 当前身份或角色不允许该操作 |
| RTCEngineErrorSwitchAudioRouteFail | `103044` | `103005` | 音频路由切换失败 |
| RTCEngineErrorCameraNoAuthorized | `103231` | 新增 | 无摄像头权限 |
| RTCEngineErrorMicNoAuthorized | `103251` | 新增 | 无麦克风权限 |
| **成员** | | | |
| RTCEngineErrorNotFound | `103204` | `100011` | 频道内没有该用户 |

<Warning>
3.1.2 及以前，无摄像头 / 麦克风权限统一返回 `RTCEngineErrorDeviceNoAuthorized`；虚拟背景的四种失败分别返回 `RTCEngineErrorConflict` / `RTCEngineErrorNotFound` / `RTCEngineErrorSystemError`。从这些版本升级时，除重新编译外，还需按上表把对应分支改为新枚举。
</Warning>
