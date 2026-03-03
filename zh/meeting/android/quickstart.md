---
title: "快速开始"
description: "Android SMeeting 会议 SDK 快速集成，10 分钟跑通基础功能"
---

### step 1：初始化 SDK 和释放 SDK 资源
#### 初始化 SDK
在调用 SDK 的任何其他函数之前，需要进行 SDK 初始化操作，这个步骤非常关键，因为只有在初始化成功后才能正常使用 MeetingSDK 的各项功能。

```kotlin
val meetingEngine: MeetingEngine = MeetingEngine.create(app);
/**
 * meetToken为sdk授权token，通过授权接口获取
 * options为流媒体参数，如无特殊需要，无需设置
 **/ 
engine?.initSdk(meetToken, options, object : MeetingResultCallback {
    override fun onFail(code: Int, errorMsg: String?, showMsg: String?) {
        // 会议组件初始化失败
    }

    override fun onSuccess() {
        // 会议组件初始化成功
    }
})
```kotlin

#### 释放 SDK
```kotlin
engine?.release()
```

### step 2：创建会议
可以创建即时会议和预约会议两种，参数说明详见 [MeetingEngine](https://www.yuque.com/anyconf/smeeting/nbyi00d99zh2sbig) 

#### 创建即时会议
```kotlin
engine?.createImmediateMeeting(
    title, option,
    object : Callback<Data<MeetingCreatedBean>>() {
        override fun onSuccess(data: Data<MeetingCreatedBean>) {
            // 会议创建成功
        }

        override fun onFailed(code: Int, errorMsg: String?, showMsg: String?) {
            // 会议创建失败
        }
    }
)
```html

#### 创建预约会议
```kotlin
engine?.createScheduleMeeting(title, planTime, planDur, option,
    object : Callback<Data<MeetingCreatedBean>>() {
        override fun onSuccess(data: Data<MeetingCreatedBean>) {
            // 会议创建成功
        }

        override fun onFailed(code: Int, errorMsg: String?, showMsg: String?) {
            // 会议创建失败
        }
    }
)
```

### step 3：加入和离开会议
参数说明详见 [MeetingEngine](https://www.yuque.com/anyconf/smeeting/nbyi00d99zh2sbig) 

#### 加入会议
```kotlin
engine?.enterMeeting(
    this, roomNo, null, nick!!, avatar, null,
    object : EnterMeetingCallback {
        override fun onSucceed(meetingId: String, uid: String) {
            // 加入会议成功
        }

        override fun onFail(code: Int, errorMsg: String?, showMsg: String?) {
            // 加入会议失败
        }
    }
)
```kotlin

#### 离开会议
```kotlin
engine?.exitMeeting()
```

#### 结束会议
```kotlin
engine?.adminDestroyMeeting(
    object : Callback<Data<String?>>(){
        override fun onSuccess(data: Data<String?>) {
            // 结束会议成功
        }

        override fun onFailed(code: Int, errorMsg: String?, showMsg: String?) {
            // 结束会议失败
        }
    }
)
```html

### step 4：开启和关闭摄像头
参数说明详见 [MeetingEngine](https://www.yuque.com/anyconf/smeeting/nbyi00d99zh2sbig) 

#### 开启摄像头
```kotlin
engine?.requestOpenCamera(
    null, PreOptionCamera.get_480P(),
    object : Callback<Data<String?>>(){
        override fun onSuccess(data: Data<String?>) {
            // 开启摄像头成功
        }

        override fun onFailed(code: Int, errorMsg: String?, showMsg: String?) {
            // 开启摄像头失败
        }
    }
)
```

#### 关闭摄像头
```kotlin
engine?.closeCamera()
```kotlin

#### 切换摄像头
```kotlin
engine?.switchCamera(isFrontCamera)
```

### step 5：开启和关闭麦克风
参数说明详见 [MeetingEngine](https://www.yuque.com/anyconf/smeeting/nbyi00d99zh2sbig) 

#### 开启麦克风
```kotlin
engine?.requestOpenMic(PreOptionMic.getDef(),
    object : Callback<Data<String?>>(){
        override fun onSuccess(data: Data<String?>) {
            // 开启麦克风成功
        }

        override fun onFailed(code: Int, errorMsg: String?, showMsg: String?) {
            // 开启麦克风失败
        }
    }
)
```kotlin

#### 关闭麦克风
```kotlin
engine?.closeMic()
```

### step 6：订阅和取消订阅远端用户画面
参数说明详见 [MeetingEngine](https://www.yuque.com/anyconf/smeeting/nbyi00d99zh2sbig) 

#### 订阅远端用户画面
订阅远端用户画面接口会返回 remoteVideoTrack，通过这个 remoteVideoTrack 可以设置视频渲染控件

```kotlin
val remoteVideoTrack = engine?.startPlayRemoteVideo(uid, trackDesc.value, view, event)
remoteVideoTrack?.addPlayView(view)
```kotlin

#### 取消订阅远端用户画面
```kotlin
engine?.stopPlayRemoteVideo(uid, trackDesc.value)
```

