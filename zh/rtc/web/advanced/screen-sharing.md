### 基本屏幕共享

屏幕共享使用 `LocalScreenTrack`，流程与摄像头类似：

```typescript
import SRTC, {
  LocalScreenTrack,
  ScreenPresets,
  ChannelEventType,
} from '@seastart/srtc-web-sdk';

const srtc = new SRTC();
let localScreenTrack: LocalScreenTrack | undefined;

const openScreen = async () => {
  // 创建屏幕共享轨道，使用 1080p 预设
  localScreenTrack = srtc.createLocalScreenTrack(ScreenPresets['1080p']);

  // 开始采集（浏览器会弹出屏幕选择弹窗）
  await localScreenTrack.startCapture();

  // 本地预览（可选）
  localScreenTrack.addPlayView(document.querySelector<HTMLElement>('#screen-preview')!);

  // 发布
  await srtc.publishLocalTrack(localScreenTrack, { desc: 'screen' });
};

const closeScreen = async () => {
  if (!localScreenTrack) return;
  await srtc.unpublishLocalTrack(localScreenTrack);
  localScreenTrack.removeAllPlayViews();
  localScreenTrack.stopCapture();
  localScreenTrack = undefined;
};
```

---

### 处理浏览器内置"停止共享"按钮

用户点击浏览器底部"停止共享"按钮时，SDK 会触发 `TRACK_ENDED` 事件，你需要在事件回调中清理状态：

```typescript
srtc.onNotifyChannelEvent = async (evt) => {
  if (evt.type === ChannelEventType.TRACK_ENDED) {
    if (evt.data === localScreenTrack) {
      // 用户点了浏览器的"停止共享"，主动清理
      await closeScreen();
      // 更新你的 UI 状态（如隐藏"共享中"提示）
    }
  }
};
```

---

### 同时采集系统音频

部分浏览器（Chrome 74+，Windows/macOS）支持在屏幕共享时同时采集**系统声音**（如视频播放的音频）。

`createLocalScreenTrack` 接受第二个参数 `audioPreset`，传入后 SDK 会在系统支持时同时采集系统音频：

```typescript
import SRTC, {
  LocalScreenTrack,
  ScreenPresets,
  ScreenAudioPresets,
} from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

// 创建屏幕共享轨道，同时请求采集系统音频
const localScreenTrack = srtc.createLocalScreenTrack(
  ScreenPresets['1080p'],
  ScreenAudioPresets.default,  // 第二参数：系统音频预设
);

await localScreenTrack.startCapture();

// 获取系统音频轨道（如果浏览器支持且用户勾选了"分享音频"）
const screenAudioTrack = localScreenTrack.getAudioTrack();
if (screenAudioTrack) {
  // 将系统音频也发布到频道
  await srtc.publishLocalTrack(screenAudioTrack, { desc: 'screen_audio' });
  console.log('系统音频已发布');
} else {
  console.warn('当前环境不支持采集系统音频，或用户未勾选"分享音频"');
}

// 发布屏幕共享视频
await srtc.publishLocalTrack(localScreenTrack, { desc: 'screen' });
```

> **注意：**
> + 系统音频采集仅在 Chrome（Windows/macOS）下稳定支持
> + Safari、Firefox 不支持系统音频采集
> + 用户在浏览器弹窗中必须勾选"分享音频"，`getAudioTrack()` 才会返回有效轨道
> + 停止共享时，记得同时 `unpublishLocalTrack(screenAudioTrack)` 并 `stopCapture()`

---

### ScreenCaptureOptions 参数说明

调用 `localScreenTrack.startCapture(options)` 时可以传入以下参数：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `width` | `number` | 期望采集宽度 |
| `height` | `number` | 期望采集高度 |
| `frameRate` | `number` | 期望帧率 |
| `contentHint` | `'motion' \| 'detail' \| 'text'` | 内容类型提示，影响编码策略：`motion` 适合视频/游戏，`detail` 适合图片/图形，`text` 适合文档/代码 |
| `showCursor` | `'always' \| 'motion' \| 'never'` | 是否显示鼠标指针 |

```typescript
await localScreenTrack.startCapture({
  frameRate: 15,
  contentHint: 'detail',  // 共享文档/代码时使用，提升清晰度
  showCursor: 'always',
});
```

---

### 预设参数（ScreenPresets）

| 预设名 | 分辨率 | 帧率 | 码率 | 说明 |
| --- | :---: | :---: | :---: | --- |
| `ScreenPresets['1080p']` | 1920×1080 | 10 fps | 2 Mbps | 默认预设 |
| `ScreenPresets['720p']` | 1280×720 | 10 fps | 1.5 Mbps | |
