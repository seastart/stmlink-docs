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
| 微信内嵌浏览器 | - | iOS 仅支持收流，Android 支持收发 |
| 移动端 Chrome / Safari | 最新版 | 支持基本音视频通话 |

> **提示：** 建议用户使用最新版 Chrome 以获得最佳体验。

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
```typescript

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
  ChannelEvent,
  ChannelEventType,
  MicPresets,
  CameraPresets,
  ScreenPresets,
  LogLevel,
  LogTarget,
} from '@seastart/srtc-web-sdk';
```typescript

#### Script 标签（配合 CDN 或本地文件）

```html
<script src="srtc.js"></script>
<script>
  // 全局变量 SRTC 即为主类
  const srtc = new SRTC({ logLevel: 'debug' });
</script>
```
