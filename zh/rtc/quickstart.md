---
title: "快速开始"
description: "SRTC 音视频 SDK 接入前的准备工作与各平台入口"
---

本页给出接入 SRTC 的最短路径。

---

## 接入前

三件事按顺序做完，再去看具体平台的文档：

<Steps>
<Step title="申请应用">
拿到 **AppID** 和 **AppKey**。AppKey 是服务端密钥，绝不能放进客户端 —— 详见 [Token 与鉴权](/zh/rtc/token)。
</Step>

<Step title="理解模型">
SRTC 只有三个对象：频道、用户、流轨道。它不带用户体系，也不带业务规则。花五分钟读一遍 [核心概念](/zh/rtc/key-concepts)，后面所有接口都会好懂很多。
</Step>

<Step title="打通 Token 签发">
客户端加入频道需要业务后端签发的 Token。调试阶段可以先在开发者后台生成临时 Token 跑通客户端，但正式环境必须走后端签发。
</Step>
</Steps>

---

## 选择你的平台

| 平台 | 入口 |
| --- | --- |
| Web | [集成](/zh/rtc/web/integration) · [快速开始](/zh/rtc/web/quickstart) |
| Android | [集成](/zh/rtc/android/integration) · [快速开始](/zh/rtc/android/quickstart) |
| Windows | [集成](/zh/rtc/windows/integration) · [快速开始](/zh/rtc/windows/quickstart) |
| Swift（iOS / macOS） | [集成](/zh/rtc/swift/integration) · [快速开始](/zh/rtc/swift/quickstart) |
| iOS（Objective-C） | [集成](/zh/rtc/ios/integration) · [快速开始](/zh/rtc/ios/quickstart) |
| C（服务端 / 嵌入式） | [集成](/zh/rtc/capi/integration) · [快速开始](/zh/rtc/capi/quickstart) |
| 服务端 | [服务端 API](/zh/rtc/server-api/overview) |

<Note>
微信小程序场景建议用 `<web-view>` 嵌入基于 Web SDK 实现的页面，一套代码同时覆盖浏览器和小程序。详见 [Web SDK 集成](/zh/rtc/web/integration)。
</Note>

---

## 典型接入顺序

各端 API 名称不同，但流程是一致的：

```text
初始化 SDK
  → 设置事件回调          （必须在加入频道前，否则会漏掉早期事件）
  → 加入频道（用 token）
  → 采集并发布本地轨道
  → 订阅远端轨道并渲染
  → 离开频道 → 释放资源
```

<Tip>
最容易踩的坑是**回调注册晚于加入频道** —— 那样会漏掉"已在频道内的用户"这批事件，表现为进会后看不到别人。各端文档的快速开始都按正确顺序给了示例。
</Tip>

---

## 如果你要做的是会议

主持人、举手、静音全场、等候室这些不在 SRTC 里，需要自己实现。如果你的形态本来就是会议产品，先看一眼 [选 SRTC 还是 SMeeting](/zh/choose) 再决定从哪一层接入。
