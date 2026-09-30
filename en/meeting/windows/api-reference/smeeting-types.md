---
title: "Enums and data structures"
description: "Enums and structs of the SMeeting Windows SDK C++ API: StatusCode values, DisconnectReason, chat, raise-hand, camera, microphone, sharing, role, device, and network-level enums, plus SMeetingCreateMeetingModel fields with defaults, attachments, resources, and CustomPublishTrack."
---

## Enums

### StatusCode

| Value | Name | Description |
| --- | --- | --- |
| 0 | OK | Success |
| 100001 | SystemError | System error |
| 100002 | NotInitialized | Not initialized |
| 100003 | MediaNotInitialized | Media not initialized |
| 100004 | ProtocolParsingError | Protocol parsing error |
| 100005 | Timeout | Timeout |
| 100006 | InvalidArgs | Invalid arguments |
| 100007 | Conflict | Conflict |
| 100008 | SdkTokenInvalid | Invalid token |
| 100009 | NetError | Network error |
| 100010 | MediaNetError | Media network error |
| 100011 | NotFound | Not found |
| 101000 | SDKFail | SDK failure |
| 101001 | DeviceFail | Device failure |
| 101002 | DeviceNoFind | Device not found |
| 101003 | UserNotFound | User not found |
| 101004 | NotDevPrivate | No device permission |
| 101005 | InvalidOperation | Invalid operation |
| 101006 | NotSupport | Not supported |
| 101007 | DealBeQuick | Operation performed too quickly |
| 101008 | MoudelNotSupport | Mode not supported |
| 101009 | BeforeSetting | Must be set first |
| 101100 | ChannelJoinError | Channel join error |
| 101101 | ChannelJoinTimeOut | Channel join timeout |
| 101200 | StreamJoinError | Stream join error |
| 101201 | StreamJoinConflict | Stream join conflict |
| 101202 | VideoCapturerError | Video capturer error |
| 101203 | NotFindStreamTrack | Stream track not found |
| 101204 | ExceedingSpecifiedQuantity | Exceeds the specified quantity |
| 201000 | SDKMeetingFail | Internal SDK error |
| 201001 | MeetingStatusReject | Rejected by room permissions |
| 201002 | MeetingHostFail | Host error or no host set |

### DisconnectReason

| Value | Name | Description |
| --- | --- | --- |
| -1 | Error | Error |
| 1 | Self | Exited voluntarily |
| 2 | Kicked | Removed |
| 3 | Replace | Replaced by another session with the same uid |
| 4 | Timeout | Exited due to timeout |
| 5 | Destroy | Destroyed |

### ChatMsgType

| Value | Name | Description |
| --- | --- | --- |
| 1 | Text | Text |
| 2 | File | File |
| 3 | Pic | Image |
| 4 | Sound | Audio |

### HandupType

| Value | Name | Description |
| --- | --- | --- |
| 1 | Mic | Raise hand for the microphone |
| 2 | Camera | Raise hand for the camera |
| 3 | Chat | Raise hand for chat |

### UserHandupStep

| Value | Name | Description |
| --- | --- | --- |
| 1 | Request | Request |
| 2 | Cancel | Cancel |
| 3 | ConfirmOpen | Approve turning on |
| 4 | RejectOpen | Decline turning on |

### CameraState

| Value | Name | Description |
| --- | --- | --- |
| 1 | On | On |
| 2 | Off | Off |

### MicState

| Value | Name | Description |
| --- | --- | --- |
| 1 | On | On |
| 2 | Off | Off |

### ShareType

| Value | Name | Description |
| --- | --- | --- |
| 0 | Normal | Normal |
| 1 | Screen | Screen |
| 2 | WhiteBoard | Whiteboard |

### Role

| Value | Name | Description |
| --- | --- | --- |
| 0 | Member | Regular member |
| 1 | Host | Host |
| 2 | CoHost | Co-host |

### DeviceType

| Value | Name | Description |
| --- | --- | --- |
| 1 | Mic | Microphone |
| 2 | Speaker | Speaker |
| 3 | Camera | Camera |

### DeviceStatus

| Value | Name | Description |
| --- | --- | --- |
| 2 | NoFail | Normal |
| 1 | Fail | Abnormal |

### StreamNetLevel

| Value | Name | Description |
| --- | --- | --- |
| 0 | Good | Good |
| -1 | NotGood | Fair |
| -2 | Terrible | Poor |
| -3 | Catastrophic | Catastrophic |

---

## Data structures

### SMeetingCreateMeetingModel

Meeting creation model:

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| room_no | std::string | Room number | - |
| title | std::string | Meeting title | - |
| content | std::string | Meeting content | - |
| password | std::string | Password | - |
| meeting_type | int | Meeting type (1: instant, 2: scheduled) | 1 |
| meeting_mode | int | Meeting mode (1: normal, 2: composite, 3: voice, 4: training, 5: sub-meeting) | 1 |
| plan_time | long long | Scheduled time (Unix timestamp) | 0 |
| plan_dur | int | Scheduled duration | 0 |
| conferee | `std::vector<std::string>` | List of invitees | - |
| co_host | `std::vector<std::string>` | List of co-hosts | - |
| maximum | int | Maximum number of people | 0 |
| end_type | int | End type (0: extend, 1: force end) | 1 |
| entry_mute_policy | int | Mute-on-entry policy (1: forced, 2: off, 3: mute when more than 6 people) | 3 |
| watermark_disabled | bool | Whether the watermark is disabled | true |
| screenshot_disabled | bool | Whether screenshots are disabled | false |
| chat_disabled | bool | Whether chat is disabled | false |
| auto_record | bool | Whether to record automatically | true |
| attend_type | int | Entry restriction type (1: unrestricted, 3: invitees only) | 1 |
| waiting_room_disabled | bool | Whether the waiting room is disabled | true |
| enter_before_host_disabled | bool | Whether entering before the host is prevented | false |
| parent | std::string | Parent meeting ID | - |
| extend_info | std::string | Extended info | - |

### SMeetingMeetingAttachments

Meeting attachment:

| Field | Type | Description |
| --- | --- | --- |
| name | std::string | Name |
| key | std::string | Key |

### SMeetingResourcesModel

Resource model:

| Field | Type | Description |
| --- | --- | --- |
| meeting_id | std::string | Meeting ID |
| parent_id | std::string | Parent resource ID |
| res_type | std::string | Resource type |
| res_key | std::string | Resource key |
| res_name | std::string | Resource name |

### CustomPublishTrack

Custom publish track:

| Field | Type | Description |
| --- | --- | --- |
| desc | std::string | Description |
| width | int | Width |
| height | int | Height |
| fps | int | Frame rate |
| bitrate | int | Bitrate |
| encode | int | Encoding |
