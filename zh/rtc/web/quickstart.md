### 基本概念
+ `SRTC`实例：通过`new SRTC`得到操作实例，绝大部分接口都通过该实例对外提供，所有事件都可通过`srtc.onNotifyChannelEvent`来监听。（如果你想同时加入多个频道，目前只能new多个实例来操作）
+ `ChannelInfo`：`srtc.join`加入频道后的频道信息（业务上可自定义props扩展属性），可通过 `srtc.getChannelInfo`获得
+ `UserInfo`：频道内用户信息(包括自己与其他远端用户)（业务上可自定义props扩展属性），可通过`srtc.getUserInfo(uid: string)`获取频道单用户信息，也可通过`srtc.getUsersInfo()`获取频道所有在线用户信息
+ `Track`：流轨道，每一路音频、每一路视频，都是一个Track，一个用户可能有多个Track

本地流轨道（可预览、可发布）包括：

本地麦克风音频轨道：`LocalMicTrack`

本地摄像头视频轨道：`LocalCameraTrack`

本地共享桌面视频轨道：`LocalScreenTrack`

本地自定义视频/音频流轨道：`LocalAudioTrack` `LocalVideoTrack`

远端流轨道（可订阅、可发布）包括：

远端频道混音流轨道：`RemoteAudioMixTrack`

远端用户音频流轨道：`RemoteAudioTrack`

远端用户视频流轨道：`RemoteVideoTrack`

+ `TrackInfo`：流轨道信息，（除desc轨道描述外，业务上还可自定义props扩展属性），归属于Track。



### 初始化SDK及环境检测
```typescript
import { CameraPresets, ChannelEvent, ChannelEventType, DisconnectEventData, LocalCameraTrack, LocalMicTrack, LocalScreenTrack, LogLevel, LogTarget, MicPresets, RemoteAudioMixTrack, RemoteVideoTrack, ScreenPresets, SRTC, TrackInfo, TrackKind, UserInfo } from '@seastart/srtc';
// 创建实例
const srtc = new SRTC({
  logLevel: LogLevel.DEBUG,
  logTarget: LogTarget.CONSOLE,
});

// 检测环境信息
const envinfo = srtc.getEnvInfo();
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
srtc.onNotifyChannelEvent = (evt: ChannelEvent) => {
  console.log('收到频道事件', evt);
  switch (evt.type) {
      // ...
  }
})
```

### 加入频道
```typescript
let join = async () => {
    // 调后台api获取加入频道token
    // api.getJoinToken
  
    let token = "后台返回的加入频道token";
    let channelInfo = await srtc.join(token);
}
```

### 获取频道信息/用户信息/用户列表
```typescript
// 获取频道信息
let channelInfo: ChannelInfo = srtc.getChannelInfo();
// 获取某用户信息
let userInfo: UserInfo = srtc.getUserInfo(uid);
// 获取频道内用户信息列表
let users: Record<string, UserInfo> = srtc.getUsersInfo(true);
```



### 获取设备列表
```typescript
// kind: 外设类别 "audioinput" | "audiooutput" | "videoinput"
let freshDeviceList = async (kind?: MediaDeviceKind) => {
  if(!envinfo.mediaDevices) {
    return;
  }
  try {
    let devices = await srtc.getDevices(kind);
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



### 监测设备插拔
```typescript
// 如果拔出的是正在使用的设备如麦克风、摄像头，sdk内部会自动尝试切换到其他设备
// 自动切换失败，会收到 ChannelEventType.TRACK_ENDED 事件，需要上层判断进行关闭
// 屏幕共享时点击浏览器的"停止共享"按钮也会收到 ChannelEventType.TRACK_ENDED

// 在onNotifyChannelEvent里
case ChannelEventType.DEVICE_ADD:
case ChannelEventType.DEVICE_REMOVE:
  freshDeviceList((evt.data as MediaDeviceInfo).kind);
  break;
case ChannelEventType.TRACK_ENDED:
  if(evt.data == localCameraTrack) {
    closeCamera();
  } else if (evt.data == localMicTrack) {
    closeMic();
  } else if (evt.data == localScreenTrack) {
    closeScreen();
  }
  break;
```

### 收全频道音频混音流
一般场景下，我们不需要单独收每一个远端用户的声音，而只用收全频道的混音流进行播放

```typescript
let remoteAudioMixTrack: RemoteAudioMixTrack | undefined;
let audioMixPlaying: boolean = false;

let playMixAudio = async (deviceId?: string) => {
  let track = remoteAudioMixTrack;
  if (!track) {
    // 订阅混音流
    track = remoteAudioMixTrack = await srtc.subscribeRemoteAudioMixTrack();
  } else {
    // 已订阅，先停止播放（可能要切换扬声器）
    track.stopPlay();
  }
  // 开始播放，可以指定扬声器deviceId（有些环境不支持指定扬声器）
  await track.startPlay({
    deviceId: deviceId
  });

  audioMixPlaying = true;
}

let stopMixAudio = async () => {
  if (!remoteAudioMixTrack) {
    throw "尚未订阅混音流";
  }
  // 停止播放
  remoteAudioMixTrack.stopPlay();
  // 如果有必要，可以取消订阅，一般不需要，只是动态切换是否播放
  // await srtc.unsubscribeRemoteTrack(remoteAudioMixTrack);
  // remoteAudioMixTrack = undefined;

  audioMixPlaying = false;
}

// 默认打开扬声器播放频道混音流
playMixAudio();

openSpeakerBtn.onclick = async() => {
  try {
    let deviceId = "选中的扬声器";
    await playMixAudio(deviceId);
    console.warn('打开扬声器(订阅混音流)成功');
  } catch (err) {
    console.error('打开扬声器(订阅混音流)失败', err);
  }
}

closeSpeakerBtn.onclick = async() => {
  await stopMixAudio();
  console.warn('关闭扬声器成功');
}
```

### 打开、关闭麦克风
```typescript
let localMicTrack: LocalMicTrack | undefined;

let openMic = async (deviceId?: string) => {
  if (localMicTrack) {
    throw "已开启麦克风";
  }
  // 可选：调后台api请求开启麦克风
  // api.openMic

  // 创建麦克风音频流轨道，可以用不同的MicPresets
  let track = localMicTrack = srtc.createLocalMicTrack(MicPresets.music);

  // 开始采集，可以指定麦克风deviceId
  await track.startCapture({
    deviceId: deviceId,
  });

  // 音频一般不需要本地播放，当然你可以用播放来做麦克风是否采到声音的测试
  // await track.startPlay();

  // 发布
  await srtc.publishLocalTrack(track);
  // 可自定义轨道描述desc以及自定义props等发布参数
  /*await srtc.publishLocalTrack(track, {
    desc: "mic",
    props: {
      "loc": "杭州",
      "label": "麦克风",
    }
  });*/
}

let closeMic = async () => {
    if (localMicTrack) {
        // 停止发布
        await srtc.unpublishLocalTrack(localMicTrack);
        // 停止采集
        await localMicTrack.stopCapture();
        // 可选：调后台api通知关闭麦克风
        // api.closeMic
    }
    localMicTrack = undefined;
}

openMicBtn.onclick = async() => {
  try {
    let deviceId = "选中的麦克风";
    await openMic(deviceId);
    console.warn('打开麦克风成功');
  } catch (err) {
    console.error('打开麦克风失败', err);
    await closeMic();
  }
}

closeMicBtn.onclick = async() => {
  try {
      await closeMic();
      console.warn('关闭麦克风成功');
  } catch (err) {
      console.error('关闭麦克风失败', err);
  }
}
```

### 打开、关闭摄像头
```typescript
let localCameraTrack: LocalCameraTrack | undefined;

let openCamera = async (deviceId?: string) => {
  if (localCameraTrack) {
    throw "已开启摄像头";
  }
  // 可选：调后台api请求开启摄像头
  // api.openCamera

  // 创建摄像头视频流轨道，可以用不同的CameraPresets
  let track = localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['720p']);

  // 开始采集，可以指定摄像头deviceId
  await track.startCapture({
    deviceId: deviceId,
  });

  // 添加到预览容器 HTMLElement
  track.addPlayView(document.querySelector('.video-ctn')!);

  // 发布
  await srtc.publishLocalTrack(track);
  // 可自定义轨道描述desc以及自定义props等发布参数
  /*await srtc.publishLocalTrack(track, {
    desc: "camera_big",
    props: {
      "label": "摄像头大流",
    },
  });*/
});


let closeCamera = async () => {
  if (localCameraTrack) {
      // 停止发布
      await srtc.unpublishLocalTrack(localCameraTrack);
      // 移除所有预览容器
      await localCameraTrack.removeAllPlayViews();
      // 停止采集
      await localCameraTrack.stopCapture();
      // 可选：调后台api通知关闭摄像头
      // api.closeCamera
  }
  localCameraTrack = undefined;
}


openCameraBtn.onclick = async() => {
  try {
    let deviceId = "选中的摄像头";
    await openCamera(deviceId);
    console.warn('打开摄像头成功');
  } catch (err) {
    console.error('打开摄像头失败', err);
    await closeCamera();
  }
}

closeCameraBtn.onclick = async() => {
  try {
      await closeCamera();
      console.warn('关闭摄像头成功');
  } catch (err) {
      console.error("关闭摄像头失败", err);
  }
}
```

### 打开、关闭桌面共享
```typescript
let localScreenTrack: LocalScreenTrack | undefined;
// 屏幕共享时点击浏览器的"停止共享"按钮会收到 ChannelEventType.TRACK_ENDED

let openScreen = async () => {
  if (localScreenTrack) {
    throw "已开启共享";
  }
  // 可选：调后台api请求开启共享
  // api.openScreen

  // 创建桌面共享流轨道，可以用不同的ScreenPresets
  let track = localScreenTrack = srtc.createLocalScreenTrack(ScreenPresets['1080p']);
  // 开始采集  
  await track.startCapture();
  // 添加到预览容器 HTMLElement
  track.addPlayView(document.querySelector('.screen-ctn')!);
  // 发布
  await srtc.publishLocalTrack(track);
  // 可自定义轨道描述desc以及自定义props等发布参数
  /*await srtc.publishLocalTrack(track, {
    desc: "screen",
    props: {
      "label": "屏幕共享",
    },
  });*/
}

let closeScreen = async () => {
  if (localScreenTrack) {
    // 停止发布
    await srtc.unpublishLocalTrack(localScreenTrack);
    // 移除所有预览容器
    await localScreenTrack.removeAllPlayViews();
    // 停止采集
    await localScreenTrack.stopCapture();
    // 可选：调后台api通知停止桌面共享
    // api.closeScreen
  }
  localScreenTrack = undefined;
}

openScreenBtn.onclick = async() => {
  try {
    await openScreen();
    console.warn('打开共享成功');
  } catch (err) {
    console.error('打开共享失败', err);
    await closeScreen();
  }
}

closeScreenBtn.onclick = async() => {
  try {
      await closeScreen();
      console.warn('关闭共享成功');
  } catch (err) {
      console.error("关闭共享失败", err);
  }
}
```

### 自定义推音频/视频流
与开麦克风和摄像头类似，只不过需自己构建`MediaStreamTrack`，然后用 `createLocalCustomAudioTrack``createLocalCustomVideoTrack` 来创建轨道

```typescript
// 自定义一个MediaStreamTrack，此track可以通过各种方式获得，如canvas.captureStream
let msTrack: MediaStreamTrack;

// 自定义音频
let track = srtc.createLocalCustomAudioTrack(msTrack);
// 发布，轨道描述desc以及自定义props
await srtc.publishLocalTrack(track, {
  desc: "自定义音频"
});

// 自定义视频
let track = srtc.createLocalCustomVideoTrack(msTrack);
// 添加到预览容器 HTMLElement
track.addPlayView(document.querySelector('.video-ctn')!);
// 发布，轨道描述desc以及自定义props
await srtc.publishLocalTrack(track, {
  desc: "自定义视频"
});

```



### 订阅/取消订阅远端视频流
```typescript
let remoteVideoTracks: Record<string, RemoteVideoTrack> = {};

// 相关频道事件
// 远端用户进入：ChannelEventType.USER_JOIN
// 远端用户退出：ChannelEventType.USER_LEAVE (sdk内部会自动取消订阅该用户所有轨道)
// 远端用户添加流轨道：ChannelEventType.USER_TRACK_ADD
// 远端用户删除流轨道：ChannelEventType.USER_TRACK_REMOVE (sdk内部会自动取消订阅该轨道)
// 远端用户信息更新事件：ChannelEventType.USER_UPDATE
// 自定义事件：ChannelEventType.CUSTOM_MSG

// 可以根据业务需要监听上述事件及实际界面需求，来订阅或取消订阅远端视频流

let subVideo = async (userinfo: UserInfo, trackinfo: TrackInfo) => {
  let id = userinfo.uid + '-' + trackinfo.id;
  if (remoteVideoTracks[id]) {
    console.warn(`已经订阅${userinfo.uid}:${trackinfo.desc}轨道`);
    return;
  }
  try {
    // 订阅
    let rtrack = await srtc.subscribeRemoteVideoTrack(userinfo.uid, trackinfo.id);
    remoteVideoTracks[id] = rtrack;
    // 添加到界面显示 HTMLElement
    rtrack.addPlayView(remote.querySelector('.video-ctn')!);
    console.warn(`订阅${userinfo.uid}:${trackinfo.desc}轨道成功`);
  } catch (err) {
    console.error(`订阅${userinfo.uid}:${trackinfo.desc}轨道失败`, err);
  }
}

let unsubVideo = async (uid: string, trackinfo: TrackInfo) => {
  let id = uid + '-' + trackinfo.id;
  if (!remoteVideoTracks[id]) {
    console.warn(`尚未订阅${uid}:${trackinfo.desc}轨道`);
    return;
  }
  try {
    let rtrack = remoteVideoTracks[id];
    // 取消订阅
    await srtc.unsubscribeRemoteTrack(rtrack);
    // 移除显示
    rtrack.removeAllPlayViews();

    delete remoteVideoTracks[id];
    console.warn(`取消订阅${uid}:${trackinfo.desc}轨道成功`);
  } catch (err) {
    console.error(`取消订阅${uid}:${trackinfo.desc}轨道失败`, err);
  }
}
```

### 监听用户进出及信息更新
```typescript
// 在onNotifyChannelEvent里
case ChannelEventType.USER_JOIN: {
  // evt.data as UserInfo
  let user = evt.data as UserInfo;
  users[user.uid] = user;
  break;
}
case ChannelEventType.USER_UPDATE: {
  // evt.data as UserInfo
  let user = evt.data as UserInfo;
  users[user.uid] = user;
  break;
}
case ChannelEventType.USER_LEAVE:
  // evt.data as UserLeaveEventData
  let leaveData = evt.data as UserLeaveEventData;
  // 如果正在订阅该用户的视频流，取消订阅
  for (const id in remoteVideoTracks) {
      let track = remoteVideoTracks[id];
      if (track.getUid() == leaveData.uid) {
          unsubVideo(uid, track.getInfo());
      }
  }
  delete users[leaveData.uid];
  break;
```

### 监听自己信息被更新
你的信息可能被后台或管理员进行强制更新

```typescript
// 在onNotifyChannelEvent里
case ChannelEventType.ME_UPDATE:
  // evt.data as UserInfo
  let user = evt.data as UserInfo;
  users[user.uid] = user;
  me = user;
  break;
```

### 开始重连/重连成功
当网络发声波动时，会触发重连开始事件，成功后会触发重连成功事件

```typescript
// 在onNotifyChannelEvent里
case ChannelEventType.RECONNECTING:
  // 开始重连
  break;
case ChannelEventType.RECONNECTED:
  // 重连成功
  break;
```

### 退出频道
退出分主动退出和被动(发生不可恢复错误时)退出

```typescript
// 主动退出
await srtc.leave();
// 界面刷新清理



// 被动退出
// 在onNotifyChannelEvent里
case ChannelEventType.DISCONNECTED:
  let data = (evt.data as DisconnectEventData);
  // 可根据reason提示退出原因
  alert('你已断开 reason:' + data.reason);
  // 界面刷新清理
  break;
```



