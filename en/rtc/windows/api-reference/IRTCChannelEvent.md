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
virtual void onJoinChannel(const char* channelJson, int channelSize, const char* meJson, int meSize, const char* membersJson, int memberSize, const char* optsJson, int optSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| channelJson | const char* | Channel info JSON |
| channelSize | int | Length of the channel info JSON |
| meJson | const char* | Your own user info JSON |
| meSize | int | Length of your own user info |
| membersJson | const char* | JSON array of info for all users in the channel |
| memberSize | int | Length of the user info array |
| optsJson | const char* | System configuration parameters |
| optSize | int | Length of the system configuration parameters |

Note: callbacks are registered per channel (`IRTCChannel::setEventHandler`), so `channelId` is no longer passed back. To tell channels apart, use `IRTCChannel::getChannelId()`.

### Channel status update callback
```cpp
virtual void onChannelUpdate(const char* propsJson, int propsSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| propsJson | const char* | Channel properties JSON |
| propsSize | int | Length of the properties string |

### User joined callback
```cpp
virtual void onUserJoin(const char* userJson, int userSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| userJson | const char* | Details JSON of the user who joined |
| userSize | int | Length of the user info string |

### User info update callback
```cpp
virtual void onUserUpdate(const char* userJson, int userSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| userJson | const char* | Updated user info JSON |
| userSize | int | Length of the user info string |

### User stream added callback
```cpp
virtual void onUserStreamAdd(const char* uid, const char* streamJson, int streamSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | const char* | User ID |
| streamJson | const char* | Stream info JSON |
| streamSize | int | Length of the stream info string |

### User stream updated callback
```cpp
virtual void onUserStreamUpdate(const char* uid, const char* streamJson, int streamSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | const char* | User ID |
| streamJson | const char* | Updated stream info JSON |
| streamSize | int | Length of the stream info string |

### User stream removed callback
```cpp
virtual void onUserStreamRemove(const char* uid, const char* streamJson, int streamSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | const char* | User ID |
| streamJson | const char* | Info JSON of the removed stream |
| streamSize | int | Length of the stream info string |

### User left callback
```cpp
virtual void onUserLeave(const char* userJson, int userSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| userJson | const char* | Details JSON of the user who left |
| userSize | int | Length of the user info string |

### Custom message callback
```cpp
virtual void onCustomMessage2(const char* action, const char* senderid, const char* name, int nameSize, const char* message, int messageSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| action | const char* | Message type / action |
| senderid | const char* | Sender's user ID |
| name | const char* | Sender's display name |
| nameSize | int | Length of the display name |
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
virtual void onDownLevel(const char* uid, int level) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | const char* | The user's ID |
| level | int | Quality level (0: good, 1: fair, 2: poor, 3: very poor) |

### Uplink statistics callback
```cpp
virtual void onUpStat(const char* upStatJson, int upStatSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| upStatJson | const char* | Uplink statistics JSON |
| upStatSize | int | Length of the uplink statistics |

### Downlink statistics callback
```cpp
virtual void onDownStat(const char* downStatJson, int downStatSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| downStatJson | const char* | Downlink statistics JSON |
| downStatSize | int | Length of the downlink statistics |

### Frame timeout callback
```cpp
virtual void onFrameTimeOut(const char* uid, const char* trackId, const char* trackDesc, int loading) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | const char* | User ID |
| trackId | const char* | Track ID |
| trackDesc | const char* | Track description |
| loading | int | Loading state |

### Audio level callback
```cpp
virtual void onSpeakers(const char* speakersJson) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| speakersJson | const char* | JSON array of speakers' audio energy data |

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
virtual void onDisconnected(int reason, StatusCode code, const char* message, size_t messageSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| reason | int | Disconnect reason (-1: error, 0: unknown, 1: left voluntarily, 2: removed from the channel, 3: replaced by another session with the same uid, 4: heartbeat timeout, 5: channel destroyed) |
| code | StatusCode | Error code |
| message | const char* | Error description |
| messageSize | size_t | Length of the error description |

### Reconnected callback
```cpp
virtual void onReconnected(const char* optionsJson, size_t optionsSize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| optionsJson | const char* | Extended reconnection info |
| optionsSize | size_t | Length of the extended info |

### Reconnecting callback
```cpp
virtual void onReconnecting() = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |

### Recording status change callback
```cpp
virtual void onRecordStatusChange(const char* channelId, LocalRecordStatusEnum status, const char* msg) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| channelId | const char* | Recording task key |
| status | LocalRecordStatusEnum | Recording status; see [LocalRecordStatusEnum](/en/rtc/windows/enums) |
| msg | const char* | Status description; the error message when an error occurs |
