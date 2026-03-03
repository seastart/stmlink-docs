---
title: "集成"
description: "微信小程序 SRTC 音视频 SDK 环境配置与 SDK 安装指南"
---

## 前提条件
开通小程序类目与推拉流标签权限（如不开通则无法正常使用）

### ![](images/337417_1721957652278-742a14bf-2e82-4806-83bf-f2b06bf2e07c.png)
根据项目配置合法域名

![](images/342477_1721957771229-74bffc59-3ea1-4310-b600-f4b12881794a.png)



## 引用
### npm
```bash
npm install @seastart/srtc-wx-sdk@latest --save
```typescript



### 本地引用
手动下载 sdk 包：

1. 下载 [srtc-wx.js](https://www.unpkg.com/@seastart/srtc-wx-sdk@latest/srtc-wx.js)  [srtc-wx.d.ts](https://www.unpkg.com/@seastart/srtc-wx-sdk@latest/srtc-wx.d.ts) 
2. 将 `srtc-wx.js``srtc-wx.d.ts`复制到您的项目中。



## 使用
可通过本地引用，也可通过 [小程序构建npm](https://developers.weixin.qq.com/miniprogram/dev/devtools/npm.html) 直接引入。



```typescript
import SRTC from './lib/srtc-wx'; // 静态文件引入

import SRTC from '@seastart/srtc-wx-sdk'; // 小程序构建npm引入
```



