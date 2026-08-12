---
title: "RTCEngineDelegate"
description: "进程级引擎事件回调协议：音频路由变更、网络测速结果与应用性能，与具体频道无关"
---

本协议只承载 [RTCEngineKit](/zh/rtc/ios/api-reference/RTCEngineKit) 单例范围内的共享能力事件，与具体频道无关。

频道内的连接、成员、消息、码流、音频与屏幕共享事件请实现 [RTCEngineChannelDelegate](/zh/rtc/ios/api-reference/RTCEngineChannelDelegate)。

<Warning>
自 `3.0.0` 起，本协议中的频道内回调已全部迁移到 `RTCEngineChannelDelegate`，且方法签名统一新增了事件来源频道实例首参。仅继续实现 `RTCEngineDelegate` 的业务层将收不到任何频道内事件，请参考 [RTCEngineChannelDelegate](/zh/rtc/ios/api-reference/RTCEngineChannelDelegate) 同步改造。
</Warning>

## 音频相关回调
### onAudioRouteChange:previousRoute:()
`- (void)onAudioRouteChange:(RTCAudioRoute)route previousRoute:(RTCAudioRoute)previousRoute`

音频路由变更回调

音频路由为进程级共享设备状态，变更对全部频道同时生效。

自`2.5.8`起，未显式选择扬声器或听筒且存在可用外设时，SDK 会先恢复外设；恢复成功后，不会上报音频会话重配期间短暂出现的扬声器或听筒路由，业务层收到的是最终实际路由。

**参数**

| route | 音频路由，详情请参照 [RTCAudioRoute](/zh/rtc/ios/types#rtcaudioroute) |
| --- | --- |
| previousRoute | 变更前的音频路由 |


## 网络测速相关回调
### onSpeedTestBegined()
`- (void)onSpeedTestBegined`

网络测速开始回调

调用`RTCEngineKit`中的`startSpeedTest:()`接口执行开始网络测速操作后，会收到该回调。

### onSpeedTestUploadResult:downResult:connectResult:()
`- (void)onSpeedTestUploadResult:(nullable RTCSpeedTestResult *)uploadResult downResult:(nullable RTCSpeedTestResult *)downResult connectResult:(nullable RTCSpeedTestConnectResult *)connectResult`

网络测速的结果回调

调用`RTCEngineKit`中的`startSpeedTest:()`接口执行开始网络测速操作后，底层监测完成之后会收到该回调。

**参数**

| uploadResult | 上行网速测试结果，详情请参考 [RTCSpeedTestResult](/zh/rtc/ios/types#rtcspeedtestresult) |
| --- | --- |
| downResult | 下行网速测试结果，详情请参考 [RTCSpeedTestResult](/zh/rtc/ios/types#rtcspeedtestresult) |
| connectResult | 连接情况测试结果，详情请参考 [RTCSpeedTestConnectResult](/zh/rtc/ios/types#rtcspeedtestconnectresult) |


## 其它相关回调
### onApplicationPerformance:cpuUsage:()
`- (void)onApplicationPerformance:(CGFloat)memory cpuUsage:(CGFloat)cpuUsage`

应用性能使用情况回调

统计维度为当前应用进程，不区分频道。

**参数**

| memory | 内存使用情况 |
| --- | --- |
| cpuUsage | CUP使用率 |
