---
title: "常见问题"
description: "Web SRTC 音视频 SDK 集成与使用常见问题解答"
---

### 浏览器提示"不允许访问摄像头/麦克风"怎么办？

**原因：** 浏览器权限被拒绝或页面不在安全上下文（HTTPS / localhost）下。

**解决步骤：**

1. 确认页面使用 HTTPS 或 localhost 访问（普通 HTTP 域名无法访问媒体设备）
2. 点击浏览器地址栏右侧的摄像头/麦克风图标，将权限改为"允许"
3. 如果之前选择了"永久拒绝"，需要在浏览器的站点设置中手动重置权限：
   - Chrome：地址栏左侧"🔒"→"网站设置"→"摄像头/麦克风"→"允许"
4. 重新刷新页面后再次尝试

可通过 `srtc.getEnvInfo()` 的 `secure` 和 `mediaDevices` 字段提前检测环境是否具备采集能力：

```typescript
const env = srtc.getEnvInfo();
if (!env.secure) {
  alert('请使用 HTTPS 或 localhost 访问本页面');
} else if (!env.mediaDevices) {
  alert('浏览器不支持媒体设备访问，请检查权限设置');
}
```typescript

---

### 本地开发时能收流，但推不了流怎么办？

**原因：** 大概率是页面在普通 HTTP 下运行，浏览器限制了 WebRTC 推流。

**解决方案：** 使用 `http://localhost` 或 `http://127.0.0.1` 访问本地开发环境，不要使用 `http://[本机局域网 IP]`（该协议不支持推流）。

协议与推流支持情况详见 [集成 - URL 协议限制](/zh/rtc/web/integration#url-协议限制)。

---

### 视频/音频自动播放被浏览器阻止怎么处理？

浏览器的自动播放策略禁止在没有用户手势的情况下播放媒体，表现为调用 `startPlay()` 后无声音或无画面。

SDK 会通过 `TRACK_AUTOPLAY_FAIL` 事件通知你：

```typescript
srtc.onNotifyChannelEvent = (evt) => {
  if (evt.type === ChannelEventType.TRACK_AUTOPLAY_FAIL) {
    // 方案一：SDK 内置引导弹窗（默认开启）
    // 用户点击弹窗后会自动触发播放

    // 方案二：自己处理，在用户点击按钮时重新播放
    const failedTrack = evt.data; // BaseTrack
    document.querySelector('#play-btn')!.addEventListener('click', async () => {
      if (failedTrack instanceof RemoteAudioMixTrack) {
        await failedTrack.startPlay({ disableAutoPlayDialog: true });
      }
    }, { once: true });
  }
};
```

> **最佳实践：** 在用户主动点击"加入"或"开始通话"按钮后再调用 `join` 和 `startPlay`，这样的用户手势上下文通常能绕过自动播放限制。

---

### 屏幕共享在 Safari 上不可用？

Safari 15.4 及以上版本支持 `getDisplayMedia`（屏幕共享），但有以下限制：

+ 不支持采集**系统音频**（`getAudioTrack()` 会返回 `undefined`）
+ 在 iOS Safari 上**不支持屏幕共享**（系统限制）
+ 部分老版本 Safari（< 15.4）完全不支持屏幕共享

可通过 `srtc.getEnvInfo().screenshare` 预先判断当前环境是否支持：

```typescript
const env = srtc.getEnvInfo();
if (!env.screenshare) {
  alert('当前浏览器不支持屏幕共享，请使用 Chrome 或桌面版 Safari 15.4+');
}
```typescript

---

### 加入频道报 TokenExpired 错误怎么办？

Token 由服务端签发，有效期较短（通常几分钟到几小时不等，具体由签发方决定）。

**解决方案：**
+ 在发起 `srtc.join()` 前，从服务端实时获取最新 Token，不要缓存旧 Token
+ 检查客户端和服务端的系统时间是否同步（时钟偏差会导致 Token 提前失效）

---

### 如何同时加入多个频道？

每个 `SRTC` 实例对应一个频道连接。需要同时加入多个频道时，创建多个实例：

```typescript
const srtc1 = new SRTC();
const srtc2 = new SRTC();

await srtc1.join(token1);
await srtc2.join(token2);
```

注意：多实例会占用更多带宽和系统资源，请谨慎使用。
