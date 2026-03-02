srtc是绝大多数操作的入口。

```typescript
/**
 * 构造函数
 */
constructor(initParams: RtcInitParams);

/**
 * 获取sdk编译信息
 */
buildInfo(): BuildInfo;

/**
 * 获取web运行环境信息，如是否支持webrtc等
 * @returns
 */
getEnvInfo(): EnvWebInfo;

/**
 * 频道事件通知回调
 */
onNotifyChannelEvent?: ((event: ChannelEvent) => void) | null;

/**
 * 加入频道
 * @param token 加入频道token
 */
join(token: string): Promise<ChannelInfo>;


/**
 * 离开频道
 */
leave(): Promise<void>;

/**
 * 获取频道信息
 * @returns
 */
getChannelInfo(): ChannelInfo | null;

/**
 * 获取当前流媒体网络质量
 * @returns 
 */
public getStreamMetric(): Record<string, any> | undefined;

/**
 * 获取某用户信息
 * @returns
 */
getUserInfo(uid: string): UserInfo;

/**
 * 获取频道内用户信息列表
 * @returns
 */
getUsersInfo(map: true): Record<string, UserInfo>;
getUsersInfo(map: false): UserInfo[];

/**
 * 获取设备列表
 * @param kind
 * @param requestPermissions
 * @returns
 */
getDevices(kind?: MediaDeviceKind, requestPermissions?: boolean): Promise<MediaDeviceInfo[]>;

/**
 * 创建麦克风本地音频流
 * @param preset 麦克风预设，默认为 MicPresets.music
 */
createLocalMicTrack(preset?: MicPreset): LocalMicTrack;

/**
 * 创建自定义本地音频流
 */
createLocalCustomAudioTrack(msTrack: MediaStreamTrack): LocalAudioTrack;

/**
 * 创建摄像头本地视频流
 * @param preset 摄像头预设，默认为 CameraPresets["720p"]
 */
createLocalCameraTrack(preset?: CameraPreset): LocalCameraTrack;

/**
 * 创建屏幕共享本地视频流
 * @param preset 屏幕共享预设，默认为 ScreenPresets["1080p"]
 */
createLocalScreenTrack(preset?: ScreenPreset): LocalScreenTrack;

/**
 * 创建自定义本地视频流
 */
createLocalCustomVideoTrack(msTrack: MediaStreamTrack): LocalVideoTrack;

/**
 * 发布本地流轨道
 * @param track
 * @returns
 */
publishLocalTrack(track: LocalAudioTrack | LocalVideoTrack, opt?: AudioPublishOptions | VideoPublishOptions): Promise<void>;

/**
 * 取消发布本地流
 * @param track
 */
unpublishLocalTrack(track: LocalAudioTrack | LocalVideoTrack): Promise<void>;

/**
 * 订阅远端频道混音流
 * @param filterUids 过滤音频的用户id
 */
subscribeRemoteAudioMixTrack(filterUids?: string[]): Promise<RemoteAudioMixTrack>;

/**
 * 订阅远端用户音频流
 * @param uid 用户id
 * @param id 流轨道id
 */
subscribeRemoteAudioTrack(uid: string, id: string): Promise<RemoteAudioTrack>;

/**
 * 订阅远端视频合成流
 */
subscribeRemoteVideoMcuTrack(): Promise<RemoteVideoTrack>;

/**
 * 订阅远端用户视频流
 * @param uid 用户id
 * @param id 流轨道id
 */
subscribeRemoteVideoTrack(uid: string, id: string): Promise<RemoteVideoTrack>;

/**
 * 取消订阅远端流
 */
unsubscribeRemoteTrack(track: RemoteAudioMixTrack | RemoteAudioTrack | RemoteVideoTrack): Promise<void>;

/**
 * 获取远端用户音视频流实例，一般用于订阅流后您没有持有返回的流实例，可以用此方法获取对应实例
 * @param uid 用户id
 * @param id 流轨道id，与desc二选一
 * @param desc 流描述，与id二选一
 */
getRemoteTrack(uid: string, id?: string, desc?: string): RemoteAudioTrack | RemoteVideoTrack;

/**
 * 频道外im事件通知回调
 */
onNotifyImEvent?: ((event: ImEvent) => void) | null;

/**
 * 启用频道外消息
 * @param token 启用频道外消息token
 * @returns im会话sid
 */
enableIm(token: string): Promise<string>;

/**
 * 关闭频道外消息
 */
disableIm(): Promise<void>;
```

