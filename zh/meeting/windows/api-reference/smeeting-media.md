---
title: "媒体轨道接口"
description: "Windows SMeeting SDK 本地 / 远端 / 自定义媒体轨道 C++ 接口参考"
---

以下媒体对象均通过 [ISMeetingChannel](/zh/meeting/windows/api-reference/smeeting-channel) 获取。

---

## 本地媒体流接口

### 获取本地麦克风对象
```cpp
virtual StatusCode getLocalMic(IMEETLocalMic**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| （输出） | IMEETLocalMic** | 输出的本地麦克风对象指针 |

**返回值**

`StatusCode` - 错误码

### 获取本地摄像头对象
```cpp
virtual StatusCode getLocalCamera(IMEETLocalCamera**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| （输出） | IMEETLocalCamera** | 输出的本地摄像头对象指针 |

**返回值**

`StatusCode` - 错误码

### 获取本地屏幕共享对象
```cpp
virtual StatusCode getLocalScreen(IMEETLocalScreen**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| （输出） | IMEETLocalScreen** | 输出的本地屏幕共享对象指针 |

**返回值**

`StatusCode` - 错误码

---

## 远端媒体流接口

### 获取远端视频对象
```cpp
virtual StatusCode getRemoteVideo(std::string uid, std::string track_desc, IMEETRemoteVideo**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| track_desc | std::string | 轨道描述 |
| （输出） | IMEETRemoteVideo** | 输出的远端视频对象指针 |

**返回值**

`StatusCode` - 错误码

### 获取远端音频对象
```cpp
virtual StatusCode getRemoteAudio(std::string uid, IMEETRemoteAudio**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| （输出） | IMEETRemoteAudio** | 输出的远端音频对象指针 |

**返回值**

`StatusCode` - 错误码

### 获取 MCU 视频对象
```cpp
virtual StatusCode getMcuVideo(IMEETRemoteVideo**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| （输出） | IMEETRemoteVideo** | 输出的 MCU 视频对象指针 |

**返回值**

`StatusCode` - 错误码

---

## 自定义轨道接口

### 获取自定义视频轨道
```cpp
virtual StatusCode getCustomVideo(CustomPublishTrack* push, IMeetCustomVideoTrack**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| push | CustomPublishTrack* | 自定义轨道配置 |
| （输出） | IMeetCustomVideoTrack** | 输出的自定义视频轨道对象指针 |

**返回值**

`StatusCode` - 错误码

### 获取自定义音频轨道
```cpp
virtual StatusCode getCustomAudio(CustomPublishTrack* push, IMeetCustomAudioTrack**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| push | CustomPublishTrack* | 自定义轨道配置 |
| （输出） | IMeetCustomAudioTrack** | 输出的自定义音频轨道对象指针 |

**返回值**

`StatusCode` - 错误码

### 设置自定义接收回调
```cpp
virtual StatusCode setCustomRecvBack(RTC_Custom_FrameEvent e, void* ext) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| e | RTC_Custom_FrameEvent | 帧事件回调函数 |
| ext | void* | 扩展数据 |

**返回值**

`StatusCode` - 错误码

---

## IMeetCustomVideoTrack 接口

由 `getCustomVideo` 返回。

### 获取自定义轨道信息
```cpp
virtual StatusCode getTrackInfo(CustomPublishTrack**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| （输出） | CustomPublishTrack** | 输出的自定义轨道配置 |

**返回值**

`StatusCode` - 错误码

### 推送视频帧
```cpp
virtual StatusCode pushVideoFrame(int stmtype, unsigned char* buf, int buf_len, int frmtype, long ts) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| stmtype | int | 流类型 |
| buf | unsigned char* | 视频帧数据 |
| buf_len | int | 数据长度 |
| frmtype | int | 帧类型 |
| ts | long | 时间戳 |

**返回值**

`StatusCode` - 错误码

### 取消发布
```cpp
virtual StatusCode unpublish() = 0;
```

**返回值**

`StatusCode` - 错误码

---

## IMeetCustomAudioTrack 接口

由 `getCustomAudio` 返回。

### 获取自定义轨道信息
```cpp
virtual StatusCode getTrackInfo(CustomPublishTrack**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| （输出） | CustomPublishTrack** | 输出的自定义轨道配置 |

**返回值**

`StatusCode` - 错误码

### 推送音频帧
```cpp
virtual StatusCode pushAudioFrame(int stmtype, unsigned char* buf, int buf_len, long ts) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| stmtype | int | 流类型 |
| buf | unsigned char* | 音频帧数据 |
| buf_len | int | 数据长度 |
| ts | long | 时间戳 |

**返回值**

`StatusCode` - 错误码

### 取消发布
```cpp
virtual StatusCode unpublish() = 0;
```

**返回值**

`StatusCode` - 错误码

---

## 本地录制接口

### 获取本地录制对象
```cpp
virtual StatusCode getLocalRecord(IMEETRecord** e) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| e | IMEETRecord** | 录制对象指针 |

**返回值**

`StatusCode` - 错误码

> 从 `1.0.0-alpha.5` 开始不再需要传入会议 ID，使用当前 channel 自己的会议 ID。

---

## IMEETLocalMic 接口

### 请求打开麦克风
```cpp
virtual StatusCode requestOpenMic(Callback back = NULL) = 0;
```

### 关闭麦克风
```cpp
virtual StatusCode closeMic(Callback back = NULL) = 0;
```

### 切换麦克风
```cpp
virtual StatusCode switchMic(std::string name) = 0;
```

### 确认打开麦克风
```cpp
virtual StatusCode confirmOpenMic(bool approve, std::string uid, Callback function = NULL) = 0;
```

---

## IMEETLocalCamera 接口

继承自 `IMEETVideo`。

### 切换摄像头
```cpp
virtual StatusCode switchCamera(std::string name, int w = 0, int h = 0) = 0;
```

### 请求打开摄像头
```cpp
virtual StatusCode requestOpenCamera(Callback back = NULL) = 0;
```

### 关闭摄像头
```cpp
virtual StatusCode closeCamera(Callback back = NULL) = 0;
```

### 确认打开摄像头
```cpp
virtual StatusCode confirmOpenCamera(bool approve, std::string uid, Callback function = nullptr) = 0;
```

---

## IMEETLocalScreen 接口

继承自 `IMEETVideo`。

### 请求共享
```cpp
virtual StatusCode requestShare(int tp, std::string data, Callback back = NULL) = 0;
```

### 停止共享
```cpp
virtual StatusCode stopShare(Callback back = NULL) = 0;
```

### 添加屏幕音频
```cpp
virtual StatusCode addScreenAudio(bool) = 0;
```

### 更新流输出
```cpp
virtual StatusCode updateStreamOutput(int w, int h) = 0;
```

### 确认打开共享
```cpp
virtual StatusCode confirmOpenShare(int tp, std::string data, Callback back = NULL) = 0;
```

---

## IMEETRemoteVideo 接口

继承自 `IMEETVideo`。

### 加载远端视频
```cpp
virtual StatusCode loadRemoteVideo() = 0;
```

### 卸载远端视频
```cpp
virtual StatusCode unLoadRemoteVideo() = 0;
```

---

## IMEETRemoteAudio 接口

### 打开扬声器
```cpp
virtual StatusCode openSpeaker() = 0;
```

### 关闭扬声器
```cpp
virtual StatusCode closeSpeaker() = 0;
```

### 切换扬声器
```cpp
virtual StatusCode switchSpeaker(std::string name) = 0;
```

---

## IMEETRecord 接口

### 设置录制文件名
```cpp
virtual StatusCode setRecordFileName(std::string filepath) = 0;
```

### 设置水印
```cpp
virtual StatusCode setWaterMask(std::string mask) = 0;
```

### 开始录制
```cpp
virtual StatusCode startRecord() = 0;
```

### 设置录制窗口
```cpp
virtual StatusCode setRecordHwnd(void*, int, int, int, int) = 0;
```

### 设置录制布局成员视图
```cpp
virtual StatusCode setRecordLayoutMemberView(std::string json) = 0;
```

### 暂停录制
```cpp
virtual StatusCode pauseRecord() = 0;
```

### 停止录制
```cpp
virtual StatusCode stopRecord() = 0;
```

---

## IMEETVideo 接口

### 添加播放视图
```cpp
virtual StatusCode addPlayView(IRTCView* v) = 0;
```

### 移除播放视图
```cpp
virtual StatusCode removePlayView(IRTCView* v) = 0;
```

### 移除所有播放视图
```cpp
virtual StatusCode removeAllPlayView() = 0;
```
