---
title: "ISMeetingEngine engine API"
description: "Engine-level C++ API of the SMeeting Windows SDK: global init and version functions, engine settings and event handler, login and logout, meeting management HTTP APIs, creating and leaving ISMeetingChannel objects, device enumeration, log upload, IM, and resource drive APIs."
---

`ISMeetingEngine` is the SDK engine object. It handles engine-level capabilities such as the login session, the meeting management HTTP APIs, the channel object lifecycle, device enumeration, IM, and the resource drive.

All in-meeting operations and media objects are on [ISMeetingChannel](/en/meeting/windows/api-reference/smeeting-channel).

---

## Global functions

### Initialize the engine
```cpp
SMEETING_API StatusCode SMEETING_CALL SMeetingEngine_Init(ISMeetingEngine** meet);
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| meet | ISMeetingEngine** | Output pointer to the engine object |

**Returns**

`StatusCode` - Error code

### Get the SDK version
```cpp
SMEETING_API StatusCode SMEETING_CALL SMeetingEngine_Version(std::string& s);
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| s | std::string& | Output version string |

**Returns**

`StatusCode` - Error code

### Get an error code description
```cpp
SMEETING_API void SMEETING_CALL SMeetingEngine_GetStatusMsg(StatusCode code, char* msg);
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| code | StatusCode | Error code |
| msg | char* | Output buffer for the error description |

---

## Engine settings and callbacks

### Get the engine settings object
```cpp
virtual StatusCode getSetting(ISMeetingSetting** sett) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| sett | ISMeetingSetting** | Output pointer to the settings object |

**Returns**

`StatusCode` - Error code

### Set the engine event handler
```cpp
virtual StatusCode setEventHandler(ISMeetingEngineEvent* e) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| e | ISMeetingEngineEvent* | Event handler object |

**Returns**

`StatusCode` - Error code

---

## Login and logout APIs

### Log in
```cpp
virtual StatusCode login(std::string token, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| token | std::string | Login token |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Log out
```cpp
virtual StatusCode logout(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Get your own info
```cpp
virtual StatusCode getSelf(Callback back) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Get the device list
```cpp
virtual StatusCode listAgent(std::vector<int> type, int page, std::string find_key = "", Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| type | `std::vector<int>` | List of device types |
| page | int | Page number |
| find_key | std::string | Search keyword |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

---

## Meeting management APIs

### Create a meeting
```cpp
virtual StatusCode createRoom(SMeetingCreateMeetingModel model, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| model | SMeetingCreateMeetingModel | Room configuration model |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update room info
```cpp
virtual StatusCode updateRoom(SMeetingCreateMeetingModel model, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| model | SMeetingCreateMeetingModel | Room configuration model |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update the background and attachments
```cpp
virtual StatusCode updateBgAndAttach(std::string meeting_id, std::string background, std::vector<SMeetingMeetingAttachments>, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| meeting_id | std::string | Meeting ID |
| background | std::string | Background URL |
| attachments | `std::vector<SMeetingMeetingAttachments>` | List of attachments |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Get ongoing meetings
```cpp
virtual StatusCode attendeeRoom(int page, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| page | int | Page number |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Get past meetings
```cpp
virtual StatusCode attendedRoom(int page, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| page | int | Page number |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Get meeting details
```cpp
virtual StatusCode detailRoom(std::string meeting_id, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| meeting_id | std::string | Meeting ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Cancel a meeting
```cpp
virtual StatusCode cancelRoom(std::string meeting_id, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| meeting_id | std::string | Meeting ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Get the meeting member list
```cpp
virtual StatusCode participantRoom(std::string meeting_id, int page, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| meeting_id | std::string | Meeting ID |
| page | int | Page number |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

---

## Meeting channel APIs

### Create a channel object
```cpp
virtual StatusCode createChannel(std::string roomno, ISMeetingChannel** ch) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| roomno | std::string | Room number |
| ch | ISMeetingChannel** | Output pointer to the channel object |

`createChannel` only creates the channel object and does **not** enter the meeting right away. After it returns, call `ISMeetingChannel::enter()` to actually enter the meeting.

**Returns**

`StatusCode` - Error code

### Create a channel object by meeting ID
```cpp
virtual StatusCode createChannelByMeetingId(std::string meetingid, ISMeetingChannel** ch) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| meetingid | std::string | Meeting ID |
| ch | ISMeetingChannel** | Output pointer to the channel object |

**Returns**

`StatusCode` - Error code

### Leave a channel
```cpp
virtual StatusCode leaveChannel(std::string channelId, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| channelId | std::string | Channel ID, that is, the room number you passed to `createChannel` |
| back | Callback | Asynchronous callback |

After you exit, the channel object is destroyed; don't use the original `ISMeetingChannel*` pointer again.

**Returns**

`StatusCode` - Error code

### Leave all channels
```cpp
virtual StatusCode leaveAllChannel(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Get the current channel ID list
```cpp
virtual StatusCode getChannelIds(std::string& s) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| s | std::string& | Output list of channel IDs as a JSON array |

**Returns**

`StatusCode` - Error code

---

## Device enumeration APIs

### Get the video device list
```cpp
virtual StatusCode getEnumVideo(std::string& dev) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| dev | std::string& | Output video devices as a JSON string |

**Returns**

`StatusCode` - Error code

### Get the screen list
```cpp
virtual StatusCode getEnumScreen(std::string& dev) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| dev | std::string& | Output screens as a JSON string |

**Returns**

`StatusCode` - Error code

### Get the audio device list
```cpp
virtual StatusCode getEnumAudio(std::string& dev) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| dev | std::string& | Output audio devices as a JSON string |

**Returns**

`StatusCode` - Error code

### Get the speaker list
```cpp
virtual StatusCode getEnumSpeaker(std::string& dev) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| dev | std::string& | Output speakers as a JSON string |

**Returns**

`StatusCode` - Error code

---

## Log and IM APIs

### Upload a log
```cpp
virtual StatusCode addUploadLog(const char* type, const char* msg) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| type | const char* | Log type |
| msg | const char* | Log content |

**Returns**

`StatusCode` - Error code

### Enable IM
```cpp
virtual StatusCode enableIm(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Disable IM
```cpp
virtual void disableIm(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

---

## Cloud storage and resource management APIs

### Presigned upload
```cpp
virtual StatusCode presignedPutObject(std::string type, std::string meeting_id, std::string ext, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| type | std::string | File type |
| meeting_id | std::string | Meeting ID |
| ext | std::string | File extension |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Presigned download
```cpp
virtual StatusCode presignedGetObject(std::string id, std::string res_key, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| id | std::string | Resource ID |
| res_key | std::string | Resource key |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### List resources
```cpp
virtual StatusCode resourcesList(std::string parent_id, std::string meeting_id, std::string res_name, int page, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| parent_id | std::string | Parent resource ID |
| meeting_id | std::string | Meeting ID |
| res_name | std::string | Resource name |
| page | int | Page number |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Create a resource
```cpp
virtual StatusCode resourcesCreate(SMeetingResourcesModel* mode, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| mode | SMeetingResourcesModel* | Resource model |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Rename a resource
```cpp
virtual StatusCode resourcesRename(std::string id, std::string res_key, std::string res_name, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| id | std::string | Resource ID |
| res_key | std::string | Resource key |
| res_name | std::string | New resource name |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Move a resource
```cpp
virtual StatusCode resourcesMoveto(std::string id, std::string res_key, std::string parent_id, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| id | std::string | Resource ID |
| res_key | std::string | Resource key |
| parent_id | std::string | Target parent resource ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Delete a resource
```cpp
virtual StatusCode resourcesRemove(std::string id, std::string res_key, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| id | std::string | Resource ID |
| res_key | std::string | Resource key |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Set the meeting background
```cpp
virtual StatusCode resourcesMeetingBg(std::string id, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| id | std::string | Resource ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

---

## Release API

### Release the engine
```cpp
virtual void del() = 0;
```
