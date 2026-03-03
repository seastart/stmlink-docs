---
title: "集成"
description: "Web SMeeting 会议 SDK 环境配置与 SDK 安装指南"
---

## **支持的平台**
SRTC Web SDK 支持主流的桌面端及移动端浏览器，包括 Chrome、Edge、Firefox、Safari、微信内嵌浏览器等，详细支持度表格请参见 [支持的平台](about:blank)。

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
```typescript

### **本地引用**
手动下载 sdk 包：

1. 下载 [smeeting.js](https://www.unpkg.com/@seastart/smeeting-web-sdk@latest/smeeting.js) [smeeting.d.ts](https://www.unpkg.com/@seastart/srtc-web-sdk@latest/smeeting.d.ts) 
2. 将 `smeeting.js` `smeeting.d.ts` 复制到您的项目中。



## 使用
通过 import 引入或者 script 引入

```typescript
import SRTC from '@seastart/smeeting-web-sdk';
// or
<script src="smeeting.js"></script>
```

  
  


  
 

