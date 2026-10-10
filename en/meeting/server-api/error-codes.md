---
title: "Error codes"
description: "Values of the code field in server API responses"
---

{/* The error code list on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the meeting-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

A `code` of `0` in the response body means success. Any other value means failure, and `msg` holds a human-readable error message.
**Check `code`**, not the `msg` text—messages may change between versions, codes don't.

## Business error codes

| Code | Name | Description |
| --- | --- | --- |
| `2040` | CodeTokenChanged | This user has logged in elsewhere |
| `2041` | HeaderMissingAppId | Missing app_id in request headers |
| `2042` | HeaderInvalidAppId | Invalid app_id in request headers |
| `2043` | HeaderInvalidSignature | Invalid signature in request headers |
| `2044` | HeaderInvalidTimestamp | Device time is inaccurate. Correct the time and try again |
| `2045` | HeaderInvalidMeetSid | Invalid meet_sid in request headers |
| `2046` | HeaderMissingNonce | Missing nonce in request headers |
| `2047` | HeaderMissingUserId | Missing user_id in request headers |
| `2050` | MakeTokenFailed | Failed to generate token |
| `2051` | Unauthorized | Not authorized |
| `2052` | AuthorizationExpired | Authorization expired |
| `2053` | InvalidCallback | Invalid callback configuration |
| `2100` | MeetingError | Internal meeting error |
| `2101` | MeetingNotFound | Meeting does not exist |
| `2102` | MeetingNotStart | Meeting has not started |
| `2103` | MeetingEnded | Meeting has ended |
| `2104` | MeetingAlreadyShare | Someone is already sharing in the meeting |
| `2105` | MeetingNotSharing | No one is sharing in the meeting |
| `2106` | MeetingLocked | Meeting is locked |
| `2107` | MeetingKickout | Removed from the meeting; cannot enter again |
| `2108` | MemberInOther | Already in another meeting |
| `2109` | MemberInMeeting | Already in this meeting |
| `2110` | MemberNotInMeeting | Not in this meeting |
| `2111` | TargetNotInMeeting | Target is not in this meeting |
| `2112` | MicNotAllow | Not allowed to turn on the microphone |
| `2113` | CameraNotAllow | Not allowed to turn on the camera |
| `2114` | ChatNotAllow | Chat not allowed |
| `2115` | PasswordNotCorrect | Incorrect password |
| `2116` | MemberNotOnList | This meeting is for invitees only. Contact the host |
| `2117` | ShareNotAllow | Sharing not allowed |
| `2118` | EnterWaitingRoom | Could not enter the meeting; placed in the waiting room |
| `2120` | EnterBeforeHost | Cannot enter the meeting before the host |
| `2131` | CastCodeInvalid | Cast code is invalid or has expired |
| `2132` | CastToSelf | Cannot cast to your own device |

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
