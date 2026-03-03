---
title: "事件参考"
description: "微信小程序 SRTC 音视频 SDK 全量事件列表与触发时机说明"
---

### 频道内事件
所有频道内事件都可通过`srtc.onNotifyChannelEvent`来监听

```typescript
// 回调事件响应
srtc.onNotifyChannelEvent = (evt: ChannelEvent) => {
  console.log('收到频道事件', evt);
  switch (evt.type) {
      // ...
  }
})
```typescript



`ChannelEvent`定义如下：

```typescript
/** 频道事件通知 */
export declare class ChannelEvent {
	/** 事件类型 */
	type: ChannelEventType;
	/** 事件携带的数据 */
	data?: any;
}
```



`ChannelEventType`及对应`data`定义如下：

```typescript
//
// 频道及连接相关
//

/** 频道自定义props更新，对应data为ChannelInfo */
static readonly CHANNEL_UPDATE = 'channel_update';

/** 开始断线自动重连，无data */
static readonly RECONNECTING = 'reconnecting';

/** 重连成功，断线重连成功后会触发，无data */
static readonly RECONNECTED = 'reconnected';

/** 自己被强制离开频道，对应data为DisconnectEventData */
static readonly DISCONNECTED = 'disconnected';

/** 自己信息被改变，对应data为UserInfo */
static readonly ME_UPDATE = 'me_update';

/** 频道内自定义消息，对应data为CustomMsgData */
static readonly CUSTOM_MSG = 'custom_msg';


//
// 远端用户、远端流相关
//

/** 其他用户加入频道，对应data为UserInfo */
static readonly USER_JOIN = 'user_join';
/** 其他用户信息改变，对应data为UserInfo */
static readonly USER_UPDATE = 'user_update';
/** 其他用户离开频道，对应data为UserLeaveEventData */
static readonly USER_LEAVE = 'user_leave';

/** 其他用户发布流轨道，对应data为{ user: UserInfo, track: TrackInfo } */
static readonly USER_TRACK_ADD = 'user_track_add';
/** 其他用户更新流轨道，对应data为{ user: UserInfo, track: TrackInfo } */
static readonly USER_TRACK_UPDATE = 'user_track_update';
/** 其他用户删除流轨道，对应data为{ user: UserInfo, track: TrackInfo } */
static readonly USER_TRACK_REMOVE = 'user_track_remove';


//
// 弱网相关
//

/** 上行弱网，无data */
static readonly UP_WEAKNET = 'up_weaknet';

/** 上行弱网恢复，无data */
static readonly UP_WEAKNET_RECOVER = 'up_weaknet_recover';

/** 推流失败，对应data为失败描述string */
static readonly UP_PUSH_FAIL = 'up_push_fail';

/** 下行弱网，对应data为{track: BaseTrack} */
static readonly DOWN_WEAKNET = 'down_weaknet';

/** 下行弱网恢复，对应data为{track: BaseTrack} */
static readonly DOWN_WEAKNET_RECOVER = 'down_weaknet_recover';

/** 拉流播放失败，对应data为{track: BaseTrack, detail: string} */
static readonly DOWN_PLAY_FAIL = 'down_play_fail';

```typescript

### 
### 频道外消息事件
所有频道外事件都可通过`srtc.onNotifyImEvent`来监听

```typescript
srtc.onNotifyImEvent = (evt: ImEvent) => {
    console.log('收到im事件', evt);
    switch (evt.type) {
        case ImEventType.IM_MSG:
          // 收到im消息
          // evt.data as ImMsgData
          break;
        case ImEventType.RECONNECTING:
          // 开始重连
          break;
        case ImEventType.RECONNECTED:
          // 重连成功
          break;
        case ImEventType.DISCONNECTED:
          let data = (evt.data as ImDisconnectEventData);
          // 可根据reason提示退出原因
          alert('im已断开 reason:' + data.reason);
          // 界面刷新清理
          imSid = "";
          break;
    }
}
```



`ImEvent`定义如下：

```typescript
/** 频道外事件通知 */
export declare class ImEvent {
	/** 事件类型 */
	type: ImEventType;
	/** 事件携带的数据 */
	data?: any;
}
```typescript



`ImEventType`及对应`data`定义如下：

```typescript
/** 频道外事件类型 */
declare class ImEventType {
	/** 首次连接im成功，无data */
	static readonly ENABLE_SUCCEED = "enable_succeed";
	/** im开始断线自动重连，无data */
	static readonly RECONNECTING = "reconnecting";
	/** im重连成功，断线重连成功后会触发 */
	static readonly RECONNECTED = "reconnected";
	/** 自己被强制断开im，对应data为ImDisconnectEventData */
	static readonly DISCONNECTED = "disconnected";
	/** im消息，对应data为ImMsgData */
	static readonly IM_MSG = "im_msg";
}
```

