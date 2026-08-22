---
title: "分组会议接口"
description: "Windows SMeeting SDK 分组会议 C++ 接口参考"
---

以下接口均在 [ISMeetingChannel](smeeting-channel) 上调用。

---

## 创建分组会议
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

## 更新分组会议标题
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

## 更新分组会议用户
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

## 删除分组会议
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

## 获取分组会议列表
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

## 启动分组会议
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

## 停止分组会议
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

## 移动分组会议用户
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

## 请求帮助
```cpp
virtual StatusCode helpSubMeeting(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码
