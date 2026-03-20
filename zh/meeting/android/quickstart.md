---
title: "快速开始"
description: "Android SMeeting 会议 SDK 快速集成，10 分钟跑通基础功能"
---

# 前置准备

开始前请先完成以下准备：

- 按照 [集成](./integration.md) 完成 Maven 仓库与 SDK 依赖接入。
- 准备好服务端签发的 `meetToken`，它是调用 `initSdk` 的必填参数。
- 如果你要在会中打开摄像头和麦克风，请先在业务侧处理 Android 运行时权限申请。
- 如果你要控制音频输出设备，可结合 [音频路由使用](./音频路由使用.md) 一起接入。

下文按“初始化 → 创建会议 → 入会 → 媒体控制 → 远端订阅”的顺序给出最小可用流程。

## Step 1：初始化 SDK 与释放资源

在调用任何会议相关接口前，必须先创建 `MeetingEngine` 并完成 `initSdk`。

- `meetToken`：通过你们自己的服务端授权接口获取。
- `options`：媒体配置，可传 `null` 使用 SDK 默认配置。
- `MeetingResultCallback`：用于接收初始化成功或失败结果。

```kotlin
private var engine: MeetingEngine? = null

fun initMeetingSdk(app: Application, meetToken: String) {
    engine = MeetingEngine.create(app)
    engine?.initSdk(meetToken, null, object : MeetingResultCallback {
        override fun onSuccess() {
            // SDK 初始化成功，可继续创建会议、查询会议、加入会议等操作
        }

        override fun onFail(code: Int, errorMsg: String?, showMsg: String?) {
            // SDK 初始化失败
        }
    })
}
```

页面退出或应用不再使用会议能力时，调用 `release()` 释放资源：

```kotlin
fun releaseMeetingSdk() {
    engine?.release()
    engine = null
}
```

## Step 2：创建会议

SDK 支持创建**即时会议**和**预约会议**。两种接口都需要标题，差别主要在于是否单独传入预约开始时间和会议时长。

### 2.1 创建参数怎么填

创建会议时，最常用的是 `CreateImmediateMeetingOption` / `CreateScheduleMeetingOption` 里的这些字段：

- `roomNo`：可选；如果你想自定义会议号就传，不传时通常由后台生成。
- `content`：会议说明，可选。
- `attendType`：入会方式。
  - `AttendType.ATTEND_NOT_LIMIT`：任何拿到会议号的人都可以进。
  - `AttendType.ATTEND_BY_PWD`：需要密码，记得同时填写 `password`。
  - `AttendType.ATTEND_ONLY_INVITE`：仅受邀成员可进，记得同时填写 `conferees`。
- `conferees`：受邀成员 UID 列表，仅“仅邀请人员参会”场景建议填写。
- `password`：会议密码，仅密码入会场景需要填写。
- `mode`：会议模式。常规场景建议使用 `MeetingMode.Normal`。
- `entryMutePolicy`：入会静音策略。
  - `MuteState.MuteState1`：所有人入会默认静音。
  - `MuteState.MuteState2`：不强制静音，跟随客户端初始音频状态。
  - `MuteState.MuteState3`：超过 6 人后，新加入成员默认静音。
- `autoRecord`：是否自动录制。
- `waitingRoomDisabled`：`true` 表示关闭等候室，`false` 表示启用等候室。
- `enterBeforeHostDisabled`：`true` 表示不允许主持人前入会。
- `extendInfo`：业务自定义扩展字段，建议传 JSON 字符串；无扩展需求可传 `null`。

更完整的数据结构可继续参考 [模型类型](./data-reference/models.md) 和 [枚举类型](./data-reference/enums.md)。

### 2.2 创建即时会议

即时会议通常只需要设置标题和一组基础选项。下面这个示例与 Demo 的用法一致，适合作为最小起步模板：

```kotlin
val option = CreateImmediateMeetingOption(
    content = "产品评审",
    attendType = AttendType.ATTEND_NOT_LIMIT,
    mode = MeetingMode.Normal,
    entryMutePolicy = MuteState.MuteState3
)

engine?.createImmediateMeeting(
    "项目周会",
    option,
    object : Callback<Data<MeetingCreatedBean>>() {
        override fun onSuccess(data: Data<MeetingCreatedBean>) {
            val meetingId = data.data.meetingId
            val roomNo = data.data.roomNo
            // 建议保存 roomNo，后续可直接用它入会
        }

        override fun onFailed(code: Int, errorMsg: String?, showMsg: String?) {
            // 会议创建失败
        }
    }
)
```

### 2.3 创建预约会议

预约会议比即时会议多两个核心参数：

- `planTime`：预约开始时间，**秒级时间戳**。
- `planDur`：会议时长，单位**分钟**。

```kotlin
val planTime = System.currentTimeMillis() / 1000 + 30 * 60 // 30 分钟后开始
val planDur = 60 // 持续 60 分钟

val option = CreateScheduleMeetingOption(
    content = "季度复盘",
    attendType = AttendType.ATTEND_BY_PWD,
    password = "123456",
    mode = MeetingMode.Normal,
    entryMutePolicy = MuteState.MuteState1,
    waitingRoomDisabled = false
)

engine?.createScheduleMeeting(
    "季度经营分析会",
    planTime,
    planDur,
    option,
    object : Callback<Data<MeetingCreatedBean>>() {
        override fun onSuccess(data: Data<MeetingCreatedBean>) {
            val meetingId = data.data.meetingId
            val roomNo = data.data.roomNo
            // 预约会议创建成功
        }

        override fun onFailed(code: Int, errorMsg: String?, showMsg: String?) {
            // 预约会议创建失败
        }
    }
)
```

## Step 3：加入会议、离开会议与结束会议

### 3.1 入会参数怎么填

`enterMeeting(...)` 的核心参数建议这样理解：

- `activity`：当前用于展示会议页面的 `Activity`。
- `roomNo`：要加入的会议号，通常来自创建会议后的返回值，或通过会前会议列表/详情查询得到。
- `password`：如果会议设置了 `ATTEND_BY_PWD`，这里传对应密码；否则传 `null`。
- `nick`：入会昵称，建议传业务用户名或展示名。
- `avatar`：头像地址或头像标识，没有可传空字符串。
- `streamVendor`：流媒体厂商标识。当前 Android Demo 使用 `"wangsucdn"`；如果你们的部署环境由后端指定其他值，请以后端配置为准。
- `extendInfo`：业务扩展字段，可传 JSON 字符串；没有扩展数据时传 `null`。

### 3.2 加入会议

```kotlin
val roomNo = "10000001"
val nick = "张三"
val avatar = "https://example.com/avatar.png"
val streamVendor = "wangsucdn"

engine?.enterMeeting(
    this,
    roomNo,
    null,
    nick,
    avatar,
    streamVendor,
    null,
    object : EnterMeetingCallback {
        override fun onSucceed(meetingId: String, uid: String) {
            // 入会成功
            // meetingId: 当前会议 ID
            // uid: 当前用户在本次会议中的 UID
        }

        override fun onFail(code: Int, errorMsg: String?, showMsg: String?) {
            // 入会失败
        }
    }
)
```

如果你手上拿到的是 `meetingId` 而不是 `roomNo`，可改用 `enterMeetingByMeetingId(...)`，其余参数填法一致。

### 3.3 离开会议

普通成员离会直接调用：

```kotlin
engine?.exitMeeting()
```

### 3.4 结束会议

只有主持人场景才需要调用 `adminDestroyMeeting(...)` 结束整个会议：

```kotlin
engine?.adminDestroyMeeting(
    object : Callback<Data<String?>>() {
        override fun onSuccess(data: Data<String?>) {
            // 结束会议成功
        }

        override fun onFailed(code: Int, errorMsg: String?, showMsg: String?) {
            // 结束会议失败
        }
    }
)
```

## Step 4：开启、关闭与切换摄像头

### 4.1 开启摄像头前要做什么

调用 `requestOpenCamera(...)` 前，建议先完成这些准备：

- 已成功入会。
- 已获取相机运行时权限。
- 如果暂时不需要本地预览，可把 `view` 传 `null`；后续也可以通过 `addPreview(view)` 补加预览控件。

`preOpt` 推荐直接使用 SDK 内置预设：

- `PreOptionCamera._480P`：640 × 480，主流最大码率约 512 kbps，适合大多数会议场景。
- `PreOptionCamera._720P`：1280 × 720，清晰度更高，带宽占用也更高。
- `PreOptionCamera._1080P`：1920 × 1080，适合对清晰度要求更高的场景。

如果你没有特殊要求，优先从 `PreOptionCamera._480P` 开始。

### 4.2 开启摄像头

```kotlin
engine?.requestOpenCamera(
    null,
    PreOptionCamera._480P,
    object : Callback<Data<String?>>() {
        override fun onSuccess(data: Data<String?>) {
            // 开启摄像头成功
        }

        override fun onFailed(code: Int, errorMsg: String?, showMsg: String?) {
            // 开启摄像头失败
        }
    }
)
```

### 4.3 关闭摄像头

```kotlin
engine?.closeCamera()
```

### 4.4 切换前后摄像头

- `true`：切到前置摄像头。
- `false`：切到后置摄像头。

```kotlin
engine?.switchCamera(isFrontCamera = false)
```

## Step 5：开启和关闭麦克风

### 5.1 麦克风参数怎么选

调用 `requestOpenMic(...)` 前，请先确保已经获取录音权限。

推荐直接使用 `PreOptionMic.def`，它已经包含常规会议所需的默认音频配置：

- 开启回声消除（AEC）
- 开启降噪（ANS）
- 开启自动增益（AGC）
- 单声道
- 48 kHz 采样率
- OPUS 编码，最大码率约 32 kbps

这套配置适合绝大多数语音会议和视频会议场景。

### 5.2 开启麦克风

```kotlin
engine?.requestOpenMic(
    PreOptionMic.def,
    object : Callback<Data<String?>>() {
        override fun onSuccess(data: Data<String?>) {
            // 开启麦克风成功
        }

        override fun onFailed(code: Int, errorMsg: String?, showMsg: String?) {
            // 开启麦克风失败
        }
    }
)
```

### 5.3 关闭麦克风

```kotlin
engine?.closeMic()
```

如果你还需要切换扬声器、听筒、蓝牙耳机或有线耳机，可继续参考 [音频路由使用](./音频路由使用.md)。

## Step 6：订阅与取消订阅远端视频

### 6.1 `uid` 和 `trackDesc` 从哪里来

订阅远端视频前，需要两个关键参数：

- `uid`：目标成员 UID。通常来自成员列表、用户事件回调，或者 `engine?.infosManager?.getMembersInfo()`。
- `trackDesc`：目标轨道描述。可通过 `engine?.infosManager?.getTrackInfos(uid)` 获取。

常见的 `trackDesc` 包括：

- `camera_big`：远端摄像头主流
- `camera_small`：远端摄像头辅流
- `screen`：远端共享画面

### 6.2 订阅远端视频

`startPlayRemoteVideo(...)` 会返回一个 `RemoteVideoTrack`，你可以直接传入渲染视图，也可以先订阅再调用 `addPlayView(view)` 绑定渲染控件。

```kotlin
val infosManager = engine?.infosManager ?: return
val targetUid = "remote-user-001"
val trackInfo = infosManager
    .getTrackInfos(targetUid)
    .firstOrNull { it.desc == "camera_big" }
    ?: return

val remoteVideoTrack = engine?.startPlayRemoteVideo(
    targetUid,
    trackInfo.desc,
    remoteView,
    null
)

remoteVideoTrack?.addPlayView(remoteView)
```

如果你想先查某一条固定轨道，也可以使用：

```kotlin
val trackInfo = engine?.infosManager?.getTrackInfoByTrackDesc(targetUid, "screen")
```

### 6.3 取消订阅远端视频

```kotlin
engine?.stopPlayRemoteVideo(targetUid, trackInfo.desc)
```

如果你还持有 `RemoteVideoTrack`，在界面销毁前也建议把渲染控件移除，例如调用 `removeAllPlayView()`，避免重复绑定。

## 相关文档

- [集成](./integration.md)
- [MeetingEngine API](./api-reference/MeetingEngine.md)
- [InfosManager](./api-reference/InfosManager.md)
- [RemoteVideoTrack](./api-reference/RemoteVideoTrack.md)
- [模型类型](./data-reference/models.md)
- [枚举类型](./data-reference/enums.md)
- [轨道预设配置总览](./data-reference/track-options.md)
- [音频路由使用](./音频路由使用.md)

