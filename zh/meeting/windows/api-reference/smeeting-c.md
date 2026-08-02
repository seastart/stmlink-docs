---
title: "C API 参考"
description: "Windows SMeeting 会议 SDK C 接口完整参考"
---

# C API 参考

本文档提供 Windows SMeeting SDK C 接口的完整参考。所有接口定义在 `SMeeting_C.h` 头文件中。

## 初始化与基础接口

### 初始化引擎
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_Init_C();
```

**返回值**

`StatusCodeC` - 错误码

### 获取 SDK 版本
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_Version_C(char* c, int len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| c | char* | 输出版本信息缓冲区 |
| len | int | 缓冲区长度 |

**返回值**

`StatusCodeC` - 错误码

### 获取错误码描述
```c
SMEETING_API_C int SMEETING_CALL_C SMeetingEngine_GetStatusMsg_C(StatusCodeC code, char* msg, int len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | StatusCodeC | 错误码 |
| msg | char* | 错误描述缓冲区 |
| len | int | 缓冲区长度 |

**返回值**

`int` - 实际写入的字符数

---

## 回调类型定义

### 房间事件回调
```c
typedef int(*SMeet_CBF_RoomEvent)(int iEvent, void* pEventData, int iDataSize, void* pContext);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| iEvent | int | 事件类型 |
| pEventData | void* | 事件数据 |
| iDataSize | int | 数据大小 |
| pContext | void* | 用户上下文 |

**返回值**

`int` - 处理结果

### 渲染事件回调
```c
typedef void(*SMeet_RenderEvent)(int renderkey, const unsigned char* buf, int w, int h, int label, void* pContext);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| renderkey | int | 渲染键 |
| buf | const unsigned char* | 帧数据 |
| w | int | 宽度 |
| h | int | 高度 |
| label | int | 标签 |
| pContext | void* | 用户上下文 |

---

## 配置接口

### 设置流模式
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setStream_model(int val);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| val | int | 流模式值 |

**返回值**

`StatusCodeC` - 错误码

### 设置 SDK 日志路径
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setSdk_log_path(const char* path);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| path | const char* | 日志路径 |

**返回值**

`StatusCodeC` - 错误码

### 设置统计间隔
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setStat_interval(int val);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| val | int | 统计间隔（毫秒） |

**返回值**

`StatusCodeC` - 错误码

### 设置发言者间隔
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setSpeaker_interval(int val);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| val | int | 发言者间隔（毫秒） |

**返回值**

`StatusCodeC` - 错误码

### 设置启用流日志
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setEnable_stream_log(int val);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| val | int | 是否启用流日志 |

**返回值**

`StatusCodeC` - 错误码

### 设置启用音频录制
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setEnable_audio_record(int val);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| val | int | 是否启用音频录制 |

**返回值**

`StatusCodeC` - 错误码

### 设置 MCU 轨道
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setMcu_track(int val);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| val | int | MCU 轨道模式 |

**返回值**

`StatusCodeC` - 错误码

### 设置降噪模式
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setDen_model(int val);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| val | int | 降噪模式 |

**返回值**

`StatusCodeC` - 错误码

### 设置限速
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setLimit_speed(int val);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| val | int | 限速值 |

**返回值**

`StatusCodeC` - 错误码

---

## 事件回调接口

### 设置事件回调
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setEventHandler(SMeet_CBF_RoomEvent e, void* t);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| e | SMeet_CBF_RoomEvent | 事件回调函数 |
| t | void* | 用户上下文 |

**返回值**

`StatusCodeC` - 错误码

### 设置渲染回调
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setRenderHandler(SMeet_RenderEvent e, void* t);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| e | SMeet_RenderEvent | 渲染回调函数 |
| t | void* | 用户上下文 |

**返回值**

`StatusCodeC` - 错误码

---

## 登录登出接口

### 用户登录
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_login(const char* token);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| token | const char* | 登录凭证 token |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 100

### 用户登出
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_logout();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 101

### 获取自身信息
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getSelf();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 102

### 获取设备列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_listAgent(char* types, int page, const char* find_key);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| types | char* | 设备类型字符串 |
| page | int | 页码 |
| find_key | const char* | 搜索关键词 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 103

---

## 会议室管理接口

### 更新房间信息
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_updateRoom(const char* json, int json_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| json | const char* | 房间配置 JSON |
| json_len | int | JSON 长度 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 104

### 获取进行中的会议
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_attendeeRoom(int page);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| page | int | 页码 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 105

### 获取历史会议
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_attendedRoom(int page);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| page | int | 页码 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 106

### 获取会议详情
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_detailRoom(const char* meeting_id);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meeting_id | const char* | 会议 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 107

### 取消会议
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_cancelRoom(const char* meeting_id);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meeting_id | const char* | 会议 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 108

### 获取会议成员列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_participantRoom(const char* meeting_id, int page);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meeting_id | const char* | 会议 ID |
| page | int | 页码 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 109

### 创建会议
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_createRoom(const char* json, int json_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| json | const char* | 房间配置 JSON |
| json_len | int | JSON 长度 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 110

### 更新背景与附件
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_updateBgAndAttach(const char* meeting_id, const char* bg, const char* users_json, int json_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meeting_id | const char* | 会议 ID |
| bg | const char* | 背景 URL |
| users_json | const char* | 用户附件 JSON |
| json_len | int | JSON 长度 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 111

### 加入房间
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_enterRoom(const char* roomno, const char* name, const char* pass);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| roomno | const char* | 房间号 |
| name | const char* | 用户昵称 |
| pass | const char* | 会议密码 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 112

### 通过会议 ID 加入
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_byMeetingId(const char* meetingid, const char* name, const char* pass);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meetingid | const char* | 会议 ID |
| name | const char* | 用户昵称 |
| pass | const char* | 会议密码 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 113

### 离开房间
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_exitRoom();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 114

### 离开等候室
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_exitWaitRoom(const char* roomno, const char* meeting_id);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| roomno | const char* | 房间号 |
| meeting_id | const char* | 会议 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 115

---

## 主持人管理接口

### 结束会议
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminDestroyRoom();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 200

### 更新房间名称
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomName();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 201

### 更新房间视频状态
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomVideoState();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 202

### 更新房间音频状态
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomAudioState();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 203

### 更新房间摄像头状态（单参数）
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomCameraState(bool self_unmute_camera_disabled);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| self_unmute_camera_disabled | bool | 是否禁止自行打开摄像头 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 204

### 更新房间摄像头状态（双参数）
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomCameraState2(bool self_unmute_camera_disabled, bool camera_disabled);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| self_unmute_camera_disabled | bool | 是否禁止自行打开摄像头 |
| camera_disabled | bool | 是否禁用摄像头 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 205

### 更新房间麦克风状态（单参数）
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomMicState(bool self_unmute_mic_disabled);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| self_unmute_mic_disabled | bool | 是否禁止自行打开麦克风 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 206

### 更新房间麦克风状态（双参数）
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomMicState2(bool self_unmute_mic_disabled, bool mic_disabled);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| self_unmute_mic_disabled | bool | 是否禁止自行打开麦克风 |
| mic_disabled | bool | 是否禁用麦克风 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 207

### 更新房间聊天状态
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomChatDisabled(bool chat_disabled);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| chat_disabled | bool | 是否禁用聊天 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 208

### 更新房间截屏状态
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomScreenshotDisabled(bool screenshot_disabled);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| screenshot_disabled | bool | 是否禁用截屏 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 209

### 更新房间 MCU 模式
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomMCUMode();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 210

### 更新房间锁定状态
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomLocked(bool locked);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| locked | bool | 是否锁定房间 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 211

### 停止房间共享
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminStopRoomShare();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 212

### 更新用户名称
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| name | const char* | 新名称 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 213

### 更新用户角色
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserRole(const char* uid, int role);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| role | int | 角色类型 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 214

### 更新用户聊天权限
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserChatDisabled(const char* uid, bool chat_disabled);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| chat_disabled | bool | 是否禁用聊天 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 215

### 禁用用户摄像头
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminDisableUserCamera();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 216

### 禁用用户麦克风
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminDisableUserMic();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 217

### 关闭用户摄像头
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminCloseUserCamera(const char* uid);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 218

### 关闭用户麦克风
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminCloseUserMic(const char* uid);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 219

### 请求用户打开摄像头
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminRequestUserOpenCamera(const char* uid);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 220

### 请求用户打开麦克风
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminRequestUserOpenMic(const char* uid);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 221

### 踢出用户
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminKickUserOut(const char* uid);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 222

### 确认举手请求
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminConfirmHandup(const char* uid, int code, bool approve);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| code | int | 举手类型代码 |
| approve | bool | 是否批准 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 223

### 邀请设备入会
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminInviteAgent(const char* no, int tp, const char* devs);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| no | const char* | 房间号 |
| tp | int | 类型 |
| devs | const char* | 设备列表（竖线分隔） |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 224

### 更新与会者列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateConferee(const char* conferee);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| conferee | const char* | 与会者列表（竖线分隔） |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 225

### 更新布局
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateLayout(const char* layout);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| layout | const char* | 布局配置 JSON |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 226

### 呼叫用户
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminCallUsers(const char* users);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| users | const char* | 用户列表（竖线分隔） |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 227

### 更新房间共享状态
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomShareState(bool v);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| v | bool | 共享状态 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 228

### 提醒用户
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminRemind(const char* users, bool sms);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| users | const char* | 用户列表（竖线分隔） |
| sms | bool | 是否发送短信 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 229

### 更新主持人入场前禁用状态
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateEnterBeforeHostDisabled(bool v);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| v | bool | 是否禁用主持人入场前进入 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 230

---

## 等候室接口

### 更新等候室状态
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateWaitRoomState(bool v);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| v | bool | 等候室状态 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 300

### 获取等候室用户列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminWaitRoomUsers();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 301

### 移入等候室
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminMoveInWaitRoom(const char* uid, const char* name);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| name | const char* | 用户名称 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 302

### 移出等候室
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminMoveOutWaitRoom(const char* uid, const char* name);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| name | const char* | 用户名称 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 303

---

## 用户操作接口

### 更新自身名称
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_updateName(const char* name);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| name | const char* | 新名称 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 301

### 发送聊天消息
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_sendRoomChatMessage(int tp, const char* msg);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| tp | int | 消息类型 |
| msg | const char* | 消息内容 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 302

### 发送自定义消息
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_sendRoomCustomMessage(const char* key, const char* msg);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| key | const char* | 消息键 |
| msg | const char* | 消息内容 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 303

### 请求举手
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_requestHandup(int code);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | int | 举手类型代码 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 304

### 取消举手
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_cancelHandup(int code);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | int | 举手类型代码 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 305

---

## 在线成员接口

### 获取在线成员列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_listOnlineMember(const char* meet_id);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meet_id | const char* | 会议 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 500

---

## 分组会议接口

### 创建分组会议
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_createSubMeeting(const char* par_meet_id, const char* title, int title_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| par_meet_id | const char* | 主会议 ID |
| title | const char* | 分组标题（JSON 数组） |
| title_len | int | 标题 JSON 长度 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 600

### 更新分组会议标题
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_updateSubMeetingTitle(const char* sub_id, const char* newTitle);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sub_id | const char* | 分组 ID |
| newTitle | const char* | 新标题 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 601

### 更新分组会议用户
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_updateSubMeetingUsers(const char* sub_id, const char* users_json, int len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sub_id | const char* | 分组 ID |
| users_json | const char* | 用户 JSON |
| len | int | JSON 长度 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 602

### 删除分组会议
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_deleteSubMeeting(const char* sub_ids);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sub_ids | const char* | 分组 ID 列表（JSON 数组） |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 603

### 获取分组会议列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getSubMeetingList(const char* meet_id);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meet_id | const char* | 会议 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 604

### 启动分组会议
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_startSubMeeting(const char* sub_ids_json);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sub_ids_json | const char* | 分组 ID 列表 JSON |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 605

### 停止分组会议
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_stopSubMeeting(const char* sub_ids_json);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sub_ids_json | const char* | 分组 ID 列表 JSON |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 606

### 移动分组会议用户
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_moveSubMeetingUser(const char* uid, const char* src_sub_id, const char* des_sub_id);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| src_sub_id | const char* | 源分组 ID |
| des_sub_id | const char* | 目标分组 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 607

### 请求帮助
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_helpSubMeeting();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 608

---

## MCU 接口

### 启动 MCU
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_mcuStart(const char* laydata);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| laydata | const char* | 布局数据 JSON |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 700

### 停止 MCU
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_mcuStop();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 701

### MCU 录制配置
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_mcuRecordConfig();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 702

### MCU 录制详情
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_mcuRecordDetail();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 703

---

## 本地录制接口

### 设置录制文件名
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setRecordFileName(const char* filepath, int filepath_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| filepath | const char* | 文件路径 |
| filepath_len | int | 路径长度 |

**返回值**

`StatusCodeC` - 错误码

### 设置水印
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setWaterMask(const char* mask, int mask_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| mask | const char* | 水印文本 |
| mask_len | int | 文本长度 |

**返回值**

`StatusCodeC` - 错误码

### 开始录制
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_startRecord();
```

**返回值**

`StatusCodeC` - 错误码

### 设置录制窗口
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setRecordHwnd(void* hwnd, int x, int y, int w, int h);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| hwnd | void* | 窗口句柄 |
| x | int | X 坐标 |
| y | int | Y 坐标 |
| w | int | 宽度 |
| h | int | 高度 |

**返回值**

`StatusCodeC` - 错误码

### 设置录制布局成员视图
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setRecordLayoutMemberView(const char* json, int json_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| json | const char* | 布局配置 JSON |
| json_len | int | JSON 长度 |

**返回值**

`StatusCodeC` - 错误码

### 暂停录制
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_pauseRecord();
```

**返回值**

`StatusCodeC` - 错误码

### 停止录制
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_stopRecord();
```

**返回值**

`StatusCodeC` - 错误码

---

## 房间信息接口

### 获取自身信息
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getMe(char** s, int* s_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | char** | 输出信息缓冲区指针 |
| s_len | int* | 输出信息长度指针 |

**返回值**

`StatusCodeC` - 错误码

### 获取房间信息
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getRoom(char** s, int* s_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | char** | 输出信息缓冲区指针 |
| s_len | int* | 输出信息长度指针 |

**返回值**

`StatusCodeC` - 错误码

### 获取所有成员信息
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getMembers(char** s, int* s_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | char** | 输出信息缓冲区指针 |
| s_len | int* | 输出信息长度指针 |

**返回值**

`StatusCodeC` - 错误码

### 获取指定成员信息
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getMember(const char* uid, char** s, int* s_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| s | char** | 输出信息缓冲区指针 |
| s_len | int* | 输出信息长度指针 |

**返回值**

`StatusCodeC` - 错误码

### 获取扩展信息
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getOpt(char** s, int* s_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | char** | 输出信息缓冲区指针 |
| s_len | int* | 输出信息长度指针 |

**返回值**

`StatusCodeC` - 错误码

---

## 设备枚举接口

### 获取视频设备列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getEnumVideo(char** s, int* s_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | char** | 输出设备列表缓冲区指针 |
| s_len | int* | 输出数据长度指针 |

**返回值**

`StatusCodeC` - 错误码

### 获取屏幕设备列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getEnumScreen(char** s, int* s_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | char** | 输出设备列表缓冲区指针 |
| s_len | int* | 输出数据长度指针 |

**返回值**

`StatusCodeC` - 错误码

### 获取音频设备列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getEnumAudio(char** s, int* s_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | char** | 输出设备列表缓冲区指针 |
| s_len | int* | 输出数据长度指针 |

**返回值**

`StatusCodeC` - 错误码

### 获取扬声器设备列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getEnumSpeaker(char** s, int* s_len);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | char** | 输出设备列表缓冲区指针 |
| s_len | int* | 输出数据长度指针 |

**返回值**

`StatusCodeC` - 错误码

---

## 音频接口

### 请求打开麦克风
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_requestOpenMic();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 800

### 关闭麦克风
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_closeMic();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 801

### 切换麦克风
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_switchMic(const char* devname);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| devname | const char* | 设备名称 |

**返回值**

`StatusCodeC` - 错误码

### 确认打开麦克风
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_confirmOpenMic(bool approve, const char* uid);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| approve | bool | 是否批准 |
| uid | const char* | 用户 ID |

**返回值**

`StatusCodeC` - 错误码

---

## 视频接口

### 切换摄像头
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_switchCamera(const char* name, int w, int h);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| name | const char* | 设备名称 |
| w | int | 宽度 |
| h | int | 高度 |

**返回值**

`StatusCodeC` - 错误码

### 设置摄像头渲染键
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setCameraRenderKey(int key);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| key | int | 渲染键 |

**返回值**

`StatusCodeC` - 错误码

### 请求打开摄像头
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_requestOpenCamera();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 802

### 关闭摄像头
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_closeCamera();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 803

### 确认打开摄像头
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_confirmOpenCamera(bool approve, const char* uid);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| approve | bool | 是否批准 |
| uid | const char* | 用户 ID |

**返回值**

`StatusCodeC` - 错误码

---

## 屏幕共享接口

### 请求共享
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_requestShare(int tp, const char* data);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| tp | int | 共享类型 |
| data | const char* | 共享数据 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 804

### 停止共享
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_stopShare();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 805

---

## 远端媒体接口

### 加载远端视频
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_loadRemoteVideo(const char* uid, const char* track_desc, int renderkey);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| track_desc | const char* | 轨道描述 |
| renderkey | int | 渲染键 |

**返回值**

`StatusCodeC` - 错误码

### 卸载远端视频
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_unloadRemoteVideo(const char* uid, const char* track_desc);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| track_desc | const char* | 轨道描述 |

**返回值**

`StatusCodeC` - 错误码

### 打开扬声器
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_openSpeaker();
```

**返回值**

`StatusCodeC` - 错误码

### 关闭扬声器
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_closeSpeaker();
```

**返回值**

`StatusCodeC` - 错误码

### 切换扬声器
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_switchSpeaker(const char* name);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| name | const char* | 设备名称 |

**返回值**

`StatusCodeC` - 错误码

---

## MCU 视频接口

### 加载 MCU 视频
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_loadMcuVideo(int renderkey);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| renderkey | int | 渲染键 |

**返回值**

`StatusCodeC` - 错误码

### 卸载 MCU 视频
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_unloadMcuVideo();
```

**返回值**

`StatusCodeC` - 错误码

---

## 日志接口

### 上传日志
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_addUploadLog(const char* type, const char* msg);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| type | const char* | 日志类型 |
| msg | const char* | 日志内容 |

**返回值**

`StatusCodeC` - 错误码

---

## IM 接口

### 启用 IM
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_enableIm();
```

**返回值**

`StatusCodeC` - 错误码

### 禁用 IM
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_disableIm();
```

**返回值**

`StatusCodeC` - 错误码

---

## 云存储接口

### 预签名上传
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_presignedPutObject(const char* type, const char* meeting_id, const char* ext);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| type | const char* | 文件类型 |
| meeting_id | const char* | 会议 ID |
| ext | const char* | 文件扩展名 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 900

### 预签名下载
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_presignedGetObject(const char* id, const char* res_key);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | const char* | 资源 ID |
| res_key | const char* | 资源键 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 901

---

## 资源管理接口

### 资源列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_resourcesList(const char* parent_id, const char* meeting_id, const char* res_name, int page);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| parent_id | const char* | 父资源 ID |
| meeting_id | const char* | 会议 ID |
| res_name | const char* | 资源名称 |
| page | int | 页码 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1000

### 创建资源
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_resourcesCreate(const char* resources_json);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| resources_json | const char* | 资源配置 JSON |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1001

### 重命名资源
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_resourcesRename(const char* id, const char* res_key, const char* res_name);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | const char* | 资源 ID |
| res_key | const char* | 资源键 |
| res_name | const char* | 新资源名称 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1002

### 移动资源
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_resourcesMoveto(const char* id, const char* res_key, const char* parent_id);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | const char* | 资源 ID |
| res_key | const char* | 资源键 |
| parent_id | const char* | 目标父资源 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1003

### 删除资源
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_resourcesRemove(const char* id, const char* res_key);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | const char* | 资源 ID |
| res_key | const char* | 资源键 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1004

### 设置会议背景
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_resourcesMeetingBg(const char* id);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | const char* | 资源 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1005

---

## 签到接口

### 签到列表
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_signinList();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1100

### 创建签到
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_signinCreate(int dt, const char* desc);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| dt | int | 签到时长 |
| desc | const char* | 签到描述 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1101

### 签到统计
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_signinCount(const char* id);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | const char* | 签到 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1102

### 结束签到
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_signinFinish();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1103

### 签到详情
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_signinDetail(const char* id);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | const char* | 签到 ID |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1104

### 签到
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_signinSign();
```

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1105

### 导出签到详情
```c
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_signinExportDetail(const char* epoch, const char* outFile);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| epoch | const char* | 时间戳 |
| outFile | const char* | 输出文件路径 |

**返回值**

`StatusCodeC` - 错误码

**回调 Key**: 1106

---

## 事件类型常量

### 连接状态事件

| 常量名 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_Disconnected | 1 | 断开连接 |
| SMeeting_Event_Reconnected | 2 | 重连成功 |
| SMeeting_Event_Reconnecting | 3 | 重连中 |

### 用户事件

| 常量名 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_UserEnter | 100 | 用户进入 |
| SMeeting_Event_UserExit | 101 | 用户离开 |
| SMeeting_Event_UserCameraStateChanged | 102 | 用户摄像头状态变化 |
| SMeeting_Event_UserAudioStateChanged | 103 | 用户音频状态变化 |
| SMeeting_Event_UserNameChanged | 104 | 用户名称变化 |
| SMeeting_Event_UserRoleChanged | 105 | 用户角色变化 |
| SMeeting_Event_UserChatDisabledChanged | 106 | 用户聊天权限变化 |
| SMeeting_Event_UserHandup | 107 | 用户举手 |

### 房间事件

| 常量名 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_RoomCameraStateChanged | 200 | 房间摄像头状态 |
| SMeeting_Event_RoomMicStateChanged | 201 | 房间麦克风状态 |
| SMeeting_Event_RoomChatDisabledChanged | 202 | 房间聊天状态 |
| SMeeting_Event_RoomScreenshotDisabledChanged | 203 | 房间截屏状态 |
| SMeeting_Event_RoomWaterMarkDisabledChanged | 204 | 房间水印状态 |
| SMeeting_Event_RoomLockChanged | 205 | 房间锁定状态 |
| SMeeting_Event_RoomShareStart | 206 | 共享开始 |
| SMeeting_Event_RoomShareStop | 207 | 共享停止 |
| SMeeting_Event_RoomChatMessage | 208 | 聊天消息 |
| SMeeting_Event_RoomCustomMessage | 209 | 自定义消息 |
| SMeeting_Event_RoomMcuTaskChange | 210 | MCU 任务变化 |
| SMeeting_Event_RoomShareStateChange | 211 | 共享状态变化 |
| SMeeting_Event_RoomStateChange | 212 | 房间状态变化 |

### 主持人控制事件

| 常量名 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_AdminConfirmHandup | 300 | 确认举手 |
| SMeeting_Event_AdminRequestOpenMic | 301 | 请求打开麦克风 |
| SMeeting_Event_AdminRequestOpenCamera | 302 | 请求打开摄像头 |
| SMeeting_Event_AdminUpdateName | 303 | 更新名称 |
| SMeeting_Event_AdminMoveInWaitRoom | 304 | 移入等候室 |
| SMeeting_Event_AdminWaitRoomEnterRoomFinish | 305 | 进入房间完成 |

### 设备事件

| 常量名 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_DeviceChange | 400 | 设备变化 |
| SMeeting_Event_DefDeviceChange | 401 | 默认设备变化 |
| SMeeting_Event_DeviceStatusChange | 402 | 设备状态变化 |
| SMeeting_Event_ShareTargetNotFind | 403 | 未找到共享目标 |

### 流媒体事件

| 常量名 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_StreamUpLevel | 500 | 上行网络质量 |
| SMeeting_Event_StreamDownLevel | 501 | 下行网络质量 |
| SMeeting_Event_StreamUpStat | 502 | 上行统计 |
| SMeeting_Event_StreamDownStat | 503 | 下行统计 |
| SMeeting_Event_StreamSpeakers | 504 | 发言者列表 |
| SMeeting_Event_FrameTimeOut | 505 | 帧超时 |
| SMeeting_Event_StreamProbeResult | 506 | 探测结果 |

### IM 事件

| 常量名 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_ImEnabled | 600 | IM 启用 |
| SMeeting_Event_ImDisconnected | 601 | IM 断开 |
| SMeeting_Event_ImReconnected | 602 | IM 重连成功 |
| SMeeting_Event_ImReconnecting | 603 | IM 重连中 |
| SMeeting_Event_ImCallMessage | 604 | 呼叫消息 |
| SMeeting_Event_MeetingStartMessage | 605 | 会议开始消息 |

### 签到事件

| 常量名 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_SigninActivity | 700 | 签到活动 |
| SMeeting_Event_SigninFinish | 701 | 签到完成 |

### 等候室事件

| 常量名 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_WaitRoomMemberEnter | 800 | 等候室成员进入 |
| SMeeting_Event_WaitRoomMemberLeave | 801 | 等候室成员离开 |

### 录制事件

| 常量名 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_RecordStatusChange | 900 | 录制状态变化 |

### 分组会议事件

| 常量名 | 值 | 说明 |
| --- | --- | --- |
| SMeeting_Event_AdminStartSubMeeting | 1000 | 启动分组会议 |
| SMeeting_Event_AdminStopSubMeeting | 1001 | 停止分组会议 |
| SMeeting_Event_AdminMoveSubMeetingUser | 1002 | 移动分组用户 |
| SMeeting_Event_UserHelpSubMeeting | 1003 | 请求帮助 |

---

## 类型定义

### StatusCodeC

```c
typedef int StatusCodeC;
```

错误码类型，与 C++ 的 `StatusCode` 枚举对应。

### 常用错误码

| 值 | 说明 |
| --- | --- |
| 0 | 成功 |
| 100001 | 系统错误 |
| 100002 | 未初始化 |
| 100003 | 媒体未初始化 |
| 100004 | 协议解析错误 |
| 100005 | 超时 |
| 100006 | 参数无效 |
| 100007 | 冲突 |
| 100008 | Token 无效 |
| 100009 | 网络错误 |
| 100010 | 媒体网络错误 |
| 100011 | 未找到 |

---

## 轨道描述常量

| 常量 | 值 | 说明 |
| --- | --- | --- |
| TRACK_DESC_CAMERA_BIG | "camera_big" | 大摄像头轨道 |
| TRACK_DESC_CAMERA_SMALL | "camera_small" | 小摄像头轨道 |
| TRACK_DESC_MIC | "mic" | 麦克风轨道 |
| TRACK_DESC_SCREEN | "screen" | 屏幕共享轨道 |
