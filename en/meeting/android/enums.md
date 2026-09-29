---
title: "Enums"
description: "Meeting, member, device, message, sharing, recording, roll call, and external device enums of Android SMeeting, with values and meanings, plus where to find the SRTC enums Meeting uses directly. Read this when mapping enum values in events and models."
---

### AgentStatus

| Enum name | Value | Description |
| --- | --- | --- |
| Unknow | 0 | Unknown |
| Online | 1 | Online |
| Offline | 2 | Offline |

### AgentType

| Enum name | Value | Description |
| --- | --- | --- |
| SIP | 2 | SIP |
| H323 | 3 | H.323 |
| GB28181 | 4 | GB28181 |
| RTSP | 5 | RTSP stream pull |
| RTMP | 6 | RTMP stream pull |
| FILE | 7 | File playback |
| TENCENT | 8 | Tencent Meeting |
| AI | 9 | AI |

### AttendType

| Enum name | Value | Description |
| --- | --- | --- |
| ATTEND_NOT_LIMIT | 1 | No restriction (default) |
| ATTEND_BY_PWD | 2 | Enter with a password |
| ATTEND_ONLY_INVITE | 3 | Invitees only |

### ChangeReason

| Enum name | Value | Description |
| --- | --- | --- |
| ChangeReasonBySelf | 0 | Changed by the user themselves |
| ChangeReasonByAdmin | 1 | Changed by the host or a co-host |

### ChatMsgType

| Enum name | Value | Description |
| --- | --- | --- |
| UnKnown | 0 | Unknown (fallback type) |
| Text | 1 | Text message |
| File | 2 | File message |
| Picture | 3 | Image message |
| Voice | 4 | Voice message |
| Custom | 5 | Custom message |

### CloudRecordStatus

| Enum name | Value | Description |
| --- | --- | --- |
| Status_Not_Start | 0 | Not started |
| Status_Ing | 1 | In progress |
| Status_Not_End | 2 | Pending end |
| Status_Error | 3 | Ended abnormally |
| Status_Ended | 4 | Ended normally |

### CloudRecordType

| Enum name | Value | Description |
| --- | --- | --- |
| Mode_Video | 1 | Video recording mode |
| Mode_Mixture | 2 | Stream mixing mode |
| Mode_All | 3 | Combined mode |

### DeviceState

| Enum name | Value | Description |
| --- | --- | --- |
| Open | 1 | On |
| Closed | 2 | Off |

### HandUpType

| Enum name | Value | Description |
| --- | --- | --- |
| UnKnown | 0 | Unknown (fallback type) |
| OpenMic | 1 | Request to turn on audio |
| OpenCamera | 2 | Request to turn on video |
| Chat | 3 | Request to chat |
| Share | 4 | Request to share |
| Draw | 5 | Request to draw on the whiteboard |
| Other | 6 | Other request |

### LeaveMeetingReason

| Enum name | Value | Description |
| --- | --- | --- |
| Unknown | 0 | Unknown |
| KickOut | 2 | Removed from the meeting |
| BeReplaced | 3 | Replaced by the same user entering again |
| HeartbeatTimeout | 4 | Heartbeat timeout |
| ChannelDestroy | 5 | Channel destroyed |

### McuAlarmStatus

| Enum name | Value | Description |
| --- | --- | --- |
| PendingStart | 0 | Pending start |
| InProgress | 1 | In progress |
| PendingEnd | 2 | Pending end |
| AbnormalEnd | 3 | Ended abnormally |
| Finished | 4 | Ended |

### MeetingMode

| Enum name | Value | Description |
| --- | --- | --- |
| Normal | 1 | Regular meeting mode |
| Mixture | 2 | Composite meeting mode |
| Voice | 3 | Voice meeting |
| Training | 4 | Training mode |
| SubMeet | 5 | Sub-meeting |

### MeetingStatus

| Enum name | Value | Description |
| --- | --- | --- |
| STATUS_UNKNOW | -1 | Unknown |
| STATUS_PRE | 1 | Not started |
| STATUS_ING | 2 | In progress |
| STATUS_END | 3 | Ended |

### MeetingType

| Enum name | Value | Description |
| --- | --- | --- |
| Immediate | 1 | Instant meeting |
| Schedule | 2 | Scheduled meeting |

### MemberRoleType

| Enum name | Value | Description |
| --- | --- | --- |
| Normal | 0 | Regular member |
| Host | 1 | Host |
| UnionHost | 2 | Co-host |

### MuteState

| Enum name | Value | Description |
| --- | --- | --- |
| MuteState1 | 1 | Mute on entry enabled (everyone is muted by default when entering the meeting) |
| MuteState2 | 2 | Mute on entry disabled (follows the client's initial audio state) |
| MuteState3 | 3 | Mute beyond 6 people (members entering after there are more than 6 people are muted) |

### RollCallMethod

| Enum name | Value | Description |
| --- | --- | --- |
| Auto | 1 | Automatic roll call |
| Manual | 2 | Manual roll call |

### ShareType

| Enum name | Value | Description |
| --- | --- | --- |
| Normal | 0 | Normal state, no sharing |
| ScreenShare | 1 | Screen sharing |
| WhiteBoardShare | 2 | Whiteboard sharing |

### SubMeetingStatus

| Enum name | Value | Description |
| --- | --- | --- |
| STATUS_UNKNOW | -1 | Unknown |
| STATUS_PRE | 1 | Not started |
| STATUS_ING | 2 | In progress |
| STATUS_END | 3 | Ended |

### UserType

| Enum name | Value | Description |
| --- | --- | --- |
| Normal | 1 | Regular member |
| SIP | 2 | SIP device |
| H323 | 3 | H.323 device |

### CastMeetingOwner

Ownership policy for a newly created casting meeting, used by `CastStartOption.owner`.

| Enum name | Value | Description |
| --- | --- | --- |
| Self | `"self"` | Owned by the casting initiator who calls startCast |

## SRTC enums

Meeting's public APIs also directly use types from the transitive SRTC dependency, such as `DeviceType`, `LeaveReason`, `ScreenCaptureState`, `TrackDesc`, and network quality levels. These are not Meeting's own enums; see [SRTC Android enums](/en/rtc/android/enums) as the authoritative reference.
