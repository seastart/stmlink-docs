---
title: "SMeeting"
description: "Full method list of SMeeting, the main entry class of the Web conferencing SDK: login, creating and entering meetings, camera/mic/sharing, chat and custom messages, raise hand, host controls, device invitations, and recording. Read this to look up a method signature."
---

SMeeting is the entry point for most operations.

```typescript

    /**
     * Room event notification callback
     */
    onNotifyRoomEvent?: ((event: RoomEvent) => void);
    /**
     * SDK build info
     * @returns
     */
    buildInfo(): BuildInfo;
    /**
     * Log in to the SDK
     * @param token
     */
    login(token: string): Promise<void>;
    /**
     * Log out of the SDK
     * @param token
     */
    logout(): Promise<void>;
    /**
     * Create a meeting
     * @returns Room number
     */
    createRoom(req: MeetingCreateReq): Promise<string>;
    /**
     * Update a meeting before it starts
     * @param meeting_id Meeting ID
     * @param req Meeting update parameters
     */
    updateRoom(meeting_id: string, req: Partial<MeetingCreateReq>): Promise<void>;
    /**
     * Enter a meeting
     * @param req Parameters for entering the meeting
     */
    enterRoom(req: MeetingEnterReq): Promise<void>;
    /**
     * Meetings you need to attend
     * @param req Pagination parameters
     */
    attendeeRoom(req: PageParam): Promise<{
        data: MeetingInfo[];
        _meta: MetaRes;
    }>;
    /**
    * Past meetings
    * @param req Pagination parameters
    */
    attendedRoom(req: PageParam): Promise<{
        data: MeetingInfo[];
        _meta: MetaRes;
    }>;
    /**
     * Meeting details
     * @param meeting_id Meeting ID
     */
    detailRoom(meeting_id: string): Promise<MeetingInfo>;
    /**
     * Cancel a meeting
     * @param meeting_id Meeting ID
     */
    cancelRoom(meeting_id: string): Promise<void>;
    /**
     * Attendance records of a meeting
     * @param meeting_id Meeting ID
     * @param pageParam Pagination parameters
     */
    roomParticipant(meeting_id: string, page: number, perPage: number): Promise<{
        data: ParticipantInfo[];
        _meta: MetaRes;
    }>;
    /**
     * Exit the meeting
     */
    exitRoom(): Promise<void>;
    /**
     * Get the meeting info
     * @returns
     */
    getRoomInfo(): RoomInfo | null;
    /**
     * Get the whiteboard URL (readable after entering the meeting; see "Whiteboard sharing")
     * @returns
     */
    getWhiteBoard(): string | undefined;
    /**
     * Get a user's info
     * @returns
     */
    getUserInfo(uid: string): UserInfo;
    /**
     * Get the list of users in the meeting
     * @returns
     */
    getUsersInfo(map: true): Record<string, UserInfo>;
    getUsersInfo(map: false): UserInfo[];
    /**
     * Decline the host's request to unmute your mic
     * @param adminUid Host ID (which host made the request)
     */
    rejectOpenMic(adminUid?: string): Promise<void>;
    /**
     * Decline the host's request to turn on your camera
     * @param adminUid Host ID (which host made the request)
     */
    rejectOpenCamera(adminUid?: string): Promise<void>;
    /**
     * Close the camera
     */
    closeCamera(): Promise<any>;
    /**
     * Close the mic
     */
    closeMic(): Promise<any>;
    /**
     * Update the in-meeting display name
     * @param name
     */
    updateName(name: string): Promise<void>;
    /**
     * Send a chat message, to one member or to everyone
     * To send a file, first upload it with presignedPutObject(PresignedPutObjectType.Chat, ...), then send a JSON string of {key, name, size} as msg;
     * see "In-meeting chat and file messages" /en/meeting/web/advanced/chat
     * @param msg Message content; a JSON string for file / image / voice messages
     * @param msgType Message type, defaults to ChatMsgType.Text
     * @param targetId Message recipient; empty means everyone in the room receives it
     */
    sendRoomChatMessage(msg: string, msgType?: ChatMsgType, targetId?: string): Promise<void>;
    /**
     * Chat message history (paged)
     * @param meeting_id Meeting ID
     * @param page Page number
     * @param perPage Items per page
     */
    roomChatMsgList(meeting_id: string, page: number, perPage: number): Promise<{
        data: ChatMsgInfo[];
        _meta: MetaRes;
    }>;
    /**
     * Resource - presigned upload: get a signed upload URL (valid for 2 hours), then PUT the file binary to it yourself
     * @param type Resource category; pass PresignedPutObjectType.Chat for chat files
     * @param meetingId Meeting ID
     * @param ext Extension without the dot
     * @returns url upload URL; key resource key (for sending the message / getting a download URL); ext extension
     */
    presignedPutObject(type: PresignedPutObjectType, meetingId: string, ext: string): Promise<{
        url: string;
        key: string;
        ext: string;
    }>;
    /**
     * Resource - presigned download: get a signed download URL (valid for 2 hours)
     * @param resKey Resource key, one of the two (for chat files, the key in the message)
     * @param id Resource ID, one of the two
     */
    presignedGetObject(resKey?: string, id?: string): Promise<{
        url: string;
    }>;
    /**
     * Send a custom message, to one member or to everyone
     * @param content Message content
     * @param targetId Message recipient; empty means everyone in the room receives it
     */
    sendRoomCustomMessage(content: string, targetId?: string): Promise<void>;
    /**
     * Raise a hand
     * @param code Raise-hand type
     */
    requestHandup(code: HandupType): Promise<void>;
    /**
     * Lower a hand
     * @param code Raise-hand type to cancel
     */
    cancelHandup(code: HandupType): Promise<void>;
    /**
     * End the meeting (dismiss)
     */
    adminDestroyRoom(): Promise<void>;
    /**
     * Update the room's camera permission state
     * @param selfUnmuteCameraDisabled Whether members are prevented from turning their own camera back on
     * @param cameraDisabled Whether the camera is disabled
     */
    adminUpdateRoomCameraState(selfUnmuteCameraDisabled: boolean, cameraDisabled: boolean): Promise<void>;
    /**
     * Update whether members can turn their own camera back on in the room
     * @param selfUnmuteCameraDisabled Whether members are prevented from turning their own camera back on
     */
    adminUpdateRoomSelfUnmuteCameraDisabled(selfUnmuteCameraDisabled: boolean): Promise<void>;
    /**
     * Update the room's mic permission state (mute all and unmute all)
     * @param selfUnmuteMicDisabled Whether members are prevented from unmuting themselves
     * @param micDisabled Whether the mic is disabled
     */
    adminUpdateRoomMicState(selfUnmuteMicDisabled: boolean, micDisabled: boolean): Promise<void>;
    /**
     * Update whether members can unmute their own mic in the room
     * @param selfUnmuteMicDisabled Whether members are prevented from unmuting themselves
     */
    adminUpdateRoomSelfUnmuteMicDisabled(selfUnmuteMicDisabled: boolean): Promise<void>;
    /**
     * Update the room's chat permission state
     * @param chatDisabled Whether chat is disabled
     */
    adminUpdateRoomChatDisabled(chatDisabled: boolean): Promise<void>;
    /**
     * Update the room's screenshot-disabled state
     * @param screenshotDisabled Whether screenshots are disabled
     */
    adminUpdateRoomScreenshotDisabled(screenshotDisabled: boolean): Promise<void>;
    /**
     * Update the room's watermark-disabled state
     * @param watermarkDisabled Watermark-disabled state: false turns the watermark on, true turns it off
     */
    adminUpdateRoomWatermarkDisabled(watermarkDisabled: boolean): Promise<void>;
    /**
     * Update the room's locked state
     * @param locked Whether the room is locked: false unlocks, true locks
     */
    adminUpdateRoomLocked(locked: boolean): Promise<void>;
    /**
     * Stop sharing in the room
     */
    adminStopRoomShare(): Promise<void>;
    /**
     * Update a user's name
     * @param targetId User ID
     * @param nickname User's display name
     */
    adminUpdateUserName(targetId: string, nickname: string): Promise<void>;
    /**
     * Update a user's role
     * @param targetId User ID
     * @param role Target role Role.Member(0) / Role.CoHost(2); Role.Host(1) is determined by the meeting's host and can't be set here
     */
    adminUpdateUserRole(targetId: string, role: Role): Promise<void>;
    /**
     * Update a remote user's chat-disabled state
     * @param targetId User ID
     * @param chatDisabled Whether chat is disabled for the user
     */
    adminUpdateUserChatDisabled(targetId: string, chatDisabled: boolean): Promise<void>;
    /**
     * Transfer the host role
     * @param targetId User ID
     */
    adminMoveHost(targetId: string): Promise<void>;
    /**
     * Ask a remote user to open the camera
     * @param targetId User ID
     */
    adminRequestUserOpenCamera(targetId: string): Promise<void>;
    /**
     * Close a remote user's camera
     * @param targetId User ID
     */
    adminCloseUserCamera(targetId: string): Promise<void>;
    /**
     * Ask a remote user to open the mic
     *  @param targetId User ID
     */
    adminRequestUserOpenMic(targetId: string): Promise<void>;
    /**
     * Close a remote user's mic
     * @param targetId User ID
     */
    adminCloseUserMic(targetId: string): Promise<void>;
    /**
     * Remove a remote user from the room
     * @param targetId User ID
     * @param joinDisabled Whether the user is prevented from entering the meeting again
     */
    adminKickUserOut(targetId: string, joinDisabled: boolean): Promise<void>;
    /**
     * The host responds to a raise-hand request, approving or declining it
     *  @param targetId User ID
     *  @param approve Whether to approve
     *  @param code Raise-hand type
     */
    adminConfirmHandup(targetId: string, approve: boolean, code: HandupType): Promise<void>;
    /**
     * The host invites devices to the meeting
     * @param agents Devices to invite
     * @param no Room number
    */
    adminInviteAgent(agents: {
        type: AgentType;
        contact: string;
    }[], no: string): Promise<void>;
    /**
     * Update the invitees
     * @param conferee Invitees
    */
    adminUpdateConferee(conferee: string[]): Promise<void>;
    /**
     * Update the layout of a composite-mode meeting
     */
    adminUpdateLayout(layoutData: LayoutData): Promise<void>;
    /**
     * Device list
     * @param type Device type
     * @param name Name
     * @param page Page number
     * @param perPage Items per page
     */
    agentList(type: AgentType[], name: string, page: number, perPage: number): Promise<{
        data: AgentInfo[];
        _meta: MetaRes;
    }>;
    /**
     * Start recording
     * @param req Recording parameters
     */
    mcuStart(req: McuStartReq): Promise<void>;
    /**
     * Stop recording
     */
    mcuStop(): Promise<void>;
    /**
     * Get the recording configuration
     */
    mcuRecordConfig(): Promise<McuRecordConfig>;
    /**
     * Get the recording details
     */
    mcuRecordDetail(): Promise<McuRecordDetail>;

    enterRoom(req: MeetingEnterReq): Promise<void>;
    /**
     * Open the camera
     *
     * When publish is false, it only captures and previews in container (device checks, settings page preview): it doesn't ask the meeting
     * for permission, doesn't publish, and doesn't fire camera state events; it works before and during a meeting. Calling it again later with
     * publish: true "promotes" this track: it asks the meeting for permission and publishes the same track without restarting capture. If the camera
     * is already open as the meeting camera, calling it with publish: false just returns the track in use (only adding the preview container).
     * Always close with closeCamera; to remove only the preview container you added, use track.removePlayView(container).
     * A camera opened before entering a meeting is published when you call it again after entering.
     * @param container Preview container
     * @param deviceId Camera device ID
     * @param preset Camera preset
     * @param byAdmin Whether this is a host operation
     * @param adminUid Host ID (which host made the request)
     * @param publish Whether to open it as the meeting camera and publish it, default true; false only captures for a preview (since 0.3.5)
     */
    requestOpenCamera(container: HTMLElement, deviceId?: string, preset?: CameraPreset, byAdmin?: boolean, adminUid?: string, publish?: boolean): Promise<LocalCameraTrack>;
    /**
     * Switch the camera
     * @param deviceId Camera device ID; on mobile, omit it to toggle between front and rear cameras; on desktop, you can specify a camera
     */
    switchCamera(deviceId?: string): Promise<void>;
    /**
     * Open the mic
     *
     * When publish is false, it only captures (device checks, testing the mic during a meeting): it doesn't ask the meeting for permission,
     * doesn't publish, and doesn't fire mic state events; it works before and during a meeting. Read the volume with getVolume() on the returned track;
     * processors set with setAudioProcessor are attached as well. Calling it again later with publish: true "promotes" this track (asks the meeting
     * for permission and publishes the same track without restarting capture); if the mic is already open as the meeting mic, calling it with
     * publish: false just returns the track in use. Always close with closeMic. A mic opened before entering a meeting is published when you call it
     * again after entering.
     * @param deviceId Mic device ID
     * @param preset Mic preset
     * @param byAdmin Whether this is a host operation
     * @param adminUid Host ID (which host made the request)
     * @param publish Whether to open it as the meeting mic and publish it, default true; false only captures (since 0.3.5)
     * @returns The local mic track (since 0.3.5)
     */
    requestOpenMic(deviceId?: string, preset?: MicPreset, byAdmin?: boolean, adminUid?: string, publish?: boolean): Promise<LocalMicTrack>;
    /**
     * Switch the mic
     * @param deviceId Mic device ID
     */
    switchMic(deviceId: string): Promise<void>;
    /**
     * Set the microphone audio processor (such as `DeepFilterNetProcessor` from the AI noise suppression plugin `@seastart/srtc-plugin-deepfilternet`).
     * Pass `undefined` to clear it. Pass an array to chain processors in order. Available since 0.3.4, Web only.
     *
     * Can be called before or after entering a meeting: if the mic is on, the processor is attached immediately (replacing the old one);
     * after that it is attached every time the mic opens and detached when the mic closes, and the setting persists after leaving the meeting.
     * The processor is destroyed when the mic closes and initialized again when it opens, so the same instance can be reused.
     * A failure to attach when the mic opens doesn't block the mic; only a warning is logged. See the "AI noise suppression" advanced guide.
     * @param processor Audio processor; `undefined` clears it
     */
    setAudioProcessor(processor?: AudioTrackProcessor | AudioTrackProcessor[]): Promise<void>;
    /**
     * Start sharing
     * @param shareType Sharing type
     * @param container Preview container
     */
    requestShare(shareType?: ShareType, preset?: ScreenPreset, container?: HTMLElement): Promise<void>;
    /**
     * Stop sharing
     */
    stopShare(): Promise<void>;
    /**
     * Start playing a remote user's video
     * @param container Playback container
     * @param uid Remote user ID
     * @param trackDesc Video track description
     * @returns
     */
    startPlayRemoteVideo(container: HTMLElement, uid: string, trackDesc: TrackDesc): Promise<RemoteVideoTrack>;
    /**
     * Stop playing a remote user's video
     * @param container Playback container
     * @param uid Remote user ID
     * @param trackDesc Video track description
     */
    stopPlayRemoteVideo(container: HTMLElement, uid: string, trackDesc: TrackDesc): Promise<void>;
    /**
     * Subscribe to a remote stream
     * @param uid Remote user ID
     * @param trackDesc Video track description
     * @returns
     */
    subscribeRemoteVideoTrack(uid: string, trackDesc: TrackDesc): Promise<RemoteVideoTrack>;
    /**
     * Unsubscribe from a remote stream
     * @param uid Remote user ID
     * @param trackDesc Video track description
     */
    unsubscribeRemoteVideoTrack(uid: string, trackDesc: TrackDesc): Promise<void>;
    /**
     * Toggle mute/unmute of remote audio (a device can be specified)
     * @param mute Whether to mute
     * @param opt Speaker options
     */
    toggleRemoteAudioMute(mute: boolean, opt?: AudioOutputOptions): Promise<void>;
    /**
     * Subscribes to the remote audio mix (everyone in the meeting except you, mixed into one track) without playing it; useful for local recording.
     * There is only one mix per meeting: if it is already playing, the same track is returned and nothing is subscribed twice. Don't unsubscribe it yourself (since 0.3.7)
     */
    subscribeRemoteAudioMixTrack(): Promise<RemoteAudioMixTrack>;
    /**
     * Start playing the remote composite video
     * @param container Playback container
     * @returns
     */
    startPlayRemoteVideoMcu(container: HTMLElement): Promise<RemoteVideoTrack>;
    /**
     * Stop playing the remote composite video
     * @param container Playback container
     */
    stopPlayRemoteVideoMcu(container: HTMLElement): Promise<void>;
    /**
     * Get info about the web runtime environment, such as whether WebRTC is supported
     * @returns
     */
    getEnvInfo(): EnvWebInfo;
    /**
     * Get the device list
     * @param kind
     * @param requestPermissions
     * @returns
     */
    getDevices(kind?: MediaDeviceKind, requestPermissions?: boolean): Promise<MediaDeviceInfo[]>;
    /**
     * Whether the camera is open as the meeting camera (requestOpenCamera defaults to publish: true).
     * During a preview-only publish: false, the camera is capturing but this returns false; use it to decide whether to call closeCamera when closing the preview (since 0.3.5)
     */
    isCameraOpened(): boolean;
    /**
     * Whether the mic is open as the meeting mic (requestOpenMic defaults to publish: true); same meaning as isCameraOpened (since 0.3.5)
     */
    isMicOpened(): boolean;
    /**
     * Gets the local mic track, e.g. to read the capture volume with getVolume() or get the underlying MediaStreamTrack; undefined when the mic is off
     */
    getLocalMicTrack(): LocalMicTrack | undefined;
    /**
     * Gets the local camera track (including a publish: false preview); undefined when the camera is off (since 0.3.7)
     */
    getLocalCameraTrack(): LocalCameraTrack | undefined;
    /**
     * Gets the local screen-share track; undefined when not sharing the screen (since 0.3.7)
     */
    getLocalScreenTrack(): LocalScreenTrack | undefined;
    /**
     * Whether transcription (captions) is on in the current meeting (since 0.3.6)
     */
    isAsrEnabled(): boolean;
    /**
     * The host turns on transcription. All members get ROOM_ASR_STATE_CHANGED; captions arrive via ASR_RESULT / ASR_TRANSLATION (since 0.3.6)
     * @param translateLang Target language for live translation (e.g. en / zh); omit to transcribe only
     * @returns The transcription session id
     */
    adminAsrStart(translateLang?: string): Promise<{ session_id: string }>;
    /**
     * The host turns off transcription. If minutes are enabled for the app, they are generated next and AI_SUMMARY_READY fires when done (since 0.3.6)
     */
    adminAsrStop(): Promise<void>;
    /**
     * Gets the meeting's transcription sessions and minutes (also after the meeting), sorted by start time (since 0.3.6)
     * @param meetingId Meeting id; defaults to the current meeting
     */
    aiSummary(meetingId?: string): Promise<MeetingAiSummary[]>;
    /**
     * Gets the meeting's raw transcript (also after the meeting), grouped by session with sentences sorted by begin_ms (since 0.3.6)
     * @param meetingId Meeting id; defaults to the current meeting
     * @param sessionId Transcription session id; omit for all sessions
     */
    aiTranscript(meetingId?: string, sessionId?: string): Promise<MeetingAiTranscript[]>;
    /**
     * The host (re)generates minutes for a transcription session; AI_SUMMARY_READY fires when done (since 0.3.6)
     * @param sessionId Transcription session id, from aiSummary
     * @param meetingId Meeting id; defaults to the current meeting
     * @param templateId Minutes template id; defaults to the app's template
     */
    adminAiSummaryGenerate(sessionId: string, meetingId?: string, templateId?: string): Promise<void>;
```
