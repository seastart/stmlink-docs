---
title: "Error codes"
description: "The SEAError enum of the iOS SMeeting SDK (Objective-C): since 2.2.0, meeting-layer client errors are 203xxx (same codes and meanings as the Swift SDK), RTC layer errors are passed through as 103xxx, and backend business codes (1000–99999) are passed through as is. Read when handling or troubleshooting an error code or upgrading from 2.1.x."
---

`SEAError` is the `code` of the failure callback `SEAFailedBlock`, and also the type of `errCode` in callbacks such as `onError` and `onImDisconnected`. `0` (`SEAErrorOK`) means success; anything non-zero is an error.

<Note>
The values on this page apply since **2.2.0**. Since 2.2.0, the meeting layer's own errors use the `203` range, and the RTC layer error codes passed through were renumbered along with `RTCEngineKit 3.2.0`. For the mapping between old codes (2.1.0 and earlier) and new ones, see the [Changelog](/en/meeting/ios/changelog). For the numbering rules shared by all platforms, see [Error code format and unified table](/en/meeting/error-codes).
</Note>

### Value rules

| Category | Values | Source | `message` |
| --- | --- | --- | --- |
| Backend business codes | `1000`–`99999` | Returned by the backend and passed through by the SDK as is | The `msg` returned by the backend; language follows `language` |
| Meeting-layer client codes | `203xxx` | Produced by MeetingKit itself: iOS prefix `203` + low 3 digits of the unified table, with the same codes and meanings as the Swift SDK | English |
| RTC layer codes passed through | `103xxx` | Produced by RTCEngineKit, with the same values as `RTCEngineError`; the meeting layer doesn't rewrap them | English, including the RTC code |

+ **Branch on `code` only**. Don't branch on `message`, and don't show `message` directly to end users; map `code` to your own user-facing prompts
+ The meeting layer and the RTC layer have two separate low-3-digit tables: `203004` (unauthorized) and `103004` (invalid token) mean different things, so compare the full 6-digit code
+ The pre-call network check `networkCheck:onItem:completion:` (since `2.3.0`) passes through RTC layer codes: `SEAErrorConflict` (`103005`) when a check is already running, `SEAErrorInvalidArgs` (`103031`) for invalid parameters or an undecodable token, and `SEAErrorUserCancelled` (`103026`) when cancelled. Only when not logged in and no parameters are passed does it return the meeting-layer `SEAErrorMeetingNotLoggedIn` (`203001`)
+ `language` only affects the `Accept-Language` sent with meeting-layer requests to the backend, i.e. the language of backend business code messages; see [MeetingKit.language](/en/meeting/ios/api-reference/MeetingKit#language). Since `2.2.1`, it also applies to the RTC layer, so the `message` of backend business codes passed through from the RTC layer is also the server-side message

### SEAError

#### Meeting-layer client error codes

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| SEAErrorOK | `0` | No error |
| SEAErrorMeetingNotLoggedIn | `203001` | Not logged in to the meeting SDK. Since `2.3.0`, returned by the pre-call network check `networkCheck:onItem:completion:` when not logged in and no parameters are passed |
| SEAErrorMeetingTokenExpired | `203002` | Token has expired (not produced on this platform yet; kept for consistency with other platforms) |
| SEAErrorMeetingNotInMeeting | `203003` | Not in a meeting (not produced on this platform yet; kept for consistency with other platforms) |
| SEAErrorMeetingUnauthorized | `203004` | Unauthorized, e.g. the API can only be called by the host or a co-host |
| SEAErrorNotAuthorized | `203004` | Deprecated; same-value alias of `SEAErrorMeetingUnauthorized` (old value `103005`) |
| SEAErrorMeetingTokenInvalid | `203005` | Invalid token format; the meeting token can't be decoded |
| SEAErrorMeetingAlreadyInMeeting | `203006` | Already in a meeting; exit first (the room instance is joining or has joined) |
| SEAErrorMeetingNetworkError | `203007` | Network error: can't connect, non-200 HTTP, etc.; the HTTP status is in `message` |
| SEAErrorMeetingDeviceError | `203008` | Device error (reserved; capture and permission failures pass through RTC layer codes) |
| SEAErrorMeetingInternalError | `203009` | SDK internal error, e.g. failed to write a downloaded file to disk |
| SEAErrorMeetingUserNotFound | `203010` | The user isn't in the meeting (not produced on this platform yet; kept for consistency with other platforms) |
| SEAErrorMeetingInvalidState | `203011` | The current state doesn't allow the operation, e.g. the room instance has been destroyed |
| SEAErrorMeetingInvalidArgument | `203012` | Invalid argument (not produced on this platform yet; kept for consistency with other platforms) |
| SEAErrorMeetingRemoteTrackUnavailable | `203209` | Remote track unavailable: the user is in the meeting but doesn't have the video stream to subscribe to |
| SEAErrorMeetingRequestTimeout | `203353` | Request timed out |
| SEAErrorMeetingRequestCancelled | `203354` | Request was cancelled |
| SEAErrorMeetingEmptyResponseBody | `203355` | Empty response body |
| SEAErrorMeetingResponseParseFailed | `203356` | Failed to parse the response: not a JSON object, missing the `code` field, or unexpected structure |

<Warning>
`SEAErrorNotAuthorized` and `SEAErrorMediaNotInitialized` are deprecated and have the same values as `SEAErrorMeetingUnauthorized` and `SEAErrorNotInitialized` respectively. Writing a pair of same-value constants in a `switch` causes a duplicate `case` error; referencing a deprecated constant produces a deprecation warning, and projects with `-Werror` enabled fail to compile, so use the new names.
</Warning>

#### RTC layer error codes passed through

Values are the same as `RTCEngineError` in `RTCEngineKit`; see [SRTC iOS error codes](/en/rtc/ios/error-codes). Values in parentheses are the old values in 2.1.0 and earlier.

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| SEAErrorNotJoinedChannel | `103001` | Not in a channel (old `103002`) |
| SEAErrorStreamNotFound | `103003` | Stream doesn't exist (old `103004`) |
| SEAErrorSdkTokenInvalid | `103004` | Invalid token (old `100008`) |
| SEAErrorConflict | `103005` | Conflict from a repeated operation (old `100007`) |
| SEAErrorNetError | `103006` | RTC layer network error, including non-200 HTTP (old `100009`). Meeting-layer network failures no longer use this code; see `203007` |
| SEAErrorTimeout | `103007` | Timed out (old `100005`) |
| SEAErrorProtocolParsingError | `103011` | Protocol parsing error (old `100004`) |
| SEAErrorMediaNetError | `103012` | Media network error (old `100010`) |
| SEAErrorNotInitialized | `103024` | Not initialized / the current state doesn't allow it (old `100002`) |
| SEAErrorMediaNotInitialized | `103024` | Deprecated; same-value alias of `SEAErrorNotInitialized` (old `100003`) |
| SEAErrorSystemError | `103025` | Internal system error (old `100001`) |
| SEAErrorUserCancelled | `103026` | Cancelled by the user (old `100012`) |
| SEAErrorVirtualBackgroundAlreadyInstalled | `103027` | Virtual background is already installed (returned as `100007` in old versions) |
| SEAErrorVirtualBackgroundNotInstalled | `103028` | Virtual background isn't installed (returned as `100007` in old versions) |
| SEAErrorVirtualBackgroundModelNotFound | `103029` | Virtual background model doesn't exist or is invalid (returned as `100011` in old versions) |
| SEAErrorVirtualBackgroundSessionFailed | `103030` | Failed to create the virtual background inference session (returned as `100001` in old versions) |
| SEAErrorInvalidArgs | `103031` | Invalid arguments (old `100006`) |
| SEAErrorDeviceNoAuthorized | `103042` | No device access permission, used when camera and microphone can't be told apart (old `103001`); no longer returned, `103231` / `103251` are reported instead |
| SEAErrorForbidden | `103043` | Operation not allowed (old `103003`) |
| SEAErrorSwitchAudioRouteFail | `103044` | Failed to switch the audio route (old `103005`) |
| SEAErrorNotFound | `103204` | The user isn't in the channel (old `100011`) |
| SEAErrorCameraNoAuthorized | `103231` | No camera permission (returned as `103001` in old versions) |
| SEAErrorMicNoAuthorized | `103251` | No microphone permission (returned as `103001` in old versions) |

#### Backend business codes

Returned by the backend and passed through by the SDK as is; `message` is the `msg` returned by the backend, in the language set by `language`. For the complete list and meanings, see [Server API error codes](/en/meeting/server-api/error-codes).

<Note>
Since 2.2.0, the SDK no longer produces codes such as `SEAErrorApiTokenDisabled` (`10042`) or `SEAErrorApiRepeatFound` (`10003`) to indicate local errors; these constants appear only when the backend actually returns those codes.
</Note>

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| SEAErrorRtcApiHeaderNotAppId | `1001` | Missing APPID in request headers |
| SEAErrorRtcApiHeaderInvalidAppId | `1002` | Invalid APPID in request headers |
| SEAErrorRtcApiHeaderInvalidSignature | `1003` | Invalid signature in request headers |
| SEAErrorRtcApiHeaderInvalidTimestamp | `1004` | Invalid timestamp in request headers |
| SEAErrorApiHeaderInvalidSession | `1005` | Invalid session ID in request headers |
| SEAErrorRtcApiHeaderNotNonce | `1006` | Missing nonce in request headers |
| SEAErrorRtcApiInvalidApplication | `1011` | Invalid app |
| SEAErrorRtcApiInvalidServiceGroup | `1012` | Invalid server group |
| SEAErrorRtcApiInvalidService | `1013` | Invalid service |
| SEAErrorRtcApiInvalidScene | `1014` | Invalid application scenario |
| SEAErrorRtcApiInvalidConfigure | `1015` | Invalid callback configuration |
| SEAErrorRtcApiChannelTokenFailed | `1020` | Failed to generate the channel token |
| SEAErrorRtcApiChannelTokenOccupied | `1021` | Channel token has already been used |
| SEAErrorRtcApiSessionNotFound | `1022` | Session is not in the channel |
| SEAErrorRtcApiMemberNotFound | `1023` | Member is not in the channel |
| SEAErrorRtcApiChannelNotOpen | `1024` | Channel is not open |
| SEAErrorRtcApiChannelOpen | `1025` | Channel is already open |
| SEAErrorRtcApiImTokenFailed | `1030` | Failed to generate the IM token |
| SEAErrorRtcApiImTokenOccupied | `1031` | IM token has already been used |
| SEAErrorRtcApiSessionOffline | `1032` | Session is not online |
| SEAErrorRtcApiInsufficientConcurrency | `1033` | Concurrency limit reached |
| SEAErrorRtcApiNotFoundMcuTask | `1040` | MCU task not found |
| SEAErrorRtcApiRecordTaskUnfinished | `1041` | Recording task has not ended yet |
| SEAErrorRtcApiRecordTaskNotFile | `1042` | Recording task has not produced a recording file yet |
| SEAErrorRtcApiMcuLayoutFailed | `1043` | MCU layout data error |
| SEAErrorRtcApiMcuTaskStoped | `1044` | MCU task has already stopped |
| SEAErrorMeetingApiRemoteLogin | `2040` | This user has logged in elsewhere |
| SEAErrorMeetingApiHeaderNotAppId | `2041` | Missing APPID in request headers |
| SEAErrorMeetingApiHeaderInvalidAppId | `2042` | Invalid APPID in request headers |
| SEAErrorMeetingApiHeaderInvalidSignature | `2043` | Invalid signature in request headers |
| SEAErrorMeetingApiHeaderInvalidTimestamp | `2044` | Invalid timestamp in request headers |
| SEAErrorMeetingApiHeaderInvalidSession | `2045` | Invalid meeting session ID in request headers |
| SEAErrorMeetingApiHeaderNotNonce | `2046` | Missing nonce in request headers |
| SEAErrorMeetingApiHeaderNotUserId | `2047` | Missing user ID in request headers |
| SEAErrorMeetingApiTokenFailed | `2050` | Failed to generate token |
| SEAErrorMeetingApiNotAuthorized | `2051` | Not authorized |
| SEAErrorMeetingApiTokenExpired | `2052` | Authorization expired |
| SEAErrorMeetingApiFailed | `2100` | Internal meeting error |
| SEAErrorMeetingApiNotFound | `2101` | Meeting does not exist |
| SEAErrorMeetingApiNotStarted | `2102` | Meeting has not started |
| SEAErrorMeetingApiFinished | `2103` | Meeting has ended |
| SEAErrorMeetingApiSomeoneSharing | `2104` | Someone is already sharing in the meeting |
| SEAErrorMeetingApiNotSharing | `2105` | No one is sharing in the meeting |
| SEAErrorMeetingApiLocked | `2106` | Meeting is locked |
| SEAErrorMeetingApiKickedout | `2107` | Removed from the meeting; cannot enter again |
| SEAErrorMeetingApiAtOtherMeeting | `2108` | Already in another meeting |
| SEAErrorMeetingApiAlreadyExisted | `2109` | Already in this meeting |
| SEAErrorMeetingApiNotMeeting | `2110` | Not in this meeting |
| SEAErrorMeetingApiMemberNotFound | `2111` | Target is not in this meeting |
| SEAErrorMeetingApiMicDisabled | `2112` | Not allowed to turn on the microphone |
| SEAErrorMeetingApiCameraDisabled | `2113` | Not allowed to turn on the camera |
| SEAErrorMeetingApiChatDisabled | `2114` | Chat not allowed |
| SEAErrorMeetingApiPasswordFailed | `2115` | Incorrect password |
| SEAErrorMeetingApiByInviteOnly | `2116` | This meeting is for invitees only. Contact the host |
| SEAErrorMeetingApiWaitingRoomEnable | `2118` | The meeting has the waiting room enabled; you can enter only after the host or a co-host admits you |
| SEAErrorMeetingApiEnterBeforeHostDisabled | `2120` | Entering the meeting before the host is not allowed |
| SEAErrorApiFailed | `10000` | Unclassified general error |
| SEAErrorApiDatabaseFailed | `10001` | Database error |
| SEAErrorApiRecordNotFound | `10002` | Record not found |
| SEAErrorApiRepeatFound | `10003` | Record already exists |
| SEAErrorApiNotAuthorized | `10040` | Permission denied |
| SEAErrorApiNotInitialized | `10041` | Not logged in |
| SEAErrorApiTokenDisabled | `10042` | Invalid token |
| SEAErrorApiTokenExpired | `10043` | Token has expired |
| SEAErrorApiNetworkFailed | `10051` | Network error |
| SEAErrorApiNetworkTimeout | `10055` | Request timed out |
| SEAErrorApiInvalidParameter | `10070` | Invalid request parameters |
