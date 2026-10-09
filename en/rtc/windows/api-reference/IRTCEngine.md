---
title: "IRTCEngine"
description: "API reference for IRTCEngine, the process-level object of the Windows SRTC C++ SDK: RTCEngine_Init / RTCEngine_Free, version and error messages, creating and leaving channels, network speed tests, device enumeration, and log upload. Read when setting up the engine or managing channels."
---



## IRTCEngine
### Create IRTCEngine
```cpp
RTCENGINE_API StatusCode RTCENGINE_CALL RTCEngine_Init(IRTCEngine** rtc, RTCEngineOptions* opt);
```

**Parameters**

| rtc | The IRTCEngine object; nullptr on failure |
| --- | --- |
| opt | Engine initialization options, [RTCEngineOptions](/en/rtc/windows/types#engine-initialization-options-rtcengineoptions). **Passing nullptr writes no SDK log at all** |


Note: the log switch and log path used to be on `IRTCSetting` (`enable_stream_log` / `sdk_log_path`) and have moved here—
they're consumed while the engine itself initializes, before any channel object exists.


### Release IRTCEngine
```cpp
RTCENGINE_API void RTCENGINE_CALL RTCEngine_Free(IRTCEngine** rtc);
```

**Parameters**

| rtc | The IRTCEngine object |
| --- | --- |




### Get the version number
```cpp
RTCENGINE_API StatusCode RTCENGINE_CALL RTCEngine_Version(const char*v1);
```

**Parameters**

| v1 | SDK version number |
| --- | --- |


Note: the caller must allocate the memory before passing it in, at least 100 bytes.

### Get the error code description
```cpp
RTCENGINE_API void RTCENGINE_CALL RTCEngine_GetStatusMsg(StatusCode code, char* msg);
```

**Parameters**

| code | Error code |
| --- | --- |
| msg | Error code description |


Note: the caller must allocate the memory for msg before passing it in, at least 100 bytes. The text is **UTF-8**, and the language is determined by [`RTCEngine_SetLanguage()`](#set-the-language); **English by default** (don't branch on the text—use the error code).

### Set the language
```cpp
RTCENGINE_API void RTCENGINE_CALL RTCEngine_SetLanguage(const char* lang);
```

**Parameters**

| lang | Language tag (BCP 47), e.g. `zh-CN`, `en`. Passing `nullptr` or any non-`zh*` value means English |
| --- | --- |


Note: process-wide and can be called at any time. It affects srtc's own error texts and is forwarded to the underlying `RTC_SetLanguage` (subsequent backend requests then carry `Accept-Language`). **English when never called**; older versions always returned Chinese, so callers that display Chinese must set it explicitly after upgrading.

### Get the last error message
```cpp
RTCENGINE_API void RTCENGINE_CALL RTCEngine_GetLastErrorMessage(char* msg);
```

**Parameters**

| msg | Output, the error message. The caller must allocate at least 100 bytes before passing it in |
| --- | --- |


Note: writes the text of the error code returned by the **last srtc API call** into the buffer (UTF-8, same language as [`RTCEngine_SetLanguage()`](#set-the-language), English by default). That error code is maintained by srtc itself, not taken from the underlying library, and is updated whenever an API returns non-`OK`; call it right after a failing synchronous call. Empty when there is no error. With multiple threads, it reads the last error code within the process, which may be overwritten by another thread.



## Basic functions
### Set the event handler
```cpp
virtual StatusCode setEventHandler(IRTCEngineEvent* e) = 0;
```

**Parameters**

| e | An implementation of the pure virtual event callback class; for the callbacks, see [IRTCEngineEvent](/en/rtc/windows/api-reference/IRTCEngineEvent) |
| --- | --- |



## Channel functions

You can join multiple channels at the same time. Each channel corresponds to an [IRTCChannel](/en/rtc/windows/api-reference/IRTCChannel) object, and channel-level methods and callbacks are all on that object,
instead of being distinguished by a leading `channelId` parameter on `IRTCEngine` as in older versions.

**About channelId**

+ `channelId` is the value of the `channel` field in the token. The SDK parses it internally, and you get it through `IRTCChannel::getChannelId()`
+ `channelId` is used only by `leaveChannel` and `getChannelIds`; all other methods are called directly on the channel object

### Create a channel object
```cpp
virtual StatusCode createChannel(const char* token, IRTCChannel** ch) = 0;
```

**Parameters**

| token | The token required to join the channel |
| --- | --- |
| ch | Output parameter, the channel object. nullptr on failure |


Note: this **only creates the object and doesn't join the channel**. After you get the object, set up its configuration and event handler, then call [IRTCChannel::join()](/en/rtc/windows/api-reference/IRTCChannel#join-the-channel).
Creating the same channel again returns `Conflict`; if no channel can be parsed from the token, it returns `SdkTokenInvalid`.


### Leave a channel
```cpp
virtual void leaveChannel(const char* channelId) = 0;
```

**Parameters**

| channelId | ID of the channel to leave |
| --- | --- |


### Leave all channels
```cpp
virtual void leaveAllChannel() = 0;
```


### Get the list of joined channels
```cpp
virtual StatusCode getChannelIds(char** s, int* c) = 0;
```

**Parameters**

| s | JSON array of joined channelIds, for example ["ch_a","ch_b"] |
| --- | --- |
| c | Length of the JSON array |



## Media streaming functions
### Network speed test
```cpp
	virtual StatusCode probeNetwork(int time, int upindex, int downindex) = 0;
```

**Parameters**

| time | Duration of the speed test; a multiple of 10 is recommended |
| --- | --- |
| upindex | Uplink test amount (in KB); 0 skips the uplink test |
| downindex | Downlink test amount (in KB); 0 skips the downlink test |


Note: the test results are returned in the [callback](/en/rtc/windows/api-reference/IRTCEngineEvent#network-probe-result-callback).





### Get camera info
```cpp
virtual StatusCode getEnumVideo(char** devices, int* iSize) = 0;
```

**Parameters**

| Devices | Camera info JSON, see [Camera enumeration info](/en/rtc/windows/types#camera-enumeration-info) |
| --- | --- |
| iSize | Length of the camera info JSON |




### Get screen info
```cpp
virtual StatusCode getEnumScreen(char** devices, int* iSize) = 0;
```

**Parameters**

| Devices | Screen info JSON, see [Shared screen enumeration info](/en/rtc/windows/types#shared-screen-enumeration-info) |
| --- | --- |
| iSize | Length of the screen info JSON |




### Get microphone info
```cpp
virtual StatusCode getEnumAudio(char** devices, int* iSize) = 0;
```

**Parameters**

| Devices | Microphone info JSON, see [Microphone info](/en/rtc/windows/types#microphone/speaker-enumeration-info) |
| --- | --- |
| iSize | Length of the microphone info JSON |




### Get speaker info
```cpp
virtual StatusCode getEnumSpeaker(char** devices, int* iSize) = 0;
```

**Parameters**

| Devices | Speaker info JSON, see [Speaker info](/en/rtc/windows/types#microphone/speaker-enumeration-info) |
| --- | --- |
| iSize | Length of the speaker info JSON |






## Other
### Add a log to upload
```cpp
virtual StatusCode addUploadLog(const char* type ,const char* msg) = 0;
```

**Parameters**

| type | Log type identifier |
| --- | --- |
| msg | Log content |


Logs you add are uploaded to the log server.
