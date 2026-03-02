# BaseTrack
BaseTrack是所有音视频流的基类

```typescript
/**
 * 轨道id
 */
get id(): string;

/**
 * 轨道类型
 */
get kind(): TrackKind;

/**
 * 轨道描述
 */
get desc(): string;

/**
 * 获取流轨道信息
 * @returns 
 */
public getInfo(): TrackInfo;

/**
 * 轨道所属用户
 * @returns 
 */
public getUid(): string;

/**
 * 获取底层MediaStreamTrack
 */
getMediaStreamTrack(): MediaStreamTrack | undefined;
```



# 本地音频流
本地流在创建并开始采集后，可通过`srtc.publishLocalTrack`发布，`srtc.unpublishLocalTrack`取消发布。

## LocalAudioTrack
本地音频流轨道基类，也可用于自定义本地音频流，通过`srtc.createLocalCustomAudioTrack`创建。

```typescript

/**
 * 播放音频(可指定播放设备)
 */
startPlay(opt?: AudioOutputOptions): Promise<void>;

/**
 * 停止播放并释放对播放设备的占用
 */
stopPlay(): void;
```

## LocalMicTrack
本地麦克风流轨道，是`LocalAudioTrack`的子类，通过`srtc.createLocalMicTrack`创建。

```typescript
/**
 * 开始采集
 * @param opt 采集参数
 */
startCapture(opt?: MicCaptureOptions): Promise<void>;

/**
 * 停止采集
 */
stopCapture(): void;

/**
 * 切换麦克风
 * @param deviceId
 * @returns
 */
changeDeviceId(deviceId: string): Promise<void>;
```



# 本地视频流
本地流在创建并开始采集后，可通过`srtc.publishLocalTrack`发布，`srtc.unpublishLocalTrack`取消发布。

## LocalVideoTrack
本地视频流轨道，也可用于自定义本地视频流，通过`srtc.createLocalCustomVideoTrack`创建。

```typescript
/**
 * 添加播放窗口
 */
addPlayView(container: HTMLElement): void;

/**
 * 是否存在播放窗口
 */
hasPlayView(): boolean;

/**
 * 移除播放窗口
 */
removePlayView(container: HTMLElement): void;

/**
 * 移除所有播放窗口
 */
removeAllPlayViews(): void;
```

## LocalCameraTrack
本地摄像头视频流轨道，是`LocalVideoTrack`的子类，通过`srtc.createLocalCameraTrack`创建。

```typescript
/**
 * 开始采集
 * @param opt 采集参数
 */
startCapture(opt?: CameraCaptureOptions): Promise<void>;

/**
 * 停止采集
 */
stopCapture(): void;

/**
 * 切换指定摄像头
 * @param deviceId
 * @returns
 */
changeDeviceId(deviceId: string): Promise<void>;

/**
 * 切换摄像头朝向(仅手机)
 * @returns
 */
switchFacingMode(): Promise<void>;
```



## LocalScreenTrack
本地屏幕共享视频流轨道，是`LocalVideoTrack`的子类，通过`srtc.createLocalScreenTrack`创建。

```typescript
/**
 * 开始采集
 * @param opt 采集参数
 */
startCapture(opt?: ScreenCaptureOptions): Promise<void>;

/**
 * 停止采集
 */
stopCapture(): void;
```

# 远端音频流
## RemoteAudioTrack
远端音频流轨道，通过`srtc.subscribeRemoteAudioTrack`订阅到，`srtc.unsubscribeRemoteTrack`取消订阅。

```typescript
/**
 * 播放音频(可指定播放设备)
 */
startPlay(opt?: AudioOutputOptions): Promise<void>;

/**
 * 停止播放并释放对播放设备的占用
 */
stopPlay(): void;
```



## RemoteAudioMixTrack
远端频道混音流，是`RemoteAudioTrack`的子类，通过`srtc.subscribeRemoteAudioMixTrack`订阅到，`srtc.unsubscribeRemoteTrack`取消订阅。



# 远端视频流
## RemoteVideoTrack
远端视频流轨道，通过`srtc.subscribeRemoteVideoTrack`订阅到，`srtc.unsubscribeRemoteTrack`取消订阅。

```typescript
/**
 * 添加播放窗口
 */
addPlayView(container: HTMLElement): void;

/**
 * 是否存在播放窗口
 */
hasPlayView(): boolean;

/**
 * 移除播放窗口
 */
removePlayView(container: HTMLElement): void;

/**
 * 移除所有播放窗口
 */
removeAllPlayViews(): void;
```



