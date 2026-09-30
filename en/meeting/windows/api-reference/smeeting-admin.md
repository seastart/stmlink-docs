---
title: "Host management APIs"
description: "C++ host and co-host APIs of the SMeeting Windows SDK on ISMeetingChannel: end the meeting, room-wide camera, microphone, chat, screenshot, lock, and sharing controls, member name, role, and chat permissions, controlling members' devices, removing members, raise-hand approval, and invites."
---

All of the following APIs are called on [ISMeetingChannel](/en/meeting/windows/api-reference/smeeting-channel) and can only be executed by the host or members with the corresponding permission.

---

## Room controls

### End the meeting
```cpp
virtual StatusCode adminDestroyRoom(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update the room name
```cpp
virtual StatusCode adminUpdateRoomName() = 0;
```

**Returns**

`StatusCode` - Error code

### Update the room video state
```cpp
virtual StatusCode adminUpdateRoomVideoState() = 0;
```

**Returns**

`StatusCode` - Error code

### Update the room audio state
```cpp
virtual StatusCode adminUpdateRoomAudioState() = 0;
```

**Returns**

`StatusCode` - Error code

### Update the room camera state
```cpp
virtual StatusCode adminUpdateRoomCameraState(bool self_unmute_camera_disabled, bool camera_disabled, Callback back = NULL) = 0;
virtual StatusCode adminUpdateRoomCameraState(bool self_unmute_camera_disabled, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| self_unmute_camera_disabled | bool | Whether members are prevented from turning their cameras back on themselves |
| camera_disabled | bool | Whether cameras are disabled |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update the room microphone state
```cpp
virtual StatusCode adminUpdateRoomMicState(bool self_unmute_mic_disabled, bool mic_disabled, Callback back = NULL) = 0;
virtual StatusCode adminUpdateRoomMicState(bool self_unmute_mic_disabled, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| self_unmute_mic_disabled | bool | Whether members are prevented from unmuting themselves |
| mic_disabled | bool | Whether microphones are disabled |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update the room chat state
```cpp
virtual StatusCode adminUpdateRoomChatDisabled(bool chat_disabled, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| chat_disabled | bool | Whether chat is disabled |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update the room screenshot state
```cpp
virtual StatusCode adminUpdateRoomScreenshotDisabled(bool screenshot_disabled, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| screenshot_disabled | bool | Whether screenshots are disabled |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update the room MCU mode
```cpp
virtual StatusCode adminUpdateRoomMCUMode() = 0;
```

**Returns**

`StatusCode` - Error code

### Update the room lock state
```cpp
virtual StatusCode adminUpdateRoomLocked(bool locked, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| locked | bool | Whether the room is locked |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Stop sharing in the room
```cpp
virtual StatusCode adminStopRoomShare(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update the room sharing state
```cpp
virtual StatusCode adminUpdateRoomShareState(bool v, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| v | bool | Sharing state |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update whether entering before the host is disabled
```cpp
virtual StatusCode adminUpdateEnterBeforeHostDisabled(bool v, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| v | bool | Whether members are prevented from entering before the host |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

---

## Member controls

### Update a member's name
```cpp
virtual StatusCode adminUpdateUserName(std::string uid, std::string name, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| name | std::string | New name |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update a member's role
```cpp
virtual StatusCode adminUpdateUserRole(std::string uid, int role, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| role | int | Role type |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update a member's chat permission
```cpp
virtual StatusCode adminUpdateUserChatDisabled(std::string uid, bool chat_disabled, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| chat_disabled | bool | Whether chat is disabled |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Disable a member's camera
```cpp
virtual StatusCode adminDisableUserCamera() = 0;
```

**Returns**

`StatusCode` - Error code

### Disable a member's microphone
```cpp
virtual StatusCode adminDisableUserMic() = 0;
```

**Returns**

`StatusCode` - Error code

### Turn off a member's camera
```cpp
virtual StatusCode adminCloseUserCamera(std::string uid, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Turn off a member's microphone
```cpp
virtual StatusCode adminCloseUserMic(std::string uid, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Ask a member to turn on the camera
```cpp
virtual StatusCode adminRequestUserOpenCamera(std::string uid, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Ask a member to turn on the microphone
```cpp
virtual StatusCode adminRequestUserOpenMic(std::string uid, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Remove a member
```cpp
virtual StatusCode adminKickUserOut(std::string uid, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Respond to a raised hand
```cpp
virtual StatusCode adminConfirmHandup(std::string uid, int code, bool approve, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| code | int | Raise-hand type code |
| approve | bool | Whether to approve |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Invite devices to the meeting
```cpp
virtual StatusCode adminInviteAgent(std::string no, int tp, std::vector<std::string> devs, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| no | std::string | Room number |
| tp | int | Type |
| devs | `std::vector<std::string>` | List of devices |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update the invitee list
```cpp
virtual StatusCode adminUpdateConferee(std::vector<std::string> conferee, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| conferee | `std::vector<std::string>` | List of invitees |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Update the layout
```cpp
virtual StatusCode adminUpdateLayout(std::string layout, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| layout | std::string | Layout configuration |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Call users
```cpp
virtual StatusCode adminCallUsers(std::vector<std::string> users, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| users | `std::vector<std::string>` | List of users |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Remind users
```cpp
virtual StatusCode adminRemind(std::vector<std::string> users, bool sms, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| users | `std::vector<std::string>` | List of users |
| sms | bool | Whether to send an SMS |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code
