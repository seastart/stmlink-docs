---
title: "Types"
description: "Complete type and struct definitions of the SMeeting Web SDK: enums (TrackDesc, HandupType, Role, ShareType, DisconnectReason, and more), request parameters for creating and entering meetings, RoomInfo and UserInfo, device, layout, and MCU recording types."
---

#### Track description TrackDesc
```typescript
/** Track description */
export enum TrackDesc {
    /** Mic track */
    MIC = 'mic',
    /** Camera high stream */
    CAMERAL_BIG = 'camera_big',
    /** Camera low stream */
    CAMERAL_SMALL = 'camera_small',
    /** Screen sharing track */
    SCREEN = 'screen',
}
```

#### Raise-hand type HandupType
```typescript
/**
 * Raise-hand type
 */
export enum HandupType {
    /**
     * Request to turn on the mic
     */
    Mic = 1,
    /**
     * Request to turn on the camera
     */
    Camera = 2,
    /**
     * Request to chat
     */
    Chat = 3
}
```

#### User raise-hand step  UserHandupStep
```typescript
/**
 * User raise-hand step
 */
export enum UserHandupStep {
    /**
     * Raise a hand
     */
    Request = 1,
    /**
     * Lower a hand
     */
    Cancel = 2,
    /**
     * Confirm turning on the device
     */
    ConfirmOpen = 3,
    /**
     * Decline turning on the device
     */
    RejectOpen = 4,
}
```

#### Camera state CameraState
```typescript
/**
 * Camera state
 */
export enum CameraState {
    /**
     * On
     */
    On = 1,
    /**
     * Off
     */
    Off = 2,
}
```

#### Mic state MicState
```typescript
/**
 * Mic state
 */
export enum MicState {
    /**
     * On
     */
    On = 1,
    /**
     * Off
     */
    Off = 2,
}

```

#### Room sharing type ShareType 
```typescript
/**
 * Room sharing type
 */
export enum ShareType {
    /**
     * Screen sharing
     */
    Screen = 1,
    /**
     * Whiteboard
     */
    WhiteBoard = 2,
}

```

#### Sharing status ShareState
```typescript
export type ShareState = 0 | ShareType;
```

#### Role type Role
```typescript
/**
 * Role type
 */
export enum Role {
    /**
     * Regular member
     */
    Member = 0,
    /**
     * Host
     */
    Host = 1,
    /**
     * Co-host
     */
    CoHost = 2,
}
```

#### Chat message type ChatMsgType
```typescript
/**
 * Chat message type
 */
export enum ChatMsgType {
    /**
     * Text
     */
    Text = 1,
    /**
     * File
     */
    File = 2,
    /**
     * Image
     */
    Pic = 3,
    /**
     * Voice
     */
    Sound = 4,
}
```

#### Reason a user exited the room DisconnectReason
```typescript
/**
 * Reason a user exited the room
 */
export declare enum DisconnectReason {
	/** Error */
	Error = -1,
	/** Exited voluntarily */
	Self = 1,
	/** Removed */
	Kicked = 2,
	/** Replaced by the same user entering again */
	Replace = 3,
	/** Exited due to heartbeat timeout */
	Timeout = 4,
	/** Exited because the room was destroyed */
	Destroy = 5
}
```

#### Meeting type MeetingType
```typescript
/**
 * Meeting type
 */
export enum MeetingType {
    /** Instant meeting */
    Instant = 1,
    /** Scheduled meeting */
    Appointment = 2
}
```

#### Mute-on-entry policy EntryMutePolicy
```typescript
/**
 * Mute-on-entry policy
 */
export enum EntryMutePolicy {
    /** Mute on entry (everyone is muted by default when entering) */
    Silent = 1,
    /** No restriction; follows the client's initial audio state */
    UnRestrict = 2,
    /** Mute after 6 (members entering after the 6th are muted) */
    SilentAfter6 = 3,
}
```

#### Token info for SDK login MeetingToken
```typescript
/**
 * Token info for SDK login
 */
export interface MeetingToken {
    /** App ID */
    app_id: string;
    /** User ID */
    user_id: string;
    /** Expiration time */
    exp_at: number;
    /** Client key */
    client_key: string;
    /** SDK API prefix */
    client_api: string;
}
```

#### User type UserType
```typescript
/**
 * User type
 */
export enum UserType {
    /** Regular user */
    Normal = 1,
    /** SIP user */
    SIP = 2,
    /** H.323 user */
    H323 = 3,
}
```

#### SDK constructor parameters SdkInitParams
```typescript
/**
 * SDK constructor parameters
 */
export interface SdkInitParams {
    /** Log level */
    logLevel?: LogLevel;
    /** Log target */
    logTarget?: LogTarget;
}
```

#### Create/update meeting parameters MeetingCreateReq
```typescript
/**
 * Create/update meeting parameters
 */
export interface MeetingCreateReq {
    /** Room number */
    room_no?: string;
    /** Meeting title */
    title: string;
    /** Meeting description */
    content?: string;
    /** Entry restriction type (unrestricted by default) */
    attend_type?: AttendType,
    /** User IDs of the invitees */
    conferee?: string[];
    /** Meeting password */
    password?: string;
    /** Meeting type 1: instant meeting (default) 2: scheduled meeting */
    meeting_type?: MeetingType;
    /** Start time (timestamp in seconds) */
    plan_time?: number;
    /** Meeting duration (in minutes) */
    plan_dur?: number;
    /** Mute-on-entry option */
    entry_mute_policy?: EntryMutePolicy;
    /** Whether the watermark is turned off */
    watermark_disabled?: boolean;
    /** Whether screenshots are disabled */
    screenshot_disabled?: boolean;
    /** Chat disabled for the room */
    chat_disabled?: boolean;
    /** Extension field */
    extend_info?: string;
    /** Meeting mode (normal mode by default) */
    meeting_mode: MeetingMode,
    /** Layout */
    layout_data?: LayoutData
    /** Whether recording is turned on */
    auto_record?: boolean
}
```

#### Enter meeting parameters MeetingEnterReq
```typescript
/**
 * Enter meeting parameters
 */
export interface MeetingEnterReq {
    /** Room number */
    room_no: string;
    /** Meeting password */
    password?: string;
    /** In-meeting display name */
    nickname: string;
    /** In-meeting avatar */
    avatar?: string;
    /** Extension field */
    extend_info?: string;
}
```

#### Room info
```typescript
/**
 * Room info
 */
export interface RoomInfo {
    /** Meeting ID */
    id: string;
    /** Room number */
    room_no: string;
    /** Meeting title */
    title: string;
    /** Meeting description */
    content: string;
    /** Meeting type, 1 instant meeting, 2 scheduled meeting */
    meeting_type: MeetingType;
    /** Start time, Unix timestamp (seconds) */
    begin_time: number;
    /** End time, Unix timestamp (seconds) */
    end_time: number;
    /** Mute-on-entry option, 1 muted by default on entry, 2 follow the client's initial audio state, 3 muted on entry after 6 members */
    entry_mute_policy: EntryMutePolicy;
    /** Watermark-off setting, false unrestricted, true watermark off */
    watermark_disabled: boolean;
    /** Screenshot-disabled setting, false unrestricted, true screenshots disabled */
    screenshot_disabled: boolean;
    /** Chat-disabled setting, false unrestricted, true chat disabled */
    chat_disabled: boolean;
    /** Mute setting, false unrestricted, true muted */
    mic_disabled: boolean;
    /** Camera-off setting, false unrestricted, true camera off */
    camera_disabled: boolean;
    /** Prevent members from unmuting themselves, false unrestricted, true prevented */
    self_unmute_mic_disabled: boolean;
    /** Prevent members from turning their own camera back on, false unrestricted, true prevented */
    self_unmute_camera_disabled: boolean;
    /** Room locked state, false unrestricted, true locked */
    locked: boolean;
    /** Sharing status, 0 none, 1 screen, 2 whiteboard */
    share_state: ShareState;
    /** Sharer ID */
    share_uid: string;
    /** Creator ID */
    creator: string;
    /** Host ID */
    host_uid: string;
    /** List of co-host IDs */
    co_hosts: string[];
    /** Custom extension, key-value pairs as a JSON string */
    extend_info: string;
}
```

#### User info UserInfo
```typescript
/**
 * User info
 */
export interface UserInfo {
    /** User ID */
    uid: string;
    /** In-meeting display name */
    name: string;
    /** Device type */
    device_type: DeviceType;
    /** Device ID */
    device_id: string;
    /** Client SDK version */
    version: string;
    /** Entry time */
    join_at: number;

    /** In-meeting role, 0 regular, 1 host, 2 co-host */
    role: Role;
    /** In-meeting avatar */
    avatar: string;
    /** Mic state, 1 on, 2 off */
    mic_state: MicState;
    /** Camera state, 1 on, 2 off */
    camera_state: CameraState;
    /** Sharing status, 0 none, 1 screen, 2 whiteboard */
    share_state: ShareState;
    /** Whether removed from the meeting, false normal, true removed */
    is_kickout: boolean;
    /** Chat-disabled setting, false unrestricted, true chat disabled */
    chat_disabled: boolean;
    /** Custom extension, key-value pairs as a JSON string */
    extend_info: string;
}
```

#### Current meeting  Room
```typescript
/**
 * Current meeting
 */
export interface Room {
    /**
     * Current meeting ID
     * @internal
     */
    meetingId: string;
    /**
     * Current meeting info
     */
    info: RoomInfo;
    /**
     * Users in the current meeting
     */
    users: Record<string, UserInfo>;
}
```

#### Meeting info
```typescript
export interface MeetingInfo {
    /** Meeting ID */
    id: string;
    /** Meeting title */
    title: string;
    /** Room number */
    room_no: string;
    /** Entry restriction type */
    attend_type: AttendType;
    /** Meeting type */
    meeting_type: MeetingType;
    /** Meeting mode */
    meeting_mode: MeetingMode;
    /** Whether recording is turned on */
    auto_record: boolean
    /** Layout data */
    layout_data: LayoutData;
    /** Meeting status */
    meeting_status: MeetingStatus;
    /** User IDs of the invitees */
    conferee: string[];
    /** Planned meeting time */
    plan_time: number;
    /** Meeting duration (seconds) */
    plan_dur: number;
    /** Meeting start time */
    begin_time: number;
    /** Meeting end time */
    end_time: number;
    /** Meeting creation time */
    created_at: number;
    /** Meeting creator */
    creator: string;
    /** Meeting host */
}
```

#### Pagination parameters
```typescript
export interface PageParam {
    /** Current page number */
    page: number;
    /** Items per page */
    'per-page': number;
}
```

#### Pagination data
```typescript
export interface MetaRes {
    totalCount: number;
    pageCount: number;
    currentPage: number;
    perPage: number;
}
```

#### Attendance record
```typescript
export interface ParticipantInfo {
    /** id */
    id: string;
    /** Member's user ID */
    user_id: string;
    /** Member's display name */
    nickname: string;
    /** Entry time */
    enter_at: number;
    /** Exit time */
    exit_at: number;
}
```

#### Device types for entering meetings
```typescript
export enum AgentType {
    /** SIP */
    SIP = 2,
    /** H.323 */
    H323 = 3,
    /** GB28181 */
    GB28181 = 4,
    /** RTSP pull */
    RTSP = 5,
    /** RTMP pull */
    RTMP = 6,
    /** File playback */
    FilePlay = 7,
    /** Tencent Meeting */
    TencentMeet = 8,
    /** AI */
    AI = 9,
}
```

#### Device status for entering meetings
```typescript
export enum AgentStatus {
    /** Idle */
    Idle = 1,
    /** Busy */
    Busy = 2,
    /** Offline */
    Offline = 3,
}
```

#### Device info for entering meetings
```typescript
export interface AgentInfo {
    /** Device ID */
    id: string;
    /** Device name */
    name: string;
    /** Device type */
    type: AgentType;
    /** Device status */
    status: AgentStatus;
    /** Device identifier */
    contact: string;
    /** Remarks */
    remark: string;
}
```

#### Layout types
```typescript
export enum LayoutType {
    /** Automatic layout */
    Auto = 'auto',
    /** Full screen */
    Full = 'full',
    /** Split in two */
    Grids2 = 'grids_2', 
    /** Pyramid (1 top, 2 bottom) */
    Grids3 = 'grids_3',
    /** 4-tile grid */
    Grids4 = 'grids_4',
    /** 5-tile grid */
    Grids5 = 'grids_5',
    /** 6-tile grid */
    Grids6 = 'grids_6',
    /** 8-tile grid */
    Grids8 = 'grids_8',
    /** 9-tile grid */
    Grids9 = 'grids_9',
    /** 10-tile grid */
    Grids10 = 'grids_10',
    /** 12-tile grid */
    Grids12 = 'grids_12',
    /** 16-tile grid */
    Grids16 = 'grids_16',
    /** 20-tile grid */
    Grids20 = 'grids_20',
    /** 25-tile grid */
    Grids25 = 'grids_25',
    /** Small windows on the right */
    Right4 = 'right_4',
    /** Small windows on top */
    Top4 = 'top_4',
    /** Bottom L-shaped layout */
    Br7 = 'br_7',
    /** Top L-shaped layout */
    Tl7 = 'tl_7',
    /** Left-right layout */
    Tb8 = 'tb_8',
}
```

#### Layout-related types
```typescript

/** Watermark */
export interface Watermark {
    /** Type 0 default, 1 none, 2 single row, 3 multiple rows */
	type: number;
    /** Specified content; empty means automatic (meeting title) */
	text: string;
    /** Font size; 0 means default */
	size?: number;
    /** Font color; empty means default */
	color?: string;
    /** Outline color; empty means default */
	ol_color?: string;
    /** Outline width; 0 means default */
	ol_width?: number;
}

/** Label */
export interface Tag {
    /** A letter or combination: L left, R right, T top, B bottom */
	type: string;
    /** Specified content; empty means automatic (in-meeting name) */
	text: string;
    /** Font size; 0 means default */
	size?: number;
    /** Font color; empty means default */
	color?: string;
    /** Background color; empty means default */
	bg_color?: string;
}

/** Grid cell */
export interface Cell {
    /** Cell index, ordered by the order of the tags in the HTML */
	idx: number;
    /** Whether to preferentially bind the meeting's shared stream */
	bind_share: boolean;
    /** Label */
	tag: Tag;
}

/** Logical block */
export interface DivList {
    /** List of cells; empty means the remaining cells share the users here */
	cell: Cell[];
    /** List of user IDs; empty means rotating through all remaining online users, multiple means rotating among these users */
	uids: string[];
}

/** Layout data */
export interface LayoutData {
    /** Layout type */
	layout: LayoutType;
    /** Rotation interval; 0 means no rotation */
	polling_dur?: number;
    /** Watermark */
	watermark?: Watermark;
    /** Label */
	tag?: Tag;
    /** List of logical blocks */
	div_list?: DivList[];
}


```

#### MCU recording types
```typescript
/**
 * Start recording request parameters
 */
export interface McuStartReq {
    /** 1 video recording mode 2 stream mixing mode 3 video recording + stream mixing */
	task_type: McuTaskType;
    /** Recording file title */
	title: string;
    /** Operator */
	user_name: string;
    /** Layout  */
	layout_data: LayoutData;
}

/**
 * Recording configuration
 */
export interface McuRecordConfig {
    /** app_id */
	app_id: string;
    /** Layout type */
	layout: LayoutType;
    /** Watermark type */
	watermark_type: number;
    /** Watermark text */
	watermark_text: string;
    /** Label type */
	window_tag_type: string;
    /** Label text */
	window_tag_text: string;
    /** Creation time */
	created_at: number;
    /** Update time */
	updated_at: number;
}

/**
 * Recording file (one segment of a recording task)
 *
 * A single recording produces multiple files: splitting by duration, or resuming after an interruption, each adds a segment; sorting by seq gives the playback order.
 */
export interface McuRecordFile {
    /** Recording file ID, used to get the playback URL or delete the file individually */
	record_id: string;
    /** ID of the recording task it belongs to */
	task_id: string;
    /** Meeting ID */
	channel: string;
    /** Segment number, starting at 1 */
	seq: number;
    /** File size (bytes) */
	vod_size: number;
    /** Duration of this segment (seconds) */
	duration: number;
    /** Start time of this segment (timestamp in seconds) */
	began_at: number;
    /** End time of this segment (timestamp in seconds) */
	ended_at: number;
    /** Offset from the task start (milliseconds), used for the progress bar in multi-segment playback */
	offset_ms: number;
    /** Segment reason 0 unknown 1 split by duration 2 resumed after an interruption (gap from the previous segment) */
	reason: number;
    /** Pre-signed playback URL, valid for 2 hours */
	addr: string;
    /** Record creation time (timestamp in seconds) */
	created_at: number;
}

/**
 * Recording task details
 */
export interface McuRecordDetail {
    /** Task ID */
	task_id: string;
    /** Operator ID */
	op_uid: string;
    /** Operator */
	op_name: string;
    /** Meeting ID */
	channel: string;
    /** Meeting title */
	title: string;
    /** Room number */
	room_no: string;
    /** Task status */
	task_status: McuTaskStatus;
    /** Task status description */
	err_desc: string;
    /** Recording start time (timestamp in seconds); 0 means the underlying task hasn't started yet */
	began_at: number;
    /** Recording end time (timestamp in seconds); 0 means not ended */
	ended_at: number;
    /** Number of recording files */
	record_count: number;
    /** Total duration of all recording files (seconds) */
	total_duration: number;
    /** Total bytes of all recording files */
	total_size: number;
    /** List of recording files */
	records: McuRecordFile[] | null;
    /**
     * Recording start time (timestamp in seconds)
     * @deprecated Legacy field from before the two-level model; equivalent to began_at. Use began_at instead
     */
	mcu_at: number;
    /**
     * Total recording duration (seconds)
     * @deprecated Legacy field from before the two-level model; equivalent to total_duration. Use total_duration instead
     */
	mcu_dur: number;
    /** Tags */
	tags: string;
    /** Creation time */
	created_at: number;
    /** Update time */
	updated_at: number;
    /** Current server time (seconds), used to help calculate recording duration when the frontend's local clock is inaccurate */
	now: number;
}

/**
 * MCU task type
 */

export enum McuTaskType {
    /** Video recording mode */
    Record = 1,
    /** Stream mixing mode */
    Mix = 2,
    /** Video recording + stream mixing */
    MixAndRecord = 3,
}

/**
 * MCU task status
 */
export enum McuTaskStatus {
    /** In progress */
    Running = 1,
    /** Ended abnormally */
    Exception = 2,
    /** Ended normally */
    Normal = 3
}
```

