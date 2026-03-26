---
title: "C++ API 参考"
description: "Windows SMeeting 会议 SDK C++ 接口完整参考"
---

# C++ API 参考

本文档提供 Windows SMeeting SDK C++ 接口的完整参考。所有接口定义在 `SMeeting.h` 头文件中。

## 初始化与基础接口

### 初始化引擎
```cpp
SMEETING_API StatusCode SMEETING_CALL SMeetingEngine_Init(ISMeetingEngine** meet);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meet | ISMeetingEngine** | 输出的引擎对象指针 |

**返回值**

`StatusCode` - 错误码

### 获取 SDK 版本
```cpp
SMEETING_API StatusCode SMEETING_CALL SMeetingEngine_Version(std::string& s);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | std::string& | 输出版本信息字符串 |

**返回值**

`StatusCode` - 错误码

### 获取错误码描述
```cpp
SMEETING_API void SMEETING_CALL SMeetingEngine_GetStatusMsg(StatusCode code, char* msg);
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | StatusCode | 错误码 |
| msg | char* | 输出错误描述缓冲区 |

---

## ISMeetingEngine 接口

### 获取配置对象
```cpp
virtual StatusCode getSetting(ISMeetingSetting** sett) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sett | ISMeetingSetting** | 输出配置对象指针 |

**返回值**

`StatusCode` - 错误码

### 设置事件回调
```cpp
virtual StatusCode setEventHandler(ISMeetingEngineEvent* e) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| e | ISMeetingEngineEvent* | 事件回调对象 |

**返回值**

`StatusCode` - 错误码

---

## 登录登出接口

### 用户登录
```cpp
virtual StatusCode login(std::string token, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| token | std::string | 登录凭证 token |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 用户登出
```cpp
virtual StatusCode logout(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 获取自身信息
```cpp
virtual StatusCode getSelf(Callback back) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 获取设备列表
```cpp
virtual StatusCode listAgent(std::vector<int> type, int page, std::string find_key = "", Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| type | `std::vector<int>` | 设备类型列表 |
| page | int | 页码 |
| find_key | std::string | 搜索关键词 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

---

## 会议室管理接口

### 更新房间信息
```cpp
virtual StatusCode updateRoom(SMeetingCreateMeetingModel model, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| model | SMeetingCreateMeetingModel | 房间配置模型 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 获取进行中的会议
```cpp
virtual StatusCode attendeeRoom(int page, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| page | int | 页码 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 获取历史会议
```cpp
virtual StatusCode attendedRoom(int page, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| page | int | 页码 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 获取会议详情
```cpp
virtual StatusCode detailRoom(std::string meeting_id, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meeting_id | std::string | 会议 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 取消会议
```cpp
virtual StatusCode cancelRoom(std::string meeting_id, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meeting_id | std::string | 会议 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 获取会议成员列表
```cpp
virtual StatusCode participantRoom(std::string meeting_id, int page, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meeting_id | std::string | 会议 ID |
| page | int | 页码 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 创建会议
```cpp
virtual StatusCode createRoom(SMeetingCreateMeetingModel model, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| model | SMeetingCreateMeetingModel | 房间配置模型 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新背景与附件
```cpp
virtual StatusCode updateBgAndAttach(std::string meeting_id, std::string background, std::vector<SMeetingMeetingAttachments>, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meeting_id | std::string | 会议 ID |
| background | std::string | 背景 URL |
| attachments | `std::vector<SMeetingMeetingAttachments>` | 附件列表 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 加入房间
```cpp
virtual StatusCode enterRoom(std::string roomno, std::string name, std::string pass = "", Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| roomno | std::string | 房间号 |
| name | std::string | 用户昵称 |
| pass | std::string | 会议密码 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 通过会议 ID 加入
```cpp
virtual StatusCode enterRoomByMeetingId(std::string roomno, std::string name, std::string pass = "", Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| roomno | std::string | 会议 ID |
| name | std::string | 用户昵称 |
| pass | std::string | 会议密码 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 离开房间
```cpp
virtual StatusCode exitRoom(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 离开等候室
```cpp
virtual StatusCode exitWaitRoom(std::string roomno, std::string meeting_id, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| roomno | std::string | 房间号 |
| meeting_id | std::string | 会议 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

---

## 主持人管理接口

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

## 等候室接口

### 更新等候室状态
```cpp
virtual StatusCode adminUpdateWaitRoomState(bool v, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| v | bool | 等候室状态 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 获取等候室用户列表
```cpp
virtual StatusCode adminWaitRoomUsers(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 移入等候室
```cpp
virtual StatusCode adminMoveInWaitRoom(std::string uid, std::string name, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| name | std::string | 用户名称 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 移出等候室
```cpp
virtual StatusCode adminMoveOutWaitRoom(std::string uid, std::string name, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| name | std::string | 用户名称 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

---

## 用户操作接口

### 更新自身名称
```cpp
virtual StatusCode updateName(std::string name, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| name | std::string | 新名称 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 发送聊天消息
```cpp
virtual StatusCode sendRoomChatMessage(int tp, std::string msg, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| tp | int | 消息类型 |
| msg | std::string | 消息内容 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 发送自定义消息
```cpp
virtual StatusCode sendRoomCustomMessage(std::string, std::string, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| 第一个参数 | std::string | 消息键 |
| 第二个参数 | std::string | 消息内容 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 请求举手
```cpp
virtual StatusCode requestHandup(int code, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | int | 举手类型代码 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 取消举手
```cpp
virtual StatusCode cancelHandup(int code, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | int | 举手类型代码 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 获取在线成员列表
```cpp
virtual StatusCode listOnlineMember(std::string _meetid, Callback back = nullptr) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| _meetid | std::string | 会议 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

---

## 分组会议接口

### 创建分组会议
```cpp
virtual StatusCode createSubMeeting(std::string par_meet_id, std::vector<std::string> title, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| par_meet_id | std::string | 主会议 ID |
| title | `std::vector<std::string>` | 分组标题列表 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新分组会议标题
```cpp
virtual StatusCode updateSubMeetingTitle(std::string sub_id, std::string newTitle, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sub_id | std::string | 分组 ID |
| newTitle | std::string | 新标题 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 更新分组会议用户
```cpp
virtual StatusCode updateSubMeetingUsers(std::string sub_id, std::vector<SMeetingMeetingAttachments> users, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sub_id | std::string | 分组 ID |
| users | `std::vector<SMeetingMeetingAttachments>` | 用户列表 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 删除分组会议
```cpp
virtual StatusCode deleteSubMeeting(std::vector<std::string> sub_id, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sub_id | `std::vector<std::string>` | 分组 ID 列表 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 获取分组会议列表
```cpp
virtual StatusCode getSubMeetingList(std::string meet_id, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meet_id | std::string | 会议 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 启动分组会议
```cpp
virtual StatusCode startSubMeeting(std::vector<std::string> sub_id, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sub_id | `std::vector<std::string>` | 分组 ID 列表 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 停止分组会议
```cpp
virtual StatusCode stopSubMeeting(std::vector<std::string> sub_id, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sub_id | `std::vector<std::string>` | 分组 ID 列表 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 移动分组会议用户
```cpp
virtual StatusCode moveSubMeetingUser(std::string uid, std::string src_sub_id, std::string des_sub_id, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| src_sub_id | std::string | 源分组 ID |
| des_sub_id | std::string | 目标分组 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 请求帮助
```cpp
virtual StatusCode helpSubMeeting(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

---

## MCU 接口

### 启动 MCU
```cpp
virtual StatusCode mcuStart(std::string laydata, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| laydata | std::string | 布局数据 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 停止 MCU
```cpp
virtual StatusCode mcuStop(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### MCU 录制配置
```cpp
virtual StatusCode mcuRecordConfig(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### MCU 录制详情
```cpp
virtual StatusCode mcuRecordDetail(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

---

## 房间信息接口

### 获取自身信息
```cpp
virtual StatusCode getMe(std::string& s) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | std::string& | 输出自身信息 JSON 字符串 |

**返回值**

`StatusCode` - 错误码

### 获取房间信息
```cpp
virtual StatusCode getRoom(std::string& s) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | std::string& | 输出房间信息 JSON 字符串 |

**返回值**

`StatusCode` - 错误码

### 获取所有成员信息
```cpp
virtual StatusCode getMembers(std::string& s) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | std::string& | 输出成员信息 JSON 字符串 |

**返回值**

`StatusCode` - 错误码

### 获取指定成员信息
```cpp
virtual StatusCode getMember(std::string uid, std::string& s) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | std::string | 用户 ID |
| s | std::string& | 输出成员信息 JSON 字符串 |

**返回值**

`StatusCode` - 错误码

### 获取扩展信息
```cpp
virtual StatusCode getOpt(std::string& opt) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| opt | std::string& | 输出扩展信息 JSON 字符串 |

**返回值**

`StatusCode` - 错误码

---

## 设备枚举接口

### 获取视频设备列表
```cpp
virtual StatusCode getEnumVideo(std::string& dev) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| dev | std::string& | 输出视频设备 JSON 字符串 |

**返回值**

`StatusCode` - 错误码

### 获取屏幕设备列表
```cpp
virtual StatusCode getEnumScreen(std::string& dev) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| dev | std::string& | 输出屏幕设备 JSON 字符串 |

**返回值**

`StatusCode` - 错误码

### 获取音频设备列表
```cpp
virtual StatusCode getEnumAudio(std::string& dev) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| dev | std::string& | 输出音频设备 JSON 字符串 |

**返回值**

`StatusCode` - 错误码

### 获取扬声器设备列表
```cpp
virtual StatusCode getEnumSpeaker(std::string& dev) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| dev | std::string& | 输出扬声器设备 JSON 字符串 |

**返回值**

`StatusCode` - 错误码

---

## 本地媒体流接口

### 获取本地麦克风对象
```cpp
virtual StatusCode getLocalMic(IMEETLocalMic**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| 返回值 | IMEETLocalMic** | 本地麦克风对象指针 |

**返回值**

`StatusCode` - 错误码

### 获取本地摄像头对象
```cpp
virtual StatusCode getLocalCamera(IMEETLocalCamera**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| 返回值 | IMEETLocalCamera** | 本地摄像头对象指针 |

**返回值**

`StatusCode` - 错误码

### 获取本地屏幕共享对象
```cpp
virtual StatusCode getLocalScreen(IMEETLocalScreen**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| 返回值 | IMEETLocalScreen** | 本地屏幕共享对象指针 |

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
| 返回值 | IMEETRemoteVideo** | 远端视频对象指针 |

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
| 返回值 | IMEETRemoteAudio** | 远端音频对象指针 |

**返回值**

`StatusCode` - 错误码

### 获取 MCU 视频对象
```cpp
virtual StatusCode getMcuVideo(IMEETRemoteVideo**) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| 返回值 | IMEETRemoteVideo** | MCU 视频对象指针 |

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
| 返回值 | IMeetCustomVideoTrack** | 自定义视频轨道对象指针 |

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
| 返回值 | IMeetCustomAudioTrack** | 自定义音频轨道对象指针 |

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

## 本地录制接口

### 获取本地录制对象
```cpp
virtual StatusCode getLocalRecord(std::string mid, IMEETRecord** e) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| mid | std::string | 会议 ID |
| e | IMEETRecord** | 录制对象指针 |

**返回值**

`StatusCode` - 错误码

---

## 日志接口

### 上传日志
```cpp
virtual StatusCode addUploadLog(const char* type, const char* msg) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| type | const char* | 日志类型 |
| msg | const char* | 日志内容 |

**返回值**

`StatusCode` - 错误码

---

## IM 接口

### 启用 IM
```cpp
virtual StatusCode enableIm(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 禁用 IM
```cpp
virtual void disableIm(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

---

## 云存储接口

### 预签名上传
```cpp
virtual StatusCode presignedPutObject(std::string type, std::string meeting_id, std::string ext, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| type | std::string | 文件类型 |
| meeting_id | std::string | 会议 ID |
| ext | std::string | 文件扩展名 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 预签名下载
```cpp
virtual StatusCode presignedGetObject(std::string id, std::string res_key, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | std::string | 资源 ID |
| res_key | std::string | 资源键 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

---

## 资源管理接口

### 资源列表
```cpp
virtual StatusCode resourcesList(std::string parent_id, std::string meeting_id, std::string res_name, int page, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| parent_id | std::string | 父资源 ID |
| meeting_id | std::string | 会议 ID |
| res_name | std::string | 资源名称 |
| page | int | 页码 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 创建资源
```cpp
virtual StatusCode resourcesCreate(SMeetingResourcesModel* mode, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| mode | SMeetingResourcesModel* | 资源模型 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 重命名资源
```cpp
virtual StatusCode resourcesRename(std::string id, std::string res_key, std::string res_name, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | std::string | 资源 ID |
| res_key | std::string | 资源键 |
| res_name | std::string | 新资源名称 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 移动资源
```cpp
virtual StatusCode resourcesMoveto(std::string id, std::string res_key, std::string parent_id, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | std::string | 资源 ID |
| res_key | std::string | 资源键 |
| parent_id | std::string | 目标父资源 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 删除资源
```cpp
virtual StatusCode resourcesRemove(std::string id, std::string res_key, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | std::string | 资源 ID |
| res_key | std::string | 资源键 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 设置会议背景
```cpp
virtual StatusCode resourcesMeetingBg(std::string id, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | std::string | 资源 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

---

## 签到接口

### 签到列表
```cpp
virtual StatusCode signinList(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 创建签到
```cpp
virtual StatusCode signinCreate(int dt, std::string desc, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| dt | int | 签到时长 |
| desc | std::string | 签到描述 |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 签到统计
```cpp
virtual StatusCode signinCount(std::string, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| 参数 | std::string | 签到 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 结束签到
```cpp
virtual StatusCode signinFinish(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 签到详情
```cpp
virtual StatusCode signinDetail(std::string id, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | std::string | 签到 ID |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 签到
```cpp
virtual StatusCode signinSign(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 导出签到详情
```cpp
virtual StatusCode signinExportDetail(std::string epoch, std::string outFile) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| epoch | std::string | 时间戳 |
| outFile | std::string | 输出文件路径 |

**返回值**

`StatusCode` - 错误码

---

## 释放接口

### 释放引擎
```cpp
virtual void del() = 0;
```

---

## ISMeetingSetting 接口

配置项设置和获取接口：

| 配置项 | 设置方法 | 获取方法 | 类型 |
| --- | --- | --- | --- |
| 流模式 | set_stream_model | get_stream_model | int |
| SDK 日志路径 | set_sdk_log_path | get_sdk_log_path | std::string |
| 统计间隔 | set_stat_interval | get_stat_interval | int |
| 发言者间隔 | set_speaker_interval | get_speaker_interval | int |
| 启用流日志 | set_enable_stream_log | get_enable_stream_log | int |
| 启用音频录制 | set_enable_audio_record | get_enable_audio_record | int |
| MCU 轨道 | set_mcu_track | get_mcu_track | int |
| 降噪模式 | set_den_model | get_den_model | int |
| 限速 | set_limit_speed | get_limit_speed | int |

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

---

## 事件回调接口 ISMeetingEngineEvent

### 连接状态事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onDisconnected | DisconnectReason, StatusCode, std::string | 断开连接 |
| onReconnected | - | 重连成功 |
| onReconnecting | - | 重连中 |

### 用户事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onUserEnter | roomno, userdata | 用户进入 |
| onUserExit | roomno, userdata, reason | 用户离开 |
| onUserCameraStateChanged | roomno, uid, newstate, by_admin, op_uid | 用户摄像头状态变化 |
| onUserAudioStateChanged | roomno, uid, newstate, by_admin, op_uid | 用户音频状态变化 |
| onUserNameChanged | roomno, uid, newname, by_admin, op_uid | 用户名称变化 |
| onUserRoleChanged | roomno, uid, newrole, by_admin, op_uid | 用户角色变化 |
| onUserChatDisabledChanged | roomno, uid, newstate, by_admin, op_uid | 用户聊天权限变化 |
| onUserHandup | roomno, uid, tp, step | 用户举手 |

### 房间事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onRoomCameraStateChanged | roomno, uid, self_unmute_camera_disabled, camera_disabled | 房间摄像头状态 |
| onRoomMicStateChanged | roomno, uid, self_unmute_mic_disabled, mic_disabled | 房间麦克风状态 |
| onRoomChatDisabledChanged | roomno, uid, newstatus | 房间聊天状态 |
| onRoomScreenshotDisabledChanged | roomno, uid, newstatus | 房间截屏状态 |
| onRoomWaterMarkDisabledChanged | roomno, uid, newstatus | 房间水印状态 |
| onRoomLockChanged | roomno, lock | 房间锁定状态 |
| onRoomShareStart | roomno, uid, st | 共享开始 |
| onRoomShareStop | roomno, uid, st, by_admin, op_uid | 共享停止 |
| onRoomChatMessage | roomno, uid, pri, msg_type, msg | 聊天消息 |
| onRoomCustomMessage | roomno, uid, pri, msg | 自定义消息 |
| onRoomMcuTaskChange | roomno, task_type, task_status | MCU 任务变化 |
| onRoomShareStateChange | roomno, share_state | 共享状态变化 |
| onRoomWaitRoomStateChange | roomno, new_st | 等候室状态变化 |

### 主持人控制事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onAdminRequestOpenMic | roomno, uid | 请求打开麦克风 |
| onAdminRequestOpenCamera | roomno, uid | 请求打开摄像头 |
| onAdminUpdateName | roomno, uid, name | 更新名称 |
| onAdminConfirmHandup | roomno, code, approve | 确认举手 |
| onAdminMoveInWaitRoom | - | 移入等候室 |
| onAdminWaitRoomEnterRoomFinish | code, msg | 进入房间完成 |

### 设备事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onDeviceChange | tp, isadd, name | 设备变化 |
| onDefDeviceChange | tp, name | 默认设备变化 |
| onDeviceStatusChange | tp, status | 设备状态变化 |
| onShareTargetNotFind | - | 未找到共享目标 |

### 流媒体事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onStreamUpLevel | level | 上行网络质量 |
| onStreamDownLevel | uid, level | 下行网络质量 |
| onStreamUpStat | upstat | 上行统计 |
| onStreamDownStat | downstat | 下行统计 |
| onStreamSpeakers | Speakers | 发言者列表 |
| onFrameTimeOut | uid, track_id, track_desc, loading | 帧超时 |
| onStreamProbeResult | step, result | 探测结果 |

### IM 事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onImEnabled | uid, sid | IM 启用 |
| onImDisconnected | reason, code, message | IM 断开 |
| onImReconnected | - | IM 重连成功 |
| onImReconnecting | - | IM 重连中 |
| onImCallMessage | uid, name, content | 呼叫消息 |
| onMeetingStartMessage | content | 会议开始消息 |

### 签到事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onSigninActivity | name, desc, enddt | 签到活动 |
| onSigninFinish | name | 签到完成 |
| onWaitRoomMemberEnter | uid, name | 等候室成员进入 |
| onWaitRoomMemberLeave | uid, name | 等候室成员离开 |

### 录制事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onRecordStatusChange | k, status, msg | 录制状态变化 |

### 分组会议事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onAdminStartSubMeeting | meeting_id, title, users | 启动分组会议 |
| onAdminStopSubMeeting | parent_meeting_id | 停止分组会议 |
| onAdminMoveSubMeetingUser | to_meeting_title, to_meeting_id | 移动分组用户 |
| onUserHelpSubMeeting | meeting_id, title, parent | 请求帮助 |

---

## 枚举类型

### StatusCode

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 0 | OK | 成功 |
| 100001 | SystemError | 系统错误 |
| 100002 | NotInitialized | 未初始化 |
| 100003 | MediaNotInitialized | 媒体未初始化 |
| 100004 | ProtocolParsingError | 协议解析错误 |
| 100005 | Timeout | 超时 |
| 100006 | InvalidArgs | 参数无效 |
| 100007 | Conflict | 冲突 |
| 100008 | SdkTokenInvalid | Token 无效 |
| 100009 | NetError | 网络错误 |
| 100010 | MediaNetError | 媒体网络错误 |
| 100011 | NotFound | 未找到 |
| 101000 | SDKFail | SDK 失败 |
| 101001 | DeviceFail | 设备失败 |
| 101002 | DeviceNoFind | 设备未找到 |
| 101003 | UserNotFound | 用户未找到 |
| 101004 | NotDevPrivate | 无设备权限 |
| 101005 | InvalidOperation | 无效操作 |
| 101006 | NotSupport | 不支持 |
| 101007 | DealBeQuick | 操作过快 |
| 101008 | MoudelNotSupport | 模式不支持 |
| 101009 | BeforeSetting | 需要先设置 |
| 101100 | ChannelJoinError | 频道加入错误 |
| 101101 | ChannelJoinTimeOut | 频道加入超时 |
| 101200 | StreamJoinError | 流加入错误 |
| 101201 | StreamJoinConflict | 流加入冲突 |
| 101202 | VideoCapturerError | 视频采集器错误 |
| 101203 | NotFindStreamTrack | 未找到流轨道 |
| 101204 | ExceedingSpecifiedQuantity | 超出指定数量 |
| 201000 | SDKMeetingFail | SDK 会议失败 |
| 201001 | MeetingStatusReject | 会议状态拒绝 |
| 201002 | MeetingHostFail | 主持人失败 |

### DisconnectReason

| 值 | 名称 | 说明 |
| --- | --- | --- |
| -1 | Error | 错误 |
| 1 | Self | 主动离开 |
| 2 | Kicked | 被踢出 |
| 3 | Replace | 被替换 |
| 4 | Timeout | 超时离开 |
| 5 | Destroy | 被销毁 |

### ChatMsgType

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | Text | 文本 |
| 2 | File | 文件 |
| 3 | Pic | 图片 |
| 4 | Sound | 声音 |

### HandupType

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | Mic | 举手麦克风 |
| 2 | Camera | 举手摄像头 |
| 3 | Chat | 举手聊天 |

### UserHandupStep

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | Request | 请求 |
| 2 | Cancel | 取消 |
| 3 | ConfirmOpen | 确认打开 |
| 4 | RejectOpen | 拒绝打开 |

### CameraState

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | On | 开启 |
| 2 | Off | 关闭 |

### MicState

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | On | 开启 |
| 2 | Off | 关闭 |

### ShareType

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 0 | Normal | 普通 |
| 1 | Screen | 屏幕 |
| 2 | WhiteBoard | 白板 |

### Role

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 0 | Member | 普通成员 |
| 1 | Host | 主持人 |
| 2 | CoHost | 联合主持人 |

### DeviceType

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | Mic | 麦克风 |
| 2 | Speaker | 扬声器 |
| 3 | Camera | 摄像头 |

### DeviceStatus

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 2 | NoFail | 正常 |
| 1 | Fail | 异常 |

### StreamNetLevel

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 0 | Good | 好 |
| -1 | NotGood | 一般 |
| -2 | Terrible | 差 |
| -3 | Catastrophic | 灾难性 |

---

## 数据结构

### SMeetingCreateMeetingModel

会议室创建模型：

| 字段 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| room_no | std::string | 房间号 | - |
| title | std::string | 会议标题 | - |
| content | std::string | 会议内容 | - |
| password | std::string | 密码 | - |
| meeting_type | int | 会议类型 (1:临时 2:预约) | 1 |
| meeting_mode | int | 会议模式 (1:普通 2:合成 3:培训 4:培训 5:小组) | 1 |
| plan_time | long long | 计划时间 (Unix 时间戳) | 0 |
| plan_dur | int | 计划时长 | 0 |
| conferee | `std::vector<std::string>` | 与会者列表 | - |
| co_host | `std::vector<std::string>` | 联合主持人列表 | - |
| maximum | int | 最大人数 | 0 |
| end_type | int | 结束类型 (0:延长 1:强制结束) | 1 |
| entry_mute_policy | int | 入场静音策略 (1:强制 2:关闭 3:超 6 人静音) | 3 |
| watermark_disabled | bool | 是否禁用水印 | true |
| screenshot_disabled | bool | 是否禁用截屏 | false |
| chat_disabled | bool | 是否禁用聊天 | false |
| auto_record | bool | 是否自动录制 | true |
| attend_type | int | 参会类型 (1:允许 3:禁止) | 1 |
| waiting_room_disabled | bool | 是否禁用等候室 | true |
| enter_before_host_disabled | bool | 是否禁止主持人前进入 | false |
| parent | std::string | 父会议 ID | - |
| extend_info | std::string | 扩展信息 | - |

### SMeetingMeetingAttachments

会议附件：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| name | std::string | 名称 |
| key | std::string | 键 |

### SMeetingResourcesModel

资源模型：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| meeting_id | std::string | 会议 ID |
| parent_id | std::string | 父资源 ID |
| res_type | std::string | 资源类型 |
| res_key | std::string | 资源键 |
| res_name | std::string | 资源名称 |

### CustomPublishTrack

自定义发布轨道：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| desc | std::string | 描述 |
| width | int | 宽度 |
| height | int | 高度 |
| fps | int | 帧率 |
| bitrate | int | 比特率 |
| encode | int | 编码 |
