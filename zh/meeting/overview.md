---
title: "概览"
description: "SMeeting 会议 SDK 的能力范围、两种对接方式与各端支持情况"
---

SMeeting 是一套完整的音视频会议 SDK。它建在 [SRTC 音视频能力](/zh/rtc/overview)之上，把会议才需要的那些规则 —— 主持人、举手、静音全场、等候室、录制 —— 都做成了现成能力，你不用再实现一遍。

还在 SRTC 和 SMeeting 之间犹豫，先看 [怎么选](/zh/choose)。

---

## 能做什么

| | |
| --- | --- |
| **会议管理** | 创建、修改、取消会议；预约会议与即时会议；会议列表与详情 |
| **音视频** | 摄像头、麦克风、屏幕共享、多人画面订阅 |
| **会控** | 主持人 / 联席主持人、静音全场、踢人、改角色、锁定会议 |
| **成员互动** | 举手申请发言、主持人邀请开麦、会中聊天、自定义消息 |
| **会议室能力** | 等候室、子会议、签到、点名 |
| **录制与直播** | 服务端 MCU 合流、录制、布局配置、旁路直播 |
| **会议外消息** | 呼叫、会议提醒、求助等独立于会议的消息通道 |

---

## 两种对接方式

### 带 UI 极简对接

直接引入我们提供的会议界面源码，你只需要在服务端把账号打通，会议内的所有交互都由我们的 UI 完成。

适合：想最快上线、能接受我们的界面风格、不需要深度定制交互。

从 [带 UI 极简对接](/zh/meeting/ui-sdk/server-integration) 开始。

### 自定义对接

你自己实现界面，调用各端 SDK 的接口完成会议功能；服务端调用会议后端 API，并提供回调接口接收事件。

适合：界面要符合自己的设计规范、交互流程有定制需求。

从下面选择你的平台。

---

## 平台支持

| 平台 | 文档 |
| --- | --- |
| Web | [Web SDK](/zh/meeting/web/integration) |
| Android | [Android SDK](/zh/meeting/android/integration) |
| Windows | [Windows SDK](/zh/meeting/windows/integration) |
| iOS / macOS（Swift） | [Swift SDK](/zh/meeting/swift/integration) |
| iOS（Objective-C） | [iOS SDK](/zh/meeting/ios/quickstart) |
| 服务端 | [服务端 API](/zh/meeting/server-api/overview) |

<Note>
微信小程序场景建议用 `<web-view>` 嵌入基于 Web SDK 实现的页面，一套代码同时覆盖浏览器和小程序。详见 [Web SDK 集成](/zh/meeting/web/integration)。
</Note>

---

## 接下来

+ [快速开始](/zh/meeting/quickstart) —— 对接流程总览
+ [核心概念](/zh/meeting/key-concepts) —— 房间、会议、成员与角色
+ [Token 与鉴权](/zh/meeting/token) —— 授权流程与密钥安全
