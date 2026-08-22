---
title: "MCU 接口"
description: "Windows SMeeting SDK MCU 合成视频 C++ 接口参考"
---

以下接口均在 [ISMeetingChannel](smeeting-channel) 上调用。

---

## 启动 MCU
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

## 停止 MCU
```cpp
virtual StatusCode mcuStop(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

## MCU 录制配置
```cpp
virtual StatusCode mcuRecordConfig(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码

## MCU 录制详情
```cpp
virtual StatusCode mcuRecordDetail(Callback back = NULL) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| back | Callback | 异步回调函数 |

**返回值**

`StatusCode` - 错误码
