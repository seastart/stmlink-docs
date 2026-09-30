---
title: "Error codes"
description: "The SEAError enum of the iOS SMeeting SDK (Objective-C): every case with its value and meaning, covering server API errors passed through (1xxx, 2xxx, 10xxx) and SDK system, common, network, and client errors (100xxx, 103xxx). Read when handling or troubleshooting an error code."
---

### SEAError
Error codes

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| SEAErrorOK | `0` | No error |
| **API errors** | | |
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
| **System errors** | | |
| SEAErrorSystemError | `100001` | Internal system error |
| SEAErrorNotInitialized | `100002` | Not initialized |
| SEAErrorMediaNotInitialized | `100003` | The media module isn't initialized yet |
| SEAErrorProtocolParsingError | `100004` | Protocol parsing error |
| **Common errors** | | |
| SEAErrorTimeout | `100005` | Timed out |
| SEAErrorInvalidArgs | `100006` | Invalid arguments |
| SEAErrorConflict | `100007` | Conflict from a repeated operation |
| SEAErrorSdkTokenInvalid | `100008` | The SDK token is invalid |
| **Network errors** | | |
| SEAErrorNetError | `100009` | Network error |
| SEAErrorMediaNetError | `100010` | Media network error |
| SEAErrorNotFound | `100011` | Target doesn't exist |
| **Client errors** | | |
| SEAErrorDeviceNoAuthorized | `103001` | No permission to access the device |
| SEAErrorNotJoinedChannel | `103002` | Not in the channel |
| SEAErrorForbidden | `103003` | Operation not allowed |
| SEAErrorStreamNotFound | `103004` | Stream doesn't exist |
| SEAErrorNotAuthorized | `103005` | No permission to perform the operation |


