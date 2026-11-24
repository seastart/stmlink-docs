---
title: "事件参考"
description: "Web SMeeting 会议 SDK 全量事件列表与触发时机说明"
---

所有事件都可通过`smeeting.onNotifyRoomEvent`来监听

```typescript
// 回调事件响应
smeeting.onNotifyRoomEvent = (evt: RoomEvent) => {
  console.log('收到房间事件', evt);
  switch (evt.type) {
      // ...
  }
})
```

RoomEvent 定义如下：

```typescript
/** 房间事件通知 */
declare class RoomEvent {
    /** 事件类型 */
    type: CommonRoomEventType;
    /** 事件携带的数据 */
    data?: any;
}
```

CommonRoomEventType及对应`data`定义如下：

```typescript
    /** 开始断线自动重连，无data */
    static readonly RECONNECTING = 'reconnecting';
    /** 重连成功，断线重连成功后会触发，无data */
    static readonly RECONNECTED = 'reconnected';
    /** 自己被强制退出会议（被踢、被顶号、心跳超时、会议结束等），对应data为 DisconnectEventData。回调返回后 SDK 即清理会议状态，可直接 enterRoom 重新入会（v0.3.3 起） */
    static readonly DISCONNECTED = 'disconnected';

    /** 其他用户进入会议，对应data为 UserInfo */
    static readonly USER_ENTER = 'user_enter';
    /** 其他用户退出会议，对应data为 UserExitEventData */
    static readonly USER_EXIT = 'user_exit';
    /** 用户摄像头状态变化(自己/他人主动改变或被主持人改变)，对应data为 UserCameraStateChangeEventData */
    static readonly USER_CAMREA_STATE_CHANGED = "user_camera_state_changed";
    /** 用户额外屏幕共享流（EXTRA_SCREEN）开/关状态变化，对应data为 UserExtraScreenChangeEventData。用于多人同时推 EXTRA_SCREEN 的场景，接收侧据此决定订阅或释放 */
    static readonly USER_EXTRA_SCREEN_CHANGED = "user_extra_screen_changed";
    /** 用户麦克风状态变化(自己/他人主动改变或被主持人改变)，对应data为 UserMicStateChangeEventData */
    static readonly USER_MIC_STATE_CHANGED = "user_mic_state_changed";
    /** 用户昵称变化(自己/他人主动改变或被主持人改变)，对应data为 UserNameChangeEventData */
    static readonly USER_NAME_CHANGED = "user_name_changed";
    /** 用户角色变化，对应data为 UserRoleChangeEventData */
    static readonly USER_ROLE_CHANGED = 'user_role_changed';
    /** 用户聊天禁用状态变化，对应data为 UserChatDisabledChangeEventData */
    static readonly USER_CHAT_DISABLED_CHANGED = 'user_chat_disabled_changed';
    /** 用户举手相关事件(管理员才会收到)，对应data为 UserHandupEventData */
    static readonly USER_HANDUP = 'user_handup';

    /** 房间摄像头禁用状态改变，对应data为 RoomCameraStateChangeEventData */
    static readonly ROOM_CAMREA_STATE_CHANGED = 'room_camera_state_changed';
    /** 房间麦克风禁用状态改变，对应data为 RoomMicStateChangeEventData */
    static readonly ROOM_MIC_STATE_CHANGED = 'room_mic_state_changed';
    /** 房间共享禁用状态改变，对应data为 RoomShareStateChangeEventData */
    static readonly ROOM_SHARE_STATE_CHANGED = 'room_share_state_changed';
    /** 房间聊天禁用状态改变，对应data为 RoomChatDisabledChangeEventData */
    static readonly ROOM_CHAT_DISABLED_CHANGED = 'room_chat_disabled_changed';
    /** 房间截屏禁用状态改变，对应data为 RoomScreenshotDisabledChangeEventData */
    static readonly ROOM_SCREENSHOT_DISABLED_CHANGED = 'room_screenshot_disabled_changed';
    /** 房间水印禁用状态改变，对应data为 RoomWatermarkDisabledChangeEventData */
    static readonly ROOM_WATERMARK_DISABLED_CHANGED = 'room_watermark_disabled_changed';
    /** 房间锁定状态改变，对应data为 RoomLockedChangeEventData */
    static readonly ROOM_LOCKED_CHANGED = 'room_locked_changed';
    /** 房间共享开始，对应data为 RoomShareStartEventData */
    static readonly ROOM_SHARE_START = 'room_share_start';
    /** 房间共享结束，对应data为 RoomShareStopEventData */
    static readonly ROOM_SHARE_STOP = 'room_share_stop';
    /** 房间聊天消息，对应data为 RoomChatMsgEventData */
    static readonly ROOM_CHAT_MSG = 'room_chat_msg';
    /** 房间自定义消息，对应data为 RoomCustomMsgEventData */
    static readonly ROOM_CUSTOM_MSG = 'room_custom_msg';
    /** 房间mcu任务，对应data为 RoomMcuTaskEventData */
    static readonly ROOM_MCU_TASK = 'room_mcu_task';
    /** 房间加入失败事件，对应data为 RoomJoinFailedEventData */
    static readonly ROOM_JOIN_FAILED = 'room_join_failed';
    /** 会议转写（字幕）开关状态改变，对应data为 RoomAsrStateChangeEventData（0.3.6 起） */
    static readonly ROOM_ASR_STATE_CHANGED = 'room_asr_state_changed';
    /** 转写结果（字幕原文），对应data为 AsrResultEventData（0.3.6 起） */
    static readonly ASR_RESULT = 'asr_result';
    /** 转写译文（实时翻译），对应data为 AsrTranslationEventData（0.3.6 起） */
    static readonly ASR_TRANSLATION = 'asr_translation';
    /** 会议纪要生成完成/失败，对应data为 AiSummaryReadyEventData（0.3.6 起） */
    static readonly AI_SUMMARY_READY = 'ai_summary_ready';

    /** 会中签到活动，对应data为 SignInActivityEventData */
    static readonly SIGN_IN_ACTIVITY = 'sign_in_activity';
    /** 会中签到活动手动/自动结束，对应data为 SignInFinishEventData */
    static readonly SIGN_IN_FINISH = 'sign_in_finish';
    /** 会中用户进入等候室，对应data为 UserEnterWaitingRoomEventData */
    static readonly USER_ENTER_WAITING_ROOM = 'user_enter_waiting_room';
    /** 会中用户离开等候室，对应data为 UserExitWaitingRoomEventData */
    static readonly USER_EXIT_WAITING_ROOM = 'user_exit_waiting_room';
    /** 等候室禁用状态改变，对应data为 AdminUpdateWaitingRoomDisabledEventData */
    static readonly ADMIN_UPDATE_WAITING_ROOM_DISABLED = 'admin_update_waiting_room_disabled';
    /** 您被主持人移进等候室（私发给该成员），无data */
    static readonly ADMIN_MOVE_IN_WAITING_ROOM = 'admin_move_in_waiting_room';
    /** 主持人开始分组讨论，对应data为 AdminStartSubMeetingEventData */
    static readonly ADMIN_START_SUB_MEETING = 'admin_start_sub_meeting';
    /** 主持人结束分组讨论，对应data为 AdminStopSubMeetingEventData */
    static readonly ADMIN_STOP_SUB_MEETING = 'admin_stop_sub_meeting';
    /** 在小组之间或小组与主会场之间移动用户，对应data为 AdminMoveSubMeetingUserEventData */
    static readonly ADMIN_MOVE_SUB_MEETING_USER = 'admin_move_sub_meeting_user';
    /** 会中点名，对应data为 RollCallNamedEventData */
    static readonly ROLL_CALL_NAMED = 'roll_call_named';

    /** 主持人处理您的举手申请，对应data为 AdminConfirmHandupEventData */
    static readonly ADMIN_CONFIRM_HANDUP = 'admin_confirm_handup';
    /** 主持人请求您开麦，对应data为 AdminRequestOpenMicEventData */
    static readonly ADMIN_REQUEST_OPEN_MIC = 'admin_request_open_mic';
    /** 主持人请求您开摄像头，对应data为 AdminRequestOpenCameraEventData */
    static readonly ADMIN_REQUEST_OPEN_CAMERA = 'admin_request_open_camera';
    /** 主持人请求您共享屏幕，对应data为 AdminRequestOpenShareEventData（op_uid=发起的主持人）。
     *  同意时调 requestShare(shareType, preset, audioPreset, container, true, data.op_uid)；不同意忽略即可（0.3.7 起） */
    static readonly ADMIN_REQUEST_OPEN_SHARE = 'admin_request_open_share';

```

RoomEventType及对应`data`定义如下：

```typescript
/** 房间事件类型 */
export class RoomEventType extends CommonRoomEventType {
     /** 设备插入 对应data为 MediaDeviceInfo */
     static readonly DEVICE_ADD = 'device_add';
     /** 设备拔出 对应data为 MediaDeviceInfo */
     static readonly DEVICE_REMOVE = 'device_remove';
     /** 流轨道停止，对应data为BaseTrack */
     static readonly TRACK_ENDED = 'track_ended';
     /** 流轨道没有数据 */
     static readonly TRACK_MUTED = 'track_muted';
     /** 流轨道恢复数据 */
     static readonly TRACK_UNMUTED = 'track_unmuted';
     /** 活跃说话人列表变化，对应data为 ActiveSpeakersEventData（全量快照，按 level 降序）。仅 SeaStart SFU 引擎触发 */
     static readonly ACTIVE_SPEAKERS_CHANGED = 'active_speakers_changed';
}

```

## 房间事件的 data 定义

下面按用途分组列出 `CommonRoomEventType` / `RoomEventType` 各事件 `data` 的类型。`UserInfo`、`ShareType`、`CameraState`、`MicState`、`Role`、`HandupType`、`UserHandupStep`、`ChatMsgType`、`McuTaskType`、`McuTaskStatus`、`DisconnectReason` 等见 [数据类型](/zh/meeting/web/types)。

### 断线与离会

```typescript
/** DISCONNECTED：自己被强制退出会议 */
export interface DisconnectEventData {
    /** 离开原因 */
    reason: DisconnectReason;
    /** 错误 */
    error?: any;
}

/** USER_EXIT：其他用户退出会议 */
export interface UserExitEventData {
    /** 用户id */
    uid: string;
    /** 离开原因 */
    reason: DisconnectReason;
}

/** ROOM_JOIN_FAILED：房间加入失败 */
export interface RoomJoinFailedEventData {
    /** 用户id */
    uid: string;
    /** 用户昵称 */
    name: string;
    /** 错误描述 */
    err_desc: string;
    /** 失败类型 */
    failed_type: string;
}
```

### 成员状态

```typescript
/** USER_CAMREA_STATE_CHANGED：用户摄像头状态变化 */
export interface UserCameraStateChangeEventData {
    /** 用户 */
    uid: string;
    /** 摄像头状态 */
    camera_state: CameraState;
    /** 是否管理员操作 */
    by_admin: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** USER_EXTRA_SCREEN_CHANGED：用户额外屏幕共享流（EXTRA_SCREEN）开/关变化 */
export interface UserExtraScreenChangeEventData {
    /** 用户 */
    uid: string;
    /** 是否处于推流中 */
    active: boolean;
}

/** USER_MIC_STATE_CHANGED：用户麦克风状态变化 */
export interface UserMicStateChangeEventData {
    /** 用户 */
    uid: string;
    /** 麦克风状态 */
    mic_state: MicState;
    /** 是否管理员操作 */
    by_admin: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** USER_NAME_CHANGED：用户昵称变化 */
export interface UserNameChangeEventData {
    /** 用户 */
    uid: string;
    /** 昵称 */
    nickname: string;
    /** 是否管理员操作 */
    by_admin: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** USER_ROLE_CHANGED：用户角色变化 */
export interface UserRoleChangeEventData {
    /** 用户 */
    uid: string;
    /** 角色 */
    role: Role;
    /** 操作者用户id */
    op_uid?: string;
}

/** USER_CHAT_DISABLED_CHANGED：用户聊天禁用状态变化 */
export interface UserChatDisabledChangeEventData {
    /** 用户 */
    uid: string;
    /** 聊天禁用状态 */
    chat_disabled: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** USER_HANDUP：用户举手相关事件（管理员才会收到） */
export interface UserHandupEventData {
    /** 用户 */
    uid: string;
    /** 举手类型 */
    type: HandupType;
    /** 举手步骤 */
    step: UserHandupStep;
}

/** ACTIVE_SPEAKERS_CHANGED：活跃说话人列表变化（全量快照）。仅 SeaStart SFU 引擎触发 */
export interface ActiveSpeakersEventData {
    /** 服务端下发时间戳（unix 毫秒），用于排序/诊断 */
    ts: number;
    /** 当前正在说话的用户列表，按 level 从大到小排序 */
    speakers: ActiveSpeakerInfo[];
}

export interface ActiveSpeakerInfo {
    /** 用户 id */
    uid: string;
    /** 对应的音频轨道 id；同一用户发布多条音频轨道时用它区分 */
    trackId: string;
    /** 当前音量，归一化线性值 0~1（0 为静音，1 对应 0 dBov），已量化到 1/8 档位，可直接映射为音柱宽度；转 dB 用 20 * Math.log10(level) */
    level: number;
}
```

### 会议设置

```typescript
/** ROOM_CAMREA_STATE_CHANGED：房间摄像头禁用状态改变 */
export interface RoomCameraStateChangeEventData {
    /** 房间视频禁用状态 */
    camera_disabled: boolean;
    /** 是否禁止自我解除视频状态 */
    self_unmute_camera_disabled: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** ROOM_MIC_STATE_CHANGED：房间麦克风禁用状态改变 */
export interface RoomMicStateChangeEventData {
    /** 房间麦克风禁用状态 */
    mic_disabled: boolean;
    /** 是否禁止自我解除麦克风状态 */
    self_unmute_mic_disabled: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** ROOM_SHARE_STATE_CHANGED：房间共享禁用状态改变 */
export interface RoomShareStateChangeEventData {
    /** 房间共享禁用状态 */
    share_disabled: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** ROOM_CHAT_DISABLED_CHANGED：房间聊天禁用状态改变 */
export interface RoomChatDisabledChangeEventData {
    /** 房间聊天禁用状态 */
    chat_disabled: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** ROOM_SCREENSHOT_DISABLED_CHANGED：房间截屏禁用状态改变 */
export interface RoomScreenshotDisabledChangeEventData {
    /** 房间截屏禁用状态 */
    screenshot_disabled: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** ROOM_WATERMARK_DISABLED_CHANGED：房间水印禁用状态改变 */
export interface RoomWatermarkDisabledChangeEventData {
    /** 房间水印禁用状态 */
    watermark_disabled: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** ROOM_LOCKED_CHANGED：房间锁定状态改变 */
export interface RoomLockedChangeEventData {
    /** 房间锁定状态 */
    locked: boolean;
    /** 操作者用户id */
    op_uid?: string;
}
```

### 共享、消息与录制

```typescript
/** ROOM_SHARE_START：房间共享开始 */
export interface RoomShareStartEventData {
    /** 共享用户 */
    uid: string;
    /** 共享类型 */
    share_type: ShareType;
}

/** ROOM_SHARE_STOP：房间共享结束 */
export interface RoomShareStopEventData {
    /** 原共享用户 */
    uid: string;
    /** 原共享类型 */
    share_type: ShareType;
    /** 是否管理员操作 */
    by_admin: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** ROOM_CHAT_MSG：房间聊天消息 */
export interface RoomChatMsgEventData {
    /** 消息类型 */
    msg_type: ChatMsgType;
    /** 消息内容 */
    msg: string;
    /** 发送用户 */
    uid?: string;
    /** 是否私聊 */
    private: boolean;
}

/** ROOM_CUSTOM_MSG：房间自定义消息 */
export interface RoomCustomMsgEventData {
    /** 消息内容 */
    msg: string;
    /** 发送用户 */
    uid?: string;
    /** 是否私聊 */
    private: boolean;
}

/** ROOM_MCU_TASK：房间 MCU 任务消息 */
export interface RoomMcuTaskEventData {
    /** 任务类型 */
    task_type: McuTaskType;
    /** 任务状态 */
    task_status: McuTaskStatus;
    /** 错误描述 */
    err_desc: string;
}
```

### 转写与纪要（0.3.6 起）

转写结果为两遍模式：说话过程中先陆续推送若干条 `is_final = false` 的增量片段（低延迟、可能不准），一句话说完再推送一条 `is_final = true` 的整句定稿（带标点、更准确）。展示字幕时，建议按 `uid` 把增量片段拼成「正在说」的临时行，收到定稿后用整句替换。

```typescript
/** ROOM_ASR_STATE_CHANGED：会议转写（字幕）开关状态改变 */
export interface RoomAsrStateChangeEventData {
    /** 是否开启 */
    enabled: boolean;
    /** 开启失败时的错误描述 */
    err_desc: string;
}

/** ASR_RESULT：转写结果（字幕原文） */
export interface AsrResultEventData {
    /** 说话人用户id */
    uid: string;
    /** 说话人昵称 */
    name: string;
    /** 文本：非定稿时是增量片段，定稿时是整句 */
    text: string;
    /** 是否整句定稿 */
    is_final: boolean;
    /** 识别引擎原始模式，如 2pass-online / 2pass-offline */
    mode: string;
}

/** ASR_TRANSLATION：转写译文（实时翻译），只针对定稿句，到达时间晚于对应的 ASR_RESULT */
export interface AsrTranslationEventData {
    /** 转写场次id */
    session_id: string;
    /** 句子id */
    sentence_id: string;
    /** 说话人用户id */
    uid: string;
    /** 说话人昵称 */
    name: string;
    /** 原文 */
    text: string;
    /** 译文 */
    trans_text: string;
    /** 译文语言，如 en / zh */
    lang: string;
}

/** AI_SUMMARY_READY：会议纪要生成完成或失败，纪要内容用 aiSummary() 获取 */
export interface AiSummaryReadyEventData {
    /** 转写场次id */
    session_id: string;
    /** 纪要状态，2完成, 3失败 */
    status: number;
}
```

### 签到、等候室、分组与点名

```typescript
/** SIGN_IN_ACTIVITY：会中签到活动 */
export interface SignInActivityEventData {
    /** 主持人用户id */
    host_id: string;
    /** 主持人昵称 */
    host_name: string;
    /** 轮次 */
    epoch: number;
    /** 开始时间 */
    begin_at: number;
    /** 预计时长 */
    dur: number;
    /** 结束时间 */
    end_at: number;
    /** 签到说明 */
    desc: string;
}

/** SIGN_IN_FINISH：会中签到活动手动/自动结束 */
export interface SignInFinishEventData {
    /** 主持人用户id */
    host_id: string;
    /** 主持人昵称 */
    host_name: string;
    /** 轮次 */
    epoch: number;
}

/** USER_ENTER_WAITING_ROOM：会中用户进入等候室 */
export interface UserEnterWaitingRoomEventData {
    /** 用户id */
    uid: string;
    /** 用户昵称 */
    name: string;
    /** 用户头像 */
    avatar: string;
}

/** USER_EXIT_WAITING_ROOM：会中用户离开等候室 */
export interface UserExitWaitingRoomEventData {
    /** 用户id */
    uid: string;
    /** 用户昵称 */
    name: string;
    /** 用户头像 */
    avatar: string;
}

/** ADMIN_UPDATE_WAITING_ROOM_DISABLED：等候室禁用状态改变 */
export interface AdminUpdateWaitingRoomDisabledEventData {
    /** 等候室禁用状态 */
    waiting_room_disabled: boolean;
    /** 操作者用户id */
    op_uid?: string;
}

/** ADMIN_START_SUB_MEETING：主持人开始分组讨论 */
export interface AdminStartSubMeetingEventData {
    /** 会议id */
    meeting_id: string;
    /** 会议标题 */
    title: string;
    /** 用户id列表 */
    uids: string[];
}

/** ADMIN_STOP_SUB_MEETING：主持人结束分组讨论 */
export interface AdminStopSubMeetingEventData {
    /** 父会议id */
    parent: string;
}

/** ADMIN_MOVE_SUB_MEETING_USER：在小组之间或小组与主会场之间移动用户 */
export interface AdminMoveSubMeetingUserEventData {
    /** 当前会议ID */
    from_meeting_id: string;
    /** 当前会议标题 */
    from_meeting_title: string;
    /** 目标会议ID */
    to_meeting_id: string;
    /** 目标会议标题 */
    to_meeting_title: string;
}

/** ROLL_CALL_NAMED：会中点名 */
export interface RollCallNamedEventData {
    /** 点名id */
    id: string;
    /** 用户ID */
    sid: string;
    /** 当前时间 */
    time: number;
}
```

### 主持人请求

```typescript
/** ADMIN_CONFIRM_HANDUP：主持人处理您的举手申请 */
export interface AdminConfirmHandupEventData {
    /** 举手类型 */
    type: HandupType;
    /** 是否同意 */
    approve: boolean;
    /** 操作者用户id */
    op_uid?: string;
    /** 目标用户id */
    target_id: string;
}

/** ADMIN_REQUEST_OPEN_MIC：主持人请求您开麦 */
export interface AdminRequestOpenMicEventData {
    /** 操作者用户id */
    op_uid?: string;
}

/** ADMIN_REQUEST_OPEN_CAMERA：主持人请求您开摄像头 */
export interface AdminRequestOpenCameraEventData {
    /** 操作者用户id */
    op_uid?: string;
}

/** ADMIN_REQUEST_OPEN_SHARE：主持人请求您共享屏幕（0.3.7 起） */
export interface AdminRequestOpenShareEventData {
    /** 发起请求的主持人用户id（服务端发起时可能为空串），同意时作为 requestShare 的 adminUid 传回 */
    op_uid?: string;
}
```

## 会外消息事件

调用 `smeeting.enableIm()` 启用会外消息后，会外消息事件通过 `smeeting.onNotifyImEvent` 监听：

```typescript
smeeting.onNotifyImEvent = (evt: ImEvent) => {
  switch (evt.type) {
    case CommonImEventType.CALL_CALLING:
      // 有人呼叫入会
      break;
    case CommonImEventType.IM_CUSTOM_MSG: {
      // 业务自定义消息，按 action 区分
      const data = evt.data as ImCustomMsgEventData;
      console.log(data.action, data.content, data.uid);
      break;
    }
  }
};
```

CommonImEventType及对应`data`定义如下：

```typescript
    /** 开始断线自动重连，无data */
    static readonly RECONNECTING = 'reconnecting';
    /** 重连成功，无data */
    static readonly RECONNECTED = 'reconnected';
    /** 自己被强制断开会议外消息连接，对应data为 ImDisconnectEventData */
    static readonly DISCONNECTED = 'disconnected';

    /** 开始呼叫，对应data为 ImCallCallingEventData */
    static readonly CALL_CALLING = 'call_calling';
    /** 会议提醒，对应data为 ImMeetingRemindEventData */
    static readonly MEETING_REMIND = 'meeting_remind';
    /** 移出等候室消息，对应data为 ImAdminMoveOutWaitingRoomEventData */
    static readonly ADMIN_MOVE_OUT_WAITING_ROOM = 'admin_move_out_waiting_room';
    /** 小组请求帮助，对应data为 ImUserHelpSubMeetingEventData */
    static readonly USER_HELP_SUB_MEETING = 'user_help_sub_meeting';
    /** 业务自定义消息（action 不属于以上内置类型），对应data为 ImCustomMsgEventData（v0.3.2 起） */
    static readonly IM_CUSTOM_MSG = 'im_custom_msg';
```

业务自定义消息由服务端 [`im/send-msg`](/zh/rtc/server-api/im#发送im消息) 发送，`action` 自行约定（不要与上面的内置类型重名），`content` 会原样透传：

```typescript
interface ImCustomMsgEventData {
    /** 消息类型，即发送时填写的 action */
    action: string;
    /** 消息内容，即发送时填写的 content */
    content: any;
    /** 发送者会话ID */
    sid: string;
    /** 发送者用户ID */
    uid: string;
    /** 发送者名称 */
    name: string;
}
```

其余会外消息事件的 `data`：

```typescript
/** 会外消息事件 data 的公共字段（发送者） */
export interface ImBaseEventData {
    /** 会话ID */
    sid: string;
    /** 用户ID */
    uid: string;
    /** 用户名 */
    name: string;
    /** 用户头像 */
    avatar?: string;
}

/** DISCONNECTED：自己被强制断开会外消息连接 */
export interface ImDisconnectEventData {
    /** 断开原因 */
    reason: ImDisconnectReason;
    /** 错误 */
    error?: any;
}

export enum ImDisconnectReason {
    /** 错误 */
    Error = -1,
    /** 主动离开 */
    Self = 1,
    /** 被踢离开 */
    Kicked = 2,
    /** 心跳超时离开 */
    Timeout = 4,
}

/** CALL_CALLING：呼叫入会 */
export interface ImCallCallingEventData extends ImBaseEventData {
    content: {
        /** 房间号 */
        room_no: string;
        /** 会议ID */
        meeting_id: string;
        /** 会议标题 */
        title: string;
        /** 是否强制加入 */
        force_join: boolean;
    };
}

/** MEETING_REMIND：会议提醒 */
export interface ImMeetingRemindEventData extends ImBaseEventData {
    content: {
        /** 房间号 */
        room_no: string;
        /** 会议ID */
        meeting_id: string;
        /** 会议标题 */
        title: string;
        /** 创建者 */
        creator_name: string;
        /** 预计时长 */
        plan_dur: number;
        /** 预计开始时间 */
        plan_time: number;
        /** 是否强制加入 */
        force_join: boolean;
    };
}

/** ADMIN_MOVE_OUT_WAITING_ROOM：被移出等候室（私发给该成员） */
export interface ImAdminMoveOutWaitingRoomEventData extends ImBaseEventData {
    content: {
        /** 主会场会议ID */
        parent: string;
        /** 分会场会议ID */
        meeting_id: string;
        /** 小组名称 */
        title: string;
    };
}

/** USER_HELP_SUB_MEETING：小组请求帮助（私发给主持人/联席主持人） */
export interface ImUserHelpSubMeetingEventData extends ImBaseEventData {
    content: {
        /** 主会场会议ID */
        parent: string;
        /** 分会场会议ID */
        meeting_id: string;
        /** 小组名称 */
        title: string;
    };
}
```
