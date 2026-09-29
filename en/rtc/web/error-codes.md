---
title: "Error codes"
description: "Error codes you can get from the SRTC Web SDK: server codes (1011, 1021–1025) for invalid app, used token, and channel state, and Web client codes (106001–106003) for not in channel, expired token, and missing track. Read when handling join or publish failures."
---

### Server error codes

| Error name | Code | Description |
| --- | :---: | --- |
| `InvalidApp` | `1011` | Invalid app |
| `ChannelTokenUsed` | `1021` | Channel token has already been used |
| `SidNotInChannel` | `1022` | Session is not in the channel |
| `UserNotInChannel` | `1023` | User is not in the channel |
| `ChannelNotOpen` | `1024` | Channel is not open |
| `ChannelOpened` | `1025` | Channel is already open |

---

### Client error codes

| Error name | Code | Description |
| --- | :---: | --- |
| `NotInChannel` | `106001` | Not currently in a channel |
| `TokenExpired` | `106002` | The channel token has expired |
| `TrackNotExists` | `106003` | The track doesn't exist |
