---
title: "RollCallManager"
description: "In-meeting roll call manager for the SMeeting Android SDK: start and end roll calls, call and confirm members as the host, answer as a member, and query or export details. Read this when building roll call features."
---

`RollCallManager` is obtained through `MeetingEngine.rollCallManager`, and all operations are bound to the Engine's current single meeting.

## Usage notes

+ This property is a stable facade that you can keep before the meeting; when you are not in a meeting, all asynchronous methods return `MeetingErrorCode.SESSION_NOT_ACTIVE`.
+ The `id` in the list and in the details mean different things: `RollCallBean.id` in the list is the roll call activity ID, while `RollCallUserBean.id` of a user in the details is the roll call user ID used for subsequent calls and answers.

+ When `allMember` is `false`, you must provide `members`; each member item contains a UID and a nickname.
+ Result callbacks stay on the network thread they come from; switch to the main thread before updating the UI.

## Methods

### listRollCall(page, perPage, callback)

```kotlin
fun listRollCall(
    page: Int,
    perPage: Int,
    callback: MeetingValueResultCallback<MeetingPage<RollCallBean>>
)
```

Description: Queries the current meeting's roll call activities page by page.

Parameters:

| Parameter | Description |
| --- | --- |
| `page` | Page number, starting from `1`. |
| `perPage` | Maximum number of items per page. |
| `callback` | Callback that returns the paginated roll call activities on success. |

Returns: None (the asynchronous result is delivered through the callback).

### startRollCall(method, allMember, members, callback)

```kotlin
fun startRollCall(
    method: RollCallMethod,
    allMember: Boolean,
    members: List<MemberRequestBean>?,
    callback: MeetingValueResultCallback<String>
)
```

Description: Creates and starts a round of roll call.

Parameters:

| Parameter | Description |
| --- | --- |
| `method` | Automatic or manual roll call method. |
| `allMember` | `true` calls the roll for all members; `false` calls only `members`. |
| `members` | List of specified members; required when `allMember=false`. |
| `callback` | Result callback that returns the new roll call activity ID on success. |

Returns: None (the asynchronous result is delivered through the callback).

### stopRollCall(rollCallId, callback)

```kotlin
fun stopRollCall(rollCallId: String, callback: MeetingResultCallback)
```

Description: Ends the specified roll call activity.

Parameters:

| Parameter | Description |
| --- | --- |
| `rollCallId` | Roll call activity ID. |
| `callback` | End result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### rollCallNamed(rollCallUserId, callback)

```kotlin
fun rollCallNamed(
    rollCallUserId: String,
    callback: MeetingResultCallback
)
```

Description: The host calls the specified user in the roll call details.

Parameters:

| Parameter | Description |
| --- | --- |
| `rollCallUserId` | `RollCallUserBean.id`, not the meeting member UID. |
| `callback` | Call result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminRollCallAnswer(rollCallUserId, clear, callback)

```kotlin
fun adminRollCallAnswer(
    rollCallUserId: String,
    clear: Boolean,
    callback: MeetingResultCallback
)
```

Description: The host confirms or clears the specified user's roll call answer record.

Parameters:

| Parameter | Description |
| --- | --- |
| `rollCallUserId` | `RollCallUserBean.id`. |
| `clear` | `true` clears the existing answer record; `false` confirms the answer. |
| `callback` | Operation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### detailRollCall(rollCallId, callback)

```kotlin
fun detailRollCall(
    rollCallId: String,
    callback: MeetingValueResultCallback<RollCallDetailBean>
)
```

Description: Queries the details of the specified roll call activity and the members' answer status.

Parameters:

| Parameter | Description |
| --- | --- |
| `rollCallId` | Roll call activity ID. |
| `callback` | Result callback that returns `RollCallDetailBean` on success. |

Returns: None (the asynchronous result is delivered through the callback).

### exportRollCallDetail(rollCallId, callback)

```kotlin
fun exportRollCallDetail(
    rollCallId: String,
    callback: MeetingValueResultCallback<String>
)
```

Description: Requests an export of the specified roll call activity's details.

Parameters:

| Parameter | Description |
| --- | --- |
| `rollCallId` | Roll call activity ID. |
| `callback` | Callback that returns the server's export result string on success. |

Returns: None (the asynchronous result is delivered through the callback).

### userRollCallAnswer(rollCallUserId, callback)

```kotlin
fun userRollCallAnswer(
    rollCallUserId: String,
    callback: MeetingResultCallback
)
```

Description: The current user answers the roll call.

Parameters:

| Parameter | Description |
| --- | --- |
| `rollCallUserId` | The current user's `RollCallUserBean.id` in the roll call details. |
| `callback` | Answer result callback. |

Returns: None (the asynchronous result is delivered through the callback).
