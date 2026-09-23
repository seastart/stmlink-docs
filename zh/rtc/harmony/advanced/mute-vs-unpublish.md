---
title: "静音与停止发布"
description: "mute / unmute 与 unpublish + stopCapture 的语义差别，以及麦克风与摄像头为什么用法不同"
---

关麦和关摄像头在 SDK 里是**两套不同的动作**，选错了会出现"对端以为你退会了"或者
"摄像头指示灯一直亮"这类问题。

---

### 三种"关"的语义

| 动作 | 采集 | 发布关系 | 对端看到 | 恢复成本 |
| --- | --- | --- | --- | --- |
| `mute()` | 继续 | 保持 | 轨道仍在，但静音 | 瞬时 |
| `unpublish` | 继续 | 断开 | 轨道消失 | 需重新协商 |
| `unpublish` + `stopCapture()` | 停止 | 断开 | 轨道消失 | 需重新采集 + 协商 |

---

### 麦克风：用 `mute` / `unmute`

```typescript
const mic = srtc.createLocalMicTrack(micPresetMusic());
await mic.startCapture();
await channel.publishLocalAudioTrack(mic);

mic.mute();      // 关麦
mic.unmute();    // 开麦
```

**不要**为了关麦去 `unpublish` + `stopCapture`。原因：

+ 用户预期是"我静音了，但还在会里" —— 轨道消失会让对端的成员列表状态错乱
+ 重新发布要走一遍 SDP 协商，开关麦这种高频操作扛不住这个开销
+ `mute` 在鸿蒙上就是把自己那条音频源的音量设 0，**不影响其它轨道**

<Note>
鸿蒙的每条音频轨道都有**独立的 `AudioSource`**，所以按轨道静音互不干扰。
这一点和 iOS / macOS 不同 —— 那边所有音频源要先混成一路再发。
</Note>

---

### 摄像头：用 `unpublish` + `stopCapture`

```typescript
// 关摄像头
await channel.unpublishLocalVideoTrack(camera);
await camera.stopCapture();

// 重新开：要重新创建轨道
const camera2 = srtc.createLocalCameraTrack(cameraPreset720p());
await camera2.startCapture();
await channel.publishLocalVideoTrack(camera2);
```

为什么摄像头不用 `mute`：

+ 用户预期是"关了摄像头就该真的关" —— **摄像头指示灯必须熄灭**，只发黑帧不行
+ 视频轨道留在会里但推黑帧，会白占带宽和对端的渲染格子

---

### 只采集、不发布

这是个有用的中间态：本地能看到画面，但不推流。

```typescript
const camera = srtc.createLocalCameraTrack(cameraPreset720p());
await camera.startCapture();   // 到这里本地预览已经能显示了
// 不调 publishLocalVideoTrack
```

用途：

+ **入会前的设备自检**：不需要服务端就能验证采集和渲染链路
+ 「摄像头预览 + 用户确认后再入会」的交互

---

### 换设备或改采集参数：必须重新发布

```typescript
// ❌ 错的：轨道换了底层 source，但发布关系还指着旧的
await mic.changeDeviceId(newDeviceId);

// ✅ 对的
await channel.unpublishLocalAudioTrack(mic);
await mic.changeDeviceId(newDeviceId);
await channel.publishLocalAudioTrack(mic);
```

<Warning>
`changeDeviceId()` 与 `restartCapture()` **会换一条底层轨道**。已发布的轨道不重新发布，
对端收到的还是旧轨道（表现为换了麦克风但对方听到的没变）。

静音状态会自动保留 —— `startCapture` 内部会回放 `isMutedByUser`，不用自己记。
</Warning>

---

### 远端音频：停播放 ≠ 退订

对**远端**音频还有第三组选择：

```typescript
// 只停本地播放，仍在订阅（带宽照旧消耗，切回来是瞬时的）
channel.setUserAudioPlayback(uid, false);
channel.setRemoteAudioPlayback(false);          // 全体

// 真正退订（省带宽，但恢复要重新协商）
await channel.unsubscribeRemoteTrack(track, 0);
```

| 场景 | 该用哪个 |
| --- | --- |
| 用户点了"扬声器关闭" | `setRemoteAudioPlayback(false)` |
| 用户把某人"本地静音" | `setUserAudioPlayback(uid, false)` |
| 成员划出可见区域、长时间不看 | `unsubscribeRemoteTrack` |

`channel.isUserAudioMuted(uid)` 和 `getMutedAudioUids()` 用来回读本地静音状态。

---

### 相关阅读

+ [轨道接口](/zh/rtc/harmony/api-reference/media-tracks)
+ [设备管理](/zh/rtc/harmony/advanced/device-management)
+ [多频道](/zh/rtc/harmony/advanced/multi-channel)
