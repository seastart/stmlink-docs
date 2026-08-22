---
title: "主持人管理接口"
description: "Windows SMeeting SDK 主持人 / 管理员 C++ 接口参考"
---

以下接口均在 [ISMeetingChannel](smeeting-channel) 上调用，仅主持人或具有相应权限的用户可执行。

---

## 房间控制

### 结束会议
```cpp
virtual StatusCode adminDestroyRoom(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新房间名称
```cpp
virtual StatusCode adminUpdateRoomName() = 0;
```

**返回值**

`StatusCode` - 错误码

### 更新房间视频状态
```cpp
virtual StatusCode adminUpdateRoomVideoState() = 0;
```

**返回值**

`StatusCode` - 错误码

### 更新房间音频状态
```cpp
virtual StatusCode adminUpdateRoomAudioState() = 0;
```

**返回值**

`StatusCode` - 错误码

### 更新房间摄像头状态
```cpp
virtual StatusCode adminUpdateRoomCameraState(bool self_unmute_camera_disabled, bool camera_disabled, Callback back = NULL) = 0;
virtual StatusCode adminUpdateRoomCameraState(bool self_unmute_camera_disabled, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| self_unmute_camera_disabled | bool | 是否禁止自行打开摄像头 |
| camera_disabled | bool | 是否禁用摄像头 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新房间麦克风状态
```cpp
virtual StatusCode adminUpdateRoomMicState(bool self_unmute_mic_disabled, bool mic_disabled, Callback back = NULL) = 0;
virtual StatusCode adminUpdateRoomMicState(bool self_unmute_mic_disabled, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| self_unmute_mic_disabled | bool | 是否禁止自行打开麦克风 |
| mic_disabled | bool | 是否禁用麦克风 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新房间聊天状态
```cpp
virtual StatusCode adminUpdateRoomChatDisabled(bool chat_disabled, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| chat_disabled | bool | 是否禁用聊天 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新房间截屏状态
```cpp
virtual StatusCode adminUpdateRoomScreenshotDisabled(bool screenshot_disabled, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| screenshot_disabled | bool | 是否禁用截屏 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新房间 MCU 模式
```cpp
virtual StatusCode adminUpdateRoomMCUMode() = 0;
```

**返回值**

`StatusCode` - 错误码

### 更新房间锁定状态
```cpp
virtual StatusCode adminUpdateRoomLocked(bool locked, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| locked | bool | 是否锁定房间 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 停止房间共享
```cpp
virtual StatusCode adminStopRoomShare(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新房间共享状态
```cpp
virtual StatusCode adminUpdateRoomShareState(bool v, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| v | bool | 共享状态 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新主持人入场前禁用状态
```cpp
virtual StatusCode adminUpdateEnterBeforeHostDisabled(bool v, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| v | bool | 是否禁用主持人入场前进入 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

---

## 用户控制

### 更新用户名称
```cpp
virtual StatusCode adminUpdateUserName(std::string uid, std::string name, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| name | std::string | 新名称 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新用户角色
```cpp
virtual StatusCode adminUpdateUserRole(std::string uid, int role, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| role | int | 角色类型 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新用户聊天权限
```cpp
virtual StatusCode adminUpdateUserChatDisabled(std::string uid, bool chat_disabled, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| chat_disabled | bool | 是否禁用聊天 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 禁用用户摄像头
```cpp
virtual StatusCode adminDisableUserCamera() = 0;
```

**返回值**

`StatusCode` - 错误码

### 禁用用户麦克风
```cpp
virtual StatusCode adminDisableUserMic() = 0;
```

**返回值**

`StatusCode` - 错误码

### 关闭用户摄像头
```cpp
virtual StatusCode adminCloseUserCamera(std::string uid, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 关闭用户麦克风
```cpp
virtual StatusCode adminCloseUserMic(std::string uid, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 请求用户打开摄像头
```cpp
virtual StatusCode adminRequestUserOpenCamera(std::string uid, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 请求用户打开麦克风
```cpp
virtual StatusCode adminRequestUserOpenMic(std::string uid, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 踢出用户
```cpp
virtual StatusCode adminKickUserOut(std::string uid, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 确认举手请求
```cpp
virtual StatusCode adminConfirmHandup(std::string uid, int code, bool approve, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| code | int | 举手类型代码 |
| approve | bool | 是否批准 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 邀请设备入会
```cpp
virtual StatusCode adminInviteAgent(std::string no, int tp, std::vector<std::string> devs, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| no | std::string | 房间号 |
| tp | int | 类型 |
| devs | `std::vector<std::string>` | 设备列表 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新与会者列表
```cpp
virtual StatusCode adminUpdateConferee(std::vector<std::string> conferee, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| conferee | `std::vector<std::string>` | 与会者列表 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新布局
```cpp
virtual StatusCode adminUpdateLayout(std::string layout, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| layout | std::string | 布局配置 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 呼叫用户
```cpp
virtual StatusCode adminCallUsers(std::vector<std::string> users, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| users | `std::vector<std::string>` | 用户列表 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 提醒用户
```cpp
virtual StatusCode adminRemind(std::vector<std::string> users, bool sms, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| users | `std::vector<std::string>` | 用户列表 |
| sms | bool | 是否发送短信 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码
