---
title: "Error codes"
description: "StatusCode values returned by the Windows SRTC C++ SDK: the common 100xxx codes shared by all platforms and the Windows-specific 101xxx codes, with the enum name and meaning of each. Read when a Windows SDK call returns a non-OK status."
---

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| OK | 0 | No error |
| **Common error codes** | | |
| SystemError | 100001 | Internal system error |
| NotInitialized | 100002 | Not initialized |
| MediaNotInitialized | 100003 | The media module isn't initialized yet |
| ProtocolParsingError | 100004 | Protocol parsing error |
| Timeout | 100005 | Timed out |
| InvalidArgs | 100006 | Invalid arguments |
| Conflict | 100007 | Conflict from a repeated operation |
| SdkTokenInvalid | 100008 | The SDK token is invalid |
| NetError | 100009 | Network error |
| MediaNetError | 100010 | Media network error |
| NotFound | 100011 | Not found |
| **Windows error codes** | | |
| SDKFail | 101000 | Internal SDK error |
| DeviceFail | 101001 | Device error |
| DeviceNoFind | 101002 | Device not found |
| UserNotFound | 101003 | The user wasn't found |
| NotDevPrivate | 101004 | No permission to access the device |
| InvalidOperation | 101005 | Invalid operation |
| NotSupport | 101006 | Not yet supported by the SDK |
| DealBeQuick | 101007 | Operation performed too quickly |
| MoudelNotSupport | 101008 | Not supported by the current media streaming mode |
| BeforeSetting | 101009 | Must be set before joining |
| ChannelJoinError | 101100 | Error joining the channel |
| ChannelJoinTimeOut | 101101 | Joining the channel timed out |
| StreamJoinError | 101200 | Error joining the media stream |
| StreamJoinConflict | 101201 | Duplicate media stream join |
| VideoCapturerError | 101202 | Camera error |
| NotFindStreamTrack | 101203 | The specified stream ID doesn't exist |
| ExceedingSpecifiedQuantity | 101204 | Exceeds the allowed quantity |
