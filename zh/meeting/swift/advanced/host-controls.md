---
title: "主持人管控"
description: "SMeeting Swift SDK 中主持人与联席主持人的房间管控、成员管理、参会人员维护与设备邀请"
---

### 概述

带 `admin` 前缀的接口需要主持人（`.host`）或联席主持人（`.coHost`）身份，普通成员调用会收到服务端返回的权限错误。调用前先判断：

```swift
let me = try? meeting.getUserInfo(meeting.currentUserId ?? "")
let isAdmin = me?.role == .host || me?.role == .coHost
```

管控动作生效后，**所有成员**都会收到对应的房间 / 成员状态事件，你不需要在发起方本地手动改状态，统一在事件里刷新即可。

---

### 房间级管控

| 接口 | 作用 | 对应房间字段 | 变化事件 |
| --- | --- | --- | --- |
| `adminUpdateRoomMicState(selfUnmuteMicDisabled:micDisabled:)` | 全体静音 | `micDisabled` / `selfUnmuteMicDisabled` | `roomMicStateDidChange` |
| `adminUpdateRoomCameraState(selfUnmuteCameraDisabled:cameraDisabled:)` | 全体禁画 | `cameraDisabled` / `selfUnmuteCameraDisabled` | `roomCameraStateDidChange` |
| `adminUpdateRoomShareState(shareDisabled:)` | 禁止共享 | `shareDisabled` | `roomShareStateDidChange` |
| `adminUpdateRoomChatDisabled(_:)` | 全体禁言 | `chatDisabled` | `roomChatDisabledDidChange` |
| `adminUpdateRoomScreenshotDisabled(_:)` | 禁止截屏 | `screenshotDisabled` | `roomScreenshotDisabledDidChange` |
| `adminUpdateRoomWatermarkDisabled(_:)` | 关闭水印 | `watermarkDisabled` | `roomWatermarkDisabledDidChange` |
| `adminUpdateRoomLocked(_:)` | 锁定会议 | `locked` | `roomLockedDidChange` |
| `adminUpdateEnterBeforeHostDisabled(_:)` | 禁止主持人前入会 | `enterBeforeHostDisabled` | 无独立事件 |
| `adminStopRoomShare()` | 强制结束当前共享 | `shareState` | `roomShareDidStop` |
| `adminDestroyRoom()` | 结束整场会议 | — | 成员收到 `didDisconnect` |

#### 全体静音的两个开关

`micDisabled` 和 `selfUnmuteMicDisabled` 含义不同，一起决定成员的体验：

```swift
// 全体静音，且不允许成员自己解除
try await meeting.adminUpdateRoomMicState(selfUnmuteMicDisabled: true, micDisabled: true)

// 全体静音，但允许成员自己解除
try await meeting.adminUpdateRoomMicState(selfUnmuteMicDisabled: false, micDisabled: true)

// 解除全体静音
try await meeting.adminUpdateRoomMicState(selfUnmuteMicDisabled: false, micDisabled: false)
```

开启「全体静音」时，非主持人成员的麦克风会被自动关闭。之后成员能否自己重新开麦，取决于 `selfUnmuteMicDisabled`。摄像头是同一套规则。

#### 结束会议

```swift
try await meeting.adminDestroyRoom()
```

所有成员会被断开，成员端通过 `meeting(_:didDisconnect:)` 感知。发起方自己也需要把界面退回会议外。

---

### 成员管理

```swift
// 改成员会中昵称
try await meeting.adminUpdateUserName(targetId: uid, nickname: "张三")

// 设为联席主持人 / 取消
try await meeting.adminUpdateUserRole(targetId: uid, role: .coHost)
try await meeting.adminUpdateUserRole(targetId: uid, role: .member)

// 转移主持人（转让后自己变成普通成员）
try await meeting.adminMoveHost(targetId: uid)

// 单独禁言
try await meeting.adminUpdateUserChatDisabled(targetId: uid, chatDisabled: true)

// 移出会议；joinDisabled 为 true 表示同时禁止再次入会
try await meeting.adminKickUserOut(targetId: uid, joinDisabled: true)
```

对应的成员状态事件：`userNameDidChange`、`userRoleDidChange`、`userChatDisabledDidChange`。被移出的成员通过 `didDisconnect` 感知。

关闭成员麦克风 / 摄像头，以及邀请成员开启，见 [举手与开启请求](/zh/meeting/swift/advanced/handup)。

---

### 修改自己的会中昵称

这个动作不需要主持人身份：

```swift
try await meeting.updateName("新的昵称")
```

---

### 参会人员维护

#### 修改受邀人员名单

```swift
try await meeting.adminUpdateConferee(meetingId: meetingId, conferee: [uid1, uid2])
```

#### 查询谁还没进来

```swift
let notEntered = try await meeting.meetNotEnter()
```

返回 `[NoEnterUserInfo]`，含昵称、手机号、头像、角色等信息。

#### 提醒入会

```swift
try await meeting.adminMeetRemind(uids: [uid1, uid2], useSms: true)
```

`useSms` 为 `true` 时同时发短信提醒。

#### 会中呼叫

```swift
try await meeting.adminCallUsers(conferee: [uid1, uid2])
```

被呼叫方如果已经启用了会议外消息，会收到 `imCallCalling` 事件，见 [会议外消息](/zh/meeting/swift/advanced/im)。

#### 在线人员列表

```swift
let page = try await meeting.adminListOnlineMember(page: 1, perPage: 20)
```

---

### 邀请设备入会

会议支持把 SIP、H.323、GB28181、RTSP / RTMP 拉流、文件播放等外部设备拉进会议。

先查可用设备：

```swift
let devices = try await meeting.agentList(type: [.sip, .h323], name: "会议室")
```

再发起邀请：

```swift
try await meeting.adminInviteAgent(
    agents: [(type: .sip, contact: "sip:1001@example.com")],
    no: roomNo
)
```

`AgentType` 可选值见 [类型定义](/zh/meeting/swift/types#agenttype)。设备当前忙闲状态读 `AgentInfo.status`。

---

### 相关页面

+ [举手与开启请求](/zh/meeting/swift/advanced/handup)
+ [等候室](/zh/meeting/swift/advanced/waiting-room)
+ [分组讨论](/zh/meeting/swift/advanced/sub-meetings)
+ [接口文档 - 会议管理](/zh/meeting/swift/api-reference/admin-actions)
