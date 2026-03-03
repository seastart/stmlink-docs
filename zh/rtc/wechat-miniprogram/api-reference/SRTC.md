---
title: "SRTC"
description: "微信小程序 SRTC 音视频 SDK SRTC 接口参考"
---

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
 * 获取小程序运行环境信息
 * @returns
 */
getEnvInfo(): EnvWxInfo;

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
 * livepusher配置
 */
getPusherOptions(): PusherOptions;

/**
 * 更新推流配置
 * @param opt
 */
changePusherOptions(opt: Partial<PusherOptions>): Promise<PusherOptions>;

/**
 * 订阅远端频道混音流
 */
subscribeRemoteAudioMixTrack(filterUids?: string[]): Promise<RemoteAudioMixTrack>;

/**
 * 订阅远端用户音频流
 * @param uid 用户id
 * @param id 流轨道id
 */
subscribeRemoteAudioTrack(uid: string, id: string): Promise<RemoteTrack>;

/**
 * 订阅远端用户视频流
 * @param uid 用户id
 * @param id 流轨道id
 */
subscribeRemoteVideoTrack(uid: string, id: string): Promise<RemoteTrack>;

/**
 * 取消订阅远端流
 */
unsubscribeRemoteTrack(track: RemoteTrack): Promise<void>;

/**
 * 获取远端用户音视频流实例，一般用于订阅流后您没有持有返回的流实例，可以用此方法获取对应实例
 * @param uid 用户id
 * @param id 流轨道id，与desc二选一
 * @param desc 流描述，与id二选一
 */
getRemoteTrack(uid: string, id?: string, desc?: string): RemoteTrack;

/**
 * 上报live-pusher的volumenotify
 * 你需要在live-pusher组件bindaudiovolumenotify
 * @param detail 小程序的event.detail
 * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html
 */
updatePusherVolume(detail: any): void;

/**
 * 上报live-pusher的error
 * 你需要在live-pusher组件binderror
 * @param detail 小程序的event.detail
 * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html
 */
updatePusherError(detail: any): void;

/**
 * 上报live-pusher的netstatus
 * 你需要在live-pusher组件bindnetstatus
 * @param detail 小程序的event.detail
 * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html
 */
updatePusherNetStatus(detail: any): void;

/**
 * 上报live-pusher的statechange事件
 * 你需要在live-pusher组件bindstatechange
 * @param detail 小程序的event.detail
 * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html
 */
updatePusherStateChange(detail: any): void;

/**
 * 上报live-player的volumenotify
 * 你需要在live-player音频组件bindaudiovolumenotify
 * @param uid 流轨道的所有者
 * @param trackId 流轨道id
 * @param detail 小程序的event.detail
 * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-player.html
 */
updatePlayerVolume(uid: string, trackId: string, detail: any): void;

/**
 * 上报live-player的netstatus
 * 你需要在live-player组件bindnetstatus
 * @param uid 流轨道的所有者
 * @param trackId 流轨道id
 * @param detail 小程序的event.detail
 * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-player.html
 */
updatePlayerNetStatus(uid: string, trackId: string, detail: any): void;

/**
 * 上报live-player的statechange事件
 * 你需要在live-player组件bindstatechange
 * @param uid 流的所有者
 * @param trackId 流轨道id
 * @param detail 小程序的event.detail
 * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-player.html
 */
updatePlayerStateChange(uid: string, trackId: string, detail: any): void;

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
```typescript

