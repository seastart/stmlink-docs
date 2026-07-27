---
title: "快速开始"
description: "微信小程序 SRTC 音视频 SDK 快速集成，10 分钟跑通基础功能"
---

### 基本概念
+ 小程序音视频基于`[live-pusher](https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html)``[live-player](https://developers.weixin.qq.com/miniprogram/dev/component/live-player.html)`实现
+ `SRTC`实例：通过`new SRTC`得到操作实例，绝大部分接口都通过该实例对外提供，所有事件都可通过`srtc.onNotifyChannelEvent`来监听。（如果你想同时加入多个频道，目前只能new多个实例来操作）
+ `ChannelInfo`：`srtc.join`加入频道后的频道信息（业务上可自定义props扩展属性），可通过 `srtc.getChannelInfo`获得
+ `UserInfo`：频道内用户信息(包括自己与其他远端用户)（业务上可自定义props扩展属性），可通过`srtc.getUserInfo(uid: string)`获取频道单用户信息，也可通过`srtc.getUsersInfo()`获取频道所有在线用户信息
+ `PusherOptions`：对应`live-pusher`的组件属性，可用于数据绑定。本地流发布、开关摄像头、开关麦等都通过`srtc.changePusherOptions`来实现
+ `RemoteTrack`：远端流轨道，每一路音频、每一路视频，都是一个Track，一个用户可能有多个Track。提供`rtmp_play`属性用于`live-player`进行播放

远端流轨道（可订阅、可发布）包括：

远端频道混音流轨道：`RemoteAudioMixTrack`

远端用户音频流轨道：`RemoteTrack`

远端用户视频流轨道：`RemoteTrack`

+ `TrackInfo`：流轨道信息，（除desc轨道描述外，业务上还可自定义props扩展属性），归属于Track。

### 初始化SDK
```typescript
import {LogTarget, LogTarget, SRTC} form "./lib/srtc-wx"

// 创建实例
const srtc = new SRTC({
    logLevel: LogLevel.DEBUG,
    logTarget: LogTarget.CONSOLE,
});

// 回调事件响应
srtc.onNotifyChannelEvent = (evt: ChannelEvent) => {
  console.log('收到频道事件', evt);
  switch (evt.type) {
      // ...
  }
})

// ...
```

### 加入频道
```typescript
let join = async () => {
    // 调后台api获取加入频道token
    // api.getJoinToken
  
    let token = "后台返回的加入频道token";
    let channelInfo = await srtc.join(token);
    wx.showToast({
        icon: "success",
        title: "加入频道成功",
    });
}
```

### 获取频道信息/用户信息/用户列表
```typescript
// 获取频道信息
let channelInfo: ChannelInfo = srtc.getChannelInfo();
// 获取某用户信息
let userInfo: UserInfo = srtc.getUserInfo(uid);
// 获取频道内用户信息列表
let usersInfo: UserInfo[] = srtc.getUsersInfo();
```

### 推流live-pusher参数相关
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
    // 初始数据（已经join成功后）
    const me = srtc.getUserInfo(meUid);
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
},

onReady() {
    // 保持高亮
    wx.setKeepScreenOn({
        keepScreenOn: true
    });
    // 离开提醒
    wx.enableAlertBeforeUnload({
        message: "确定离开频道？"
    });
},

onUnload() {
    // 离开页面，退出频道
    srtc.leave();
    wx.setKeepScreenOn({
        keepScreenOn: false
    });
},

/**
 * 延迟回到上一页并且不弹框提醒（wx.navigateBack会弹出离开提醒）
 * 如果是从分享的连接打开，没有页面栈，回到首页
 */
navigateBack: function (delay: number = 0) {
    wx.disableAlertBeforeUnload();
    setTimeout(() => {
        if (getCurrentPages().length > 1) {
            //have pages on stack
            wx.navigateBack({});
        } else {
            //no page on stack, usually means start from shared links
            wx.redirectTo({
                url: '../index/index',
            });
        }
    }, delay);
},

// 将live-pusher的状态通知sdk
/**
 * 推流状态改变
 * @param event 
 */
onPushStateChange(event: WechatMiniprogram.CustomEvent): void {
    console.log("pusher statechange", event.detail);
    srtc.updatePusherStateChange(event.detail);
},
/**
 * 推流网络状态通知
 * @param event 
 */
onPushNetStatus(event: WechatMiniprogram.CustomEvent) {
    // console.log("pusher netstatus", event.detail);
    srtc.updatePusherNetStatus(event.detail);
},
/**
 * 推流渲染错误
 * @param event 
 */
onPushError(event: WechatMiniprogram.CustomEvent) {
    console.log("pusher error", event.detail);
    srtc.updatePusherError(event.detail);
    wx.showToast({
        icon: "none",
        title: `推流失败${event.detail.errMsg}${event.detail.errCode}，将自动重试`,
    });
},
/**
 * 推流麦克风采集音量大小
 * @param event 
 */
onPushVolumeNotify(event: WechatMiniprogram.CustomEvent) {
    srtc.updatePusherVolume(event.detail);
},
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



### 打开、关闭麦克风
```typescript
/**
 * 打开麦克风
 */
async openMic() {
    if (this.data.pusherOpt.enableMic) {
        throw "已开启麦克风";
    }
    // 可选：调后台api请求开启麦克风
    // api.openMic

    // 设置音频轨道描述desc以及自定义props
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
},
/**
 * 关闭麦克风
 */
async closeMic() {
    try {
        if (this.data.pusherOpt.enableMic) {
            let opt = await srtc.changePusherOptions({
                enableMic: false,
            });
            this.setData({
                pusherOpt: opt,
            });
        }
        // 可选：调后台api通知关闭麦克风
        // api.closeMic
    } catch (err) {
        console.error("关闭麦克风失败，强制关闭", err);
    }
},
/**
 * 切换开关麦克风
 */
async onTapMicBtn() {
    if (this.data.pusherOpt.enableMic) {
        await this.closeMic();
        console.warn('关闭麦克风成功');
    } else {
        try {
            await this.openMic();
            console.warn('打开麦克风成功');
        } catch (err) {
            console.error('打开麦克风失败', err);
            await this.closeMic();
        }
    }
},
```



### 打开、关闭摄像头、切换前后置摄像头
```typescript
/**
 * 切换前后置
 */
async onTapSwitchCameraBtn() {
    let pos: "front"|"back" = this.data.pusherOpt.devicePosition === 'front' ? 'back' : 'front';
    let opt = await srtc.changePusherOptions({
        devicePosition: pos,
        videoProps: {
            "position": pos,
        }
    });
    this.setData({
        pusherOpt: opt
    });
},
/**
 * 打开摄像头
 */
async openCamera() {
    if (this.data.pusherOpt.enableCamera) {
        throw "已开启摄像头";
    }
    // 可选：调后台api请求开启摄像头
    // api.openCamera

    // 设置视频轨道描述desc以及自定义props
    let opt = await srtc.changePusherOptions({
        enableCamera: true,
        videoDesc: "摄像头",
        videoProps: {
            "position": this.data.pusherOpt.devicePosition,
        },
    });
    this.setData({
        pusherOpt: opt,
    });
},
/**
 * 关闭摄像头
 */
async closeCamera() {
    try {
        if (this.data.pusherOpt.enableCamera) {
            let opt = await srtc.changePusherOptions({
                enableCamera: false,
            });
            this.setData({
                pusherOpt: opt,
            });
        }
        // 可选：调后台api通知关闭摄像头
        // api.closeCamera
    } catch (err) {
        console.error("关闭摄像头失败，强制关闭", err);
    }
},
/**
 * 开关摄像头
 */
async onTapCameraBtn() {
    if (this.data.pusherOpt.enableCamera) {
        await this.closeCamera();
        console.warn('关闭摄像头成功');
    } else {
        try {
            await this.openCamera();
            console.warn('打开摄像头成功');
        } catch (err) {
            console.error('打开摄像头失败', err);
            await this.closeCamera();
        }
    }
},
```



### 监听用户进出及信息更新
```typescript
// 在onNotifyChannelEvent里
case ChannelEventType.USER_JOIN: {
  // evt.data as UserInfo
  let users = this.data.users;
  let user = evt.data as UserInfo;
  users[user.uid] = user;
  this.setData({
      users: users,
      userNum: ++this.data.userNum,
  });
  break;
}
case ChannelEventType.USER_UPDATE: {
  // evt.data as UserInfo
  let users = this.data.users;
  let user = evt.data as UserInfo;
  users[user.uid] = user;
  this.setData({
      users: users,
  });
  break;
}
case ChannelEventType.USER_LEAVE: {
  // evt.data as UserLeaveEventData
  let users = this.data.users;
  let uid = evt.data.uid;
  // 如果正在订阅该用户的视频流，取消订阅
  let remoteVideoTracks = this.data.remoteVideoTracks;
  for (const id in remoteVideoTracks) {
      let track = remoteVideoTracks[id];
      if (track.getUid() == uid) {
          this.unsubVideo(uid, track.getInfo());
      }
  }
  delete users[uid];
  this.setData({
      users: users,
      userNum: --this.data.userNum,
  })
  break;
}
```

### 监听自己信息被更新
你的信息可能被后台或管理员进行强制更新

```typescript
// 在onNotifyChannelEvent里
case ChannelEventType.ME_UPDATE:
  // evt.data as UserInfo
  let users = this.data.users;
  let user = evt.data as UserInfo;
  users[user.uid] = user;
  this.setData({
      me: user,
      users: users,
  });
  break;
```

### 订阅/取消订阅远端视频流
```typescript
// 相关频道事件
// 远端用户进入：ChannelEventType.USER_JOIN
// 远端用户退出：ChannelEventType.USER_LEAVE (sdk内部会自动取消订阅该用户所有轨道)
// 远端用户添加流轨道：ChannelEventType.USER_TRACK_ADD
// 远端用户删除流轨道：ChannelEventType.USER_TRACK_REMOVE (sdk内部会自动取消订阅该轨道)
// 远端用户信息更新事件：ChannelEventType.USER_UPDATE
// 自定义事件：ChannelEventType.CUSTOM_MSG

// 可以根据业务需要监听上述事件及实际界面需求，来订阅或取消订阅远端视频流

/**
 * 订阅视频轨道
 * @param userinfo 
 * @param trackinfo 
 */
async subVideo(userinfo: UserInfo, trackinfo: TrackInfo) {
    let remoteVideoTracks = this.data.remoteVideoTracks;
    let id = userinfo.uid + '-' + trackinfo.id;
    if (remoteVideoTracks[id]) {
        console.warn(`已经订阅${userinfo.uid}:${trackinfo.id}:${trackinfo.desc}轨道`);
        return;
    }
    try {
        let rtrack = await srtc.subscribeRemoteVideoTrack(userinfo.uid, trackinfo.id);
        this.setData({
          [`remoteVideoTracks.${id}`] : rtrack
        });
        // 订阅后，刷新某已pick的远端流样式
        setTimeout(() => this.freshStyle(id), 500);
        console.log(rtrack);
        console.warn(`订阅${userinfo.uid}:${trackinfo.id}:${trackinfo.desc}轨道成功`);
    } catch (err) {
        console.error(`订阅${userinfo.uid}:${trackinfo.id}:${trackinfo.desc}轨道失败`, err);
    }
},
/**
 * 取消订阅
 * @param uid 
 * @param trackinfo 
 */
async unsubVideo(uid: string, trackinfo: TrackInfo) {
    let remoteVideoTracks = this.data.remoteVideoTracks;
    let id = uid + '-' + trackinfo.id;
    if (!remoteVideoTracks[id]) {
        console.warn(`尚未订阅${uid}:${trackinfo.id}:${trackinfo.desc}轨道`);
        return;
    }
    try {
        await srtc.unsubscribeRemoteTrack(remoteVideoTracks[id]);
        delete remoteVideoTracks[id];
        this.setData({
            remoteVideoTracks: remoteVideoTracks
        });
        console.warn(`取消订阅${uid}:${trackinfo.id}:${trackinfo.desc}轨道成功`);
    } catch (err) {
        console.error(`取消订阅${uid}:${trackinfo.id}:${trackinfo.desc}轨道失败`, err);
    }
},

// 将live-player的状态通知sdk 
/**
 * 拉流播放音量大小
 * @param event 
 */
onPlayVolumeNotify(event: WechatMiniprogram.CustomEvent): void {
    let dataset = event.target.dataset;
    // console.log(`player volumenotify`, dataset, event.detail);
    srtc.updatePlayerVolume(dataset.uid, dataset.id, event.detail);
},
/**
 * 拉流状态改变
 * @param event 
 */
onPlayStateChange(event: WechatMiniprogram.CustomEvent): void {
    let dataset = event.target.dataset;
    console.log(`player statechange`, dataset, event.detail);
    srtc.updatePlayerStateChange(dataset.uid, dataset.id, event.detail);

},
/**
 * 拉流网络状态通知
 * @param event 
 */
onPlayNetStatus(event: WechatMiniprogram.CustomEvent) {
    let dataset = event.target.dataset;
    // console.log(`player netstatus`, dataset, event.detail);
    srtc.updatePlayerNetStatus(dataset.uid, dataset.id, event.detail);
},
```

```html
<block wx:for="{{remoteVideoTracks}}" wx:key="id" wx:for-index="id" wx:for-item="track">
  <view class="track" id="track-{{id}}">
    <!-- 收用户视频流，可能会有多个player -->
    <!-- 参考 https://developers.weixin.qq.com/miniprogram/dev/component/live-player.html -->
    <live-player class="player" style="{{track.player_style}}" wx:if="{{track.rtmp_play}}" data-uid="{{track.uid}}" data-id="{{track.info.id}}" src="{{track.rtmp_play}}" mode="RTC" autoplay="{{true}}" 
      min-cache="0.2" max-cache="0.8" object-fit="contain"
      bindstatechange="onPlayStateChange" bindnetstatus="onPlayNetStatus"
      ></live-player>
  </view>
</block>
```

**关于播放画面的旋转、镜像：**

一般情况下推过来的流是没有角度，不需要做任何处理，但有些手机app推过来的视频流可能是需要做旋转、镜像的，如有实际需要，可按如下处理：

+ 首先设置css，`live-player`设置为绝对定位并撑满其父容器

```css
.track {
    position: relative;
}
.player {
    position: absolute;
    width: 100%;
    height: 100%;
}
```

+ 其次将`live-player`的style属性绑定为`{{track.player_style}}`
+ 最后在订阅流后(或者视图尺寸发生变化如屏幕旋转时)，调用`track.freshPlayerStyle`(可以加延迟，必须等到已经将player渲染到视图后)

```typescript
// 订阅后，刷新某已pick的远端流样式
setTimeout(() => this.freshStyle(id), 500);

async freshStyle(id:string): void {
    let rtrack = this.data.remoteVideoTracks[id];
    if(!rtrack) {
        return;
    }

    // 传live-player的父容器selector字串
    await rtrack.freshPlayerStyle('#track-' + id);
    this.setData({
        [`remoteVideoTracks.${id}`] : rtrack
    });
}
```

### 收全频道音频混音流
一般场景下，我们不需要单独收每一个远端用户的声音，而只用收全频道的混音流进行播放

```typescript
// 订阅混音流
srtc.subscribeRemoteAudioMixTrack().then((track) => {
    this.setData({
        remoteAudioMixTrack: track,
    });
    console.log("订阅混音流成功");
}).catch((e) => {
    console.error('订阅混音流失败', e);
});
```

```html
<!-- 频道混音流播放器 -->
<live-player class="amix-player" data-id="{{remoteAudioMixTrack.info.id}}" src="{{remoteAudioMixTrack.rtmp_play}}" mode="RTC" autoplay="{{true}}" muted="{{!enableSpeaker}}"
  min-cache="0.1" max-cache="0.2" object-fit="contain"
  bindstatechange="onPlayStateChange" bindnetstatus="onPlayNetStatus"
  bindaudiovolumenotify="onPlayVolumeNotify"
  ></live-player>
```

```css
/* 隐藏混音流播放器 */
.amix-player {
    width: 0;
    height: 0;
    position: absolute;
    top: 0;
    left: 0;
}
```

### 开始重连/重连成功
当网络发生波动时，会触发重连开始事件，成功后会触发重连成功事件。ui上可对用户进行提示。

```typescript
// 在onNotifyChannelEvent里
case ChannelEventType.RECONNECTING:
  // 开始重连
  this.setData({
      reconnecting: true,
  });
  break;
case ChannelEventType.RECONNECTED:
  // 重连成功
  this.setData({
      reconnecting: false,
  });
  break;
```

```html
<!-- 网络重连提示 -->
<view class="reconnect-tip" wx:if="{{reconnecting}}">
    <text>网络重连中...</text>
</view>
```

### 退出频道
退出分主动退出和被动(发生不可恢复错误时)退出

```typescript
// 主动退出
await srtc.leave();


// 被动退出
// 在onNotifyChannelEvent里
case ChannelEventType.DISCONNECTED:
  let data = (evt.data as DisconnectEventData);
  wx.showModal({
      content: "你已断开 reason:" + data.reason + ' ' + (data.error ?? ''),
      showCancel: false,
      success: () => {
          // 界面刷新清理，如退出当前界面
          this.navigateBack();
      }
  });
  break;
```

