---
title: "大小流与分辨率"
description: "Web SRTC 音视频 SDK 中摄像头分辨率、大小流与 simulcast 的使用说明"
---

### 先说结论

`rtc-js` 里用户最容易混淆的，其实是两件不同的事：

+ **采集分辨率**：决定摄像头采上来的原始画面有多大
+ **发布大小流**：决定是否把同一份画面编码成多层一起发出去

从第一性原理看，**“小流”不是另一台摄像头，也不是单独的一种模式**，它本质上只是同一条视频轨道的低分辨率编码层。

所以：

+ 想把画面采得更清楚，改的是**采集参数**
+ 想控制“发一层还是发两层”，改的是**发布参数里的 `simulcasts`**
+ 想“只发小流”，本质上不是“开启小流模式”，而是**只发一条低分辨率单流**

---

### SDK 默认行为

Web SDK 内置摄像头预设里，默认行为如下：

+ `CameraPresets['720p']`：默认发布 `camera_big + camera_small`
+ `CameraPresets['1080p']`：默认发布 `camera_big + camera_small`
+ `CameraPresets['360p']` / `CameraPresets['180p']`：不带默认 simulcast 配置

当前内置小流参数为：

| 流层 | `desc` | 分辨率 | 帧率 | 码率 |
| --- | --- | --- | --- | --- |
| 大流 | `camera_big` | 跟随主预设 | 跟随主预设 | 跟随主预设 |
| 小流 | `camera_small` | 320 × 180 | 15 fps | 250 Kbps |

这意味着如果你直接这样写：

```typescript
const localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['720p']);
await localCameraTrack.startCapture();
await srtc.publishLocalTrack(localCameraTrack);
```

默认就已经是在发：

+ 一路 `camera_big`
+ 一路 `camera_small`

---

### 概念拆开看

#### 1. 采集分辨率

采集分辨率由 `createLocalCameraTrack(...)` 的预设，或 `startCapture(...)` 传入的参数决定：

```typescript
const localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['1080p']);

await localCameraTrack.startCapture({
  width: 1920,
  height: 1080,
  frameRate: 15,
});
```

它影响的是“源头有多清楚”。

#### 2. 发布大小流

发布大小流由 `publishLocalTrack(...)` 时的 `VideoPublishOptions.simulcasts` 决定：

```typescript
await srtc.publishLocalTrack(localCameraTrack, {
  desc: 'camera_big',
  width: 1280,
  height: 720,
  maxBitrate: 1_200_000,
  maxFramerate: 15,
  simulcasts: [
    {
      desc: 'camera_small',
      width: 320,
      height: 180,
      maxBitrate: 250_000,
      maxFramerate: 15,
    },
  ],
});
```

它影响的是“往频道里发几层编码”。

> **关键点：**
> 只改采集分辨率，不会自动关闭小流；
> 只改 `simulcasts`，也不会改变摄像头实际采集分辨率。

---

### 场景一：想改大流分辨率，但仍然保留大小流

这是最常见需求。做法是：

+ 先把摄像头采集分辨率调到目标值
+ 再保留 `simulcasts`

例如把大流改成 1080p，同时继续发一条 320 × 180 的小流：

```typescript
import SRTC, { CameraPresets } from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

const localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['1080p']);
await localCameraTrack.startCapture();

// 使用 1080p 预设时，默认就会带 camera_small
await srtc.publishLocalTrack(localCameraTrack);
```

如果你想自定义小流参数，也可以显式覆盖：

```typescript
await srtc.publishLocalTrack(localCameraTrack, {
  desc: 'camera_big',
  width: 1920,
  height: 1080,
  maxBitrate: 2_500_000,
  maxFramerate: 15,
  // 核心逻辑：同一条摄像头轨道再编码出一条更低规格的副层
  simulcasts: [
    {
      desc: 'camera_small',
      width: 480,
      height: 270,
      maxBitrate: 350_000,
      maxFramerate: 15,
    },
  ],
});
```

---

### 场景二：只发大流，不发小流

这时不要只改 `width / height`，而是要把 `simulcasts` 显式清空。

```typescript
import SRTC, { CameraPresets } from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

const localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['720p']);
await localCameraTrack.startCapture();

await srtc.publishLocalTrack(localCameraTrack, {
  desc: 'camera_big',
  // 核心逻辑：清空 simulcasts，表示只发主层
  simulcasts: [],
});
```

适用场景：

+ 频道规模很小，不需要多层切换
+ 业务只消费一路主画面
+ 想减少上行编码和带宽开销

> **注意：**
> `CameraPresets['720p']` / `['1080p']` 默认带小流。
> 如果你的目标是“只发大流”，就必须显式传 `simulcasts: []` 覆盖默认值。

---

### 场景三：只发一条低清流

很多人说的“只发小流”，如果从编码原理上说，真正想要的通常是：

+ 不发 `camera_big`
+ 只发一条低分辨率单流

这时不要用“720p 大流 + 小流”的思路，而是直接创建一条低分辨率摄像头轨道并只发布这一层：

```typescript
import SRTC from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

const localCameraTrack = srtc.createLocalCameraTrack({
  capture: {
    width: 320,
    height: 180,
    frameRate: 15,
  },
  publish: {
    desc: 'camera_small',
    width: 320,
    height: 180,
    maxBitrate: 250_000,
    maxFramerate: 15,
  },
});

await localCameraTrack.startCapture();
await srtc.publishLocalTrack(localCameraTrack);
```

这个方案的本质是：

+ 只有一条视频轨
+ 这条轨的规格就是低清
+ 它叫不叫 `camera_small` 只是业务语义命名，底层并不是“大流里的副层被单独打开”

---

### 场景四：自定义大小流参数

如果默认的 `320 × 180 / 250 Kbps` 不适合你的业务，可以直接自定义：

```typescript
const localCameraTrack = srtc.createLocalCameraTrack({
  capture: {
    width: 1280,
    height: 720,
    frameRate: 15,
  },
  publish: {
    desc: 'camera_big',
    width: 1280,
    height: 720,
    maxBitrate: 1_200_000,
    maxFramerate: 15,
    simulcasts: [
      {
        desc: 'camera_small',
        width: 640,
        height: 360,
        maxBitrate: 400_000,
        maxFramerate: 15,
      },
    ],
  },
});

await localCameraTrack.startCapture();
await srtc.publishLocalTrack(localCameraTrack);
```

建议：

+ 主层分辨率先按实际业务 UI 需要决定，不要盲目追求 1080p
+ 小层优先服务于缩略图、小窗、宫格，因此分辨率和码率都应明显低于主层
+ 如果频道里经常出现弱网或多路视频同屏，保留小流通常比只发大流更稳

---

### 不建议的用法

#### 不要手动创建两条摄像头轨道来模拟大小流

例如下面这种思路不建议：

```typescript
const bigTrack = srtc.createLocalCameraTrack(CameraPresets['720p']);
const smallTrack = srtc.createLocalCameraTrack({
  capture: { width: 320, height: 180, frameRate: 15 },
  publish: { desc: 'camera_small', width: 320, height: 180, maxBitrate: 250_000 },
});
```

原因很直接：

+ 它会变成两条独立业务轨道，而不是同一条视频的多编码层
+ 远端需要分别处理两条流，语义更乱
+ 本地采集、编码、带宽开销也更高

正确做法是：

+ 需要大小流时，用**一条摄像头轨道 + `simulcasts`**
+ 只需要低清单流时，直接发**一条低清主流**

---

### 远端如何理解大小流

远端看到的 `TrackInfo` 里，关键字段有两个：

+ `fallback_ids`：主层可降级到哪些更低层
+ `variant`：是否为 simulcast 副层

通常业务层应遵循这个规则：

+ **优先订阅主层轨道**
+ 不要把 `variant === true` 的副层当成一条普通新视频单独展示

SDK 在自动订阅时也遵循这个原则：会跳过副层，真正的层切换交给 SFU 和 `fallback_ids` 处理。

---

### 选择建议

| 需求 | 推荐做法 |
| --- | --- |
| 想把主画面从 720p 改成 1080p | 改摄像头预设或 `startCapture` 参数 |
| 想继续保留大小流 | 保留 `simulcasts`，或直接用 `CameraPresets['720p'] / ['1080p']` |
| 想只发大流 | `publishLocalTrack(..., { simulcasts: [] })` |
| 想只发一条低清流 | 直接创建低分辨率单流，不要走双层编码 |
| 想单独调整小流规格 | 自定义 `simulcasts` 数组 |

---

### 相关文档

+ [核心概念](/zh/rtc/web/key-concepts)
+ [SRTC 接口参考](/zh/rtc/web/api-reference/SRTC)
+ [类型定义](/zh/rtc/web/types#videopublishoptions)
+ [media-tracks 接口参考](/zh/rtc/web/api-reference/media-tracks)
