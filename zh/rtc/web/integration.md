---
title: "集成"
description: "Web SRTC 音视频 SDK 环境配置与 SDK 安装指南"
---

### 支持的浏览器

SRTC Web SDK 支持主流桌面端及移动端浏览器：

| 浏览器 | 最低版本 | 说明 |
| --- | :---: | --- |
| Chrome | 72+ | 推荐，全功能支持 |
| Edge | 79+ | 基于 Chromium |
| Firefox | 66+ | 不支持指定扬声器输出 |
| Safari | 14+ | 不支持屏幕共享系统音频 |
| 微信内嵌浏览器 | iOS 14.3+ / Android | 支持收发。iOS 低于 14.3 的旧系统仅支持收流 |
| 移动端 Chrome / Safari | 最新版 | 支持基本音视频通话 |

> **提示：** 建议用户使用最新版 Chrome 以获得最佳体验。

---

### 微信小程序场景

需要在微信小程序里接入音视频时，**推荐用小程序的 `<web-view>` 嵌入一个基于本 Web SDK 实现的页面**，而不是再单独做一套小程序原生实现。这样一套 Web 代码同时覆盖浏览器端和小程序端，功能和后续迭代自然保持一致，维护成本最低。

接入要点：

+ 被嵌入的页面必须是 **HTTPS**，且其域名需要在小程序管理后台配置为**业务域名**并通过校验
+ 小程序与嵌入页之间通过 `web-view` 的通信机制传参，频道名、Token 等可以走 URL query 下发
+ 页面运行在微信内嵌浏览器中，iOS 14.3 及以上、Android 均可正常推流与收流；仅 iOS 14.3 以下的旧系统受限于系统 WebView，只能收流

---

### URL 协议限制

WebRTC API 对页面协议有限制，请根据部署场景选择合适的协议：

| 场景 | 协议 | 收流 | 推流 | 备注 |
| --- | --- | :---: | :---: | --- |
| 生产环境 | HTTPS | ✅ | ✅ | **推荐** |
| 生产环境 | HTTP | ✅ | ❌ | 只能收流 |
| 本地开发 | http://localhost | ✅ | ✅ | **推荐** |
| 本地开发 | http://127.0.0.1 | ✅ | ✅ | |
| 本地开发 | http://[本机 IP] | ✅ | ❌ | 只能收流 |
| 本地开发 | file:/// | ✅ | ✅ | |

---

### 安装

#### npm

```bash
npm install @seastart/srtc-web-sdk --save
```

#### CDN 直接引用

适合不使用构建工具的项目，直接在 HTML 中通过 `<script>` 标签引入：

```html
<!-- 通过 unpkg CDN 引入最新版本 -->
<script src="https://unpkg.com/@seastart/srtc-web-sdk@latest/srtc.js"></script>
```

CDN 引入后，全局变量 `SRTC` 即可直接使用。

#### 本地下载引用

1. 下载 [srtc.js](https://unpkg.com/@seastart/srtc-web-sdk@latest/srtc.js) 和 [srtc.d.ts](https://unpkg.com/@seastart/srtc-web-sdk@latest/srtc.d.ts)
2. 将两个文件复制到你的项目目录中

---

### 引入方式

#### ES Module（推荐，配合 npm）

```typescript
import SRTC, {
  LocalMicTrack,
  LocalCameraTrack,
  LocalScreenTrack,
  RemoteAudioMixTrack,
  RemoteVideoTrack,
  ChannelEventType,
  MicPresets,
  CameraPresets,
  ScreenPresets,
  LogLevel,
  LogTarget,
} from '@seastart/srtc-web-sdk';
import type { ChannelEvent } from '@seastart/srtc-web-sdk';
```

#### Script 标签（配合 CDN 或本地文件）

```html
<script src="srtc.js"></script>
<script>
  // 全局变量 SRTC 即为主类
  const srtc = new SRTC({ logLevel: 'debug' });
</script>
```
