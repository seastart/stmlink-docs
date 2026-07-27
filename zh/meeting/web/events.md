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
    /** 自己被强制离开频道，对应data为 DisconnectEventData */
    static readonly DISCONNECTED = 'disconnected';

    /** 其他用户加入频道，对应data为 UserInfo */
    static readonly USER_ENTER = 'user_enter';
    /** 其他用户离开频道，对应data为 UserExitEventData */
    static readonly USER_EXIT = 'user_exit';
    /** 用户摄像头状态变化(自己/他人主动改变或被主持人改变)，对应data为 UserCameraStateChangeEventData */
    static readonly USER_CAMREA_STATE_CHANGED = "user_camera_state_changed";
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

    /** 主持人处理您的举手申请，对应data为 AdminConfirmHandupEventData */
    static readonly ADMIN_CONFIRM_HANDUP = 'admin_confirm_handup';
    /** 主持人请求您开麦，对应data为 AdminRequestOpenMicEventData */
    static readonly ADMIN_REQUEST_OPEN_MIC = 'admin_request_open_mic';
    /** 主持人请求您开摄像头，对应data为 AdminRequestOpenCameraEventData */
    static readonly ADMIN_REQUEST_OPEN_CAMERA = 'admin_request_open_camera';

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
}

```

