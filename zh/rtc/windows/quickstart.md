---
title: "快速开始"
description: "Windows SRTC 音视频 SDK 快速集成，10 分钟跑通基础功能"
---

调用顺序上有两层对象，先分清楚：

+ [IRTCEngine](./api-reference/IRTCEngine.md) —— 进程级，一个就够。负责创建频道、枚举设备、IM、日志上传
+ [IRTCChannel](./api-reference/IRTCChannel.md) —— 一个频道一个对象，成员查询、轨道、推拉流、本地录制都在它上面

### 初始化SDK
```cpp
SRTC::RTCEngineOptions opt;
opt.enable_log = 1;              // 0 或者干脆不传 opt，就完全不写 SDK 日志
opt.log_path   = "D:/log/";      // 为空则用「文档/应用名/logs/」

SRTC::IRTCEngine* _irtc = nullptr;
SRTC::StatusCode ret = SRTC::RTCEngine_Init(&_irtc, &opt);
if ((ret != SRTC::StatusCode::OK) || !_irtc)
{
    return false;
}
```

日志开关和日志目录只能在这里设置，[RTCEngineOptions](./types.md#引擎初始化参数（RTCEngineOptions）)。



### 设置引擎级消息回调
```cpp
_irtc->setEventHandler(this);
```

这里只有**不属于任何频道**的回调：设备变化、网络探测、IM。
更多内容[查看](./api-reference/IRTCEngineEvent.md)。频道级回调见下一步。




### 加入频道

分两步：`createChannel` 只创建对象**不入会**，配置好之后再 `join()`。
之所以要分两步 —— `onJoinChannel` 是在 `join()` 还没返回时就回调出去的，回调设置晚了就收不到。

```cpp
std::string token = "";
SRTC::IRTCChannel* _ch = nullptr;
SRTC::StatusCode ret = _irtc->createChannel(token.c_str(), &_ch);
if ((ret != SRTC::StatusCode::OK) || !_ch)
{
    return ret;                  // 失败时 _ch 一定是 nullptr
}

// 1) 配置。stream_model / simple / mcu_track / enable_audio_record
//    是在 join() 阶段读取的，必须在这里设置
SRTC::IRTCChannelSetting* set = nullptr;
_ch->getSetting(&set);
set->set_stream_model(1);

// 2) 频道级回调，必须在 join() 之前
_ch->setEventHandler(this);

// 3) 真正入会。同步接口，返回前 onJoinChannel 已经回调完毕
ret = _ch->join();
if (ret != SRTC::StatusCode::OK)
{
    _irtc->leaveChannel(_ch->getChannelId());   // 失败的频道对象也要回收
    _ch = nullptr;
    return ret;
}
```

更多参数设置[参看](./api-reference/IRTCChannelSetting.md)，频道级回调[参看](./api-reference/IRTCChannelEvent.md)。

### 开关摄像头
```cpp
    SRTC::IRTCLocalCameraTrack* _camStream = nullptr;
    const char* track_key = "camera";
    SRTC::StatusCode ret = _ch->getCameraTrack(track_key, &_camStream);
    if ((ret != SRTC::StatusCode::OK) || !_camStream)
    {
        return ret;
    }
    _camStream->addPlayView(callbackView);
    _camStream->startCapture();

    SRTC::RTCVideoPublishOptions* opt = nullptr;   // nullptr 表示用默认推流参数
    _ch->publish(_camStream, opt);
```

```cpp
    SRTC::IRTCLocalCameraTrack* _camStream = nullptr;
    const char* track_key = "camera";
    SRTC::StatusCode ret = _ch->getCameraTrack(track_key, &_camStream);
    if ((ret != SRTC::StatusCode::OK) || !_camStream)
    {
        return ret;
    }

    _camStream->stopCapture();
    _camStream->removeAllPlayView();
    _ch->unpublish(_camStream);
```

<Warning>
两个 `publish` 重载不带默认参数，`opt` 必须显式传。而且不能直接写 `publish(tk, nullptr)` ——
视频/音频两个重载会二义，要像上面那样用一个**带类型的**空指针变量。
</Warning>

更多本地摄像头方法[参看](./api-reference/IRTCLocalCameraTrack.md)



### 开关麦克风
```cpp
    SRTC::IRTCLocalMicTrack* _micStream = nullptr;
    const char* track_key = "mic";
    SRTC::StatusCode ret = _ch->getAudioTrack(track_key, &_micStream);
    if ((ret != SRTC::StatusCode::OK) || !_micStream)
    {
        return ret;
    }
    _micStream->startCapture();

    SRTC::RTCAudioPublishOptions* opt = nullptr;
    _ch->publish(_micStream, opt);
```

```cpp
    SRTC::IRTCLocalMicTrack* _micStream = nullptr;
    const char* track_key = "mic";
    SRTC::StatusCode ret = _ch->getAudioTrack(track_key, &_micStream);
    if ((ret != SRTC::StatusCode::OK) || !_micStream)
    {
        return ret;
    }

    _micStream->stopCapture();
    _ch->unpublish(_micStream);
```

更多本地麦克风方法[参看](./api-reference/IRTCLocalMicTrack.md)



### 开关桌面共享
```cpp
    SRTC::IRTCLocalScreenTrack* _screenStream = nullptr;
    const char* track_key = "screen";
    SRTC::StatusCode ret = _ch->getScreenTrack(track_key, &_screenStream);
    if ((ret != SRTC::StatusCode::OK) || !_screenStream)
    {
        return ret;
    }
    _screenStream->startCapture();

    SRTC::RTCVideoPublishOptions* opt = nullptr;
    _ch->publish(_screenStream, opt);
```

```cpp
    SRTC::IRTCLocalScreenTrack* _screenStream = nullptr;
    const char* track_key = "screen";
    SRTC::StatusCode ret = _ch->getScreenTrack(track_key, &_screenStream);
    if ((ret != SRTC::StatusCode::OK) || !_screenStream)
    {
        return ret;
    }

    _screenStream->stopCapture();
    _ch->unpublish(_screenStream);
```

更多本地桌面共享方法[参看](./api-reference/IRTCLocalScreenTrack.md)



### 开关扬声器
```cpp
    SRTC::IRTCRemoteAudioTrack* _speakerStream = nullptr;
    SRTC::StatusCode ret = _ch->getRemoteAudioTrack("", "", &_speakerStream);
    if ((ret != SRTC::StatusCode::OK) || !_speakerStream)
    {
        return ret;
    }
    _speakerStream->startPlay(nullptr);
```

```cpp
    SRTC::IRTCRemoteAudioTrack* _speakerStream = nullptr;
    SRTC::StatusCode ret = _ch->getRemoteAudioTrack("", "", &_speakerStream);
    if ((ret != SRTC::StatusCode::OK) || !_speakerStream)
    {
        return ret;
    }

    _speakerStream->stopPlay();
```

更多本地扬声器方法[参看](./api-reference/IRTCRemoteAudioTrack.md)



### 显示关闭远端视频流
```cpp
    SRTC::IRTCRemoteVideoTrack* _remoteStream = nullptr;
    std::string uid = "";              //用户uid
    std::string stream_track_id = "";  //用户stream_tracks 对应的流id
    SRTC::StatusCode ret = _ch->getRemoteVideoTrack(uid.c_str(), stream_track_id.c_str(), &_remoteStream);
    if ((ret != SRTC::StatusCode::OK) || !_remoteStream)
    {
        return ret;
    }

    SRTC::RTCHwndView view(hwnd);      // 或者自己实现 IRTCView
    _remoteStream->addPlayView(&view);
    _ch->subscribe(_remoteStream);
```

```cpp
    SRTC::IRTCRemoteVideoTrack* _remoteStream = nullptr;
    std::string uid = "";              //用户uid
    std::string stream_track_id = "";  //用户stream_tracks 对应的流id
    SRTC::StatusCode ret = _ch->getRemoteVideoTrack(uid.c_str(), stream_track_id.c_str(), &_remoteStream);
    if ((ret != SRTC::StatusCode::OK) || !_remoteStream)
    {
        return ret;
    }

    _remoteStream->removeAllPlayView();
    _ch->unsubscribe(_remoteStream);
```

<Note>
`addPlayView` 收的是 [IRTCView*](./api-reference/IRTCView.md)。窗口渲染可以直接用头文件里现成的
`SRTC::RTCHwndView`，注意它的生命周期要覆盖到 `removeAllPlayView` 之后。
</Note>

### 开关本地录制
```cpp
    SRTC::IRTCRecord* _rc = nullptr;
    SRTC::StatusCode ret = _ch->getLocalRecord("", &_rc);
    if ((ret != SRTC::StatusCode::OK) || !_rc)
    {
        return ret;      // 未加入频道或当前流媒体模式不支持录制时返回错误
    }
    //录制指定窗口
    HWND hwnd = (HWND)this->winID();
    _rc->setRecordHwnd(hwnd, 0, 0, 0, 0);
    //录制画面配置
    //_rc->setRecordLayoutMemberView(dt.c_str(), dt.size());
    _rc->startRecord();
```

```cpp
    SRTC::IRTCRecord* _rc = nullptr;
    _ch->getLocalRecord("", &_rc);
    _rc->stopRecord();
```

每个频道只有**一个**录制对象，`mid` 参数仅作接口兼容保留，传空串即可。
更多本地录制方法[参看](./api-reference/IRTCRecord.md)


### 退出频道
```cpp
_irtc->leaveChannel(_ch->getChannelId());
_ch = nullptr;      // 对象已销毁，必须自己置空
```

`IRTCChannel` 自身没有 `leave()`。要一次退掉全部频道用 `_irtc->leaveAllChannel()`，
之后所有 `IRTCChannel*` 一并失效。
