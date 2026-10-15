---
title: "产品全景"
description: "一页看懂我们能提供什么：SRTC 音视频 SDK、SMeeting 会议 SDK、会议室连接器（硬件设备接入）、云录制与语音录制、语音识别、管理后台、终端产品、私有化与光闸部署。不写代码的同学从这里开始"
---

我们提供一整套**可私有化部署**的实时音视频平台：从底层的音视频能力，到开箱即用的会议，
再到会议室硬件接入和跨网部署。这一页按「能解决什么问题」把它们串起来，每一项都可以点进去看细节。

想了解产品亮点和行业方案，也可以访问[官网](https://www.stmlink.com)。

---

## 平台能力

<Columns cols={2}>
  <Card title="SRTC 音视频 SDK" icon="video" href="/zh/rtc/overview">
    低延迟音视频通话、直播、对讲。覆盖 Web、小程序、Android、iOS、Windows、Mac、鸿蒙，以及服务端 C / Python SDK
  </Card>
  <Card title="SMeeting 会议 SDK" icon="users" href="/zh/meeting/overview">
    主持人、会控、举手、等候室、预约、签到等会议能力现成可用，还提供带界面的极简对接
  </Card>
  <Card title="会议室连接器" icon="tv" href="/zh/product/device-access/overview">
    华为、科达等 SIP / H.323 视频终端，国标监控摄像头，RTSP 视频流，不换设备直接进会
  </Card>
  <Card title="云录制" icon="circle-dot" href="/zh/rtc/server-api/guides/recording">
    服务端多画面合成录制、转推直播，录像统一存储、在线回放下载
  </Card>
  <Card title="语音录制" icon="microphone" href="/zh/rtc/server-api/talkrec">
    按人分段录音，适合对讲、调度、执法等需要留痕的场景
  </Card>
  <Card title="语音识别与会议纪要" icon="closed-captioning" href="/zh/rtc/server-api/asr">
    会中实时字幕、发言转写，会后生成纪要
  </Card>
  <Card title="AI 语音 / 视频智能体" icon="robot" href="/zh/rtc/python/quickstart">
    用 Python SDK 把语音识别、大模型、语音合成接进通话，做 AI 客服、AI 助手
  </Card>
  <Card title="互动白板" icon="pen" href="/zh/rtc/whiteboard">
    多人实时协作白板与文档批注
  </Card>
</Columns>

---

## 管理与运维

<Columns cols={2}>
  <Card title="管理后台" icon="gauge" href="/zh/product/admin-console">
    应用、频道与会议、录制、设备、用量统计、通话质量、节点运维，一个后台全管
  </Card>
  <Card title="在线体验" icon="play" href="/zh/product/demos">
    RTC 演示、会议演示，先体验再决定
  </Card>
</Columns>

---

## 终端产品

除了 SDK，我们也有可以直接装在设备上用的终端应用：

<Columns cols={2}>
  <Card title="软 SIP / H.323 终端" icon="phone" href="/zh/product/terminals/softsip">
    装在安卓设备上的 App，让大屏、一体机变成标准 SIP / H.323 视频终端
  </Card>
  <Card title="安卓 TV 大屏版" icon="display" href="/zh/product/terminals/tv">
    面向会议室电视和大屏，遥控器操作，一键入会、投屏
  </Card>
</Columns>

---

## 部署

<Columns cols={2}>
  <Card title="组件与架构" icon="sitemap" href="/zh/product/deploy/architecture">
    全离线安装，支持 x86 / ARM、信创系统、人大金仓 / 达梦数据库
  </Card>
  <Card title="网络与端口要求" icon="network-wired" href="/zh/product/deploy/ports">
    客户端只需 3 个端口，附防火墙命令，开墙申请直接用
  </Card>
  <Card title="内外网与多线路" icon="route" href="/zh/product/deploy/networks">
    一套平台同时服务内网和外网用户
  </Card>
  <Card title="光闸跨网接入" icon="shield-halved" href="/zh/product/deploy/optical-gap">
    内外网光闸隔离，外网用户照样入会，只需 3 条穿透通道
  </Card>
</Columns>

---

## 我该看哪里

| 我是 | 建议从这里开始 |
| --- | --- |
| 售前、项目经理 | 本页 → [会议室连接器](/zh/product/device-access/overview) → [组件与架构](/zh/product/deploy/architecture) |
| 实施、运维 | [网络与端口要求](/zh/product/deploy/ports) → [设备接入](/zh/product/device-access/overview) |
| 开发者 | [SRTC 还是 SMeeting？](/zh/choose) → 对应平台的快速开始 |
