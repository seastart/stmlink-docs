---
title: "IRTCChannel"
description: "API reference for IRTCChannel, the Windows SRTC per-channel object: the create → configure → join() sequence, settings and event handler, user and channel info queries, local and remote track objects, publishing, and subscribing. Read when working with a channel after createChannel."
---



## IRTCChannel

`IRTCChannel` represents **one channel** and is created by [IRTCEngine::createChannel](/en/rtc/windows/api-reference/IRTCEngine#create-a-channel-object).

`createChannel` only parses the token and creates the object; it **doesn't join the channel**. This gives you a chance to set up the
configuration and event handler before `join()`—`onJoinChannel` is called back before `join()` returns, so if you set the handler too late, you miss it.

```cpp
SRTC::IRTCChannel* ch = nullptr;
if (engine->createChannel(token, &ch) != SRTC::StatusCode::OK) {
    return;   // On failure, ch is always nullptr
}

// 1) Configuration (for items that only matter before join, see IRTCChannelSetting)
SRTC::IRTCChannelSetting* set = nullptr;
ch->getSetting(&set);
set->set_stream_model(1);

// 2) Event handler; must be set before join()
ch->setEventHandler(this);

// 3) Join the channel
if (ch->join() != SRTC::StatusCode::OK) {
    engine->leaveChannel(ch->getChannelId());   // A failed channel object must also be reclaimed
    ch = nullptr;
    return;
}
```

Always leave through [IRTCEngine::leaveChannel](/en/rtc/windows/api-reference/IRTCEngine#leave-a-channel); `IRTCChannel` itself **has no** `leave()`.
After the call, the object has been destroyed, and you must set the pointer to null yourself.

## Basic functions
### Get the channel ID
```cpp
virtual const char* getChannelId() = 0;
```

Returns the value of the `channel` field in the token. The pointer is owned by the SDK and stays valid until you leave the channel; you don't need to free it.


### Get the settings object
```cpp
virtual StatusCode getSetting(IRTCChannelSetting** set) = 0;
```

**Parameters**

| set | The channel settings class; for details, see [IRTCChannelSetting](/en/rtc/windows/api-reference/IRTCChannelSetting) |
| --- | --- |


### Set the event handler
```cpp
virtual StatusCode setEventHandler(IRTCChannelEvent* e) = 0;
```

**Parameters**

| e | An implementation of the pure virtual channel event callback class; for the callbacks, see [IRTCChannelEvent](/en/rtc/windows/api-reference/IRTCChannelEvent) |
| --- | --- |


Note: you must set it before `join()`; otherwise you don't receive `onJoinChannel`.


### Join the channel
```cpp
virtual StatusCode join() = 0;
```

Note: this is synchronous; `onJoinChannel` has already been called back before it returns. Calling it again returns `Conflict`. On failure, the channel object still exists,
and you need to reclaim it with [IRTCEngine::leaveChannel](/en/rtc/windows/api-reference/IRTCEngine#leave-a-channel).


## User info functions
### Get your own user info
```cpp
virtual StatusCode getMe(char** s, int* c) = 0;
```

**Parameters**

| s | User info JSON |
| --- | --- |
| c | Length of the user info JSON |




### Get channel info
```cpp
virtual StatusCode getChannel(char** s, int* c) = 0;
```

**Parameters**

| s | Channel info JSON |
| --- | --- |
| c | Length of the channel info JSON |



### Get info for all users in the channel
```cpp
virtual StatusCode getMembers(char** s, int* c) = 0;
```

**Parameters**

| s | JSON array of all users' info |
| --- | --- |
| c | Length of the JSON array of all users' info |






### Get info for a specific user
```cpp
virtual StatusCode getMember(const char* uid, char** s, int* c) = 0;
virtual StatusCode getMemberByLinkId(const char* linkId, char** s, int* c) = 0;
virtual StatusCode getMemberByLinkId(int linkId, char** s, int* c) = 0;
		
```

**Parameters**

| uid/linkid | User ID, media streaming linkid |
| --- | --- |
| s | User info JSON |
| c | Length of the user info JSON |



### Error codes for channel-level methods

| Calling a media method before `join()` | `NotInitialized` |
| --- | --- |

## Media streaming functions
### Get a video track object
```cpp
virtual StatusCode getCameraTrack(const char* track_key,IRTCLocalCameraTrack ** track) = 0;
```

**Parameters**

| track_key | Key of the local video track object, maintained by you. Distinguishes different track objects; it's also the default publishing desc |
| --- | --- |
| track | [Video track object](/en/rtc/windows/api-reference/IRTCLocalCameraTrack) |




### Get a screen sharing track object
```cpp
virtual StatusCode getScreenTrack(const char* track_key,IRTCLocalScreenTrack ** track) = 0;
```

**Parameters**

| track_key | Key of the local video track object, maintained by you. Distinguishes different track objects; it's also the default publishing desc |
| --- | --- |
| track | [Screen track object](/en/rtc/windows/api-reference/IRTCLocalScreenTrack) |




### Get an audio track object
```cpp
virtual StatusCode getAudioTrack(const char* track_key,IRTCLocalMicTrack** track) = 0;
```

**Parameters**

| track_key | Key of the local audio track object, maintained by you. Distinguishes different track objects; it's also the default publishing desc |
| --- | --- |
| track | [Microphone track object](/en/rtc/windows/api-reference/IRTCLocalMicTrack) |




### Get a user's audio track object
```cpp
virtual StatusCode getRemoteAudioTrack(const char* uid, const char* trackid, IRTCRemoteAudioTrack** track) = 0;
```

**Parameters**

| uid | User ID (empty for all users) |
| --- | --- |
| trackid | ID of the user's audio track (empty for all tracks) |
| track | [Local audio mixing track object](/en/rtc/windows/api-reference/IRTCRemoteAudioTrack) |




### Get a user's video track object
```cpp
virtual StatusCode getRemoteVideoTrack(const char* uid, const char* trackid, IRTCRemoteVideoTrack** track) = 0;
```

**Parameters**

| uid | User ID |
| --- | --- |
| trackid | ID of the user's video track |
| track | [User video track object](/en/rtc/windows/api-reference/IRTCRemoteVideoTrack) |




### Get the composite stream video track object
```cpp
virtual StatusCode getMCUVideoTrack(IRTCRemoteVideoTrack** track) = 0;
```

**Parameters**

| track | [Composite stream video track object](/en/rtc/windows/api-reference/IRTCRemoteVideoTrack) |
| --- | --- |






### Subscribe to a track
```cpp
virtual StatusCode subscribe(IRTCTrack* tk ) = 0;
```

**Parameters**

| tk | The track, [IRTCRemoteVideoTrack](/en/rtc/windows/api-reference/IRTCRemoteVideoTrack), [IRTCRemoteAudioTrack](/en/rtc/windows/api-reference/IRTCRemoteAudioTrack) |
| --- | --- |


### Unsubscribe from a track
```cpp
virtual StatusCode unsubscribe(IRTCTrack* tk ) = 0;
```

**Parameters**

| tk | The track, [IRTCRemoteVideoTrack](/en/rtc/windows/api-reference/IRTCRemoteVideoTrack), [IRTCRemoteAudioTrack](/en/rtc/windows/api-reference/IRTCRemoteAudioTrack) |
| --- | --- |


### Publish a video track
```cpp
virtual StatusCode publish(IRTCTrack* tk, RTCVideoPublishOptions* opt) = 0;
```

**Parameters**

| tk | The track, [IRTCLocalCameraTrack](/en/rtc/windows/api-reference/IRTCLocalCameraTrack), [IRTCLocalScreenTrack](/en/rtc/windows/api-reference/IRTCLocalScreenTrack) |
| --- | --- |
| opt | Publishing parameters for the track; `nullptr` uses the default publishing parameters, [RTCVideoPublishOptions](/en/rtc/windows/types#video-track-publishing-options-rtcvideopublishoptions) |


### Publish an audio track
```cpp
virtual StatusCode publish(IRTCTrack* tk, RTCAudioPublishOptions* opt) = 0;
```

**Parameters**

| tk | The track, [IRTCLocalMicTrack](/en/rtc/windows/api-reference/IRTCLocalMicTrack) |
| --- | --- |
| opt | Publishing parameters for the track; `nullptr` uses the default publishing parameters, [RTCAudioPublishOptions](/en/rtc/windows/types#audio-track-publishing-options-rtcaudiopublishoptions) |


Note: the two `publish` overloads no longer have a default argument (the old `publish(tk)` was itself an ambiguous call and didn't compile), so you must pass `opt` explicitly.
