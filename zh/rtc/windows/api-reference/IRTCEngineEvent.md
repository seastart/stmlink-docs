---
title: "IRTCEngineEvent"
description: "引擎级事件回调接口：设备变化、网络探测与 IM 相关通知"
---

## 函数说明
引擎级事件回调接口，继承此接口并重写回调方法，通过 [IRTCEngine::setEventHandler](./IRTCEngine.md#设置消息回调) 注册。

## 继承关系
无

## 回调方法

这里只有**不属于任何单个频道**的回调：设备变化、网络探测、IM。
频道级回调（加入频道、成员进出、流变化、统计、断线重连、录制状态）已经移到
[IRTCChannelEvent](./IRTCChannelEvent.md)，并且去掉了 `channelId` 首参。


以下回调不属于某一个频道，签名保持不变。

### 网络探测结果回调
```cpp
virtual void onProbeResult(int action, const char* result) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| action | int | 探测步骤标识 |
| result | const char* | 探测结果 JSON |

### 设备变化回调
```cpp
virtual void onDeviceChange(int type, int action, const char* name, int namesize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| type | int | 设备类型（1：麦克风，2：扬声器，3：摄像头） |
| action | int | 动作（1：插入，2：拔出） |
| name | const char* | 设备名称 |
| namesize | int | 设备名称长度 |

### 默认设备变化回调
```cpp
virtual void onDefDeviceChange(int type, const char* name, int namesize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| type | int | 设备类型（1：麦克风，2：扬声器） |
| name | const char* | 新默认设备名称 |
| namesize | int | 设备名称长度 |

### IM 启用回调
```cpp
virtual void onImEnabled(const char* uid, const char* sid) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| sid | const char* | 会话 ID |

### IM 断开连接回调
```cpp
virtual void onImDisconnected(int reason, StatusCode code, const char* message, size_t message_size) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| reason | int | 断开原因 |
| code | StatusCode | 错误码 |
| message | const char* | 错误描述信息 |
| message_size | size_t | 错误描述长度 |

### IM 重连成功回调
```cpp
virtual void onImReconnected() = 0;
```

### IM 正在重连回调
```cpp
virtual void onImReconnecting() = 0;
```

### IM 消息回调
```cpp
virtual void onImMessage2(const char* uid, const char* sid, const char* name, int name_size, const char* action, const char* content, size_t content_size) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 发送者用户 ID |
| sid | const char* | 会话 ID |
| name | const char* | 发送者昵称 |
| name_size | int | 昵称长度 |
| action | const char* | 消息类型/动作 |
| content | const char* | 消息内容 |
| content_size | size_t | 消息内容长度 |

