---
title: "屏幕录制"
description: "iOS SMeeting 会议 SDK 屏幕录制功能配置指南"
---

## 开发环境准备
Xcode 12及以上的版本，手机也必须升级至 iOS 12 以上，否则无法使用录屏特性。

#### 创建扩展程序
在现有工程选择【New】->【Target…】，选择【Broadcast Upload Extension】，如图所示：

![](images/377016_1591942375623-34530649-a3fe-4a08-8a5d-f2eb0d2a9a85.png)

配置好 Product Name。单击【Finish】后可以看到，工程多了所输 Product Name 的目录，目录下有个系统自动生成的 `SampleHandler` 类，这个类负责录屏的相关处理；以及对应的Product Name SetupUI 的目录，目录下有个系统自动生成的 `BroadcastSetupViewController`类，这个类负责录屏的UI相关处理。

#### 为扩展添加SDK依赖
想将`MeetingKit.framework`集成到屏幕录制扩展，需更改`Podfile`文件，并执行`pod install`，如下图所示：

![](images/162144_1721980142474-6e009eeb-2771-478c-a249-d63608f32ea9.png)

#### 为宿主添加后台权限
工程宿主【TARGETS】->【Signing & Capabilities】->【Capability】，选择【Background Modes】，如图所示：

![](images/236350_1591942975317-bd2e2df2-2452-44cb-b652-3db10a7d3928.png)

双击添加后勾选【Audio, AirPlay, and Picture in Picture】选项，如下图所示：

![](images/875454_1591943083527-5e406fa3-2988-48ed-a8b0-eaf1bb6b9def.png)

## 对接流程
1、在需要使用录制服务的位置引入 `#import <MeetingKit/MeetingKit.h>` 并创建`RPSystemBroadcastPickerView`对象，如下图：

![](images/692079_1721979921917-cdc69773-454e-4a1b-84d6-0cdbf3c744f0.png)

2、为实现业务细节，采用如下方式替换`RPSystemBroadcastPickerView`按钮，`broadcastButton`按钮事件后出现以下页面说明扩展集成成功：

![](images/574588_1721979942480-41eb9848-2602-43ef-a2e4-66080d0af1fd.png)

3、宿主工程在初始化`MeetingKit`之后，实现屏幕共享状态回调：

```objectivec
/// 屏幕采集状态回调
/// @param status 状态码
- (void)onScreenRecordStatus:(SEAScreenRecordStatus)status {
    
    SGLOG(@"屏幕共享状态通知，status = %ld", status);
    
    switch (status) {
        case SEAScreenRecordStatusError:
            /// 屏幕采集连接错误
            break;
        case SEAScreenRecordStatusStop:
            /// 屏幕采集已经停止
            break;
        case SEAScreenRecordStatusStart:
            /// 屏幕采集已经开始
            break;
        default:
            break;
    }
}
```

4、屏幕扩展`SampleHandler`中实现`RTCScreenDelegate`代理：

```objectivec
@interface SampleHandler : NSObject <MeetingKitScreenDelegate>
/// 根据需要，在此处添加以下任何回调函数。
```

```objectivec
/// 录屏完成回调
/// @param engine 回调实例
/// @param reason 结束原因
- (void)broadcastFinished:(MeetingKit *)engine reason:(NSString *)reason {

    /// 声明描述
    NSString *describe = @"屏幕录制已结束";
    /// 构建Error信息
    NSError *error = [NSError errorWithDomain:NSStringFromClass(self.class) code:0 userInfo:@{NSLocalizedFailureReasonErrorKey : describe}];
    /// 完成屏幕录制
    [self finishBroadcastWithError:error];
}
```

5、屏幕扩展`SampleHandler`中实现开启屏幕录制功能：

```objectivec
- (void)broadcastStartedWithSetupInfo:(NSDictionary<NSString *,NSObject *> *)setupInfo {
    
    /// User has requested to start the broadcast. Setup info from the UI extension can be supplied but optional.
    [[MeetingKit sharedInstance] broadcastStartedWithAppGroup:@"Application Group Identifier" delegate:self];
}
```

6、屏幕扩展`SampleHandler`中实现发送共享屏幕帧数据：

```objectivec
- (void)processSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType {
    
    /// 媒体数据(音视频)发送
    [[MeetingKit sharedInstance] sendSampleBuffer:sampleBuffer withType:sampleBufferType];
}
```





