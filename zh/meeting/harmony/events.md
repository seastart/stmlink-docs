---
title: "事件参考"
description: "SMeeting HarmonyOS SDK 的全部 52 个事件回调与各自的数据结构字段"
---

会议 SDK 的事件全部走一个接口 `SMeetingDelegate`，注册在引擎上：

```typescript
import { SMeetingDelegate } from 'smeeting';

const delegate: SMeetingDelegate = {
  onUserEnter: (meeting, user) => { /* ... */ },
  onUserMicStateChange: (meeting, data) => { /* ... */ }
};

meeting.delegates.add(delegate);
```

<Note>
**所有回调的第一个参数都是引擎实例 `meeting`**，第二个参数是该事件的数据对象。
下面的表格省略第一个参数。

两个例外：`onUserEnter` 的第二个参数直接是 `MeetingUserInfo`，
`onDeviceAdd` / `onDeviceRemove` 的第二个参数直接是 `DeviceInfo`。
</Note>

<Warning>
**`delegates` 是强引用，必须成对 `add` / `remove`，退出时还要调 `dispose()`。**

ArkTS 既没有弱引用、也没有 `deinit`。漏掉会导致监听者永不回收、且离开页面后仍收到回调。

```typescript
aboutToDisappear(): void {
  this.meeting.delegates.remove(this.delegate);
  this.meeting.dispose();          // 摘掉挂在全局单例上的监听
}
```
</Warning>

---

## 连接状态

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onMeetingReconnecting` | — | 会议连接中断，正在自动重连 |
| `onMeetingReconnected` | — | 重连成功 |
| `onDisconnected` | `reason: DisconnectReason`, `error?: Error` | 断开且不再自动恢复 |

`onReconnecting` / `onReconnected` 之间 SDK 会自行恢复，业务侧只需更新连接指示。
收到 `onDisconnected` 才走"退出会议"流程。

---

## 成员

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onUserEnter` | `MeetingUserInfo`（直接是对象） | 成员进入会议 |
| `onUserExit` | `uid`, `reason: DisconnectReason` | 成员离开 |
| `onUserNameChange` | `uid`, `nickname`, `byAdmin`, `opUid?` | 成员改名 |
| `onUserRoleChange` | `uid`, `role: Role`, `opUid?` | 角色变化（主持人 / 联席 / 普通） |
| `onUserChatDisabledChange` | `uid`, `chatDisabled`, `opUid?` | 某成员被禁言 / 解禁 |

<Note>
带 `byAdmin` 与 `opUid?` 的事件表示"是谁操作的"：`byAdmin` 为 `true` 时
`opUid` 是操作者。UI 上提示"你已被主持人静音"就靠这两个字段。
</Note>

## 成员媒体状态

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onUserMicStateChange` | `uid`, `micState: MicState`, `byAdmin`, `opUid?` | 成员麦克风开关 |
| `onUserCameraStateChange` | `uid`, `cameraState: CameraState`, `byAdmin`, `opUid?` | 成员摄像头开关 |

拿到 `onUserCameraStateChange` 且 `cameraState === CameraState.on` 时才去
`subscribeRemoteVideoTrack(uid)`，关掉时退订 —— 这是控制带宽的主要手段。

## 举手

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onUserHandup` | `uid`, `type: HandupType`, `step: UserHandupStep` | 成员举手状态变化 |
| `onAdminConfirmHandup` | `type: HandupType`, `approve`, `targetId`, `opUid?` | 主持人处理了举手 |

`HandupType` 区分举手的用途：`mic` / `camera` / `chat` / `share`；
`UserHandupStep` 是流转步骤：`request` / `cancel` / `confirmOpen` / `rejectOpen`。

详见[举手](/zh/meeting/harmony/advanced/handup)。

---

## 房间级会控

这一组都是主持人改了全局开关。字段形如 `xxxDisabled: boolean` + `opUid?`。

| 事件 | 数据字段 | 说明 |
| --- | --- | --- |
| `onRoomMicStateChange` | `micDisabled`, `selfUnmuteMicDisabled`, `opUid?` | 全体静音 |
| `onRoomCameraStateChange` | `cameraDisabled`, `selfUnmuteCameraDisabled`, `opUid?` | 全体关摄像头 |
| `onRoomShareStateChange` | `shareDisabled`, `opUid?` | 禁止共享 |
| `onRoomChatDisabledChange` | `chatDisabled`, `opUid?` | 禁止聊天 |
| `onRoomScreenshotDisabledChange` | `screenshotDisabled`, `opUid?` | 禁止截图 |
| `onRoomWatermarkDisabledChange` | `watermarkDisabled`, `opUid?` | 水印开关 |
| `onRoomLockedChange` | `locked`, `opUid?` | 会议锁定 |

<Note>
**`micDisabled` 与 `selfUnmuteMicDisabled` 是两件事：**

+ `micDisabled` —— 现在是不是全体静音状态
+ `selfUnmuteMicDisabled` —— 成员**能不能自己解除**静音

两者组合出三种常见形态：自由发言、全体静音但可自行解除、全体静音且不可自行解除。
UI 上"开麦"按钮的可用性要同时看这两个字段。摄像头同理。
</Note>

## 共享

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onRoomShareStart` | `uid`, `shareType: ShareType` | 有人开始共享 |
| `onRoomShareStop` | `uid`, `shareType`, `byAdmin`, `opUid?` | 共享结束 |

`ShareType` 有 `screen` 与 `whiteBoard` 两种。

---

## 消息

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onChatMessage` | `msgType: ChatMsgType`, `msg`, `uid?`, `isPrivate` | 收到聊天消息 |
| `onCustomMessage` | `msg`, `uid?`, `isPrivate` | 收到自定义消息 |

`ChatMsgType`：`text` / `file` / `pic` / `sound`。`isPrivate` 为 `true` 表示私聊。

`msg` 统一是**字符串** —— 结构化内容（文件、图片元信息）需要自己 `JSON.parse`。

---

## 录制与点名

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onRoomMcuTask` | `taskType: McuTaskType`, `taskStatus: McuTaskStatus`, `errDesc` | MCU 录制 / 混流任务状态变化 |
| `onRollCallNamed` | `id`, `sid`, `time` | 自己被点名 |

`McuTaskStatus` 为 `exception` 时 `errDesc` 有原因，UI 上要提示（录制出问题用户需要知道）。

---

## 签到

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onSignInActivity` | `hostId`, `hostName`, `epoch`, `beginAt`, `dur`, `endAt`, `desc` | 主持人发起了签到 |
| `onSignInFinish` | `hostId`, `hostName`, `epoch` | 签到结束 |

`epoch` 是这一轮签到的标识，后续查询统计要带上它。

---

## 等候室

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onUserEnterWaitingRoom` | `uid`, `name`, `avatar` | 有人进入等候室（**主持人侧**） |
| `onUserExitWaitingRoom` | `uid`, `name`, `avatar` | 有人离开等候室 |
| `onWaitingRoomDisabledChange` | `waitingRoomDisabled`, `opUid?` | 等候室开关变化 |
| `onMoveToWaitingRoom` | — | **自己**被移入等候室 |

<Note>
`onMoveToWaitingRoom` 没有数据参数，收到就意味着你已经被移出会议主房间 ——
UI 要切到等候页，并停止渲染会议内容。
</Note>

---

## 子会议

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onAdminStartSubMeeting` | `meetingId`, `title`, `uids` | 子会议开启 |
| `onAdminStopSubMeeting` | `parent` | 子会议结束，`parent` 是主会议 ID |
| `onAdminMoveSubMeetingUser` | `fromMeetingId`, `fromMeetingTitle`, `toMeetingId`, `toMeetingTitle` | 自己被跨子会议移动 |

`onAdminMoveSubMeetingUser` 带了两侧的标题，可以直接拿来做
"你已被移动到「XX 组」"这种提示。

---

## 主持人对我的请求

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onAdminRequestOpenMic` | `opUid?` | 主持人请求你开麦 |
| `onAdminRequestOpenCamera` | `opUid?` | 主持人请求你开摄像头 |

<Note>
这是**请求**而不是命令 —— 应当弹窗征求用户同意，同意后调
`requestOpenMic()` / `requestOpenCamera()`。SDK 不会自动开。
</Note>

---

## 音频路由与设备

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onAudioRouteChange` | `route: AudioRoute`, `previousRoute: AudioRoute` | 输出路由变化 |
| `onCallStateChange` | `state: AudioCallState`, `previousState: AudioCallState` | 系统通话状态变化 |
| `onDeviceAdd` | `DeviceInfo`（直接是对象） | 设备接入 |
| `onDeviceRemove` | `DeviceInfo`（直接是对象） | 设备移除 |

外接设备由系统接管，SDK 只上报不主动切换。详见
[音频路由](/zh/meeting/harmony/advanced/audio-routing)。

---

## 质量

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onConnectionQualityChange` | `ConnectionQualityChange` | 连接质量**等级**变化 |
| `onQualityReport` | `QualityReport` | 周期性原始采样 |
| `onActiveSpeakersChange` | `ActiveSpeakersSnapshot` | 活跃说话人变化 |
| `onLayerSwitched` | `LayerSwitchedInfo` | Simulcast 层切换 |

这几个的参数类型来自 SRTC，字段说明见
[SRTC 类型定义](/zh/rtc/harmony/types)与[通话质量](/zh/rtc/harmony/advanced/call-quality)。

做 UI 指示器用 `onConnectionQualityChange`（已做等级判定与抖动抑制），
`onQualityReport` 是原始采样、适合上报监控。

---

## IM

| 事件 | 数据字段 | 触发时机 |
| --- | --- | --- |
| `onImReconnecting` | — | IM 重连中 |
| `onImReconnected` | — | IM 重连成功 |
| `onImDisconnected` | `reason?: string` | IM 断开 |
| `onImCallCalling` | `base: ImBaseEventData`, `content: ImCallContent` | 收到呼叫 |
| `onImMeetingRemind` | `base`, `content: ImMeetingRemindContent` | 会议提醒 |
| `onImAdminMoveOutWaitingRoom` | `base`, `content: ImSubMeetingContent` | 被移出等候室 |
| `onImUserHelpSubMeeting` | `base`, `content: ImSubMeetingContent` | 子会议求助 |

IM 类事件统一是「`base` + `content`」两段结构：

| `ImBaseEventData` 字段 | 说明 |
| --- | --- |
| `sid` | 会话 ID |
| `uid` | 发送者 |
| `name` | 发送者昵称 |
| `avatar?` | 头像 |

`content` 的类型按事件不同。详见 [IM](/zh/meeting/harmony/advanced/im)。

---

### 相关阅读

+ [核心概念](/zh/meeting/harmony/key-concepts)
+ [类型定义](/zh/meeting/harmony/types)
+ [会控](/zh/meeting/harmony/advanced/host-controls)
+ [SMeetingEngine 接口](/zh/meeting/harmony/api-reference/SMeetingEngine)
