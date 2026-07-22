---
title: "快速开始"
description: "Web SRTC 音视频 SDK 快速集成，10 分钟跑通基础功能"
---

### 前提条件

+ 已完成 [SDK 集成](/zh/rtc/web/integration)
+ 已从服务端获取加入频道的 Token（通过你自己的后台调用服务端 API 生成）
+ 页面运行在 HTTPS 或 localhost 环境下

---

### 完整示例

以下代码展示了一个最小可运行的音视频通话流程：初始化 → 环境检测 → 监听事件 → 加入频道 → 订阅混音 → 订阅远端视频 → 开麦克风 → 开摄像头 → 离开频道。

```typescript
import SRTC, {
  ChannelEventType,
  LocalCameraTrack,
  LocalMicTrack,
  MicPresets,
  CameraPresets,
  RemoteAudioMixTrack,
  RemoteVideoTrack,
  TrackKind,
  LogLevel,
  LogTarget,
} from '@seastart/srtc-web-sdk';
import type { ChannelEvent, TrackInfo } from '@seastart/srtc-web-sdk';

// ─── 1. 初始化 SDK ───────────────────────────────────────────────────────────

const srtc = new SRTC({
  logLevel: LogLevel.DEBUG,
  logTarget: LogTarget.CONSOLE,
});

// ─── 2. 检测运行环境 ─────────────────────────────────────────────────────────

const env = srtc.getEnvInfo();
if (!env.supported) {
  alert('当前浏览器不支持 WebRTC，请使用最新版 Chrome');
  // 停止后续流程
}

// ─── 3. 注册事件监听 ─────────────────────────────────────────────────────────

let remoteAudioMixTrack: RemoteAudioMixTrack | undefined;
let localMicTrack: LocalMicTrack | undefined;
let localCameraTrack: LocalCameraTrack | undefined;
// 已订阅的远端视频轨道，key 为 `${uid}-${trackId}`
const remoteVideoTracks: Record<string, RemoteVideoTrack> = {};

// 订阅远端视频轨道并渲染到页面（远端音频统一走第 5 步的全频道混音，无需单独订阅）
async function subscribeRemoteVideo(uid: string, trackInfo: TrackInfo) {
  const remoteVideoTrack = await srtc.subscribeRemoteVideoTrack(uid, trackInfo.id);
  remoteVideoTracks[`${uid}-${trackInfo.id}`] = remoteVideoTrack;
  // 将画面渲染到该用户对应的容器（容器元素需自行创建）
  remoteVideoTrack.addPlayView(document.querySelector<HTMLElement>(`#remote-video-${uid}`)!);
}

srtc.onNotifyChannelEvent = async (evt: ChannelEvent) => {
  switch (evt.type) {
    case ChannelEventType.USER_TRACK_ADD: {
      // 远端用户发布了新轨道，订阅其中的视频轨道
      const { user, track } = evt.data;
      if (track.kind === TrackKind.Video) {
        await subscribeRemoteVideo(user.uid, track);
      }
      break;
    }

    case ChannelEventType.USER_TRACK_REMOVE: {
      // 远端用户停止发布，SDK 已自动取消订阅，这里只需清理本地引用和界面
      const { user, track } = evt.data;
      delete remoteVideoTracks[`${user.uid}-${track.id}`];
      break;
    }

    case ChannelEventType.RECONNECTING:
      console.warn('网络断开，正在重连...');
      break;

    case ChannelEventType.RECONNECTED:
      console.warn('重连成功');
      break;

    case ChannelEventType.DISCONNECTED:
      console.error('已断开连接', evt.data);
      // 清理本地状态，刷新界面
      break;

    case ChannelEventType.TRACK_ENDED:
      // 设备被拔出或屏幕共享被用户停止时触发
      console.warn('轨道已停止', evt.data);
      break;

    case ChannelEventType.TRACK_AUTOPLAY_FAIL:
      // 浏览器阻止了自动播放，需要在用户手势后重新调用 startPlay
      console.warn('自动播放失败，请在用户交互后重试', evt.data);
      break;
  }
};

// ─── 4. 加入频道 ─────────────────────────────────────────────────────────────

// token 由你的后台服务签发
const token = '从服务端获取的加入频道 token';
const channelInfo = await srtc.join(token);
console.log('已加入频道', channelInfo.channel);

// ─── 5. 订阅全频道混音（收听远端声音）────────────────────────────────────────

remoteAudioMixTrack = await srtc.subscribeRemoteAudioMixTrack();
await remoteAudioMixTrack.startPlay();

// ─── 6. 订阅频道内已有用户的视频 ─────────────────────────────────────────────

// USER_TRACK_ADD 只通知加入后新发布的轨道；对加入前就在推流的用户，需主动遍历订阅
// （getUsersInfo 返回的列表包含自己，此时自己尚未发布任何轨道，无需特殊处理）
for (const user of srtc.getUsersInfo(false)) {
  for (const track of user.stream_tracks ?? []) {
    if (track.kind === TrackKind.Video) {
      await subscribeRemoteVideo(user.uid, track);
    }
  }
}

// ─── 7. 打开麦克风 ───────────────────────────────────────────────────────────

localMicTrack = srtc.createLocalMicTrack(MicPresets.music);
await localMicTrack.startCapture();
await srtc.publishLocalTrack(localMicTrack);

// ─── 8. 打开摄像头 ───────────────────────────────────────────────────────────

localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['720p']);
await localCameraTrack.startCapture();
// 本地预览：将画面渲染到指定容器
localCameraTrack.addPlayView(document.querySelector<HTMLElement>('#local-video')!);
await srtc.publishLocalTrack(localCameraTrack);

// ─── 9. 离开频道（在页面卸载或用户主动离开时调用）────────────────────────────

async function leaveChannel() {
  if (localMicTrack) {
    await srtc.unpublishLocalTrack(localMicTrack);
    localMicTrack.stopCapture();
    localMicTrack = undefined;
  }
  if (localCameraTrack) {
    await srtc.unpublishLocalTrack(localCameraTrack);
    localCameraTrack.removeAllPlayViews();
    localCameraTrack.stopCapture();
    localCameraTrack = undefined;
  }
  // 远端轨道随 leave 自动取消订阅，这里只需清理渲染容器和本地引用
  for (const [key, track] of Object.entries(remoteVideoTracks)) {
    track.removeAllPlayViews();
    delete remoteVideoTracks[key];
  }
  await srtc.leave();
  console.log('已离开频道');
}
```

---

### 下一步

+ [核心概念](/zh/rtc/web/key-concepts) — 了解 SRTC 实例、频道、Track 体系
+ [静音 vs 停止发布](/zh/rtc/web/advanced/mute-vs-unpublish) — 两种控制推流的方式对比
+ [大小流与分辨率](/zh/rtc/web/advanced/video-stream-layers) — 讲清采集分辨率、`camera_big`、`camera_small` 与 simulcast
+ [屏幕共享](/zh/rtc/web/advanced/screen-sharing) — 含系统音频采集
+ [自定义推流](/zh/rtc/web/advanced/custom-track) — 使用 Canvas / 自定义 MediaStreamTrack
+ [接口文档 - SRTC](/zh/rtc/web/api-reference/SRTC) — 完整 API 参考
