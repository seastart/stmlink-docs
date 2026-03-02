SMeeting是绝大多数操作的入口。

```typescript

    /**
     * 房间事件通知回调
     */
    onNotifyRoomEvent?: ((event: RoomEvent) => void);
    constructor(initParams: SdkInitParams);
    /**
     * sdk编译信息
     * @returns
     */
    buildInfo(): BuildInfo;
    /**
     * 登录sdk
     * @param token
     */
    login(token: string): Promise<void>;
    /**
     * 退出sdk
     * @param token
     */
    logout(): Promise<void>;
    /**
     * 创建会议
     * @returns 房间号
     */
    createRoom(req: MeetingCreateReq): Promise<string>;
    /**
     * 会前修改会议
     */
    updateRoom(id: string, req: Partial<MeetingCreateReq>): Promise<void>;
    /**
     * 进入会议
     */
    enterRoom(req: MeetingEnterReq): Promise<void>;
    /**
     * 退出会议
     */
    exitRoom(): Promise<void>;
    /**
     * 获取会议信息
     * @returns
     */
    getRoomInfo(): RoomInfo | null;
    /**
     * 获取某用户信息
     * @returns
     */
    getUserInfo(uid: string): UserInfo;
    /**
     * 获取会议内用户信息列表
     * @returns
     */
    getUsersInfo(map: true): Record<string, UserInfo>;
    getUsersInfo(map: false): UserInfo[];
    /**
     * 关闭摄像头
     * @param byAdmin 是否管理员强制关闭
     */
    abstract closeCamera(byAdmin: boolean): Promise<any>;
    /**
     * 关闭麦克风
     * @param byAdmin 是否管理员强制关闭
     */
    abstract closeMic(byAdmin: boolean): Promise<any>;
    /**
     * 停止播放远端用户视频
     * @param uid 远端用户id
     * @param trackDesc 视频轨道描述
     */
    abstract stopPlayRemoteVideo(uid: string, trackDesc: TrackDesc): Promise<void>;
    /**
     * 更新会中昵称
     * @param name
     */
    updateName(name: string): Promise<void>;
    /**
     * 发送聊天消息，可单发和群发
     * @param msg_type 消息类型
     * @param msg 消息内容
     * @param target_id 消息接收者 为空时表示全房间接收
     */
    sendRoomChatMessage(msg: string, target_id: string, msg_type?: ChatMsgType): Promise<void>;
    /**
     * 发送自定义消息，可单发和群发
     * @param content 消息内容
     * @param target_id 消息接收者 为空时表示全房间接收
     */
    sendRoomCustomMessage(content: string, target_id: string): Promise<void>;
    /**
     * 举手
     */
    requestHandup(code: HandupType): Promise<void>;
    /**
     * 取消举手
     * @param code 举手类型
     */
    cancelHandup(code: HandupType): Promise<void>;
    /**
     * 回复打开摄像头请求
     * @param approve 是否同意
     * @param target_id //来源用户(主持人)id
     */
    confirmOpenCamera(target_id: string, approve: boolean): Promise<void>;
    /**
     * 回复打开麦克风请求
     * @param approve 是否同意
     * @param target_id 来源用户(主持人)id
     */
    confirmOpenMic(target_id: string, approve: boolean): Promise<void>;
    /**
     * 结束会议（解散）
     */
    adminDestroyRoom(): Promise<void>;
    /**
     * 更新房间摄像头使用权限禁用状态
     * @param self_unmute_camera_disabled 是否允许自我解除 false允许, true禁止
     * @param camera_disabled 是否允许开关摄像头  false允许, true禁止
     */
    adminUpdateRoomCameraState(self_unmute_camera_disabled: boolean, camera_disabled: boolean): Promise<void>;
    /**
     * 更新房间摄像头允许自我解除
     * @param self_unmute_camera_disabled 是否允许自我解除 false允许, true禁止
     */
    adminUpdateRoomSelfUnmuteCameraDisabled(self_unmute_camera_disabled: boolean): Promise<void>;
    /**
     * 更新房间麦克风使用权限禁用状态
     * @param self_unmute_mic_disabled 是否允许自我解除 false允许, true禁止
     * @param mic_disabled 是否允许开关麦克风  false允许, true禁止
     */
    adminUpdateRoomMicState(self_unmute_mic_disabled: boolean, mic_disabled: boolean): Promise<void>;
    /**
     * 更新房间麦克风允许自我解除
     * @param self_unmute_mic_disabled 是否允许自我解除 false允许, true禁止
     */
    adminUpdateRoomSelfUnmuteMicDisabled(self_unmute_mic_disabled: boolean): Promise<void>;
    /**
     * 更新房间聊天使用权限禁用状态
     * @param chat_disabled 是否允许聊天  false允许, true禁止
     */
    adminUpdateRoomChatDisabled(chat_disabled: boolean): Promise<void>;
    /**
     * 更新房间截屏禁用状态
     * @param screenshot_disabled 是否允许截屏  false允许, true禁止
     */
    adminUpdateRoomScreenshotDisabled(screenshot_disabled: boolean): Promise<void>;
    /**
     * 更新房间水印禁用状态
     * @param watermark_disabled 水印禁用状态  false开启水印, true关闭水印
     */
    adminUpdateRoomWatermarkDisabled(watermark_disabled: boolean): Promise<void>;
    /**
     * 更新房间锁定状态
     * @param locked 是否锁定  false解锁, true锁定
     */
    adminUpdateRoomLocked(locked: boolean): Promise<void>;
    /**
     * 停止房间共享
     */
    adminStopRoomShare(): Promise<void>;
    /**
     * 更新用户名称
     * @param target_id 用户id
     * @param nickname 用户昵称
     */
    adminUpdateUserName(target_id: string, nickname: string): Promise<void>;
    /**
     * 更新用户角色
     * @param target_id 用户id
     * @param role 用户角色
     */
    adminUpdateUserRole(target_id: string, role: Role): Promise<void>;
    /**
     * 更新远端用户聊天禁用状态
     * @param target_id 用户id
     * @param chat_disabled 是否允许聊天  false允许, true禁止
     */
    adminUpdateUserChatDisabled(target_id: string, chat_disabled: boolean): Promise<void>;
    /**
     * 主动转移主持人
     * @param target_id 用户id
     */
    adminMoveHost(target_id: string): Promise<void>;
    /**
     * 请求远端用户打开摄像头
     * @param target_id 用户id
     */
    adminRequestUserOpenCamera(target_id: string): Promise<void>;
    /**
     * 关闭远端用户摄像头
     * @param target_id 用户id
     */
    adminCloseUserCamera(target_id: string): Promise<void>;
    /**
     * 请求远端用户打开麦克风
     */
    adminRequestUserOpenMic(target_id: string): Promise<void>;
    /**
     * 关闭远端用户麦克风
     * @param target_id 用户id
     */
    adminCloseUserMic(target_id: string): Promise<void>;
    /**
     * 将远端用户踢出房间
     * @param target_id 用户id
     * @param join_disabled 是否禁止再入会
     */
    adminKickUserOut(target_id: string, join_disabled: boolean): Promise<void>;
    /**
     * 主持人确认举手请求，同意或拒绝
     */
    adminConfirmHandup(target_id: string, approve: boolean, code: HandupType): Promise<void>;
    /**
     * 打开摄像头
     */
    requestOpenCamera(): Promise<PusherOptions>;
    /**
     * 关闭摄像头
     * @param byAdmin 是否管理员强制关闭
     */
    closeCamera(byAdmin?: boolean): Promise<PusherOptions>;
    /**
     * 切换前后置摄像头
     */
    switchCamera(): Promise<PusherOptions>;
    /**
     * 打开麦克风
     */
    requestOpenMic(): Promise<PusherOptions>;
    /**
     * 关闭麦克风
     * @param byAdmin 是否管理员强制关闭
     */
    closeMic(byAdmin?: boolean): Promise<PusherOptions>;
    /**
     * 开始播放远端用户视频
     * @param container 播放容器
     * @param uid 远程用户id
     * @param trackDesc 视频轨道描述
     * @returns
     */
    startPlayRemoteVideo(uid: string, trackDesc: TrackDesc): Promise<RemoteTrack>;
    /**
     * 停止播放远端用户视频
     * @param uid 远端用户id
     * @param trackDesc 视频轨道描述
     */
    stopPlayRemoteVideo(uid: string, trackDesc: TrackDesc): Promise<void>;
    /**
     * 获取小程序运行环境信息
     * @returns
     */
    getEnvInfo(): EnvWxInfo;
    /**
     * livepusher配置
     */
    getPusherOptions(): PusherOptions;
    /**
     * 上报live-pusher的volumenotify
     * 你需要在live-pusher组件bindaudiovolumenotify
     * @param detail 小程序的event.detail
     * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html
     */
    updatePusherVolume(detail: any): void;
    /**
     * 上报live-pusher的error
     * 你需要在live-pusher组件binderror
     * @param detail 小程序的event.detail
     * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html
     */
    updatePusherError(detail: any): void;
    /**
     * 上报live-pusher的netstatus
     * 你需要在live-pusher组件bindnetstatus
     * @param detail 小程序的event.detail
     * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html
     */
    updatePusherNetStatus(detail: any): void;
    /**
     * 上报live-pusher的statechange事件
     * 你需要在live-pusher组件bindstatechange
     * @param detail 小程序的event.detail
     * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html
     */
    updatePusherStateChange(detail: any): void;
    /**
     * 上报live-player的netstatus
     * 你需要在live-player组件bindnetstatus
     * @param uid 流轨道的所有者
     * @param trackId 流轨道id
     * @param detail 小程序的event.detail
     * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-player.html
     */
    updatePlayerNetStatus(uid: string, trackId: string, detail: any): void;
    /**
     * 上报live-player的statechange事件
     * 你需要在live-player组件bindstatechange
     * @param uid 流的所有者
     * @param trackId 流轨道id
     * @param detail 小程序的event.detail
     * @see https://developers.weixin.qq.com/miniprogram/dev/component/live-player.html
     */
    updatePlayerStateChange(uid: string, trackId: string, detail: any): void;
    
```

