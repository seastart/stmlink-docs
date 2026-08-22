---
title: "ISMeetingEngine 引擎接口"
description: "Windows SMeeting SDK 引擎级 C++ 接口参考"
---

`ISMeetingEngine` 是 SDK 引擎对象，负责登录会话、会议管理 HTTP 接口、频道生命周期、设备枚举、IM、资源盘等引擎级能力。

所有会中操作和媒体对象都在 [ISMeetingChannel](smeeting-channel) 中。

---

## 全局函数

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

## 引擎配置与回调

### 获取引擎配置对象
```cpp
virtual StatusCode getSetting(ISMeetingSetting** sett) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| sett | ISMeetingSetting** | 输出配置对象指针 |

**返回值**

`StatusCode` - 错误码

### 设置引擎事件回调
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

---

## 会议频道接口

### 创建频道
```cpp
virtual StatusCode createChannel(std::string roomno, ISMeetingChannel** ch) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| roomno | std::string | 房间号 |
| ch | ISMeetingChannel** | 输出频道对象指针 |

`createChannel` 只创建频道对象，**不会**立即入会。返回后需要通过 `ISMeetingChannel::enter()` 真正入会。

**返回值**

`StatusCode` - 错误码

### 通过会议 ID 创建频道
```cpp
virtual StatusCode createChannelByMeetingId(std::string meetingid, ISMeetingChannel** ch) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| meetingid | std::string | 会议 ID |
| ch | ISMeetingChannel** | 输出频道对象指针 |

**返回值**

`StatusCode` - 错误码

### 离开频道
```cpp
virtual StatusCode leaveChannel(std::string channelId, Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| channelId | std::string | 频道 ID，即 `createChannel` 时传入的房间号 |
| back | Callback | 异步回调函数 |

离开后频道对象会被销毁，不要再使用原来的 `ISMeetingChannel*` 指针。

**返回值**

`StatusCode` - 错误码

### 离开所有频道
```cpp
virtual StatusCode leaveAllChannel(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

### 获取当前频道 ID 列表
```cpp
virtual StatusCode getChannelIds(std::string& s) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| s | std::string& | 输出 JSON 数组形式的频道 ID 列表 |

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

## 日志与 IM 接口

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

## 云存储与资源管理接口

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

## 释放接口

### 释放引擎
```cpp
virtual void del() = 0;
```
