---
title: "类型定义"
description: "Web SRTC 音视频 SDK 完整类型与结构体定义"
---

### SdkInitParams

SRTC 构造函数参数。

```typescript
export interface SdkInitParams {
  /** 日志打印等级，默认 LogLevel.WARN */
  logLevel?: LogLevel;
  /** 日志打印目标，默认 LogTarget.CONSOLE */
  logTarget?: LogTarget;
}
```typescript

---

### JoinOptions

`srtc.join(token, options?)` 的可选参数。

```typescript
export interface JoinOptions {
  /**
   * 用户自定义属性，加入频道后其他用户可通过 UserInfo.props 获取
   */
  props?: Record<string, any>;
}
```

---

### ChannelInfo

频道信息，由 `srtc.join` 返回，也可通过 `srtc.getChannelInfo()` 获取。

```typescript
export interface ChannelInfo {
  /** 应用 ID */
  app_id: string;
  /** 频道名 */
  channel: string;
  /** 流媒体服务商标识 */
  stream_vendor?: string;
  /** 白板配置信息 */
  white_board?: Record<string, any>;
  /** 频道自定义扩展属性 */
  props?: Record<string, any>;
  /** 频道创建时间（Unix 时间戳，秒） */
  created_at: number;
  /** 频道最近更新时间（Unix 时间戳，秒） */
  updated_at: number;
}
```typescript

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
  /** 信息最近更新时间（Unix 时间戳，秒） */
  updated_at: number;
  /** 所在频道名 */
  channel: string;
  /** 会话 ID */
  sid: string;
  /**
   * 是否为观众模式（类似研讨会观众，只收流不推流）
   * 由服务端签发 Token 时决定
   */
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
  Unknown = 0,
  Windows = 1,
  Android = 2,
  IOS = 3,
  Linux = 4,
  MacOS = 5,
  WebRTC = 6,
  /** 微信小程序 */
  XCX = 7,
}
```

---

### TrackInfo

流轨道信息，归属于某个 `BaseTrack`，可通过 `track.getInfo()` 获取。

```typescript
export interface TrackInfo {
  /** 轨道 ID，在频道内唯一 */
  id: string;
  /** 轨道描述，如 'camera_big'、'screen' */
  desc: string;
  /** 轨道类型 */
  kind: TrackKind;
  /** 编码类型 */
  codec: Codec;
  /** 视频宽（音频轨道为 0） */
  width: number;
  /** 视频高（音频轨道为 0） */
  height: number;
  /** 视频帧率（音频轨道为 0） */
  fps: number;
  /** 视频旋转角度 */
  angle: number;
  /** 码率（bps） */
  bitrate: number;
  /** 音频采样率（视频轨道为 0） */
  sampleRate: number;
  /** 自定义扩展属性 */
  props?: Record<string, any>;
}

export enum TrackKind {
  Video = 'video',
  Audio = 'audio',
}
```typescript

---

### 音频采集、播放、发布相关

```typescript
/** 麦克风采集配置 */
export interface MicCaptureOptions {
  /** 设备 ID */
  deviceId?: string;
  /** 回声消除（AEC） */
  echoCancellation?: boolean;
  /** 降噪（ANS） */
  noiseSuppression?: boolean;
  /** 自动增益（AGC） */
  autoGainControl?: boolean;
  /** 声道数（目前仅支持单声道） */
  channelCount?: number;
  /** 采样率，目前固定 16kHz */
  sampleRate?: number;
  /** 每个采样点位数（bits per sample），默认 16 */
  sampleSize?: number;
  /** 延迟约束 */
  latency?: ConstrainDouble;
}

/** 扬声器播放配置 */
export interface AudioOutputOptions {
  /**
   * 输出设备 ID
   * 仅在浏览器支持 setSinkId 时有效
   */
  deviceId?: string;
  /**
   * 音量（0 ~ 1），默认 1
   */
  volume?: number;
  /**
   * 当自动播放因权限被阻止时，禁用 SDK 内置的播放引导弹窗，改为手动处理
   */
  disableAutoPlayDialog?: boolean;
}

/** 音频发布配置 */
export interface AudioPublishOptions {
  /** 轨道描述 */
  desc: string;
  /** 编码格式 */
  codec?: Codec;
  /** 最大码率（bps） */
  maxBitrate?: number;
  /** 不连续传输（DTX），默认对单声道启用 */
  dtx?: boolean;
  /** 冗余音频数据（RED），默认对单声道启用 */
  red?: boolean;
  /** 发送优先级，默认音频优先 */
  priority?: RTCPriorityType;
  /** 自定义扩展属性 */
  props?: Record<string, any>;
}

/** 麦克风预设值 */
export interface MicPreset {
  capture: MicCaptureOptions;
  publish: AudioPublishOptions;
}

/** 麦克风内置预设参数 */
export declare const MicPresets: {
  /** 单声道，48kHz，24 Kbps */
  speech: MicPreset;
  /** 单声道，48kHz，32 Kbps（默认） */
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
/** 摄像头采集配置 */
export interface CameraCaptureOptions {
  /** 设备 ID */
  deviceId?: string;
  /** 摄像头朝向（移动端） */
  facingMode?: 'user' | 'environment' | 'left' | 'right';
  /** 采集宽度 */
  width?: number;
  /** 采集高度 */
  height?: number;
  /** 最大帧率 */
  frameRate?: number;
}

/** 视频发布配置 */
export interface VideoPublishOptions {
  /** 轨道描述 */
  desc: string;
  /** 编码格式 */
  codec?: Codec;
  /** 发布宽度（默认与采集宽度一致） */
  width?: number;
  /** 发布高度（默认与采集高度一致） */
  height?: number;
  /** 最大码率（bps） */
  maxBitrate?: number;
  /** 最大帧率 */
  maxFramerate?: number;
  /**
   * 带宽受限时的降级策略
   * 'maintain-framerate' | 'maintain-resolution' | 'balanced'
   */
  degradationPreference?: RTCDegradationPreference;
  /**
   * 联播（Simulcast）配置，配置后会同时发布多路不同清晰度的流
   */
  simulcasts?: SimulcastLayer[];
  /** 发送优先级 */
  priority?: RTCPriorityType;
  /** 自定义扩展属性 */
  props?: Record<string, any>;
}

/** 摄像头预设值 */
export interface CameraPreset {
  capture: CameraCaptureOptions;
  publish: VideoPublishOptions;
}

/** 摄像头内置预设参数 */
export declare const CameraPresets: {
  /** 1920×1080，15fps，2.5 Mbps */
  '1080p': CameraPreset;
  /** 1280×720，15fps，1.2 Mbps（默认） */
  '720p': CameraPreset;
  /** 640×360，15fps，550 Kbps */
  '360p': CameraPreset;
  /** 320×180，15fps，250 Kbps */
  '180p': CameraPreset;
};
```typescript

---

### 屏幕共享相关

```typescript
/** 屏幕采集配置 */
export interface ScreenCaptureOptions {
  /** 期望采集宽度 */
  width?: number;
  /** 期望采集高度 */
  height?: number;
  /** 期望帧率 */
  frameRate?: number;
  /**
   * 内容类型提示，影响编码策略
   * 'motion'  → 视频/游戏，优化流畅度
   * 'detail'  → 图片/图形，优化清晰度
   * 'text'    → 文档/代码，优化文字清晰度
   */
  contentHint?: 'motion' | 'detail' | 'text';
  /**
   * 是否显示鼠标指针
   * 'always' | 'motion' | 'never'
   */
  showCursor?: 'always' | 'motion' | 'never';
  /**
   * 采集区域裁剪（部分浏览器支持）
   */
  rect?: { x: number; y: number; width: number; height: number };
}

/** 屏幕共享预设值 */
export interface ScreenPreset {
  capture: ScreenCaptureOptions;
  publish: VideoPublishOptions;
}

/** 屏幕共享内置预设参数 */
export declare const ScreenPresets: {
  /** 1920×1080，10fps，2 Mbps（默认） */
  '1080p': ScreenPreset;
  /** 1280×720，10fps，1.5 Mbps */
  '720p': ScreenPreset;
};

/** 系统音频采集配置 */
export interface ScreenAudioCaptureOptions {
  /** 回声消除 */
  echoCancellation?: boolean;
  /** 降噪 */
  noiseSuppression?: boolean;
  /** 自动增益 */
  autoGainControl?: boolean;
}

/** 系统音频预设值 */
export interface ScreenAudioPreset {
  capture: ScreenAudioCaptureOptions;
  publish: AudioPublishOptions;
}

/** 系统音频内置预设参数 */
export declare const ScreenAudioPresets: {
  /** 默认系统音频预设 */
  default: ScreenAudioPreset;
};

/** 画中画配置 */
export interface PipOptions {
  /** 画中画窗口宽度 */
  width?: number;
  /** 画中画窗口高度 */
  height?: number;
  /** 是否优先使用 Document PiP，默认 true */
  preferDocumentPip?: boolean;
  /**
   * 是否隐藏原始播放视图，默认 true
   * 仅在 Document PiP 生效，传统 video PiP 仍依赖原始 video 元素
   */
  hideOriginView?: boolean;
}

/** 画中画句柄 */
export interface PipHandle {
  /** 画中画类型 */
  type: 'document-pip' | 'video-pip';
  /** Document PiP 模式下的新窗口引用 */
  pipWindow?: Window;
  /** 退出画中画 */
  exit(): Promise<void>;
}

/** 弹出窗口配置 */
export interface PopOutOptions {
  /** 弹出窗口宽度 */
  width?: number;
  /** 弹出窗口高度 */
  height?: number;
  /** 弹出窗口标题 */
  title?: string;
  /** 是否隐藏原始播放视图，默认 true */
  hideOriginView?: boolean;
}

/** 弹出窗口句柄 */
export interface PopOutHandle {
  /** 弹出窗口的 window 引用 */
  window: Window;
  /** 将视频回收到主页面指定容器 */
  moveBack(container: HTMLElement): void;
  /** 关闭弹出窗口 */
  close(): void;
}
```

---

### 事件数据类型

```typescript
/** 强制离开事件 data */
export interface DisconnectEventData {
  reason: DisconnectReason;
  error?: any;
}

export enum DisconnectReason {
  Error = -1,
  /** 主动离开 */
  Self = 1,
  /** 被踢出 */
  Kicked = 2,
  /** 被顶号（同一账号在另一端登录） */
  Replace = 3,
  /** 心跳超时 */
  Timeout = 4,
  /** 频道销毁 */
  Destroy = 5,
}

/** 用户离开事件 data */
export interface UserLeaveEventData {
  uid: string;
  reason: DisconnectReason;
}

/** 频道内自定义消息 data */
export interface CustomMsgData {
  /** 消息命令 */
  action: string;
  /** 消息内容 */
  content: any;
  /** 发送者会话 ID */
  sid: string;
  /** 发送者用户 ID */
  uid: string;
  /** 所在频道名 */
  channel: string;
}
```typescript

---

### IM 相关类型

```typescript
/** IM 断开事件 data */
export interface ImDisconnectEventData {
  reason: ImDisconnectReason;
  error?: any;
}

export enum ImDisconnectReason {
  Error = -1,
  Self = 1,
  Kicked = 2,
  Timeout = 4,
}

/** IM 消息 data */
export interface ImMsgData {
  /** 消息命令 */
  action: string;
  /** 消息内容 */
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

浏览器环境检测结果，由 `srtc.getEnvInfo()` 返回。

```typescript
export interface EnvWebInfo {
  /** 浏览器信息 */
  browser: { name?: string; version?: string };
  /** 操作系统信息 */
  os: { name?: string; version?: string; versionName?: string };
  /** 平台信息 */
  platform: { type?: string; vendor?: string; model?: string };
  /** 渲染引擎 */
  engine: { name?: string; version?: string };
  /** 是否支持 WebRTC */
  supported: boolean;
  /** 当前上下文是否安全（HTTPS / localhost / 127.0.0.1） */
  secure: boolean;
  /** 是否可访问媒体设备（麦克风、摄像头） */
  mediaDevices: boolean;
  /** 是否支持屏幕共享 */
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
  /** 支持的视频编码能力 */
  videoEncCodecs: RTCRtpCapabilities | null;
  /** 支持的视频解码能力 */
  videoDecCodecs: RTCRtpCapabilities | null;
  /** 支持的音频编码能力 */
  audeoEncCodecs: RTCRtpCapabilities | null;
  /** 支持的音频解码能力 */
  audeoDecCodecs: RTCRtpCapabilities | null;
  /** User-Agent 字符串 */
  ua: string;
  screenWidth: number;
  screenHeight: number;
  clientWidth: number;
  clientHeight: number;
  devicePixelRatio: number;
}
```typescript

---

### 日志与编译信息

```typescript
export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARN = 'warn',
  ERROR = 'error',
}

export enum LogTarget {
  /** 输出到控制台 */
  CONSOLE = 'console',
  /** 不打印任何日志 */
  NONE = 'none',
}

export interface BuildInfo {
  /** 编译时间戳（秒） */
  timestamp: number;
  /** SDK 版本号 */
  version: string;
}
```

---

### MixedAudioMediaStreamTrack

`createMixedAudioMediaStreamTrack` 工具函数返回的混音轨道，继承自浏览器原生 `MediaStreamTrack`，可直接传入 `srtc.createLocalCustomAudioTrack`。

```typescript
/**
 * 将多路 MediaStreamTrack 混合为单路音频轨道
 * @param tracks 要混合的音频 MediaStreamTrack 数组
 * @returns 合并后的 MediaStreamTrack
 */
export declare function createMixedAudioMediaStreamTrack(
  tracks: MediaStreamTrack[]
): MediaStreamTrack;
```typescript
