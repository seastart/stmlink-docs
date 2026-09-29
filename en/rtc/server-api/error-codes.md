---
title: "Error codes"
description: "Values of the code field in server API responses"
---

{/* The error code list on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the rtc-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

A `code` of `0` in the response body means success. Any other value means failure, and `msg` holds a human-readable error message.
**Check `code`**, not the `msg` text—messages may change between versions, codes don't.

## Business error codes

| Code | Name | Description |
| --- | --- | --- |
| `1001` | HeaderMissingAppId | Missing app_id in request headers |
| `1002` | HeaderInvalidAppId | Invalid app_id in request headers |
| `1003` | HeaderInvalidSignature | Invalid signature in request headers |
| `1004` | HeaderInvalidTimestamp | Invalid timestamp in request headers |
| `1005` | HeaderInvalidSid | Invalid sid in request headers |
| `1006` | HeaderMissingNonce | Missing nonce in request headers |
| `1011` | InvalidApp | Invalid app |
| `1012` | InvalidSrvGroup | Invalid server group |
| `1013` | InvalidServer | Invalid service |
| `1014` | InvalidScene | Invalid application scenario |
| `1015` | InvalidCallback | Invalid callback configuration |
| `1020` | GrantChannelTokenFailed | Failed to generate the channel token |
| `1021` | ChannelTokenUsed | Channel token has already been used |
| `1022` | SidNotInChannel | Session is not in the channel |
| `1023` | UserNotInChannel | User is not in the channel |
| `1024` | ChannelNotOpen | Channel is not open |
| `1025` | ChannelOpened | Channel is already open |
| `1027` | GrantWbTokenFailed | Failed to generate the whiteboard token |
| `1028` | InvalidChannelName | Invalid channel name |
| `1029` | InvalidUid | Invalid uid |
| `1030` | GrantImTokenFailed | Failed to generate the IM token |
| `1031` | ImTokenUsed | IM token has already been used |
| `1032` | SidNotFound | Session is not online |
| `1033` | ConcurrentLimit | Concurrency limit reached |
| `1034` | SfuNoAvailableNode | No media server node available |
| `1035` | SfuNodeOverloaded | Media server node is fully loaded |
| `1040` | McuTaskNotFound | MCU task not found |
| `1041` | McuRecordNotStop | Recording task has not ended yet |
| `1042` | McuRecordNoVod | Recording task has not produced a recording file yet |
| `1043` | McuLayoutDataErr | MCU layout data error |
| `1044` | McuTaskIsEnd | MCU task has already stopped |
| `1045` | McuRecordNotFound | Recording file not found |
| `1046` | McuRecordNotDone | Recording file has not finished uploading |
| `1050` | TalkrecTaskNotFound | Voice recording task not found |
| `1051` | TalkrecRecordNotFound | Voice segment not found |
| `1052` | TalkrecRecordNoVod | Voice segment has not produced an audio file yet |
| `1053` | TalkrecGatewayNotFound | No voice recording gateway available |

## Common framework error codes

Any API can return these. The most common is `10070`, returned when a parameter fails validation (required, length, character set, or value range); `msg` tells you which parameter.

| Code | Name | Description |
| --- | --- | --- |
| `10000` | CodeUnSpecial | Unspecified error |
| `10001` | CodeDatabaseException | Database error |
| `10002` | CodeDataRecordNotFound | Record not found |
| `10003` | CodeDataRecordExists | Record already exists |
| `10040` | CodeUnAuthorized | Permission denied |
| `10041` | CodeAuthFailed | Not logged in |
| `10042` | CodeTokenInvalid | Invalid token |
| `10043` | CodeTokenExpired | Token has expired |
| `10051` | CodeNetError | Network error |
| `10055` | CodeRequestTimeout | Request timed out |
| `10070` | CodeInvalidParams | Invalid request parameters |
