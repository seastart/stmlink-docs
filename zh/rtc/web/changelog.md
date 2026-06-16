---
title: "更新日志"
description: "Web SRTC 音视频 SDK 版本更新记录"
---

### 最新版本

请通过 npm 查看最新版本：

```bash
npm info @seastart/srtc-web-sdk version
```typescript

---

### 历史版本记录

> 版本更新日志持续完善中，如需了解具体版本变更，请联系技术支持。

### 近期更新

### v0.5.6 - 2026-06-16

+ feat: 视频支持前置摄像头镜像，前置默认开启且可由用户调整
+ feat: DeepFilterNet 降噪插件

### v0.5.4 - 2026-06-03

+ feat: 新增音视频处理器插件机制
+ feat: 新增wasm降噪插件

### v0.5.3 - 2026-05-08

+ feat: add local composite recorder (47a20b0)
+ chore: 共享屏幕默认配置优化 (f079eeb)

### v0.5.1 - 2026-04-27

+ fix: 视频卡顿 (b7a36c2)
+ feat: RemoteVideoTrack支持设置jitterBufferTarget(抗抖动目标延迟) (6aed177)

### v0.5.0 - 2026-04-23

+ feat: seastart引擎接入服务端下发质量报告
+ feat: 频道事件系统类型安全改造，支持判别联合及自动类型收窄
+ feat: seastart引擎Active speaker（说话中的用户）接入
+ feat: 新增自适应流功能，支持根据播放窗口状态自动切换 simulcast 层，支持 SFU 下行切层通知及主动切层请求

### v0.4.4 - 2026-04-18

+ feat: simulcast 联播支持及 SFU 订阅层切换优化 (781f520)

+ Web 视频轨道新增画中画与独立窗口能力：`enterPictureInPicture`、`exitPictureInPicture`、`popOutToWindow`、`closePopOutWindow`
+ 新增频道事件：`TRACK_PIP_ENTER`、`TRACK_PIP_EXIT`、`TRACK_POPOUT_OPEN`、`TRACK_POPOUT_CLOSE`
+ `PipOptions`、`PopOutOptions` 新增 `hideOriginView` 选项，默认 `true`
