---
title: "快速开始"
description: "SMeeting Swift SDK 最小可运行接入流程：登录、创建会议、进入会议、开关音视频、渲染画面"
---

### 前提条件

+ 已完成 [SDK 集成](/zh/meeting/swift/integration)
+ 业务后端可以签发登录 SDK 用的 meeting token
+ 应用已经申请摄像头和麦克风权限

> meeting token 由你们的业务后端签发后下发给客户端，SDK 只负责使用它，不要在客户端自行拼装凭据。

---

### 最小可运行示例

下面的示例覆盖最核心链路：登录 SDK、创建即时会议、进入会议、开关本地音视频、渲染本端与远端画面、退出会议。

```swift
import SMeeting
import SRTC
import SwiftUI

@MainActor
final class MeetingViewModel: ObservableObject {
    /// SDK 主入口，整个 App 生命周期内只创建一个实例
    let meeting = SMeetingEngine(logLevel: .info)

    @Published var users: [MeetingUserInfo] = []
    @Published var isInMeeting = false
    @Published var isCameraOn = false

    /// 1. 登录：token 来自业务后端
    func login(token: String) async throws {
        try await meeting.login(token: token)
        meeting.delegates.add(delegate: self)
    }

    /// 2. 创建一场即时会议并进入
    func createAndEnter(nickname: String) async throws {
        var createReq = MeetingCreateReq(title: "\(nickname) 的会议", meetingMode: .normal)
        createReq.meetingType = .instant
        let (_, meetingId) = try await meeting.createRoom(createReq)

        try await meeting.enterRoom(MeetingEnterReq(nickname: nickname, meetingId: meetingId))
        isInMeeting = true
        users = meeting.getUsersInfoList()
    }

    /// 3. 用房间号进入已有会议
    func enter(roomNo: String, nickname: String, password: String? = nil) async throws {
        var enterReq = MeetingEnterReq(nickname: nickname, roomNo: roomNo)
        enterReq.password = password
        try await meeting.enterRoom(enterReq)
        isInMeeting = true
        users = meeting.getUsersInfoList()
    }

    /// 4. 打开本地麦克风与摄像头（SwiftUI 场景不需要传预览 view）
    func openLocalMedia() async throws {
        try await meeting.requestOpenMic()
        try await meeting.requestOpenCamera()
        isCameraOn = true      // 触发界面刷新，让本端画面显示出来
    }

    /// 5. 退出会议
    func exit() async {
        await meeting.closeCamera()
        await meeting.closeMic()
        await meeting.exitRoom()
        isCameraOn = false
        isInMeeting = false
        users = []
    }
}

// 事件回调在主线程派发；@MainActor 类型需要把协议方法声明为 nonisolated
extension MeetingViewModel: SMeetingDelegate {
    nonisolated func meeting(_ meeting: SMeetingEngine, userDidEnter user: MeetingUserInfo) {
        DispatchQueue.main.async { self.users = meeting.getUsersInfoList() }
    }

    nonisolated func meeting(_ meeting: SMeetingEngine, userDidExit data: UserExitEventData) {
        DispatchQueue.main.async { self.users = meeting.getUsersInfoList() }
    }
}

struct MeetingView: View {
    @StateObject private var vm = MeetingViewModel()

    var body: some View {
        VStack(spacing: 8) {
            // 本端画面：把本地摄像头轨道交给 SRTCVideoView
            if vm.isCameraOn, let cameraTrack = vm.meeting.cameraTrack {
                SRTCVideoView(track: cameraTrack).frame(height: 180)
            }

            // 远端画面：组件内部负责订阅与退订
            ForEach(vm.users.filter { $0.uid != vm.meeting.currentUserId }, id: \.uid) { user in
                SMeetingRemoteVideoView(meeting: vm.meeting, uid: user.uid, trackDesc: .cameraBig)
                    .frame(height: 180)
            }
        }
    }
}
```

---

### 接入流程说明

#### 1. 创建 `SMeetingEngine`

```swift
let meeting = SMeetingEngine(logLevel: .info)
```

`SMeetingEngine` 是整个 SDK 的唯一入口，负责登录、会议管理、进出会议、媒体控制、主持人操作和事件分发。**同一个 App 内只应创建一个实例**并全局持有，多实例会造成会议状态与媒体设备互相抢占。

#### 2. 登录并注册事件

```swift
try await meeting.login(token: token)
meeting.delegates.add(delegate: self)
```

`delegates` 是弱引用多播，支持多个观察者同时监听。`SMeetingDelegate` 的所有方法都有默认空实现，你只实现关心的事件即可。对象释放或登出前记得调用 `meeting.delegates.remove(delegate:)`。

#### 3. 创建会议还是直接进入会议

会前与会中是两个阶段：

+ `createRoom(_:)` 创建会议，返回 `(roomNo, meetingId)`
+ `enterRoom(_:)` 进入会议，`MeetingEnterReq` 里 `meetingId` 与 `roomNo` 二选一

如果会议已经由其他人（或你们的后台）创建好，跳过 `createRoom`，直接用房间号进入即可。

#### 4. 打开本地音视频

```swift
try await meeting.requestOpenMic()
try await meeting.requestOpenCamera()
```

方法名带 `request` 是因为它同时包含「向会议申请开启」和「本地起流并发布」两步 —— 当房间被主持人设为全体静音 / 全体禁画且禁止自我解除时，非主持人调用会抛出 `SMeetingError.unauthorized`。

SwiftUI 场景 `requestOpenCamera` 不需要传 `view`，把 `meeting.cameraTrack` 交给 `SRTCVideoView(track:)` 渲染即可。

#### 5. 渲染远端画面

远端画面用 `SMeetingRemoteVideoView`，它会在视图出现时按 `uid + TrackDesc` 订阅、视图消失时退订，你不需要手动管理订阅生命周期。

需要在 UIKit / AppKit 中渲染，或需要自己控制订阅时机，见 [视频渲染](/zh/meeting/swift/advanced/video-rendering)。

#### 6. 退出

+ `exitRoom()` 退出当前会议，不会退出登录
+ `logout()` 退出登录，如果仍在会议中会先自动退会

---

### 下一步

+ [核心概念](/zh/meeting/swift/key-concepts)
+ [媒体控制](/zh/meeting/swift/advanced/media-control)
+ [视频渲染](/zh/meeting/swift/advanced/video-rendering)
+ [主持人管控](/zh/meeting/swift/advanced/host-controls)
+ [接口文档 - SMeetingEngine](/zh/meeting/swift/api-reference/SMeetingEngine)
+ [事件参考](/zh/meeting/swift/events)
