---
title: "C Quickstart"
sidebarTitle: "C"
description: "Windows SMeeting C SDK quick integration: get the basic flow running in 10 minutes."
---

> Note: since `1.0.0-alpha.7`, `SMeeting_C.h` / `SMeetingEngineGlobal` have been ported to the split engine-level / meeting-level interfaces, matching the new `ISMeetingEngine` / `ISMeetingChannel` structure, so they can be used normally. Since `1.0.0-alpha.8`, the release package (`meeting_dll/include/`) **already ships** `SMeeting_C.h`, so `#include "SMeeting_C.h"` just works.

This page shows how to integrate the SMeeting SDK with C on Windows.

## Basic concepts

+ **SMeetingEngine**: the SDK core engine. Bind your callbacks with `SMeetingEngine_setEventHandler`.
+ Basic settings are made through the `SMeetingEngine_setXxx` family of functions.
+ Some APIs can only be called after you have entered the meeting.

---

## Initialize the SDK

```c
#include "SMeeting_C.h"

// Initialize the engine
StatusCodeC ret = SMeetingEngine_Init_C();
if (ret != 0) {
    return ret;
}

// Set the event callback
SMeetingEngine_setEventHandler(RoomEvent, NULL);
```

### Implement the event callback function

```c
// Event callback
int RoomEvent(int iEvent, void* pEventData, int iDataSize, void* pContext)
{
    switch(iEvent) {
        case SMeeting_Func_CallBack:
            // A function result came back; see "callback key: xx"
            break;
        case SMeeting_Event_Disconnected:
            // The connection dropped
            break;
            
        case SMeeting_Event_Reconnected:
            // Reconnected successfully
            break;
            
        case SMeeting_Event_UserEnter:
            // A user entered
            break;
            
        case SMeeting_Event_UserExit:
            // A user left
            break;
            
        // ... handle the other events you need
    }
    return 0;
}
```

---

## Set the language

```c
// BCP 47 language code, e.g. "zh-CN", "en"; affects the SDK error texts and the
// language of backend requests. Process-wide, callable at any time, English until you call it
StatusCodeC ret = SMeetingEngine_SetLanguage_C("zh-CN");
```

---

## Log in and log out

### Log in

```c
const char* token = "your_token_here";
StatusCodeC ret = SMeetingEngine_login(token);
// The result arrives asynchronously in the callback (callback key: 100)
```

### Log out

```c
StatusCodeC ret = SMeetingEngine_logout();
// The result arrives asynchronously in the callback (callback key: 101)
```

---

## Create a meeting

```c
const char* json = "{\"title\":\"My meeting\",\"content\":\"Meeting description\",\"meeting_type\":1,\"meeting_mode\":1}";
int json_len = strlen(json);

char* outdata = NULL;
int outlen = 0;

StatusCodeC ret = SMeetingEngine_createRoom(json, json_len);
// The result arrives asynchronously in the callback (callback key: 110)
// On success it carries the meeting number
```

---

## Enter a meeting

### Configure SDK settings

```c
SMeetingEngine_setStream_model(1);          // Stream media mode
SMeetingEngine_setSpeaker_interval(500);    // Audio-level callback period (ms)
SMeetingEngine_setStat_interval(10000);     // Network-stat callback period (ms)
SMeetingEngine_setEnable_audio_record(1);   // Enable audio recording
SMeetingEngine_setEnable_stream_log(1);     // Enable the stream log
```

### Enter the room

```c
const char* roomno = "123456789";
const char* pass = "";  // Meeting password; empty when there is none

// The display name comes from the token used by SMeetingEngine_login; it is no
// longer an enter parameter
StatusCodeC ret = SMeetingEngine_enterRoom(roomno, pass);
// The result arrives asynchronously in the callback (callback key: 112)
```

---

## Exit the meeting

```c
StatusCodeC ret = SMeetingEngine_exitRoom();
// The result arrives asynchronously in the callback (callback key: 114)
```

---

## End the meeting (host)

```c
// The host dissolves the meeting
StatusCodeC ret = SMeetingEngine_adminDestroyRoom();
// The result arrives asynchronously in the callback (callback key: 200)
```

---

## Cancel a meeting (outside the meeting)

```c
const char* meeting_id = "sw46gz";
StatusCodeC ret = SMeetingEngine_cancelRoom(meeting_id);
// The result arrives asynchronously in the callback (callback key: 108)
```

---

## Get room and member info

```c
char* out = NULL;
int len = 0;

// Local member
SMeetingEngine_getMe(&out, &len);

// Room
SMeetingEngine_getRoom(&out, &len);

// Every member
SMeetingEngine_getMembers(&out, &len);

// One member
const char* uid = "user_123";
SMeetingEngine_getMember(uid, &out, &len);
```

---

## Update your nickname

```c
const char* new_name = "New name";
StatusCodeC ret = SMeetingEngine_updateName(new_name);
// The result arrives asynchronously in the callback (callback key: 301)
```

---

## Get the device list

```c
// type: 2 SIP, 3 H323, 4 GB28181, 5 RTSP pull, 6 RTMP pull, 7 file playback, 8 Tencent Meeting, 9 AI
const char* types = "2|3|5";  // pipe separated
int page = 1;
const char* find_key = "";

char* out = NULL;
int len = 0;

StatusCodeC ret = SMeetingEngine_listAgent(types, page, find_key);
// The result arrives asynchronously in the callback (callback key: 103)
```

---

## Camera operations

### Turn on the camera

```c
// Set the render window key
int camera_render_key = 1;
SMeetingEngine_setCameraRenderKey(camera_render_key);

// Request the camera to be opened
StatusCodeC ret = SMeetingEngine_requestOpenCamera();
// The result arrives asynchronously in the callback (callback key: 802)
```

### Switch cameras

```c
const char* camera_name = "Integrated Camera";
int width = 640;
int height = 480;

StatusCodeC ret = SMeetingEngine_switchCamera(camera_name, width, height);
```

### Turn off the camera

```c
StatusCodeC ret = SMeetingEngine_closeCamera();
// The result arrives asynchronously in the callback (callback key: 803)
```

---

## Remote video playback

### Start playback

```c
const char* uid = "user_123";
const char* track_desc = "camera_big";  // or "camera_small"
int render_key = 2;  // render key

StatusCodeC ret = SMeetingEngine_loadRemoteVideo(uid, track_desc, render_key);
```

### Stop playback

```c
const char* uid = "user_123";
const char* track_desc = "camera_big";

StatusCodeC ret = SMeetingEngine_unloadRemoteVideo(uid, track_desc);
```

---

## Microphone operations

### Turn on the microphone

```c
StatusCodeC ret = SMeetingEngine_requestOpenMic();
// The result arrives asynchronously in the callback (callback key: 800)
```

### Switch microphones

```c
const char* mic_name = "Default Microphone";
StatusCodeC ret = SMeetingEngine_switchMic(mic_name);
```

### Turn off the microphone

```c
StatusCodeC ret = SMeetingEngine_closeMic();
// The result arrives asynchronously in the callback (callback key: 801)
```

---

## Speaker operations

### Turn on the speaker

```c
StatusCodeC ret = SMeetingEngine_openSpeaker();
```

### Switch speakers

```c
const char* speaker_name = "Default Speakers";
StatusCodeC ret = SMeetingEngine_switchSpeaker(speaker_name);
```

### Turn off the speaker

```c
StatusCodeC ret = SMeetingEngine_closeSpeaker();
```

---

## Screen sharing

### Start sharing

```c
// tp: 1 = screen share, 2 = window share
// data: screen index or window information
int tp = 1;
const char* data = "0";  // primary screen

StatusCodeC ret = SMeetingEngine_requestShare(tp, data);
// The result arrives asynchronously in the callback (callback key: 804)
```

### Stop sharing

```c
StatusCodeC ret = SMeetingEngine_stopShare();
// The result arrives asynchronously in the callback (callback key: 805)
```

---

## Chat messages

### Send a chat message

```c
// tp: 1 = text, 2 = file, 3 = image, 4 = sound
int msg_type = 1;
const char* msg = "Hello everyone!";

StatusCodeC ret = SMeetingEngine_sendRoomChatMessage(msg_type, msg);
// The result arrives asynchronously in the callback (callback key: 302)
```

---

## Host management APIs

### Ask a member to turn on the camera

```c
const char* uid = "user_123";
StatusCodeC ret = SMeetingEngine_adminRequestUserOpenCamera(uid);
// The result arrives asynchronously in the callback (callback key: 220)
```

### Turn off a member's camera

```c
StatusCodeC ret = SMeetingEngine_adminCloseUserCamera(uid);
// The result arrives asynchronously in the callback (callback key: 218)
```

### Ask a member to turn on the microphone

```c
StatusCodeC ret = SMeetingEngine_adminRequestUserOpenMic(uid);
// The result arrives asynchronously in the callback (callback key: 221)
```

### Turn off a member's microphone

```c
StatusCodeC ret = SMeetingEngine_adminCloseUserMic(uid);
// The result arrives asynchronously in the callback (callback key: 219)
```

### Remove a member

```c
StatusCodeC ret = SMeetingEngine_adminKickUserOut(uid);
// The result arrives asynchronously in the callback (callback key: 222)
```

### Set the room's microphone permissions

```c
bool self_unmute_mic_disabled = true;   // whether members may unmute themselves
bool mic_disabled = true;               // whether room audio is disabled

StatusCodeC ret = SMeetingEngine_adminUpdateRoomMicState2(self_unmute_mic_disabled, mic_disabled);
// The result arrives asynchronously in the callback (callback key: 207)
```

---

## MCU composite video

### Play the composite stream

```c
int mcu_render_key = 3;
StatusCodeC ret = SMeetingEngine_loadMcuVideo(mcu_render_key);
```

### Stop playback

```c
StatusCodeC ret = SMeetingEngine_unloadMcuVideo();
```

---

## Local recording

### Set the recording options

```c
const char* filepath = "C:\\record\\meeting.mp4";
int filepath_len = strlen(filepath);

SMeetingEngine_setRecordFileName(filepath, filepath_len);

// Watermark
const char* mask = "Meeting recording";
SMeetingEngine_setWaterMask(mask, strlen(mask));

// Recording window
void* hwnd = GetWindowHandle();
SMeetingEngine_setRecordHwnd(hwnd, 0, 0, 0, 0);
```

### Start recording

```c
StatusCodeC ret = SMeetingEngine_startRecord();
```

### Pause / resume recording

```c
SMeetingEngine_pauseRecord();
```

### Stop recording

```c
SMeetingEngine_stopRecord();
```

---

## Status code handling

### Get the text of a status code

```c
StatusCodeC code = 100001;
char msg[256];
int len = SMeetingEngine_GetStatusMsg_C(code, msg, sizeof(msg));
printf("Status: %s\n", msg);
```

### Common status codes

| Code | Meaning |
| --- | --- |
| 0 | Success |
| 100001 | System error |
| 100002 | Not initialized |
| 100006 | Invalid argument |
| 100009 | Network error |

---

## Complete example

```c
#include "SMeeting_C.h"
#include <stdio.h>
#include <string.h>
#include <windows.h>


#define camera_render_key 1
#define remote_render_key 2
#define mcu_render_key 2

YUV420Player* camera_player = nullptr;
YUV420Player* remote_player = nullptr;
YUV420Player* mcu_player = nullptr;
// Event callback
int RoomEvent(int iEvent, void* pEventData, int iDataSize, void* pContext)
{
    switch(iEvent) {
        case SMeeting_Func_CallBack:
            // A function result came back; see "callback key: xx"
            break;
        case SMeeting_Event_Disconnected:
            printf("Disconnected\n");
            break;
            
        case SMeeting_Event_Reconnected:
            printf("Reconnected\n");
            break;
            
        case SMeeting_Event_UserEnter:
            printf("User entered\n");
            break;
        //...
    }
    return 0;
}

void RenderEvent(int renderkey, const unsigned char* buf, int w, int h, int label, void* pContext)
{
    if(renderkey == camera_render_key){
        if(camera_player){
            camera_player->render(buf,w,h,label);
        }
    }
    //...
    return 0;
}

int main() {
    // Initialize
    StatusCodeC ret = SMeetingEngine_Init_C();
    if (ret != 0) {
        printf("Init failed: %d\n", ret);
        return -1;
    }

    // Set the event callbacks
    SMeetingEngine_setEventHandler(RoomEvent, NULL);
    SMeetingEngine_setRenderHandler(RenderEvent, NULL);


    // Log in
    const char* token = "your_token";
    ret = SMeetingEngine_login(token);
    if (ret != 0) {
        printf("Login failed: %d\n", ret);
        return -1;
    }

    // Wait for the login callback... SMeeting_Func_CallBack key:100
    Sleep(1000);

    // Create a meeting
    const char* json = "{\"title\":\"Test meeting\",\"meeting_type\":1}";
    ret = SMeetingEngine_createRoom(json, strlen(json));
    
    // Wait for async work (a real app would run an event loop)
    Sleep(30000);

    // Cleanup
    SMeetingEngine_logout();
    
    // Configure
    SMeetingEngine_setStream_model(1);
    SMeetingEngine_setStat_interval(10000);

    const char* no ="111222333";
    SMeetingEngine_enterRoom(no,"");
    return 0;
}
```

---

## Callback event reference

### Connection state events

| Event constant | Value | Meaning |
| --- | --- | --- |
| SMeeting_Event_Disconnected | 1 | Connection dropped |
| SMeeting_Event_Reconnected | 2 | Reconnected successfully |
| SMeeting_Event_Reconnecting | 3 | Reconnecting |

### User events

| Event constant | Value | Meaning |
| --- | --- | --- |
| SMeeting_Event_UserEnter | 100 | User entered |
| SMeeting_Event_UserExit | 101 | User left |
| SMeeting_Event_UserCameraStateChanged | 102 | Camera state changed |
| SMeeting_Event_UserAudioStateChanged | 103 | Audio state changed |
| SMeeting_Event_UserNameChanged | 104 | Name changed |

### Room events

| Event constant | Value | Meaning |
| --- | --- | --- |
| SMeeting_Event_RoomChatMessage | 208 | Chat message |
| SMeeting_Event_RoomShareStart | 206 | Sharing started |
| SMeeting_Event_RoomShareStop | 207 | Sharing stopped |

See `SMeeting_C.h` for the full list of event constants.

---

## Notes

1. **Callbacks are asynchronous**: most APIs return their result through a callback rather than the return value.
2. **Thread safety**: callbacks may be invoked on different threads—take care when touching shared state.
3. **Initialization order**: you must call `SMeetingEngine_Init_C()` before any other API.
4. **UTF-8 encoding**: all string parameters are UTF-8.
