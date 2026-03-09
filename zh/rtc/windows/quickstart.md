---
title: "快速开始"
description: "Windows SRTC 音视频 SDK 快速集成，10 分钟跑通基础功能"
---

### 初始化SDK
```cpp
SRTC::StatusCode ret = SRTC::RTCEngine_Init(&_irtc);
if((ret |= SRTC::StatusCode::OK) || !_irtc)
{
    return false;
}
```



### 设置消息回调
```cpp
_irtc->setEventHandler(this);
```

更多消息回调内容[查看](./api-reference/IRTCEngineEvent.md)





### 加入频道
```cpp
//如果需要修改配置信息请在,通过getSetting,进行参数设置
std::string token = "";
_irtc->joinChannel(token);
//触发 IRTCEngineEvent.onJoinRoom 事件之后才是真正的入会成功
```

更多参数设置[参看](./api-reference/IRTCSetting.md)



### 开关摄像头
```cpp
    SRTC::IRTCLocalCameraTrack* _camStream = nullptr;
    const char* track_key = "camera";
    SRTC::StatusCode ret = _irtc->getCameraTrack(track_key,&_camStream);
    if((ret != SRTC::StatusCode::OK) || !_camStream )
    {
        return ret;
    }
    _camStream->addPlayView(callbackView);
    _camStream->startCapture();
    _irtc->publish(_camStream);
```

```cpp
    SRTC::IRTCLocalCameraTrack* _camStream = nullptr;
    const char* track_key = "camera";
    SRTC::StatusCode ret = _irtc->getCameraTrack(track_key,&_camStream);
    if((ret != SRTC::StatusCode::OK) || !_camStream )
    {
        retrun ret;
    }
    
    _camStream->stopCapture();
    _camStream->removeAllPlayView();
    _irtc->unpublish(_camStream);
```

更多本地摄像头方法[参看](./api-reference/IRTCLocalScreenTrack.md)



### 开关麦克风
```cpp
    SRTC::IRTCLocalMicTrack* _micStream = nullptr;
    const char* track_key = "mic";
    SRTC::StatusCode ret = _irtc->getAudioTrack(track_key,&_micStream);
    if((ret != SRTC::StatusCode::OK) || !_micStream )
    {
        return ret;
    }
    _micStream->startCapture();   
    _irtc->publish(_micStream); 
```

```cpp
    SRTC::IRTCLocalMicTrack* _micStream = nullptr;
    const char* track_key = "mic";
    SRTC::StatusCode ret = _irtc->getAudioTrack(track_key,&_micStream);
    if((ret != SRTC::StatusCode::OK) || !_micStream )
    {
        return ret;
    }

    _micStream->stopCapture();
    _irtc->unpublish(_micStream); 
```

更多本地麦克风方法[参看](./api-reference/IRTCLocalAudioTrack.md)



### 开关桌面共享
```cpp
    SRTC::IRTCLocalScreenTrack* _screenStream = nullptr;
    const char* track_key = "screen";
    SRTC::StatusCode ret = _irtc->getScreenTrack(track_key,&_screenStream);
    if((ret != SRTC::StatusCode::OK) || !_screenStream )
    {
        return ret;
    }
    _screenStream->startCapture();
    _irtc->publish(_screenStream); 
```

```cpp
    SRTC::IRTCLocalScreenTrack* _screenStream = nullptr;
    const char* track_key = "screen";
    SRTC::StatusCode ret = _irtc->getScreenTrack(track_key,&_screenStream);
    if((ret != SRTC::StatusCode::OK) || !_screenStream )
    {
        return ret;
    }

    _screenStream->stopCapture();
    _irtc->unpublish(_screenStream); 
```

更多本地桌面共享方法[参看](./api-reference/IRTCLocalScreenTrack.md)



### 开关扬声器
```cpp
    SRTC::IRTCRemoteAudioTrack* _speakerStream = nullptr;
    SRTC::StatusCode ret = _irtc->getRemoteAudioTrack("","",&_speakerStream);
    if((ret != SRTC::StatusCode::OK) || !_speakerStream )
    {
        return ret;
    }
    _speakerStream->startPlay();
```

```cpp
    SRTC::IRTCRemoteAudioTrack* _speakerStream = nullptr;
    SRTC::StatusCode ret = _irtc->getRemoteAudioTrack("","",&_speakerStream);
    if((ret != SRTC::StatusCode::OK) || !_speakerStream )
    {
        return ret;
    }

    _speakerStream->stopPlay();
```

更多本地扬声器方法[参看](./api-reference/IRTCRemoteAudioTrack.md)



### 显示关闭远端视频流
```cpp
    SRTC::IRTCRemoteVideoTrack* _remoteStream = nullptr;
    std::string uid = "";//用户uid
    std::string stream_track_id = "";//用户stream_tracks 对应的流id
    SRTC::StatusCode ret = _irtc->getRemoteVideoTrack(uid,stream_track_id,&_remoteStream);
    if((ret != SRTC::StatusCode::OK) || !_remoteStream )
    {
        return ret;
    }

    _remoteStream->addPlayView(hwnd);
    _irtc->subscribe(_remoteStream);
```

```cpp
    SRTC::IRTCRemoteVideoTrack* _remoteStream = nullptr;
    std::string uid = "";//用户uid
    std::string stream_track_id = "";//用户stream_tracks 对应的流id
    SRTC::StatusCode ret = _irtc->getRemoteVideoTrack(uid,stream_track_id,&_remoteStream);
    if((ret != SRTC::StatusCode::OK) || !_remoteStream )
    {
        return ret;
    }

    _remoteStream->removeAllPlayView();
    _irtc->unsubscribe(_remoteStream);
```

### 开关本地录制
```cpp
    std::string mid = sdkInfo.meeting_id().toStdString();
    SMeeting::IMEETRecord* _rc;
    _imeet->getLocalRecord(mid, &_rc);
    //录制指定窗口
    HWND hwnd = (HWND)this->widID();
    _rc->setRecordHwnd(hwnd, 0, 0, 0, 0);
    //录制画面配置
    //_rc->setRecordLayoutMemberView(dt.c_str(),dt.size());
    _rc->startRecord();
```

```cpp
    std::string mid = sdkInfo.meeting_id().toStdString();
    SMeeting::IMEETRecord* _rc;
    _imeet->getLocalRecord(mid, &_rc);
    _rc->stopRecord();
```
更多本地录制方法[参看](./api-reference/IRTCRecord.md)


### 
### 退出频道
```cpp
_irtc->leaveChannel();
```

### 


