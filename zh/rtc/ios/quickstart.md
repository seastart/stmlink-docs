### step 1：初始化SDK
#### 创建初始化参数
在调用 SDK 的任何其他函数之前，需要进行 SDK 初始化。要初始化 SDK，请创建`RTCEngineConfig`对象的实例。

```objectivec
RTCEngineConfig *engineConfig = [[RTCEngineConfig alloc] init];
engineConfig.enableLocalLog = YES;
```

+ **<font style="color:rgb(51, 51, 51);">下表描述了</font>**`**<font style="color:rgb(51, 51, 51);">RTCEngineConfig</font>**`**<font style="color:rgb(51, 51, 51);">对象的所有属性。</font>**

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
若要订阅委托事件，必须创建 `RTCEngineDelegate` 的实例，并使您的类符合 `RTCEngineDelegate` 协议。

```objectivec
@interface YourClass : NSObject <RTCEngineDelegate>
/// 根据需要，在此处添加以下任何回调函数。
```

#### 实现回调函数
+ **<font style="color:rgb(51, 51, 51);">加入频道成功回调</font>**

```objectivec
/// 加入频道成功回调
/// @param channel 频道名称
/// @param userId 用户标识
- (void)onJoinSucceed:(NSString *)channel userId:(NSString *)userId {
    
    NSLog(@"加入频道成功 channel = %@, userId = %@", channel, userId);
}
```

+ **<font style="color:rgb(51, 51, 51);">自己数据更新回调</font>**

```objectivec
/// 自己数据更新回调
/// @param channel 频道名称
/// @param userId 用户标识
- (void)onUserUpdate:(NSString *)channel userId:(NSString *)userId {
    
    NSLog(@"加入频道成功 channel = %@, userId = %@", channel, userId);
}
```

+ **<font style="color:rgb(51, 51, 51);">开始重连回调</font>**

```objectivec
/// 开始重连回调
- (void)onReconnecting {
    
    NSLog(@"连接已经断开，组件开始尝试重连。");
}
```

+ **<font style="color:rgb(51, 51, 51);">重连成功回调</font>**

```objectivec
/// 重连成功回调
- (void)onReconnected {
    
    NSLog(@"服务连接/重连成功。");
}
```

+ **<font style="color:rgb(51, 51, 51);">连接断开回调</font>**

```objectivec
/// 连接断开回调
/// 发生不可恢复的错误或者被动离开频道，这个事件触发需要重新获取令牌
/// @param reason 离开原因
/// @param errCode 错误码
/// @param errMsg 错误信息
- (void)onDisconnected:(RTCLeaveReason)reason errCode:(RTCEngineError)errCode errMsg:(nullable NSString *)errMsg {
    
    NSLog(@"当前连接断开或被动离开频道，请重新登录 reason = %ld, errCode = %ld, errMsg = %@", reason, errCode, errMsg);
}
```

+ **<font style="color:rgb(51, 51, 51);">自定义消息回调</font>**

```objectivec
/// 自定义消息回调
/// @param content 消息内容
/// @param action 消息标识
/// @param userId 用户标识
- (void)onCustomMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId {
    
    NSLog(@"接收到自定义消息 action = %@ content = %@", action, content);
}
```

+ **<font style="color:rgb(51, 51, 51);">频道更新回调</font>**

```objectivec
/// 频道更新回调
/// @param channel 频道名称
/// @param props 自定义数据
- (void)onChannelUpdate:(NSString *)channel props:(NSString *)props {
    
    NSLog(@"频道数据更新 channel = %@, props = %@", channel, props);
}
```

+ **<font style="color:rgb(51, 51, 51);">用户加入频道回调</font>**

```objectivec
/// 用户加入频道回调
/// @param channel 频道名称
/// @param userId 用户标识
- (void)onRemoteUserJoinChannel:(NSString *)channel userId:(NSString *)userId {
    
    NSLog(@"通知有用户加入频道 channel = %@, userId = %@", channel, userId);
}
```

+ **<font style="color:rgb(51, 51, 51);">成员数据更新回调</font>**

```objectivec
/// 成员数据更新回调
/// @param channel 频道名称
/// @param userId 用户标识
- (void)onRemoteUserUpdate:(NSString *)channel userId:(NSString *)userId {
    
    NSLog(@"通知成员数据更新 channel = %@, userId = %@", channel, userId);
}
```

+ **<font style="color:rgb(51, 51, 51);">用户离开频道回调</font>**

```objectivec
/// 用户离开频道回调
/// @param channel 频道名称
/// @param userId 用户标识
/// @param reason 离开原因
- (void)onRemoteUserLeaveChannel:(NSString *)channel userId:(NSString *)userId reason:(RTCLeaveReason)reason {
    
    NSLog(@"通知有用户离开频道 channel = %@, userId = %@", channel, userId);
}
```

+ **<font style="color:rgb(51, 51, 51);">用户码流数据变更回调</font>**

```objectivec
/// 用户码流数据变更回调
/// @param channel 频道名称
/// @param userId 用户标识
/// @param streamTrackModel 码流轨道数据
/// @param changeType 操作类型
- (void)onRemoteStreamTrackChange:(NSString *)channel userId:(NSString *)userId streamTrackModel:(RTCEngineStreamTrackModel *)streamTrackModel changeType:(RTCChangeType)changeType {
    
    NSLog(@"用户码流数据发生变更 channel = %@, userId = %@, streamTrackModel = %@", channel, userId, streamTrackModel);
}
```

### step 2：加入和离开频道
#### 加入频道
```objectivec
RTCEngineError errorCode = [[RTCEngineKit sharedEngine] joinChannelWithToken:@"Your Token"];
if (errorCode != RTCEngineErrorOK) {
    NSLog(@"加入频道失败");
}
```

#### 离开频道
```objectivec
[[RTCEngineKit sharedEngine] leaveChannel:^{
    /// TO DO...
}];
```

### step 3：发布视频流
#### **开启预览画面**
```objectivec
[[RTCEngineKit sharedEngine] startLocalPreview:YES view:self.localView];
```

#### **更新预览画面**
```objectivec
[[RTCEngineKit sharedEngine] updateLocalView:self.localView];
```

#### **停止预览画面**
```objectivec
[[RTCEngineKit sharedEngine] stopLocalPreview];
```

#### **恢复/暂停推流**
```objectivec
[[RTCEngineKit sharedEngine] publishLocalVideo:YES];
```

### step 4：订阅和取消订阅远端视频
#### **订阅远端用户的视频流**
```objectivec
[[RTCEngineKit sharedEngine] startRemoteView:userId trackId:trackId view:self.previewView];
```

+ **<font style="color:rgb(51, 51, 51);">下表描述了 </font>**`**RTCTrackIdentifierFlags**`**<font style="color:rgb(51, 51, 51);"> 轨道标识枚举类型的所有值。</font>**

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCTrackIdentifierFlags0 | `0` | 轨道0 |
| RTCTrackIdentifierFlags1 | `1` | 轨道1 |
| RTCTrackIdentifierFlags2 | `2` | 轨道2 |
| RTCTrackIdentifierFlags3 | `3` | 轨道3 |
| RTCTrackIdentifierFlags4 | `4` | 轨道4 |
| RTCTrackIdentifierFlags5 | `5` | 轨道5 |
| RTCTrackIdentifierFlags6 | `6` | 轨道6 |


#### **更新远端用户的视频流**
```objectivec
[[RTCEngineKit sharedEngine] updateRemoteView:userId trackId:trackId view:self.previewView];
```

#### **停止订阅远端用户的视频流**
```objectivec
[[RTCEngineKit sharedEngine] stopRemoteView:userId trackId:trackId];
```

#### **停止订阅指定远端用户的所有视频流**
```objectivec
[[RTCEngineKit sharedEngine] stopAllRemoteViewWithUserId:userId];
```

### step 5：销毁资源
```objectivec
[[RTCEngineKit sharedEngine] destroy];
```

