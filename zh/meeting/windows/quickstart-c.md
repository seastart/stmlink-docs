---
title: "C 快速开始"
description: "Windows SMeeting 会议 SDK C 快速集成，10 分钟跑通基础功能"
---

# C 快速开始

本文档介绍如何在 Windows 平台使用 C 语言集成 SMeeting SDK。

## 基本概念

+ **SMeetingEngine**：SDK 核心引擎，通过 `SMeetingEngine_setEventHandler` 绑定回调监听。
+ 配置接口通过 `SMeetingEngine_setXxx` 系列函数设置基本参数。
+ 部分接口只允许在进入会议后调用。

---

## 初始化 SDK

```c
#include "SMeeting_C.h"

// 初始化引擎
StatusCodeC ret = SMeetingEngine_Init_C();
if (ret != 0) {
    return ret;
}

// 设置事件回调
SMeetingEngine_setEventHandler(RoomEvent, NULL);
```

### 实现事件回调函数

```c
// 事件回调函数
int RoomEvent(int iEvent, void* pEventData, int iDataSize, void* pContext)
{
    switch(iEvent) {
        case SMeeting_Func_CallBack:
            // 处理函数结果回调事件，参考(回调 Key:xx)
            break;
        case SMeeting_Event_Disconnected:
            // 处理断开连接事件
            break;
            
        case SMeeting_Event_Reconnected:
            // 处理重连成功事件
            break;
            
        case SMeeting_Event_UserEnter:
            // 处理用户进入事件
            break;
            
        case SMeeting_Event_UserExit:
            // 处理用户离开事件
            break;
            
        // ... 处理其他需要的事件
    }
    return 0;
}
```

---

## 登录与登出

### 登录

```c
const char* token = "your_token_here";
StatusCodeC ret = SMeetingEngine_login(token);
// 登录结果通过回调函数异步返回（回调 Key: 100）
```

### 登出

```c
StatusCodeC ret = SMeetingEngine_logout();
// 登出结果通过回调函数异步返回（回调 Key: 101）
```

---

## 创建会议

```c
const char* json = "{\"title\":\"我的会议\",\"content\":\"会议说明\",\"meeting_type\":1,\"meeting_mode\":1}";
int json_len = strlen(json);

char* outdata = NULL;
int outlen = 0;

StatusCodeC ret = SMeetingEngine_createRoom(json, json_len);
// 创建结果通过回调函数异步返回（回调 Key: 110）
// 成功时返回会议号
```

---

## 加入会议

### 配置 SDK 参数

```c
SMeetingEngine_setStream_model(1);          // 设置流媒体模式
SMeetingEngine_setSpeaker_interval(500);    // 音柱回调周期 (ms)
SMeetingEngine_setStat_interval(10000);     // 网络统计回调周期 (ms)
SMeetingEngine_setEnable_audio_record(1);   // 启用音频录制
SMeetingEngine_setEnable_stream_log(1);     // 启用流日志
```

### 进入房间

```c
const char* roomno = "123456789";
const char* name = "张三";
const char* pass = "";  // 会议密码，无密码则为空

StatusCodeC ret = SMeetingEngine_enterRoom(roomno, name, pass);
// 进入房间结果通过回调函数异步返回（回调 Key: 112）
```

---

## 退出会议

```c
StatusCodeC ret = SMeetingEngine_exitRoom();
// 退出房间结果通过回调函数异步返回（回调 Key: 114）
```

---

## 结束会议（主持人）

```c
// 主持人解散会议
StatusCodeC ret = SMeetingEngine_adminDestroyRoom();
// 结束会议结果通过回调函数异步返回（回调 Key: 200）
```

---

## 取消会议（会前）

```c
const char* meeting_id = "sw46gz";
StatusCodeC ret = SMeetingEngine_cancelRoom(meeting_id);
// 取消会议结果通过回调函数异步返回（回调 Key: 108）
```

---

## 获取房间和成员信息

```c
char* out = NULL;
int len = 0;

// 获取自身信息
SMeetingEngine_getMe(&out, &len);

// 获取房间信息
SMeetingEngine_getRoom(&out, &len);

// 获取所有成员信息
SMeetingEngine_getMembers(&out, &len);

// 获取指定成员信息
const char* uid = "user_123";
SMeetingEngine_getMember(uid, &out, &len);
```

---

## 更新昵称

```c
const char* new_name = "新昵称";
StatusCodeC ret = SMeetingEngine_updateName(new_name);
// 昵称修改结果通过回调函数异步返回（回调 Key: 301）
```

---

## 获取设备列表

```c
// type: 2SIP,3H323,4GB28181,5RTSP拉流,6RTMP拉流,7文件播放,8腾讯会议,9AI
const char* types = "2|3|5";  // 竖线分隔
int page = 1;
const char* find_key = "";

char* out = NULL;
int len = 0;

StatusCodeC ret = SMeetingEngine_listAgent(types, page, find_key);
// 设备列表结果通过回调函数异步返回（回调 Key: 103）
```

---

## 摄像头操作

### 打开摄像头

```c
// 设置渲染窗口句柄
int camera_render_key = 1;
SMeetingEngine_setCameraRenderKey(camera_render_key);

// 请求打开摄像头
StatusCodeC ret = SMeetingEngine_requestOpenCamera();
// 打开结果通过回调函数异步返回（回调 Key: 802）
```

### 切换摄像头

```c
const char* camera_name = "Integrated Camera";
int width = 640;
int height = 480;

StatusCodeC ret = SMeetingEngine_switchCamera(camera_name, width, height);
```

### 关闭摄像头

```c
StatusCodeC ret = SMeetingEngine_closeCamera();
// 关闭结果通过回调函数异步返回（回调 Key: 803）
```

---

## 远端视频播放

### 开始播放远端视频

```c
const char* uid = "user_123";
const char* track_desc = "camera_big";  // 或 "camera_small"
int render_key = 2;  // 渲染key

StatusCodeC ret = SMeetingEngine_loadRemoteVideo(uid, track_desc, render_key);
```

### 停止播放

```c
const char* uid = "user_123";
const char* track_desc = "camera_big";

StatusCodeC ret = SMeetingEngine_unloadRemoteVideo(uid, track_desc);
```

---

## 麦克风操作

### 打开麦克风

```c
StatusCodeC ret = SMeetingEngine_requestOpenMic();
// 打开结果通过回调函数异步返回（回调 Key: 800）
```

### 切换麦克风

```c
const char* mic_name = "Default Microphone";
StatusCodeC ret = SMeetingEngine_switchMic(mic_name);
```

### 关闭麦克风

```c
StatusCodeC ret = SMeetingEngine_closeMic();
// 关闭结果通过回调函数异步返回（回调 Key: 801）
```

---

## 扬声器操作

### 打开扬声器

```c
StatusCodeC ret = SMeetingEngine_openSpeaker();
```

### 切换扬声器

```c
const char* speaker_name = "Default Speakers";
StatusCodeC ret = SMeetingEngine_switchSpeaker(speaker_name);
```

### 关闭扬声器

```c
StatusCodeC ret = SMeetingEngine_closeSpeaker();
```

---

## 屏幕共享

### 开始共享

```c
// tp: 1=屏幕共享，2=窗口共享
// data: 屏幕索引或窗口信息
int tp = 1;
const char* data = "0";  // 主屏幕

StatusCodeC ret = SMeetingEngine_requestShare(tp, data);
// 共享结果通过回调函数异步返回（回调 Key: 804）
```

### 停止共享

```c
StatusCodeC ret = SMeetingEngine_stopShare();
// 停止结果通过回调函数异步返回（回调 Key: 805）
```

---

## 聊天消息

### 发送聊天消息

```c
// tp: 1=文本，2=文件，3=图片，4=声音
int msg_type = 1;
const char* msg = "大家好！";

StatusCodeC ret = SMeetingEngine_sendRoomChatMessage(msg_type, msg);
// 发送结果通过回调函数异步返回（回调 Key: 302）
```

---

## 主持人管理接口

### 请求用户打开摄像头

```c
const char* uid = "user_123";
StatusCodeC ret = SMeetingEngine_adminRequestUserOpenCamera(uid);
// 请求结果通过回调函数异步返回（回调 Key: 220）
```

### 关闭用户摄像头

```c
StatusCodeC ret = SMeetingEngine_adminCloseUserCamera(uid);
// 操作结果通过回调函数异步返回（回调 Key: 218）
```

### 请求用户打开麦克风

```c
StatusCodeC ret = SMeetingEngine_adminRequestUserOpenMic(uid);
// 请求结果通过回调函数异步返回（回调 Key: 221）
```

### 关闭用户麦克风

```c
StatusCodeC ret = SMeetingEngine_adminCloseUserMic(uid);
// 操作结果通过回调函数异步返回（回调 Key: 219）
```

### 踢出用户

```c
StatusCodeC ret = SMeetingEngine_adminKickUserOut(uid);
// 踢出结果通过回调函数异步返回（回调 Key: 222）
```

### 设置房间麦克风权限

```c
bool self_unmute_mic_disabled = true;   // 是否禁止自行解除静音
bool mic_disabled = true;               // 是否禁用房间音频

StatusCodeC ret = SMeetingEngine_adminUpdateRoomMicState2(self_unmute_mic_disabled, mic_disabled);
// 设置结果通过回调函数异步返回（回调 Key: 207）
```

---

## MCU 合成视频

### 播放合成流

```c
int mcu_render_key = 3;
StatusCodeC ret = SMeetingEngine_loadMcuVideo(mcu_render_key);
```

### 停止播放

```c
StatusCodeC ret = SMeetingEngine_unloadMcuVideo();
```

---

## 本地录制

### 设置录制参数

```c
const char* filepath = "C:\\record\\meeting.mp4";
int filepath_len = strlen(filepath);

SMeetingEngine_setRecordFileName(filepath, filepath_len);

// 设置水印
const char* mask = "会议录制";
SMeetingEngine_setWaterMask(mask, strlen(mask));

// 设置录制窗口
void* hwnd = GetWindowHandle();
SMeetingEngine_setRecordHwnd(hwnd, 0, 0, 0, 0);
```

### 开始录制

```c
StatusCodeC ret = SMeetingEngine_startRecord();
```

### 暂停/继续录制

```c
SMeetingEngine_pauseRecord();
```

### 停止录制

```c
SMeetingEngine_stopRecord();
```

---

## 错误码处理

### 获取错误码描述

```c
StatusCodeC code = 100001;
char msg[256];
int len = SMeetingEngine_GetStatusMsg_C(code, msg, sizeof(msg));
printf("错误描述：%s\n", msg);
```

### 常见错误码

| 错误码 | 说明 |
| --- | --- |
| 0 | 成功 |
| 100001 | 系统错误 |
| 100002 | 未初始化 |
| 100006 | 参数无效 |
| 100009 | 网络错误 |

---

## 完整示例

```c
#include "SMeeting_C.h"
#include <stdio.h>
#include <string.h>
#include <windows.h>


#define camera_render_key 1
#define remote_render_key 2
#define mcu_render_key 2

YUV420Player* camera_player = nullptr;
YUV420Player* remote_player = nullptr;
YUV420Player* mcu_player = nullptr;
// 事件回调函数
int RoomEvent(int iEvent, void* pEventData, int iDataSize, void* pContext)
{
    switch(iEvent) {
        case SMeeting_Func_CallBack:
            // 处理函数结果回调事件，参考(回调 Key:xx)
            break;
        case SMeeting_Event_Disconnected:
            printf("Disconnected\n");
            break;
            
        case SMeeting_Event_Reconnected:
            printf("Reconnected\n");
            break;
            
        case SMeeting_Event_UserEnter:
            printf("User entered\n");
            break;
        //...
    }
    return 0;
}

void RenderEvent(int renderkey, const unsigned char* buf, int w, int h, int label, void* pContext)
{
    if(renderkey == camera_render_key){
        if(camera_player){
            camera_player->render(buf,w,h,label);
        }
    }
    //...
    return 0;
}

int main() {
    // 初始化
    StatusCodeC ret = SMeetingEngine_Init_C();
    if (ret != 0) {
        printf("Init failed: %d\n", ret);
        return -1;
    }

    // 设置事件回调
    SMeetingEngine_setEventHandler(RoomEvent, NULL);
    SMeetingEngine_setRenderHandler(RenderEvent, NULL);


    // 登录
    const char* token = "your_token";
    ret = SMeetingEngine_login(token);
    if (ret != 0) {
        printf("Login failed: %d\n", ret);
        return -1;
    }

    // 等待登录回调...SMeeting_Func_CallBack key:100
    Sleep(1000);

    // 创建会议
    const char* json = "{\"title\":\"测试会议\",\"meeting_type\":1}";
    ret = SMeetingEngine_createRoom(json, strlen(json));
    
    // 等待异步操作完成（实际应用中应有事件循环）
    Sleep(30000);

    // 清理
    SMeetingEngine_logout();
    
    // 配置参数
    SMeetingEngine_setStream_model(1);
    SMeetingEngine_setStat_interval(10000);

    const char* no ="111222333";
    const char* name = "yjl";
    SMeetingEngine_enterRoom(no,name,"");
    return 0;
}
```

---

## 回调事件参考

### 连接状态事件

| 事件常量 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_Disconnected | 1 | 断开连接 |
| SMeeting_Event_Reconnected | 2 | 重连成功 |
| SMeeting_Event_Reconnecting | 3 | 重连中 |

### 用户事件

| 事件常量 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_UserEnter | 100 | 用户进入 |
| SMeeting_Event_UserExit | 101 | 用户离开 |
| SMeeting_Event_UserCameraStateChanged | 102 | 摄像头状态变化 |
| SMeeting_Event_UserAudioStateChanged | 103 | 音频状态变化 |
| SMeeting_Event_UserNameChanged | 104 | 名称变化 |

### 房间事件

| 事件常量 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_RoomChatMessage | 208 | 聊天消息 |
| SMeeting_Event_RoomShareStart | 206 | 共享开始 |
| SMeeting_Event_RoomShareStop | 207 | 共享停止 |

更多事件常量请参考 [C API 参考](/zh/meeting/windows/api-reference/smeeting-c)。

---

## 注意事项

2. **回调异步**：大多数 API 都是异步返回结果，需要通过回调函数处理
3. **线程安全**：回调函数可能在不同线程调用，注意线程安全
4. **初始化顺序**：必须先调用 `SMeetingEngine_Init_C()` 才能使用其他接口
5. **UTF-8 编码**：所有字符串参数使用 UTF-8 编码
