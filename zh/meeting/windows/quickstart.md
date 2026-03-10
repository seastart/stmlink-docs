---
title: "C++ 快速开始"
description: "Windows SMeeting 会议 SDK C++ 快速集成，10 分钟跑通基础功能"
---

# C++ 快速开始

本文档介绍如何在 Windows 平台使用 C++ 集成 SMeeting SDK。

## 基本概念

+ **ISMeetingEngine**：SDK 核心引擎类，提供 SMeeting 的基础功能。通过 `setEventHandler` 绑定回调监听，通过 `getSetting` 设置基本参数。
+ 部分接口只允许在进入会议后调用。

---

## 初始化 SDK

```cpp
#include "SMeeting.h"

// 初始化引擎
SMeeting::ISMeetingEngine* _imeet = nullptr;
SMeeting::StatusCode ret = SMeeting::SMeetingEngine_Init(&_imeet);
if (ret != SMeeting::StatusCode::OK) {
    return ret;
}

// 设置事件回调（当前类需继承 ISMeetingEngineEvent）
_imeet->setEventHandler(this);
```

### 实现事件回调类

```cpp
class MyEventHandler : public SMeeting::ISMeetingEngineEvent {
public:
    void onDisconnected(SMeeting::DisconnectReason reason, 
                        SMeeting::StatusCode code, 
                        std::string message) override {
        // 处理断开连接事件
    }

    void onReconnected() override {
        // 处理重连成功事件
    }

    void onUserEnter(std::string roomno, std::string userdata) override {
        // 处理用户进入事件
    }

    // ... 实现其他需要的事件回调
};
```

---

## 登录与登出

### 登录

```cpp
std::string token = "your_token_here";
_imeet->login(token, [&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // 登录成功
    } else {
        // 登录失败
    }
});
```

### 登出

```cpp
_imeet->logout([&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // 登出成功
    }
});
```

---

## 创建会议

```cpp
SMeeting::SMeetingCreateMeetingModel model;
model.title = "我的会议";
model.content = "会议说明";
model.meeting_type = 1;  // 1: 临时会议，2: 预约会议
model.meeting_mode = 1;  // 1: 普通

_imeet->createRoom(model, [&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // msg 为会议号
        std::cout << "会议创建成功，会议号：" << msg << std::endl;
    }
});
```

---

## 加入会议

### 配置 SDK 参数

```cpp
SMeeting::ISMeetingSetting* setting = nullptr;
_imeet->getSetting(&setting);
if (setting) {
    setting->set_stream_model(1);           // 设置流媒体模式
    setting->set_speaker_interval(500);     // 音柱回调周期 (ms)
    setting->set_stat_interval(10000);      // 网络统计回调周期 (ms)
    setting->set_enable_audio_record(1);    // 启用音频录制
    setting->set_enable_stream_log(1);      // 启用流日志
}
```

### 进入房间

```cpp
std::string roomno = "123456789";
std::string name = "张三";
std::string pass = "";  // 会议密码，无密码则为空

_imeet->enterRoom(roomno, name, pass, [&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // 进入房间成功
    } else {
        // 进入房间失败
    }
});
```

---

## 退出会议

```cpp
_imeet->exitRoom([&](SMeeting::StatusCode status, std::string msg) {
    // 退出房间结果
});
```

---

## 结束会议（主持人）

```cpp
// 主持人解散会议
_imeet->adminDestroyRoom([&](SMeeting::StatusCode status, std::string msg) {
    // 结束会议结果
});
```

---

## 取消会议（会议外）

```cpp
std::string meeting_id = "sw46gz";
_imeet->cancelRoom(meeting_id, [&](SMeeting::StatusCode status, std::string msg) {
    // 取消会议结果
});
```

---

## 获取房间和成员信息

```cpp
std::string s;

// 获取自身信息
_imeet->getMe(s);

// 获取房间信息
_imeet->getRoom(s);

// 获取所有成员信息
_imeet->getMembers(s);

// 获取指定成员信息
std::string uid = "user_123";
_imeet->getMember(uid, s);
```

---

## 更新昵称

```cpp
std::string new_name = "新昵称";
_imeet->updateName(new_name, [&](SMeeting::StatusCode status, std::string msg) {
    // 昵称修改结果
});
```

---

## 获取设备列表

```cpp
// type: 1=麦克风，2=扬声器，3=摄像头
std::vector<int> types = {1, 2, 3};
int page = 1;
std::string find_key = "";

_imeet->listAgent(types, page, find_key, [&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // msg 为设备列表 JSON 字符串
    }
});
```

---

## 摄像头操作

### 获取摄像头对象

```cpp
SMeeting::IMEETLocalCamera* camera = nullptr;
SMeeting::StatusCode sc = _imeet->getLocalCamera(&camera);
if (sc != SMeeting::StatusCode::OK) {
    return;
}
```

### 打开摄像头

```cpp
// 设置渲染窗口（hwnd 为窗口句柄）
camera->addPlayView(hwnd);

// 请求打开摄像头
camera->requestOpenCamera([&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // 摄像头打开成功
    }
});
```

### 切换摄像头

```cpp
std::string camera_name = "Integrated Camera";
int width = 640;
int height = 480;
camera->switchCamera(camera_name, width, height);
```

### 关闭摄像头

```cpp
camera->closeCamera([&](SMeeting::StatusCode status, std::string msg) {
    // 摄像头关闭结果
});
```

---

## 远端视频播放

### 获取远端视频对象

```cpp
std::string uid = "user_123";
std::string track_desc = SMeeting::TRACK_DESC_CAMERA_BIG;  // 或 TRACK_DESC_CAMERA_SMALL

SMeeting::IMEETRemoteVideo* remote_video = nullptr;
_imeet->getRemoteVideo(uid, track_desc, &remote_video);
```

### 开始播放

```cpp
// 设置渲染窗口
remote_video->addPlayView(hwnd);

// 开始加载远端视频流
remote_video->loadRemoteVideo();
```

### 停止播放

```cpp
remote_video->unLoadRemoteVideo();
remote_video->removeAllPlayView();
```

---

## 麦克风操作

### 获取麦克风对象

```cpp
SMeeting::IMEETLocalMic* mic = nullptr;
_imeet->getLocalMic(&mic);
```

### 打开麦克风

```cpp
mic->requestOpenMic([&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // 麦克风打开成功
    }
});
```

### 切换麦克风

```cpp
std::string mic_name = "Default Microphone";
mic->switchMic(mic_name);
```

### 关闭麦克风

```cpp
mic->closeMic([&](SMeeting::StatusCode status, std::string msg) {
    // 麦克风关闭结果
});
```

---

## 扬声器操作

### 获取远端音频对象

```cpp
SMeeting::IMEETRemoteAudio* audio = nullptr;
_imeet->getRemoteAudio("", &audio);
```

### 打开扬声器

```cpp
audio->openSpeaker();
```

### 切换扬声器

```cpp
std::string speaker_name = "Default Speakers";
audio->switchSpeaker(speaker_name);
```

### 关闭扬声器

```cpp
audio->closeSpeaker();
```

---

## 屏幕共享

### 获取屏幕共享对象

```cpp
SMeeting::IMEETLocalScreen* screen = nullptr;
_imeet->getLocalScreen(&screen);
```

### 开始共享

```cpp
// tp: 1=屏幕共享，2=窗口共享
// data: 屏幕索引或窗口句柄字符串
int tp = 1;
std::string data = "0,0,1920,1080";  // 主屏幕
//std::string data_hwnd = "hwnd:123321";//窗口采集

screen->requestShare(tp, data, [&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // 共享开始成功
    }
});
```

### 停止共享

```cpp
screen->stopShare([&](SMeeting::StatusCode status, std::string msg) {
    // 共享停止结果
});
```

---

## 聊天消息

### 发送聊天消息

```cpp
// tp: 1=文本，2=文件，3=图片，4=声音
int msg_type = 1;
std::string msg = "大家好！";

_imeet->sendRoomChatMessage(msg_type, msg, [&](SMeeting::StatusCode status, std::string m) {
    // 发送结果
});
```

---

## 主持人管理接口

### 请求用户打开摄像头

```cpp
std::string uid = "user_123";
_imeet->adminRequestUserOpenCamera(uid, [&](SMeeting::StatusCode status, std::string msg) {
    // 请求结果
});
```

### 关闭用户摄像头

```cpp
_imeet->adminCloseUserCamera(uid, [&](SMeeting::StatusCode status, std::string msg) {
    // 操作结果
});
```

### 请求用户打开麦克风

```cpp
_imeet->adminRequestUserOpenMic(uid, [&](SMeeting::StatusCode status, std::string msg) {
    // 请求结果
});
```

### 关闭用户麦克风

```cpp
_imeet->adminCloseUserMic(uid, [&](SMeeting::StatusCode status, std::string msg) {
    // 操作结果
});
```

### 踢出用户

```cpp
_imeet->adminKickUserOut(uid, [&](SMeeting::StatusCode status, std::string msg) {
    // 踢出结果
});
```

### 设置房间麦克风权限

```cpp
bool self_unmute_mic_disabled = true;   // 是否禁止自行解除静音
bool mic_disabled = true;               // 是否禁用房间音频

_imeet->adminUpdateRoomMicState(self_unmute_mic_disabled, mic_disabled, 
    [&](SMeeting::StatusCode status, std::string msg) {
        // 设置结果
    });
```

---

## MCU 合成视频

### 获取 MCU 视频对象

```cpp
SMeeting::IMEETRemoteVideo* mcu_video = nullptr;
_imeet->getMcuVideo(&mcu_video);
```

### 播放合成流

```cpp
mcu_video->addPlayView(hwnd);
mcu_video->loadRemoteVideo();
```

### 停止播放

```cpp
mcu_video->unLoadRemoteVideo();
```

---

## 释放资源

```cpp
// 释放引擎
if (_imeet) {
    _imeet->del();
    _imeet = nullptr;
}
```

---

## 完整示例

```cpp
#include "SMeeting.h"
#include <iostream>

class MyHandler : public SMeeting::ISMeetingEngineEvent {
public:
    void onDisconnected(SMeeting::DisconnectReason reason,
                        SMeeting::StatusCode code,
                        std::string message) override {
        std::cout << "Disconnected: " << (int)code << std::endl;
    }

    void onUserEnter(std::string roomno, std::string userdata) override {
        std::cout << "User entered: " << userdata << std::endl;
    }
    
    // 实现其他需要的回调...
};

int main() {
    // 初始化
    SMeeting::ISMeetingEngine* engine = nullptr;
    SMeeting::StatusCode ret = SMeeting::SMeetingEngine_Init(&engine);
    if (ret != SMeeting::StatusCode::OK) {
        return -1;
    }

    MyHandler handler;
    engine->setEventHandler(&handler);

    // 登录
    std::string token = "your_token";
    engine->login(token, [&](SMeeting::StatusCode status, std::string msg) {
        if (status == SMeeting::StatusCode::OK) {
            // 创建会议
            SMeeting::SMeetingCreateMeetingModel model;
            model.title = "测试会议";
            engine->createRoom(model, [&](SMeeting::StatusCode status, std::string roomno) {
                if (status == SMeeting::StatusCode::OK) {
                    // 进入会议
                    engine->enterRoom(roomno, "用户 A", "", 
                        [&](SMeeting::StatusCode status, std::string msg) {
                            if (status == SMeeting::StatusCode::OK) {
                                std::cout << "进入会议成功" << std::endl;
                            }
                        });
                }
            });
        }
    });

    // 等待异步操作完成（实际应用中应有事件循环）
    std::this_thread::sleep_for(std::chrono::seconds(30));

    // 清理
    engine->logout();
    engine->del();

    return 0;
}
```
