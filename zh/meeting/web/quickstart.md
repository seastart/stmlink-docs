---
title: "快速开始"
description: "Web SMeeting 会议 SDK 快速集成，10 分钟跑通基础功能"
---

### 基本概念
+ SMeeting实例：通过`new SMeeting`得到操作实例，绝大部分接口都通过该实例对外提供，所有事件都可通过`SMeeting.onNotifyRoomEvent`来监听。（如果你想同时加入多个频道，目前只能new多个实例来操作）
+ 首页需要获取meeting的token（从后端接口中获取），调用smeeting.login登录成功后才能进行后续的操作如创建会议、加入会议等操作
+ RoomInfo：`smeeting.enterRoom`加入会议后的会议信息，可通过 `smeeting.getRoomInfo`获得
+ `UserInfo`：会议内用户信息(包括自己与其他远端用户)，可通过`smeeting.getUserInfo(uid: string)`获取会议单用户信息，也可通过`smeeting.getUsersInfo(true/false)`获取频道所有在线用户信息 true获取map数据   false获取array数据





### 初始化SDK及环境检测
```typescript
// 创建实例
const smeeting = new SMeeting({
  logLevel: LogLevel.DEBUG,
  logTarget: LogTarget.CONSOLE,
});

// 检测环境信息
const envinfo = smeeting.getEnvInfo();
console.log("environment", envinfo);
if(!envinfo.supported) {
  alert("当前环境不支持SRTC，建议切换到最新chrome浏览器");
} else {
  if(!envinfo.mediaDevices) {
    if(!envinfo.secure) {
      alert("当前非安全环境(https或localhost或127.0.0.1)，将无法获取麦克风、摄像头等媒体设备进行音视频采集、推流");
    } else {
      alert("当前环境不支持获取外设，将无法获取麦克风、摄像头等媒体设备进行音视频采集、推流");
    }
  }
  if(!envinfo.h264Enc) {
    alert("当前环境不支持H264编码，将无法推流");
  }
  if(!envinfo.h264Dec) {
    alert("当前环境不支持H264解码，将无法收流");
  }
  if(!envinfo.screenshare) {
    alert("当前环境不支持发起屏幕共享");
  }
} 

// 回调事件响应
smeeting.onNotifyRoomEvent = (evt: RoomEvent) => {
  console.log('收到会议事件', evt);
  switch (evt.type) {
      // ...
  }
})
```

### 创建会议
```typescript
const createRoom = async () => {
    // 调后台api获取Meet授权
  
    let token = "后台返回的Meet授权token";
    await smeeting.login(token);
    const roomNo = await smeeting.createRoom({
        title: 'shu的会议',  // 会议名称
    }); // 获取到会议号
}
```

### 加入会议
```typescript
const enterRoom = async () => {
   await smeeting.enterRoom({
        room_no: roomNo,  // 会议号
        nickname: nickname, // 昵称
    });
}
```

### 退出会议
```typescript
await smeeting.exitRoom()
```

### 结束会议（解散）
```typescript
await smeeting.adminDestroyRoom()
```

### 取消会议
```typescript
await smeeting.value.cancelRoom(meeting_id)
```

### 获取房间信息/用户信息/用户列表
```typescript
// 获取房间信息
let roomInfo: RoomInfo = smeeting.getRoomInfo();
// 获取某用户信息
let userInfo: UserInfo = smeeting.getUserInfo(uid);
// 获取房间内用户信息列表
let users: Record<string, UserInfo> = smeeting.getUsersInfo(true);
```

### 更新会中昵称
```typescript
await smeeting.updateName(name)
```

### 获取设备列表
```typescript
// kind: 外设类别 "audioinput" | "audiooutput" | "videoinput"
let freshDeviceList = async (kind?: MediaDeviceKind) => {
  if(!envinfo.mediaDevices) {
    return;
  }
  try {
    let devices = await smeeting.getDevices(kind);
    console.log("获取设备列表成功", devices);
    devices.forEach((device) => {
      // 后续可以用deviceId来进行指定摄像头采集、麦克风采集、扬声器放声(有些环境不支持)
      console.log(device.deviceId, device.kind, device.label);
      // 添加到界面select选择列表
      // let opt = document.createElement('option');
      // opt.value = device.deviceId;
      // 有时候label可能为空字串，界面显示可以用 label || deviceId
      // opt.text = device.label || device.deviceId;
      // select.append(opt);
    });
  } catch(err) {
    console.error("获取设备列表失败", err);
  };
};
```

### 打开、关闭、切换摄像头
```typescript
/**
 * 打开摄像头
 * @param container 预览容器
 * @param deviceId 摄像头设备id
 * @param preset 摄像头预设值
 * @param byAdmin 是否主持人操作
 * @param adminUid 主持人id（哪个主持人请求打开）
 */
await smeeting.requestOpenCamera(container: HTMLElement, deviceId?: string, preset?: CameraPreset, byAdmin?: boolean, adminUid?: string)
/**
* 关闭摄像头
*/
await smeeting.closeCamera()
 /**
 * 切换摄像头
 * @param deviceId 摄像头设备id，手机端不传自动切换前后置摄像头，桌面端可指定摄像头
 */
await smeeting.switchCamera(deviceId?: string)
```

### 开始、停止播放远端用户视频
```typescript
/**
 * 开始播放远端用户视频
 * @param container 播放容器
 * @param uid 远程用户id
 * @param trackDesc 视频轨道描述
 * @returns  RemoteVideoTrack 
 */
const track:RemoteVideoTrack = await smeeting.startPlayRemoteVideo(container: HTMLElement,uid: string, trackDesc: TrackDesc)
  /**
   * 停止播放远端用户视频
   * @param container 播放容器
   * @param uid 远端用户id
   * @param trackDesc 视频轨道描述
   */
await smeeting.stopPlayRemoteVideo(container: HTMLElement, uid: string, trackDesc: TrackDesc)
```

### 打开、关闭、切换麦克风
```typescript
  /**
 * 打开麦克风
 * @param deviceId 麦克风设备id
 * @param preset 麦克风预设值
  * @param admin_uid 主持人id（哪个主持人请求打开）
 */
await smeeting.requestOpenMic(deviceId?: string, preset?: MicPreset, byAdmin?: boolean, adminUid?: string)
  /**
 * 关闭麦克风
 */
await smeeting.closeMic()
/**
 * 切换麦克风
 * @param deviceId 麦克风设备id
 */
await smeeting.switchMic(deviceId: string)
```

### 打开、关闭、切换扬声器
```typescript
/**
 * 切换远程音频的静音/取消静音状态(可以指定设备)
 * @param mute 是否静音
 * @param opt 扬声器配置
 */
await smeeting.toggleRemoteAudioMute(false,{deviceId?: string})  // 打开和切换
await smeeting.toggleRemoteAudioMute(true)  // 关闭
```

### 请求打开、关闭共享
```typescript
/**
 * 打开共享
 * @param shareType 共享类型
 * @param container 预览容器
 */
await smeeting.requestShare(shareType: ShareType = ShareType.Screen, preset?: ScreenPreset, container?: HTMLElement)
await smeeting.stopShare()
```

### 发送聊天消息
```typescript
/**
     * 发送聊天消息，可单发和群发
     * @param msg_type 消息类型 1文本  2文件 3图片 4语音
     * @param msg 消息内容
     * @param target_id 消息接收者 为空时表示全房间接收
     */
await smeeting.sendRoomChatMessage(msg: string, target_id: string, msg_type: ChatMsgType = ChatMsgType.Text)
```

### 发送自定义消息
```typescript
/**
 * 发送自定义消息，可单发和群发
 * @param content 消息内容
 * @param target_id 消息接收者 为空时表示全房间接收
 */
await smeeting.sendRoomCustomMessage(content: string, target_id: string)
```

### 举手、取消举手
```typescript
enum HandupType {
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
await smeeting.requestHandup(code:HandupType)
await smeeting.cancelHandup(code:HandupType)
```

### 主持人请求远端用户打开摄像头、 关闭远端用户摄像头
```typescript
    /**
     * 请求远端用户打开摄像头
     * @param target_id 用户id
     */
    await smeeting.adminRequestUserOpenCamera(target_id: string)
   /**
     * 关闭远端用户摄像头
     * @param target_id 用户id
     */
    await smeeting.adminCloseUserCamera(target_id: string)

```

### 主持人请求远端用户打开麦克风、关闭远端用户麦克风
```typescript
 /**
 * 请求远端用户打开麦克风
 * @param targetId 用户id
 */
await smeeting.adminRequestUserOpenMic(target_id: string)
/**
 * 关闭远端用户麦克风
 * @param target_id 用户id
 */
await smeeting.adminCloseUserMic(target_id: string)
```

### 主持人将远端用户踢出房间
```typescript
 /**
     * 将远端用户踢出房间
     * @param target_id 用户id
     * @param join_disabled 是否禁止再入会
     */
   await smeeting.adminKickUserOut(target_id: string, join_disabled: boolean)
```

### 主持人更新房间麦克风使用权限禁用状态(全体禁音和全体解除禁音)
```typescript
 /**
 * 更新房间麦克风使用权限禁用状态(全体禁音和全体解除禁音)
 * @param self_unmute_mic_disabled 是否禁用自我解除
 * @param mic_disabled 是否禁用麦克风
 */
await smeeting.adminUpdateRoomMicState(self_unmute_mic_disabled: boolean, mic_disabled: boolean)
```

### 主持人更新房间麦克风允许自我解除
```typescript
/**
 * 更新房间麦克风允许自我解除
 * @param self_unmute_mic_disabled 是否禁用自我解除
 */
await smeeting.adminUpdateRoomSelfUnmuteMicDisabled(self_unmute_mic_disabled: boolean)
```

### 主持人更新房间摄像头允许自我解除
```typescript
/**
 * 更新房间摄像头允许自我解除
 * @param self_unmute_camera_disabled 是否禁用自我解除
 */
await smeeting.adminUpdateRoomSelfUnmuteCameraDisabled(self_unmute_camera_disabled: boolean)
```

### 主持人更新房间摄像头使用权限禁用状态
```typescript
/**
 * 更新房间摄像头使用权限禁用状态
 * @param self_unmute_camera_disabled 是否禁用自我解除
 * @param camera_disabled 是否禁用摄像头
 */
await smeeting.adminUpdateRoomCameraState(self_unmute_camera_disabled: boolean, camera_disabled: boolean)
```

### 主持人邀请设备入会
```typescript
 /**
   * 主持人邀请设备入会
   * @param agents 邀请的设备 {type: 设备类型，contact: 设备标识}
   * @param no 房间号
  */
await smeeting.adminInviteAgent(agents:{ type: AgentType, contact: string }[], no: string)
```

### 主持人修改参会人员
```typescript
 /**
   * 修改参会人员
   * @param conferee 参会人员id集合
  */
await smeeting.adminUpdateConferee(conferee: string[])
```

### 主持人修改合成会议的布局
```typescript
 /**
 * 修改合成会议的布局
 * @param layoutData 布局数据
 */
await smeeting.adminUpdateLayout(layoutData: LayoutData)
```

### 获取设备列表
```typescript
 /**
 * 设备列表
 * @param type 设备类型
 * @param name 名称
 * @param page 页码
 * @param perPage 每页数量
 */
smeeting.agentList(type: AgentType[], name: string, page: number, perPage: number): Promise<{
      data: AgentInfo[];
      _meta: MetaRes;
  }>
```

### 录制相关
```typescript
/**
 * 开始录制
 * @param req 录制参数
 */
await smeeting.mcuStart(req: McuStartReq)
/**
 * 停止录制
 */
await smeeting.mcuStop()
/**
 * 获取录制配置
 */
const mcuRecordConfig:McuRecordConfig = await smeeting.mcuRecordConfig()
/**
 * 获取录制详情
 */
const mcuRecordDetail:McuRecordDetail = await smeeting.mcuRecordDetail()
```

### 远端合成视频
```typescript
/**
 * 开始播放远端合成视频
 * @param container 播放容器
 * @returns 
 */
const track:RemoteVideoTrack = await startPlayRemoteVideoMcu(container: HTMLElement)

 /**
 * 停止播放远端合成视频
 * @param container 播放容器
 */
await stopPlayRemoteVideoMcu(container: HTMLElement)
```

