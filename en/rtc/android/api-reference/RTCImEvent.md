---
title: "RTCImEvent"
description: "Android event callbacks for the IM channel (out-of-channel messaging): connection success, disconnect, reconnecting, reconnected, and incoming IM messages. Read when handling IM connection state or messages on Android."
---

## Description

`RTCImEvent` is the event callback interface for the IM channel (out-of-channel messaging).

## Interface methods

### onImConnectSucceed(uid, sid)
```kotlin
fun onImConnectSucceed(uid: String, sid: String)
```
Description: Called when the IM connection succeeds.  
Parameters:
- `uid`: `String`, the current user ID.
- `sid`: `String`, the current session ID.
Returns: None (`Unit`).

### onImDisconnected(reason, statusCode, message)
```kotlin
fun onImDisconnected(reason: LeaveReason, statusCode: Int, message: String)
```
Description: Called when the IM connection drops.  
Parameters:
- `reason`: `LeaveReason`, the disconnect reason (for the enum definition, see the `LeaveReason` docs).
- `statusCode`: `Int`, the status code.
- `message`: `String`, the status description.
Returns: None (`Unit`).

### onImReconnecting()
```kotlin
fun onImReconnecting()
```
Description: Called when IM starts reconnecting.  
Parameters: None.  
Returns: None (`Unit`).

### onImReconnected()
```kotlin
fun onImReconnected()
```
Description: Called when IM reconnects successfully.  
Parameters: None.  
Returns: None (`Unit`).

### onImMessage(uid, sid, name, action, content)
```kotlin
fun onImMessage(uid: String, sid: String, name: String, action: String, content: String)
```
Description: Called when an IM message is received.  
Parameters:
- `uid`: `String`, the sender's user ID.
- `sid`: `String`, the sender's session ID.
- `name`: `String`, the sender's name.
- `action`: `String`, the message action identifier.
- `content`: `String`, the message content.
Returns: None (`Unit`).
