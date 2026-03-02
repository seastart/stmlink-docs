## 支持的平台
SRTC Web SDK 支持主流的桌面端及移动端浏览器，包括 Chrome、Edge、Firefox、Safari、微信内嵌浏览器等，详细支持度表格请参见 [支持的平台](https://web.sdk.qcloud.com/trtc/webrtc/v5/doc/zh-cn/tutorial-05-info-browser.html)。

## URL 域名协议限制
| **<font style="color:#000000;">应用场景</font>** | **<font style="color:#000000;">协议</font>** | **<font style="color:#000000;">收音视频流</font>** | **<font style="color:#000000;">推音视频流</font>** | **<font style="color:#000000;">备注</font>** |
| --- | --- | --- | --- | --- |
| 生产环境 | HTTPS 协议 | 支持 | 支持 | **<font style="color:#DF2A3F;">推荐</font>** |
| 生产环境 | HTTP 协议 | 支持 | 不支持 | <font style="color:rgb(201, 197, 190);"> </font> |
| 本地开发环境 | http://localhost | 支持 | 支持 | **<font style="color:#DF2A3F;">推荐</font>** |
| 本地开发环境 | http://127.0.0.1 | 支持 | 支持 | <font style="color:rgb(201, 197, 190);"> </font> |
| 本地开发环境 | http://[本机IP] | 支持 | 不支持 | <font style="color:rgb(201, 197, 190);"> </font> |
| 本地开发环境 | file:/// | 支持 | 支持 | <font style="color:rgb(201, 197, 190);"> </font> |


## 引用
### npm
```bash
npm install @seastart/srtc-web-sdk@latest --save
```



### 本地引用
手动下载 sdk 包：

1. 下载 [srtc.js](https://www.unpkg.com/@seastart/srtc-web-sdk@latest/srtc.js) [srtc.d.ts](https://www.unpkg.com/@seastart/srtc-web-sdk@latest/srtc.d.ts) 
2. 将 `srtc.js` `srtc.d.ts` 复制到您的项目中。



## 使用
通过 import 引入或者 script 引入

```typescript
import SRTC from '@seastart/srtc-web-sdk';
// or
<script src="srtc.js"></script>
```





