---
title: "SRTC"
description: "微信小程序音视频 SDK 的主入口类，绝大多数操作都从这里发起"
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
 * 会前网络检测：入会前调用，不需要加入频道、不使用 token 鉴权（v0.3.1 起）
 * 依次检测网络权限、网络连接、MTU、域名解析、服务器连接 5 项，每完成一项回调一次 onItem
 * @param options appId + serverUrl（即 token 里的 client_api），或直接传 token
 * @returns 检测结果，固定 5 项、固定顺序
 */
networkCheck(options: NetworkCheckOptions): Promise<NetworkCheckResult>;

/**
 * 取消正在进行的网络检测，networkCheck 随即以 107026（Cancelled）结束；没有检测在跑时无操作
 */
cancelNetworkCheck(): void;

/**
 * 频道事件通知回调
 */
onNotifyChannelEvent?: ((event: ChannelEvent) => void) | null;

/**
 * 加入频道
 * @param token 加入频道token
 * @returns 频道对象（v0.2.0 起返回值由频道信息改为 Channel 对象，
 *   频道信息改用 channel.getInfo() 或 srtc.getChannelInfo() 获取）
 */
join(token: string): Promise<Channel>;


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
```

### 会前网络检测

`networkCheck` 的参数与结果类型见 [会前网络检测相关](/zh/rtc/wechat-miniprogram/types#会前网络检测相关)，接口与 [Web SDK](/zh/rtc/web/api-reference/SRTC#networkcheck) 一致。

```typescript
const srtc = new SRTC({});
const result = await srtc.networkCheck({
  appId: 'your_app_id',
  serverUrl: 'https://rtc.example.com/client/', // 即 token 里的 client_api
  onItem: (item) => console.log(item.id, item.status, item.message),
});
```

- 小程序端的平台限制：`permission`、`mtu`、`dns` 三项固定为 `unsupported`；服务器连接项里的媒体（UDP）子检查同样记 `unsupported`，信令只测 WebSocket。所以小程序上 `server` 通过只说明 SDK 接口与信令可达。
- SDK 接口地址与信令地址需已加入小程序的 request / socket 合法域名，否则对应子检查失败。
- 需要服务端提供网络检测接口；服务端版本较老、没有该接口时，服务器连接项记 `fail`（`api_unreachable`），信令、媒体子检查记 `skipped`。
- 同一个实例同时只能跑一个检测，进行中再次调用抛 `107005`；被 `cancelNetworkCheck` 取消时抛 `107026`；缺 `appId` / `serverUrl` 且 `token` 解不出来时抛 `107031`。
