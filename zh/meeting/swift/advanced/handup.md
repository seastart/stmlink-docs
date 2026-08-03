---
title: "举手与开启请求"
description: "SMeeting Swift SDK 中成员举手申请、主持人审批，以及主持人邀请成员开麦开摄像头的完整流程"
---

### 概述

会议里有两条方向相反的「请求」链路，容易混淆，先分清：

| 链路 | 发起方 | 成员端接口 | 主持人端接口 |
| --- | --- | --- | --- |
| 举手申请 | 成员 → 主持人 | `requestHandup(_:)` / `cancelHandup(_:)` | `adminConfirmHandup(targetId:approve:code:)` |
| 开启邀请 | 主持人 → 成员 | `requestOpenMic(byAdmin:adminUid:)` / `rejectOpenMic(adminUid:)` | `adminRequestUserOpenMic(targetId:)` |

举手类型 `HandupType` 有四种：`.mic` 申请开麦、`.camera` 申请开摄像头、`.chat` 申请发言权、`.share` 申请共享。

---

### 成员举手

```swift
// 申请开麦
try await meeting.requestHandup(.mic)

// 取消申请
try await meeting.cancelHandup(.mic)
```

---

### 主持人收到举手

```swift
func meeting(_ meeting: SMeetingEngine, userDidHandup data: UserHandupEventData) {
    // data.uid  举手的成员
    // data.type 举手类型
    // data.step 动作步骤
}
```

`UserHandupStep` 表示这条事件处在流程的哪一步：

| 步骤 | 说明 |
| --- | --- |
| `.request` | 成员发起举手 |
| `.cancel` | 成员取消举手 |
| `.confirmOpen` | 成员同意了主持人的开启邀请 |
| `.rejectOpen` | 成员拒绝了主持人的开启邀请 |

也就是说，这一个事件同时承载了「举手申请」和「邀请被响应」两类通知，用 `step` 区分处理。

---

### 主持人审批举手

```swift
try await meeting.adminConfirmHandup(targetId: data.uid, approve: true, code: .mic)
```

审批结果会通过事件下发给相关成员：

```swift
func meeting(_ meeting: SMeetingEngine, adminDidConfirmHandup data: AdminConfirmHandupEventData) {
    // data.targetId 被审批的成员
    // data.approve  是否同意
    // data.type     举手类型
    // data.opUid    审批的主持人
}
```

审批通过**不会**自动打开成员的麦克风或摄像头 —— 成员端需要在收到这个事件后自行调用 `requestOpenMic()` / `requestOpenCamera()`。

---

### 主持人邀请成员开启

```swift
try await meeting.adminRequestUserOpenMic(targetId: user.uid)
try await meeting.adminRequestUserOpenCamera(targetId: user.uid)
```

成员端收到：

```swift
func meeting(_ meeting: SMeetingEngine, adminDidRequestOpenMic data: AdminRequestOpenMicEventData) {
    // data.opUid 发起邀请的主持人
}

func meeting(_ meeting: SMeetingEngine, adminDidRequestOpenCamera data: AdminRequestOpenCameraEventData) {
    // data.opUid
}
```

同意时，把 `byAdmin: true` 和 `adminUid` 一起传给开启接口，让 SDK 走「响应邀请」而不是「主动申请」：

```swift
try await meeting.requestOpenMic(byAdmin: true, adminUid: data.opUid)
try await meeting.requestOpenCamera(byAdmin: true, adminUid: data.opUid)
```

拒绝时：

```swift
try await meeting.rejectOpenMic(adminUid: data.opUid)
try await meeting.rejectOpenCamera(adminUid: data.opUid)
```

不论同意还是拒绝，主持人端都会收到一条 `userDidHandup`，`step` 为 `.confirmOpen` 或 `.rejectOpen`。

---

### 主持人直接关闭成员设备

关闭方向不需要征求同意：

```swift
try await meeting.adminCloseUserMic(targetId: user.uid)
try await meeting.adminCloseUserCamera(targetId: user.uid)
```

被关闭方的 SDK 会自动停流，并上报一次 `userMicStateDidChange` / `userCameraStateDidChange`，其中 `byAdmin` 为 `true`、`opUid` 为操作者，你可以据此给用户一个「已被主持人关闭麦克风」的提示。

---

### 一个完整的交互建议

```swift
// 成员端
func meeting(_ meeting: SMeetingEngine, adminDidRequestOpenMic data: AdminRequestOpenMicEventData) {
    Task { @MainActor in
        showConfirmDialog(
            title: "主持人邀请你开麦",
            onAccept: { Task { try? await meeting.requestOpenMic(byAdmin: true, adminUid: data.opUid) } },
            onReject: { Task { try? await meeting.rejectOpenMic(adminUid: data.opUid) } }
        )
    }
}
```

---

### 相关页面

+ [媒体控制](/zh/meeting/swift/advanced/media-control)
+ [主持人管控](/zh/meeting/swift/advanced/host-controls)
+ [事件参考](/zh/meeting/swift/events)
