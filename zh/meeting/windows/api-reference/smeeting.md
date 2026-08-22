---
title: "C++ API 参考"
description: "Windows SMeeting 会议 SDK C++ 接口完整参考"
---

本文档提供 Windows SMeeting SDK C++ 接口的完整参考。所有接口定义在 `SMeeting.h` 头文件中。

从 `1.0.0-alpha.5` 开始，`ISMeetingEngine` 按**引擎级 / 会议级**拆分为两套接口：

| 接口 | 作用域 | 说明 |
| --- | --- | --- |
| [ISMeetingEngine](smeeting-engine) | 引擎级 | 登录、会议管理 HTTP 接口、频道生命周期、设备枚举、IM、资源盘。 |
| [ISMeetingChannel](smeeting-channel) | 会议级 | 一个会议一个对象，包含入会、会中操作、媒体对象。 |
| [ISMeetingEngineEvent](smeeting-events) | 引擎级回调 | 设备、网络探测、IM 事件。 |
| [ISMeetingChannelEvent](smeeting-events) | 会议级回调 | 连接状态、成员、房间、流媒体等会议内事件。 |
| [ISMeetingSetting](smeeting-settings) | 引擎级配置 | 仅 `sdk_log_path` / `enable_stream_log`。 |
| [ISMeetingChannelSetting](smeeting-settings) | 会议级配置 | 流模式、统计间隔、入会昵称头像等。 |

**重要**：`ISMeetingEngine` / `ISMeetingChannel` 及 `IMEET*` 系列都是纯虚接口，签名变动会改变 vtable；升级 SDK 后必须重新编译业务工程，不能只替换 dll。

---

## 接口模块索引

- [ISMeetingEngine 引擎接口](smeeting-engine) — 初始化、登录登出、会议管理、频道管理、设备枚举、IM、资源盘。
- [ISMeetingChannel 会议接口](smeeting-channel) — 入会/退会、房间信息、用户操作、等候室。
- [主持人管理接口](smeeting-admin) — 房间控制、用户控制、权限管理。
- [分组会议接口](smeeting-submeeting) — 创建/启动/停止/移动分组会议。
- [MCU 接口](smeeting-mcu) — 合成视频、录制配置。
- [签到接口](smeeting-signin) — 签到活动创建、统计、导出。
- [媒体轨道接口](smeeting-media) — 本地/远端音视频、屏幕共享、自定义轨道、本地录制。
- [事件回调](smeeting-events) — `ISMeetingEngineEvent` 与 `ISMeetingChannelEvent`。
- [配置项](smeeting-settings) — `ISMeetingSetting` 与 `ISMeetingChannelSetting`。
- [枚举类型与数据结构](smeeting-types) — `StatusCode`、`Role`、`SMeetingCreateMeetingModel` 等。
