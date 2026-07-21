---
title: "类型定义"
description: "Web SRTC 音视频 SDK 主要类型与结构体定义"
---

### SdkInitParams

SRTC 构造函数参数。

```typescript
export interface SdkInitParams {
  /** 日志打印等级 */
  logLevel?: LogLevel;
  /** 日志打印目标 */
  logTarget?: LogTarget;
}
```

---

### JoinOptions

`srtc.join(token, options?)` 的可选参数。

```typescript
export interface JoinOptions {
  /** 是否自动订阅远端音频，默认 false */
  autoSubscribeAudio?: boolean;
  /** 是否自动订阅远端视频，默认 false */
  autoSubscribeVideo?: boolean;
  /** 希望优先使用的视频编码 */
  preferVideoCodec?: Codec;
  /** 希望优先使用的音频编码 */
  preferAudioCodec?: Codec;
  /**
   * 是否启用远端视频自适应流。
   * 启用后，SDK 会根据 video 容器的显示/隐藏、尺寸变化，以及页面前后台状态，
   * 自动为远端视频选择更合适的 simulcast 层。
   *
   * 说明：
   * - 当前仅 WebRTC SeaStart SFU 生效
   * - `true` 表示使用默认策略
   * - 传对象可进一步调整像素密度和后台页面策略
   */
  adaptiveStream?: boolean | AdaptiveStreamOptions;
}
```

---

### AdaptiveStreamOptions

远端视频自适应流配置。设计目标是只把“当前有没有人看、正在看多大”这两个关键事实传给订阅层，由 SDK 自动选择更合适的 simulcast 层。

```typescript
export interface AdaptiveStreamOptions {
  /**
   * 像素密度倍率。
   * - `screen`：使用真实 `window.devicePixelRatio`
   * - 不传：高密屏默认取 2，其余取 1
   */
  pixelDensity?: number | "screen";
  /**
   * 页面切到后台时，是否按“不可见”处理远端视频，默认 true。
   * 当前实现没有“暂停下行”协议，因此后台时会切到最低候选层，而不是直接停流。
   */
  pauseVideoInBackground?: boolean;
}
```

---

### ChannelInfo

频道信息，由 `srtc.join()` 返回，也可通过 `srtc.getChannelInfo()` 获取。

```typescript
export interface ChannelInfo {
  /** 应用 ID */
  app_id: string;
  /** 频道名 */
  channel: string;
  /** 流媒体服务商标识 */
  stream_vendor: string;
  /** 频道自定义扩展属性 */
  props?: Record<string, any>;
  /** 频道创建时间（Unix 时间戳，秒） */
  created_at: number;
  /** 频道最近更新时间（Unix 时间戳，秒） */
  updated_at: number;
  /** 白板地址 */
  white_board: string;
}
```

---

### UserInfo

频道内用户信息，包含本人和远端用户。

```typescript
export interface UserInfo {
  /** 应用 ID */
  app_id: string;
  /** 用户 ID */
  uid: string;
  /** 会中昵称 */
  name: string;
  /** 设备类型 */
  device_type: DeviceType;
  /** 设备 ID */
  device_id: string;
  /** 客户端 RTC SDK 版本号 */
  version: string;
  /** 用户自定义扩展属性 */
  props?: Record<string, any>;
  /** 网络标识 */
  net: string;
  /** 服务分组 */
  sg: string;
  /** 最近更新时间（Unix 时间戳，秒） */
  updated_at: number;
  /** 所在频道名 */
  channel: string;
  /** 会话 ID */
  sid: string;
  /** 是否为观众模式 */
  is_audience: boolean;
  /** 加入时间（Unix 时间戳，秒） */
  join_at: number;
  /** 退出时间（Unix 时间戳，秒），0 表示仍在频道中 */
  leave_at: number;
  /** 用户当前发布的流轨道列表 */
  stream_tracks?: TrackInfo[];
}

/** 终端类型枚举 */
export enum DeviceType {
  /** 未知设备 */
  Unknown = 0,
  /** Windows */
  Windows = 1,
  /** Android */
  Android = 2,
  /** iOS */
  IOS = 3,
  /** Linux */
  Linux = 4,
  /** macOS */
  MacOS = 5,
  /** 浏览器 Web SDK */
  WebRTC = 6,
  /** 微信小程序 */
  XCX = 7,
}
```

---

### TrackInfo

流轨道信息，可通过 `track.getInfo()` 获取。

```typescript
export interface TrackInfo {
  /** 轨道 ID */
  id: string;
  /** 轨道描述，例如 'camera_big'、'screen' */
  desc: string;
  /** 轨道类型 */
  kind: TrackKind;
  /** 编码类型 */
  codec: Codec;
  /** 视频宽 */
  width: number;
  /** 视频高 */
  height: number;
  /** 视频帧率 */
  fps: number;
  /** 视频旋转角度 */
  angle: number;
  /** 码率 */
  bitrate: number;
  /** 音频采样率 */
  sample_rate: number;
  /** 音频声道数 */
  channel_count: number;
  /** 自定义扩展属性 */
  props?: Record<string, any>;
  /**
   * simulcast 降级候选层 id 列表，按画质从高到低排列，仅包含比当前层低的副层（不含自己）。
   * 订阅侧用于拼 SFU 的 `prefer_track_ids = [当前层 id, ...fallback_ids]`。
   */
  fallback_ids?: string[];
  /**
   * 是否为 simulcast 副层。仅副层为 `true`，主层不写。
   * 用于 `autoSubscribe` 跳过副层，真正的层切换通过订阅主层时的 `fallback_ids` 候选池交给 SFU。
   */
  variant?: boolean;
}

/** 流轨道类型 */
export enum TrackKind {
  /** 视频轨道 */
  Video = 'video',
  /** 音频轨道 */
  Audio = 'audio',
}

/** 编码类型 */
export enum Codec {
  /** H.264 */
  H264 = 0x1b,
  /** H.265 */
  H265 = 0x24,
  /** AAC */
  AAC = 0x0f,
  /** VP8 */
  VP8 = 0x38,
  /** VP9 */
  VP9 = 0x39,
  /** AV1 */
  AV1 = 0x3a,
  /** Opus */
  OPUS = 0x5355504f,
}
```

---

### 音频采集、播放、发布相关

```typescript
export interface MicCaptureOptions {
  /** 麦克风设备 ID */
  deviceId?: string;
  /** 回声消除（AEC） */
  echoCancellation?: boolean;
  /** 降噪（ANS） */
  noiseSuppression?: boolean;
  /** 自动增益（AGC） */
  autoGainControl?: boolean;
  /** 声道数，目前主要使用单声道 */
  channelCount?: number;
  /** 采样率 */
  sampleRate?: number;
  /** 每个采样点位数 */
  sampleSize?: number;
  /** 延迟约束 */
  latency?: ConstrainDouble;
}

export interface AudioOutputOptions {
  /**
   * 输出设备 ID
   * 仅在浏览器支持 `setSinkId` 时有效
   */
  deviceId?: string;
  /** 自动播放失败时，禁用 SDK 内置引导弹窗 */
  disableAutoPlayDialog?: boolean;
  /** 播放音量，范围 0 ~ 1 */
  volume?: number;
}

export interface AudioPublishOptions {
  /** 轨道描述，例如 `mic`、`screen_audio` */
  desc: string;
  /** 编码格式 */
  codec?: Codec;
  /** 最大码率（bps） */
  maxBitrate?: number;
  /** 不连续传输（DTX） */
  dtx?: boolean;
  /** 冗余音频数据（RED） */
  red?: boolean;
  /** 发送优先级 */
  priority?: RTCPriorityType;
  /** 自定义扩展属性 */
  props?: Record<string, any>;
}

export interface MicPreset {
  capture: MicCaptureOptions;
  publish: AudioPublishOptions;
}

/** 麦克风内置预设参数 */
export declare const MicPresets: {
  /** 单声道，48kHz，24 Kbps */
  speech: MicPreset;
  /** 单声道，48kHz，32 Kbps，默认预设 */
  music: MicPreset;
  /** 双声道，48kHz，48 Kbps */
  musicStereo: MicPreset;
  /** 单声道，48kHz，64 Kbps */
  musicHighQuality: MicPreset;
  /** 双声道，48kHz，96 Kbps */
  musicHighQualityStereo: MicPreset;
};
```

---

### 视频采集、播放、发布相关

```typescript
export interface CameraCaptureOptions {
  /** 摄像头设备 ID */
  deviceId?: string;
  /** 摄像头朝向，主要用于移动端 */
  facingMode?: 'user' | 'environment' | 'left' | 'right';
  /** 采集宽度 */
  width?: number;
  /** 采集高度 */
  height?: number;
  /** 最大帧率 */
  frameRate?: number;
}

export interface VideoPublishOptions {
  /** 轨道描述，例如 `camera_big`、`screen` */
  desc: string;
  /** 编码格式 */
  codec?: Codec;
  /** 发布宽度，默认沿用采集宽度 */
  width?: number;
  /** 发布高度，默认沿用采集高度 */
  height?: number;
  /** 最大码率（bps） */
  maxBitrate?: number;
  /** 最大帧率 */
  maxFramerate?: number;
  /** 发送优先级 */
  priority?: RTCPriorityType;
  /** 弱网降级策略 */
  degradationPreference?: RTCDegradationPreference;
  /** 自定义扩展属性 */
  props?: Record<string, any>;
  /**
   * 联播（Simulcast）配置，会额外发布多路不同清晰度的视频。
   *
   * **顺序约定：按画质从高到低排列**，即 `simulcasts[0]` 是仅次于主层的次高画质，
   * `simulcasts[length-1]` 是最低画质。该顺序决定了 `TrackInfo.fallback_ids` 候选池的排序，
   * 也是订阅侧降级时的搜索顺序。
   */
  simulcasts?: VideoPublishOptions[];
}

export interface CameraPreset {
  capture: CameraCaptureOptions;
  publish: VideoPublishOptions;
}

/** 摄像头内置预设参数 */
export declare const CameraPresets: {
  /** 1920×1080，15fps，2.5 Mbps，默认 maintain-resolution 降级策略 */
  '1080p': CameraPreset;
  /** 1280×720，15fps，1.2 Mbps，默认预设，默认 maintain-resolution 降级策略 */
  '720p': CameraPreset;
  /** 640×360，15fps，550 Kbps */
  '360p': CameraPreset;
  /** 320×180，15fps，250 Kbps */
  '180p': CameraPreset;
};
```

---

### 屏幕共享相关

```typescript
export interface ScreenCaptureOptions {
  /** 期望采集宽度 */
  width?: number;
  /** 期望采集高度 */
  height?: number;
  /** 期望帧率 */
  frameRate?: number;
  /**
   * 内容类型提示，会影响浏览器编码策略
   * `detail` 适合图片/图形
   * `text` 适合文档/代码
   * `motion` 适合视频/动画
   */
  contentHint?: 'detail' | 'text' | 'motion';
  /** 是否显示鼠标 */
  showCursor: boolean;
  /** Windows 侧的区域裁剪参数 */
  rect: {
    x: number;
    y: number;
    w: number;
    h: number;
  };
}

export interface ScreenPreset {
  capture: ScreenCaptureOptions;
  publish: VideoPublishOptions;
}

/** 屏幕共享内置预设参数 */
export declare const ScreenPresets: {
  /** 1920×1080，10fps，2 Mbps，默认预设，默认 medium 优先级和 maintain-resolution 降级策略 */
  '1080p': ScreenPreset;
  /** 1280×720，10fps，1.5 Mbps，默认 medium 优先级和 maintain-resolution 降级策略 */
  '720p': ScreenPreset;
};

export interface ScreenAudioCaptureOptions {
  /** 回声消除 */
  echoCancellation?: boolean;
  /** 降噪 */
  noiseSuppression?: boolean;
  /** 自动增益 */
  autoGainControl?: boolean;
}

export interface ScreenAudioPreset {
  /**
   * `true` 表示直接使用浏览器默认系统音频采集能力
   * 也可以传入更细粒度的音频采集约束
   */
  capture: ScreenAudioCaptureOptions | true;
  publish: AudioPublishOptions;
}

/** 系统音频内置预设参数 */
export declare const ScreenAudioPresets: {
  /** 默认系统音频预设 */
  default: ScreenAudioPreset;
};

export interface PipOptions {
  /** PiP 窗口宽度 */
  width?: number;
  /** PiP 窗口高度 */
  height?: number;
  /** 是否优先使用 Document PiP，默认 `true` */
  preferDocumentPip?: boolean;
  /**
   * 是否隐藏原始播放视图，默认 `true`
   * 仅对 Document PiP 生效，传统 video PiP 依赖原始 video 元素
   */
  hideOriginView?: boolean;
}

/** 画中画句柄 */
export interface PipHandle {
  /** 画中画类型 */
  type: 'document-pip' | 'video-pip';
  /** Document PiP 模式下的新窗口引用 */
  pipWindow?: Window;
  /** 主动退出画中画 */
  exit(): Promise<void>;
}

export interface PopOutOptions {
  /** 弹出窗口宽度 */
  width?: number;
  /** 弹出窗口高度 */
  height?: number;
  /** 弹出窗口标题 */
  title?: string;
  /** 是否隐藏原始播放视图，默认 `true` */
  hideOriginView?: boolean;
}

/** 弹出窗口句柄 */
export interface PopOutHandle {
  /** 弹出窗口的 `window` 引用 */
  window: Window;
  /** 将视频移回主页面指定容器 */
  moveBack(container: HTMLElement): void;
  /** 关闭弹出窗口 */
  close(): void;
}
```

---

### 本地合成录制相关

本地合成录制（`srtc.createLocalCompositeRecorder()`）相关的类型定义如下。完整用法、参数表与场景说明见进阶实践的 [本地合成录制](/zh/rtc/web/advanced/local-recording)。

```typescript
/** 本地合成录制器可接受的输入轨道 */
export type LocalCompositeRecorderTrack =
  | MediaStreamTrack
  | LocalVideoTrack
  | RemoteVideoTrack
  | LocalAudioTrack
  | RemoteAudioTrack;

/** 本地合成录制器状态 */
export type LocalCompositeRecorderState = 'inactive' | 'recording' | 'paused';

/** 视频项在录制画布上的绘制区域，单位为 canvas 像素 */
export interface LocalCompositeRecorderRect {
  /** 距离画布左侧的坐标 */
  x: number;
  /** 距离画布顶部的坐标 */
  y: number;
  /** 绘制区域宽度 */
  width: number;
  /** 绘制区域高度 */
  height: number;
}

/** 单个视频轨道在本地合成录制中的绘制配置 */
export interface LocalCompositeRecorderVideoItem {
  /** 调用方维护的稳定唯一标识；同一个 id 的 track 变更时会复用槽位并替换解码源 */
  id: string;
  /** 要绘制的视频轨道；支持原生 MediaStreamTrack 或 SDK 音视频 Track */
  track?: LocalCompositeRecorderTrack | null;
  /** 该视频在录制画布上的绘制区域 */
  rect: LocalCompositeRecorderRect;
  /** 绘制在视频左下角的标签文本，例如用户名；不传则不绘制标签 */
  label?: string;
  /** 头像 URL；当该槽位没有可绘制视频帧（如摄像头关闭）时，在格子中央绘制圆形头像。
   *  匿名跨域加载，加载失败或跨域被拒时回退为昵称首字母灰底圆 */
  avatar?: string;
  /** 视频填充方式：contain 保留完整画面，cover 填满区域并裁剪溢出部分；默认 contain */
  fit?: 'contain' | 'cover';
  /** 单个视频槽位背景色；默认 #1a1c22 */
  background?: string;
}

/** 本地合成录制启动参数 */
export interface LocalCompositeRecorderStartOptions {
  /** 初始视频绘制列表；后续可通过 updateVideoItems 跟随业务视角更新 */
  videoItems: LocalCompositeRecorderVideoItem[];
  /** 需要混入录制文件的音频轨道；支持原生 MediaStreamTrack 或 SDK 音视频 Track */
  audioTracks?: LocalCompositeRecorderTrack[];
  /** 输出视频宽度，单位为像素；默认 1280 */
  width?: number;
  /** 输出视频高度，单位为像素；默认 720 */
  height?: number;
  /** canvas.captureStream 的帧率；默认 15 */
  fps?: number;
  /** MediaRecorder mimeType，未传或不支持时自动选择浏览器支持的 webm 格式 */
  mimeType?: string;
  /** MediaRecorder.start(timeslice) 的分片间隔，单位毫秒；不传则浏览器在 stop 时一次性返回 */
  timeslice?: number;
  /** 录制画布整体背景色；默认 #101216 */
  background?: string;
  /** 标签背景色；默认 rgba(0, 0, 0, 0.58) */
  labelBackground?: string;
  /** 每次 MediaRecorder 输出有效分片时触发，可用于边录边上传或保存分片 */
  onDataAvailable?: (blob: Blob) => void;
}

export declare class LocalCompositeRecorder {
  /** 获取当前录制状态 */
  getState(): LocalCompositeRecorderState;
  /** 开始本地合成录制 */
  start(options: LocalCompositeRecorderStartOptions): Promise<void>;
  /** 更新视频绘制列表 */
  updateVideoItems(items: LocalCompositeRecorderVideoItem[]): void;
  /** 更新参与混音的音频轨道 */
  updateAudioTracks(tracks: LocalCompositeRecorderTrack[]): Promise<void>;
  /** 暂停录制写入 */
  pause(): void;
  /** 恢复录制写入 */
  resume(): void;
  /** 停止录制并返回最终 Blob */
  stop(): Promise<Blob>;
  /** 强制销毁录制器内部资源 */
  destroy(): void;
}
```

---

### 事件数据类型

```typescript
export interface DisconnectEventData {
  /** 离开原因 */
  reason: DisconnectReason;
  /** 额外错误信息 */
  error?: any;
}

export enum DisconnectReason {
  /** 内部错误 */
  Error = -1,
  /** 主动离开 */
  Self = 1,
  /** 被踢出频道 */
  Kicked = 2,
  /** 同一账号被其他终端顶替 */
  Replace = 3,
  /** 心跳超时 */
  Timeout = 4,
  /** 频道被销毁 */
  Destroy = 5,
}

export interface UserLeaveEventData {
  /** 离开的用户 ID */
  uid: string;
  /** 离开原因 */
  reason: DisconnectReason;
}

export interface CustomMsgData {
  /** 消息命令 */
  action: string;
  /** 消息体 */
  content: any;
  /** 发送者会话 ID */
  sid: string;
  /** 发送者用户 ID */
  uid: string;
  /** 所在频道名；非频道内自定义消息时可能为空字符串 */
  channel: string;
  /** 是否为私发消息 */
  private: boolean;
}
```

---

### IM 相关类型

```typescript
export interface ImDisconnectEventData {
  /** 断开原因 */
  reason: ImDisconnectReason;
  /** 额外错误信息 */
  error?: any;
}

export enum ImDisconnectReason {
  /** 内部错误 */
  Error = -1,
  /** 主动关闭 IM */
  Self = 1,
  /** 被踢下线 */
  Kicked = 2,
  /** 心跳超时 */
  Timeout = 4,
}

export interface ImMsgData {
  /** 消息命令 */
  action: string;
  /** 消息体 */
  content: any;
  /** 发送者 IM 会话 ID */
  sid: string;
  /** 发送者用户 ID */
  uid: string;
  /** 发送者昵称 */
  name: string;
}
```

---

### EnvWebInfo

浏览器环境检测结果，由 `srtc.getEnvInfo()` 返回。该类型在源码中继承自 Bowser 的浏览器解析结果，这里列出 Web SDK 额外补充的核心字段。

```typescript
export interface EnvWebInfo {
  /** 浏览器信息 */
  browser?: { name?: string; version?: string };
  /** 操作系统信息 */
  os?: { name?: string; version?: string; versionName?: string };
  /** 设备平台信息 */
  platform?: { type?: string; vendor?: string; model?: string };
  /** 浏览器引擎信息 */
  engine?: { name?: string; version?: string };
  /** 是否支持 WebRTC */
  supported: boolean;
  /** 当前上下文是否为安全环境，例如 HTTPS / localhost */
  secure: boolean;
  /** 是否支持访问媒体设备 */
  mediaDevices: boolean;
  /** 是否支持发起屏幕共享 */
  screenshare: boolean;
  /** 是否支持 H.264 编码 */
  h264Enc: boolean;
  /** 是否支持 H.264 解码 */
  h264Dec: boolean;
  /** 是否支持 VP8 编码 */
  vp8Enc: boolean;
  /** 是否支持 VP8 解码 */
  vp8Dec: boolean;
  /** 是否支持 Opus 编码 */
  opusEnc: boolean;
  /** 是否支持 Opus 解码 */
  opusDec: boolean;
  /** 视频编码能力 */
  videoEncCodecs: RTCRtpCapabilities | null;
  /** 视频解码能力 */
  videoDecCodecs: RTCRtpCapabilities | null;
  /** 音频编码能力 */
  audeoEncCodecs: RTCRtpCapabilities | null;
  /** 音频解码能力 */
  audeoDecCodecs: RTCRtpCapabilities | null;
  /** 当前 User-Agent */
  ua: string;
  /** 屏幕宽度 */
  screenWidth: number;
  /** 屏幕高度 */
  screenHeight: number;
  /** 页面可视区域宽度 */
  clientWidth: number;
  /** 页面可视区域高度 */
  clientHeight: number;
  /** 设备像素比 */
  devicePixelRatio: number;
}
```

---

### 日志与编译信息

```typescript
export enum LogLevel {
  /** 调试日志 */
  DEBUG = 'debug',
  /** 信息日志 */
  INFO = 'info',
  /** 警告日志 */
  WARN = 'warn',
  /** 错误日志 */
  ERROR = 'error',
}

export enum LogTarget {
  /** 输出到控制台 */
  CONSOLE = 'console',
  /** 输出到微信实时日志 */
  WXREALTIME = 'wxrealtime',
  /** 不输出日志 */
  NONE = 'none',
}

export interface BuildInfo {
  /** 构建时间戳，单位秒 */
  timestamp: number;
  /** SDK 版本号 */
  version: string;
}
```

---

### MixedAudioMediaStreamTrack

`createMixedAudioMediaStreamTrack` 工具函数返回的混音轨道，继承自浏览器原生 `MediaStreamTrack`，可直接传入 `srtc.createLocalCustomAudioTrack(...)`。

```typescript
export declare function createMixedAudioMediaStreamTrack(
  tracks: MediaStreamTrack[]
): MediaStreamTrack;
```
