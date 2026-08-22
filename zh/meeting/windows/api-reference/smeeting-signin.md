---
title: "签到接口"
description: "Windows SMeeting SDK 签到 C++ 接口参考"
---

以下接口均在 [ISMeetingChannel](smeeting-channel) 上调用。

---

## 签到列表
```cpp
virtual StatusCode signinList(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

## 创建签到
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

## 签到统计
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

## 结束签到
```cpp
virtual StatusCode signinFinish(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

## 签到详情
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

## 签到
```cpp
virtual StatusCode signinSign(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

## 导出签到详情
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
