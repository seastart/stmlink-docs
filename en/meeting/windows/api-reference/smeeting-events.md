---
title: "Event callbacks"
description: "All callbacks of the SMeeting Windows SDK: engine-level ISMeetingEngineEvent (devices, network probe, IM) and meeting-level ISMeetingChannelEvent (connection, members, room state, host controls, media quality, sign-in, recording, sub-meetings), with parameters and when to bind them."
---

Callbacks are split into **engine-level** `ISMeetingEngineEvent` and **meeting-level** `ISMeetingChannelEvent`.

- Engine-level callbacks are bound through `ISMeetingEngine::setEventHandler()`.
- Meeting-level callbacks are bound through `ISMeetingChannel::setEventHandler()` and **must be set before `enter()`**; otherwise you miss events raised while entering the meeting.

Meeting-level callbacks no longer take `roomno` as the first parameter. If one handler serves multiple channel objects, use `channel->getChannelId()` or `channel->getRoom()` to tell them apart.

---

## ISMeetingEngineEvent (engine level)

### Device events

| Event | Parameters | Description |
| --- | --- | --- |
| onDeviceChange | DeviceType tp, bool isadd, std::string name | A device was plugged in or unplugged |
| onDefDeviceChange | DeviceType tp, std::string name | The default device changed |

### Network probe events

| Event | Parameters | Description |
| --- | --- | --- |
| onStreamProbeResult | int step, std::string result | Network probe result |

### IM events

| Event | Parameters | Description |
| --- | --- | --- |
| onImEnabled | std::string uid, std::string sid | IM is enabled |
| onImDisconnected | int reason, StatusCode code, std::string message | IM disconnected |
| onImReconnected | - | IM reconnected |
| onImReconnecting | - | IM is reconnecting |
| onImCallMessage | std::string uid, std::string name, std::string content | Call message |
| onMeetingStartMessage | std::string content | Meeting start message |

---

## ISMeetingChannelEvent (meeting level)

### Connection state events

| Event | Parameters | Description |
| --- | --- | --- |
| onDisconnected | DisconnectReason, StatusCode, std::string | Disconnected |
| onReconnected | - | Reconnected |
| onReconnecting | - | Reconnecting |

### Member events

| Event | Parameters | Description |
| --- | --- | --- |
| onUserEnter | std::string userdata | A member entered |
| onUserExit | std::string userdata, DisconnectReason reason | A member exited |
| onUserCameraStateChanged | std::string uid, CameraState newstate, bool by_admin, std::string op_uid | A member's camera state changed |
| onUserAudioStateChanged | std::string uid, MicState newstate, bool by_admin, std::string op_uid | A member's audio state changed |
| onUserNameChanged | std::string uid, std::string newname, bool by_admin, std::string op_uid | A member's name changed |
| onUserRoleChanged | std::string uid, Role newrole, bool by_admin, std::string op_uid | A member's role changed |
| onUserChatDisabledChanged | std::string uid, bool newstate, bool by_admin, std::string op_uid | A member's chat permission changed |
| onUserHandup | std::string uid, HandupType tp, UserHandupStep step | A member raised a hand |

### Room events

| Event | Parameters | Description |
| --- | --- | --- |
| onRoomCameraStateChanged | std::string uid, bool self_unmute_camera_disabled, bool camera_disabled | Room camera state |
| onRoomMicStateChanged | std::string uid, bool self_unmute_mic_disabled, bool mic_disabled | Room microphone state |
| onRoomChatDisabledChanged | std::string uid, bool newstatus | Room chat state |
| onRoomScreenshotDisabledChanged | std::string uid, bool newstatus | Room screenshot state |
| onRoomWaterMarkDisabledChanged | std::string uid, bool newstatus | Room watermark state |
| onRoomLockChanged | bool lock | Room lock state |
| onRoomShareStart | std::string uid, ShareType st | Sharing started |
| onRoomShareStop | std::string uid, ShareType st, bool by_admin, std::string op_uid | Sharing stopped |
| onRoomChatMessage | std::string uid, bool pri, ChatMsgType msg_type, std::string msg | Chat message |
| onRoomCustomMessage | std::string uid, bool pri, std::string msg | Custom message |
| onRoomMcuTaskChange | int task_type, int task_status | MCU task changed |
| onRoomShareStateChange | bool share_state | Sharing state changed |
| onRoomWaitRoomStateChange | bool new_st | Waiting room state changed |

### Host control events

| Event | Parameters | Description |
| --- | --- | --- |
| onAdminRequestOpenMic | std::string uid | The host asks you to turn on the microphone |
| onAdminRequestOpenCamera | std::string uid | The host asks you to turn on the camera |
| onAdminUpdateName | std::string uid, std::string name | The host changed your name |
| onAdminConfirmHandup | std::string uid, int code, bool approve | The host responded to your raised hand |
| onAdminMoveInWaitRoom | - | Moved into the waiting room |
| onAdminWaitRoomEnterRoomFinish | int code, std::string msg | Finished entering the room |

### Device events

| Event | Parameters | Description |
| --- | --- | --- |
| onDeviceStatusChange | DeviceType tp, DeviceStatus status | Device status changed |
| onShareTargetNotFind | - | Sharing target not found |

### Media stream events

| Event | Parameters | Description |
| --- | --- | --- |
| onStreamUpLevel | StreamNetLevel level | Uplink network quality |
| onStreamDownLevel | std::string uid, StreamNetLevel level | Downlink network quality |
| onStreamUpStat | std::string upstat | Uplink statistics |
| onStreamDownStat | std::string downstat | Downlink statistics |
| onStreamSpeakers | std::string Speakers | List of speakers |
| onFrameTimeOut | std::string uid, std::string track_id, std::string track_desc, int loading | Frame timeout |

### Sign-in events

| Event | Parameters | Description |
| --- | --- | --- |
| onSigninActivity | std::string name, std::string desc, long long enddt | Sign-in activity |
| onSigninFinish | std::string name | Sign-in finished |
| onWaitRoomMemberEnter | std::string uid, std::string name | A member entered the waiting room |
| onWaitRoomMemberLeave | std::string uid, std::string name | A member exited the waiting room |

### Recording events

| Event | Parameters | Description |
| --- | --- | --- |
| onRecordStatusChange | std::string k, int status, std::string msg | Recording status changed |

### Sub-meeting events

| Event | Parameters | Description |
| --- | --- | --- |
| onAdminStartSubMeeting | std::string meeting_id, std::string title, std::string users | Sub-meeting started |
| onAdminStopSubMeeting | std::string parent_meeting_id | Sub-meeting stopped |
| onAdminMoveSubMeetingUser | std::string to_meeting_title, std::string to_meeting_id | Member moved to another sub-meeting |
| onUserHelpSubMeeting | std::string meeting_id, std::string title, std::string parent | Help requested |
