---
title: "核心概念"
description: "理解 SRTC HarmonyOS SDK 中 SRTCEngine、Channel、Track、渲染层与设备管理的关系"
---

### 整体模型

对象模型可以概括为：

+ `SRTCEngine`：SDK 主入口，负责入会和创建本地轨道
+ `Channel`：一次真实的频道连接，负责发布、订阅、用户列表和事件分发
+ `Track`：音频或视频流的抽象对象
+ `ChannelDelegate` / `TrackDelegate`：事件回调入口
+ `SRTCVideoView` / `SRTCVideoRenderer`：视频渲染层
+ `SRTC`：只做一件事 —— 把宿主的 Context 交给 SDK（见下方「为什么需要 `SRTC.init`」）

从第一性原理看，RTC 系统本质上是在同步三类状态：

+ 连接状态
+ 用户状态
+ 媒体轨道状态

SDK 也是围绕这三类状态设计的，理解这套模型之后，绝大多数接口都会变得自然。

---

### 为什么需要 `SRTC.init`

```typescript
export default class EntryAbility extends UIAbility {
  onCreate(): void {
    SRTC.init(this.context);
  }
}
```

这是 HarmonyOS 特有的一步。摄像头档位查询需要 Context，而 HAR 形态的库拿不到宿主的
Context（`getContext()` 只在 UI 组件里可用），所以必须由集成方在 `UIAbility.onCreate`
里交一次。

<Warning>
不调用**不会报错**，但摄像头分辨率会退化为"由底层自行吸附档位"，实际分辨率因机型而异，
你在 `CameraPreset` 里设定的值不再生效。
</Warning>

---

### SRTCEngine 与 Channel

#### `SRTCEngine`

更像一个「工厂 + 会话入口」，通常只用它做两件事：

+ `joinChannel(tokenString, options?)`
+ `createLocalMicTrack(...)` / `createLocalCameraTrack(...)` / `createLocalScreenTrack(...)`

它是**无参构造**，日志级别通过属性设置：

```typescript
const srtc: SRTCEngine = new SRTCEngine();
srtc.logLevel = LogLevel.info;
```

#### `Channel`

加入频道成功后，真正承载业务状态的是 `Channel`：

+ 发布本地轨道、订阅远端轨道
+ 获取频道信息与用户信息
+ 监听用户进出、轨道变化、断线重连、自定义消息

可以把它理解为「已经完成鉴权和网络连接的一次 RTC 会话」。

`joinChannel` 可以调用多次，一个引擎能同时加入多个频道，各频道的发布、订阅、成员与事件
互不干扰；`srtc.channels` 是当前存活的频道列表，`srtc.defaultChannel` 是最早加入的那个。

**轨道属于引擎而不是频道** —— 同一条采集轨道可以发布给多个频道，采集只做一次。

---

### Track 体系

继承关系（父类一般不用直接接触，但知道层级有助于理解类型标注）：

```
Track
├── LocalTrack
│   ├── LocalAudioTrack ── LocalMicTrack / LocalScreenAudioTrack
│   └── LocalVideoTrack ── LocalCameraTrack / LocalScreenTrack
└── RemoteTrack
    ├── RemoteAudioTrack ── RemoteAudioMixTrack
    └── RemoteVideoTrack
```

#### 本地轨道

| 类型 | 创建方式 | 说明 |
| --- | --- | --- |
| `LocalMicTrack` | `srtc.createLocalMicTrack(preset?)` | 麦克风采集 |
| `LocalCameraTrack` | `srtc.createLocalCameraTrack(preset?)` | 摄像头采集 |
| `LocalScreenTrack` | `srtc.createLocalScreenTrack(preset?, audioPreset?)` | 屏幕采集 |
| `LocalScreenAudioTrack` | 随屏幕采集一并产生 | 屏幕共享里的系统音频 |

<Note>
本地轨道类本身都是**无参构造**，预设要经引擎传入 —— 写 `new LocalCameraTrack(preset)`
是编不过的。
</Note>

采集与发布是**两件独立的事**：

```typescript
const camera = srtc.createLocalCameraTrack(cameraPreset720p());
await camera.startCapture();                    // 开始采集（本地能看到画面）
await channel.publishLocalVideoTrack(camera);   // 发布出去（对端能看到）
```

只 `startCapture` 不 `publish`，就是「本地预览、不推流」；这也是不需要服务端就能自测
采集与渲染链路的办法。

#### 远端轨道

| 类型 | 说明 |
| --- | --- |
| `RemoteAudioTrack` | 远端单路音频 |
| `RemoteAudioMixTrack` | 远端**云端混音**轨道，见下节 |
| `RemoteVideoTrack` | 远端视频 |

远端轨道由信令先建对象、订阅协商完成后才绑定底层轨道 —— 所以拿到 `Track` 对象不等于
已经有帧，渲染组件内部会等 `onTrackBindRtcTrack` 再挂。

---

### 音频的 Mix 模式

SeaStart 引擎支持在**服务端**把多路音频混成一路下发，客户端只订阅这一条
（`RemoteAudioMixTrack`），省掉 N 路解码。

+ 混音轨的 id 与描述固定是 `audio_mix`，与其它端一致 —— 服务端按这个字符串识别
+ `channel.getFilterUids()` 非空时表示只混指定用户的音频

对多人会议来说这是默认更优的形态：人数增长时客户端解码开销不随之线性上升。

---

### 视频渲染

#### `SRTCVideoView`（推荐）

SDK 自带的 ArkUI 组件，视频帧由底层直接写进 XComponent 的 surface，**不经过 ArkUI 的
绘制流程** —— 这是唯一能承受 30fps 全屏刷新的路径。

```typescript
SRTCVideoView({ track: this.cameraTrack, trackKey: this.cameraTrack.id })
  .width('100%')
  .height(240)
```

<Warning>
**`track` 是普通成员变量，不能声明成 `@Prop`。**

ArkTS 的 `@Prop` 对复杂类型做**深拷贝**，且拷贝过程中除基本类型 / Map / Set / Date /
Array 之外**会丢失类型** —— `Track` 拷过来会变成一个没有方法的普通对象，结果是画面黑屏、
事件也永远收不到。

`@Link` / `@ObjectLink` 能引用传递，但要求父组件为每一路画面单独持有一个 `@State`，
多路远端画面根本写不出来。所以轨道走**普通成员变量**（构造时按引用传入），
**换轨道靠组件重建** —— 让 `if` 分支或 `ForEach` 的 key 带上 trackId。
</Warning>

#### `SRTCVideoRenderer` / `VideoRendererRegistry`

需要自己接渲染（比如画到自定义画布、或做录制）时用这一层。`VideoRendererRegistry`
维护 trackKey → 渲染器的映射，`SRTCVideoView` 内部也是走它。

绝大多数业务不需要碰这层。

---

### 设备管理

`DeviceManager.shared` 是单例，提供：

+ 摄像头 / 麦克风 / 扬声器枚举：`cameras()` / `microphones()` / `speakers()` / `getDevices()`
+ 热插拔事件：`DeviceManagerDelegate`

枚举出来的 `deviceId` 可以直接喂回采集参数（`CameraCaptureOptions.deviceId`），
这条回路是设备切换能力的地基。

音频**输出路由**是另一套：`AudioRouteSession`，负责扬声器 / 听筒的持久设置与通话中临时
切换。外接设备（蓝牙 / 有线）由系统接管，SDK 只上报不主动切换。

---

### 流媒体引擎

频道用哪套引擎由服务端下发的 `stream_vendor` 决定，SDK 侧对应 `StreamVendor`：

| 值 | 说明 |
| --- | --- |
| `seastart` | SeaStart 自研 SFU，支持云端混音与 Simulcast |
| `wangsucdn` | 网宿 CDN |

业务代码通常不需要关心这个，但排障时 `channel.streamVendor` 能告诉你当前走的是哪条路。

---

### 事件模型

频道级事件走 `ChannelDelegate`：加入成功、重连 / 断开、用户加入离开更新、远端轨道增删改、
自定义消息、网络质量、活跃说话人、Simulcast 层切换。

轨道级事件走 `TrackDelegate`：轨道信息变化、静音 / 取消静音、采集结束、镜像变化、
底层轨道绑定完成。

```typescript
channel.delegates.add(myDelegate);
```

<Warning>
**`delegates` 是强引用，必须成对 `add` / `remove`。**

ArkTS 既没有弱引用、也没有 `deinit`。注册后不摘除会导致监听者永不回收，
而且离开页面后仍然收到回调。通常在组件的 `aboutToAppear` / `aboutToDisappear` 里配对处理。

`channel.delegates` / `track.delegates` / `AudioRouteSession.delegates` 都是这样。
</Warning>

详细清单见 [事件参考](/zh/rtc/harmony/events)。

---

### 建议继续阅读

+ [静音与停止发布](/zh/rtc/harmony/advanced/mute-vs-unpublish)
+ [设备管理](/zh/rtc/harmony/advanced/device-management)
+ [音频路由](/zh/rtc/harmony/advanced/audio-routing)
+ [屏幕共享](/zh/rtc/harmony/advanced/screen-sharing)
+ [多频道](/zh/rtc/harmony/advanced/multi-channel)
+ [通话质量](/zh/rtc/harmony/advanced/call-quality)
