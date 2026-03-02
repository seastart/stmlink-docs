## **<font style="color:rgb(38, 38, 38);">支持的平台</font>**
SRTC Web SDK 支持主流的桌面端及移动端浏览器，包括 Chrome、Edge、Firefox、Safari、微信内嵌浏览器等，详细支持度表格请参见 [支持的平台](about:blank)。

## <font style="color:rgb(38, 38, 38);">URL 域名协议限制</font>
| 应用场景    | 协议    | 收音视频流    | 推音视频流    | 备注<font style="color:rgb(38, 38, 38);">   </font> |
| --- | --- | --- | --- | --- |
| 生产环境    | HTTPS 协议    | 支持    | 支持    | **<font style="color:rgb(223, 42, 63);">推荐</font>**<font style="color:rgb(38, 38, 38);">   </font> |
| 生产环境    | HTTP 协议    | 支持    | 不支持    | <font style="color:rgb(38, 38, 38);">   </font> |
| 本地开发环境    | http://localhost    | 支持    | 支持    | **<font style="color:rgb(223, 42, 63);">推荐</font>**<font style="color:rgb(38, 38, 38);">   </font> |
| 本地开发环境    | http://127.0.0.1    | 支持    | 支持    | <font style="color:rgb(38, 38, 38);">   </font> |
| 本地开发环境    | http://[本机IP]    | 支持    | 不支持    | <font style="color:rgb(38, 38, 38);">   </font> |
| 本地开发环境    | file:///    | 支持    | 支持    | <font style="color:rgb(38, 38, 38);">   </font> |


## <font style="color:rgb(38, 38, 38);">引用</font>
### <font style="color:rgb(38, 38, 38);">npm</font>
```bash
npm install @seastart/smeeting-web-sdk@latest --save
```

### **<font style="color:rgb(38, 38, 38);">本地引用</font>**
手动下载 sdk 包：

1. <font style="color:rgb(38, 38, 38);">下载 </font>[smeeting.js](https://www.unpkg.com/@seastart/smeeting-web-sdk@latest/smeeting.js)<font style="color:rgb(38, 38, 38);"> </font>[smeeting.d.ts](https://www.unpkg.com/@seastart/srtc-web-sdk@latest/smeeting.d.ts)<font style="color:rgb(38, 38, 38);"> </font>
2. <font style="color:rgb(38, 38, 38);">将 </font>`<font style="color:rgb(38, 38, 38);">smeeting.js</font>`<font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgb(38, 38, 38);">smeeting.d.ts</font>`<font style="color:rgb(38, 38, 38);"> 复制到您的项目中。</font>

<font style="color:rgb(38, 38, 38);"></font>

## <font style="color:rgb(38, 38, 38);">使用</font>
通过 import 引入或者 script 引入

```typescript
import SRTC from '@seastart/smeeting-web-sdk';
// or
<script src="smeeting.js"></script>
```

<font style="color:rgb(38, 38, 38);">  
</font><font style="color:rgb(38, 38, 38);">  
</font>

  
 

