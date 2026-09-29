---
title: "InfosManager"
description: "Read-only local snapshots of the current meeting, its members, and their SRTC tracks in the SMeeting Android SDK. Read this when you need meeting info, member info, or a track to subscribe to without a network request."
---

`InfosManager` is the read-only information query entry point for the current meeting, obtained through `MeetingEngine.infosManager`. It provides meeting info, member info, and media track info; it doesn't send network requests or change meeting state.

## Usage notes

+ `MeetingEngine` always returns the same `InfosManager` facade, so your app can hold it long-term; each query reads the meeting the Engine has currently entered and doesn't keep exposing data from the previous meeting.
+ Query results come from the SDK's local cache and may briefly lag behind an operation that was just started but not yet confirmed by the server. To be notified of state changes, also listen to the corresponding `MeetingRoomEvent` or `MeetingUserEvent`.
+ When there is no entered meeting, nullable properties and object queries return `null`, list queries return an empty list, and boolean queries return `false`.
+ The audience is not part of the full member list. When the current user entered the meeting as audience, `isAudience()` returns `true`, but `getMeInfo()` may return `null`.
+ The returned models and lists are snapshots of the state at query time; don't rely on modifying these objects to update the SDK or the server's meeting state.

## Properties

### meUid

```kotlin
val meUid: String?
```

Description: The current user's UID in the SRTC channel; `null` until entering the meeting completes or after exiting the meeting.

### meetingId

```kotlin
val meetingId: String?
```

Description: The current meeting ID; `null` until entering the meeting completes or after exiting the meeting.

### whiteBoard

```kotlin
val whiteBoard: String?
```

Description: The current meeting's whiteboard URL; `null` when not in a meeting, after exiting the meeting, or when the meeting has no whiteboard URL.

## Methods

### getMeetingInfo()

```kotlin
fun getMeetingInfo(): MeetingInfo?
```

Description: Reads a snapshot of the current meeting's room configuration and its sharing, recording, and other states.

Parameters: None.

Returns: The current meeting's [MeetingInfo](/en/meeting/android/types#meetinginfo); `null` when there is no entered meeting or the room properties can't be parsed.

### getMeInfo()

```kotlin
fun getMeInfo(): MemberInfo?
```

Description: Reads the current user's full member info in the meeting, including role, device state, and member permissions.

Parameters: None.

Returns: The current user's [MemberInfo](/en/meeting/android/types#memberinfo); `null` when not in a meeting, when the current user is audience, or when the member properties can't be parsed.

### isAudience()

```kotlin
fun isAudience(): Boolean
```

Description: Determines whether the current user entered the meeting as audience.

Parameters: None.

Returns: `true` means the current user is audience; `false` when not in a meeting or when the current user is a full member.

### getMembersInfo()

```kotlin
fun getMembersInfo(): MutableList<MemberInfo>
```

Description: Reads the current meeting's full member list, including the current user if they entered as a full member, excluding the audience.

Parameters: None.

Returns: A snapshot list of member info; an empty list when not in a meeting, when the meeting has no full members, or when none of the member properties can be parsed.

### getMemberByUid(uid)

```kotlin
fun getMemberByUid(uid: String): MemberInfo?
```

Description: Reads the info of the specified full member by UID.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | The target member's UID in the current meeting |

Returns: The matching `MemberInfo`; `null` when not in a meeting or the member doesn't exist.

### isExistMember(uid)

```kotlin
fun isExistMember(uid: String): Boolean
```

Description: Determines whether the specified UID is in the current meeting's full member list.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | The target member's UID in the current meeting |

Returns: `true` when the member exists; `false` when not in a meeting or the member doesn't exist.

### getTrackInfos(uid)

```kotlin
fun getTrackInfos(uid: String): MutableList<TrackInfo>
```

Description: Reads info on all SRTC media tracks the specified user currently publishes.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | The target user's UID in the current meeting |

Returns: A snapshot list of SRTC `TrackInfo`; an empty list when not in a meeting, when the user doesn't exist, or when the user has no published tracks. For the model fields, see [SRTC Android model types](/en/rtc/android/types).

### getTrackInfoByTrackDesc(uid, trackDesc)

```kotlin
fun getTrackInfoByTrackDesc(uid: String, trackDesc: String): TrackInfo?
```

Description: Reads one SRTC media track by user UID and track description.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | The target user's UID in the current meeting |
| `trackDesc` | Track description, such as the string value corresponding to the high camera stream `TRACK_MAIN`, the mic `TRACK_AUDIO`, or the sharing stream `TRACK_SHARE` |

Returns: The matching `TrackInfo`; `null` when not in a meeting or there is no matching track. For the track description definitions, see [SRTC Android enums](/en/rtc/android/enums).

### getTrackInfoByTrackId(uid, trackId)

```kotlin
fun getTrackInfoByTrackId(uid: String, trackId: String): TrackInfo?
```

Description: Reads one media track by user UID and SRTC track ID.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | The target user's UID in the current meeting |
| `trackId` | The unique ID SRTC assigned to the target track |

Returns: The matching `TrackInfo`; `null` when not in a meeting or there is no matching track.
