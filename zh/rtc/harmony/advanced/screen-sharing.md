---
title: "屏幕共享"
description: "在 HarmonyOS 上采集屏幕与系统音频、三种采集模式、以及授权窗与常见报错的排查"
---

HarmonyOS 的屏幕采集是**同进程**的 —— 不需要像 iOS 那样单独做一个扩展进程，
也就没有那 50MB 内存上限的约束。

---

### 最小流程

```typescript
import { screenPreset1080p, screenAudioPresetDefault, LocalScreenTrack } from 'srtc';

const screen: LocalScreenTrack = srtc.createLocalScreenTrack(screenPreset1080p());
await screen.startCapture();                        // 会弹系统授权窗
await channel.publishLocalVideoTrack(screen);
```

停止：

```typescript
await channel.unpublishLocalVideoTrack(screen);
await screen.stopCapture();
```

---

### 权限与授权窗

在 `module.json5` 里声明：

```json5
{ "name": "ohos.permission.CAPTURE_SCREEN", "reason": "$string:screen_reason" }
```

<Warning>
**`startCapture()` 返回只代表采集已发起，不代表已经出帧。**

系统会弹窗让用户确认，**用户点同意之后才真正出帧**。UI 上不要在 `await` 返回后就
立刻显示"正在共享"，应该等到第一帧到达（渲染器回调）或用 `onTrackBindRtcTrack` 判断。
</Warning>

<Warning>
**重启采集会再弹一次授权窗。**

鸿蒙的 `AVScreenCapture` 每次 `getDisplayMedia` / `createVideoSource(isScreencast)`
都要用户确认，**拿不到"沿用上次授权"这种待遇**。所以不要为了改参数而随手
`restartCapture()` —— 用户会看到弹窗反复出现。
</Warning>

---

### 三种采集模式

`ScreenCaptureMode` 决定采什么：

| 模式 | 说明 | 需要 `targetId` |
| --- | --- | --- |
| `homeScreen` | 整个主屏，**默认** | 否 |
| `specifiedScreen` | 指定显示器 | 是（显示器 ID） |
| `specifiedWindow` | 指定窗口 | 是（任务 ID） |

```typescript
import { defaultScreenCaptureOptions, ScreenCaptureMode, ScreenCaptureOptions } from 'srtc';

const opts: ScreenCaptureOptions = defaultScreenCaptureOptions();
opts.mode = ScreenCaptureMode.specifiedWindow;
opts.targetId = someMissionId;
await screen.startCapture(opts);
```

<Warning>
**用 `specifiedScreen` / `specifiedWindow` 时 `targetId` 必须有值。**

这两个模式下 SDK 才会把对应的底层约束挂上去。如果模式选了但 `targetId` 是
`undefined`，底层约束解析会失败，抛出来的是一个**既没有 message 也没有 code 的裸
`Error`** —— 上层只看到"共享屏幕失败: "，而且系统的屏幕采集服务根本没被调到。

这个报错**很容易被误判成缺 `ohos.permission.CAPTURE_SCREEN`**（实测补上权限也没用）。
遇到空错误信息时先回头检查 `targetId`。
</Warning>

---

### 采集系统音频

传第二个预设参数即可，系统音频会作为**独立的一条音频轨道**产生：

```typescript
const screen = srtc.createLocalScreenTrack(
  screenPreset1080p(),
  screenAudioPresetDefault()
);
await screen.startCapture();
await channel.publishLocalVideoTrack(screen);

// 系统音频要单独发布
const sysAudio = screen.audioTrack;
if (sysAudio !== undefined) {
  await channel.publishLocalAudioTrack(sysAudio);
}
```

`ScreenAudioCaptureOptions` 有个关键字段：

| 字段 | 说明 |
| --- | --- |
| `excludesCurrentProcessAudio` | 是否排除本进程音频。共享时如果本 App 自己也在放声音，不排除会形成**回环** |

<Note>
系统音频是独立轨道，所以可以单独控制 —— 比如"共享画面但不共享声音"就只发布视频轨。

麦克风与系统音频也是两条独立轨道，鸿蒙上每条音频轨有自己的 `AudioSource`，
不存在 iOS 那种"必须先混成一路"的限制。
</Note>

---

### 编码策略：屏幕与摄像头相反

屏幕内容变化慢、细节多（文字、表格），所以 SDK 内部对屏幕轨道启用
`isScreencast=true`，让编码器切到**保清晰度优先**的策略 —— 宁可掉帧也不糊字。

这与摄像头正相反（摄像头保帧率、宁可降分辨率）。默认帧率也不同：

| 预设 | 分辨率 | 帧率 |
| --- | --- | --- |
| `screenPreset1080p()` | 1920×1080 | 10 |
| `screenPreset720p()` | 1280×720 | 10 |

如果共享的是视频播放画面，可以自己把 `frameRate` 提上去，但要相应提高
`maxBitrate`，否则会更糊。

---

### 横竖屏

SDK 内部开了 `ohosScreenCaptureAutoRotation`，旋转屏幕时采集会自动跟随 ——
否则横竖屏切换后对端画面是躺着的。这一点不需要业务侧处理。

---

### 排查清单

| 现象 | 先查什么 |
| --- | --- |
| 报错信息为空 | `specifiedScreen` / `specifiedWindow` 模式下 `targetId` 是不是 `undefined` |
| 一直不出帧 | 用户是不是没点授权窗；`startCapture` 返回 ≠ 已出帧 |
| 授权窗反复弹 | 是不是在循环里调了 `restartCapture()` |
| 对端画面躺着 | 正常情况下 SDK 已处理，若仍有问题查是不是自己另接了渲染层 |
| 有回声 | `excludesCurrentProcessAudio` 是否为 `true` |
| 对端看不到共享 | 视频轨发布了、系统音频轨是不是漏发了（或反过来） |

排障时先看日志里那条 `请求屏幕采集 WxH@fps mode=... 系统声音=...` ——
有这条说明参数已经组好、走到了系统调用；没有这条说明更早就失败了。

---

### 相关阅读

+ [轨道接口](/zh/rtc/harmony/api-reference/media-tracks)
+ [类型定义](/zh/rtc/harmony/types) —— `ScreenCaptureOptions` / `ScreenAudioCaptureOptions`
+ [错误码](/zh/rtc/harmony/error-codes)
