# 推流
小程序推流完全依赖`[PusherOptions](https://www.yuque.com/anyconf/rtcengine/afztwq)`，可以将其用于`live-pusher`进行数据绑定

```typescript
/**
 * 页面的初始数据
 */
data: {
    /**频道名 */
    channel: "",
    /**个人信息 */
    me:  {} as UserInfo,
    /**推流配置 */
    pusherOpt:  {} as PusherOptions,
    /** 启用扬声器 */
    enableSpeaker: true,
    /** 订阅的频道混音流*/
    remoteAudioMixTrack: undefined as (undefined | RemoteAudioMixTrack),
    /** 订阅的远端视频流*/
    remoteVideoTracks: {} as Record<string, RemoteTrack>,
    /** 在线用户 */
    users: {} as Record<string, UserInfo>,
    userNum: 0,
    /**是否断线重连中 */
    reconnecting: false,
},

onLoad() {
    // 初始数据
    const me = srtc.getUserInfo(app.meID);
    const channel = srtc.getChannelInfo()?.channel;
    const pusherOpt = srtc.getPusherOptions();
    const users = srtc.getUsersInfo(true);
    this.setData({
        me: me,
        channel: channel,
        pusherOpt: pusherOpt,
        users: users,
        userNum: Object.values(users).length,
    });
}
```

```html
<!-- 推流组件 -->
<!-- 参考 https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html -->
<live-pusher class="pusher {{pusherOpt.enableCamera ? '':'mic-pusher'}}" url="{{pusherOpt.url}}" mode="RTC" autopush="{{true}}"
  enable-camera="{{pusherOpt.enableCamera}}" enable-mic="{{pusherOpt.enableMic}}" device-position="{{pusherOpt.devicePosition}}"
  beauty="{{pusherOpt.beautyLevel}}" whiteness="{{pusherOpt.whitenessLevel}}" 
  local-mirror="{{pusherOpt.localMirror}}" remote-mirror="{{pusherOpt.remoteMirror}}" 
  video-width="{{pusherOpt.width}}" video-height="{{pusherOpt.height}}" fps="{{pusherOpt.fps}}"
  enable-agc="{{pusherOpt.enableAgc}}" enable-ans="{{pusherOpt.enableAns}}"
  min-bitrate="{{pusherOpt.minBitrate}}" max-bitrate="{{pusherOpt.maxBitrate}}" audio-quality="high" 
  bindstatechange="onPushStateChange" bindnetstatus="onPushNetStatus"
  binderror="onPushError" bindaudiovolumenotify="onPushVolumeNotify"
  ></live-pusher>
```

当需要调整推流参数，如开关摄像头、开关麦克风、切换前后置摄像头、调整美颜等参数时，只需调用`srtc.changePusherOptions`修改响应参数，下例如打开麦克风：

```typescript
let opt = await srtc.changePusherOptions({
    enableMic: true,
    audioDesc: "麦克风",
    audioProps: {
        "loc": "浙江杭州",
    },
});
this.setData({
    pusherOpt: opt,
});
```



# 拉流
## BaseTrack
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
```



## RemoteTrack
远端音/视频流轨道，是`BaseTrack`的子类，通过 `srtc.subscribeRemoteVideoTrack`， `srtc.subscribeRemoteAudioTrack`（一般不会订阅单个用户的单路音频流，而是用下面的频道混音流）订阅到，`srtc.unsubscribeRemoteTrack`取消订阅。

```typescript
/** 小程序远端流轨道 */
export declare class RemoteTrack extends BaseTrack {
  /** 播放地址 */
  rtmp_play?: string;
  /** live-player播放器的style */
  public player_style: string = "";
  /**
	 * 更新播放器transform style
	 */
	freshPlayerStyle(containerSelector: string): Promise<void>;
}
```



## RemoteAudioMixTrack
远端频道混音流，是`RemoteTrack`的子类，通过`srtc.subscribeRemoteAudioMixTrack` 订阅到，`srtc.unsubscribeRemoteTrack`取消订阅。

```typescript
/**
 * 远端混音流
 */
export declare class RemoteAudioMixTrack extends RemoteTrack {
  getFilterUids(): string[];
}
```

```html
<!-- 音频混音流播放器 -->
<live-player class="amix-player" data-id="{{remoteAudioMixTrack.info.id}}" src="{{remoteAudioMixTrack.rtmp_play}}" mode="RTC" autoplay="{{true}}" muted="{{!enableSpeaker}}"
  min-cache="0.1" max-cache="0.2" object-fit="contain"
  bindstatechange="onPlayStateChange" bindnetstatus="onPlayNetStatus"
  bindaudiovolumenotify="onPlayVolumeNotify"
  ></live-player>


<!-- 视频流，可能有多个 -->
<live-player class="player" style="{{track.player_style}}" wx:if="{{track.rtmp_play}}" data-uid="{{track.uid}}" data-id="{{track.info.id}}" src="{{track.rtmp_play}}" mode="RTC" autoplay="{{true}}" 
    min-cache="0.2" max-cache="0.8" object-fit="contain"
    bindstatechange="onPlayStateChange" bindnetstatus="onPlayNetStatus"
></live-player>
```

