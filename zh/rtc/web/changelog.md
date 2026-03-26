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

+ Web 视频轨道新增画中画与独立窗口能力：`enterPictureInPicture`、`exitPictureInPicture`、`popOutToWindow`、`closePopOutWindow`
+ 新增频道事件：`TRACK_PIP_ENTER`、`TRACK_PIP_EXIT`、`TRACK_POPOUT_OPEN`、`TRACK_POPOUT_CLOSE`
+ `PipOptions`、`PopOutOptions` 新增 `hideOriginView` 选项，默认 `true`
