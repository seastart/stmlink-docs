---
title: "Media track APIs"
description: "C++ media object APIs of the SMeeting Windows SDK: local microphone, camera, and screen objects, remote audio and video, MCU video, custom tracks, and local recording, plus the IMEETLocalMic, IMEETLocalCamera, IMEETLocalScreen, IMEETRemoteVideo, IMEETRemoteAudio, IMEETRecord, and IMEETVideo methods."
---

All of the following media objects are obtained through [ISMeetingChannel](/en/meeting/windows/api-reference/smeeting-channel).

---

## Local media stream APIs

### Get the local microphone object
```cpp
virtual StatusCode getLocalMic(IMEETLocalMic**) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| (output) | IMEETLocalMic** | Output pointer to the local microphone object |

**Returns**

`StatusCode` - Error code

### Get the local camera object
```cpp
virtual StatusCode getLocalCamera(IMEETLocalCamera**) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| (output) | IMEETLocalCamera** | Output pointer to the local camera object |

**Returns**

`StatusCode` - Error code

### Get the local screen sharing object
```cpp
virtual StatusCode getLocalScreen(IMEETLocalScreen**) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| (output) | IMEETLocalScreen** | Output pointer to the local screen sharing object |

**Returns**

`StatusCode` - Error code

---

## Remote media stream APIs

### Get a remote video object
```cpp
virtual StatusCode getRemoteVideo(std::string uid, std::string track_desc, IMEETRemoteVideo**) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| track_desc | std::string | Track description |
| (output) | IMEETRemoteVideo** | Output pointer to the remote video object |

**Returns**

`StatusCode` - Error code

### Get a remote audio object
```cpp
virtual StatusCode getRemoteAudio(std::string uid, IMEETRemoteAudio**) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| (output) | IMEETRemoteAudio** | Output pointer to the remote audio object |

**Returns**

`StatusCode` - Error code

### Get the MCU video object
```cpp
virtual StatusCode getMcuVideo(IMEETRemoteVideo**) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| (output) | IMEETRemoteVideo** | Output pointer to the MCU video object |

**Returns**

`StatusCode` - Error code

---

## Custom track APIs

### Get a custom video track
```cpp
virtual StatusCode getCustomVideo(CustomPublishTrack* push, IMeetCustomVideoTrack**) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| push | CustomPublishTrack* | Custom track configuration |
| (output) | IMeetCustomVideoTrack** | Output pointer to the custom video track object |

**Returns**

`StatusCode` - Error code

### Get a custom audio track
```cpp
virtual StatusCode getCustomAudio(CustomPublishTrack* push, IMeetCustomAudioTrack**) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| push | CustomPublishTrack* | Custom track configuration |
| (output) | IMeetCustomAudioTrack** | Output pointer to the custom audio track object |

**Returns**

`StatusCode` - Error code

### Set the custom receive callback
```cpp
virtual StatusCode setCustomRecvBack(RTC_Custom_FrameEvent e, void* ext) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| e | RTC_Custom_FrameEvent | Frame event callback function |
| ext | void* | Extension data |

**Returns**

`StatusCode` - Error code

---

## IMeetCustomVideoTrack methods

Returned by `getCustomVideo`.

### Get the custom track info
```cpp
virtual StatusCode getTrackInfo(CustomPublishTrack**) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| (output) | CustomPublishTrack** | Output custom track configuration |

**Returns**

`StatusCode` - Error code

### Push a video frame
```cpp
virtual StatusCode pushVideoFrame(int stmtype, unsigned char* buf, int buf_len, int frmtype, long ts) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| stmtype | int | Stream type |
| buf | unsigned char* | Video frame data |
| buf_len | int | Data length |
| frmtype | int | Frame type |
| ts | long | Timestamp |

**Returns**

`StatusCode` - Error code

### Unpublish
```cpp
virtual StatusCode unpublish() = 0;
```

**Returns**

`StatusCode` - Error code

---

## IMeetCustomAudioTrack methods

Returned by `getCustomAudio`.

### Get the custom track info
```cpp
virtual StatusCode getTrackInfo(CustomPublishTrack**) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| (output) | CustomPublishTrack** | Output custom track configuration |

**Returns**

`StatusCode` - Error code

### Push an audio frame
```cpp
virtual StatusCode pushAudioFrame(int stmtype, unsigned char* buf, int buf_len, long ts) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| stmtype | int | Stream type |
| buf | unsigned char* | Audio frame data |
| buf_len | int | Data length |
| ts | long | Timestamp |

**Returns**

`StatusCode` - Error code

### Unpublish
```cpp
virtual StatusCode unpublish() = 0;
```

**Returns**

`StatusCode` - Error code

---

## Local recording APIs

### Get the local recording object
```cpp
virtual StatusCode getLocalRecord(IMEETRecord** e) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| e | IMEETRecord** | Pointer to the recording object |

**Returns**

`StatusCode` - Error code

> Starting with `1.0.0-alpha.5`, you no longer pass in a meeting ID; the current channel object's own meeting ID is used.

---

## IMEETLocalMic methods

### Request to turn on the microphone
```cpp
virtual StatusCode requestOpenMic(Callback back = NULL) = 0;
```

### Turn off the microphone
```cpp
virtual StatusCode closeMic(Callback back = NULL) = 0;
```

### Switch microphones
```cpp
virtual StatusCode switchMic(std::string name) = 0;
```

### Confirm turning on the microphone
```cpp
virtual StatusCode confirmOpenMic(bool approve, std::string uid, Callback function = NULL) = 0;
```

---

## IMEETLocalCamera methods

Inherits from `IMEETVideo`.

### Switch cameras
```cpp
virtual StatusCode switchCamera(std::string name, int w = 0, int h = 0) = 0;
```

### Request to turn on the camera
```cpp
virtual StatusCode requestOpenCamera(Callback back = NULL) = 0;
```

### Turn off the camera
```cpp
virtual StatusCode closeCamera(Callback back = NULL) = 0;
```

### Confirm turning on the camera
```cpp
virtual StatusCode confirmOpenCamera(bool approve, std::string uid, Callback function = nullptr) = 0;
```

---

## IMEETLocalScreen methods

Inherits from `IMEETVideo`.

### Request to share
```cpp
virtual StatusCode requestShare(int tp, std::string data, Callback back = NULL) = 0;
```

### Stop sharing
```cpp
virtual StatusCode stopShare(Callback back = NULL) = 0;
```

### Add screen audio
```cpp
virtual StatusCode addScreenAudio(bool) = 0;
```

### Update the stream output
```cpp
virtual StatusCode updateStreamOutput(int w, int h) = 0;
```

### Confirm starting to share
```cpp
virtual StatusCode confirmOpenShare(int tp, std::string data, Callback back = NULL) = 0;
```

---

## IMEETRemoteVideo methods

Inherits from `IMEETVideo`.

### Load the remote video
```cpp
virtual StatusCode loadRemoteVideo() = 0;
```

### Unload the remote video
```cpp
virtual StatusCode unLoadRemoteVideo() = 0;
```

---

## IMEETRemoteAudio methods

### Turn on the speaker
```cpp
virtual StatusCode openSpeaker() = 0;
```

### Turn off the speaker
```cpp
virtual StatusCode closeSpeaker() = 0;
```

### Switch speakers
```cpp
virtual StatusCode switchSpeaker(std::string name) = 0;
```

---

## IMEETRecord methods

### Set the recording file name
```cpp
virtual StatusCode setRecordFileName(std::string filepath) = 0;
```

### Set the watermark
```cpp
virtual StatusCode setWaterMask(std::string mask) = 0;
```

### Start recording
```cpp
virtual StatusCode startRecord() = 0;
```

### Set the recording window
```cpp
virtual StatusCode setRecordHwnd(void*, int, int, int, int) = 0;
```

### Set the recording layout member views
```cpp
virtual StatusCode setRecordLayoutMemberView(std::string json) = 0;
```

### Pause recording
```cpp
virtual StatusCode pauseRecord() = 0;
```

### Stop recording
```cpp
virtual StatusCode stopRecord() = 0;
```

---

## IMEETVideo methods

### Add a playback view
```cpp
virtual StatusCode addPlayView(IRTCView* v) = 0;
```

### Remove a playback view
```cpp
virtual StatusCode removePlayView(IRTCView* v) = 0;
```

### Remove all playback views
```cpp
virtual StatusCode removeAllPlayView() = 0;
```
