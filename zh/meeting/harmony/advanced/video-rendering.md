---
title: "视频渲染"
description: "两种渲染写法的取舍、@Prop 的陷阱、同一路画面渲染在多处的限制、宫格与大窗布局"
---

### 两种写法

| 用哪个 | 场景 |
| --- | --- |
| `SMeetingRemoteVideoView` | 常规多路远端画面。订阅生命周期自动管 |
| `SRTCVideoView` + 手动订阅 | 同一路渲染在多处；或需要精确控制订阅时机 |
| `SRTCVideoView` + `meeting.cameraTrack` | **本地预览**（前者只管远端） |

---

### 常规多路：用 `SMeetingRemoteVideoView`

```typescript
import { SMeetingRemoteVideoView } from 'smeeting';
import { TrackDesc } from 'smeeting';

ForEach(this.users, (u: MeetingUserInfo) => {
  SMeetingRemoteVideoView({
    meeting: this.meeting,
    uid: u.uid,
    trackDesc: TrackDesc.cameraSmall
  })
    .width('50%')
    .height(160)
}, (u: MeetingUserInfo) => u.uid)
```

组件出现时订阅、消失时（防抖 300ms）退订，不用自己管。

---

### `@Prop` 是这里最容易踩的坑

<Warning>
**`meeting`（以及 `SRTCVideoView` 的 `track`）不能声明成 `@Prop`。**

ArkTS 的 `@Prop` 对复杂类型做**深拷贝**，且拷贝过程中除基本类型 / Map / Set /
Date / Array 之外**会丢失类型** —— `SMeetingEngine` / `Track` 拷过来会变成一个
没有方法的普通对象。

后果：**画面黑屏，事件也永远收不到**，而且不会报错。

`@Link` / `@ObjectLink` 能引用传递，但要求父组件为每一路画面单独持有一个
`@State`，多路远端画面根本写不出来。

所以：**走普通成员变量（按引用传入），换对象靠组件重建** ——
让 `if` 分支或 `ForEach` 的 key 带上 uid / trackId。
</Warning>

```typescript
// ✅ 对的
struct MyView {
  private meeting: SMeetingEngine | undefined = undefined;
  private track?: Track;
}

// ❌ 错的
struct MyView {
  @Prop meeting: SMeetingEngine;   // 深拷贝丢类型 → 黑屏
  @Prop track: Track;
}
```

---

### 同一路画面渲染在多处

<Warning>
**同一 `uid` + `trackDesc` 同时挂两个 `SMeetingRemoteVideoView` 实例
（大窗 + 缩略图）会出问题**：关掉其中一个，防抖窗口后整路流被退订，另一个变黑屏。

这个场景要**自己订阅一次**，把同一个 track 交给两个 `SRTCVideoView`：

```typescript
// 订阅一次
await this.meeting.subscribeRemoteVideoTrack(uid, TrackDesc.cameraBig);
this.speakerTrack = this.meeting.getRemoteVideoTrack(uid, TrackDesc.cameraBig);

// 交给两个渲染组件，trackKey 不同
SRTCVideoView({ track: this.speakerTrack, trackKey: `${uid}-big` })
  .width('100%').height(240)
SRTCVideoView({ track: this.speakerTrack, trackKey: `${uid}-thumb` })
  .width(120).height(80)
```

退订时机自己控制（比如切换主讲人时）。
</Warning>

#### 为什么组件不用守卫版退订

SDK 有 `unsubscribeRemoteVideoTrackIfNoRenderers()` ——
靠 `RemoteVideoTrack.hasRenderers` 引用计数判断，理论上正好解决上面的问题。

但它在 ArkUI 的 `aboutToDisappear` 里**不可靠**：

**父组件的 `aboutToDisappear` 先于子组件执行。** 在
`SMeetingRemoteVideoView.aboutToDisappear` 里调守卫版时，
子 `SRTCVideoView` 还没 `removeRenderer`，会永远判成"还有渲染器"而**永不退订** ——
那是带宽泄漏，比黑屏更糟。

所以组件选了防抖退订这个更保守的方案。你自己在明确时机调守卫版是可以的。

---

### surface 与轨道的生命周期不同步

`SRTCVideoView` 内部处理了两个方向，但理解它有助于排查黑屏：

1. **surface 比轨道晚到**：远端轨道是信令先建对象、订阅协商完成后才绑底层轨道
   （所以拿到 `Track` 不等于有帧）；本地轨道可能在组件挂载前就采集好了。
2. **surface 会重建**：切后台、旋屏都会走一遍 destroy → create。

组件的做法是「挂载时主动挂一次 + 监听 `onTrackBindRtcTrack` 补挂」，
前提是**保持同一个组件实例** —— 不要每次 `build` 都换 `trackKey`。

---

### 宫格 + 大窗的典型布局

```typescript
build() {
  Column() {
    // 大窗：主讲人或共享
    if (this.mainUid !== undefined) {
      SMeetingRemoteVideoView({
        meeting: this.meeting,
        uid: this.mainUid,
        trackDesc: this.isSharing ? TrackDesc.screen : TrackDesc.cameraBig
      }).width('100%').height('60%')
    }

    // 宫格：其余人，小流
    Grid() {
      ForEach(this.others, (u: MeetingUserInfo) => {
        GridItem() {
          SMeetingRemoteVideoView({
            meeting: this.meeting,
            uid: u.uid,
            trackDesc: TrackDesc.cameraSmall
          })
        }
      }, (u: MeetingUserInfo) => u.uid)
    }.height('40%')
  }
}
```

<Warning>
ArkTS 的 `@Observed` / `@State` **只观测第一层属性的赋值**。
`this.users` / `this.others` 这类数组永远用「建新数组再整体赋值」，
不要 `push` / `splice` 原数组 —— 那样 UI 不会刷新。

```typescript
// ✅
this.users = m.getUsersInfoList();
// ❌
this.users.push(newUser);
```
</Warning>

---

### 大型会议：用 MCU 合流

人多时不要 N 路各自订阅，改订服务端合成的一路：

```typescript
const mcu = await meeting.subscribeRemoteVideoMcu(hostUid);
// 渲染 meeting.mcuTrack
```

客户端解码开销不随人数线性上升。布局由主持人的
`adminUpdateLayout(layoutData)` 控制，`LayoutType` 有 20 种预置。

---

### 相关阅读

+ [SMeetingRemoteVideoView](/zh/meeting/harmony/api-reference/SMeetingRemoteVideoView)
+ [媒体控制](/zh/meeting/harmony/advanced/media-control)
+ [SRTC 轨道接口](/zh/rtc/harmony/api-reference/media-tracks)
