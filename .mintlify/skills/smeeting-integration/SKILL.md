---
name: SMeeting 会议接入
description: 用 SMeeting 会议 SDK 做视频会议时使用——三种对接方式的选择、房间与会议模型、主持人会控、举手与等候室、会中聊天与消息通道。覆盖服务端极简对接、带 UI 极简对接和各端 SDK 自定义对接。只要音视频通道、不要会议规则时读「SRTC 音视频接入」。
metadata:
  version: "1.0"
  docs: https://docs.stmlink.com
---

# SMeeting 会议接入

SMeeting 建在 SRTC 之上，把会议才需要的规则——主持人、举手、静音全场、等候室、录制——都做成了现成能力。

## 第一步：选对接方式，这决定了工作量

**先问清楚客户要不要自己做会议界面。** 选错方式会导致大量返工。

| 方式 | 要做的事 | 界面 | 适合 |
| --- | --- | --- | --- |
| **服务端极简对接** | 后端对 3 个接口，拼一个 URL | 我们部署好的 | 把会议挂到既有业务流程上（评审、工单、招投标） |
| **带 UI 极简对接** | 拿前端源码自己改、自己部署 | 我们的源码，可改 | 要自己的品牌和少量定制 |
| **自定义对接** | 集成各端 SDK，自己写界面 | 完全自己做 | 做会议产品，交互深度定制 |

**默认先推荐服务端极简对接。** 需求是"给这场评审加一个视频会议入口"时，它不需要集成任何 SDK、不写一行前端：

```text
业务活动创建时
  └─ POST /meeting/server/v1/meet/create        挂上你的业务单据号 → 拿到 room_no

用户点「进入会议」
  ├─ POST /meeting/stm/srvapi/v1/member/grant   account + 昵称 → token（人不存在就现场建）
  └─ 302 跳转 /meeting/stm/ui/outer?token=<token>&room_no=<room_no>&nickname=<昵称>
```

**别漏掉 `/meeting` 网关前缀**——标准部署下同域名的根路径走的是 SRTC 音视频服务，
漏了就会找不到会议接口。只有第 3 步的 URL 会到达浏览器，`app_key` 始终留在后端。

## 核心模型

### 房间与会议是两个东西

| 概念 | 说明 |
| --- | --- |
| **房间 room** | 相对固定的会议空间，有房间号 `room_no`，用于对外分发 |
| **会议 meeting** | 一次具体的会议，有会议 ID，创建后才能进入 |

日常接入主要用**会议 ID**：创建会议拿到它，之后进入、会控、录制都用它。

### 生命周期有严格顺序

```text
登录 → 会前（创建/查询/修改会议）→ 进入会议 → 会中 → 退出会议 → 登出
```

- **登录之后**才能调会议管理接口
- **进入会议之后**才能调会中接口（媒体控制、会控、消息）
- 退出会议不影响登录状态，可以接着进下一场

各端 SDK 在调用时机不对时会返回明确错误（未登录 / 不在会议中），不用自己维护状态机去猜。

### 角色决定能做什么

| 角色 | 能力 |
| --- | --- |
| **主持人** | 完整会控：静音全场、踢人、改角色、锁定会议、开关等候室、结束会议 |
| **联席主持人** | 由主持人指定，具备大部分会控能力 |
| **普通成员** | 自己的音视频开关、举手申请、聊天 |
| **观众** | 只收流，不出现在成员列表里 |

**会控大多是「请求 - 批准」形态**：成员举手申请开麦、主持人批准；主持人邀请开麦、成员同意或拒绝。开摄像头麦克风涉及隐私，**主持人不能单方面强开**——不要设计成一键强制打开对方摄像头。

### 一个用户可以多端同时在线

同一用户在手机和电脑同时进会，会被识别成两个参会身份（按设备类型区分），互不顶替。这层映射 SMeeting 自动完成，**不需要自己拼 uid**（这点和 SRTC 不同）。

## 术语：不要和 SRTC 混用

| 概念 | SMeeting | SRTC |
| --- | --- | --- |
| 空间 | 房间 room / 会议 meeting | 频道 channel |
| 出入 | 进入 enter / 退出 exit | 加入 join / 离开 leave |
| 参与者 | 参会成员 | 频道用户 uid |
| 媒体 | 由会议层管理 | 流轨道 track |

SMeeting 的接口不接受频道名，SRTC 的接口也不认识会议号。少数错误码里带「频道」字样是底层 RTC 原样透传，不是笔误。

## 三条消息通道，别选错

| | 会中聊天 | 会中自定义消息 | 会议外消息（IM） |
| --- | --- | --- | --- |
| 前提 | 已进入会议 | 已进入会议 | 已登录并启用 IM，**不需要在会议里** |
| 内容 | 给人看的文字 | 给程序看的业务信令 | 呼叫、会议提醒、等候室移入、子会议求助 |
| 历史记录 | 有，可翻页拉取 | 无 | 无 |
| 会控 | 可被主持人禁言 | 不受禁言影响 | 不适用 |

**「IM」不是聊天工具**，是独立于会议的通知通道，作用是在用户还没进会议时把消息推给他。它没有好友关系、会话列表、聊天记录、群组、已读回执、离线消息队列。**要在会议里做文字交流用「会中聊天」，不是 IM。**

一句话：会中聊天给人看，自定义消息给程序看，IM 在会议之外找人。

## 各端入口（自定义对接）

| 端 | 安装 | 主入口 |
| --- | --- | --- |
| Web | `npm i @seastart/smeeting-web-sdk` | `new SMeeting({...})` |
| Android | `implementation 'cn.seastart.meeting:meeting:<version>'` | `MeetingEngine.create()` |
| Windows | 下载 [meeting-win-sdk-2.0.zip](https://repo.open.seastart.cn/repository/vcs-releases/meeting-win-sdk-2.0.zip)，**x86 32 位** | C++ 接口 |
| Swift（iOS/macOS） | Swift Package `smeeting-swift-sdk` | `import SMeeting` → `SMeetingEngine()` |
| Objective-C（iOS） | CocoaPods | `MeetingKit`（单例） |

**苹果平台有两套 SDK**：Swift 原生（`import SMeeting`，支持 iOS 与 macOS）和 Objective-C（`MeetingKit`，仅 iOS）。**新项目用 Swift 那套**，两套不能混用。

**微信小程序**建议用 `<web-view>` 嵌入基于 Web SDK 的页面。

### Web 最小流程

注意与 SRTC 的差别：**先 `login` 再 `enterRoom`**，媒体操作用「请求」语义的方法。

```typescript
const smeeting = new SMeeting({ /* ... */ });

// 1. 注册事件回调——在 login/enterRoom 之前
smeeting.onNotifyRoomEvent = (evt) => { /* 会议与成员状态变化 */ };

// 2. 登录（token 由你的后端签发）
await smeeting.login(token);

// 3. 创建会议或直接进入
const roomNo = await smeeting.createRoom({ /* ... */ });
await smeeting.enterRoom({ /* ... */ });

// 4. 媒体：注意是 requestOpenCamera 而非直接打开——走的是会控许可流程
await smeeting.requestOpenCamera(container, deviceId, preset);
await smeeting.requestOpenMic(deviceId, preset);

// 5. 播放远端画面
await smeeting.startPlayRemoteVideo(container, uid, trackDesc);

// 6. 退出
await smeeting.exitRoom();
```

## 常见坑

- **选错对接方式**：客户只想"加个会议入口"却上了自定义对接，白做几周界面。先问清楚。
- **术语混用**：把「房间」「会议」安到 SRTC 接口上，或给 SMeeting 传频道名。
- **调用时机**：没 `login` 就创建会议、没 `enterRoom` 就调会中接口。
- **强开摄像头**：设计成主持人一键打开对方摄像头——做不到，也不该做，走邀请-同意流程。
- **自己拼 uid 做多端**：SMeeting 已内置按设备类型区分，不要再拼。
- **拿 IM 当聊天用**：没有历史记录和离线队列，会中文字交流要用会中聊天。
- **`app_key` 泄露**：极简对接里只有最后那个跳转 URL 该到浏览器，签名一律在后端做。

## 交付前自检

- [ ] 对接方式与客户的界面需求匹配，没有过度集成
- [ ] `app_key` 只在后端，没进前端配置或 App 包体
- [ ] 事件回调在 `login` / `enterRoom` 之前注册
- [ ] 调用顺序符合「登录 → 会前 → 进入 → 会中 → 退出」
- [ ] 开麦开摄像头走请求-批准流程，没有强开
- [ ] 用的是会议层术语与接口，没混用 SRTC 的频道概念
- [ ] 文字交流用会中聊天，通知类才用 IM
- [ ] 错误码按 `code` 判断，不匹配 `msg` 文案

## 深入查阅

先取 https://docs.stmlink.com/llms.txt 看全站目录，再按需读页面（URL 末尾加 `.md` 拿 Markdown）。

- 概览与三种方式 `/zh/meeting/overview` · 核心概念 `/zh/meeting/key-concepts` · Token `/zh/meeting/token`
- 服务端极简对接 `/zh/meeting/ui-sdk/server-integration`
- 各端：`/zh/meeting/{web,android,windows,swift,ios}/quickstart`
