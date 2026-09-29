---
title: "Channel messages"
description: "Use the Web SDK's IM channel (out-of-channel messaging) for pre-call ringing and notifications: enable it with an IM token, receive messages via onNotifyImEvent, send through your backend, and handle reconnect and disconnect. Read when you need messaging outside a channel."
---

SRTC provides an IM channel (out-of-channel messaging) for things like pre-call ringing and notifications.

### Enable
```typescript
// IM session ID
let imSid = "";
let enableIm = async () => {
    // Call your backend API to get the IM enable token
    // api.getImToken
  
    let token = "IM enable token returned by your backend";
    imSid = await srtc.enableIm(token);
}
```



### Receive IM messages
```typescript
srtc.onNotifyImEvent = (evt: ImEvent) => {
    console.log('Received IM event', evt);
    switch (evt.type) {
        case ImEventType.IM_MSG:
            // Received an IM message
            // evt.data as ImMsgData
            break;
        
    }
}
```



### Send IM messages
All IM messages must be sent through your backend API, so you can apply your own logic, such as sensitive-word filtering

```typescript
// Call your backend API to send the IM message
// api.sendImMsg
```



### Reconnecting / reconnected
When the network fluctuates, a reconnecting event fires; once reconnection succeeds, a reconnected event fires

```typescript
// Inside onNotifyImEvent
case ImEventType.RECONNECTING:
  // Reconnecting started
  break;
case ImEventType.RECONNECTED:
  // Reconnected successfully
  break;
```

### Disable / disconnect
Disconnection is either an active disable or a passive disconnect (when an unrecoverable error occurs)

```typescript
// Active disable
await srtc.disableIm();
// Refresh and clean up the UI



// Passive disconnect
// Inside onNotifyImEvent
case ImEventType.DISCONNECTED:
  let data = (evt.data as ImDisconnectEventData);
  // You can show why IM disconnected based on reason
  alert('IM disconnected reason:' + data.reason);
  // Refresh and clean up the UI
  imSid = "";
  break;
```
