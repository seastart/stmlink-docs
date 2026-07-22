---
title: "快速开始"
description: "全平台 C++ SRTC 音视频 SDK 快速集成，10 分钟跑通基础功能"
---

### 初始化SDK
```cpp
RTC::RTCClientOptions opts;
opts.app_id = "AppId";
opts.token = "token";
opts.domain = "服务端地址";
opts.terminal_type = RTC::TerminalType::EmbeddedDev;
opts.terminal_desc = "嵌入式demo";

RTC_CreateEngine(&opts, &rtcEngine);
rtcEngine->setEventHandler(this);  //设置事件接收接口
```

[Token获取方法](https://www.yuque.com/anyconf/rtcengine/xnpez8#AXrXV)

### 登录
收到RTCEvents.Login之后才是成功登录

```typescript
//user是一个json格式的字符串
//uid 在token中已经签名
std::string user="\
{
    \"name\":\"会议中显示的名字\",\
    \"avatar\":\"用户头像地址\"\
}\
"

//sdk内部的文本都以utf8处理，输入和输出时都需要转换。
std::string utf8User = StringUtil::Gb2312ToUtf8(user);

//登录
rtcEngine->login(utf8User.c_str(), utf8User.size());

//需要收到onLogin事件之后才是登录成功
```

### 加入房间
```typescript

//UserRole.Default-普通用户
//UserRole.Audience-听众用户,听众不会显示在别人的成员列表里
rtcEngine->joinRoom('自定义房间id',UserRole.Default)



//需要onRoom事件之后才是登录成功

```

### 开始推视频流
```typescript


rtcEngine->createLocalVideoStream(2/*轨道号*/, 0/*轨道自定义type*/, RTC::CodecType::H264, 1280, 720, 25, 1024000, 0, &localVideo);

//开始推流
localVideo->publish();

//输入一帧h264流
localVideo->input();

//停止推流
localVide->unpublish();

//销毁对象
localVideo->close();
```

### 开始推音频流
```typescript
rtcEngine->createLocalAudioStream(RTC::CodecType::OPUS, 48000, 2, &localAudio);

//开始推流
localAudio->publish();

//输入一帧编码后的音频流
localAudio->input();

//停止推流
localAudio->unpublish();

//销毁对象
localAudio->close();
```

### 订阅远端视频
```typescript
//创建用户id=1的远端流
rtcEngine->createRemoteVideoStream("1",&remoteVideo);

//设置收流回调函数  RTC::FrameEvent
remoteVideo->setFrameEvent(onFrameEvent, ctx);

//开始订阅
//mask是多个轨道的掩码
//sync:true表示同步，不管对方是否有i帧都切换；false表示异步，如果目标轨道没有i帧则会切换失败
remoteVideo->subscribe(mask,sync);

//取消订阅这个用户的所有流
remoteVideo->unsubscribe();

//销毁对象
remoteVideo->close();

```

### 收全局音频流
```typescript
rtcEngine->createRemoteMixAudioStream(&remoteAudio);

//设置收流回调函数  RTC::FrameEvent
remoteAudio->setFrameEvent(onFrameEvent, ctx);

//开始订阅
remoteAudio->subscribe();

//取消订阅
remoteAudio->unsubscribe();

//销毁对象
remoteAudio->close();

```

### 退出房间
```typescript
//退出房间前必须销毁所有打开的流
localVideo->close();
localAudio->close();
remoteVideo->close()
remoteAudio->close();

//退出房间
rtcEngine->leaveRoom()
```

### 退出登录
可以不调用leaveRoom而直接调用logout，但必须先手动销毁自己打开的流。

```typescript

rtcEngine->logout()

```

### 销毁对象
可以不调用leaveRoom和logout而直接调用release释放，但必须先手动销毁自己打开的流。

```typescript

rtcEngine->release();
rtcEngine=nullptr;

//release之后rtcEngine指针将不可用

```

