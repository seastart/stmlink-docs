---
title: "Quickstart"
description: "Code snippets for the SMeeting Web SDK: create an instance, check the environment, log in, create / enter / exit / end meetings, manage camera, mic, speaker, and screen sharing, send messages, host controls, device invitations, and recording. Read this to get a basic Web meeting running."
---

### Basic concepts
+ SMeeting instance: create an instance with `new SMeeting`. Almost all APIs are exposed on this instance, and all events can be listened to through `SMeeting.onNotifyRoomEvent`. (If you want to enter multiple meetings at the same time, currently the only way is to create multiple instances.)
+ On the home page, get a meeting token (from your backend API) and call smeeting.login. Only after login succeeds can you perform further operations such as creating a meeting or entering a meeting
+ RoomInfo: the meeting information after entering a meeting with `smeeting.enterRoom`, available through `smeeting.getRoomInfo`
+ `UserInfo`: information about users in the meeting (including yourself and other remote users). Get a single user's information with `smeeting.getUserInfo(uid: string)`, or get all online users in the meeting with `smeeting.getUsersInfo(true/false)`—true returns a map, false returns an array





### Initialize the SDK and check the environment
```typescript
// Create an instance
const smeeting = new SMeeting({
  logLevel: LogLevel.DEBUG,
  logTarget: LogTarget.CONSOLE,
});

// Check environment information
const envinfo = smeeting.getEnvInfo();
console.log("environment", envinfo);
if(!envinfo.supported) {
  alert("SMeeting is not supported in this environment. Switch to the latest version of Chrome.");
} else {
  if(!envinfo.mediaDevices) {
    if(!envinfo.secure) {
      alert("This is not a secure context (https, localhost, or 127.0.0.1). Media devices such as the mic and camera cannot be accessed for audio and video capture and publishing.");
    } else {
      alert("This environment does not support accessing devices. Media devices such as the mic and camera cannot be accessed for audio and video capture and publishing.");
    }
  }
  if(!envinfo.h264Enc) {
    alert("This environment does not support H264 encoding. Publishing is unavailable.");
  }
  if(!envinfo.h264Dec) {
    alert("This environment does not support H264 decoding. Receiving streams is unavailable.");
  }
  if(!envinfo.screenshare) {
    alert("This environment does not support starting screen sharing.");
  }
} 

// Handle event callbacks
smeeting.onNotifyRoomEvent = (evt: RoomEvent) => {
  console.log('Meeting event received', evt);
  switch (evt.type) {
      // ...
  }
})
```

### Create a meeting
```typescript
const createRoom = async () => {
    // Call your backend API to get a Meet grant
  
    let token = "Meet grant token returned by your backend";
    await smeeting.login(token);
    const { room_no, meeting_id } = await smeeting.createRoom({
        title: 'Weekly project sync',      // Meeting title
        meeting_mode: MeetingMode.Normal,  // Meeting mode (required): Normal / Mix (composite) / Voice / Training
    }); // Returns the meeting number and meeting ID
}
```

### Enter a meeting
```typescript
const enterRoom = async () => {
   await smeeting.enterRoom({
        room_no: roomNo,  // Meeting number
        nickname: nickname, // Display name
    });
}
```

### Exit a meeting
```typescript
await smeeting.exitRoom()
```

### End a meeting (dismiss)
```typescript
await smeeting.adminDestroyRoom()
```

### Cancel a meeting
```typescript
await smeeting.cancelRoom(meeting_id)
```

### Get room info / user info / user list
```typescript
// Get room info
let roomInfo: RoomInfo = smeeting.getRoomInfo();
// Get a user's info
let userInfo: UserInfo = smeeting.getUserInfo(uid);
// Get the list of users in the room
let users: Record<string, UserInfo> = smeeting.getUsersInfo(true);
```

### Update the in-meeting display name
```typescript
await smeeting.updateName(name)
```

### Get the device list
```typescript
// kind: device category "audioinput" | "audiooutput" | "videoinput"
let freshDeviceList = async (kind?: MediaDeviceKind) => {
  if(!envinfo.mediaDevices) {
    return;
  }
  try {
    let devices = await smeeting.getDevices(kind);
    console.log("Got device list", devices);
    devices.forEach((device) => {
      // Later you can use deviceId to capture from a specific camera or mic, or play through a specific speaker (not supported in some environments)
      console.log(device.deviceId, device.kind, device.label);
      // Add to a select list in the UI
      // let opt = document.createElement('option');
      // opt.value = device.deviceId;
      // label can sometimes be an empty string; display label || deviceId in the UI
      // opt.text = device.label || device.deviceId;
      // select.append(opt);
    });
  } catch(err) {
    console.error("Failed to get device list", err);
  };
};
```

### Open, close, and switch the camera
```typescript
/**
 * Open the camera
 * @param container Preview container
 * @param deviceId Camera device ID
 * @param preset Camera preset
 * @param byAdmin Whether this is a host operation
 * @param adminUid Host ID (which host made the request)
 */
await smeeting.requestOpenCamera(container: HTMLElement, deviceId?: string, preset?: CameraPreset, byAdmin?: boolean, adminUid?: string)
/**
* Close the camera
*/
await smeeting.closeCamera()
 /**
 * Switch the camera
 * @param deviceId Camera device ID. On mobile, omit it to toggle between front and rear cameras; on desktop, you can specify a camera
 */
await smeeting.switchCamera(deviceId?: string)
```

### Start and stop playing a remote user's video
```typescript
/**
 * Start playing a remote user's video
 * @param container Playback container
 * @param uid Remote user ID
 * @param trackDesc Video track description
 * @returns  RemoteVideoTrack 
 */
const track:RemoteVideoTrack = await smeeting.startPlayRemoteVideo(container: HTMLElement,uid: string, trackDesc: TrackDesc)
  /**
   * Stop playing a remote user's video
   * @param container Playback container
   * @param uid Remote user ID
   * @param trackDesc Video track description
   */
await smeeting.stopPlayRemoteVideo(container: HTMLElement, uid: string, trackDesc: TrackDesc)
```

### Open, close, and switch the mic
```typescript
  /**
 * Open the mic
 * @param deviceId Mic device ID
 * @param preset Mic preset
  * @param admin_uid Host ID (which host made the request)
 */
await smeeting.requestOpenMic(deviceId?: string, preset?: MicPreset, byAdmin?: boolean, adminUid?: string)
  /**
 * Close the mic
 */
await smeeting.closeMic()
/**
 * Switch the mic
 * @param deviceId Mic device ID
 */
await smeeting.switchMic(deviceId: string)
```

### Open, close, and switch the speaker
```typescript
/**
 * Toggle mute / unmute for remote audio (a device can be specified)
 * @param mute Whether to mute
 * @param opt Speaker options
 */
await smeeting.toggleRemoteAudioMute(false,{deviceId?: string})  // Open and switch
await smeeting.toggleRemoteAudioMute(true)  // Close
```

### Request to start and stop sharing
```typescript
/**
 * Start sharing
 * @param shareType Share type
 * @param container Preview container
 */
await smeeting.requestShare(shareType: ShareType = ShareType.Screen, preset?: ScreenPreset, container?: HTMLElement)
await smeeting.stopShare()
```

### Send a chat message
```typescript
/**
     * Send a chat message, to one member or to everyone
     * @param msg_type Message type: 1 text, 2 file, 3 image, 4 voice
     * @param msg Message content
     * @param target_id Message recipient; empty means everyone in the room receives it
     */
await smeeting.sendRoomChatMessage(msg: string, target_id: string, msg_type: ChatMsgType = ChatMsgType.Text)
```

### Send a custom message
```typescript
/**
 * Send a custom message, to one member or to everyone
 * @param content Message content
 * @param target_id Message recipient; empty means everyone in the room receives it
 */
await smeeting.sendRoomCustomMessage(content: string, target_id: string)
```

### Raise and lower a hand
```typescript
enum HandupType {
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
await smeeting.requestHandup(code:HandupType)
await smeeting.cancelHandup(code:HandupType)
```

### The host asks a remote user to open the camera, or closes a remote user's camera
```typescript
    /**
     * Ask a remote user to open the camera
     * @param target_id User ID
     */
    await smeeting.adminRequestUserOpenCamera(target_id: string)
   /**
     * Close a remote user's camera
     * @param target_id User ID
     */
    await smeeting.adminCloseUserCamera(target_id: string)

```

### The host asks a remote user to open the mic, or closes a remote user's mic
```typescript
 /**
 * Ask a remote user to open the mic
 * @param targetId User ID
 */
await smeeting.adminRequestUserOpenMic(target_id: string)
/**
 * Close a remote user's mic
 * @param target_id User ID
 */
await smeeting.adminCloseUserMic(target_id: string)
```

### The host removes a remote user from the room
```typescript
 /**
     * Remove a remote user from the room
     * @param target_id User ID
     * @param join_disabled Whether to prevent the user from entering the meeting again
     */
   await smeeting.adminKickUserOut(target_id: string, join_disabled: boolean)
```

### The host updates the room's mic permission state (mute all and unmute all)
```typescript
 /**
 * Update the room's mic permission state (mute all and unmute all)
 * @param self_unmute_mic_disabled Whether to disable self-unmute
 * @param mic_disabled Whether to disable the mic
 */
await smeeting.adminUpdateRoomMicState(self_unmute_mic_disabled: boolean, mic_disabled: boolean)
```

### The host updates whether members can unmute their own mic
```typescript
/**
 * Update whether members can unmute their own mic
 * @param self_unmute_mic_disabled Whether to disable self-unmute
 */
await smeeting.adminUpdateRoomSelfUnmuteMicDisabled(self_unmute_mic_disabled: boolean)
```

### The host updates whether members can turn their own camera back on
```typescript
/**
 * Update whether members can turn their own camera back on
 * @param self_unmute_camera_disabled Whether to disable self-unmute
 */
await smeeting.adminUpdateRoomSelfUnmuteCameraDisabled(self_unmute_camera_disabled: boolean)
```

### The host updates the room's camera permission state
```typescript
/**
 * Update the room's camera permission state
 * @param self_unmute_camera_disabled Whether to disable self-unmute
 * @param camera_disabled Whether to disable the camera
 */
await smeeting.adminUpdateRoomCameraState(self_unmute_camera_disabled: boolean, camera_disabled: boolean)
```

### The host invites a device to the meeting
```typescript
 /**
   * The host invites a device to the meeting
   * @param agents Devices to invite {type: device type, contact: device identifier}
   * @param no Room number
  */
await smeeting.adminInviteAgent(agents:{ type: AgentType, contact: string }[], no: string)
```

### The host updates the invitees
```typescript
 /**
   * Update the invitees
   * @param conferee Array of invitee IDs
  */
await smeeting.adminUpdateConferee(conferee: string[])
```

### The host updates the layout of a composite-mode meeting
```typescript
 /**
 * Update the layout of a composite-mode meeting
 * @param layoutData Layout data
 */
await smeeting.adminUpdateLayout(layoutData: LayoutData)
```

### Get the device list
```typescript
 /**
 * Device list
 * @param type Device type
 * @param name Name
 * @param page Page number
 * @param perPage Items per page
 */
smeeting.agentList(type: AgentType[], name: string, page: number, perPage: number): Promise<{
      data: AgentInfo[];
      _meta: MetaRes;
  }>
```

### Recording
```typescript
/**
 * Start recording
 * @param req Recording parameters
 */
await smeeting.mcuStart(req: McuStartReq)
/**
 * Stop recording
 */
await smeeting.mcuStop()
/**
 * Get the recording configuration
 */
const mcuRecordConfig:McuRecordConfig = await smeeting.mcuRecordConfig()
/**
 * Get recording details
 */
const mcuRecordDetail:McuRecordDetail = await smeeting.mcuRecordDetail()
```

### Remote composite video
```typescript
/**
 * Start playing the remote composite video
 * @param container Playback container
 * @returns 
 */
const track:RemoteVideoTrack = await startPlayRemoteVideoMcu(container: HTMLElement)

 /**
 * Stop playing the remote composite video
 * @param container Playback container
 */
await stopPlayRemoteVideoMcu(container: HTMLElement)
```
