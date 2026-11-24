---
title: "类型定义"
description: "微信小程序 SRTC 音视频 SDK 完整类型与结构体定义"
---

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



### EnvWxInfo
```typescript
/**
 * 微信小程序环境详情
 */
export interface EnvWxInfo {
	system: WechatMiniprogram.SystemInfo;
	device: WechatMiniprogram.DeviceInfo;
}
```

### JoinParams
```typescript
/**
 * 加入频道选项
 */
export interface JoinParams {
	/** 线路号 */
	netID: string;
	/** 服务器分组id */
	sgID: string;
}
```

### PusherOptions
```typescript
/**
* 小程序推流器配置
* @see https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html
*/
export interface PusherOptions {
	/**
	 * 推流地址
	 */
	url: string;
	/**
	 * 是否开启摄像头
	 */
	enableCamera: boolean;
	/**
	 * 视频描述
	 */
	videoDesc?: string;
	/**
	 * 视频自定义属性
	 */
	videoProps?: Record<string, any>;
	/**
	 * 前置或后置摄像头
	 */
	devicePosition: "front" | "back";
	/**
	 * 推流画面是否镜像
	 */
	remoteMirror: boolean;
	/**
	 * 本地预览画面是否镜像
	 */
	localMirror: "auto" | "enable" | "disable";
	/**
	 * 视频推流宽度
	 */
	width: number;
	/**
	 * 视频推流高度
	 */
	height: number;
	/**
	 * 帧率
	 */
	fps: number;
	/**
	 * 美颜。取值范围 0-9，0表示关闭
	 */
	beautyLevel: number;
	/**
	 * 美白。取值范围 0-9，0表示关闭
	 */
	whitenessLevel: number;
	/**
	 * 是否开启麦克风
	 */
	enableMic: boolean;
	/**
	 * 音频描述
	 */
	audioDesc?: string;
	/**
	 * 音频自定义属性
	 */
	audioProps?: Record<string, any>;
	/**
	 * 是否开启音频自动增益
	 */
	enableAgc: boolean;
	/**
	 * 是否开启音频噪声抑制
	 */
	enableAns: boolean;
	/**
	 * 最小码率 kbps
	 */
	minBitrate: number;
	/**
	 * 最大码率 kbps
	 */
	maxBitrate: number;
}
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



### 会前网络检测相关

`srtc.networkCheck()` 的参数与结果类型。

#### NetworkCheckOptions

```typescript
export interface NetworkCheckOptions {
  /** 应用 ID，与 serverUrl 一起使用；也可以只传 token 由 SDK 从中解出 */
  appId?: string;
  /** SDK 接口地址，即入会 token 里的 client_api（如 https://rtc.example.com/client/） */
  serverUrl?: string;
  /**
   * 入会 / IM token（可选）。已有 token 时可只传它，SDK 从中取应用 ID 与 SDK 接口地址；
   * 同时传了 appId / serverUrl 时以显式传入的为准。检测不会用 token 鉴权，过期的 token 也可以
   */
  token?: string;
  /** 单项超时 ms，默认 3000 */
  timeoutMs?: number;
  /** 进度回调：每完成一项回调一次（按固定顺序） */
  onItem?: (item: NetworkCheckItem) => void;
}
```

#### NetworkCheckResult

```typescript
export interface NetworkCheckResult {
  /** 总状态：有 fail 即 fail；无 fail 但有 warning 即 warning；否则 ok（skipped / unsupported 不参与） */
  status: 'ok' | 'warning' | 'fail';
  /** 固定 5 项、固定顺序：permission、connectivity、mtu、dns、server */
  items: NetworkCheckItem[];
  /** 总耗时 ms */
  costMs: number;
}
```

#### NetworkCheckItem

```typescript
/** 检测项 id */
export type NetworkCheckItemId = 'permission' | 'connectivity' | 'mtu' | 'dns' | 'server';

/**
 * 单项 / 子检查状态：pass 通过；warning 有隐患但不影响使用；fail 不通过；
 * skipped 无需检测；unsupported 当前平台不支持该检测
 */
export type NetworkCheckItemStatus = 'pass' | 'warning' | 'fail' | 'skipped' | 'unsupported';

export interface NetworkCheckItem {
  /** 检测项 id */
  id: NetworkCheckItemId;
  /** 检测状态 */
  status: NetworkCheckItemStatus;
  /** 机器可读的原因码，pass 时为空串 */
  reason: string;
  /** 给人看的中文说明，可直接展示给用户 */
  message: string;
  /** 本项耗时 ms */
  costMs: number;
  /**
   * 各项的测量值：
   * - permission / mtu / dns：{}
   * - connectivity：{ netType: NetworkCheckNetType }
   * - server：NetworkCheckServerData
   */
  data: Record<string, any>;
}

/** 网络类型 */
export type NetworkCheckNetType = 'wifi' | 'cellular' | 'ethernet' | 'unknown';
```

#### NetworkCheckServerData

服务器连接项（`id` 为 `server`）的 `data`，包含 SDK 接口、信令、媒体 3 个子检查。

```typescript
export interface NetworkCheckSubResult {
  /** 是否连通 */
  ok: boolean;
  /** 子检查状态（skipped / unsupported 时 ok 为 false，但不计为失败） */
  status: NetworkCheckItemStatus;
  /** 机器可读原因码，pass 时为空 */
  reason: string;
  /** 耗时 ms（未执行时为 0） */
  rttMs: number;
}

export interface NetworkCheckServerData {
  /**
   * SDK 接口是否可达。失败时 httpStatus 为非 200 的 HTTP 状态码（服务端版本较老、没有该接口时为 404），
   * code 为服务端返回的业务错误码（如 app_id 不存在）
   */
  api: NetworkCheckSubResult & { code?: number; httpStatus?: number };
  /** 信令是否可连；JS 只能走 WebSocket，via 恒为 'ws' */
  signal: NetworkCheckSubResult & { via: 'tcp' | 'ws' };
  /** 媒体（SFU UDP）是否可达 */
  media: NetworkCheckSubResult;
}
```

#### 原因码

| `reason` | 出现在 | 含义 | `message` |
| --- | --- | --- | --- |
| `offline` | connectivity | 当前没有网络连接 | 当前没有网络连接 |
| `api_unreachable` | server、`data.api` | SDK 接口调不通：网络不通、服务地址不对、服务端版本较老没有检测接口，或服务端返回业务错误 | 无法连接服务器，请检查网络或服务器地址 |
| `signal_unreachable` | server、`data.signal` | 信令 WebSocket 连不上 | 无法连接信令服务器，请联系网络管理员放行 |
| `udp_blocked` | server、`data.media` | 媒体服务器 UDP 不通 | 无法连接媒体服务器（UDP 被拦截），请联系网络管理员放行 |
| `media_unavailable` | server、`data.media` | 服务端暂无可用的媒体节点 | 服务器暂无可用的媒体节点，请稍后重试 |
| `vendor_not_supported` | `data.media`（skipped） | 服务端流媒体不是 seastart，没有可探测的媒体节点 | —— |
| `server_info_unavailable` | `data.signal`、`data.media`（skipped） | SDK 接口没调通，拿不到信令 / 媒体地址 | —— |

信令与媒体都失败时，server 项的 `reason` 取信令的原因。

---

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
  /** 微信实时日志 */
	WXREALTIME = "wxrealtime",
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

