---
title: "SMeeting"
description: "Web SMeeting 会议 SDK SMeeting 接口参考"
---

SMeeting是绝大多数操作的入口。

```typescript

    /**
     * 房间事件通知回调
     */
    onNotifyRoomEvent?: ((event: RoomEvent) => void);
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
     * @param meeting_id 会议id
     * @param req 修改会议参数
     */
    updateRoom(meeting_id: string, req: Partial<MeetingCreateReq>): Promise<void>;
    /**
     * 进入会议
     * @param req 加入会议参数
     */
    enterRoom(req: MeetingEnterReq): Promise<void>;
    /**
     * 需要参加的会议
     * @param req 分页参数
     */
    attendeeRoom(req: PageParam): Promise<{
        data: MeetingInfo[];
        _meta: MetaRes;
    }>;
    /**
    * 历史会议
    * @param req 分页参数
    */
    attendedRoom(req: PageParam): Promise<{
        data: MeetingInfo[];
        _meta: MetaRes;
    }>;
    /**
     * 会议详情
     * @param meeting_id 会议id
     */
    detailRoom(meeting_id: string): Promise<MeetingInfo>;
    /**
     * 取消会议
     * @param meeting_id 会议id
     */
    cancelRoom(meeting_id: string): Promise<void>;
    /**
     * 会议参会人员
     * @param meeting_id 会议id
     * @param pageParam 分页参数
     */
    roomParticipant(meeting_id: string, page: number, perPage: number): Promise<{
        data: ParticipantInfo[];
        _meta: MetaRes;
    }>;
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
     * 拒绝主持人打开麦克风的请求
     * @param adminUid 主持人id（哪个主持人请求打开）
     */
    rejectOpenMic(adminUid?: string): Promise<void>;
    /**
     * 拒绝主持人打开摄像头的请求
     * @param adminUid 主持人id（哪个主持人请求打开）
     */
    rejectOpenCamera(adminUid?: string): Promise<void>;
    /**
     * 关闭摄像头
     */
    closeCamera(): Promise<any>;
    /**
     * 关闭麦克风
     */
    closeMic(): Promise<any>;
    /**
     * 更新会中昵称
     * @param name
     */
    updateName(name: string): Promise<void>;
    /**
     * 发送聊天消息，可单发和群发
     * @param msg 消息内容
     * @param msg_type 消息类型
     * @param target_id 消息接收者 为空时表示全房间接收
     */
    sendRoomChatMessage(msg: string, msgType?: ChatMsgType, targetId?: string): Promise<void>;
    /**
     * 发送自定义消息，可单发和群发
     * @param content 消息内容
     * @param targetId 消息接收者 为空时表示全房间接收
     */
    sendRoomCustomMessage(content: string, targetId?: string): Promise<void>;
    /**
     * 举手
     * @param code 举手类型
     */
    requestHandup(code: HandupType): Promise<void>;
    /**
     * 取消举手
     * @param code 取消举手类型
     */
    cancelHandup(code: HandupType): Promise<void>;
    /**
     * 结束会议（解散）
     */
    adminDestroyRoom(): Promise<void>;
    /**
     * 更新房间摄像头使用权限禁用状态
     * @param selfUnmuteCameraDisabled 是否禁用自我解除
     * @param cameraDisabled 是否禁用摄像头
     */
    adminUpdateRoomCameraState(selfUnmuteCameraDisabled: boolean, cameraDisabled: boolean): Promise<void>;
    /**
     * 更新房间摄像头允许自我解除
     * @param selfUnmuteCameraDisabled 是否禁用自我解除
     */
    adminUpdateRoomSelfUnmuteCameraDisabled(selfUnmuteCameraDisabled: boolean): Promise<void>;
    /**
     * 更新房间麦克风使用权限禁用状态(全体禁音和全体解除禁音)
     * @param selfUnmuteMicDisabled 是否禁用自我解除
     * @param micDisabled 是否禁用麦克风
     */
    adminUpdateRoomMicState(selfUnmuteMicDisabled: boolean, micDisabled: boolean): Promise<void>;
    /**
     * 更新房间麦克风允许自我解除
     * @param selfUnmuteMicDisabled 是否禁用自我解除
     */
    adminUpdateRoomSelfUnmuteMicDisabled(selfUnmuteMicDisabled: boolean): Promise<void>;
    /**
     * 更新房间聊天使用权限禁用状态
     * @param chatDisabled 是否禁用聊天
     */
    adminUpdateRoomChatDisabled(chatDisabled: boolean): Promise<void>;
    /**
     * 更新房间截屏禁用状态
     * @param screenshotDisabled 是否禁用截屏
     */
    adminUpdateRoomScreenshotDisabled(screenshotDisabled: boolean): Promise<void>;
    /**
     * 更新房间水印禁用状态
     * @param watermarkDisabled 水印禁用状态  false开启水印, true关闭水印
     */
    adminUpdateRoomWatermarkDisabled(watermarkDisabled: boolean): Promise<void>;
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
     * @param targetId 用户id
     * @param nickname 用户昵称
     */
    adminUpdateUserName(targetId: string, nickname: string): Promise<void>;
    /**
     * 更新用户角色
     * @param targetId 用户id
     * @param role 用户角色
     */
    adminUpdateUserRole(targetId: string, role: Role): Promise<void>;
    /**
     * 更新远端用户聊天禁用状态
     * @param targetId 用户id
     * @param chatDisabled 是否禁止聊天
     */
    adminUpdateUserChatDisabled(targetId: string, chatDisabled: boolean): Promise<void>;
    /**
     * 主动转移主持人
     * @param targetId 用户id
     */
    adminMoveHost(targetId: string): Promise<void>;
    /**
     * 请求远端用户打开摄像头
     * @param targetId 用户id
     */
    adminRequestUserOpenCamera(targetId: string): Promise<void>;
    /**
     * 关闭远端用户摄像头
     * @param targetId 用户id
     */
    adminCloseUserCamera(targetId: string): Promise<void>;
    /**
     * 请求远端用户打开麦克风
     *  @param targetId 用户id
     */
    adminRequestUserOpenMic(targetId: string): Promise<void>;
    /**
     * 关闭远端用户麦克风
     * @param targetId 用户id
     */
    adminCloseUserMic(targetId: string): Promise<void>;
    /**
     * 将远端用户踢出房间
     * @param targetId 用户id
     * @param joinDisabled 是否禁止再入会
     */
    adminKickUserOut(targetId: string, joinDisabled: boolean): Promise<void>;
    /**
     * 主持人确认举手请求，同意或拒绝
     *  @param targetId 用户id
     *  @param approve 是否同意
     *  @param code 举手类型
     */
    adminConfirmHandup(targetId: string, approve: boolean, code: HandupType): Promise<void>;
    /**
     * 主持人邀请设备入会
     * @param agents 邀请的设备
     * @param no 房间号
    */
    adminInviteAgent(agents: {
        type: AgentType;
        contact: string;
    }[], no: string): Promise<void>;
    /**
     * 修改参会人员
     * @param conferee 参会人员
    */
    adminUpdateConferee(conferee: string[]): Promise<void>;
    /**
     * 修改合成会议的布局
     */
    adminUpdateLayout(layoutData: LayoutData): Promise<void>;
    /**
     * 设备列表
     * @param type 设备类型
     * @param name 名称
     * @param page 页码
     * @param perPage 每页数量
     */
    agentList(type: AgentType[], name: string, page: number, perPage: number): Promise<{
        data: AgentInfo[];
        _meta: MetaRes;
    }>;
    /**
     * 开始录制
     * @param req 录制参数
     */
    mcuStart(req: McuStartReq): Promise<void>;
    /**
     * 停止录制
     */
    mcuStop(): Promise<void>;
    /**
     * 获取录制配置
     */
    mcuRecordConfig(): Promise<McuRecordConfig>;
    /**
     * 获取录制详情
     */
    mcuRecordDetail(): Promise<McuRecordDetail>;

    enterRoom(req: MeetingEnterReq): Promise<void>;
    /**
     * 打开摄像头
     * @param container 预览容器
     * @param deviceId 摄像头设备id
     * @param preset 摄像头预设值
     * @param byAdmin 是否主持人操作
     * @param adminUid 主持人id（哪个主持人请求打开）
     */
    requestOpenCamera(container: HTMLElement, deviceId?: string, preset?: CameraPreset, byAdmin?: boolean, adminUid?: string): Promise<LocalCameraTrack>;
    /**
     * 切换摄像头
     * @param deviceId 摄像头设备id，手机端不传自动切换前后置摄像头，桌面端可指定摄像头
     */
    switchCamera(deviceId?: string): Promise<void>;
    /**
     * 打开麦克风
     * @param deviceId 麦克风设备id
     * @param preset 麦克风预设值
     * @param byAdmin 是否主持人操作
     * @param adminUid 主持人id（哪个主持人请求打开）
     */
    requestOpenMic(deviceId?: string, preset?: MicPreset, byAdmin?: boolean, adminUid?: string): Promise<void>;
    /**
     * 切换麦克风
     * @param deviceId 麦克风设备id
     */
    switchMic(deviceId: string): Promise<void>;
    /**
     * 打开共享
     * @param shareType 共享类型
     * @param container 预览容器
     */
    requestShare(shareType?: ShareType, preset?: ScreenPreset, container?: HTMLElement): Promise<void>;
    /**
     * 停止共享
     */
    stopShare(): Promise<void>;
    /**
     * 开始播放远端用户视频
     * @param container 播放容器
     * @param uid 远程用户id
     * @param trackDesc 视频轨道描述
     * @returns
     */
    startPlayRemoteVideo(container: HTMLElement, uid: string, trackDesc: TrackDesc): Promise<RemoteVideoTrack>;
    /**
     * 停止播放远端用户视频
     * @param container 播放容器
     * @param uid 远端用户id
     * @param trackDesc 视频轨道描述
     */
    stopPlayRemoteVideo(container: HTMLElement, uid: string, trackDesc: TrackDesc): Promise<void>;
    /**
     * 订阅远端流
     * @param uid 远端用户id
     * @param trackDesc 视频轨道描述
     * @returns
     */
    subscribeRemoteVideoTrack(uid: string, trackDesc: TrackDesc): Promise<RemoteVideoTrack>;
    /**
     * 取消订阅远端流
     * @param uid 远端用户id
     * @param trackDesc 视频轨道描述
     */
    unsubscribeRemoteVideoTrack(uid: string, trackDesc: TrackDesc): Promise<void>;
    /**
     * 切换远程音频的静音/取消静音状态(可以指定设备)
     * @param mute 是否静音
     * @param opt 扬声器配置
     */
    toggleRemoteAudioMute(mute: boolean, opt?: AudioOutputOptions): Promise<void>;
    /**
     * 开始播放远端合成视频
     * @param container 播放容器
     * @returns
     */
    startPlayRemoteVideoMcu(container: HTMLElement): Promise<RemoteVideoTrack>;
    /**
     * 停止播放远端合成视频
     * @param container 播放容器
     */
    stopPlayRemoteVideoMcu(container: HTMLElement): Promise<void>;
    /**
     * 获取web运行环境信息，如是否支持webrtc等
     * @returns
     */
    getEnvInfo(): EnvWebInfo;
    /**
     * 获取设备列表
     * @param kind
     * @param requestPermissions
     * @returns
     */
    getDevices(kind?: MediaDeviceKind, requestPermissions?: boolean): Promise<MediaDeviceInfo[]>;
```



