---
title: "屏幕录制"
description: "iOS SRTC 音视频 SDK 屏幕录制功能配置指南"
---

## 开发环境准备
Xcode 10及以上的版本，手机也必须升级至 iOS 12 以上，否则无法使用录屏特性。

#### 创建扩展程序
在现有工程选择【New】->【Target…】，选择【Broadcast Upload Extension】，如图所示：

![](images/563485_1591942375623-34530649-a3fe-4a08-8a5d-f2eb0d2a9a85.png)

配置好 Product Name。单击【Finish】后可以看到，工程多了所输 Product Name 的目录，目录下有个系统自动生成的 SampleHandler类，这个类负责录屏的相关处理；以及对应的Product Name SetupUI 的目录，目录下有个系统自动生成的 `BroadcastSetupViewController`类，这个类负责录屏的UI相关处理。

#### 为扩展添加SDK依赖
1. 手动集成方式需要将`RTCEngineKit.frameworknl`导入上述Product Name 的工程目录，并配置依赖的系统库；
2. 自动集成方式需更改`Podfile`文件，并执行`pod install`，如下图所示：

![](images/431440_1659061024229-9c42a253-7849-4db5-83e6-0302afcaede6.png)

#### 为宿主添加后台权限
工程宿主【TARGETS】->【Signing & Capabilities】->【Capability】，选择【Background Modes】，如图所示：

![](images/557448_1591942975317-bd2e2df2-2452-44cb-b652-3db10a7d3928.png)

双击添加后勾选【Audio, AirPlay, and Picture in Picture】选项，如下图所示：

![](images/792573_1591943083527-5e406fa3-2988-48ed-a8b0-eaf1bb6b9def.png)

## 对接流程
1、在需要使用录制服务的位置引入 `#import <ReplayKit/ReplayKit.h>` 并创建`RPSystemBroadcastPickerView`对象，如下图：![](images/730239_1659061385614-7b8fbffe-03b4-439e-9358-4078457b5920.png)
2、为实现业务细节，采用如下方式替换`RPSystemBroadcastPickerView`按钮，`broadcastButton`按钮事件后出现以下页面说明扩展集成成功：![](images/743648_1659061479129-4bb5753b-86f1-4277-90d8-ea9a8797c1ca.png)![](images/375434_1591944630207-bd25dc92-4aab-4c28-9798-3b6d28449f8a.png)
3、宿主工程在创建频道实例时传入 `RTCEngineChannelDelegate`，实现屏幕共享状态回调：

<Note>
自 `3.0.0` 起，ReplayKit 采集是进程级共享能力，单个频道是否推送共享流由该频道实例的 `publishScreenRecord:` 控制，屏幕共享状态回调也随之迁移到 `RTCEngineChannelDelegate` 并带上事件来源频道实例。需要一次性关闭进程内全部频道的屏幕录制时，仍调用 `-[RTCEngineKit stopScreenRecord]`。

自 `3.0.1` 起，加入频道成功后 SDK 即启动采集服务并保持监听，用户可以随时通过系统面板拉起屏幕录制；扩展端连接建立后才会回调 `RTCScreenRecordStatusStart`。因此**业务层必须在收到 `Start` 回调之后再调用 `publishScreenRecord:YES`**，不要为了发布共享流而提前调用它。
</Note>

```objectivec
/// 屏幕共享状态回调
/// @param channel 事件来源频道实例
/// @param status 状态码
- (void)engineChannel:(RTCEngineChannel *)channel onScreenRecordStatus:(RTCScreenRecordStatus)status {
    
    /// 提示操作信息
    NSString *toastStr = @"屏幕共享连接错误";
    switch (status) {
        case RTCScreenRecordStatusError:
            toastStr = @"屏幕共享连接错误";
            break;
        case RTCScreenRecordStatusStop:
            toastStr = @"屏幕共享已经停止";
            break;
        case RTCScreenRecordStatusStart:
            toastStr = @"屏幕共享已经开始";
            break;
        default:
            break;
    }
    [FWToastBridge showToastAction:toastStr];
    SGLOG(@"%@", toastStr);
}
```

4、屏幕扩展`SampleHandler`中实现`RTCScreenDelegate`代理：

```objectivec
@interface SampleHandler : NSObject <RTCScreenDelegate>
/// 根据需要，在此处添加以下任何回调函数。
```

```objectivec
/// 录屏完成回调
/// @param engine 回调实例
/// @param reason 结束原因
- (void)broadcastFinished:(RTCEngineKit *)engine reason:(NSString *)reason {

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
    [[RTCEngineKit sharedEngine] broadcastStartedWithAppGroup:@"Application Group Identifier" delegate:self];
}
```

6、屏幕扩展`SampleHandler`中实现发送共享屏幕帧数据：

```objectivec
- (void)processSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType {
    
    /// 媒体数据(音视频)发送
    [[RTCEngineKit sharedEngine] sendSampleBuffer:sampleBuffer withType:sampleBufferType];
}
```

7、宿主工程在收到 `RTCScreenRecordStatusStart` 回调后，在需要推送共享流的频道实例上发布屏幕共享。最后一个发布的频道取消发布时，才会断开扩展端连接并结束本次系统录屏：

```objectivec
/// 当前频道发布屏幕共享流(应在收到 RTCScreenRecordStatusStart 回调之后调用)
[self.channel publishScreenRecord:YES];

/// 当前频道停止屏幕共享流
[self.channel publishScreenRecord:NO];
```

完整时序为：加入频道成功（SDK 自动启动采集服务并监听）→ 用户通过 `RPSystemBroadcastPickerView` 拉起系统录屏 → 扩展端接入，收到 `RTCScreenRecordStatusStart` → 频道实例 `publishScreenRecord:YES` 开始推流。结束时调用 `publishScreenRecord:NO`（仅当前频道停止推流）或 `-[RTCEngineKit stopScreenRecord]`（结束本次系统录屏，采集服务保持监听，用户可再次拉起）。





