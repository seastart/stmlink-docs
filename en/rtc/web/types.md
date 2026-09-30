---
title: "Types"
description: "Type definitions of the Web SDK: SdkInitParams, JoinOptions, AdaptiveStreamOptions, ChannelInfo, UserInfo, TrackInfo, audio/video/screen capture and publish options and presets, PiP and pop-out, local recording, event data, IM types, EnvWebInfo, and logging. Use as a lookup while coding."
---

### SdkInitParams

Parameters of the SRTC constructor.

```typescript
export interface SdkInitParams {
  /** Log level */
  logLevel?: LogLevel;
  /** Log output target */
  logTarget?: LogTarget;
  /**
   * Language (for example `zh-CN` or `en`). A process-wide global setting (since 0.7.0).
   * Affects the `Accept-Language` header sent to the server (the language of server business error messages) and the built-in text of the autoplay prompt.
   * The SDK's own errors (106xxx) are always in English and aren't affected by this parameter.
   * If omitted, follows `navigator.language`; falls back to `zh` if that isn't available.
   */
  language?: string;
  /**
   * Overrides the autoplay prompt text. A process-wide global setting (since 0.7.0).
   * Fields you don't override use the built-in Chinese / English text chosen by `language`; has no effect when the play option `disableAutoPlayDialog: true` is set.
   */
  autoPlayDialogText?: AutoPlayDialogText;
}

/** Autoplay prompt text (shown to end users) */
export interface AutoPlayDialogText {
  /** Prompt message */
  message?: string;
  /** Confirm button text */
  confirm?: string;
}
```

---

### JoinOptions

Optional parameters of `srtc.join(token, options?)`.

```typescript
export interface JoinOptions {
  /** Whether to auto-subscribe to remote audio; defaults to false */
  autoSubscribeAudio?: boolean;
  /** Whether to auto-subscribe to remote video; defaults to false */
  autoSubscribeVideo?: boolean;
  /** Preferred video codec */
  preferVideoCodec?: Codec;
  /** Preferred audio codec */
  preferAudioCodec?: Codec;
  /**
   * Whether to enable adaptive streaming for remote video.
   * When enabled, the SDK automatically picks a more suitable simulcast layer for remote video
   * based on whether the video container is shown or hidden, its size changes, and whether the page is in the foreground or background.
   *
   * Notes:
   * - Currently only takes effect with the WebRTC SeaStart SFU
   * - `true` means using the default strategy
   * - Pass an object to further adjust pixel density and the background page strategy
   */
  adaptiveStream?: boolean | AdaptiveStreamOptions;
}
```

---

### AdaptiveStreamOptions

Adaptive streaming configuration for remote video. The design goal is to pass only two key facts to the subscription layer—"is anyone watching right now, and how large is it being viewed"—and let the SDK automatically pick a more suitable simulcast layer.

```typescript
export interface AdaptiveStreamOptions {
  /**
   * Pixel density multiplier.
   * - `screen`: use the real `window.devicePixelRatio`
   * - Omitted: 2 for high-density screens by default, 1 otherwise
   */
  pixelDensity?: number | "screen";
  /**
   * Whether to treat remote video as "invisible" when the page goes to the background; defaults to true.
   * The current implementation has no "pause downlink" protocol, so in the background it switches to the lowest candidate layer rather than stopping the stream.
   */
  pauseVideoInBackground?: boolean;
}
```

---

### ChannelInfo

Channel info, returned by `srtc.join()` and also available from `srtc.getChannelInfo()`.

```typescript
export interface ChannelInfo {
  /** App ID */
  app_id: string;
  /** Channel name */
  channel: string;
  /** Media streaming vendor identifier */
  stream_vendor: string;
  /** Custom channel properties */
  props?: Record<string, any>;
  /** Channel creation time (Unix timestamp, seconds) */
  created_at: number;
  /** Channel last update time (Unix timestamp, seconds) */
  updated_at: number;
  /** Whiteboard URL with the authorization code already appended; embed it in an iframe directly. See "Whiteboard" */
  white_board: string;
}
```

---

### UserInfo

Info of users in the channel, including yourself and remote users.

```typescript
export interface UserInfo {
  /** App ID */
  app_id: string;
  /** User ID */
  uid: string;
  /** Display name */
  name: string;
  /** Device type */
  device_type: DeviceType;
  /** Device ID */
  device_id: string;
  /** Client RTC SDK version */
  version: string;
  /** Custom user properties */
  props?: Record<string, any>;
  /** Network identifier */
  net: string;
  /** Service group */
  sg: string;
  /** Last update time (Unix timestamp, seconds) */
  updated_at: number;
  /** Name of the channel the user is in */
  channel: string;
  /** Session ID */
  sid: string;
  /** Whether in audience mode */
  is_audience: boolean;
  /** Join time (Unix timestamp, seconds) */
  join_at: number;
  /** Leave time (Unix timestamp, seconds); 0 means still in the channel */
  leave_at: number;
  /** List of tracks the user is currently publishing */
  stream_tracks?: TrackInfo[];
}

/** Device type enum */
export enum DeviceType {
  /** Unknown device */
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
  /** Browser Web SDK */
  WebRTC = 6,
  /** WeChat Mini Program */
  XCX = 7,
}
```

---

### TrackInfo

Track info, available from `track.getInfo()`.

```typescript
export interface TrackInfo {
  /** Track ID */
  id: string;
  /** Track description, such as 'camera_big' or 'screen' */
  desc: string;
  /** Track type */
  kind: TrackKind;
  /** Codec */
  codec: Codec;
  /** Video width */
  width: number;
  /** Video height */
  height: number;
  /** Video frame rate */
  fps: number;
  /** Video rotation angle */
  angle: number;
  /** Bitrate */
  bitrate: number;
  /** Audio sample rate */
  sample_rate: number;
  /** Audio channel count */
  channel_count: number;
  /** Custom properties */
  props?: Record<string, any>;
  /**
   * List of simulcast fallback candidate layer ids, ordered from highest to lowest quality, containing only secondary layers lower than the current one (not itself).
   * Used by the subscriber to build the SFU's `prefer_track_ids = [current layer id, ...fallback_ids]`.
   */
  fallback_ids?: string[];
  /**
   * Whether this is a simulcast secondary layer. Only secondary layers are `true`; the main layer doesn't set it.
   * Used by `autoSubscribe` to skip secondary layers; actual layer switching is left to the SFU through the `fallback_ids` candidate pool when subscribing to the main layer.
   */
  variant?: boolean;
}

/** Track type */
export enum TrackKind {
  /** Video track */
  Video = 'video',
  /** Audio track */
  Audio = 'audio',
}

/** Codec */
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

### Audio capture, playback, and publishing

```typescript
export interface MicCaptureOptions {
  /** Microphone device ID */
  deviceId?: string;
  /** Echo cancellation (AEC) */
  echoCancellation?: boolean;
  /** Noise suppression (ANS) */
  noiseSuppression?: boolean;
  /** Automatic gain control (AGC) */
  autoGainControl?: boolean;
  /** Channel count; mono is mainly used for now */
  channelCount?: number;
  /** Sample rate */
  sampleRate?: number;
  /** Bits per sample */
  sampleSize?: number;
  /** Latency constraint */
  latency?: ConstrainDouble;
}

export interface AudioOutputOptions {
  /**
   * Output device ID
   * Only effective when the browser supports `setSinkId`
   */
  deviceId?: string;
  /** Disable the SDK's built-in guide dialog when autoplay fails */
  disableAutoPlayDialog?: boolean;
  /** Playback volume, range 0–1 */
  volume?: number;
}

export interface AudioPublishOptions {
  /** Track description, such as `mic` or `screen_audio` */
  desc: string;
  /** Codec */
  codec?: Codec;
  /** Maximum bitrate (bps) */
  maxBitrate?: number;
  /** Discontinuous transmission (DTX) */
  dtx?: boolean;
  /** Redundant audio data (RED) */
  red?: boolean;
  /** Sending priority */
  priority?: RTCPriorityType;
  /** Custom properties */
  props?: Record<string, any>;
}

export interface MicPreset {
  capture: MicCaptureOptions;
  publish: AudioPublishOptions;
}

/** Built-in microphone presets */
export declare const MicPresets: {
  /** Mono, 48 kHz, 24 Kbps */
  speech: MicPreset;
  /** Mono, 48 kHz, 32 Kbps, default preset */
  music: MicPreset;
  /** Stereo, 48 kHz, 48 Kbps */
  musicStereo: MicPreset;
  /** Mono, 48 kHz, 64 Kbps */
  musicHighQuality: MicPreset;
  /** Stereo, 48 kHz, 96 Kbps */
  musicHighQualityStereo: MicPreset;
};
```

---

### Video capture, playback, and publishing

```typescript
export interface CameraCaptureOptions {
  /** Camera device ID */
  deviceId?: string;
  /** Camera facing mode, mainly for mobile */
  facingMode?: 'user' | 'environment' | 'left' | 'right';
  /** Capture width */
  width?: number;
  /** Capture height */
  height?: number;
  /** Maximum frame rate */
  frameRate?: number;
}

export interface VideoPublishOptions {
  /** Track description, such as `camera_big` or `screen` */
  desc: string;
  /** Codec */
  codec?: Codec;
  /** Publish width; defaults to the capture width */
  width?: number;
  /** Publish height; defaults to the capture height */
  height?: number;
  /** Maximum bitrate (bps) */
  maxBitrate?: number;
  /** Maximum frame rate */
  maxFramerate?: number;
  /** Sending priority */
  priority?: RTCPriorityType;
  /** Degradation strategy on poor networks */
  degradationPreference?: RTCDegradationPreference;
  /** Custom properties */
  props?: Record<string, any>;
  /**
   * Simulcast configuration; additionally publishes video layers at different quality levels.
   *
   * **Order convention: from highest to lowest quality**, i.e., `simulcasts[0]` is the next-highest quality after the main layer,
   * and `simulcasts[length-1]` is the lowest quality. This order determines the ordering of the `TrackInfo.fallback_ids` candidate pool,
   * and is also the search order when the subscriber degrades.
   */
  simulcasts?: VideoPublishOptions[];
}

export interface CameraPreset {
  capture: CameraCaptureOptions;
  publish: VideoPublishOptions;
}

/** Built-in camera presets */
export declare const CameraPresets: {
  /** 1920×1080, 15 fps, 2.5 Mbps, maintain-resolution degradation by default */
  '1080p': CameraPreset;
  /** 1280×720, 15 fps, 1.2 Mbps, default preset, maintain-resolution degradation by default */
  '720p': CameraPreset;
  /** 640×360, 15 fps, 550 Kbps */
  '360p': CameraPreset;
  /** 320×180, 15 fps, 250 Kbps */
  '180p': CameraPreset;
};
```

---

### Screen sharing

```typescript
export interface ScreenCaptureOptions {
  /** Desired capture width */
  width?: number;
  /** Desired capture height */
  height?: number;
  /** Desired frame rate */
  frameRate?: number;
  /**
   * Content type hint, which affects the browser's encoding strategy
   * `detail` suits images/graphics
   * `text` suits documents/code
   * `motion` suits video/animation
   */
  contentHint?: 'detail' | 'text' | 'motion';
  /** Whether to show the mouse cursor */
  showCursor: boolean;
  /** Region cropping parameter on Windows */
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

/** Built-in screen sharing presets */
export declare const ScreenPresets: {
  /** 1920×1080, 10 fps, 2 Mbps, default preset, medium priority and maintain-resolution degradation by default */
  '1080p': ScreenPreset;
  /** 1280×720, 10 fps, 1.5 Mbps, medium priority and maintain-resolution degradation by default */
  '720p': ScreenPreset;
};

export interface ScreenAudioCaptureOptions {
  /** Echo cancellation */
  echoCancellation?: boolean;
  /** Noise suppression */
  noiseSuppression?: boolean;
  /** Automatic gain control */
  autoGainControl?: boolean;
}

export interface ScreenAudioPreset {
  /**
   * `true` means using the browser's default system audio capture directly
   * You can also pass finer-grained audio capture constraints
   */
  capture: ScreenAudioCaptureOptions | true;
  publish: AudioPublishOptions;
}

/** Built-in system audio presets */
export declare const ScreenAudioPresets: {
  /** Default system audio preset */
  default: ScreenAudioPreset;
};

export interface PipOptions {
  /** PiP window width */
  width?: number;
  /** PiP window height */
  height?: number;
  /** Whether to prefer Document PiP; defaults to `true` */
  preferDocumentPip?: boolean;
  /**
   * Whether to hide the original play view; defaults to `true`
   * Only effective for Document PiP; traditional video PiP relies on the original video element
   */
  hideOriginView?: boolean;
}

/** Picture-in-picture handle */
export interface PipHandle {
  /** Picture-in-picture type */
  type: 'document-pip' | 'video-pip';
  /** Reference to the new window in Document PiP mode */
  pipWindow?: Window;
  /** Exit picture-in-picture */
  exit(): Promise<void>;
}

export interface PopOutOptions {
  /** Pop-out window width */
  width?: number;
  /** Pop-out window height */
  height?: number;
  /** Pop-out window title */
  title?: string;
  /** Whether to hide the original play view; defaults to `true` */
  hideOriginView?: boolean;
}

/** Pop-out window handle */
export interface PopOutHandle {
  /** `window` reference of the pop-out window */
  window: Window;
  /** Move the video back to the given container on the main page */
  moveBack(container: HTMLElement): void;
  /** Close the pop-out window */
  close(): void;
}
```

---

### Local recording

Type definitions related to local recording (`srtc.createLocalCompositeRecorder()`) are below. For full usage, parameter tables, and scenarios, see [Local recording](/en/rtc/web/advanced/local-recording) in the advanced guides.

```typescript
/** Input tracks accepted by the local composite recorder */
export type LocalCompositeRecorderTrack =
  | MediaStreamTrack
  | LocalVideoTrack
  | RemoteVideoTrack
  | LocalAudioTrack
  | RemoteAudioTrack;

/** Local composite recorder state */
export type LocalCompositeRecorderState = 'inactive' | 'recording' | 'paused';

/** Drawing area of a video item on the recording canvas, in canvas pixels */
export interface LocalCompositeRecorderRect {
  /** Coordinate from the left edge of the canvas */
  x: number;
  /** Coordinate from the top edge of the canvas */
  y: number;
  /** Drawing area width */
  width: number;
  /** Drawing area height */
  height: number;
}

/** Drawing configuration of a single video track in local recording */
export interface LocalCompositeRecorderVideoItem {
  /** Stable unique identifier maintained by the caller; when the track for the same id changes, the slot is reused and the decode source replaced */
  id: string;
  /** Video track to draw; supports a native MediaStreamTrack or an SDK audio/video Track */
  track?: LocalCompositeRecorderTrack | null;
  /** Drawing area of this video on the recording canvas */
  rect: LocalCompositeRecorderRect;
  /** Label text drawn in the bottom-left corner of the video, such as the user name; no label is drawn if omitted */
  label?: string;
  /** Avatar URL; when this slot has no video frame to draw (e.g., the camera is off), a round avatar is drawn in the center of the tile.
   *  Loaded anonymously cross-origin; falls back to a gray circle with the nickname's first letter if loading fails or cross-origin access is refused */
  avatar?: string;
  /** Video fit mode: contain keeps the full video, cover fills the area and crops the overflow; defaults to contain */
  fit?: 'contain' | 'cover';
  /** Background color of a single video slot; defaults to #1a1c22 */
  background?: string;
}

/** Local recording start options */
export interface LocalCompositeRecorderStartOptions {
  /** Initial list of videos to draw; can later be updated with updateVideoItems to follow your app's view */
  videoItems: LocalCompositeRecorderVideoItem[];
  /** Audio tracks to mix into the recording file; supports a native MediaStreamTrack or an SDK audio/video Track */
  audioTracks?: LocalCompositeRecorderTrack[];
  /** Output video width in pixels; defaults to 1280 */
  width?: number;
  /** Output video height in pixels; defaults to 720 */
  height?: number;
  /** Frame rate of canvas.captureStream; defaults to 15 */
  fps?: number;
  /** MediaRecorder mimeType; if omitted or unsupported, a webm format supported by the browser is chosen automatically */
  mimeType?: string;
  /** Chunk interval of MediaRecorder.start(timeslice), in milliseconds; if omitted, the browser returns everything at once on stop */
  timeslice?: number;
  /** Overall background color of the recording canvas; defaults to #101216 */
  background?: string;
  /** Label background color; defaults to rgba(0, 0, 0, 0.58) */
  labelBackground?: string;
  /** Fires each time MediaRecorder outputs a valid chunk; can be used to upload or save chunks while recording */
  onDataAvailable?: (blob: Blob) => void;
}

export declare class LocalCompositeRecorder {
  /** Get the current recording state */
  getState(): LocalCompositeRecorderState;
  /** Start local recording */
  start(options: LocalCompositeRecorderStartOptions): Promise<void>;
  /** Update the list of videos to draw */
  updateVideoItems(items: LocalCompositeRecorderVideoItem[]): void;
  /** Update the audio tracks participating in the mix */
  updateAudioTracks(tracks: LocalCompositeRecorderTrack[]): Promise<void>;
  /** Pause writing the recording */
  pause(): void;
  /** Resume writing the recording */
  resume(): void;
  /** Stop recording and return the final Blob */
  stop(): Promise<Blob>;
  /** Force-destroy the recorder's internal resources */
  destroy(): void;
}
```

---

### Event data types

```typescript
export interface DisconnectEventData {
  /** Reason for leaving */
  reason: DisconnectReason;
  /** Additional error info */
  error?: any;
}

export enum DisconnectReason {
  /** Internal error */
  Error = -1,
  /** Left voluntarily */
  Self = 1,
  /** Removed from the channel */
  Kicked = 2,
  /** Replaced by another session with the same uid */
  Replace = 3,
  /** Heartbeat timeout */
  Timeout = 4,
  /** Channel destroyed */
  Destroy = 5,
}

export interface UserLeaveEventData {
  /** ID of the user who left */
  uid: string;
  /** Reason for leaving */
  reason: DisconnectReason;
}

export interface CustomMsgData {
  /** Message command */
  action: string;
  /** Message body */
  content: any;
  /** Sender's session ID */
  sid: string;
  /** Sender's user ID */
  uid: string;
  /** Channel name; may be an empty string for custom messages not sent in a channel */
  channel: string;
  /** Whether this is a private message */
  private: boolean;
}
```

---

### IM types

```typescript
export interface ImDisconnectEventData {
  /** Disconnect reason */
  reason: ImDisconnectReason;
  /** Additional error info */
  error?: any;
}

export enum ImDisconnectReason {
  /** Internal error */
  Error = -1,
  /** IM disabled voluntarily */
  Self = 1,
  /** Forced offline */
  Kicked = 2,
  /** Heartbeat timeout */
  Timeout = 4,
}

export interface ImMsgData {
  /** Message command */
  action: string;
  /** Message body */
  content: any;
  /** Sender's IM session ID */
  sid: string;
  /** Sender's user ID */
  uid: string;
  /** Sender's nickname */
  name: string;
}
```

---

### EnvWebInfo

Browser environment detection result, returned by `srtc.getEnvInfo()`. In the source, this type extends Bowser's browser parsing result; the core fields added by the Web SDK are listed here.

```typescript
export interface EnvWebInfo {
  /** Browser info */
  browser?: { name?: string; version?: string };
  /** Operating system info */
  os?: { name?: string; version?: string; versionName?: string };
  /** Device platform info */
  platform?: { type?: string; vendor?: string; model?: string };
  /** Browser engine info */
  engine?: { name?: string; version?: string };
  /** Whether WebRTC is supported */
  supported: boolean;
  /** Whether the current context is secure, e.g., HTTPS / localhost */
  secure: boolean;
  /** Whether media device access is supported */
  mediaDevices: boolean;
  /** Whether starting screen sharing is supported */
  screenshare: boolean;
  /** Whether H.264 encoding is supported */
  h264Enc: boolean;
  /** Whether H.264 decoding is supported */
  h264Dec: boolean;
  /** Whether VP8 encoding is supported */
  vp8Enc: boolean;
  /** Whether VP8 decoding is supported */
  vp8Dec: boolean;
  /** Whether Opus encoding is supported */
  opusEnc: boolean;
  /** Whether Opus decoding is supported */
  opusDec: boolean;
  /** Video encoding capabilities */
  videoEncCodecs: RTCRtpCapabilities | null;
  /** Video decoding capabilities */
  videoDecCodecs: RTCRtpCapabilities | null;
  /** Audio encoding capabilities */
  audeoEncCodecs: RTCRtpCapabilities | null;
  /** Audio decoding capabilities */
  audeoDecCodecs: RTCRtpCapabilities | null;
  /** Current User-Agent */
  ua: string;
  /** Screen width */
  screenWidth: number;
  /** Screen height */
  screenHeight: number;
  /** Page viewport width */
  clientWidth: number;
  /** Page viewport height */
  clientHeight: number;
  /** Device pixel ratio */
  devicePixelRatio: number;
}
```

---

### Logging and build info

```typescript
export enum LogLevel {
  /** Debug logs */
  DEBUG = 'debug',
  /** Info logs */
  INFO = 'info',
  /** Warning logs */
  WARN = 'warn',
  /** Error logs */
  ERROR = 'error',
}

export enum LogTarget {
  /** Output to the console */
  CONSOLE = 'console',
  /** Output to WeChat real-time logs */
  WXREALTIME = 'wxrealtime',
  /** No log output */
  NONE = 'none',
}

export interface BuildInfo {
  /** Build timestamp, in seconds */
  timestamp: number;
  /** SDK version */
  version: string;
}
```

---

### MixedAudioMediaStreamTrack

The mixed audio track returned by the `createMixedAudioMediaStreamTrack` utility function. It extends the browser's native `MediaStreamTrack` and can be passed directly to `srtc.createLocalCustomAudioTrack(...)`.

```typescript
export declare function createMixedAudioMediaStreamTrack(
  tracks: MediaStreamTrack[]
): MediaStreamTrack;
```
