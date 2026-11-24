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
    /** You were forced to exit the meeting (removed, replaced by another login, heartbeat timeout, meeting ended, etc.); data is DisconnectEventData. The SDK clears its meeting state once the callback returns, so you can call enterRoom again directly (since v0.3.3) */
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
    /** Meeting transcription (captions) turned on or off; data is RoomAsrStateChangeEventData (since 0.3.6) */
    static readonly ROOM_ASR_STATE_CHANGED = 'room_asr_state_changed';
    /** Transcription result (caption text); data is AsrResultEventData (since 0.3.6) */
    static readonly ASR_RESULT = 'asr_result';
    /** Translated caption (live translation); data is AsrTranslationEventData (since 0.3.6) */
    static readonly ASR_TRANSLATION = 'asr_translation';
    /** Meeting minutes finished or failed; data is AiSummaryReadyEventData (since 0.3.6) */
    static readonly AI_SUMMARY_READY = 'ai_summary_ready';

    /** The host handled your raise-hand request; data is AdminConfirmHandupEventData */
    static readonly ADMIN_CONFIRM_HANDUP = 'admin_confirm_handup';
    /** The host asks you to unmute your mic; data is AdminRequestOpenMicEventData */
    static readonly ADMIN_REQUEST_OPEN_MIC = 'admin_request_open_mic';
    /** The host asks you to turn on your camera; data is AdminRequestOpenCameraEventData */
    static readonly ADMIN_REQUEST_OPEN_CAMERA = 'admin_request_open_camera';
    /** The host asks you to share your screen; data is AdminRequestOpenShareEventData (op_uid = the requesting host).
     *  To accept, call requestShare(shareType, preset, audioPreset, container, true, data.op_uid); to decline, just ignore it (since 0.3.7) */
    static readonly ADMIN_REQUEST_OPEN_SHARE = 'admin_request_open_share';

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

### Data for transcription and minutes events (since 0.3.6)

Transcription works in two passes: while someone is speaking, several partial results with `is_final = false` arrive (low latency, may be inaccurate); when the sentence ends, one final result with `is_final = true` arrives (punctuated, more accurate). For captions, join the partial results per `uid` into a temporary "speaking" line and replace it with the final sentence when it arrives.

```typescript
/** ROOM_ASR_STATE_CHANGED: meeting transcription (captions) turned on or off */
export interface RoomAsrStateChangeEventData {
    /** Whether it is on */
    enabled: boolean;
    /** Error description when turning on failed */
    err_desc: string;
}

/** ASR_RESULT: transcription result (caption text) */
export interface AsrResultEventData {
    /** Speaker user id */
    uid: string;
    /** Speaker nickname */
    name: string;
    /** Text: a partial result when not final, the full sentence when final */
    text: string;
    /** Whether this is the final sentence */
    is_final: boolean;
    /** Raw recognition mode, e.g. 2pass-online / 2pass-offline */
    mode: string;
}

/** ASR_TRANSLATION: translated caption (live translation), only for final sentences; arrives after the matching ASR_RESULT */
export interface AsrTranslationEventData {
    /** Transcription session id */
    session_id: string;
    /** Sentence id */
    sentence_id: string;
    /** Speaker user id */
    uid: string;
    /** Speaker nickname */
    name: string;
    /** Original text */
    text: string;
    /** Translated text */
    trans_text: string;
    /** Translation language, e.g. en / zh */
    lang: string;
}

/** AI_SUMMARY_READY: meeting minutes finished or failed; get the content with aiSummary() */
export interface AiSummaryReadyEventData {
    /** Transcription session id */
    session_id: string;
    /** Minutes status: 2 done, 3 failed */
    status: number;
}
```

### Data for the host share request event (since 0.3.7)

```typescript
/** ADMIN_REQUEST_OPEN_SHARE: the host asks you to share your screen */
export interface AdminRequestOpenShareEventData {
    /** User id of the requesting host (may be an empty string when sent by the server); pass it back as adminUid of requestShare to accept */
    op_uid?: string;
}
```

## Out-of-meeting message events

After enabling out-of-meeting messages with `smeeting.enableIm()`, listen for them via `smeeting.onNotifyImEvent`:

```typescript
smeeting.onNotifyImEvent = (evt: ImEvent) => {
  switch (evt.type) {
    case CommonImEventType.CALL_CALLING:
      // someone is calling you into a meeting
      break;
    case CommonImEventType.IM_CUSTOM_MSG: {
      // your own business message; branch on action
      const data = evt.data as ImCustomMsgEventData;
      console.log(data.action, data.content, data.uid);
      break;
    }
  }
};
```

CommonImEventType and the corresponding `data`:

```typescript
    /** Auto-reconnect started; no data */
    static readonly RECONNECTING = 'reconnecting';
    /** Reconnected; no data */
    static readonly RECONNECTED = 'reconnected';
    /** Your IM connection was forcibly closed; data is ImDisconnectEventData */
    static readonly DISCONNECTED = 'disconnected';

    /** Incoming call; data is ImCallCallingEventData */
    static readonly CALL_CALLING = 'call_calling';
    /** Meeting reminder; data is ImMeetingRemindEventData */
    static readonly MEETING_REMIND = 'meeting_remind';
    /** Moved out of the waiting room; data is ImAdminMoveOutWaitingRoomEventData */
    static readonly ADMIN_MOVE_OUT_WAITING_ROOM = 'admin_move_out_waiting_room';
    /** A breakout group asks for help; data is ImUserHelpSubMeetingEventData */
    static readonly USER_HELP_SUB_MEETING = 'user_help_sub_meeting';
    /** Custom business message (action is not one of the built-in types above); data is ImCustomMsgEventData (since v0.3.2) */
    static readonly IM_CUSTOM_MSG = 'im_custom_msg';
```

Custom messages are sent with the server API [`im/send-msg`](/en/rtc/server-api/im#send-an-im-message). Choose your own `action` values (avoid the built-in names above); `content` is passed through unchanged:

```typescript
interface ImCustomMsgEventData {
    /** Message type: the action given when sending */
    action: string;
    /** Message body: the content given when sending */
    content: any;
    /** Sender's session ID */
    sid: string;
    /** Sender's user ID */
    uid: string;
    /** Sender's name */
    name: string;
}
```
