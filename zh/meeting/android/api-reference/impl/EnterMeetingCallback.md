---
title: "EnterMeetingCallback"
description: "Android SMeeting 会议 SDK EnterMeetingCallback 接口参考"
---

说明：`EnterMeetingCallback` 是进入会议结果回调接口。

## 回调方法

### onSucceed(meetingId, uid)
```kotlin
fun onSucceed(meetingId: String, uid: String)
```
方法说明：进入会议成功回调。  
参数说明：
- `meetingId`：`String`，会议 id。
- `uid`：`String`，当前用户 uid。
返回值说明：无（`Unit`）。

### onFail(code, errorMsg, showMsg)
```kotlin
fun onFail(code: Int, errorMsg: String?, showMsg: String?)
```
方法说明：进入会议失败回调。  
参数说明：
- `code`：`Int`，错误码。
- `errorMsg`：`String?`，技术错误信息。
- `showMsg`：`String?`，面向用户的提示信息。
返回值说明：无（`Unit`）。
