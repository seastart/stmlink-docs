---
title: "集成"
description: "微信小程序 SMeeting 会议 SDK 环境配置与 SDK 安装指南"
---

## 前提条件
开通小程序类目与推拉流标签权限（如不开通则无法正常使用）

![](images/160069_1721957652278-742a14bf-2e82-4806-83bf-f2b06bf2e07c.png)

根据项目配置合法域名

![](images/224110_1721957771229-74bffc59-3ea1-4310-b600-f4b12881794a.png)



## 引用
### npm
```bash
npm install @seastart/smeeting-wx-sdk@latest --save
```

### **本地引用**
手动下载 sdk 包：

1. 下载 [smeeting-wx.js](https://www.unpkg.com/@seastart/smeeting-wx-sdk@latest/smeeting-wx.js) [smeeting-wx.d.ts](https://www.unpkg.com/@seastart/smeeting-wx-sdk@latest/smeeting-wx.d.ts) 
2. 将 `smeeting-wx.js` `smeeting-wx.d.ts` 复制到您的项目中。



## 使用
可通过本地引用，也可通过 [小程序构建npm](https://developers.weixin.qq.com/miniprogram/dev/devtools/npm.html) 直接引入。

```typescript
import SMeeting from './lib/smeeting-wx'; // 静态文件引入
// or
import SMeeting from '@seastart/smeeting-wx-sdk'; // 小程序构建npm引入
```

  
  


  
 

