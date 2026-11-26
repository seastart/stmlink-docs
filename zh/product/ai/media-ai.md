---
title: "音视频 AI 处理"
sidebarTitle: "降噪与虚拟背景"
description: "终端本地运行的音视频 AI 处理：AI 降噪（RNNoise、DeepFilterNet）、虚拟背景（背景虚化 / 替换）、美颜，各自在哪些端、哪个 SDK 提供，一张能力 × 端的支持表，附各端接入文档链接。回答客户「某端能不能降噪 / 换背景」时查这页"
---

降噪、虚拟背景、美颜都在**终端本地**运行：处理发生在采集之后、发送之前，不经过服务器，
也不需要配置服务端的 AI 服务。对方看到、听到的就是处理后的效果，录制里也是。

---

## 能做什么

| 能力 | 效果 | 说明 |
| --- | --- | --- |
| **AI 降噪 · RNNoise** | 去掉键盘声、风扇声、环境嘈杂 | 轻量，比浏览器自带降噪对非稳态噪声抑制更强 |
| **AI 降噪 · DeepFilterNet** | 同上，降噪质量更高 | 可在运行时调节降噪强度；计算量与资源体积比 RNNoise 大，设备算力不足时 SDK 会提示 |
| **虚拟背景** | 人像分割后背景虚化，或替换成指定图片 | 自研组件，不需要授权密钥；提供低端机保帧率的参数 |
| **美颜** | 磨皮、美白、红润、锐化、滤镜 | 视频渲染组件，需要组件密钥 |

---

## 各端支持情况

表中 ✅ 可点进对应的接入文档；没有列出的端或空白格表示目前文档中没有该能力。

### SRTC 音视频 SDK

| 能力 | Web | Android | iOS（Objective-C） | Swift | Windows | 微信小程序 |
| --- | --- | --- | --- | --- | --- | --- |
| AI 降噪 · RNNoise | [✅](/zh/rtc/web/advanced/rnnoise) | | | | | |
| AI 降噪 · DeepFilterNet | [✅](/zh/rtc/web/advanced/deepfilternet) | [✅](/zh/rtc/android/advanced/deepfilternet) | | [✅](/zh/rtc/swift/advanced/deepfilternet) | | |
| AI 降噪（SDK 内置模式） | | | | | [✅](/zh/rtc/windows/api-reference/IRTCChannelSetting) 降噪模式可选 AI / AI + 声学 | |
| 虚拟背景 | | [✅](/zh/rtc/android/api-reference/RTCEngine#虚拟背景) | [✅](/zh/rtc/ios/advanced/virtual-background) | [✅](/zh/rtc/swift/advanced/virtual-background) 仅 iOS | | |
| 美颜 | | | [✅](/zh/rtc/ios/advanced/beauty) | | | [✅](/zh/rtc/wechat-miniprogram/api-reference/streaming) 微信推流组件自带 |

### SMeeting 会议 SDK

| 能力 | Web | Android | iOS（Objective-C） | Swift | Windows |
| --- | --- | --- | --- | --- | --- |
| AI 降噪 · DeepFilterNet | [✅](/zh/meeting/web/advanced/deepfilternet) | [✅](/zh/meeting/android/advanced/deepfilternet) | | [✅](/zh/meeting/swift/advanced/deepfilternet) | |
| AI 降噪（SDK 内置模式） | | | | | [✅](/zh/meeting/windows/api-reference/smeeting-settings) 降噪模式 |
| 虚拟背景 | | [✅](/zh/meeting/android/api-reference/MeetingEngine#虚拟背景) | [✅](/zh/meeting/ios/advanced/virtual-background) | [✅](/zh/meeting/swift/advanced/virtual-background) 仅 iOS | |

<Note>
Web 端的降噪以独立 npm 插件提供（`@seastart/srtc-plugin-rnnoise`、`@seastart/srtc-plugin-deepfilternet`），模型和 wasm 文件需要随网站一起托管，见各自页面。
挂处理器的通用机制见 [音频处理器](/zh/rtc/web/advanced/audio-processor)。
</Note>

---

## 选型建议

+ **只要降噪**：Web 先用 RNNoise（资源小）；对降噪效果要求高、终端性能够的，用 DeepFilterNet
+ **降噪不要叠两层**：插件自己做降噪时，SDK 会关掉浏览器自带的降噪，避免人声发闷
+ **虚拟背景**：低端手机上开启后注意帧率，可调大人像分割的推理间隔换帧率，参数见各端页面
