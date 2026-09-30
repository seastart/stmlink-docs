---
title: "C++ API reference"
description: "Entry point to the SMeeting Windows SDK C++ API: how the engine-level ISMeetingEngine and meeting-level ISMeetingChannel split the work, their event and setting interfaces, the vtable recompilation rule, and an index of every API module page."
---

This page is the complete reference for the SMeeting Windows SDK C++ API. All APIs are defined in the `SMeeting.h` header file.

Starting with `1.0.0-alpha.5`, `ISMeetingEngine` is split into two sets of interfaces (**engine level / meeting level**):

| Interface | Scope | Description |
| --- | --- | --- |
| [ISMeetingEngine](/en/meeting/windows/api-reference/smeeting-engine) | Engine level | Login, meeting management HTTP APIs, channel object lifecycle, device enumeration, IM, and the resource drive. |
| [ISMeetingChannel](/en/meeting/windows/api-reference/smeeting-channel) | Meeting level | One object per meeting, covering entering the meeting, in-meeting operations, and media objects. |
| [ISMeetingEngineEvent](/en/meeting/windows/api-reference/smeeting-events) | Engine-level callbacks | Device, network probe, and IM events. |
| [ISMeetingChannelEvent](/en/meeting/windows/api-reference/smeeting-events) | Meeting-level callbacks | In-meeting events such as connection state, members, room, and media streams. |
| [ISMeetingSetting](/en/meeting/windows/api-reference/smeeting-settings) | Engine-level settings | Only `sdk_log_path` / `enable_stream_log`. |
| [ISMeetingChannelSetting](/en/meeting/windows/api-reference/smeeting-settings) | Meeting-level settings | Streaming mode, statistics interval, display name and avatar for entering the meeting, and more. |

**Important**: `ISMeetingEngine` / `ISMeetingChannel` and the `IMEET*` family are all pure virtual interfaces, and any signature change alters the vtable. After upgrading the SDK you must recompile your project; replacing only the DLLs is not enough.

---

## API module index

- [ISMeetingEngine engine API](/en/meeting/windows/api-reference/smeeting-engine)—initialization, login and logout, meeting management, channel object management, device enumeration, IM, and the resource drive.
- [ISMeetingChannel meeting API](/en/meeting/windows/api-reference/smeeting-channel)—entering / exiting the meeting, room info, user operations, and the waiting room.
- [Host management APIs](/en/meeting/windows/api-reference/smeeting-admin)—room controls, member controls, and permission management.
- [Sub-meeting APIs](/en/meeting/windows/api-reference/smeeting-submeeting)—create / start / stop sub-meetings and move members between them.
- [MCU APIs](/en/meeting/windows/api-reference/smeeting-mcu)—composite video and recording configuration.
- [Sign-in APIs](/en/meeting/windows/api-reference/smeeting-signin)—create sign-in activities, get statistics, and export them.
- [Media track APIs](/en/meeting/windows/api-reference/smeeting-media)—local / remote audio and video, screen sharing, custom tracks, and local recording.
- [Event callbacks](/en/meeting/windows/api-reference/smeeting-events)—`ISMeetingEngineEvent` and `ISMeetingChannelEvent`.
- [Settings](/en/meeting/windows/api-reference/smeeting-settings)—`ISMeetingSetting` and `ISMeetingChannelSetting`.
- [Enums and data structures](/en/meeting/windows/api-reference/smeeting-types)—`StatusCode`, `Role`, `SMeetingCreateMeetingModel`, and more.
