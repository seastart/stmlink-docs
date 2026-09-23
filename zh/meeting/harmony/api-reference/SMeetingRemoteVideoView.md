---
title: "SMeetingRemoteVideoView"
description: "远端画面组件的参数、订阅生命周期管理，以及同一路画面渲染在多处时的限制"
---

远端视频组件。它的职责只有一件：**替你管订阅生命周期** ——
组件出现时订阅、消失时（防抖）退订。

渲染本身复用 SRTC 的 `SRTCVideoView`，所以远端轨道晚到时的重绑逻辑不用写第二遍。

```typescript
import { SMeetingRemoteVideoView } from 'smeeting';

// 多路远端画面：key 带上 uid，一路一个组件实例
ForEach(this.users, (u: MeetingUserInfo) => {
  SMeetingRemoteVideoView({ meeting: this.meeting, uid: u.uid })
    .width('50%')
    .height(160)
}, (u: MeetingUserInfo) => u.uid)
```

---

### 参数

| 参数 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `meeting` | `SMeetingEngine \| undefined` | `undefined` | 引擎实例，**必传** |
| `uid` | `string` | `''` | 要渲染哪个成员 |
| `trackDesc` | `TrackDesc` | `cameraBig` | 订哪一路：大流 / 小流 / 屏幕 |
| `scalingMode` | `ScalingMode` | `AspectFit` | 填充方式 |
| `unsubscribeDebounceMs` | `number` | `300` | 退订防抖窗口（毫秒） |

<Note>
**宫格视图传 `TrackDesc.cameraSmall`、大窗传 `cameraBig`。**
20 个人的宫格全订大流会把下行打满。
</Note>

---

### `meeting` 必须是普通成员变量

<Warning>
**`meeting` 不能声明成 `@Prop`。**

与 `SRTCVideoView` 的 `track` 同理：`@Prop` 对复杂类型做**深拷贝**且会丢类型，
`SMeetingEngine` 拷过来就成了一个没有方法的普通对象 —— 结果是黑屏、事件也收不到。

所以按引用传入，**换用户靠组件重建**（`ForEach` 的 key 或 `if` 分支带上 uid）。

注意组件内部 `uid` 是 `@Prop`（字符串是基本类型，深拷贝没问题），
但**换 uid 仍然建议靠重建**而不是改 `@Prop` —— 订阅关系是在
`aboutToAppear` 里建立的。
</Warning>

---

### 退订是防抖的

组件在 `aboutToDisappear` 里走
`unsubscribeRemoteVideoTrack(uid, trackDesc, unsubscribeDebounceMs)`。

为什么要防抖：列表滚动、分页切换时同一路画面会在几十毫秒内消失又出现，
立即退订再重订就是一轮轮完整的 SDP 协商。防抖窗口内重新订阅会把待执行的退订取消掉，
所以快速滑动是**无感**的。

需要更激进或更保守时调 `unsubscribeDebounceMs`：

+ 长列表快速滚动 → 调大（如 `800`）
+ 需要尽快省带宽 → 调小

---

### 已知限制：同一路画面不能挂两个本组件实例

<Warning>
**同一 `uid` + `trackDesc` 同时挂两个 `SMeetingRemoteVideoView` 实例
（比如大窗 + 缩略图），关掉其中一个会在防抖窗口后把整路流退掉，另一个变黑屏。**

这个场景请**自己订阅一次**，把同一个 `RemoteVideoTrack` 交给两个 `SRTCVideoView`：

```typescript
// 自己订阅
await this.meeting.subscribeRemoteVideoTrack(uid, TrackDesc.cameraBig);
this.speakerTrack = this.meeting.getRemoteVideoTrack(uid, TrackDesc.cameraBig);

// 同一个 track 交给两个 SRTCVideoView
SRTCVideoView({ track: this.speakerTrack, trackKey: `${uid}-big` })
  .width('100%').height(240)
SRTCVideoView({ track: this.speakerTrack, trackKey: `${uid}-thumb` })
  .width(120).height(80)
```

退订时机自己控制（比如切换主讲人时）。
</Warning>

#### 为什么组件不用「有渲染器就不退订」的守卫版

SDK 里确实有守卫版接口
`unsubscribeRemoteVideoTrackIfNoRenderers()`（靠 `RemoteVideoTrack.hasRenderers`
引用计数判断）。但本组件**没有**用它，原因是 ArkUI 的卸载顺序：

**父组件的 `aboutToDisappear` 先于子组件执行。** 在本组件的
`aboutToDisappear` 里调守卫版时，子 `SRTCVideoView` 还没 `removeRenderer`，
会永远判成"还有渲染器"而**永不退订** —— 那就成了带宽泄漏，比黑屏更糟。

所以现阶段选择了防抖退订这个更保守的方案。

---

### 与 `SRTCVideoView` 的分工

| 用哪个 | 场景 |
| --- | --- |
| `SMeetingRemoteVideoView` | 常规多路远端画面。省心，订阅生命周期自动管 |
| `SRTCVideoView` + 手动订阅 | 同一路渲染在多处；或需要精确控制订阅时机 |
| `SRTCVideoView` + `meeting.cameraTrack` | **本地预览**（本组件只管远端） |

本地预览的写法：

```typescript
if (this.meeting.cameraTrack !== undefined) {
  SRTCVideoView({
    track: this.meeting.cameraTrack,
    trackKey: this.meeting.cameraTrack.id
  }).width('100%').height(240)
}
```

---

### 相关阅读

+ [视频渲染](/zh/meeting/harmony/advanced/video-rendering)
+ [媒体控制接口](/zh/meeting/harmony/api-reference/media-control)
+ [SRTC 轨道接口](/zh/rtc/harmony/api-reference/media-tracks)
