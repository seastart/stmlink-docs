---
title: "Quickstart"
description: "The minimal Windows SRTC C++ flow: initialize IRTCEngine with log options, create an IRTCChannel, configure it and register callbacks before join(), publish camera/microphone/screen tracks, play remote audio, render remote video, record locally, and leave. Read after completing integration."
---

There are two layers of objects in the call sequence; tell them apart first:

+ [IRTCEngine](/en/rtc/windows/api-reference/IRTCEngine)—process-level; one is enough. It creates channels, enumerates devices, and handles IM and log upload
+ [IRTCChannel](/en/rtc/windows/api-reference/IRTCChannel)—one object per channel. User queries, tracks, publishing and subscribing, and local recording are all on it

### Initialize the SDK
```cpp
SRTC::RTCEngineOptions opt;
opt.enable_log = 1;              // 0 (or not passing opt at all) disables SDK logging entirely
opt.log_path   = "D:/log/";      // If empty, uses "Documents/<app name>/logs/"

SRTC::IRTCEngine* _irtc = nullptr;
SRTC::StatusCode ret = SRTC::RTCEngine_Init(&_irtc, &opt);
if ((ret != SRTC::StatusCode::OK) || !_irtc)
{
    return false;
}
```

The log switch and log directory can only be set here; see [RTCEngineOptions](/en/rtc/windows/types#engine-initialization-options-rtcengineoptions).



### Set the engine-level event handler
```cpp
_irtc->setEventHandler(this);
```

This handler only receives callbacks that **don't belong to any channel**: device changes, network probing, and IM.
For details, see [IRTCEngineEvent](/en/rtc/windows/api-reference/IRTCEngineEvent). Channel-level callbacks are covered in the next step.




### Join a channel

This takes two steps: `createChannel` only creates the object and **doesn't join**; call `join()` after you've configured it.
The reason for two steps: `onJoinChannel` is called back before `join()` returns, so if you set the handler too late, you miss it.

```cpp
std::string token = "";
SRTC::IRTCChannel* _ch = nullptr;
SRTC::StatusCode ret = _irtc->createChannel(token.c_str(), &_ch);
if ((ret != SRTC::StatusCode::OK) || !_ch)
{
    return ret;                  // On failure, _ch is always nullptr
}

// 1) Configuration. stream_model / simple / mcu_track / enable_audio_record
//    are read during join(), so they must be set here
SRTC::IRTCChannelSetting* set = nullptr;
_ch->getSetting(&set);
set->set_stream_model(1);

// 2) Channel-level callbacks; must be set before join()
_ch->setEventHandler(this);

// 3) Actually join. This is synchronous; onJoinChannel has already been called back before it returns
ret = _ch->join();
if (ret != SRTC::StatusCode::OK)
{
    _irtc->leaveChannel(_ch->getChannelId());   // A failed channel object must also be reclaimed
    _ch = nullptr;
    return ret;
}
```

For more settings, see [IRTCChannelSetting](/en/rtc/windows/api-reference/IRTCChannelSetting); for channel-level callbacks, see [IRTCChannelEvent](/en/rtc/windows/api-reference/IRTCChannelEvent).

### Turn the camera on and off
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

    SRTC::RTCVideoPublishOptions* opt = nullptr;   // nullptr means use the default publishing parameters
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
The two `publish` overloads have no default argument, so you must pass `opt` explicitly. And you can't write `publish(tk, nullptr)` directly—
the video and audio overloads would be ambiguous. Use a **typed** null pointer variable as shown above.
</Warning>

For more local camera methods, see [IRTCLocalCameraTrack](/en/rtc/windows/api-reference/IRTCLocalCameraTrack).



### Turn the microphone on and off
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

For more local microphone methods, see [IRTCLocalMicTrack](/en/rtc/windows/api-reference/IRTCLocalMicTrack).



### Start and stop screen sharing
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

For more local screen sharing methods, see [IRTCLocalScreenTrack](/en/rtc/windows/api-reference/IRTCLocalScreenTrack).



### Turn the speaker on and off
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

For more speaker methods, see [IRTCRemoteAudioTrack](/en/rtc/windows/api-reference/IRTCRemoteAudioTrack).



### Show and hide remote video
```cpp
    SRTC::IRTCRemoteVideoTrack* _remoteStream = nullptr;
    std::string uid = "";              // The user's uid
    std::string stream_track_id = "";  // Track ID from the user's stream_tracks
    SRTC::StatusCode ret = _ch->getRemoteVideoTrack(uid.c_str(), stream_track_id.c_str(), &_remoteStream);
    if ((ret != SRTC::StatusCode::OK) || !_remoteStream)
    {
        return ret;
    }

    SRTC::RTCHwndView view(hwnd);      // Or implement IRTCView yourself
    _remoteStream->addPlayView(&view);
    _ch->subscribe(_remoteStream);
```

```cpp
    SRTC::IRTCRemoteVideoTrack* _remoteStream = nullptr;
    std::string uid = "";              // The user's uid
    std::string stream_track_id = "";  // Track ID from the user's stream_tracks
    SRTC::StatusCode ret = _ch->getRemoteVideoTrack(uid.c_str(), stream_track_id.c_str(), &_remoteStream);
    if ((ret != SRTC::StatusCode::OK) || !_remoteStream)
    {
        return ret;
    }

    _remoteStream->removeAllPlayView();
    _ch->unsubscribe(_remoteStream);
```

<Note>
`addPlayView` takes an [IRTCView*](/en/rtc/windows/api-reference/IRTCView). For window rendering, you can use the ready-made
`SRTC::RTCHwndView` from the header directly; make sure its lifetime extends past `removeAllPlayView`.
</Note>

### Start and stop local recording
```cpp
    SRTC::IRTCRecord* _rc = nullptr;
    SRTC::StatusCode ret = _ch->getLocalRecord("", &_rc);
    if ((ret != SRTC::StatusCode::OK) || !_rc)
    {
        return ret;      // Returns an error if you haven't joined the channel or the current media streaming mode doesn't support recording
    }
    // Record the specified window
    HWND hwnd = (HWND)this->winID();
    _rc->setRecordHwnd(hwnd, 0, 0, 0, 0);
    // Recording layout configuration
    //_rc->setRecordLayoutMemberView(dt.c_str(), dt.size());
    _rc->startRecord();
```

```cpp
    SRTC::IRTCRecord* _rc = nullptr;
    _ch->getLocalRecord("", &_rc);
    _rc->stopRecord();
```

Each channel has only **one** recording object. The `mid` parameter is kept only for interface compatibility; pass an empty string.
For more local recording methods, see [IRTCRecord](/en/rtc/windows/api-reference/IRTCRecord).


### Leave the channel
```cpp
_irtc->leaveChannel(_ch->getChannelId());
_ch = nullptr;      // The object has been destroyed; you must set the pointer to null yourself
```

`IRTCChannel` itself has no `leave()`. To leave all channels at once, use `_irtc->leaveAllChannel()`;
after that, every `IRTCChannel*` becomes invalid.
