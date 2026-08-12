---
title: "快速开始"
description: "iOS SRTC 音视频 SDK 快速集成，10 分钟跑通基础功能"
---

<Note>
自 `3.0.0` 起，SDK 分为两层：`RTCEngineKit` 是进程级单例，负责初始化、共享硬件（摄像头、音频路由、屏幕采集）与频道实例的创建；`RTCEngineChannel` 是频道实例，负责加入频道、发布与订阅码流。同一进程可以创建多个频道实例并同时加入多个频道。
</Note>

### step 1：初始化SDK
#### 创建初始化参数
在调用 SDK 的任何其他函数之前，需要进行 SDK 初始化。要初始化 SDK，请创建`RTCEngineConfig`对象的实例。

```objectivec
RTCEngineConfig *engineConfig = [[RTCEngineConfig alloc] init];
engineConfig.enableLocalLog = YES;
```

+ **下表描述了`RTCEngineConfig`对象的所有属性。**

| **参数名** | **必填** | **说明** |
| --- | :---: | --- |
| logPath | 否 | 日志文件路径，默认沙盒 Document 目录 |
| enableLocalLog | 否 | 是否启用本地日志，默认 NO |


#### 初始化RTC引擎
创建 `RTCEngineConfig` 对象后，调用 SDK 的 `initializeWithConfig` 函数设置代理并验证它是否已正确初始化。

```objectivec
RTCEngineError errorCode = [[RTCEngineKit sharedEngine] initializeWithConfig:self.engineConfig appGroup:@"Application Group Identifier" delegate:self];
if (errorCode != RTCEngineErrorOK) {
    NSLog(@"初始化RTC服务失败");
}
```

#### 设置委托
SDK 有两个事件协议，按事件归属分别实现：

+ `RTCEngineDelegate`：进程级事件（音频路由变更、网络测速、应用性能），在初始化时传入；
+ `RTCEngineChannelDelegate`：频道内事件（连接、成员、消息、码流、屏幕共享），在创建频道实例时传入。

```objectivec
@interface YourClass : NSObject <RTCEngineDelegate, RTCEngineChannelDelegate>
/// 根据需要，在此处添加以下任何回调函数。
```

#### 实现回调函数

`RTCEngineChannelDelegate` 的每个回调首参都是事件来源的频道实例，多频道场景下据此区分事件归属，频道名称可从 `channel.channel` 读取。

+ **加入频道成功回调**

```objectivec
/// 加入频道成功回调
/// @param channel 事件来源频道实例
/// @param userId 用户标识
- (void)engineChannel:(RTCEngineChannel *)channel onJoinSucceed:(NSString *)userId {
    
    NSLog(@"加入频道成功 channel = %@, userId = %@", channel.channel, userId);
}
```

+ **自己数据更新回调**

```objectivec
/// 自己数据更新回调
/// @param channel 事件来源频道实例
/// @param userId 用户标识
- (void)engineChannel:(RTCEngineChannel *)channel onUserUpdate:(NSString *)userId {
    
    NSLog(@"自己数据更新 channel = %@, userId = %@", channel.channel, userId);
}
```

+ **开始重连回调**

```objectivec
/// 开始重连回调
/// @param channel 事件来源频道实例
- (void)engineChannelOnReconnecting:(RTCEngineChannel *)channel {
    
    NSLog(@"连接已经断开，组件开始尝试重连 channel = %@", channel.channel);
}
```

+ **重连成功回调**

```objectivec
/// 重连成功回调
/// @param channel 事件来源频道实例
- (void)engineChannelOnReconnected:(RTCEngineChannel *)channel {
    
    NSLog(@"服务连接/重连成功 channel = %@", channel.channel);
}
```

+ **连接断开回调**

```objectivec
/// 连接断开回调
/// 发生不可恢复的错误或者被动离开频道，这个事件触发需要重新获取令牌
/// @param channel 事件来源频道实例
/// @param reason 离开原因
/// @param errCode 错误码
/// @param errMsg 错误信息
- (void)engineChannel:(RTCEngineChannel *)channel onDisconnected:(RTCLeaveReason)reason errCode:(RTCEngineError)errCode errMsg:(nullable NSString *)errMsg {
    
    NSLog(@"当前连接断开或被动离开频道，请重新登录 channel = %@, reason = %ld, errCode = %ld, errMsg = %@", channel.channel, (long)reason, (long)errCode, errMsg);
}
```

+ **自定义消息回调**

```objectivec
/// 自定义消息回调
/// @param channel 事件来源频道实例
/// @param content 消息内容
/// @param action 消息标识
/// @param userId 用户标识
/// @param sessionId 会话标识
/// @param nickname 用户昵称
- (void)engineChannel:(RTCEngineChannel *)channel onCustomMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname {
    
    NSLog(@"接收到自定义消息 channel = %@, action = %@, content = %@", channel.channel, action, content);
}
```

+ **频道更新回调**

```objectivec
/// 频道更新回调
/// @param channel 事件来源频道实例
/// @param props 自定义数据
- (void)engineChannel:(RTCEngineChannel *)channel onChannelUpdate:(NSString *)props {
    
    NSLog(@"频道数据更新 channel = %@, props = %@", channel.channel, props);
}
```

+ **用户加入频道回调**

```objectivec
/// 用户加入频道回调
/// @param channel 事件来源频道实例
/// @param userId 用户标识
- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserJoinChannel:(NSString *)userId {
    
    NSLog(@"通知有用户加入频道 channel = %@, userId = %@", channel.channel, userId);
}
```

+ **成员数据更新回调**

```objectivec
/// 成员数据更新回调
/// @param channel 事件来源频道实例
/// @param userId 用户标识
- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserUpdate:(NSString *)userId {
    
    NSLog(@"通知成员数据更新 channel = %@, userId = %@", channel.channel, userId);
}
```

+ **用户离开频道回调**

```objectivec
/// 用户离开频道回调
/// @param channel 事件来源频道实例
/// @param userId 用户标识
/// @param reason 离开原因
- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserLeaveChannel:(NSString *)userId reason:(RTCLeaveReason)reason {
    
    NSLog(@"通知有用户离开频道 channel = %@, userId = %@", channel.channel, userId);
}
```

+ **用户码流数据变更回调**

```objectivec
/// 用户码流数据变更回调
/// @param channel 事件来源频道实例
/// @param userId 用户标识
/// @param streamTrackModel 码流轨道数据
/// @param changeType 操作类型
- (void)engineChannel:(RTCEngineChannel *)channel onRemoteStreamTrackChange:(NSString *)userId streamTrackModel:(RTCEngineStreamTrackModel *)streamTrackModel changeType:(RTCChangeType)changeType {
    
    NSLog(@"用户码流数据发生变更 channel = %@, userId = %@, streamTrackModel = %@", channel.channel, userId, streamTrackModel);
}
```

### step 2：创建频道实例并加入频道
#### 创建频道实例
```objectivec
RTCEngineChannel *channel = [[RTCEngineKit sharedEngine] createChannelWithDelegate:self];
/// 频道实例由引擎持有，业务侧自行保存引用即可
self.channel = channel;
```

需要同时加入多个频道时，多次调用 `createChannelWithDelegate:` 分别持有各自的实例，实例之间的成员数据、码流统计与渲染互不干扰。

#### 加入频道
```objectivec
RTCEngineError errorCode = [self.channel joinChannelWithToken:@"Your Token"];
if (errorCode != RTCEngineErrorOK) {
    NSLog(@"加入频道失败");
}
```

#### 离开频道
```objectivec
[self.channel leaveChannel:^{
    /// TO DO...
}];
```

#### 销毁频道实例
使用完毕后必须归还实例，否则引擎会一直持有该频道。

```objectivec
[self.channel destroy];
self.channel = nil;
```

### step 3：发布视频流
摄像头是进程级共享硬件，采集与预览通过 `RTCEngineKit` 单例控制；是否把该路画面推送到某个频道，由该频道实例的 `publishLocalVideo:` 单独控制。

#### 开启预览画面
```objectivec
[[RTCEngineKit sharedEngine] startLocalPreview:YES view:self.localView];
```

#### 更新预览画面
```objectivec
[[RTCEngineKit sharedEngine] updateLocalView:self.localView];
```

#### 停止预览画面
```objectivec
[[RTCEngineKit sharedEngine] stopLocalPreview];
```

#### 恢复/暂停向当前频道推流
```objectivec
[self.channel publishLocalVideo:YES];
```

### step 4：订阅和取消订阅远端视频
#### 订阅远端用户的视频流
```objectivec
[self.channel startRemoteView:userId trackId:trackId view:self.previewView];
```

+ **下表描述了`RTCTrackIdentifierFlags`轨道标识枚举类型的所有值。**

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCTrackIdentifierFlags0 | `0` | 轨道0 |
| RTCTrackIdentifierFlags1 | `1` | 轨道1 |
| RTCTrackIdentifierFlags2 | `2` | 轨道2 |
| RTCTrackIdentifierFlags3 | `3` | 轨道3 |
| RTCTrackIdentifierFlags4 | `4` | 轨道4 |
| RTCTrackIdentifierFlags5 | `5` | 轨道5 |
| RTCTrackIdentifierFlags6 | `6` | 轨道6 |


#### 更新远端用户的视频流
```objectivec
[self.channel updateRemoteView:userId trackId:trackId view:self.previewView];
```

#### 停止订阅远端用户的视频流
```objectivec
[self.channel stopRemoteView:userId trackId:trackId];
```

#### 停止订阅指定远端用户的所有视频流
```objectivec
[self.channel stopAllRemoteViewWithUserId:userId];
```

### step 5：销毁资源
`destroy` 会先销毁全部存活的频道实例，等待其离开完成后再释放进程级资源，业务层无需逐个调用频道实例的 `destroy`。

```objectivec
[[RTCEngineKit sharedEngine] destroy];
```
