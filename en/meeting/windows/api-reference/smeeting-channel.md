---
title: "ISMeetingChannel meeting API"
description: "Meeting-level C++ API of the SMeeting Windows SDK on ISMeetingChannel: channel ID and settings, setting the event handler before enter(), entering the meeting and exiting the waiting room, room and member info, nickname, chat, custom messages, raise hand, and waiting room management."
---

`ISMeetingChannel` represents one meeting object. It is created by `ISMeetingEngine::createChannel()` or `createChannelByMeetingId()` and destroyed by `ISMeetingEngine::leaveChannel()`.

---

## Channel basics

### Get the channel ID
```cpp
virtual std::string getChannelId() = 0;
```

Returns the room number / meeting ID passed in when the channel object was created. The ID stays the same even if the object switches to entering by meeting ID midway because of the waiting room, and it is the key `leaveChannel()` uses to release the object.

### Get the channel settings object
```cpp
virtual StatusCode getSetting(ISMeetingChannelSetting** sett) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| sett | ISMeetingChannelSetting** | Output pointer to the settings object |

**Returns**

`StatusCode` - Error code

### Set the channel event handler
```cpp
virtual StatusCode setEventHandler(ISMeetingChannelEvent* e) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| e | ISMeetingChannelEvent* | Event handler object |

**Returns**

`StatusCode` - Error code

> You must set the handler before `enter()`: events raised while entering the meeting (member list, camera state, and so on) fire before `enter()` returns.

---

## Enter / exit APIs

### Enter the meeting
```cpp
virtual StatusCode enter(std::string pass = "", Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| pass | std::string | Meeting password |
| back | Callback | Asynchronous callback |

`enter()` calls `/v1/meet/enter` and joins the underlying SRTC channel. Set the display name, avatar, streaming vendor, and so on for entering the meeting through `ISMeetingChannelSetting` before calling `enter()`.

**Returns**

`StatusCode` - Error code

### Exit the waiting room
```cpp
virtual StatusCode exitWaitRoom(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

---

## Room info APIs

### Get your own info
```cpp
virtual StatusCode getMe(std::string& s) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| s | std::string& | Output your own info as a JSON string |

**Returns**

`StatusCode` - Error code

### Get the room info
```cpp
virtual StatusCode getRoom(std::string& s) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| s | std::string& | Output the room info as a JSON string |

**Returns**

`StatusCode` - Error code

### Get info for all members
```cpp
virtual StatusCode getMembers(std::string& s) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| s | std::string& | Output member info as a JSON string |

**Returns**

`StatusCode` - Error code

### Get info for a specific member
```cpp
virtual StatusCode getMember(std::string uid, std::string& s) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| s | std::string& | Output member info as a JSON string |

**Returns**

`StatusCode` - Error code

### Get extended info
```cpp
virtual StatusCode getOpt(std::string& opt) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| opt | std::string& | Output extended info as a JSON string |

**Returns**

`StatusCode` - Error code

---

## User operation APIs

### Update your own name
```cpp
virtual StatusCode updateName(std::string name, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| name | std::string | New name |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Send a chat message
```cpp
virtual StatusCode sendRoomChatMessage(int tp, std::string msg, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| tp | int | Message type |
| msg | std::string | Message content |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Send a custom message
```cpp
virtual StatusCode sendRoomCustomMessage(std::string, std::string, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| First parameter | std::string | Message key |
| Second parameter | std::string | Message content |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Raise a hand
```cpp
virtual StatusCode requestHandup(int code, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| code | int | Raise-hand type code |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Lower a raised hand
```cpp
virtual StatusCode cancelHandup(int code, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| code | int | Raise-hand type code |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Get the online member list
```cpp
virtual StatusCode listOnlineMember(std::string _meetid, Callback back = nullptr) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| _meetid | std::string | Meeting ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

---

## Waiting room APIs

### Update the waiting room state
```cpp
virtual StatusCode adminUpdateWaitRoomState(bool v, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| v | bool | Waiting room state |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Get the waiting room user list
```cpp
virtual StatusCode adminWaitRoomUsers(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Move into the waiting room
```cpp
virtual StatusCode adminMoveInWaitRoom(std::string uid, std::string name, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| name | std::string | User name |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

### Move out of the waiting room
```cpp
virtual StatusCode adminMoveOutWaitRoom(std::string uid, std::string name, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| name | std::string | User name |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code
