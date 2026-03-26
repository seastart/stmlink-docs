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
  /** 联播（Simulcast）配置，会额外发布多路不同清晰度的视频 */
  simulcasts?: VideoPublishOptions[];
}

export interface CameraPreset {
  capture: CameraCaptureOptions;
  publish: VideoPublishOptions;
}

/** 摄像头内置预设参数 */
export declare const CameraPresets: {
  /** 1920×1080，15fps，2.5 Mbps */
  '1080p': CameraPreset;
  /** 1280×720，15fps，1.2 Mbps，默认预设 */
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
  /** 1920×1080，10fps，2 Mbps，默认预设 */
  '1080p': ScreenPreset;
  /** 1280×720，10fps，1.5 Mbps */
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
