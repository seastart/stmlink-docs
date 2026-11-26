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
    /** A user's extra screen-share stream (EXTRA_SCREEN) started or stopped; data is UserExtraScreenChangeEventData. For scenarios where several people publish EXTRA_SCREEN at once; receivers use it to subscribe or release */
    static readonly USER_EXTRA_SCREEN_CHANGED = "user_extra_screen_changed";
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
    /** The room's share-disabled state changed; data is RoomShareStateChangeEventData */
    static readonly ROOM_SHARE_STATE_CHANGED = 'room_share_state_changed';
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
    /** Simultaneous interpretation on/off state changed; data is RoomInterpStateChangeEventData (since 0.3.9) */
    static readonly ROOM_INTERP_STATE_CHANGED = 'room_interp_state_changed';
    /** A member's interpretation language ("my language") changed; data is UserInterpLangChangeEventData (since 0.3.9) */
    static readonly USER_INTERP_LANG_CHANGED = 'user_interp_lang_changed';

    /** In-meeting sign-in; data is SignInActivityEventData */
    static readonly SIGN_IN_ACTIVITY = 'sign_in_activity';
    /** In-meeting sign-in ended (manually or automatically); data is SignInFinishEventData */
    static readonly SIGN_IN_FINISH = 'sign_in_finish';
    /** A user entered the waiting room; data is UserEnterWaitingRoomEventData */
    static readonly USER_ENTER_WAITING_ROOM = 'user_enter_waiting_room';
    /** A user left the waiting room; data is UserExitWaitingRoomEventData */
    static readonly USER_EXIT_WAITING_ROOM = 'user_exit_waiting_room';
    /** The waiting-room-disabled state changed; data is AdminUpdateWaitingRoomDisabledEventData */
    static readonly ADMIN_UPDATE_WAITING_ROOM_DISABLED = 'admin_update_waiting_room_disabled';
    /** The host moved you into the waiting room (sent privately to that member); no data */
    static readonly ADMIN_MOVE_IN_WAITING_ROOM = 'admin_move_in_waiting_room';
    /** The host started breakout groups; data is AdminStartSubMeetingEventData */
    static readonly ADMIN_START_SUB_MEETING = 'admin_start_sub_meeting';
    /** The host ended breakout groups; data is AdminStopSubMeetingEventData */
    static readonly ADMIN_STOP_SUB_MEETING = 'admin_stop_sub_meeting';
    /** A user was moved between groups, or between a group and the main meeting; data is AdminMoveSubMeetingUserEventData */
    static readonly ADMIN_MOVE_SUB_MEETING_USER = 'admin_move_sub_meeting_user';
    /** In-meeting roll call; data is RollCallNamedEventData */
    static readonly ROLL_CALL_NAMED = 'roll_call_named';

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
     /** The active speaker list changed; data is ActiveSpeakersEventData (full snapshot, sorted by level descending). Only fired by the SeaStart SFU engine */
     static readonly ACTIVE_SPEAKERS_CHANGED = 'active_speakers_changed';
}

```

## Data of room events

The `data` types of the `CommonRoomEventType` / `RoomEventType` events, grouped by purpose. For `UserInfo`, `ShareType`, `CameraState`, `MicState`, `Role`, `HandupType`, `UserHandupStep`, `ChatMsgType`, `McuTaskType`, `McuTaskStatus`, `DisconnectReason` and similar types, see [Data types](/en/meeting/web/types).

### Disconnecting and leaving

```typescript
/** DISCONNECTED: you were forced out of the meeting */
export interface DisconnectEventData {
    /** Reason for leaving */
    reason: DisconnectReason;
    /** Error */
    error?: any;
}

/** USER_EXIT: another user left the meeting */
export interface UserExitEventData {
    /** User id */
    uid: string;
    /** Reason for leaving */
    reason: DisconnectReason;
}

/** ROOM_JOIN_FAILED: joining the room failed */
export interface RoomJoinFailedEventData {
    /** User id */
    uid: string;
    /** User nickname */
    name: string;
    /** Error description */
    err_desc: string;
    /** Failure type */
    failed_type: string;
}
```

### Member state

```typescript
/** USER_CAMREA_STATE_CHANGED: a user's camera state changed */
export interface UserCameraStateChangeEventData {
    /** User */
    uid: string;
    /** Camera state */
    camera_state: CameraState;
    /** Whether a host made the change */
    by_admin: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** USER_EXTRA_SCREEN_CHANGED: a user's extra screen-share stream (EXTRA_SCREEN) started or stopped */
export interface UserExtraScreenChangeEventData {
    /** User */
    uid: string;
    /** Whether the stream is being published */
    active: boolean;
}

/** USER_MIC_STATE_CHANGED: a user's mic state changed */
export interface UserMicStateChangeEventData {
    /** User */
    uid: string;
    /** Mic state */
    mic_state: MicState;
    /** Whether a host made the change */
    by_admin: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** USER_NAME_CHANGED: a user's nickname changed */
export interface UserNameChangeEventData {
    /** User */
    uid: string;
    /** Nickname */
    nickname: string;
    /** Whether a host made the change */
    by_admin: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** USER_ROLE_CHANGED: a user's role changed */
export interface UserRoleChangeEventData {
    /** User */
    uid: string;
    /** Role */
    role: Role;
    /** Operator user id */
    op_uid?: string;
}

/** USER_CHAT_DISABLED_CHANGED: a user's chat-disabled state changed */
export interface UserChatDisabledChangeEventData {
    /** User */
    uid: string;
    /** Whether chat is disabled */
    chat_disabled: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** USER_HANDUP: raise-hand events (hosts only) */
export interface UserHandupEventData {
    /** User */
    uid: string;
    /** Raise-hand type */
    type: HandupType;
    /** Raise-hand step */
    step: UserHandupStep;
}

/** ACTIVE_SPEAKERS_CHANGED: the active speaker list changed (full snapshot). Only fired by the SeaStart SFU engine */
export interface ActiveSpeakersEventData {
    /** Server timestamp (unix ms), for ordering and diagnostics */
    ts: number;
    /** Users currently speaking, sorted by level from high to low */
    speakers: ActiveSpeakerInfo[];
}

export interface ActiveSpeakerInfo {
    /** User id */
    uid: string;
    /** Audio track id; tells tracks apart when one user publishes several audio tracks */
    trackId: string;
    /** Current volume, normalized linear 0–1 (0 is silence, 1 is 0 dBov), quantized to steps of 1/8, so it can drive a level meter directly; for dB use 20 * Math.log10(level) */
    level: number;
}
```

### Meeting settings

```typescript
/** ROOM_CAMREA_STATE_CHANGED: the room's camera-disabled state changed */
export interface RoomCameraStateChangeEventData {
    /** Whether video is disabled in the room */
    camera_disabled: boolean;
    /** Whether members are prevented from turning their video back on */
    self_unmute_camera_disabled: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** ROOM_MIC_STATE_CHANGED: the room's mic-disabled state changed */
export interface RoomMicStateChangeEventData {
    /** Whether mics are disabled in the room */
    mic_disabled: boolean;
    /** Whether members are prevented from unmuting themselves */
    self_unmute_mic_disabled: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** ROOM_SHARE_STATE_CHANGED: the room's share-disabled state changed */
export interface RoomShareStateChangeEventData {
    /** Whether sharing is disabled in the room */
    share_disabled: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** ROOM_CHAT_DISABLED_CHANGED: the room's chat-disabled state changed */
export interface RoomChatDisabledChangeEventData {
    /** Whether chat is disabled in the room */
    chat_disabled: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** ROOM_SCREENSHOT_DISABLED_CHANGED: the room's screenshot-disabled state changed */
export interface RoomScreenshotDisabledChangeEventData {
    /** Whether screenshots are disabled in the room */
    screenshot_disabled: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** ROOM_WATERMARK_DISABLED_CHANGED: the room's watermark-disabled state changed */
export interface RoomWatermarkDisabledChangeEventData {
    /** Whether the watermark is disabled in the room */
    watermark_disabled: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** ROOM_LOCKED_CHANGED: the room's locked state changed */
export interface RoomLockedChangeEventData {
    /** Whether the room is locked */
    locked: boolean;
    /** Operator user id */
    op_uid?: string;
}
```

### Sharing, messages and recording

```typescript
/** ROOM_SHARE_START: sharing started in the room */
export interface RoomShareStartEventData {
    /** Sharing user */
    uid: string;
    /** Share type */
    share_type: ShareType;
}

/** ROOM_SHARE_STOP: sharing stopped in the room */
export interface RoomShareStopEventData {
    /** User who was sharing */
    uid: string;
    /** Share type that was in use */
    share_type: ShareType;
    /** Whether a host stopped it */
    by_admin: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** ROOM_CHAT_MSG: room chat message */
export interface RoomChatMsgEventData {
    /** Message type */
    msg_type: ChatMsgType;
    /** Message content */
    msg: string;
    /** Sender */
    uid?: string;
    /** Whether it is a private message */
    private: boolean;
}

/** ROOM_CUSTOM_MSG: room custom message */
export interface RoomCustomMsgEventData {
    /** Message content */
    msg: string;
    /** Sender */
    uid?: string;
    /** Whether it is a private message */
    private: boolean;
}

/** ROOM_MCU_TASK: room MCU task message */
export interface RoomMcuTaskEventData {
    /** Task type */
    task_type: McuTaskType;
    /** Task status */
    task_status: McuTaskStatus;
    /** Error description */
    err_desc: string;
}
```

### Transcription and minutes (since 0.3.6)

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
    /** Translation language, e.g. en / zh. When interpretation is on, each sentence arrives once per language of the members in the meeting; for captions, take the one whose lang equals my language */
    lang: string;
    /**
     * URL of the synthesized speech for the translation (absolute URL, already built by the SDK), present only when simultaneous interpretation is on and synthesis succeeded; expires after 10 minutes (since 0.3.9).
     * The interpretation player built into the Web SDK plays it automatically by its rules, so you usually don't need to handle it
     */
    audio_url: string;
}

/** AI_SUMMARY_READY: meeting minutes finished or failed; get the content with aiSummary() */
export interface AiSummaryReadyEventData {
    /** Transcription session id */
    session_id: string;
    /** Minutes status: 2 done, 3 failed */
    status: number;
}
```

### Simultaneous interpretation (since 0.3.9)

For how to use interpretation and the playback rules of the built-in player, see [SMeeting · Simultaneous interpretation](/en/meeting/web/api-reference/SMeeting#simultaneous-interpretation). For the interpretation state when entering, check `isInterpEnabled()` and `getRoomInfo()`, then update incrementally with the two events below; after reconnecting, the SDK re-emits them if anything changed.

```typescript
/** ROOM_INTERP_STATE_CHANGED: simultaneous interpretation on/off state changed */
export interface RoomInterpStateChangeEventData {
    /** Whether it's on */
    enabled: boolean;
    /** Volume the speaker's original voice is lowered to while interpretation audio plays (0–1, 0 is muted) */
    duck_volume: number;
    /** Reason for a passive shutdown (such as transcription having stopped) */
    err_desc: string;
}

/** USER_INTERP_LANG_CHANGED: a member's interpretation language ("my language") changed */
export interface UserInterpLangChangeEventData {
    /** Member user id */
    uid: string;
    /** The effective language, such as zh / en (the meeting's default language when the member resets to default) */
    lang: string;
}
```

### Sign-in, waiting room, breakout groups and roll call

```typescript
/** SIGN_IN_ACTIVITY: in-meeting sign-in */
export interface SignInActivityEventData {
    /** Host user id */
    host_id: string;
    /** Host nickname */
    host_name: string;
    /** Round */
    epoch: number;
    /** Start time */
    begin_at: number;
    /** Planned duration */
    dur: number;
    /** End time */
    end_at: number;
    /** Sign-in description */
    desc: string;
}

/** SIGN_IN_FINISH: in-meeting sign-in ended (manually or automatically) */
export interface SignInFinishEventData {
    /** Host user id */
    host_id: string;
    /** Host nickname */
    host_name: string;
    /** Round */
    epoch: number;
}

/** USER_ENTER_WAITING_ROOM: a user entered the waiting room */
export interface UserEnterWaitingRoomEventData {
    /** User id */
    uid: string;
    /** User nickname */
    name: string;
    /** User avatar */
    avatar: string;
}

/** USER_EXIT_WAITING_ROOM: a user left the waiting room */
export interface UserExitWaitingRoomEventData {
    /** User id */
    uid: string;
    /** User nickname */
    name: string;
    /** User avatar */
    avatar: string;
}

/** ADMIN_UPDATE_WAITING_ROOM_DISABLED: the waiting-room-disabled state changed */
export interface AdminUpdateWaitingRoomDisabledEventData {
    /** Whether the waiting room is disabled */
    waiting_room_disabled: boolean;
    /** Operator user id */
    op_uid?: string;
}

/** ADMIN_START_SUB_MEETING: the host started breakout groups */
export interface AdminStartSubMeetingEventData {
    /** Meeting id */
    meeting_id: string;
    /** Meeting title */
    title: string;
    /** User id list */
    uids: string[];
}

/** ADMIN_STOP_SUB_MEETING: the host ended breakout groups */
export interface AdminStopSubMeetingEventData {
    /** Parent meeting id */
    parent: string;
}

/** ADMIN_MOVE_SUB_MEETING_USER: a user was moved between groups, or between a group and the main meeting */
export interface AdminMoveSubMeetingUserEventData {
    /** Current meeting ID */
    from_meeting_id: string;
    /** Current meeting title */
    from_meeting_title: string;
    /** Target meeting ID */
    to_meeting_id: string;
    /** Target meeting title */
    to_meeting_title: string;
}

/** ROLL_CALL_NAMED: in-meeting roll call */
export interface RollCallNamedEventData {
    /** Roll call id */
    id: string;
    /** User ID */
    sid: string;
    /** Current time */
    time: number;
}
```

### Host requests

```typescript
/** ADMIN_CONFIRM_HANDUP: the host handled your raise-hand request */
export interface AdminConfirmHandupEventData {
    /** Raise-hand type */
    type: HandupType;
    /** Whether it was approved */
    approve: boolean;
    /** Operator user id */
    op_uid?: string;
    /** Target user id */
    target_id: string;
}

/** ADMIN_REQUEST_OPEN_MIC: the host asks you to unmute your mic */
export interface AdminRequestOpenMicEventData {
    /** Operator user id */
    op_uid?: string;
}

/** ADMIN_REQUEST_OPEN_CAMERA: the host asks you to turn on your camera */
export interface AdminRequestOpenCameraEventData {
    /** Operator user id */
    op_uid?: string;
}

/** ADMIN_REQUEST_OPEN_SHARE: the host asks you to share your screen (since 0.3.7) */
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

`data` of the other out-of-meeting message events:

```typescript
/** Common fields (sender) of out-of-meeting message event data */
export interface ImBaseEventData {
    /** Session ID */
    sid: string;
    /** User ID */
    uid: string;
    /** User name */
    name: string;
    /** User avatar */
    avatar?: string;
}

/** DISCONNECTED: your out-of-meeting message connection was forcibly closed */
export interface ImDisconnectEventData {
    /** Disconnect reason */
    reason: ImDisconnectReason;
    /** Error */
    error?: any;
}

export enum ImDisconnectReason {
    /** Error */
    Error = -1,
    /** Left on your own */
    Self = 1,
    /** Kicked */
    Kicked = 2,
    /** Heartbeat timeout */
    Timeout = 4,
}

/** CALL_CALLING: you are being called into a meeting */
export interface ImCallCallingEventData extends ImBaseEventData {
    content: {
        /** Room number */
        room_no: string;
        /** Meeting ID */
        meeting_id: string;
        /** Meeting title */
        title: string;
        /** Whether joining is forced */
        force_join: boolean;
    };
}

/** MEETING_REMIND: meeting reminder */
export interface ImMeetingRemindEventData extends ImBaseEventData {
    content: {
        /** Room number */
        room_no: string;
        /** Meeting ID */
        meeting_id: string;
        /** Meeting title */
        title: string;
        /** Creator */
        creator_name: string;
        /** Planned duration */
        plan_dur: number;
        /** Planned start time */
        plan_time: number;
        /** Whether joining is forced */
        force_join: boolean;
    };
}

/** ADMIN_MOVE_OUT_WAITING_ROOM: you were moved out of the waiting room (sent privately to that member) */
export interface ImAdminMoveOutWaitingRoomEventData extends ImBaseEventData {
    content: {
        /** Main meeting ID */
        parent: string;
        /** Breakout meeting ID */
        meeting_id: string;
        /** Group name */
        title: string;
    };
}

/** USER_HELP_SUB_MEETING: a breakout group asks for help (sent privately to the host / co-hosts) */
export interface ImUserHelpSubMeetingEventData extends ImBaseEventData {
    content: {
        /** Main meeting ID */
        parent: string;
        /** Breakout meeting ID */
        meeting_id: string;
        /** Group name */
        title: string;
    };
}
```
