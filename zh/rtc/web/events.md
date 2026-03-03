### 频道内事件（onNotifyChannelEvent）

通过 `srtc.onNotifyChannelEvent` 注册回调，在 `join` 前设置：

```typescript
srtc.onNotifyChannelEvent = (evt: ChannelEvent) => {
  switch (evt.type) {
    case ChannelEventType.USER_JOIN:
      // evt.data as UserInfo
      break;
    // ...
  }
};
```

---

#### 频道与连接

| 事件常量 | 字符串值 | 触发时机 | data 类型 |
| --- | --- | --- | --- |
| `CHANNEL_UPDATE` | `'channel_update'` | 频道自定义属性（props）被更新 | `ChannelInfo` |
| `ME_UPDATE` | `'me_update'` | 自己的用户信息被服务端或管理员更新 | `UserInfo` |
| `RECONNECTING` | `'reconnecting'` | 网络波动，开始自动重连 | 无 |
| `RECONNECTED` | `'reconnected'` | 重连成功 | 无 |
| `DISCONNECTED` | `'disconnected'` | 被强制踢出或发生不可恢复错误 | `DisconnectEventData` |
| `CUSTOM_MSG` | `'custom_msg'` | 收到频道内自定义消息 | `CustomMsgData` |

---

#### 远端用户与流

| 事件常量 | 字符串值 | 触发时机 | data 类型 |
| --- | --- | --- | --- |
| `USER_JOIN` | `'user_join'` | 远端用户加入频道 | `UserInfo` |
| `USER_UPDATE` | `'user_update'` | 远端用户信息更新 | `UserInfo` |
| `USER_LEAVE` | `'user_leave'` | 远端用户离开频道 | `UserLeaveEventData` |
| `USER_TRACK_ADD` | `'user_track_add'` | 远端用户发布了新轨道 | `{ user: UserInfo, track: TrackInfo }` |
| `USER_TRACK_UPDATE` | `'user_track_update'` | 远端用户更新了轨道信息 | `{ user: UserInfo, track: TrackInfo }` |
| `USER_TRACK_REMOVE` | `'user_track_remove'` | 远端用户停止发布了某轨道 | `{ user: UserInfo, track: TrackInfo }` |

> SDK 内部会在远端用户离开时（`USER_LEAVE`）自动取消订阅该用户的所有轨道；在 `USER_TRACK_REMOVE` 时自动取消订阅对应轨道。

---

#### 轨道与外设

| 事件常量 | 字符串值 | 触发时机 | data 类型 |
| --- | --- | --- | --- |
| `TRACK_MUTED` | `'track_muted'` | 某轨道暂停发送数据（静音/画面暂停） | `BaseTrack` |
| `TRACK_UNMUTED` | `'track_unmuted'` | 某轨道恢复发送数据 | `BaseTrack` |
| `TRACK_ENDED` | `'track_ended'` | 轨道停止（设备拔出 / 用户点击浏览器"停止共享"） | `BaseTrack` |
| `TRACK_AUTOPLAY_FAIL` | `'track_autoplay_fail'` | 浏览器阻止自动播放，需在用户手势后重新调用 `startPlay` | `BaseTrack` |
| `DEVICE_ADD` | `'device_add'` | 外设插入 | `MediaDeviceInfo` |
| `DEVICE_REMOVE` | `'device_remove'` | 外设拔出 | `MediaDeviceInfo` |

---

### 频道外消息事件（onNotifyImEvent）

通过 `srtc.onNotifyImEvent` 注册回调（需先调用 `srtc.enableIm(token)` 启用 IM）：

```typescript
srtc.onNotifyImEvent = (evt: ImEvent) => {
  switch (evt.type) {
    case ImEventType.IM_MSG:
      // evt.data as ImMsgData
      break;
  }
};
```

| 事件常量 | 字符串值 | 触发时机 | data 类型 |
| --- | --- | --- | --- |
| `ENABLE_SUCCEED` | `'enable_succeed'` | IM 首次连接成功 | 无 |
| `IM_MSG` | `'im_msg'` | 收到 IM 消息 | `ImMsgData` |
| `RECONNECTING` | `'reconnecting'` | IM 连接断开，开始重连 | 无 |
| `RECONNECTED` | `'reconnected'` | IM 重连成功 | 无 |
| `DISCONNECTED` | `'disconnected'` | IM 被强制断开 | `ImDisconnectEventData` |
