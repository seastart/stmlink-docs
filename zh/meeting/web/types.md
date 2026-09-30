---
title: "类型定义"
description: "Web SMeeting 会议 SDK 完整类型与结构体定义"
---

#### 轨道描述 TrackDesc
```typescript
/** 轨道描述 */
export enum TrackDesc {
    /** 麦克风流 */
    MIC = 'mic',
    /** 摄像头大流 */
    CAMERAL_BIG = 'camera_big',
    /** 摄像头小流 */
    CAMERAL_SMALL = 'camera_small',
    /** 桌面共享流 */
    SCREEN = 'screen',
}
```

#### 举手类型 HandupType
```typescript
/**
 * 举手类型
 */
export enum HandupType {
    /**
     * 申请开麦克风
     */
    Mic = 1,
    /**
     * 申请开摄像头
     */
    Camera = 2,
    /**
     * 申请聊天
     */
    Chat = 3
}
```

#### 用户举手动作步骤  UserHandupStep
```typescript
/**
 * 用户举手动作步骤
 */
export enum UserHandupStep {
    /**
     * 请求举手
     */
    Request = 1,
    /**
     * 取消举手
     */
    Cancel = 2,
    /**
     * 确认打开设备
     */
    ConfirmOpen = 3,
    /**
     * 拒绝打开设备
     */
    RejectOpen = 4,
}
```

#### 摄像头状态 CameraState
```typescript
/**
 * 摄像头状态
 */
export enum CameraState {
    /**
     * 开
     */
    On = 1,
    /**
     * 关
     */
    Off = 2,
}
```

#### 麦克风状态 MicState
```typescript
/**
 * 麦克风状态
 */
export enum MicState {
    /**
     * 开
     */
    On = 1,
    /**
     * 关
     */
    Off = 2,
}

```

#### 房间共享类型 ShareType 
```typescript
/**
 * 房间共享类型
 */
export enum ShareType {
    /**
     * 屏幕共享
     */
    Screen = 1,
    /**
     * 电子白板
     */
    WhiteBoard = 2,
}

```

#### 共享状态 ShareState
```typescript
export type ShareState = 0 | ShareType;
```

#### 角色类型 Role
```typescript
/**
 * 角色类型
 */
export enum Role {
    /**
     * 普通成员
     */
    Member = 0,
    /**
     * 主持人
     */
    Host = 1,
    /**
     * 联席主持人
     */
    CoHost = 2,
}
```

#### 聊天消息类型 ChatMsgType
```typescript
/**
 * 聊天消息类型
 */
export enum ChatMsgType {
    /**
     * 文本
     */
    Text = 1,
    /**
     * 文件
     */
    File = 2,
    /**
     * 图片
     */
    Pic = 3,
    /**
     * 语音
     */
    Sound = 4,
}
```

#### 用户离开房间的原因 DisconnectReason
```typescript
/**
 * 用户离开房间的原因
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
	/** 房间销毁离开 */
	Destroy = 5
}
```

#### 会议类型 MeetingType
```typescript
/**
 * 会议类型
 */
export enum MeetingType {
    /** 即时会议 */
    Instant = 1,
    /** 预约会议 */
    Appointment = 2
}
```

#### 入会静音状态 EntryMutePolicy
```typescript
/**
 * 入会静音状态
 */
export enum EntryMutePolicy {
    /** 开启入会静音(所有人入会默认静音) */
    Silent = 1,
    /** 不限制，跟随客户端初始音频状态 */
    UnRestrict = 2,
    /** 超6人静音(超过6人后入会静音) */
    SilentAfter6 = 3,
}
```

#### 登录sdk的token信息 MeetingToken
```typescript
/**
 * 登录sdk的token信息
 */
export interface MeetingToken {
    /** 应用ID */
    app_id: string;
    /** 用户ID */
    user_id: string;
    /** 过期时间 */
    exp_at: number;
    /** 客户端密钥 */
    client_key: string;
    /** sdk接口前缀 */
    client_api: string;
}
```

#### 用户类型 UserType
```typescript
/**
 * 用户类型
 */
export enum UserType {
    /** 普通用户 */
    Normal = 1,
    /** SIP用户 */
    SIP = 2,
    /** H323用户 */
    H323 = 3,
}
```

#### sdk构造参数 SdkInitParams
```typescript
/**
 * sdk构造参数
 */
export interface SdkInitParams {
    /** 日志等级 */
    logLevel?: LogLevel;
    /** 日志目标 */
    logTarget?: LogTarget;
    /**
     * 语言（如 `zh-CN`、`en`），进程级全局配置，会同时设置底层 SRTC（0.3.0 起）。
     * 影响：请求会议服务端 / SRTC 服务端时的 `Accept-Language` 头（服务端业务错误文案的语言）、自动播放提示框的内置文案。
     * SDK 自身的报错（206xxx，以及透传的 106xxx）固定为英文，不受此参数影响。
     * 不传则跟随 `navigator.language`，取不到时为 `zh`。
     */
    language?: string;
    /**
     * 自动播放提示框文案覆盖，进程级全局配置（0.3.0 起）。
     * 未覆盖的字段按 `language` 取内置中 / 英文案。类型见 SRTC 的 AutoPlayDialogText。
     */
    autoPlayDialogText?: AutoPlayDialogText;
}
```

#### 创建/修改会议参数 MeetingCreateReq
```typescript
/**
 * 创建/修改会议参数
 */
export interface MeetingCreateReq {
    /** 房间号 */
    room_no?: string;
    /** 会议标题 */
    title: string;
    /** 会议说明 */
    content?: string;
    /** 会议限制类型(默认无限制) */
    attend_type?: AttendType,
    /** 参会人员用户id */
    conferee?: string[];
    /** 入会密码 */
    password?: string;
    /** 会议类型 1:即时会议(默认) 2：预约会议 */
    meeting_type?: MeetingType;
    /** 开始时间(时间戳秒) */
    plan_time?: number;
    /** 会议时长(单位分钟) */
    plan_dur?: number;
    /** 入会静音选项 */
    entry_mute_policy?: EntryMutePolicy;
    /** 水印是否关闭 */
    watermark_disabled?: boolean;
    /** 截屏是否禁止 */
    screenshot_disabled?: boolean;
    /** 房间禁聊天 */
    chat_disabled?: boolean;
    /** 扩展字段 */
    extend_info?: string;
    /** 会议模式(默认普通模式) */
    meeting_mode: MeetingMode,
    /** 布局 */
    layout_data?: LayoutData
    /** 是否开启录制 */
    auto_record?: boolean
}
```

#### 加入会议参数 MeetingEnterReq
```typescript
/**
 * 加入会议参数
 */
export interface MeetingEnterReq {
    /** 房间号 */
    room_no: string;
    /** 入会密码 */
    password?: string;
    /** 会中昵称 */
    nickname: string;
    /** 会中头像 */
    avatar?: string;
    /** 扩展字段 */
    extend_info?: string;
}
```

#### 房间信息
```typescript
/**
 * 房间信息
 */
export interface RoomInfo {
    /** 会议ID */
    id: string;
    /** 房间号 */
    room_no: string;
    /** 会议标题 */
    title: string;
    /** 会议说明 */
    content: string;
    /** 会议类型，1即时会议, 2预约会议 */
    meeting_type: MeetingType;
    /** 开始时间，unix时间戳(秒) */
    begin_time: number;
    /** 结束时间，unix时间戳(秒) */
    end_time: number;
    /** 入会静音选项，1 入会默认静音，2 跟随客户端初始音频状态，3 超过6人后入会静音 */
    entry_mute_policy: EntryMutePolicy;
    /** 关水印设置，false不限, true关水印 */
    watermark_disabled: boolean;
    /** 禁截屏设置，false不限, true禁截屏 */
    screenshot_disabled: boolean;
    /** 禁聊设置，false不限, true禁聊 */
    chat_disabled: boolean;
    /** 静音设置，false不限, true静音 */
    mic_disabled: boolean;
    /** 禁画设置，false不限, true禁画 */
    camera_disabled: boolean;
    /** 禁自我解除静音，false不限, true禁解除 */
    self_unmute_mic_disabled: boolean;
    /** 禁自我解除禁画，false不限, true禁解除 */
    self_unmute_camera_disabled: boolean;
    /** 房间锁定状态，false不限, true锁定 */
    locked: boolean;
    /** 共享状态，0无, 1屏幕, 2白板 */
    share_state: ShareState;
    /** 共享者ID */
    share_uid: string;
    /** 创建者ID */
    creator: string;
    /** 主持人ID */
    host_uid: string;
    /** 联席主持ID列表 */
    co_hosts: string[];
    /** 自定义扩展，json串表示的键值对 */
    extend_info: string;
}
```

#### 用户信息 UserInfo
```typescript
/**
 * 用户信息
 */
export interface UserInfo {
    /** 用户id */
    uid: string;
    /** 会中昵称 */
    name: string;
    /** 设备类型 */
    device_type: DeviceType;
    /** 设备ID */
    device_id: string;
    /** 客户端sdk版本号 */
    version: string;
    /** 进入时间 */
    join_at: number;

    /** 会中角色，0普通, 1主持, 2联席主持 */
    role: Role;
    /** 会中头像 */
    avatar: string;
    /** 麦克风状态，1开, 2关 */
    mic_state: MicState;
    /** 摄像头状态，1开, 2关 */
    camera_state: CameraState;
    /** 共享状态，0无, 1屏幕, 2白板 */
    share_state: ShareState;
    /** 是否被踢出，false正常, true被踢 */
    is_kickout: boolean;
    /** 禁聊设置，false不限, true禁聊 */
    chat_disabled: boolean;
    /** 自定义扩展，json串表示的键值对 */
    extend_info: string;
}
```

#### 当前会议  Room
```typescript
/**
 * 当前会议
 */
export interface Room {
    /**
     * 当前会议id
     * @internal
     */
    meetingId: string;
    /**
     * 当前会议信息
     */
    info: RoomInfo;
    /**
     * 当前会议中用户
     */
    users: Record<string, UserInfo>;
}
```

#### 会议信息
```typescript
export interface MeetingInfo {
    /** 会议ID */
    id: string;
    /** 会议标题 */
    title: string;
    /** 房间号 */
    room_no: string;
    /** 会议限制类型 */
    attend_type: AttendType;
    /** 会议类型 */
    meeting_type: MeetingType;
    /** 会议模式 */
    meeting_mode: MeetingMode;
    /** 是否开启录制 */
    auto_record: boolean
    /** 布局数据 */
    layout_data: LayoutData;
    /** 会议状态 */
    meeting_status: MeetingStatus;
    /** 参会人员用户id */
    conferee: string[];
    /** 会议计划时间 */
    plan_time: number;
    /** 会议时长(秒) */
    plan_dur: number;
    /** 会议开始时间 */
    begin_time: number;
    /** 会议结束时间 */
    end_time: number;
    /** 会议创建时间 */
    created_at: number;
    /** 会议创建者 */
    creator: string;
    /** 会议主持人 */
}
```

#### 分页参数
```typescript
export interface PageParam {
    /** 当前页码 */
    page: number;
    /** 每页条数 */
    'per-page': number;
}
```

#### 分页数据
```typescript
export interface MetaRes {
    totalCount: number;
    pageCount: number;
    currentPage: number;
    perPage: number;
}
```

#### 参会记录
```typescript
export interface ParticipantInfo {
    /** id */
    id: string;
    /** 参会成员用户id */
    user_id: string;
    /** 参会成员昵称 */
    nickname: string;
    /** 进入时间 */
    enter_at: number;
    /** 离开时间 */
    exit_at: number;
}
```

#### 入会设备类型
```typescript
export enum AgentType {
    /** SIP */
    SIP = 2,
    /** H323 */
    H323 = 3,
    /** GB28181 */
    GB28181 = 4,
    /** RTSP拉流 */
    RTSP = 5,
    /** RTMP拉流 */
    RTMP = 6,
    /** 文件播放 */
    FilePlay = 7,
    /** 腾讯会议 */
    TencentMeet = 8,
    /** AI */
    AI = 9,
}
```

#### 入会设备状态
```typescript
export enum AgentStatus {
    /** 空闲 */
    Idle = 1,
    /** 忙碌 */
    Busy = 2,
    /** 离线 */
    Offline = 3,
}
```

#### 入会设备信息
```typescript
export interface AgentInfo {
    /** 设备ID */
    id: string;
    /** 设备名称 */
    name: string;
    /** 设备类型 */
    type: AgentType;
    /** 设备状态 */
    status: AgentStatus;
    /** 设备标识 */
    contact: string;
    /** 备注 */
    remark: string;
}
```

#### 布局类型
```typescript
export enum LayoutType {
    /** 自动布局 */
    Auto = 'auto',
    /** 全屏 */
    Full = 'full',
    /** 二等分 */
    Grids2 = 'grids_2', 
    /** 品字形 */
    Grids3 = 'grids_3',
    /** 四宫格 */
    Grids4 = 'grids_4',
    /** 五宫格 */
    Grids5 = 'grids_5',
    /** 六宫格 */
    Grids6 = 'grids_6',
    /** 八宫格 */
    Grids8 = 'grids_8',
    /** 九宫格 */
    Grids9 = 'grids_9',
    /** 十宫格 */
    Grids10 = 'grids_10',
    /** 十二宫格 */
    Grids12 = 'grids_12',
    /** 十六宫格 */
    Grids16 = 'grids_16',
    /** 二十宫格 */
    Grids20 = 'grids_20',
    /** 二十五宫格 */
    Grids25 = 'grids_25',
    /** 右侧小窗口 */
    Right4 = 'right_4',
    /** 顶部小窗口 */
    Top4 = 'top_4',
    /** 下L型布局 */
    Br7 = 'br_7',
    /** 上L型布局 */
    Tl7 = 'tl_7',
    /** 左右布局 */
    Tb8 = 'tb_8',
}
```

#### 布局相关
```typescript

/** 水印 */
export interface Watermark {
    /** 类型 0默认, 1无, 2单排, 3多排 */
	type: number;
    /** 指定内容, 空表示自动(会议标题) */
	text: string;
    /** 字体大小, 0表示默认 */
	size?: number;
    /** 字体颜色, 空表示默认 */
	color?: string;
    /** 轮廓颜色, 空表示默认值 */
	ol_color?: string;
    /** 轮廓线宽, 0表示默认值 */
	ol_width?: number;
}

/** 标签 */
export interface Tag {
    /** 字母或组合: L左, R右, T上, B下 */
	type: string;
    /** 指定内容, 空表示自动(会中名称) */
	text: string;
    /** 字体大小, 0表示默认 */
	size?: number;
    /** 字体颜色, 空表示默认 */
	color?: string;
    /** 背景颜色, 空表示默认 */
	bg_color?: string;
}

/** 宫格 */
export interface Cell {
    /** 格子序号, 排序规则按HTML中标签的顺序 */
	idx: number;
    /** 是否优先绑定会议内的共享流 */
	bind_share: boolean;
    /** 标签 */
	tag: Tag;
}

/** 逻辑块 */
export interface DivList {
    /** 宫格列表, 空表示剩余格子共用此处的用户 */
	cell: Cell[];
    /** 用户ID列表, 空表示大轮询在线剩余用户, 多个表示小轮询 */
	uids: string[];
}

/** 布局数据 */
export interface LayoutData {
    /** 布局类型 */
	layout: LayoutType;
    /** 轮询间隔 0表示不轮询 */
	polling_dur?: number;
    /** 水印 */
	watermark?: Watermark;
    /** 标签 */
	tag?: Tag;
    /** 逻辑块列表 */
	div_list?: DivList[];
}


```

#### mcu录制相关
```typescript
/**
 * 开启录制请求参数
 */
export interface McuStartReq {
    /** 1录像模式 2合流模式 3录像+合流 */
	task_type: McuTaskType;
    /** 录制文件标题 */
	title: string;
    /** 操作人 */
	user_name: string;
    /** 布局  */
	layout_data: LayoutData;
}

/**
 * 录制配置信息
 */
export interface McuRecordConfig {
    /** app_id */
	app_id: string;
    /** 布局类型 */
	layout: LayoutType;
    /** 水印类型 */
	watermark_type: number;
    /** 水印文本 */
	watermark_text: string;
    /** 标签类型 */
	window_tag_type: string;
    /** 标签文本 */
	window_tag_text: string;
    /** 创建时间 */
	created_at: number;
    /** 更新时间 */
	updated_at: number;
}

/**
 * 录制文件(一次录制任务的一个分片)
 *
 * 一次录制会产出多个文件：按时长切段、或中断后续录都会多出一片，按 seq 排序即播放顺序。
 */
export interface McuRecordFile {
    /** 录制文件ID，单独取播放地址/删除时用 */
	record_id: string;
    /** 所属录制任务ID */
	task_id: string;
    /** 会议id */
	channel: string;
    /** 分片序号，从1开始 */
	seq: number;
    /** 文件大小(字节) */
	vod_size: number;
    /** 本片时长(秒) */
	duration: number;
    /** 本片开始时间(秒级时间戳) */
	began_at: number;
    /** 本片结束时间(秒级时间戳) */
	ended_at: number;
    /** 相对任务开始的偏移(毫秒)，做多片连播的进度轴用 */
	offset_ms: number;
    /** 分片原因 0未知 1按时长切段 2中断后续录(与上一片间有空洞) */
	reason: number;
    /** 预签名播放地址，有效期2小时 */
	addr: string;
    /** 记录创建时间(秒级时间戳) */
	created_at: number;
}

/**
 * 录制任务详情
 */
export interface McuRecordDetail {
    /** 任务id */
	task_id: string;
    /** 操作人ID */
	op_uid: string;
    /** 操作人 */
	op_name: string;
    /** 会议id */
	channel: string;
    /** 会议标题 */
	title: string;
    /** 房间号 */
	room_no: string;
    /** 任务状态 */
	task_status: McuTaskStatus;
    /** 任务状态描述 */
	err_desc: string;
    /** 录制开始时间(秒级时间戳)，0表示底层任务还没跑起来 */
	began_at: number;
    /** 录制结束时间(秒级时间戳)，0表示未结束 */
	ended_at: number;
    /** 录制文件数 */
	record_count: number;
    /** 全部录制文件的总时长(秒) */
	total_duration: number;
    /** 全部录制文件的总字节 */
	total_size: number;
    /** 录制文件列表 */
	records: McuRecordFile[] | null;
    /**
     * 录制开始时间(秒级时间戳)
     * @deprecated 两级模型改造前的老字段，与 began_at 等价，请改用 began_at
     */
	mcu_at: number;
    /**
     * 录制总时长(秒)
     * @deprecated 两级模型改造前的老字段，与 total_duration 等价，请改用 total_duration
     */
	mcu_dur: number;
    /** 标签 */
	tags: string;
    /** 创建时间 */
	created_at: number;
    /** 更新时间 */
	updated_at: number;
    /** 服务器当前时间(秒)，用于前端本地时间不准时辅助计算录制时长 */
	now: number;
}

/**
 * mcu任务类型
 */

export enum McuTaskType {
    /** 录像模式 */
    Record = 1,
    /** 合流模式 */
    Mix = 2,
    /** 录像+合流 */
    MixAndRecord = 3,
}

/**
 * mcu任务状态，取值与服务端 task_status 一致
 * 注意：0.2.0 及以前的定义有误（Exception = 2、Normal = 3），0.3.0 起成员名不变、值已改正；
 * 直接写数字 2 / 3 判断的代码需自查
 */
export enum McuTaskStatus {
    /** 待开始（临时过渡状态，已下发指令、底层任务尚未跑起来） */
    WaitStart = 0,
    /** 进行中 */
    Running = 1,
    /** 待结束（临时过渡状态，已下发停止指令、底层尚未确认结束） */
    WaitEnd = 2,
    /** 异常结束，原因见 err_desc */
    Exception = 3,
    /** 正常结束 */
    Normal = 4,
}
```

