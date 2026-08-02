---
name: SRTC 音视频接入
description: 用 SRTC 音视频 SDK 做实时音视频时使用——加入频道、发布与订阅音视频轨道、屏幕共享、频道内外消息、云录制。覆盖 Web、Android、Windows、Swift（iOS/macOS）、Objective-C（iOS）、C（服务端/嵌入式）各端。做的是会议产品时先读「SMeeting 会议接入」。
metadata:
  version: "1.0"
  docs: https://docs.stmlink.com
---

# SRTC 音视频接入

SRTC 是音视频通道层。它**只做三件事：实时消息传输、状态同步、音视频传输**，不带用户体系、不带业务规则。

## 先判断该不该用 SRTC

| 需求 | 用什么 |
| --- | --- |
| 做会议产品，要主持人、举手、静音全场、等候室 | **SMeeting**，读「SMeeting 会议接入」 |
| 直播连麦、客服双人通话、AI 语音对话、远程巡检 | SRTC |
| 已有自己的业务规则和 UI，只缺音视频传输 | SRTC |
| 服务端旁路录制、转推、AI Agent 接入 | SRTC 的 C SDK |

会控规则（谁能说话、谁是主持人）在 SRTC 里**不存在**，要自己实现。如果发现自己在 SRTC 上手写会控，说明该换 SMeeting。

## 核心模型

只有三个对象，层层包含：

```
频道 Channel
 └── 用户 User（uid）
      └── 流轨道 Track
```

- **频道**：音视频空间，名字自定义。第一个人加入时自动打开；开启后 2 小时无人加入、或最后一人离开 2 小时后自动销毁。
- **uid**：你自己业务系统的用户 ID，SRTC 不管用户体系。一个 uid 可同时加入**多个不同**频道；同一 uid 加入**同一个**频道时，**后加入的会顶掉先加入的**——要多端同时在线就把设备标识拼进 uid。
- **Track**：每一路音频/视频都是一个轨道。轨道的业务含义由 `desc` 字段标记（是摄像头还是屏幕共享），接收端据此决定怎么渲染。

**订阅是显式的**：加入频道不会自动收到所有画面，必须主动订阅，这是为了让你能按需控制带宽。

## Token：必须后端签发

客户端加入频道需要 token，**只能由业务方后端调 `/server/v1/channel/grant` 签发**。

- `app_id` 可以出现在客户端；**`app_key` 绝对不行**——拿到它就能签发任意身份、踢人、销毁频道。
- token 与一次会话绑定，**用过就不能再用**。每个客户端实例各签各的。
- 签名细节读「SRTC 服务端 API」skill。

## 各端入口

| 端 | 安装 | 主入口 |
| --- | --- | --- |
| Web | `npm i @seastart/srtc-web-sdk` | `new SRTC({...})` |
| Android | `implementation 'cn.seastart.rtc:rtc:<version>'` | `RTCEngine.create(...)` |
| Windows | 向我们获取 SDK 包 | `IRTCEngine`（C++） |
| Swift（iOS/macOS） | Swift Package | `import SRTC` → `SRTC()` |
| Objective-C（iOS） | CocoaPods | `RTCEngineKit` |
| C（服务端/嵌入式） | 向我们获取 SDK 包 | `rtc_create()` |

**苹果平台有两套 SDK**：Swift 原生（`import SRTC`，同时支持 iOS 与 macOS）和 Objective-C（`RTCEngineKit`，仅 iOS）。**新项目用 Swift 那套**，两套 API 不能混用，也不要在同一工程里同时引入。

**微信小程序**建议用 `<web-view>` 嵌入基于 Web SDK 的页面，一套代码同时覆盖浏览器和小程序。

## 标准接入顺序（以 Web 为例，其它端同构）

顺序错了是最常见的失败原因，尤其是第 2 步和第 5 步。

```typescript
import SRTC, { MicPresets, CameraPresets, TrackKind, ChannelEventType } from '@seastart/srtc-web-sdk';

// 1. 创建实例
const srtc = new SRTC({ logLevel: 'debug' });

// 2. 注册事件回调——必须在 join 之前，否则会漏掉加入瞬间的事件
srtc.onNotifyChannelEvent = (evt) => {
  switch (evt.type) {
    case ChannelEventType.USER_TRACK_ADD:   // 有人新发布轨道 → 在这里订阅
      break;
    case ChannelEventType.USER_TRACK_REMOVE:
      break;
    case ChannelEventType.TRACK_AUTOPLAY_FAIL: // 浏览器拦了自动播放
      break;                                    // 需在用户手势后重新 startPlay
  }
};

// 3. 加入频道（token 来自你的后端）
const channelInfo = await srtc.join(token);

// 4. 订阅全频道混音，才能听到别人
const audioMix = await srtc.subscribeRemoteAudioMixTrack();
await audioMix.startPlay();

// 5. 订阅"加入前就已在推流"的用户
//    USER_TRACK_ADD 只通知加入之后新发布的轨道，早于你进来的必须主动遍历
for (const user of srtc.getUsersInfo(false)) {
  for (const track of user.stream_tracks ?? []) {
    if (track.kind === TrackKind.Video) { /* 订阅 */ }
  }
}

// 6. 发布本地媒体：先 startCapture 再 publish，顺序不能反
const mic = srtc.createLocalMicTrack(MicPresets.music);
await mic.startCapture();
await srtc.publishLocalTrack(mic);

const cam = srtc.createLocalCameraTrack(CameraPresets['720p']);
await cam.startCapture();
cam.addPlayView(document.querySelector('#local-video')!);
await srtc.publishLocalTrack(cam);

// 7. 退出：先停本地轨道，再 leave
await srtc.unpublishLocalTrack(mic); mic.stopCapture();
await srtc.leave();
```

## 两条消息通道

区别只有一个：**收发时人在不在频道里**。

| | 频道内自定义消息 | 频道外 IM 消息 |
| --- | --- | --- |
| 前提 | 已加入频道 | 已 `enableIm(token)`，不需要在频道里 |
| 发送 | 客户端 SDK 直接发 | **只能后端调服务端接口发** |
| 接收 | 频道事件 `custom_msg` | IM 事件 `im_msg` |
| 用途 | 举手、白板同步、状态广播 | 会前呼叫、邀请、通知提醒 |

**「IM」不是聊天产品**，别按聊天工具去设计。它没有会话列表、聊天记录、消息漫游、群组、已读回执、离线消息队列；消息不持久化，只保证断线重连期间补发。要做完整聊天功能，那是业务系统自己的事。

发送必须走后端是有意的——让你有机会做敏感词过滤、频率限制、权限校验。

## 错误码怎么读

| 位数/前缀 | 来源 | 例 |
| --- | --- | --- |
| 4 位 `1xxx` | 服务端返回 | `1021` Token 已被使用 |
| 6 位 `100xxx` | SDK 各端通用 | `100008` 令牌失效 |
| 6 位 `10Nxxx` | SDK 特定平台，N 为端侧类型 | `106001` Web 端不在频道内 |
| 6 位 `180xxx` | C SDK（服务端/嵌入式接入） | `180001` 不在频道内 |

端侧类型：1 Windows、2 Android、3 iOS、4 Linux C/C++、5 macOS、6 Web、7 小程序、8 Android 盒子、9 Android 嵌入式、80 服务端/嵌入式接入。

**不要按错误文案做分支判断**，文案会随版本变，错误码不会。

## 常见坑

- **回调注册晚于 join** → 漏掉加入瞬间的事件。永远先注册再加入。
- **只处理 `USER_TRACK_ADD`** → 看不到比自己先进频道的人。必须额外遍历 `getUsersInfo()` 补订阅。
- **忘记订阅混音** → 全程听不到声音。
- **`publishLocalTrack` 前没 `startCapture`** → 发布失败。
- **token 复用** → 第二个实例拿到 `1032`（会话不在线）。每个实例单独签发。
- **同 uid 重复进同一频道** → 前一个被顶掉，表现为"莫名其妙掉线"。
- **Web 非 HTTPS** → 只能收流不能推流（localhost 除外）。
- **浏览器拦自动播放** → 收到 `TRACK_AUTOPLAY_FAIL`，要在用户点击等手势之后重新 `startPlay()`。
- **频道名非法** → 限 64 字节以内，仅大小写字母、数字、下划线 `_`、连字符 `-`。带 `+` `*` 等字符会导致连接异常。
- **移动端没申请运行时权限** → `startCapture()` 前必须拿到摄像头/麦克风权限。

## 交付前自检

- [ ] `app_key` 没有出现在任何客户端代码、配置、包体里
- [ ] token 每次从后端新签，没有缓存复用
- [ ] 事件回调在 `join` 之前注册
- [ ] 加入后既订阅了混音，也遍历补订阅了已有用户的视频
- [ ] 本地轨道先 `startCapture` 后 `publish`
- [ ] 退出时停轨道、清渲染容器、再 `leave`
- [ ] 检查了返回的错误码，不是只判断成功/失败
- [ ] 频道名符合字符与长度限制

## 深入查阅

先取 https://docs.stmlink.com/llms.txt 看全站目录，再按需读具体页面（URL 末尾加 `.md` 可直接拿 Markdown）。

- 核心概念 `/zh/rtc/key-concepts` · Token 与鉴权 `/zh/rtc/token` · 错误码规则 `/zh/rtc/error-codes`
- 各端：`/zh/rtc/{web,android,windows,swift,ios,capi}/quickstart`
