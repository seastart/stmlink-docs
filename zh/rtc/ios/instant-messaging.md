---
title: "即时通讯"
description: "iOS SRTC 音视频 SDK 即时消息（IM）功能集成指南"
---

### step 1：初始化SDK
在调用 SDK 的任何其他函数之前，需要进行 SDK 初始化。详情请参看 [组件初始化](https://www.yuque.com/anyconf/rtcengine/am4ult#LfkAQ)。

### step 2：启用即时通讯
#### 获取令牌
启用 SDK 即时通讯服务，需要首先通过服务接口获取鉴权令牌，然后通过以下接口建立通讯连接。

```objectivec
RTCEngineError errorCode = [[RTCEngineKit sharedEngine] enableImWithToken:@"Your Token" delegate:self];
if (errorCode != RTCEngineErrorOK) {
    NSLog(@"即时通讯连接建立失败");
}
```

#### 设置委托
若要订阅委托事件，必须创建 `RTCEngineIMDelegate` 的实例，并使您的类符合 `RTCEngineIMDelegate` 协议。

```objectivec
@interface YourClass : NSObject <RTCEngineIMDelegate>
/// 根据需要，在此处添加以下任何回调函数。
```

#### 实现回调函数
+ **连接成功回调**

```objectivec
/// 连接成功回调
/// 调用 enableImWithToken:() 接口执行启用即时通讯操作后，会收到该事件通知，如果遇到错误会通过 onImDisconnected:() 事件抛出。
/// - Parameters:
///   - userId: 用户标识
///   - sessionId: 会话标识
- (void)onImConnectSucceed:(NSString *)userId sessionId:(NSString *)sessionId {
    
    NSLog(@"im连接建立成功 userId = %@, sessionId = %@", userId, sessionId);
}
```

+ **开始重连回调**

```objectivec
/// 开始重连回调
/// 收到该事件说明连接出现异常，正在尝试重连，如：网络异常等。
- (void)onImReconnecting {
    
    NSLog(@"im连接已经断开，组件开始尝试重连。");
}
```

+ **重连成功回调**

```objectivec
/// 重连成功回调
/// 当连接恢复时，会收到该事件通知。
- (void)onImReconnected {
    
    NSLog(@"im连接已经恢复。");
}
```

+ **连接断开回调**

```objectivec
/// 连接断开回调
/// 发生不可恢复的错误或者被动断开连接，如果是错误事件需要重新获取令牌
/// @param reason 离开原因
/// @param errCode 错误码
/// @param errMsg 错误信息
- (void)onImDisconnected:(RTCImDisconnectReason)reason errCode:(RTCEngineError)errCode errMsg:(nullable NSString *)errMsg {
    
    NSLog(@"im连接出错或被动断开连接，请重新建联 reason = %ld, errCode = %ld, errMsg = %@", reason, errCode, errMsg);
}
```

+ **接收消息回调**

```objectivec
/// 接收消息回调
/// 调用后台接口执行发送消息后，指定成员会收到该事件通知。
/// @param content 消息内容
/// @param action 消息标识
/// @param userId 用户标识
/// @param sessionId 会话标识
/// @param nickname 用户昵称
- (void)onImMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname {
    
    NSLog(@"im接收到消息 action = %@ content = %@ userId = %@", action, content, userId);
}
```

### step 3：停用即时通讯
```objectivec
[[RTCEngineKit sharedEngine] disableIm];
```

### step 4：销毁资源
```objectivec
[[RTCEngineKit sharedEngine] destroy];
```

