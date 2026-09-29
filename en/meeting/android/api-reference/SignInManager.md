---
title: "SignInManager"
description: "In-meeting sign-in manager for the SMeeting Android SDK: create and end sign-in activities, sign in as a member, count sign-ins, query records, and export them as a stream. Read this when building sign-in features."
---

`SignInManager` is obtained through `MeetingEngine.signInManager`, and all operations are bound to the Engine's current single meeting.

## Usage notes

+ This property is a stable facade that you can keep before the meeting; when you are not in a meeting, all asynchronous methods return `MeetingErrorCode.SESSION_NOT_ACTIVE`.

+ Result callbacks stay on the network thread they come from and don't switch to the main thread automatically.
+ `exportSignInDetail()` returns a one-shot `MeetingDownload`, which you must close when you finish reading it or give up.

## Methods

### listSignInActivities(callback)

```kotlin
fun listSignInActivities(
    callback: MeetingValueResultCallback<SignInListBean>
)
```

Description: Gets the current meeting's list of sign-in activities and the server's current time.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | Result callback that returns `SignInListBean` on success. |

Returns: None (the asynchronous result is delivered through the callback).

### createSignInActivity(dur, desc, callback)

```kotlin
fun createSignInActivity(
    dur: Int,
    desc: String,
    callback: MeetingResultCallback
)
```

Description: The host creates a round of sign-in.

Parameters:

| Parameter | Description |
| --- | --- |
| `dur` | Sign-in duration in minutes; `0` means no time limit. |
| `desc` | Sign-in description. |
| `callback` | Creation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### countSignInMembers(epoch, callback)

```kotlin
fun countSignInMembers(
    epoch: Int,
    callback: MeetingValueResultCallback<SignInCountBean>
)
```

Description: Counts how many members actually signed in for the specified sign-in round.

Parameters:

| Parameter | Description |
| --- | --- |
| `epoch` | Sign-in round. |
| `callback` | Result callback that returns `SignInCountBean` on success. |

Returns: None (the asynchronous result is delivered through the callback).

### finishSignInActivity(callback)

```kotlin
fun finishSignInActivity(callback: MeetingResultCallback)
```

Description: Ends the sign-in activity currently in progress.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | End result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### getSignInDetail(epoch, callback)

```kotlin
fun getSignInDetail(
    epoch: Int,
    callback: MeetingValueResultCallback<List<SignInRecordBean>>
)
```

Description: Queries the member records for the specified sign-in round.

Parameters:

| Parameter | Description |
| --- | --- |
| `epoch` | Sign-in round. |
| `callback` | Result callback that returns the list of sign-in records on success. |

Returns: None (the asynchronous result is delivered through the callback).

### signIn(callback)

```kotlin
fun signIn(callback: MeetingResultCallback)
```

Description: The current member signs in to the sign-in activity in progress.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | Sign-in result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### exportSignInDetail(epoch, callback)

```kotlin
fun exportSignInDetail(
    epoch: Int,
    callback: MeetingValueResultCallback<MeetingDownload>
)
```

Description: Exports the data stream for the specified sign-in round or for all rounds.

Parameters:

| Parameter | Description |
| --- | --- |
| `epoch` | Sign-in round; `-1` means all rounds. |
| `callback` | Result callback that returns a one-shot `MeetingDownload` on success. |

Returns: None (the asynchronous result is delivered through the callback). The caller should close the download stream with `use { ... }` or an explicit `close()`.
