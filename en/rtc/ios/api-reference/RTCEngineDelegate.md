---
title: "RTCEngineDelegate"
description: "API reference for RTCEngineDelegate, the process-level engine event protocol in the Objective-C SRTC SDK on iOS: audio route changes, network speed test results, and app performance, independent of any channel. Look here for events not tied to a channel."
---

This protocol carries only events for shared capabilities scoped to the [RTCEngineKit](/en/rtc/ios/api-reference/RTCEngineKit) singleton, independent of any specific channel.

For in-channel connection, user, message, stream, audio, and screen sharing events, implement [RTCEngineChannelDelegate](/en/rtc/ios/api-reference/RTCEngineChannelDelegate).

<Warning>
Starting with `3.0.0`, all in-channel callbacks in this protocol have moved to `RTCEngineChannelDelegate`, and their method signatures now all take the channel instance the event comes from as the first parameter. If you keep implementing only `RTCEngineDelegate`, you won't receive any in-channel events; update your code as described in [RTCEngineChannelDelegate](/en/rtc/ios/api-reference/RTCEngineChannelDelegate).
</Warning>

## Audio callbacks
### onAudioRouteChange:previousRoute:()
`- (void)onAudioRouteChange:(RTCAudioRoute)route previousRoute:(RTCAudioRoute)previousRoute`

Called when the audio route changes.

The audio route is process-level shared device state, and a change applies to all channels at once.

Starting with `2.5.8`, when neither the speaker nor the earpiece has been explicitly selected and an external device is available, the SDK restores the external device first; once it's restored, the speaker or earpiece routes that briefly appear while the audio session is being reconfigured aren't reported, so what you receive is the final actual route.

**Parameters**

| route | Audio route; see [RTCAudioRoute](/en/rtc/ios/types#rtcaudioroute) |
| --- | --- |
| previousRoute | Audio route before the change |


## Network speed test callbacks
### onSpeedTestBegined()
`- (void)onSpeedTestBegined`

Called when a network speed test starts.

You receive this callback after calling `startSpeedTest:()` in `RTCEngineKit` to start a network speed test.

### onSpeedTestUploadResult:downResult:connectResult:()
`- (void)onSpeedTestUploadResult:(nullable RTCSpeedTestResult *)uploadResult downResult:(nullable RTCSpeedTestResult *)downResult connectResult:(nullable RTCSpeedTestConnectResult *)connectResult`

Called with the network speed test results.

After you call `startSpeedTest:()` in `RTCEngineKit` to start a network speed test, you receive this callback once the underlying measurement completes.

**Parameters**

| uploadResult | Uplink speed test result; see [RTCSpeedTestResult](/en/rtc/ios/types#rtcspeedtestresult) |
| --- | --- |
| downResult | Downlink speed test result; see [RTCSpeedTestResult](/en/rtc/ios/types#rtcspeedtestresult) |
| connectResult | Connectivity test result; see [RTCSpeedTestConnectResult](/en/rtc/ios/types#rtcspeedtestconnectresult) |


## Other callbacks
### onApplicationPerformance:cpuUsage:()
`- (void)onApplicationPerformance:(CGFloat)memory cpuUsage:(CGFloat)cpuUsage`

Called with app performance data.

Statistics are for the current app process and aren't broken down by channel.

**Parameters**

| memory | Memory usage |
| --- | --- |
| cpuUsage | CPU usage |
