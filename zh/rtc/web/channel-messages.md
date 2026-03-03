---
title: "频道消息"
description: "Web SRTC 音视频 SDK 频道外消息通道使用说明"
---

SRTC提供便捷易用的频道外消息通道，方便开发者集成使用，如会前呼叫、通知等。

### 启用
```typescript
// im会话id
let imSid = "";
let enableIm = async () => {
    // 调后台api获取启用im token
    // api.getImToken
  
    let token = "后台返回的启用im token";
    imSid = await srtc.enableIm(token);
}
```typescript



### 接收im消息
```typescript
srtc.onNotifyImEvent = (evt: ImEvent) => {
    console.log('收到im事件', evt);
    switch (evt.type) {
        case ImEventType.IM_MSG:
            // 收到im消息
            // evt.data as ImMsgData
            break;
        
    }
}
```



### 发送im消息
发送im消息都需要通过后台api，这样可以根据自己的业务做如敏感词拦截等处理

```typescript
// 调后台api发送im消息
// api.sendImMsg
```typescript



### 开始重连/重连成功
当网络发生波动时，会触发重连开始事件，成功后会触发重连成功事件

```typescript
// 在onNotifyImEvent里
case ImEventType.RECONNECTING:
  // 开始重连
  break;
case ImEventType.RECONNECTED:
  // 重连成功
  break;
```

### 停用/断开
断开分主动停用和被动(发生不可恢复错误时)断开

```typescript
// 主动停用
await srtc.disableIm();
// 界面刷新清理



// 被动断开
// 在onNotifyImEvent里
case ImEventType.DISCONNECTED:
  let data = (evt.data as ImDisconnectEventData);
  // 可根据reason提示退出原因
  alert('im已断开 reason:' + data.reason);
  // 界面刷新清理
  imSid = "";
  break;
```typescript

