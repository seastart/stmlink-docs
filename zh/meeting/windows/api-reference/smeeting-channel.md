---
title: "ISMeetingChannel 会议接口"
description: "Windows SMeeting SDK 会议级 C++ 接口参考"
---

`ISMeetingChannel` 代表一个会议对象，由 `ISMeetingEngine::createChannel()` 或 `createChannelByMeetingId()` 创建，通过 `ISMeetingEngine::leaveChannel()` 销毁。

---

## 频道基础接口

### 获取频道 ID
```cpp
virtual std::string getChannelId() = 0;
```

返回创建频道时传入的房间号 / 会议 ID。即使中途因等候室切换为按会议 ID 入会，该 ID 也不变，是 `leaveChannel()` 回收对象的 key。

### 获取频道配置对象
```cpp
virtual StatusCode getSetting(ISMeetingChannelSetting** sett) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sett | ISMeetingChannelSetting** | 输出配置对象指针 |

**返回值**

`StatusCode` - 错误码

### 设置频道事件回调
```cpp
virtual StatusCode setEventHandler(ISMeetingChannelEvent* e) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| e | ISMeetingChannelEvent* | 事件回调对象 |

**返回值**

`StatusCode` - 错误码

> 必须在 `enter()` 之前设置回调，入会过程中的事件（成员列表、摄像头状态等）在 `enter()` 返回前就会发出。

---

## 入会 / 退会接口

### 进入会议
```cpp
virtual StatusCode enter(std::string pass = "", Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| pass | std::string | 会议密码 |
| back | Callback | 异步回调函数 |

`enter()` 会执行 `/v1/meet/enter` 并加入 rtc 频道。入会昵称、头像、流厂商等需在 `enter()` 前通过 `ISMeetingChannelSetting` 设置。

**返回值**

`StatusCode` - 错误码

### 离开等候室
```cpp
virtual StatusCode exitWaitRoom(Callback back = NULL) = 0;
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
