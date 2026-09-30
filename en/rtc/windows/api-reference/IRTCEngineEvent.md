---
title: "IRTCEngineEvent"
description: "API reference for IRTCEngineEvent, the Windows SRTC engine-level callback interface: network probe results, device plug and unplug, default device changes, and IM connection and message callbacks. Read when handling events that don't belong to any single channel."
---

## Description
The engine-level event callback interface. Inherit from it, override the callback methods, and register it with [IRTCEngine::setEventHandler](/en/rtc/windows/api-reference/IRTCEngine#set-the-event-handler).

## Inheritance
None

## Callbacks

This interface only has callbacks that **don't belong to any single channel**: device changes, network probing, and IM.
Channel-level callbacks (joining a channel, users joining and leaving, stream changes, statistics, disconnection and reconnection, recording status) have moved to
[IRTCChannelEvent](/en/rtc/windows/api-reference/IRTCChannelEvent), and their leading `channelId` parameter has been removed.


The following callbacks don't belong to any channel, and their signatures are unchanged.

### Network probe result callback
```cpp
virtual void onProbeResult(int action, const char* result) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| action | int | Probe step identifier |
| result | const char* | Probe result JSON |

### Device change callback
```cpp
virtual void onDeviceChange(int type, int action, const char* name, int namesize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| type | int | Device type (1: microphone, 2: speaker, 3: camera) |
| action | int | Action (1: plugged in, 2: unplugged) |
| name | const char* | Device name |
| namesize | int | Length of the device name |

### Default device change callback
```cpp
virtual void onDefDeviceChange(int type, const char* name, int namesize) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| type | int | Device type (1: microphone, 2: speaker) |
| name | const char* | Name of the new default device |
| namesize | int | Length of the device name |

### IM enabled callback
```cpp
virtual void onImEnabled(const char* uid, const char* sid) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | const char* | User ID |
| sid | const char* | Session ID |

### IM disconnected callback
```cpp
virtual void onImDisconnected(int reason, StatusCode code, const char* message, size_t message_size) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| reason | int | Disconnect reason |
| code | StatusCode | Error code |
| message | const char* | Error description |
| message_size | size_t | Length of the error description |

### IM reconnected callback
```cpp
virtual void onImReconnected() = 0;
```

### IM reconnecting callback
```cpp
virtual void onImReconnecting() = 0;
```

### IM message callback
```cpp
virtual void onImMessage2(const char* uid, const char* sid, const char* name, int name_size, const char* action, const char* content, size_t content_size) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | const char* | Sender's user ID |
| sid | const char* | Session ID |
| name | const char* | Sender's display name |
| name_size | int | Length of the display name |
| action | const char* | Message type / action |
| content | const char* | Message content |
| content_size | size_t | Length of the message content |
