---
title: "SMeeting"
description: "Web 会议 SDK 的主入口类，绝大多数会议操作都从这里发起"
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
     * 会议参会记录
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
     * 获取白板地址（进入会议后可读，见「白板共享」）
     * @returns
     */
    getWhiteBoard(): string | undefined;
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
     * 发文件时先用 presignedPutObject(PresignedPutObjectType.Chat, ...) 上传，再把 {key, name, size} 的 JSON 字符串作为 msg 发出，
     * 详见「聊天与文件消息」/zh/meeting/web/advanced/chat
     * @param msg 消息内容，文件 / 图片 / 语音类消息为 JSON 字符串
     * @param msgType 消息类型，默认 ChatMsgType.Text
     * @param targetId 消息接收者 为空时表示全房间接收
     */
    sendRoomChatMessage(msg: string, msgType?: ChatMsgType, targetId?: string): Promise<void>;
    /**
     * 聊天历史消息（分页）
     * @param meeting_id 会议ID
     * @param page 页码
     * @param perPage 每页数量
     */
    roomChatMsgList(meeting_id: string, page: number, perPage: number): Promise<{
        data: ChatMsgInfo[];
        _meta: MetaRes;
    }>;
    /**
     * 资源-预签名上传：换一个带签名的上传地址（2 小时有效），拿到后自己 PUT 文件二进制上去
     * @param type 资源类别，聊天文件传 PresignedPutObjectType.Chat
     * @param meetingId 会议ID
     * @param ext 扩展名，不带点
     * @returns url 上传地址；key 资源Key（发消息 / 换下载地址用）；ext 扩展名
     */
    presignedPutObject(type: PresignedPutObjectType, meetingId: string, ext: string): Promise<{
        url: string;
        key: string;
        ext: string;
    }>;
    /**
     * 资源-预签名下载：换一个带签名的下载地址（2 小时有效）
     * @param resKey 资源Key 二选一（聊天文件传消息里的 key）
     * @param id 资源ID 二选一
     */
    presignedGetObject(resKey?: string, id?: string): Promise<{
        url: string;
    }>;
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
     * @param role 目标角色 Role.Member(0) / Role.CoHost(2)；Role.Host(1) 由会议的主持人决定，不能在这里设
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
     *
     * publish 为 false 时只采集、只在 container 里预览（设备检测、设置页预览）：不请求会控、不发布、
     * 不发摄像头状态事件，会前会中都可用。之后再以 publish: true 调用会把这条轨「转正」——
     * 请求会控并发布同一条轨，不重新采集；摄像头已作为会议摄像头打开时以 publish: false 调用，
     * 直接返回正在用的轨（只追加预览容器）。关闭统一用 closeCamera；只想移除自己加的预览容器用
     * track.removePlayView(container)。会前打开的摄像头入会后再次调用会补发布。
     * @param container 预览容器
     * @param deviceId 摄像头设备id
     * @param preset 摄像头预设值
     * @param byAdmin 是否主持人操作
     * @param adminUid 主持人id（哪个主持人请求打开）
     * @param publish 是否作为会议摄像头打开并发布，默认 true；false 只采集预览（0.3.5 起）
     */
    requestOpenCamera(container: HTMLElement, deviceId?: string, preset?: CameraPreset, byAdmin?: boolean, adminUid?: string, publish?: boolean): Promise<LocalCameraTrack>;
    /**
     * 切换摄像头
     * @param deviceId 摄像头设备id，手机端不传自动切换前后置摄像头，桌面端可指定摄像头
     */
    switchCamera(deviceId?: string): Promise<void>;
    /**
     * 打开麦克风
     *
     * publish 为 false 时只采集（设备检测、会中试音）：不请求会控、不发布、不发麦克风状态事件，
     * 会前会中都可用，用返回轨道的 getVolume() 读音量；setAudioProcessor 设置的处理器同样会挂上。
     * 之后再以 publish: true 调用会把这条轨「转正」（请求会控并发布同一条轨，不重新采集）；
     * 麦克风已作为会议麦克风打开时以 publish: false 调用直接返回正在用的轨。关闭统一用 closeMic。
     * 会前打开的麦克风入会后再次调用会补发布。
     * @param deviceId 麦克风设备id
     * @param preset 麦克风预设值
     * @param byAdmin 是否主持人操作
     * @param adminUid 主持人id（哪个主持人请求打开）
     * @param publish 是否作为会议麦克风打开并发布，默认 true；false 只采集（0.3.5 起）
     * @returns 本地麦克风轨道（0.3.5 起）
     */
    requestOpenMic(deviceId?: string, preset?: MicPreset, byAdmin?: boolean, adminUid?: string, publish?: boolean): Promise<LocalMicTrack>;
    /**
     * 切换麦克风
     * @param deviceId 麦克风设备id
     */
    switchMic(deviceId: string): Promise<void>;
    /**
     * 设置麦克风音频处理器（如 AI 降噪插件 `@seastart/srtc-plugin-deepfilternet` 的 `DeepFilterNetProcessor`），
     * 传 `undefined` 清除。传数组时按顺序串联。自 0.3.4 起提供，仅 Web 端。
     *
     * 入会前后都可以调用：麦克风已开时立即挂上（替换旧处理器），之后每次开麦自动挂上、关麦时卸下，
     * 离会后设置仍保留。处理器在关麦时会被 destroy、开麦时重新 init，同一个实例可以反复使用。
     * 开麦时挂载失败不影响开麦，只记录警告。用法见「AI 降噪」进阶实践页。
     * @param processor 音频处理器；`undefined` 表示清除
     */
    setAudioProcessor(processor?: AudioTrackProcessor | AudioTrackProcessor[]): Promise<void>;
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
    /**
     * 摄像头是否作为会议摄像头打开（requestOpenCamera 默认 publish: true）。
     * publish: false 只预览时摄像头在采集、本方法返回 false，用来决定关预览时要不要 closeCamera（0.3.5 起）
     */
    isCameraOpened(): boolean;
    /**
     * 麦克风是否作为会议麦克风打开（requestOpenMic 默认 publish: true），含义同 isCameraOpened（0.3.5 起）
     */
    isMicOpened(): boolean;
```



