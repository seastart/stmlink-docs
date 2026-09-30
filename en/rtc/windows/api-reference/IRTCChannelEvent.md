---
title: "IRTCChannelEvent"
description: "API reference for IRTCChannelEvent, the Windows SRTC per-channel callback interface: join success, channel and user updates, stream add/update/remove, custom messages, uplink/downlink levels and statistics, audio levels, disconnection, reconnection, and recording status. Register it before join()."
---

## Description
The channel-level event callback interface. Inherit from it, override the callback methods, and register it with [IRTCChannel::setEventHandler](/en/rtc/windows/api-reference/IRTCChannel#set-the-event-handler).

## Inheritance
None

## Callbacks

Callbacks are registered **per channel**: one `IRTCChannelEvent` instance is bound to one [IRTCChannel](/en/rtc/windows/api-reference/IRTCChannel),
so none of the callbacks **carry** a `channelId` parameter (the channel-level callbacks on the old `IRTCEngineEvent` did).
You can bind the same instance to multiple channels; in that case you need to tell the channels apart yourself.

**You must register it before `IRTCChannel::join()`**; otherwise you don't receive `onJoinChannel`—it's called back before `join()` returns.

### Join channel success callback
```cpp
virtual void onJoinChannel(const char* channel, int channelSize, const char* me, int meSize, const char* members, int memberSize, const char* opts, int optSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| channel | const char* | Channel info JSON |
| channelSize | int | Length of the channel info JSON |
| me | const char* | Your own user info JSON |
| meSize | int | Length of your own user info |
| members | const char* | JSON array of info for all users in the channel |
| memberSize | int | Length of the user info array |
| opts | const char* | System configuration parameters |
| optSize | int | Length of the system configuration parameters |

Note: callbacks are registered per channel (`IRTCChannel::setEventHandler`), so `channelId` is no longer passed back. To tell channels apart, use `IRTCChannel::getChannelId()`.

### Channel status update callback
```cpp
virtual void onChannelUpdate(const char* props, int propsSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| props | const char* | Channel properties JSON |
| propsSize | int | Length of the properties string |

### User joined callback
```cpp
virtual void onUserJoin(const char* user, int userSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| user | const char* | Details JSON of the user who joined |
| userSize | int | Length of the user info string |

### User info update callback
```cpp
virtual void onUserUpdate(const char* user, int userSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| user | const char* | Updated user info JSON |
| userSize | int | Length of the user info string |

### User stream added callback
```cpp
virtual void onUserStreamAdd(const char* user, const char* stream, int streamSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| user | const char* | User ID |
| stream | const char* | Stream info JSON |
| streamSize | int | Length of the stream info string |

### User stream updated callback
```cpp
virtual void onUserStreamUpdate(const char* user, const char* stream, int streamSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| user | const char* | User ID |
| stream | const char* | Updated stream info JSON |
| streamSize | int | Length of the stream info string |

### User stream removed callback
```cpp
virtual void onUserStreamRemove(const char* user, const char* stream, int streamSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| user | const char* | User ID |
| stream | const char* | Info JSON of the removed stream |
| streamSize | int | Length of the stream info string |

### User left callback
```cpp
virtual void onUserLeave(const char* user, int userSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| user | const char* | Details JSON of the user who left |
| userSize | int | Length of the user info string |

### Custom message callback
```cpp
virtual void onCustomMessage2(const char* action, const char* senderid, const char* name, int name_len, const char* message, int messageSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| action | const char* | Message type / action |
| senderid | const char* | Sender's user ID |
| name | const char* | Sender's display name |
| name_len | int | Length of the display name |
| message | const char* | Message content |
| messageSize | int | Length of the message content |

### Uplink level change callback
```cpp
virtual void onUpLevel(int level) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| level | int | Quality level (0: good, 1: fair, 2: poor, 3: very poor) |

### Downlink level change callback
```cpp
virtual void onDownLevel(const char* id, int level) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| id | const char* | The user's ID |
| level | int | Quality level (0: good, 1: fair, 2: poor, 3: very poor) |

### Uplink statistics callback
```cpp
virtual void onUpStat(const char* upstat, int upstatsize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| upstat | const char* | Uplink statistics JSON |
| upstatsize | int | Length of the uplink statistics |

### Downlink statistics callback
```cpp
virtual void onDownStat(const char* downstat, int downstatsize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| downstat | const char* | Downlink statistics JSON |
| downstatsize | int | Length of the downlink statistics |

### Frame timeout callback
```cpp
virtual void onFrameTimeOut(const char* uid, const char* track_id, const char* track_desc, int loading) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | const char* | User ID |
| track_id | const char* | Track ID |
| track_desc | const char* | Track description |
| loading | int | Loading state |

### Audio level callback
```cpp
virtual void onSpeakers(const char* Speakers) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| Speakers | const char* | JSON array of speakers' audio energy data |

### Device status change callback
```cpp
virtual void onDeviceStatusChange(int tp, int status) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| tp | int | Device type (1: microphone, 2: speaker, 3: camera) |
| status | int | Status (1: error, 2: recovered) |

### Share target not found callback
```cpp
virtual void onShareTargetNotFind() = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |

### Disconnected callback
```cpp
virtual void onDisconnected(int reason, StatusCode code, const char* message, size_t message_size) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| reason | int | Disconnect reason (-1: error, 0: unknown, 1: left voluntarily, 2: removed from the channel, 3: replaced by another session with the same uid, 4: heartbeat timeout, 5: channel destroyed) |
| code | StatusCode | Error code |
| message | const char* | Error description |
| message_size | size_t | Length of the error description |

### Reconnected callback
```cpp
virtual void onReconnected(const char* options, size_t options_size) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| options | const char* | Extended reconnection info |
| options_size | size_t | Length of the extended info |

### Reconnecting callback
```cpp
virtual void onReconnecting() = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |

### Recording status change callback
```cpp
virtual void onRecordStatusChange(const char* key, LocalRecordStatusEnum status, const char* msg) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| key | const char* | Recording task key |
| status | LocalRecordStatusEnum | Recording status; see [LocalRecordStatusEnum](/en/rtc/windows/enums) |
| msg | const char* | Status description; the error message when an error occurs |
