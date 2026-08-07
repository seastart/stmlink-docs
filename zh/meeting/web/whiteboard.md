---
title: "白板共享"
description: "会议里怎么开白板：用 getWhiteBoard() 取页面地址内嵌 iframe，用 requestShare(ShareType.WhiteBoard) 广播共享状态，以及中途入会时如何恢复现场"
---

会议里的电子白板是一个**内嵌的 H5 页面**（`iframe`），笔迹同步走白板自己的通道，不产生媒体流。会议层在此之上多做了一件事：**替你管理"现在谁在共享白板"这个状态**，不用像 SRTC 层那样自己广播。

<Note>
白板页面本身的能力（URL 参数、隐藏菜单、桌面批注模式、销毁时机）与 SRTC 层完全一致，见 [SRTC · 电子白板](/zh/rtc/whiteboard)。本页只讲会议层的用法差异。
</Note>

---

### 取白板地址

进入会议后即可读取，SDK 已经把授权码拼好，直接内嵌：

```typescript
await smeeting.enterRoom(/* ... */);

const url = smeeting.getWhiteBoard();
if (url) {
  const iframe = document.createElement("iframe");
  iframe.src = url;
  iframe.style.cssText = "width:100%;height:100%;border:0";
  boardContainer.appendChild(iframe);
}
```

白板与会议一一对应——同一个会议里的人打开的是同一块板。退出会议后该地址失效。

---

### 开始与停止共享

白板共享**只广播状态，不采集任何画面**：

```typescript
import { ShareType } from "@seastart/smeeting-web-sdk";

// 开始：会议内广播「我在共享白板」
await smeeting.requestShare(ShareType.WhiteBoard);

// 结束
await smeeting.stopShare();
```

同一时刻一个会议只允许一位成员共享，屏幕共享与白板互斥。主持人开启了"房间禁共享"时，普通成员调用会抛错。

---

### 响应他人的白板共享

其他人开白板时，你会收到房间事件，据此显示白板：

```typescript
smeeting.onNotifyRoomEvent = (evt: RoomEvent) => {
  switch (evt.type) {
    case CommonRoomEventType.ROOM_SHARE_START:
      if (evt.data.share_type === ShareType.WhiteBoard) {
        showWhiteBoard(smeeting.getWhiteBoard());
      }
      break;
    case CommonRoomEventType.ROOM_SHARE_STOP:
      hideWhiteBoard();
      break;
  }
};
```

**中途入会的人收不到这个事件**，要自己补一次判断——会议信息里带着当前共享状态：

```typescript
const info = smeeting.getRoomInfo();
if (info?.share_state === ShareType.WhiteBoard) {
  // 会议中已经有人在共享白板，进来就要显示
  showWhiteBoard(smeeting.getWhiteBoard());
}
```

`share_state` 的取值：`0` 无共享、`1` 屏幕共享、`2` 白板；共享者是 `share_uid`。

---

### 相关

+ [SRTC · 电子白板](/zh/rtc/whiteboard) —— 白板页面的 URL 参数、原生端内嵌、生命周期与销毁
+ [事件参考](/zh/meeting/web/events) —— 共享相关事件的完整定义
+ [SMeeting](/zh/meeting/web/api-reference/SMeeting) —— 接口签名
