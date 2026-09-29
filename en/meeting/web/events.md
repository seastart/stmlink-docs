---
title: "Events"
description: "Every room event the SMeeting Web SDK delivers through onNotifyRoomEvent: the RoomEvent structure, each CommonRoomEventType and RoomEventType value, when it fires, and which data type it carries."
---

You can listen to every event through `smeeting.onNotifyRoomEvent`

```typescript
// Handle callback events
smeeting.onNotifyRoomEvent = (evt: RoomEvent) => {
  console.log('Received room event', evt);
  switch (evt.type) {
      // ...
  }
})
```

RoomEvent is defined as follows:

```typescript
/** Room event notification */
declare class RoomEvent {
    /** Event type */
    type: CommonRoomEventType;
    /** Data carried by the event */
    data?: any;
}
```

CommonRoomEventType and the corresponding `data` are defined as follows:

```typescript
    /** Automatic reconnection after a disconnect has started, no data */
    static readonly RECONNECTING = 'reconnecting';
    /** Reconnected; fires after reconnecting successfully following a disconnect, no data */
    static readonly RECONNECTED = 'reconnected';
    /** You were forced to exit the meeting; data is DisconnectEventData */
    static readonly DISCONNECTED = 'disconnected';

    /** Another user entered the meeting; data is UserInfo */
    static readonly USER_ENTER = 'user_enter';
    /** Another user exited the meeting; data is UserExitEventData */
    static readonly USER_EXIT = 'user_exit';
    /** A user's camera state changed (changed by yourself/others, or by the host); data is UserCameraStateChangeEventData */
    static readonly USER_CAMREA_STATE_CHANGED = "user_camera_state_changed";
    /** A user's mic state changed (changed by yourself/others, or by the host); data is UserMicStateChangeEventData */
    static readonly USER_MIC_STATE_CHANGED = "user_mic_state_changed";
    /** A user's display name changed (changed by yourself/others, or by the host); data is UserNameChangeEventData */
    static readonly USER_NAME_CHANGED = "user_name_changed";
    /** A user's role changed; data is UserRoleChangeEventData */
    static readonly USER_ROLE_CHANGED = 'user_role_changed';
    /** A user's chat-disabled state changed; data is UserChatDisabledChangeEventData */
    static readonly USER_CHAT_DISABLED_CHANGED = 'user_chat_disabled_changed';
    /** User raise-hand events (received only by the host and co-hosts); data is UserHandupEventData */
    static readonly USER_HANDUP = 'user_handup';

    /** The room's camera-disabled state changed; data is RoomCameraStateChangeEventData */
    static readonly ROOM_CAMREA_STATE_CHANGED = 'room_camera_state_changed';
    /** The room's mic-disabled state changed; data is RoomMicStateChangeEventData */
    static readonly ROOM_MIC_STATE_CHANGED = 'room_mic_state_changed';
    /** The room's chat-disabled state changed; data is RoomChatDisabledChangeEventData */
    static readonly ROOM_CHAT_DISABLED_CHANGED = 'room_chat_disabled_changed';
    /** The room's screenshot-disabled state changed; data is RoomScreenshotDisabledChangeEventData */
    static readonly ROOM_SCREENSHOT_DISABLED_CHANGED = 'room_screenshot_disabled_changed';
    /** The room's watermark-disabled state changed; data is RoomWatermarkDisabledChangeEventData */
    static readonly ROOM_WATERMARK_DISABLED_CHANGED = 'room_watermark_disabled_changed';
    /** The room's locked state changed; data is RoomLockedChangeEventData */
    static readonly ROOM_LOCKED_CHANGED = 'room_locked_changed';
    /** Sharing started in the room; data is RoomShareStartEventData */
    static readonly ROOM_SHARE_START = 'room_share_start';
    /** Sharing stopped in the room; data is RoomShareStopEventData */
    static readonly ROOM_SHARE_STOP = 'room_share_stop';
    /** Room chat message; data is RoomChatMsgEventData */
    static readonly ROOM_CHAT_MSG = 'room_chat_msg';
    /** Room custom message; data is RoomCustomMsgEventData */
    static readonly ROOM_CUSTOM_MSG = 'room_custom_msg';
    /** Room MCU task; data is RoomMcuTaskEventData */
    static readonly ROOM_MCU_TASK = 'room_mcu_task';
    /** Failed to enter the room; data is RoomJoinFailedEventData */
    static readonly ROOM_JOIN_FAILED = 'room_join_failed';

    /** The host handled your raise-hand request; data is AdminConfirmHandupEventData */
    static readonly ADMIN_CONFIRM_HANDUP = 'admin_confirm_handup';
    /** The host asks you to unmute your mic; data is AdminRequestOpenMicEventData */
    static readonly ADMIN_REQUEST_OPEN_MIC = 'admin_request_open_mic';
    /** The host asks you to turn on your camera; data is AdminRequestOpenCameraEventData */
    static readonly ADMIN_REQUEST_OPEN_CAMERA = 'admin_request_open_camera';

```

RoomEventType and the corresponding `data` are defined as follows:

```typescript
/** Room event types */
export class RoomEventType extends CommonRoomEventType {
     /** Device plugged in; data is MediaDeviceInfo */
     static readonly DEVICE_ADD = 'device_add';
     /** Device unplugged; data is MediaDeviceInfo */
     static readonly DEVICE_REMOVE = 'device_remove';
     /** Track stopped; data is BaseTrack */
     static readonly TRACK_ENDED = 'track_ended';
     /** Track has no data */
     static readonly TRACK_MUTED = 'track_muted';
     /** Track data resumed */
     static readonly TRACK_UNMUTED = 'track_unmuted';
}

```
