---
title: "MeetingKitDelegate"
description: "会议组件全局事件回调协议：音频路由变更与应用性能，与加入了几个房间无关"
---

本协议只承载账号级与设备级的全局事件，通过 `-[MeetingKit addDelegate:]` 设置。

房间内的一切事件请实现 [MeetingKitRoomDelegate](/zh/meeting/ios/api-reference/MeetingKitRoomDelegate)，并在 `createRoomWithDelegate:` 创建房间时传入。

<Warning>
自 `2.0.0` 起，本协议中的房间内回调已全部迁移到 `MeetingKitRoomDelegate`，且方法签名统一新增了事件来源房间实例首参。仅继续实现 `MeetingKitDelegate` 的业务层将收不到任何房间内事件，请参考 [MeetingKitRoomDelegate](/zh/meeting/ios/api-reference/MeetingKitRoomDelegate) 同步改造。
</Warning>

## 音频事件回调
### onAudioRouteChange:previousRoute:()
`- (void)onAudioRouteChange:(SEAAudioRoute)route previousRoute:(SEAAudioRoute)previousRoute`

音频路由变更回调

音频路由对应进程内唯一的 `AVAudioSession`，属设备级事件，与加入了几个房间无关。音频路由发生改变时，SDK 会抛出该回调。

参考文档：[SEAAudioRoute](/zh/meeting/ios/types#seaaudioroute)

| 参数 | 描述 |
| --- | --- |
| route | 音频路由 |
| previousRoute | 变更前的音频路由 |


## 其它事件回调
### onApplicationPerformance:cpuUsage:()
`- (void)onApplicationPerformance:(CGFloat)memory cpuUsage:(CGFloat)cpuUsage`

应用性能使用情况回调

统计的是宿主进程整体占用，属进程级事件。

| 参数 | 描述 |
| --- | --- |
| memory | 内存使用情况 |
| cpuUsage | CUP使用率 |
