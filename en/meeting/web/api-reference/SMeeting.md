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
     * Pre-call network check: call it before entering a meeting, without entering; no parameters needed when logged in (since 0.3.8)
     * The check is done by the SRTC layer and passed through; the meeting layer adds a sub-check meeting_api (whether the meeting API is reachable) to the server item
     * @param options When not logged in, pass appId + serverUrl, or token; see "Pre-call network check" below
     * @returns The check result, always 5 items in a fixed order
     */
    networkCheck(options?: MeetingNetworkCheckOptions): Promise<NetworkCheckResult>;
    /**
     * Cancels the network check in progress; networkCheck then ends with the SRTC-layer 106026 (Cancelled). No-op when no check is running (since 0.3.8)
     */
    cancelNetworkCheck(): void;
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
     * @param resKey Resource key (for chat files, the key in the message)
     * @param id Resource ID (not supported by the server yet; pass resKey)
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
    /**
     * Whether simultaneous interpretation is on in the current meeting (since 0.3.9)
     */
    isInterpEnabled(): boolean;
    /**
     * The host / co-host turns on simultaneous interpretation; transcription is turned on first automatically if it isn't on. All members then get ROOM_INTERP_STATE_CHANGED,
     * translations and interpretation audio arrive via ASR_TRANSLATION (lang, audio_url), and the built-in player automatically plays interpretation audio in "my language" (since 0.3.9)
     * @returns The transcription session id, and the volume the speaker's original voice is lowered to while interpretation audio plays (0–1)
     */
    startInterp(): Promise<{ session_id: string, duck_volume: number }>;
    /**
     * The host / co-host turns off simultaneous interpretation; transcription continues (since 0.3.9)
     */
    stopInterp(): Promise<void>;
    /**
     * Sets my interpretation language: which language my speech is recognized in, and which language others' speech is translated into for me.
     * Can be set even when interpretation is off, taking effect once it's on; all members then get USER_INTERP_LANG_CHANGED (since 0.3.9)
     * @param lang Language code, such as zh / en (codes with a region like zh-CN are treated as zh); an empty string resets to the default language
     */
    setMyInterpLang(lang: string): Promise<void>;
    /**
     * My interpretation language; the meeting's default language (zh by default) if never set; an empty string when not in a meeting (since 0.3.9)
     */
    getMyInterpLang(): string;
    /**
     * A member's effective interpretation language; the meeting's default language (zh by default) if never set (since 0.3.9)
     * @param uid Member user id
     */
    getUserInterpLang(uid: string): string;
    /**
     * Refreshes and returns the interpretation state and member language table from the server. The SDK already fetches it once after entering and maintains it incrementally from messages, so you usually don't need to call it (since 0.3.9)
     */
    getInterpLangs(): Promise<InterpLangs>;
    /**
     * Listen to the original only: when on, no interpretation audio plays (any playing audio stops immediately); captions are unaffected. A user preference, kept after exiting the meeting (since 0.3.9)
     * @param listenOriginal true to listen to the original only, false to listen to interpretation audio in my language
     */
    setInterpListenOriginal(listenOriginal: boolean): void;
    /**
     * Whether listening to the original only (since 0.3.9)
     */
    isInterpListenOriginal(): boolean;
```

---

### Pre-call network check

Call `networkCheck` **before entering a meeting**. It doesn't require entering and doesn't use token authentication (since 0.3.8; requires `@seastart/srtc-web-sdk` 0.7.6 or later, which npm installs automatically).

All five checks (network permission, network connection, MTU, DNS resolution, server connectivity) are done by the SRTC layer and passed through as is, with the same types and the same platform limitations as [SRTC · networkCheck](/en/rtc/web/api-reference/SRTC#networkcheck) (on the Web, `permission`, `mtu`, and `dns` are always `unsupported`). The meeting layer only adds one sub-check, `meeting_api`, to the server connectivity item (`server`): whether the meeting API is reachable. For parameters and types, see [Pre-call network check types](/en/meeting/web/types#pre-call-network-check-types-since-0-3-8).

```typescript
import { SMeeting } from '@seastart/smeeting-web-sdk';

const smeeting = new SMeeting({});
// Logged in: no need to pass appId / serverUrl; the SDK uses the login info
// Not logged in: pass token (the meeting token used for login), or appId + serverUrl (the client_api in the meeting token)
const result = await smeeting.networkCheck({
  token: meetingToken,
  onItem: (item) => console.log(item.id, item.status, item.message),
});
if (result.status === 'fail') {
  const bad = result.items.find((i) => i.status === 'fail');
  showTip(bad?.message); // message is a Chinese description you can show to users directly
}
```

+ **Total duration**: the meeting API probe runs in parallel with the SRTC checks, adding no extra time; each item times out after 3 seconds by default (adjustable with `timeoutMs`). The four items from `permission` to `dns` are reported one by one as the SRTC checks progress; the `server` item is reported only after the meeting API probe also finishes
+ **How `meeting_api` is judged**: the SDK sends an unsigned request to the meeting API, and any HTTP response counts as reachable. A network error or timeout counts as unreachable; the `server` item is then `fail` with `reason` `meeting_api_unreachable`, and the overall status is recalculated. When `server` has already failed because of an SRTC sub-check (SDK API, signaling, media), the SRTC `reason` and `message` are kept
+ **Service address**: `serverUrl` is most complete as the `client_api` in the meeting token (such as `https://meet.example.com/meeting/client`). You can also use the `client_api` of the SRTC token or the service root address, but neither lets the SDK derive the meeting API address; when not logged in, `meeting_api` is `skipped` (`server_info_unavailable`). Priority: explicit parameters > `token` > login info
+ **Error codes**: an instance can run only one check at a time; calling again while one is in progress throws `106005`. When canceled by `cancelNetworkCheck()`, it throws `106026`; when `token` can't be decoded, it throws `106031`. These three are SRTC-layer codes passed through, the same as when calling SRTC directly. When not logged in and neither `appId` / `serverUrl` nor `token` is passed, it throws the meeting-layer `206001` (`NotLoggedIn`)

---

### Simultaneous interpretation

Simultaneous interpretation (since 0.3.9; requires `@seastart/srtc-web-sdk` 0.7.7 or later, which npm installs automatically) builds on meeting transcription: once the host turns it on, each finalized sentence is translated by the server into the languages of the members in the meeting and synthesized into speech, and each member hears interpretation audio in their own "my language". On the server side, first configure a profile for the app under **AI capabilities → AI services and profiles** in the admin console (a large language model is required; without speech synthesis there are only translated captions, no interpretation audio).

```typescript
import { CommonRoomEventType } from '@seastart/smeeting-web-sdk';

// Every member: set your own language (you can set it before interpretation is on)
await smeeting.setMyInterpLang('en');

// Host: turn on / off
await smeeting.startInterp();
await smeeting.stopInterp();

smeeting.onNotifyRoomEvent = (evt) => {
  switch (evt.type) {
    case CommonRoomEventType.ROOM_INTERP_STATE_CHANGED:
      // { enabled, duck_volume, err_desc }: refresh the UI state of the interpretation switch
      break;
    case CommonRoomEventType.ASR_TRANSLATION:
      // When interpretation is on, each sentence arrives once per language of the members in the meeting; show only the one in my language as captions
      if (evt.data.lang === smeeting.getMyInterpLang()) {
        showSubtitle(evt.data.uid, evt.data.trans_text);
      }
      break;
  }
};

// The user chooses "listen to the original only": no interpretation audio, captions unaffected
smeeting.setInterpListenOriginal(true);
```

+ **Automatic interpretation audio playback**: the Web SDK has a built-in interpretation player, so you don't need to handle `audio_url`. It plays only sentences whose language equals my language, that have interpretation audio, when "listen to the original only" isn't selected, and that weren't spoken by me. All speakers share one queue played in order, so two clips never overlap; when more than 4 sentences are waiting, the oldest is dropped
+ **Lowering the original voice**: while someone's interpretation audio plays, that person's original voice is lowered to `duck_volume` (from the AI profile, default 0.2, `0` is muted) and restored afterward; this only affects what you hear locally
+ **When playback stops immediately**: turning interpretation off, switching to "listen to the original only", changing my language, or exiting the meeting immediately stops the current audio, clears the queue, and restores the original voice; when a speaker exits the meeting, their queued sentences are dropped
+ **Captions vs. interpretation audio**: the audio is synthesized from the translation, and captions still come through `ASR_TRANSLATION`; when others use other languages, the same sentence arrives as multiple `ASR_TRANSLATION` events, so filter by `lang`
+ **Reconnecting**: after reconnecting, the SDK automatically refreshes the interpretation state and member language table from the server and re-emits `ROOM_INTERP_STATE_CHANGED` / `USER_INTERP_LANG_CHANGED` for anything that changed
+ **State when entering**: `isInterpEnabled()`, and `interp_enabled` / `interp_duck_volume` / `interp_langs` / `interp_default_lang` from `getRoomInfo()`; see [Types · Room info](/en/meeting/web/types#room-info)
+ **Captions but no interpretation audio**: first make sure the AI profile has speech synthesis configured; then make sure the reverse proxy at deployment allows the `/aiapi/interp-audio/` path (interpretation audio is downloaded from this path and read cross-origin by web pages), see [Internal network and public internet](/en/product/deploy/networks#what-to-prepare-at-deployment)

<Warning>
When interpretation is on, each sentence is delivered as multiple translations with different `lang` values, and older clients that don't know the `lang` field show all of them as captions. Enable this feature only after all meeting clients (Web, App, desktop) are upgraded to versions that support interpretation.
</Warning>
