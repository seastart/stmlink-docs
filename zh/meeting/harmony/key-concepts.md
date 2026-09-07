---
title: "核心概念"
description: "理解 SMeeting HarmonyOS SDK 的对象模型、与 SRTC 的分层关系、角色与会控体系"
---

### 与 SRTC 的关系

SMeeting 建在 SRTC 之上，**不是**替代它：

```
SMeetingEngine        会议业务：账号、会议 CRUD、会控、等候室、子会议、录制、签到
   └── srtc: SRTCEngine   媒体：频道连接、采集、发布、订阅、渲染
```

`meeting.srtc` 是可以直接访问的。这意味着：

+ 会议 SDK 覆盖不到的底层能力，可以从 `meeting.srtc` 拿
+ 渲染组件、轨道类型、编解码工具**都来自 `srtc`** ——
  所以 `import { SRTCVideoView, Track } from 'srtc'` 是常态，不是绕路
+ 媒体相关的错误会是 `SRTCError`（`108xxx`），会议业务的错误是 `SMeetingError`（`208xxx`）

<Note>
必须**同时引入两个 HAR**。HAR 没有依赖传递性，SMeeting 把 `srtc` 声明为
`peerDependencies`，需要由你的工程提供。只声明 `smeeting` 会在
`ohpm install` 阶段直接失败。
</Note>

---

### 对象模型

+ `SMeetingEngine`：唯一入口。账号、会议、媒体、会控全在它上面
+ `SMeetingDelegate`：**所有** 52 个事件的统一回调接口
+ `SMeetingRemoteVideoView`：远端画面组件（替你管订阅生命周期）
+ `MeetingUserInfo` / `RoomInfo` / `MeetingInfo`：成员、房间、会议的数据模型

与 SRTC 不同，**会议 SDK 没有 `Channel` 这一层** —— 一个引擎实例同时只在一个会议里，
频道的概念被收进了引擎内部。

```typescript
const meeting: SMeetingEngine = new SMeetingEngine(LogLevel.info);
```

---

### 三段生命周期

```
登录        login(token)              ← token 由业务后端签发
   ↓
会议管理    createRoom / attendeeRoom / detailRoom …   （不在会中也能调）
   ↓
入会        enterRoom({ nickname, meetingId | roomNo })
   ↓
会中        requestOpenMic / subscribeRemoteVideoTrack / admin* / …
   ↓
离会        exitRoom()
   ↓
登出        logout() → dispose()
```

区分这三段很重要，因为**接口对状态有要求**：

| 状态 | 能做什么 | 违反时的错误 |
| --- | --- | --- |
| 未登录 | 只能 `login` | `notLoggedIn`（`208001`） |
| 已登录、不在会中 | 会议 CRUD、列表查询 | — |
| 在会中 | 媒体、会控、聊天、签到… | `notInMeeting`（`208003`） |

<Warning>
`dispose()` 必须调用 —— 它会摘掉挂在全局单例上的监听。ArkTS 没有析构函数，
漏掉会导致页面永不回收、摄像头指示灯一直亮。
</Warning>

---

### 一体化的媒体接口

这是 SMeeting 与直接用 SRTC 的最大差别。SRTC 里开麦是四步：

```typescript
// 直接用 SRTC
const mic = srtc.createLocalMicTrack(preset);
await mic.startCapture();
await channel.publishLocalAudioTrack(mic);
```

SMeeting 把它收成一步，**内部还多做了一次后端授权**：

```typescript
// 用 SMeeting
await meeting.requestOpenMic();
```

`requestOpenMic` / `requestOpenCamera` / `requestShare` 内部完成
「向会议后端申请授权 → 创建本地轨道 → 启动采集 → 发布到频道」。

<Note>
名字里的 `request` 是实义的：**会议后端可以拒绝**。主持人开了全体静音时，
`requestOpenMic()` 会失败。所以 UI 上应该按 `onRoomMicStateChange` 提前禁用按钮，
而不是等调用失败再提示。
</Note>

本地轨道通过属性取用：`meeting.micTrack` / `cameraTrack` / `screenTrack` / `mcuTrack`。

---

### 角色与权限

`Role` 有三档：

| 值 | 说明 |
| --- | --- |
| `member = 0` | 普通成员 |
| `host = 1` | 主持人 |
| `coHost = 2` | 联席主持人 |

所有 `admin*` 方法都要求主持人或联席主持人身份，否则抛 `unauthorized`（`208004`）。

<Note>
**按角色隐藏 / 禁用按钮，而不是靠捕获 `unauthorized`。** 后者的体验是
"点了才知道不能点"。角色变化通过 `onUserRoleChange` 事件下发。
</Note>

---

### 房间开关是「两个字段一组」

会控里的静音、关摄像头这类开关，事件与状态都是**成对**的：

| 字段 | 含义 |
| --- | --- |
| `micDisabled` | 现在是不是全体静音 |
| `selfUnmuteMicDisabled` | 成员**能不能自己解除** |

组合出三种常见形态：

| `micDisabled` | `selfUnmuteMicDisabled` | 实际效果 |
| --- | --- | --- |
| `false` | — | 自由发言 |
| `true` | `false` | 全体静音，但成员可自行开麦 |
| `true` | `true` | 全体静音且不可自行开麦（只能举手） |

摄像头同理。判断"开麦按钮能不能点"必须同时看这两个字段。

---

### 订阅与渲染

远端画面有两种写法：

#### 用 `SMeetingRemoteVideoView`（推荐）

它替你管订阅生命周期 —— 组件出现时订阅、消失时（防抖）退订。

```typescript
ForEach(this.users, (u: MeetingUserInfo) => {
  SMeetingRemoteVideoView({ meeting: this.meeting, uid: u.uid })
    .width('50%').height(160)
}, (u: MeetingUserInfo) => u.uid)
```

#### 自己订阅 + `SRTCVideoView`

需要把**同一路画面同时渲染在多处**（大窗 + 缩略图）时必须走这条，
原因见[视频渲染](/zh/meeting/harmony/advanced/video-rendering)。

```typescript
await meeting.subscribeRemoteVideoTrack(uid);
const track: Track | undefined = meeting.getRemoteVideoTrack(uid);
```

<Warning>
`SMeetingRemoteVideoView` 的 `meeting` 与 `SRTCVideoView` 的 `track` 一样，
**必须是普通成员变量、不能声明成 `@Prop`** —— `@Prop` 深拷贝会丢类型，
拷过来就是个没有方法的普通对象。换用户靠组件重建（`ForEach` 的 key 带上 uid）。
</Warning>

---

### `TrackDesc`：会议里的轨道是按用途命名的

| 值 | 说明 |
| --- | --- |
| `mic` | 麦克风 |
| `cameraBig` | 摄像头大流 |
| `cameraSmall` | 摄像头小流（Simulcast 副层） |
| `screen` | 屏幕共享 |

订阅时传 `trackDesc` 就能选大流还是小流 —— 宫格视图用 `cameraSmall`、
大窗用 `cameraBig`，是控制带宽最直接的手段。

---

### MCU 合流

大型会议可以订阅**服务端合成的一路画面**，而不是 N 路各自订阅：

```typescript
const mcu = await meeting.subscribeRemoteVideoMcu(uid);
await meeting.unsubscribeRemoteVideoMcu();
```

布局由 `adminUpdateLayout(layoutData)` 控制，`LayoutType` 提供了 20 种预置布局
（`auto` / `full` / `grids_2` … `grids_25` / `right_4` / `tb_8` 等）。

MCU 同时也是录制的基础，见[录制](/zh/meeting/harmony/advanced/recording)。

---

### 事件模型

**52 个事件全在一个 `SMeetingDelegate` 接口上**，只实现关心的那几个。
所有回调第一个参数都是引擎实例，第二个是该事件的数据对象。

```typescript
meeting.delegates.add(delegate);
```

<Warning>
`delegates` 是**强引用**，必须成对 `add` / `remove`。ArkTS 没有弱引用也没有 `deinit`。
</Warning>

完整清单见 [事件参考](/zh/meeting/harmony/events)。

---

### 建议继续阅读

+ [会控](/zh/meeting/harmony/advanced/host-controls)
+ [媒体控制](/zh/meeting/harmony/advanced/media-control)
+ [视频渲染](/zh/meeting/harmony/advanced/video-rendering)
+ [等候室](/zh/meeting/harmony/advanced/waiting-room)
+ [子会议](/zh/meeting/harmony/advanced/sub-meetings)
