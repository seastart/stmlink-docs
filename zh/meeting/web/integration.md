---
title: "集成"
description: "Web SMeeting 会议 SDK 环境配置与 SDK 安装指南"
---

## 支持的平台

SMeeting Web SDK 支持主流桌面端及移动端浏览器：

| 浏览器 | 最低版本 | 说明 |
| --- | :---: | --- |
| Chrome | 72+ | 推荐，全功能支持 |
| Edge | 79+ | 基于 Chromium |
| Firefox | 66+ | 不支持指定扬声器输出 |
| Safari | 14+ | 不支持屏幕共享系统音频 |
| 微信内嵌浏览器 | iOS 14.3+ / Android | 支持收发。iOS 低于 14.3 的旧系统仅支持收流 |
| 移动端 Chrome / Safari | 最新版 | 支持基本音视频通话 |

> **提示：** 建议用户使用最新版 Chrome 以获得最佳体验。

## 微信小程序场景

需要在微信小程序里接入会议时，**推荐用小程序的 `<web-view>` 嵌入一个基于本 Web SDK 实现的页面**，而不是再单独做一套小程序原生实现。这样一套 Web 代码同时覆盖浏览器端和小程序端，功能和后续迭代自然保持一致，维护成本最低。

接入要点：

+ 被嵌入的页面必须是 **HTTPS**，且其域名需要在小程序管理后台配置为**业务域名**并通过校验
+ 小程序与嵌入页之间通过 `web-view` 的通信机制传参，房间号、Token 等可以走 URL query 下发
+ 页面运行在微信内嵌浏览器中，iOS 14.3 及以上、Android 均可正常推流与收流；仅 iOS 14.3 以下的旧系统受限于系统 WebView，只能收流

## URL 域名协议限制
| 应用场景    | 协议    | 收音视频流    | 推音视频流    | 备注    |
| --- | --- | --- | --- | --- |
| 生产环境    | HTTPS 协议    | 支持    | 支持    | **推荐**    |
| 生产环境    | HTTP 协议    | 支持    | 不支持    |     |
| 本地开发环境    | http://localhost    | 支持    | 支持    | **推荐**    |
| 本地开发环境    | http://127.0.0.1    | 支持    | 支持    |     |
| 本地开发环境    | http://[本机IP]    | 支持    | 不支持    |     |
| 本地开发环境    | file:///    | 支持    | 支持    |     |


## 引用
### npm
```bash
npm install @seastart/smeeting-web-sdk@latest --save
```

### 本地引用
手动下载 sdk 包：

1. 下载 [smeeting.js](https://www.unpkg.com/@seastart/smeeting-web-sdk@latest/smeeting.js) 和 [smeeting.d.ts](https://www.unpkg.com/@seastart/smeeting-web-sdk@latest/smeeting.d.ts)
2. 将 `smeeting.js` `smeeting.d.ts` 复制到您的项目中。



## 使用
通过 import 引入或者 script 引入

```typescript
import SMeeting from '@seastart/smeeting-web-sdk';
// or
<script src="smeeting.js"></script>
```

  
  


  
 

