### 概述

控制本地音视频推流有两种粒度不同的操作，选错方式会导致不必要的资源浪费或功能异常：

| | `enableLocalTrack` / `disableLocalTrack` | `unpublishLocalTrack` / `publishLocalTrack` |
| --- | --- | --- |
| 操作对象 | 已发布的轨道 | 整条发布链路 |
| 底层行为 | 暂停/恢复发送媒体数据，连接保持 | 销毁/重建推流通道 |
| 对远端影响 | 远端收到 `TRACK_MUTED` / `TRACK_UNMUTED` 事件 | 远端收到 `USER_TRACK_REMOVE` / `USER_TRACK_ADD` 事件 |
| 耗时 | 极快（< 10ms） | 较慢（需重新协商，~100ms+） |
| 典型场景 | 临时静音、临时关闭画面 | 彻底停止推流（如离开舞台） |

---

### enableLocalTrack / disableLocalTrack

这两个方法仅控制**媒体数据的发送**，底层 WebRTC 连接仍然保持。适合需要快速切换静音/取消静音的场景。

```typescript
import SRTC, { LocalMicTrack, MicPresets } from '@seastart/srtc-web-sdk';

const srtc = new SRTC();
// 假设已加入频道且 localMicTrack 已发布
let localMicTrack: LocalMicTrack;

// 创建并发布麦克风轨道
localMicTrack = srtc.createLocalMicTrack(MicPresets.music);
await localMicTrack.startCapture();
await srtc.publishLocalTrack(localMicTrack);

// ── 临时静音（不停止采集，不断开推流）────────────────────────────────────────
await srtc.disableLocalTrack(localMicTrack);
// 远端会收到 ChannelEventType.TRACK_MUTED 事件

// ── 取消静音 ──────────────────────────────────────────────────────────────────
await srtc.enableLocalTrack(localMicTrack);
// 远端会收到 ChannelEventType.TRACK_UNMUTED 事件
```

> **注意：** `disableLocalTrack` 后麦克风采集仍在进行（指示灯仍亮），只是不往频道推数据。
> 如果希望完全停止采集以释放麦克风，请使用 `unpublishLocalTrack` + `stopCapture`。

---

### unpublishLocalTrack / publishLocalTrack

彻底停止/重启推流，会触发远端的 `USER_TRACK_REMOVE` / `USER_TRACK_ADD` 事件。适合用户离开舞台、会议中「停止分享」等场景。

```typescript
// ── 停止发布（彻底退出推流）──────────────────────────────────────────────────
await srtc.unpublishLocalTrack(localMicTrack);
localMicTrack.stopCapture();
localMicTrack = undefined;

// ── 重新发布（需要重新创建轨道）──────────────────────────────────────────────
localMicTrack = srtc.createLocalMicTrack(MicPresets.music);
await localMicTrack.startCapture();
await srtc.publishLocalTrack(localMicTrack);
```

---

### 选择建议

+ **会议麦克风静音按钮** → 用 `disableLocalTrack` / `enableLocalTrack`，响应快，体验流畅
+ **停止分享屏幕** → 用 `unpublishLocalTrack` + `stopCapture`，彻底释放资源
+ **摄像头暂时关闭（画面变黑）** → 用 `disableLocalTrack`
+ **摄像头彻底关闭（释放设备）** → 用 `unpublishLocalTrack` + `stopCapture`
