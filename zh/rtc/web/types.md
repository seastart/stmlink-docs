### ChannelInfo
```typescript
/**
 * 频道信息
 */
export interface ChannelInfo {
	/** 应用id */
	app_id: string;
	/** 频道名 */
	channel: string;
	/** 频道扩展属性 */
	props?: Record<string, any>;
	/** 频道创建时间 */
	created_at: number;
	/** 频道更新时间 */
	updated_at: number;
}
```

### UserInfo
```typescript
/**
 * 用户信息
 */
export interface UserInfo {
	/** 应用id */
	app_id: string;
	/** 用户id */
	uid: string;
	/** 会中昵称 */
	name: string;
	/** 设备类型 */
	device_type: DeviceType;
	/** 设备ID */
	device_id: string;
	/** 客户端RTCsdk版本号 */
	version: string;
	/** 用户扩展属性 */
	props?: Record<string, any>;
	/** 网络号 */
	net: string;
	/** 服务分组 */
	sg: string;
	/** 更新时间 */
	updated_at: number;
	/** 频道名 */
	channel: string;
	/** 会话id */
	sid: string;
	/** 是否观众，类似研讨会观众，只收流 */
	is_audience: boolean;
	/** 进入时间 */
	join_at: number;
	/** 退出时间 */
	leave_at: number;
	/** 流轨道 */
	stream_tracks?: TrackInfo[];
}

/**
 * 终端类型枚举
 */
export enum DeviceType {
    /**
     * 未知设备
     */
    Unknown = 0,
    /**
     * Windows
     */
    Windows = 1,
    /**
     * Android
     */
    Android = 2,
    /**
     * iOS
     */
    IOS = 3,
    /**
     * Linux
     */
    Linux = 4,
    /**
     * MacOS
     */
    MacOS = 5,
    /**
     * webrtc
     */
    WebRTC = 6,
    /**
     * 小程序
     */
    XCX = 7
}
```

### TrackInfo
```typescript
/**
 * 流轨道信息
 */
export interface TrackInfo {
    /** 轨道id，在stream里唯一，在全局不一定唯一 */
    id: string;
    /** 自定义描述，如摄像头大流、摄像头小流、共享桌面流等 */
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
    /** 视频角度 */
    angle: number;
    /** 码率 */
    bitrate: number;
    /** 音频采样率 */
    sampleRate: number;
    /** 流扩展属性 */
    props?: Record<string, any>;
}

/** 
 * 流轨道类型 
 */
export enum TrackKind {
    Video = 'video',
    Audio = 'audio',
}
```



### EnvWebInfo
```typescript
/**
 * web环境详情
 */
export interface EnvWebInfo {
  /**
   * 浏览器
   */
  browser: {
    name?: string;
    version?: string;
  };
  /**
   * 操作系统
   */
  os: {
    name?: string;
    version?: string;
    versionName?: string;
  };
  /**
   * 平台
   */
  platform: {
    type?: string;
    vendor?: string;
    model?: string;
  };
  /**
   * 浏览器渲染引擎
   */
  engine: {
    name?: string;
    version?: string;
  };
	/**
	 * 是否支持webrtc
	 */
	supported: boolean;
	/**
	 * 当前上下文是否安全(https或localhost或127.0.0.1)
	 */
	secure: boolean;
	/**
	 * 是否支持获取麦克风、摄像头等媒体设备进行枚举、音视频采集、推流
	 */
	mediaDevices: boolean;
	/**
	 * 是否支持发起屏幕共享
	 */
	screenshare: boolean;
	/**
	 * 是否支持h264编码
	 */
	h264Enc: boolean;
	/**
	 * 是否支持h264解码
	 */
	h264Dec: boolean;
	/**
	 * 是否支持vp8编码
	 */
	vp8Enc: boolean;
	/**
	 * 是否支持vp8解码
	 */
	vp8Dec: boolean;
	/**
	 * 是否支持opus编码
	 */
	opusEnc: boolean;
	/**
	 * 是否支持opus解码
	 */
	opusDec: boolean;
	/**
	 * 当前支持的视频编码
	 */
	videoEncCodecs: RTCRtpCapabilities | null;
	/**
	 * 当前支持的视频解码
	 */
	videoDecCodecs: RTCRtpCapabilities | null;
	/**
	 * 当前支持的音频编码
	 */
	audeoEncCodecs: RTCRtpCapabilities | null;
	/**
	 * 当前支持的音频解码
	 */
	audeoDecCodecs: RTCRtpCapabilities | null;
	/**
	 * ua
	 */
	ua: string;
	/**
	 * 屏幕宽度
	 */
	screenWidth: number;
	/**
	 * 屏幕高度
	 */
	screenHeight: number;
	/**
	 * 可视区域宽度
	 */
	clientWidth: number;
	/**
	 * 可视区域高度
	 */
	clientHeight: number;
	/**
	 * 设备的物理像素分辨率与CSS像素分辨率之比
	 */
	devicePixelRatio: number;
}
```



### 声音采集、播放、发布相关
```typescript
/**
 * 麦克风采集配置
 */
export interface MicCaptureOptions {
	/**
	 * 设备id
	 */
	deviceId?: string;
	/**
	 * AEC回声消除
	 */
	echoCancellation?: boolean;
	/**
	 * ANS降噪
	 */
	noiseSuppression?: boolean;
	/**
	 * AGC自动增益
	 */
	autoGainControl?: boolean;
	/**
	 * 声道数，目前只支持单声道
	 */
	channelCount?: number;
	/**
	 * 采样率16k/48k，目前固定16k
	 */
	sampleRate?: number;
	/**
	 * 每个采样点大小的位数(bits per sample)，默认16
	 */
	sampleSize?: number;
	/**
	 * the latency or range of latencies which are acceptable and/or required.
	 */
	latency?: ConstrainDouble;
}

/**
 * 扬声器配置
 */
export interface AudioOutputOptions {
	/**
	 * deviceId to output audio
	 *
	 * Only supported on browsers where `setSinkId` is available
	 */
	deviceId?: string;
	/**
	 * 当因权限问题自动播放失败时，禁用sdk自带的播放弹窗，手动处理
	 */
	disableAutoPlayDialog?: boolean;
}

/**
 * 音频发布配置
 */
export interface AudioPublishOptions {
	/** 描述 */
	desc: string;
	/** 编码格式 */
	codec?: Codec;
	/** 最大码率 */
	maxBitrate?: number;
	/**
	 * dtx (Discontinuous Transmission of audio), enabled by default for mono tracks.
	 */
	dtx?: boolean;
	/**
	 * red (Redundant Audio Data), enabled by default for mono tracks.
	 */
	red?: boolean;
	/**
	 * 优先级，默认音频优先
	 */
	priority?: RTCPriorityType;
	/** 自定义属性 */
	props?: Record<string, any>;
}

/**
 * 麦克风预设值
 */
export interface MicPreset {
	capture: MicCaptureOptions;
	publish: AudioPublishOptions;
}

/**
 * 麦克风预设参数
 */
export declare const MicPresets: {
	/** 单声道，采样率48kHz，码率24Kbps */
	speech: MicPreset;
	/** 单声道，采样率48kHz，码率32Kbps，createLocalMicTrack的默认预设参数 */
	music: MicPreset;
	/** 双声道，采样率48kHz，码率48Kbps */
	musicStereo: MicPreset;
	/** 单声道，采样率48kHz，码率64Kbps */
	musicHighQuality: MicPreset;
	/** 双声道，采样率48kHz，码率96Kbps */
	musicHighQualityStereo: MicPreset;
};

```

### 视频采集、播放、发布相关
```typescript
/**
 * 摄像头采集配置
 */
export interface CameraCaptureOptions {
	/**
	 * 设备id
	 */
	deviceId?: string;
	/**
	 * webrtc专用：摄像头朝向
	 * @see https://developer.mozilla.org/en-US/docs/Web/API/MediaTrackConstraints/facingMode
	 */
	facingMode?: "user" | "environment" | "left" | "right";
	/**
	 * 宽
	 */
	width?: number;
	/**
	 * 高
	 */
	height?: number;
	/**
	 * 最大帧率
	 */
	frameRate?: number;
}

/**
 * 视频发布配置
 */
export interface VideoPublishOptions {
	/** 描述 */
	desc: string;
	/** 编码格式 */
	codec?: Codec;
	/**
	 * 宽(默认采集到的宽)
	 */
	width?: number;
	/**
	 * 高(默认采集到的高)
	 */
	height?: number;
	/** 最大码率 */
	maxBitrate?: number;
	/** 最大帧率 */
	maxFramerate?: number;
	/**
	 * 优先级，默认音频优先
	 */
	priority?: RTCPriorityType;
	/** 自定义属性 */
	props?: Record<string, any>;
}

/**
 * 摄像头预设值
 */
export interface CameraPreset {
	capture: CameraCaptureOptions;
	publish: VideoPublishOptions;
}

/**
 * 摄像头预设参数
 */
export declare const CameraPresets: {
	/** 分辨率1920*1080，帧率15，码率2.5Mbps */
	"1080p": CameraPreset;
	/** 分辨率1280*720，帧率15，码率1.2Mbps，createLocalCameraTrack的默认预设参数 */
	"720p": CameraPreset;
	/** 分辨率640*360，帧率15，码率550Kbps */
	"360p": CameraPreset;
	/** 分辨率320*180，帧率15，码率250Kbps */
	"180p": CameraPreset;
};

/**
 * 屏幕采集配置
 */
export interface ScreenCaptureOptions {
	/**
	 * 宽
	 */
	width?: number;
	/**
	 * 高
	 */
	height?: number;
	/**
	 * 帧率
	 */
	frameRate?: number;
}

/**
 * 屏幕采集预设值
 */
export interface ScreenPreset {
	capture: ScreenCaptureOptions;
	publish: VideoPublishOptions;
}

/**
 * 屏幕采集预设值
 */
export interface ScreenPreset {
	capture: ScreenCaptureOptions;
	publish: VideoPublishOptions;
}

/**
 * 屏幕共享预设参数
 */
export declare const ScreenPresets: {
	/** 分辨率1920*1080，帧率10，码率2Mbps，createLocalScreenTrack时的默认预设参数 */
	"1080p": ScreenPreset;
	/** 分辨率1280*720，帧率10，码率1.5Mbps */
	"720p": ScreenPreset;
};
```

### DisconnectEventData
```typescript
/**
 * 强制离开事件data
 */
export interface DisconnectEventData {
	/** 离开原因 */
	reason: DisconnectReason;
	/** 错误 */
	error?: any;
}

/**
 * 用户离开频道的原因
 */
export declare enum DisconnectReason {
	/** 错误 */
	Error = -1,
	/** 主动离开 */
	Self = 1,
	/** 被踢离开 */
	Kicked = 2,
	/** 被顶号 */
	Replace = 3,
	/** 心跳超时离开 */
	Timeout = 4,
	/** 频道销毁离开 */
	Destroy = 5
}
```

### UserLeaveEventData
```typescript
/**
 * 用户离开事件data
 */
export interface UserLeaveEventData {
	/** 用户id */
	uid: string;
	/** 离开原因 */
	reason: DisconnectReason;
}
```



### CustomMsgData
```typescript
/**
 * 自定义消息
 */
export interface CustomMsgData {
    /** 消息命令 */
    action: string;
    /** 消息体 */
    content: any;
    /** 发送者会话id */
    sid: string;
    /** 发送者ID */
    uid: string;
    /** 频道名(如果非频道内自定义消息，为空) */
    channel: string;
}
```



### ImDisconnectEventData
```typescript
/**
 * im断开事件data
 */
export interface ImDisconnectEventData {
	/** 断开原因 */
	reason: ImDisconnectReason;
	/** 错误 */
	error?: any;
}

/**
 * 用户断开im的原因
 */
export declare enum ImDisconnectReason {
	/** 错误 */
	Error = -1,
	/** 主动离开 */
	Self = 1,
	/** 被踢离开 */
	Kicked = 2,
	/** 心跳超时离开 */
	Timeout = 4
}
```



### ImMsgData
```typescript
/**
 * im频道外消息
 */
export interface ImMsgData {
	/** 消息命令 */
	action: string;
	/** 消息体 */
	content: any;
	/** 发送者im会话id */
	sid: string;
	/** 发送者ID */
	uid: string;
	/** 发送者昵称 */
	name: string;
}
```



### LogLevel / LogTarget / BuildInfo
```typescript
/**
 * 日志打印等级
 */
export declare enum LogLevel {
	DEBUG = "debug",
	INFO = "info",
	WARN = "warn",
	ERROR = "error"
}
/**
 * 日志打印目标
 */
export declare enum LogTarget {
	/** 控制台打印 */
	CONSOLE = "console",
	/** 不打任何日志 */
	NONE = "none"
}
/**
 * sdk编译信息
 */
export interface BuildInfo {
	/** 编译时间s */
	timestamp: number;
	/** sdk版本号 */
	version: string;
}
```

