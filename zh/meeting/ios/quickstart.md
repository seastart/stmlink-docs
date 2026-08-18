---
title: "快速开始"
description: "iOS SMeeting 会议 SDK 快速集成，10 分钟跑通基础功能"
---

<Note>
**苹果平台有两套 SMeeting SDK，先确认你要用哪一套。** 本章是 Objective-C 的 `MeetingKit`（CocoaPods 分发，仅 iOS）；另有一套 Swift 原生 SDK（`import SMeeting`，Swift Package 形态，同时支持 iOS 与 macOS），见 [Swift SDK](/zh/meeting/swift/integration)。

**新项目建议用 Swift SDK。** 两套 API 不能混用，也不要在同一工程里同时引入。
</Note>

### 环境准备
+ iOS 10.0 及以上版本
+ Xcode 10.0 及以上版本

<Note>
自 `2.0.0` 起，组件分为两层：`MeetingKit` 是全局单例，负责登录、即时通讯、会议查询与预约、共享设备（摄像头、音频路由、屏幕采集）与房间实例的创建；`MeetingKitRoom` 是房间实例，负责进出房间与一切会中操作。同一账号可以创建多个房间实例并同时加入多个房间。
</Note>

### step 1：导入 SDK 并设置 App 权限
#### 导入 SDK
1、在您的 `Podfile` 文件中添加以下依赖。

```objectivec
pod 'MeetingKit'
```

2、执行以下命令，安装组件。

```objectivec
pod install
```

> 说明：
>
> 如果无法安装 MeetingKit 最新版本，执行以下命令更新本地的 CocoaPods 仓库列表：
>

```objectivec
pod repo update
```

> 如果，还是拉取不到最新版本可以尝试指定 MeetingKit 的源：
>

```objectivec
pod 'MeetingKit', :git => "https://github.com/seastart/meeting-ios-cocoapods.git"
```

3、在所使用到 MeetingKit 组件的地方引入头文件。

```objectivec
#import <MeetingKit/MeetingKit.h>
```

#### 配置 App 权限
使用音视频功能，需要授权麦克风、摄像头以及相册的使用权限。在 App 的 Info.plist 中添加以下几项，分别对应麦克风、摄像头和相册在系统弹出授权对话框时的提示信息。

```xml
<key>NSCameraUsageDescription</key>
<string>MeetingKit 需要访问您的相机权限</string>
<key>NSMicrophoneUsageDescription</key>
<string>MeetingKit 需要访问您的麦克风权限</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>MeetingKit 需要访问您的相册</string>
```

### step 2：登录和登出
#### 登录
在调用 SDK 的任何其他函数之前，需要进行 SDK 登录操作，在您的项目中添加如下代码，它的作用是通过调用 MeetingKit 中的相关接口完成会议组件的初始化。这个步骤非常关键，因为只有在登录成功后才能正常使用 MeetingKit 的各项功能：

```objectivec
SEALogConfig *logConfig = [[SEALogConfig alloc] init];
logConfig.enableLocalLog = YES;

[[MeetingKit sharedInstance] loginWithToken:@"Meeting User Auth Token" appGroup:@"Application Group Identifier" logConfig:logConfig onSuccess:^(id _Nullable data) {
    NSLog(@"会议组件登录成功");
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"会议组件登录失败(%ld，%@)", code, message);
}];
```

`enableLocalLog`默认值为`YES`。启用后会采集全进程日志到本地文件，同时保留宿主 App 的控制台输出。继续使用不带`logConfig`参数的登录接口时，也会采用该默认值。

#### 登出
```objectivec
[[MeetingKit sharedInstance] logout];
```

### step 3：创建房间
#### 构建会议参数
会议参数由很多的字段构成，但通常您只需要关注特定几个字段，详情可参看 [SEAMeetingParam](/zh/meeting/ios/types#seameetingparam)。

```objectivec
SEAMeetingParam *meetingParam = [[SEAMeetingParam alloc] init];
meetingParam.title = @"Meeting Title";
```

+ **下表描述了**`**SEAMeetingParam**`**对象的部分属性。**

| **参数名** | **必填** | **描述** |
| --- | :---: | --- |
| title | 是 | 会议标题 |
| content | 否 | 会议说明 |
| password | 否 | 会议密码 |


#### 创建房间
创建 `SEAMeetingParam` 对象后，调用 SDK 的 `createRoom` 函数创建云会议房间。

```objectivec
[[MeetingKit sharedInstance] createRoom:meetingParam onSuccess:^(id _Nullable data) {
    NSString *roomNo = (NSString *)data;
    NSLog(@"创建房间成功，生成的房间号码为：%@", roomNo);
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"创建房间失败，code = %ld, message = %@", code, message);
}];
```

### step 4：创建房间实例并加入房间
自 `2.0.0` 起，会中的一切操作与事件都属于房间维度。加入房间前先通过 `createRoomWithDelegate:` 创建 `MeetingKitRoom` 实例，并在创建时传入房间事件代理。

#### 设置委托
组件有两个事件协议，按事件归属分别实现：

+ `MeetingKitDelegate`：全局事件（音频路由变更、应用性能），通过 `addDelegate:` 设置；
+ `MeetingKitRoomDelegate`：房间内事件（进出房间、成员状态、消息、云录制、码流质量等），在创建房间实例时传入。

```objectivec
@interface YourClass : NSObject <MeetingKitDelegate, MeetingKitRoomDelegate>
/// 根据需要，在此处添加以下任何回调函数。
```

#### 创建房间实例
```objectivec
MeetingKitRoom *room = [[MeetingKit sharedInstance] createRoomWithDelegate:self];
/// 房间实例调用 exitRoom: 之后即失效，业务层自行保存引用
self.room = room;
```

需要同时加入多个房间时，多次调用 `createRoomWithDelegate:` 分别持有各自的实例，各房间的媒体与业务状态相互独立。

#### 实现回调事件

`MeetingKitRoomDelegate` 的每个回调首参都是事件来源的房间实例，多房间场景下据此区分事件归属，房间号与会议标识可从 `room.roomNo`、`room.meetingId` 读取。

+ **错误事件回调**

```objectivec
/// 错误事件回调
/// 发生不可恢复的错误，这个事件触发一般需要获取新的令牌重新入会。
/// - Parameters:
///   - room: 事件来源房间实例
///   - errCode: 错误码
///   - errMsg: 错误信息
- (void)meetingRoom:(MeetingKitRoom *)room onError:(SEAError)errCode errMsg:(nullable NSString *)errMsg {
    
    NSLog(@"发生了错误(%ld)，%@", (long)errCode, errMsg);
}
```

+ **进入房间事件回调**

```objectivec
/// 进入房间事件回调
/// 调用 enterRoom: 接口执行加入房间操作后，会收到该事件通知，如果遇到错误会通过方法的 onFailed 参数抛出。
/// - Parameters:
///   - room: 事件来源房间实例
///   - meetingId: 会议标识
///   - userId: 用户标识
- (void)meetingRoom:(MeetingKitRoom *)room onEnterRoom:(NSString *)meetingId userId:(NSString *)userId {
    
    NSLog(@"加入房间成功，%@ %@", meetingId, userId);
}
```

+ **远端用户加入房间回调**

```objectivec
/// 远端用户加入房间回调
/// 成员调用 enterRoom: 接口执行加入房间后，当前房间所有成员都会收到该事件通知。
/// - Parameters:
///   - room: 事件来源房间实例
///   - userId: 成员标识
- (void)meetingRoom:(MeetingKitRoom *)room onUserEnter:(NSString *)userId {

    NSLog(@"远端用户加入房间通知，userId = %@", userId);
}
```

+ **远端用户离开房间回调**

```objectivec
/// 远端用户离开房间回调
/// 成员调用 exitRoom: 接口执行离开房间后，当前房间所有成员都会收到该事件通知。
/// - Parameters:
///   - room: 事件来源房间实例
///   - userId: 成员标识
- (void)meetingRoom:(MeetingKitRoom *)room onUserExit:(NSString *)userId {

    NSLog(@"远端用户离开房间通知，userId = %@", userId);
}
```

+ **用户摄像头状态变化回调**

```objectivec
/// 用户摄像头状态变化回调
/// 成员调用 requestOpenCamera: 或 closeCamera: 接口执行打开/关闭摄像头以及主持人调用 adminCloseUserCamera: 接口执行关闭远端用户摄像头后，当前房间所有成员都会收到该事件通知，注：当房间内已经有成员开启了摄像头，这时进入房间时也会收到该事件通知。
/// - Parameters:
///   - room: 事件来源房间实例
///   - targetUserId: 目标成员标识
///   - cameraState: 视频状态
///   - reason: 变更原因
- (void)meetingRoom:(MeetingKitRoom *)room onUserCameraStateChanged:(NSString *)targetUserId cameraState:(SEADeviceState)cameraState reason:(SEAChangeReason)reason {

    NSLog(@"用户摄像头状态变化，userId = %@ cameraState = %ld reason = %ld", targetUserId, (long)cameraState, (long)reason);
}
```

+ **用户麦克风状态变化回调**

```objectivec
/// 用户麦克风状态变化回调
/// 成员调用 requestOpenMic: 或 closeMic: 接口执行打开/关闭麦克风以及主持人调用 adminCloseUserMic: 接口执行关闭远端用户麦克风后，当前房间所有成员都会收到该事件通知，注：当房间内已经有成员开启了麦克风，这时进入房间时也会收到该事件通知。
/// - Parameters:
///   - room: 事件来源房间实例
///   - targetUserId: 目标成员标识
///   - micState: 音频状态
///   - reason: 变更原因
- (void)meetingRoom:(MeetingKitRoom *)room onUserMicStateChanged:(NSString *)targetUserId micState:(SEADeviceState)micState reason:(SEAChangeReason)reason {

    NSLog(@"用户麦克风状态变化，userId = %@ micState = %ld reason = %ld", targetUserId, (long)micState, (long)reason);
}
```

#### 创建加入会议参数
在调用 enterRoom 接口时，需要填写 SEAMeetingEnterParam 关键参数，详情可参看 [SEAMeetingEnterParam](/zh/meeting/ios/types#seameetingenterparam)。

```objectivec
SEAMeetingEnterParam *meetingEnterParam = [[SEAMeetingEnterParam alloc] init];
meetingEnterParam.roomNo = @"Target Room No";
meetingEnterParam.nickname = @"Your Name";
meetingEnterParam.avatar = @"Your Portrait";
meetingEnterParam.isAudience = NO; // 默认以普通参会者身份入会，设置为 YES 时以观众身份入会
```

#### 加入房间
创建 `SEAMeetingEnterParam` 对象后，调用 SDK 的 `enterRoom` 函数加入云会议房间。

> 值得注意的是，该方法的成功参数不能作为加入房间的真实情况，仅用于接口层面的调用成功使用，即：接口调用结束。要想确认加入房间是否真实成功，需要通过上述委托监听 `onEnterRoom` 事件来实现。
>

```objectivec
[self.room enterRoom:meetingEnterParam onSuccess:^(id  _Nullable data) {
    NSString *roomId = (NSString *)data;
    NSLog(@"加入房间成功，房间标识为：%@", roomId);
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"加入房间失败，code = %ld, message = %@", code, message);
}];
```

#### 离开房间
> 调用该接口会让用户离开自己所在的房间，并释放摄像头、麦克风、扬声器等设备资源。 等资源释放完毕之后，SDK 会通过`onSuccess`回调向您通知。 如果您要再次调用`enterRoom:()`，建议等待`onSuccess`回调到来之后再执行之后的操作，以避免摄像头或麦克风被占用等异常问题。
>

```objectivec
[self.room exitRoom:^(id  _Nullable data) {
    /// TO DO...
}];
self.room = nil;
```

> 房间实例调用 `exitRoom:` 之后即失效，需要重新入会时请通过 `createRoomWithDelegate:` 创建新实例。调用 `logout` 会离开并销毁全部房间实例，无需逐个退出。
>

### step 5：打开和关闭摄像头
请求开启或关闭摄像头后，服务会通过一系列逻辑确定用户的摄像头状态。此时，组件会收到`onUserCameraStateChanged`事件。

#### 打开摄像头
```objectivec
[self.room requestOpenCamera:YES view:preview onSuccess:^(id  _Nullable data) {
    NSLog(@"请求开启摄像头成功");
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"请求开启摄像头失败，code = %ld, message = %@", code, message);
}];
```

#### 关闭摄像头
```objectivec
[self.room closeCamera:^(id  _Nullable data) {
    NSLog(@"请求关闭摄像头成功");
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"请求关闭摄像头失败，code = %ld, message = %@", code, message);
}];
```

> 需要注意的是，以上方法的成功参数不能作为摄像头状态的真实情况，仅用于接口层面的调用成功使用，即：接口调用结束。为保证摄像头状态客户端与服务端的一致性，需要通过委托监听 `onUserCameraStateChanged` 事件来实现。
>

### step 6：打开和关闭麦克风
请求开启或关闭麦克风后，服务会通过一系列逻辑确定用户的麦克风状态。此时，组件会收到`onUserMicStateChanged`事件。

#### 打开麦克风
```objectivec
[self.room requestOpenMic:^(id  _Nullable data) {
    NSLog(@"请求打开麦克风成功");
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"请求打开麦克风失败，code = %ld, message = %@", code, message);
}];
```

#### 关闭麦克风
```objectivec
[self.room closeMic:^(id  _Nullable data) {
    NSLog(@"请求关闭麦克风成功");
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"请求关闭麦克风失败，code = %ld, message = %@", code, message);
}];
```

> 需要注意的是，以上方法的成功参数不能作为麦克风状态的真实情况，仅用于接口层面的调用成功使用，即：接口调用结束。为保证麦克风状态客户端与服务端的一致性，需要通过委托监听 `onUserMicStateChanged` 事件来实现。
>

### step 7：订阅和取消订阅远端用户画面
#### 订阅远端用户画面
```objectivec
[self.room startRemoteView:@"Remote User ID" streamType:SEAVideoStreamTypeBig view:playerView];
```

+ **下表描述了`SEAVideoStreamType`视频流类型的所有值。**

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAVideoStreamTypeBig | `0` | 高清大画面，一般用来传输摄像头的视频数据 |
| SEAVideoStreamTypeSmall | `1` | 低清小画面，小画面和大画面的内容相同，但是分辨率和码率都比大画面低，因此清晰度也更低 |
| SEAVideoStreamTypeScreen | `2` | 屏幕共享流 |


#### 取消订阅远端用户画面
```objectivec
[self.room stopRemoteView:@"Remote User ID" streamType:SEAVideoStreamTypeBig];
```

#### 取消订阅指定远端用户的所有视频画面
```objectivec
[self.room stopAllRemoteViewWithUserId:@"Remote User ID"];
```

#### 取消订阅所有远端用户的视频画面
组件未提供一次性退订全部成员的接口，业务层遍历成员列表逐个调用 `stopAllRemoteViewWithUserId:` 即可。

```objectivec
for (SEAUserModel *userModel in [self.room getRemoteUsers]) {
    [self.room stopAllRemoteViewWithUserId:userModel.userId];
}
```

> 注：取消订阅成员视频画面后，组件会自行释放渲染控件。
>
