---
title: "快速开始"
description: "基于 rtc-swift Demo 整理的 SRTC Swift SDK 最小可运行接入流程"
---

### 前提条件

+ 已完成 [SDK 集成](/zh/rtc/swift/integration)
+ 服务端可以签发加入频道的 Token
+ 应用已经申请摄像头和麦克风权限

如果你使用 `rtc-swift` 仓库自带 Demo，Token 获取逻辑可参考 `Example/SRTCDemo/Sources/DemoApi.swift`，默认会调用 `/demo/token` 等演示接口。

---

### 最小可运行示例

下面的示例覆盖最核心链路：初始化 SDK、加入频道、打开麦克风和摄像头、订阅远端视频、离开频道。

```swift
import SRTC
import SwiftUI

@MainActor
final class RoomViewModel: ObservableObject, ChannelDelegate {
    @Published var localTrack: LocalCameraTrack?
    @Published var remoteTrack: Track?

    private let srtc = SRTC()
    private var channel: Channel?
    private var micTrack: LocalMicTrack?

    func join(with token: String) async throws {
        srtc.logLevel = .debug

        let channel = try await srtc.joinChannel(
            token: token,
            options: JoinOptions(autoSubscribeAudio: true)
        )
        channel.delegates.add(delegate: self)
        self.channel = channel

        let micTrack = srtc.createLocalMicTrack(preset: .music)
        try await micTrack.startCapture()
        try await channel.publishLocalTrack(micTrack)
        self.micTrack = micTrack

        let cameraTrack = srtc.createLocalCameraTrack(preset: .h720p)
        try await cameraTrack.startCapture()
        try await channel.publishLocalTrack(cameraTrack)
        self.localTrack = cameraTrack
    }

    func leave() async {
        // SDK 内部自动停止采集、取消发布，业务层只需清除引用
        await srtc.leaveChannel()
        channel = nil
        micTrack = nil
        localTrack = nil
        remoteTrack = nil
    }

    func channel(_ channel: Channel, user: UserInfo, didAddTrack track: TrackInfo) {
        guard track.kind == .video else { return }

        Task {
            try? await channel.subscribeRemoteVideoTrack(uid: user.uid, trackId: track.id)
            let subscribedTrack = channel.getRemoteTrack(uid: user.uid, trackId: track.id)
            await MainActor.run {
                self.remoteTrack = subscribedTrack
            }
        }
    }
}

struct RoomView: View {
    @StateObject private var vm = RoomViewModel()
    let token: String

    var body: some View {
        VStack(spacing: 12) {
            if let localTrack = vm.localTrack {
                SRTCVideoView(track: localTrack)
                    .frame(height: 220)
            }

            if let remoteTrack = vm.remoteTrack {
                SRTCVideoView(track: remoteTrack)
                    .frame(height: 220)
            }

            HStack {
                Button("加入频道") {
                    Task { try? await vm.join(with: token) }
                }

                Button("离开频道") {
                    Task { await vm.leave() }
                }
            }
        }
        .padding()
    }
}
```

---

### 接入流程说明

#### 1. 初始化 `SRTC`

`SRTC` 是整个 SDK 的主入口，负责：

+ 创建本地轨道
+ 解析 Token 并加入频道
+ 管理当前 `Channel` 生命周期
+ 配置日志级别和音频处理器

#### 2. 调用 `joinChannel`

```swift
let channel = try await srtc.joinChannel(
    token: token,
    options: JoinOptions(autoSubscribeAudio: true)
)
```

这里的第一性原理很简单：实时音视频的核心对象不是“房间页面”，而是“连接后的频道状态”。因此 `joinChannel(...)` 返回的不是布尔值，而是一个 `Channel` 对象，后续发布、订阅、消息、用户列表都围绕它展开。

#### 3. 创建并发布本地轨道

音频与视频遵循同一条主线：

+ `create...Track(...)` 只负责创建轨道对象
+ `startCapture()` 才真正打开硬件采集
+ `publishLocalTrack(...)` 才会把数据发到频道

这三个步骤拆开以后，你可以更精确地控制“什么时候申请硬件资源”和“什么时候真正推流”。

#### 4. 在回调里订阅远端视频

远端用户发流后，会通过 `ChannelDelegate` 的 `didAddTrack` 回调通知你。拿到 `TrackInfo` 以后：

+ 用 `subscribeRemoteVideoTrack(uid:trackId:)` 发起订阅
+ 再通过 `getRemoteTrack(uid:trackId:)` 取得轨道对象
+ 将轨道传给 `SRTCVideoView`、`VideoView` 或 `SRTCVideoRenderer`

---

### 下一步

+ [核心概念](/zh/rtc/swift/key-concepts)
+ [静音与停止发布](/zh/rtc/swift/advanced/mute-vs-unpublish)
+ [设备管理](/zh/rtc/swift/advanced/device-management)
+ [屏幕共享](/zh/rtc/swift/advanced/screen-sharing)
+ [自定义推流](/zh/rtc/swift/advanced/custom-track)
+ [接口文档 - SRTC](/zh/rtc/swift/api-reference/SRTC)
+ [接口文档 - Channel 与 Track](/zh/rtc/swift/api-reference/media-tracks)
