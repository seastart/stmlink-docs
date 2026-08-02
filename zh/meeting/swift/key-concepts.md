---
title: "核心概念"
description: "理解 SMeeting Swift SDK 中的会议生命周期、房间状态模型、角色、轨道描述与事件体系"
---

### 整体模型

SMeeting Swift SDK 的对象模型很集中：

+ `SMeeting`：唯一对外类，登录、会议管理、进出会议、媒体控制、主持人操作都在它上面
+ `RoomInfo`：当前会议的房间级状态（标题、全体禁音禁画、锁定、共享状态等）
+ `MeetingUserInfo`：会中某个成员的状态（昵称、角色、麦克风、摄像头、共享）
+ `SMeetingDelegate`：所有会议事件的回调入口
+ `SMeetingRemoteVideoView` / `SRTCVideoView`：画面渲染入口

会议 SDK 本质上是在同步三类状态：**会议状态**、**成员状态**、**媒体状态**。SDK 的接口与事件都是围绕这三类状态组织的，理解这一点之后大部分 API 都会变得自然。

---

### 会议层与 RTC 层的术语差异

SMeeting 建立在 SRTC 之上，两层的名词不通用，混用会让你在读接口时反复卡壳：

| 概念 | 会议层（SMeeting） | RTC 层（SRTC） |
| --- | --- | --- |
| 空间 | 房间 room / 会议 meeting | 频道 channel |
| 出入 | 进入 enter / 退出 exit | 加入 join / 离开 leave |
| 成员 | 参会成员 | 频道用户 |

在 SMeeting 的接口里你只会看到 `enterRoom` / `exitRoom` / `createRoom` 这类会议语义的命名。

---

### 会议生命周期

一次完整的接入按下面的顺序展开：

```text
login  →  会前（创建 / 查询 / 修改会议）  →  enterRoom  →  会中  →  exitRoom  →  logout
```

| 阶段 | 典型接口 | 说明 |
| --- | --- | --- |
| 登录 | `login(token:)` | token 由业务后端签发，登录后才能调用其余接口 |
| 会前 | `createRoom(_:)`、`updateRoom(meetingId:req:)`、`cancelRoom(meetingId:)`、`detailRoom(meetingId:roomNo:)`、`attendeeRoom(page:)`、`attendedRoom(page:)` | 只需要登录，不需要在会议中 |
| 进入 | `enterRoom(_:)` | 成功后 SDK 内部建立会议状态，事件开始上报 |
| 会中 | 媒体控制、消息、主持人管控…… | 未在会议中调用会抛 `SMeetingError.notInMeeting` |
| 退出 | `exitRoom()` | 只退出当前会议，登录状态保留 |
| 登出 | `logout()` | 若仍在会议中会先自动退会 |

判断当前是否在会议中，用 `meeting.isInRoom`。

---

### 会议 ID 与房间号

两个标识经常同时出现，含义不同：

| 标识 | 来源 | 用途 |
| --- | --- | --- |
| `meetingId` | `createRoom` 返回值、会议列表 / 详情 | 会议的唯一 ID，绝大多数会议管理接口用它 |
| `roomNo` | `createRoom` 返回值、会议详情 | 面向用户的会议号，用来分享和邀请他人入会 |

`MeetingEnterReq` 里 `meetingId` 与 `roomNo` 二选一填写即可。

---

### 会议类型与会议模式

创建会议时有两个正交的维度：

+ `MeetingType`：`.instant` 即时会议 / `.appointment` 预约会议。预约会议需要额外填 `planTime`（秒级时间戳）和 `planDur`（分钟）
+ `MeetingMode`：`.normal` 普通、`.mix` 合成、`.voice` 语音会议、`.training` 培训、`.subMeeting` 分会场

入会限制由 `AttendType` 控制，密码入会要同时填 `password`，仅邀请入会要同时填 `conferee`。

---

### 会中状态：RoomInfo 与 MeetingUserInfo

进入会议后，SDK 会持续维护一份会中状态快照，随时可读：

```swift
let roomInfo = meeting.getRoomInfo()          // 当前房间信息，未入会时为 nil
let users = meeting.getUsersInfoList()        // 所有成员（数组）
let usersMap = meeting.getUsersInfo()         // 所有成员（uid → 成员）
let me = try meeting.getUserInfo(meeting.currentUserId ?? "")
```

这份快照是**读快照**：状态变化通过 `SMeetingDelegate` 事件通知你，你在事件回调里重新读一次即可，不要缓存过期的成员对象。

`MeetingUserInfo` 里几个高频字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `micState` | `MicState` | `.on` / `.off` |
| `cameraState` | `CameraState` | `.on` / `.off` |
| `shareState` | `Int` | `0` 无共享、`1` 屏幕共享、`2` 白板，可与 `ShareType` 的 `rawValue` 比较 |
| `role` | `Role` | `.member` / `.host` / `.coHost` |
| `chatDisabled` | `Bool` | 是否被单独禁言 |

---

### 角色与权限

| 角色 | 说明 |
| --- | --- |
| `.host` | 主持人，拥有全部管控权限 |
| `.coHost` | 联席主持人，与主持人共享大部分管控权限 |
| `.member` | 普通成员 |

判断自己是否有管控权限，读自己的 `MeetingUserInfo.role`：

```swift
let me = try? meeting.getUserInfo(meeting.currentUserId ?? "")
let isAdmin = me?.role == .host || me?.role == .coHost
```

`admin` 前缀的接口只有主持人 / 联席主持人调用才会成功，普通成员调用会收到服务端返回的权限错误。

---

### 轨道描述 TrackDesc

会议里的每一路媒体流都有一个固定的描述，用来在订阅远端画面时定位目标：

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `.mic` | `mic` | 麦克风音频 |
| `.cameraBig` | `camera_big` | 摄像头大流 |
| `.cameraSmall` | `camera_small` | 摄像头小流 |
| `.screen` | `screen` | 屏幕共享 |

成员当前发布了哪些轨道，可以读 `MeetingUserInfo.trackDescs`。

---

### 媒体控制的命名规则

+ **开启侧**叫 `requestOpenMic` / `requestOpenCamera` / `requestShare` —— 带 `request` 是因为这些动作要先向会议申请（受全体静音、全体禁画、禁共享等房间策略约束），再在本地起流
+ **关闭侧**叫 `closeMic` / `closeCamera` / `stopShare` —— 直接停止本地流，没有申请环节，不会抛错

当你是在响应主持人的开麦 / 开摄像头邀请时，给开启侧接口传 `byAdmin: true` 和 `adminUid`，SDK 会走「确认主持人请求」的分支而不是「主动申请」。

---

### 视频渲染入口

| 场景 | 推荐入口 |
| --- | --- |
| SwiftUI 本端画面 | `SRTCVideoView(track: meeting.cameraTrack)` |
| SwiftUI 远端画面 | `SMeetingRemoteVideoView(meeting:uid:trackDesc:)` |
| UIKit / AppKit 远端画面 | `startPlayRemoteVideo(view:uid:trackDesc:)` / `stopPlayRemoteVideo(view:uid:trackDesc:)` |
| 自行控制订阅 | `subscribeRemoteVideoTrack(uid:trackDesc:)` / `unsubscribeRemoteVideoTrack(uid:trackDesc:)` |

细节见 [视频渲染](/zh/meeting/swift/advanced/video-rendering)。

---

### 音频的订阅语义

远端音频与远端视频的处理方式不同：

+ **音频**：进入会议后自动订阅，不需要你逐个成员去订阅。听筒 / 外放开关走 `toggleRemoteAudioMute(_:)`，它只切播放，不动订阅关系
+ **视频**：按需订阅。大会场里如果把所有人的视频都订阅了，带宽和解码开销都不可控，所以要由你决定当前布局里哪几路需要拉流

---

### 事件体系

所有会议事件都通过 `SMeetingDelegate` 上报，注册方式：

```swift
meeting.delegates.add(delegate: self)
// 不再需要时
meeting.delegates.remove(delegate: self)
```

要点：

+ `delegates` 是**弱引用多播**，可以注册多个观察者；SDK 不会因为注册而延长你的对象生命周期
+ 协议里所有方法都提供了默认空实现，只实现关心的事件即可
+ 事件回调统一在**主线程**派发，可以直接更新 UI

如果你的观察者是 `@MainActor` 类型（例如 SwiftUI 的 `ObservableObject`），协议方法需要声明为 `nonisolated`，再在里面回到主 actor 上下文：

```swift
@MainActor
final class MeetingController: ObservableObject {
    @Published var users: [MeetingUserInfo] = []
}

extension MeetingController: SMeetingDelegate {
    nonisolated func meeting(_ meeting: SMeeting, userDidEnter user: MeetingUserInfo) {
        DispatchQueue.main.async { self.users = meeting.getUsersInfoList() }
    }
}
```

事件大致分为这几组：连接事件、成员事件、房间状态事件、消息事件、举手与主持人指令、等候室、分组讨论、签到与点名、外设事件、会议外消息（IM）。完整清单见 [事件参考](/zh/meeting/swift/events)。

---

### 会议外消息（IM）

`enableIm()` 会建立一条独立于会议的消息通道，用于在**没有进入会议时**接收呼叫、会议提醒等通知。它与会中的聊天消息是两套东西：会中聊天走 `sendRoomChatMessage`，只在会议内有效。

见 [会议外消息](/zh/meeting/swift/advanced/im)。

---

### 底层 RTC 能力

当会议层的高层接口不足以满足需求时（例如需要 SRTC 才有的原始帧处理、自定义编码参数），可以通过 `meeting.srtc` 访问底层实例。

```swift
meeting.srtc.logLevel = .debug
```

> 请始终使用 `meeting.srtc`，不要自行另建一个 SRTC 实例：会议与底层共享同一个实例，另起一个会导致状态分裂、消息通道重复、设备被抢占。

---

### 建议继续阅读

+ [媒体控制](/zh/meeting/swift/advanced/media-control)
+ [视频渲染](/zh/meeting/swift/advanced/video-rendering)
+ [屏幕共享](/zh/meeting/swift/advanced/screen-sharing)
+ [主持人管控](/zh/meeting/swift/advanced/host-controls)
+ [类型定义](/zh/meeting/swift/types)
