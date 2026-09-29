---
title: "Whiteboard sharing"
description: "How to open a whiteboard in a meeting: embed the page URL from getWhiteBoard() in an iframe, broadcast the sharing status with requestShare(ShareType.WhiteBoard), and restore the whiteboard for members who enter mid-meeting."
---

The whiteboard in a meeting is an **embedded H5 page** (`iframe`). Stroke sync goes through the whiteboard's own connection and produces no media streams. On top of that, the meeting layer does one more thing: **it manages the "who is sharing the whiteboard right now" status for you**, so you don't have to broadcast it yourself as you would at the SRTC layer.

<Note>
The whiteboard page's own capabilities (URL parameters, hiding menus, desktop annotation mode, when it's destroyed) are exactly the same as at the SRTC layer; see [SRTC · Whiteboard](/en/rtc/whiteboard). This page only covers how usage differs at the meeting layer.
</Note>

---

### Get the whiteboard URL

You can read it once you've entered the meeting. The SDK has already appended the authorization code, so embed it directly:

```typescript
await smeeting.enterRoom(/* ... */);

const url = smeeting.getWhiteBoard();
if (url) {
  const iframe = document.createElement("iframe");
  iframe.src = url;
  iframe.style.cssText = "width:100%;height:100%;border:0";
  boardContainer.appendChild(iframe);
}
```

Whiteboards map one-to-one to meetings—everyone in the same meeting opens the same board. The URL becomes invalid after you exit the meeting.

---

### Start and stop sharing

Whiteboard sharing **only broadcasts a status; it doesn't capture any video**:

```typescript
import { ShareType } from "@seastart/smeeting-web-sdk";

// Start: broadcast "I'm sharing the whiteboard" in the meeting
await smeeting.requestShare(ShareType.WhiteBoard);

// Stop
await smeeting.stopShare();
```

Only one member in a meeting can share at a time, and screen sharing and the whiteboard are mutually exclusive. When the host has turned on "sharing disabled for the room", a call from a regular member throws an error.

---

### Respond to someone else's whiteboard sharing

When someone else opens the whiteboard, you receive a room event; use it to show the whiteboard:

```typescript
smeeting.onNotifyRoomEvent = (evt: RoomEvent) => {
  switch (evt.type) {
    case CommonRoomEventType.ROOM_SHARE_START:
      if (evt.data.share_type === ShareType.WhiteBoard) {
        showWhiteBoard(smeeting.getWhiteBoard());
      }
      break;
    case CommonRoomEventType.ROOM_SHARE_STOP:
      hideWhiteBoard();
      break;
  }
};
```

**Members who enter mid-meeting don't receive this event**, so check once yourself—the meeting info carries the current sharing status:

```typescript
const info = smeeting.getRoomInfo();
if (info?.share_state === ShareType.WhiteBoard) {
  // Someone in the meeting is already sharing the whiteboard, so show it on entry
  showWhiteBoard(smeeting.getWhiteBoard());
}
```

`share_state` values: `0` no sharing, `1` screen sharing, `2` whiteboard; the sharer is `share_uid`.

---

### Related

+ [SRTC · Whiteboard](/en/rtc/whiteboard)—whiteboard page URL parameters, embedding in native apps, lifecycle, and destruction
+ [Events](/en/meeting/web/events)—full definitions of the sharing-related events
+ [SMeeting](/en/meeting/web/api-reference/SMeeting)—method signatures
