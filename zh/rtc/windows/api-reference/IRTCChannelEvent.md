---
title: "IRTCChannelEvent"
description: "频道级事件回调接口：加入频道、用户进出、流变化、自定义消息、统计与断线重连"
---

## 函数说明
频道级事件回调接口，继承此接口并重写回调方法，通过 [IRTCChannel::setEventHandler](./IRTCChannel.md#设置消息回调) 注册。

## 继承关系
无

## 回调方法

回调是**按频道**注册的，一个 `IRTCChannelEvent` 实例绑定到一个 [IRTCChannel](./IRTCChannel.md)，
因此所有回调都**不带** `channelId` 参数（旧版 `IRTCEngineEvent` 的频道级回调是带的）。
同一个实例可以绑给多个频道，那种情况下需要调用方自己区分。

**必须在 `IRTCChannel::join()` 之前注册**，否则收不到 `onJoinChannel` —— 它是在 `join()` 还没返回时就回调出去的。

### 加入频道成功回调
```cpp
virtual void onJoinChannel(const char* channel, int channelSize, const char* me, int meSize, const char* members, int memberSize, const char* opts, int optSize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| channel | const char* | 频道信息 JSON |
| channelSize | int | 频道信息 JSON 长度 |
| me | const char* | 自身用户信息 JSON |
| meSize | int | 自身用户信息长度 |
| members | const char* | 频道内所有成员信息 JSON 数组 |
| memberSize | int | 成员信息数组长度 |
| opts | const char* | 系统配置参数 |
| optSize | int | 系统配置参数长度 |

注：回调是按频道注册的（`IRTCChannel::setEventHandler`），所以不再回传 `channelId`。需要区分频道时用 `IRTCChannel::getChannelId()`。

### 频道状态更新回调
```cpp
virtual void onChannelUpdate(const char* props, int propsSize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| props | const char* | 频道扩展属性 JSON |
| propsSize | int | 扩展属性字符串长度 |

### 用户加入回调
```cpp
virtual void onUserJoin(const char* user, int userSize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| user | const char* | 加入用户的详细信息 JSON |
| userSize | int | 用户信息字符串长度 |

### 用户信息更新回调
```cpp
virtual void onUserUpdate(const char* user, int userSize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| user | const char* | 更新后的用户信息 JSON |
| userSize | int | 用户信息字符串长度 |

### 用户流添加回调
```cpp
virtual void onUserStreamAdd(const char* user, const char* stream, int streamSize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| user | const char* | 用户 ID |
| stream | const char* | 流信息 JSON |
| streamSize | int | 流信息字符串长度 |

### 用户流更新回调
```cpp
virtual void onUserStreamUpdate(const char* user, const char* stream, int streamSize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| user | const char* | 用户 ID |
| stream | const char* | 更新后的流信息 JSON |
| streamSize | int | 流信息字符串长度 |

### 用户流移除回调
```cpp
virtual void onUserStreamRemove(const char* user, const char* stream, int streamSize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| user | const char* | 用户 ID |
| stream | const char* | 被移除的流信息 JSON |
| streamSize | int | 流信息字符串长度 |

### 用户离开回调
```cpp
virtual void onUserLeave(const char* user, int userSize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| user | const char* | 离开用户的详细信息 JSON |
| userSize | int | 用户信息字符串长度 |

### 自定义消息回调
```cpp
virtual void onCustomMessage2(const char* action, const char* senderid, const char* name, int name_len, const char* message, int messageSize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| action | const char* | 消息类型/动作 |
| senderid | const char* | 发送者用户 ID |
| name | const char* | 发送者昵称 |
| name_len | int | 昵称长度 |
| message | const char* | 消息内容 |
| messageSize | int | 消息内容长度 |

### 上行挡位变化回调
```cpp
virtual void onUpLevel(int level) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| level | int | 挡位等级（0：好，1：中，2：差，3：极差） |

### 下行挡位变化回调
```cpp
virtual void onDownLevel(const char* id, int level) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| id | const char* | 成员用户 ID |
| level | int | 挡位等级（0：好，1：中，2：差，3：极差） |

### 上行统计回调
```cpp
virtual void onUpStat(const char* upstat, int upstatsize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| upstat | const char* | 上行统计数据 JSON |
| upstatsize | int | 上行统计数据长度 |

### 下行统计回调
```cpp
virtual void onDownStat(const char* downstat, int downstatsize) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| downstat | const char* | 下行统计数据 JSON |
| downstatsize | int | 下行统计数据长度 |

### 帧超时回调
```cpp
virtual void onFrameTimeOut(const char* uid, const char* track_id, const char* track_desc, int loading) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uid | const char* | 用户 ID |
| track_id | const char* | 轨道 ID |
| track_desc | const char* | 轨道描述 |
| loading | int | 加载状态 |

### 音柱回调
```cpp
virtual void onSpeakers(const char* Speakers) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| Speakers | const char* | 发言者能量数据 JSON 数组 |

### 设备状态变化回调
```cpp
virtual void onDeviceStatusChange(int tp, int status) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| tp | int | 设备类型（1：麦克风，2：扬声器，3：摄像头） |
| status | int | 状态（1：异常，2：恢复） |

### 共享目标未找到回调
```cpp
virtual void onShareTargetNotFind() = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |

### 断开连接回调
```cpp
virtual void onDisconnected(int reason, StatusCode code, const char* message, size_t message_size) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| reason | int | 断开原因（-1：异常，0：未知，1：主动离开，2：被踢出，3：被顶号，4：心跳超时，5：频道销毁） |
| code | StatusCode | 错误码 |
| message | const char* | 错误描述信息 |
| message_size | size_t | 错误描述长度 |

### 重连成功回调
```cpp
virtual void onReconnected(const char* options, size_t options_size) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| options | const char* | 重连扩展信息 |
| options_size | size_t | 扩展信息长度 |

### 正在重连回调
```cpp
virtual void onReconnecting() = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |

### 录制状态变化回调
```cpp
virtual void onRecordStatusChange(const char* key, LocalRecordStatusEnum status, const char* msg) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| key | const char* | 录制任务 key |
| status | LocalRecordStatusEnum | 录制状态，[查看](../enums.md) |
| msg | const char* | 状态描述，异常时为异常信息 |
