---
title: "MeetingRemoteVideoEvent"
description: "接收单条远端视频、合成流或网宿视频流的接收与卡顿状态"
---

`MeetingRemoteVideoEvent` 监听单条远端视频控制轨，通过 `startPlayRemoteVideo()`、`startPlayRemoteMixture()` 或 `subscribeWsVideoStream()` 的 `event` 参数注册。可继承 `MeetingRemoteVideoSimpleEvent`。

## 特殊说明

该监听随一次订阅调用绑定，不通过 `MeetingEngine` 属性全局注册；不同远端轨道可使用不同监听实例。

## 注意事项

+ 事件保持 SRTC 实际回调线程，不切换主线程。
+ Meeting 会隐藏底层频道参数，并过滤旧会议的迟到事件。
+ 合成流的订阅成功只表示请求已提交，是否真正收到画面应结合本事件和渲染结果判断。

## 接口方法

### onReceiveStreamStatusChange(uid, trackDesc, isChoke)

```kotlin
fun onReceiveStreamStatusChange(
    uid: String,
    trackDesc: String,
    isChoke: Boolean
)
```

方法说明：远端视频流的接收或卡顿状态发生变化。

参数说明：

+ `uid`：订阅时使用的远端用户或渲染路由标识。
+ `trackDesc`：订阅时使用的轨道描述。
+ `isChoke`：`true` 表示当前接收卡顿，`false` 表示恢复正常。

返回值说明：无（`Unit`）。
