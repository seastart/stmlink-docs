---
title: "AI 降噪（DeepFilterNet）"
description: "在 Web 会议里给麦克风开启 AI 降噪：安装 @seastart/srtc-plugin-deepfilternet，用 setAudioProcessor 交给会议层，开麦自动挂载、关麦自动卸载"
---

### 概述

会议层通过 `setAudioProcessor` 设置麦克风音频处理器，自 `0.3.4` 起提供。最常见的用法是挂 SRTC 的 AI 降噪插件 `@seastart/srtc-plugin-deepfilternet`：它基于 DeepFilterNet，与 Android、iOS 端使用同一份算法和模型，支持运行时调整降噪强度与旁路。

插件的安装、静态资源托管、选项与运行时方法见 SRTC 文档 [DeepFilterNet 降噪插件](/zh/rtc/web/advanced/deepfilternet)，本页只讲会议层怎么接。仅 Web 端提供，小程序不支持。

---

### 安装

```bash
npm install @seastart/smeeting-web-sdk@latest @seastart/srtc-plugin-deepfilternet --save
```

插件运行时要加载模型和 WebAssembly 文件，需先按 [托管静态资源](/zh/rtc/web/advanced/deepfilternet#托管静态资源) 把它们放到你的站点上。

---

### 使用

```typescript
import { SMeeting } from "@seastart/smeeting-web-sdk";
import { DeepFilterNetProcessor } from "@seastart/srtc-plugin-deepfilternet";

const processor = new DeepFilterNetProcessor({
  assetBasePath: "/deepfilternet/",  // 上一步托管资源的目录
  suppressionLevel: 50,              // 0–100
});

// 入会前后都可以调用；麦克风已开时立即生效
await meeting.setAudioProcessor(processor);

// 之后每次开麦都会自动挂上降噪，不需要再处理
await meeting.requestOpenMic();
```

运行时调整强度或旁路，直接调插件，不需要重新设置：

```typescript
processor.setSuppressionLevel(80); // 0–100
processor.setEnabled(false);       // 旁路（输出原始音频）
processor.setEnabled(true);        // 恢复降噪
```

关闭降噪：

```typescript
await meeting.setAudioProcessor(undefined);
```

---

### 会议层的行为

+ **SDK 记住设置**：会议里的麦克风轨每次开麦都会新建，所以由 SDK 保存处理器，每次开麦在采集之后、发布之前自动挂上，关麦和离会时卸下。离会后设置仍保留，下次入会开麦继续生效。
+ **同一个实例可以反复使用**：关麦时处理器会被销毁、下次开麦重新初始化，不需要业务每次新建。
+ **开麦时挂载失败不影响开麦**（例如静态资源加载失败），麦克风照常打开、发出未降噪的声音，SDK 只在控制台记录警告；麦克风已开着时调用 `setAudioProcessor`，失败会直接抛错。
+ 降噪插件会自动关闭浏览器自带的降噪，避免两道降噪叠加；这依赖 SRTC Web `0.7.3` 及以上，`0.3.4` 已经依赖该版本。
+ 传数组时按顺序串联多个处理器，例如先降噪再变声，规则见 SRTC 文档 [音频处理器](/zh/rtc/web/advanced/audio-processor)。
