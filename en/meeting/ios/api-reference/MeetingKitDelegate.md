---
title: "MeetingKitDelegate"
description: "Global event callback protocol of the iOS SMeeting SDK: audio route changes and app performance, independent of how many rooms you have entered. Read this to handle device-level events; in-room events are in MeetingKitRoomDelegate."
---

This protocol carries only account-level and device-level global events. Set it through `-[MeetingKit addDelegate:]`.

For all in-room events, implement [MeetingKitRoomDelegate](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) and pass it in when you create a room with `createRoomWithDelegate:`.

<Warning>
Since `2.0.0`, all in-room callbacks in this protocol have moved to `MeetingKitRoomDelegate`, and every method signature now takes the room instance that is the event source as its first parameter. If your app still implements only `MeetingKitDelegate`, it receives no in-room events at all. Update your code accordingly by referring to [MeetingKitRoomDelegate](/en/meeting/ios/api-reference/MeetingKitRoomDelegate).
</Warning>

## Audio callbacks
### onAudioRouteChange:previousRoute:()
`- (void)onAudioRouteChange:(SEAAudioRoute)route previousRoute:(SEAAudioRoute)previousRoute`

Called when the audio route changes.

The audio route maps to the single `AVAudioSession` in the process, so this is a device-level event, independent of how many rooms you have entered. The SDK fires this callback when the audio route changes.

See: [SEAAudioRoute](/en/meeting/ios/types#seaaudioroute)

| Parameter | Description |
| --- | --- |
| route | Audio route |
| previousRoute | Audio route before the change |


## Other callbacks
### onApplicationPerformance:cpuUsage:()
`- (void)onApplicationPerformance:(CGFloat)memory cpuUsage:(CGFloat)cpuUsage`

Called with the app's performance usage.

Reports the overall usage of the host process, so this is a process-level event.

| Parameter | Description |
| --- | --- |
| memory | Memory usage |
| cpuUsage | CPU usage |
