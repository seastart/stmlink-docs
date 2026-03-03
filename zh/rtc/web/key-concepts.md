### SRTC 实例

通过 `new SRTC(initParams)` 创建实例，绝大多数操作都通过该实例对外提供。

+ 每个实例对应一个频道连接
+ 若需同时加入多个频道，需创建多个实例
+ 所有频道内事件通过 `srtc.onNotifyChannelEvent` 回调通知

```typescript
import SRTC, { LogLevel, LogTarget } from '@seastart/srtc-web-sdk';

const srtc = new SRTC({
  logLevel: LogLevel.DEBUG,   // 开发阶段建议使用 DEBUG
  logTarget: LogTarget.CONSOLE,
});
```

---

### 频道（Channel）与 Token

**频道**是一次多人音视频会话的容器，由频道名唯一标识。加入同一频道的用户可以互相收发音视频流。

**Token** 是加入频道的凭证，由你的服务端通过 StmLink 服务端 API 签发，携带了频道名、用户 ID、权限等信息。每次加入频道都需要传入有效的 Token。

```typescript
// 从后台获取 token 后调用 join
const channelInfo = await srtc.join(token);
console.log(channelInfo.channel); // 频道名
```

加入后可随时通过以下方法获取频道和用户信息：

```typescript
// 获取当前频道信息
const channelInfo = srtc.getChannelInfo();

// 获取频道内某用户信息
const userInfo = srtc.getUserInfo(uid);

// 获取频道内所有用户（map 形式）
const usersMap = srtc.getUsersInfo(true);   // Record<uid, UserInfo>

// 获取频道内所有用户（数组形式）
const usersArr = srtc.getUsersInfo(false);  // UserInfo[]
```

---

### Track 体系

Track（轨道）是音视频数据的最小单元，每一路音频或视频都是一个 Track。

#### 继承关系

```
BaseTrack
├── LocalAudioTrack          ← 本地音频基类（自定义音频流）
│   └── LocalMicTrack        ← 麦克风流
├── LocalVideoTrack          ← 本地视频基类（自定义视频流）
│   ├── LocalCameraTrack     ← 摄像头流
│   └── LocalScreenTrack     ← 屏幕共享流
├── RemoteAudioTrack         ← 远端单路音频流
│   └── RemoteAudioMixTrack  ← 远端全频道混音流
└── RemoteVideoTrack         ← 远端视频流
```

#### 分类说明

| Track 类型 | 创建方式 | 说明 |
| --- | --- | --- |
| `LocalMicTrack` | `srtc.createLocalMicTrack()` | 麦克风采集，支持切换设备 |
| `LocalCameraTrack` | `srtc.createLocalCameraTrack()` | 摄像头采集，支持切换设备 |
| `LocalScreenTrack` | `srtc.createLocalScreenTrack()` | 屏幕共享，可同时采集系统音频 |
| `LocalAudioTrack` | `srtc.createLocalCustomAudioTrack(msTrack)` | 自定义音频，传入 `MediaStreamTrack` |
| `LocalVideoTrack` | `srtc.createLocalCustomVideoTrack(msTrack)` | 自定义视频，传入 `MediaStreamTrack` |
| `RemoteAudioMixTrack` | `srtc.subscribeRemoteAudioMixTrack()` | 全频道混音，一般场景只需订阅这一路 |
| `RemoteAudioTrack` | `srtc.subscribeRemoteAudioTrack(uid, id)` | 订阅指定用户的单路音频 |
| `RemoteVideoTrack` | `srtc.subscribeRemoteVideoTrack(uid, id)` | 订阅指定用户的视频 |

#### 本地 Track 生命周期

```
createLocalXxxTrack()
  → startCapture()        // 开始采集（请求摄像头/麦克风权限）
  → publishLocalTrack()   // 发布到频道（其他用户可以订阅）
  → unpublishLocalTrack() // 停止发布（其他用户看不到，但本地仍在采集）
  → stopCapture()         // 停止采集，释放设备
```

---

### 事件系统

SRTC 提供两套事件回调：

#### 频道内事件（onNotifyChannelEvent）

监听频道连接状态、远端用户进出、远端轨道变化、本地设备状态等事件：

```typescript
srtc.onNotifyChannelEvent = (evt: ChannelEvent) => {
  switch (evt.type) {
    case ChannelEventType.USER_JOIN:
      // 远端用户加入，evt.data 为 UserInfo
      break;
    case ChannelEventType.USER_TRACK_ADD:
      // 远端用户发布了新轨道，evt.data 为 { user: UserInfo, track: TrackInfo }
      break;
    // ... 更多事件详见《事件参考》
  }
};
```

#### 频道外消息事件（onNotifyImEvent）

监听 IM 消息（需先调用 `srtc.enableIm(token)` 启用）：

```typescript
srtc.onNotifyImEvent = (evt: ImEvent) => {
  if (evt.type === ImEventType.IM_MSG) {
    // evt.data 为 ImMsgData
  }
};
```

完整事件列表详见 [事件参考](/zh/rtc/web/events)。

---

### 观众模式（is_audience）

`UserInfo.is_audience` 为 `true` 时，表示该用户以观众身份加入频道：

+ 观众只接收音视频流，**不能发布**本地轨道
+ 是否以观众身份加入，由服务端签发 Token 时决定
+ 可通过 `ChannelEventType.ME_UPDATE` 事件感知自己的观众状态变化
