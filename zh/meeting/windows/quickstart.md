---
title: "快速开始"
description: "Windows SMeeting 会议 SDK 快速集成，10 分钟跑通基础功能"
---

### 基本概念
+ ISMeetingEngine：是提供SMeeting 的基础功能虚函数，可以通过设置setEventHandler 绑定回调监听。通过getSetting 来设置基本设置的修改。
+ 部分接口只允许在进入会议后调用。





### 初始化SDK及环境检测
```typescript
//----------- c++ 语言----------
SMeeting::ISMeetingEngine* _imeet;
SMeeting::StatusCode ret = SMeeting::SMeetingEngine_Init(&_imeet);
if (ret != SMeeting::StatusCode::OK) {
  return ret;
}
_imeet->setEventHandler(this);//当前类集成ISMeetingEngineEvent

//-----------其他语言----------
SMeetingEngine_Init_C();
SMeetingEngine_setEventHandler(RoomEvent,this);

//回调函数
int RoomEvent(int iEvent, void* pEventData, int iDataSize, void* pContext)
{
  switch(iEvent){
    
  }
}
```typescript

### 登录登出
```typescript
//----------- c++ 语言----------
SMeeting::StatusCode sc = _imeet->login(token.toStdString(),
                      [&](SMeeting::StatusCode Status, std::string msg) {
            qDebug() << tr("登录结果：") << (int)Status;
    });

SMeeting::StatusCode sc = _imeet->logout(
                      [&](SMeeting::StatusCode Status, std::string msg) {
            qDebug() << tr("登出结果：") << (int)Status;
    });

//-----------其他语言----------
SMeeting::StatusCode sc = SMeetingEngine_login(token);
qDebug() << tr("登录结果：") << (int)Status;

SMeeting::StatusCode sc = SMeetingEngine_logout();
qDebug() << tr("登出结果：") << (int)Status;

```

### 创建会议
```typescript
//----------- c++ 语言----------
SMeeting::SMeetingCreateMeetingModel m;
m.title = title.toStdString();
SMeeting::StatusCode sc = _imeet->createRoom(m, [&](SMeeting::StatusCode Status, std::string msg) {
      qDebug() << tr("会议创建结果：") << (int)Status<<tr("会议号：")<<msg.c_str();
    });

//-----------其他语言----------
std::string json = "{\"title\":\"123\"}";//更多参数参考SMeetingCreateMeetingModel
char* outdata = nullptr;
int outlen = 0;
SMeeting::StatusCode sc = SMeetingEngine_createRoom(json,&outdata,&outlen);
qDebug() << tr("会议创建结果：") << (int)Status<<tr("会议号：")<<outdata;
```typescript

### 加入会议
```typescript
//----------- c++ 语言----------
SMeeting::ISMeetingSetting* setting = nullptr;
_imeet->getSetting(&setting);
if (setting)
{
  setting->set_stream_model(STREAM_MODEL);//设置流媒体模式
  setting->set_speaker_interval(500);//设置音柱信息回调周期
  setting->set_stat_interval(10000); //设置网络信息回调周期
  setting->set_enable_audio_record(sdkInfo.StreamRecordAudioEnable);//设置存储录音文件
  setting->set_enable_stream_log(sdkInfo.StreamLogEnable);//设置存储流媒体日志文件
}

auto sc = _imeet->enterRoom(roomno.toStdString(), name.toStdString(), pass.toStdString(),
  [&](SMeeting::StatusCode Status, std::string msg) {
      qDebug() << tr("进入房间结果：") << (int)Status;
  });

//-----------其他语言----------
SMeetingEngine_settingStream_model(500);//设置流媒体模式
auto sc = SMeetingEngine_enterRoom(roomno,name,pass);
qDebug() << tr("进入房间结果：") << (int)sc;
```

### 退出会议
```typescript
//----------- c++ 语言----------
_imeet->exitRoom([&](SMeeting::StatusCode Status, std::string msg) {

});

//-----------其他语言----------
SMeetingEngine_exitRoom();
```cpp

### 结束会议（解散）
```typescript
//----------- c++ 语言----------
_imeet->adminDestroyRoom();

//-----------其他语言----------
SMeetingEngine_adminDestroyRoom();
```

### 取消会议
```typescript
//----------- c++ 语言----------
_imeet->cancelRoom(id.toStdString());

//-----------其他语言----------
SMeetingEngine_cancelRoom(id);
```typescript

### 获取房间信息/用户信息/用户列表
```typescript
//----------- c++ 语言----------
std::string s;
_imeet->getMe(s);				//获取自身信息
_imeet->getRoom(s);			//获取房间信息
_imeet->getMembers(s);	//获取所有成员信息
_imeet->getMember(uid.toStdString(), s);//获取指定成员信息

//-----------其他语言----------
char* out;
int len;
SMeetingEngine_getMe(&out,&len);
SMeetingEngine_getRoom(&out,&len);
SMeetingEngine_getMembers(&out,&len);
SMeetingEngine_getMember(uid,&out,&len);
```

### 更新会中昵称
```typescript
//----------- c++ 语言----------
_imeet->updateName(nname.toStdString(), [&](SMeeting::StatusCode Status, std::string msg) {
    qDebug() << tr("昵称修改：")<<(int)Status;
    });

//-----------其他语言----------
auto sc = SMeetingEngine_updateName(nname);
qDebug() << tr("昵称修改：")<<(int)sc;
```typescript

### 获取设备列表
```typescript
//----------- c++ 语言----------
std::vector<int> li = {2,3};
int page = 1;
_imeet->listAgent(li,page, find.toStdString(), [&,find](SMeeting::StatusCode Status, std::string msg) {
        qDebug() << tr("设备获取：") << (int)Status << tr("获取结果：")<<msg.c_str();
        });

//-----------其他语言----------
char* out;
int len;
const char* li = "2|3";
int page = 1;
auto sc = SMeetingEngine_listAgent(li,page,&out,&len);
qDebug() << tr("设备获取：") << (int)Status << tr("获取结果：")<<out;
```

### 打开、关闭、切换摄像头
```typescript
//----------- c++ 语言----------
SMeeting::IMEETLocalCamera* mc = nullptr;
SMeeting::StatusCode sc = _imeet->getLocalCamera(&mc);

mc->switchCamera(_cameraName.toLocal8Bit().data(),w,h);			//切换摄像头

mc->addPlayView(hwnd);//设置渲染窗口
mc->requestOpenCamera([&](SMeeting::StatusCode Status, std::string msg) //打开摄像头
{
    qDebug() << tr("打开设备：") << (int)Status ;
});

mc->closeCamera([&](SMeeting::StatusCode Status, std::string msg) //关闭摄像头
{
    qDebug() << tr("关闭设备设备：") << (int)Status ;
});
//-----------其他语言----------
SMeetingEngine_requestOpenCamera(hwnd);		//打开摄像头
SMeetingEngine_closeCamera();							//关闭摄像头
SMeetingEngine_switchCamera(name,w,h);		//切换摄像头
```cpp

### 开始、停止播放远端用户视频
```typescript
//----------- c++ 语言----------
SMeeting::IMEETRemoteVideo* mc = nullptr;
_imeet->getRemoteVideo(uid.toStdString(), track_desc.toStdString(),&mc);

mc->loadRemoteVideo();			//开始取流
mc->addPlayView(hwnd);			//绑定窗口
mc->unLoadRemoteVideo()			//停止取流

//-----------其他语言----------
SMeetingEngine_loadRemoteVideo(uid,track_desc,hwnd);		//开始取远端流
SMeetingEngine_unloadRemoteVideo(uid,track_desc);				//停止取远端流
```

### 打开、关闭、切换麦克风
```typescript
//----------- c++ 语言----------
SMeeting::IMEETLocalMic* mc = nullptr;
_imeet->getLocalMic(&mc);

mc->switchMic(name.toLocal8Bit().data());			//切换麦克风
mc->requestOpenMic([&](SMeeting::StatusCode Status, std::string msg) {//打开麦克风
            qDebug() << tr("打开麦克风：") << (int)Status;
            });
mc->closeMic([&](SMeeting::StatusCode Status, std::string msg) {//关闭麦克风
            qDebug() << tr("关闭麦克风：") << (int)Status;
            });

//-----------其他语言----------
SMeetingEngine_switchMic(name);			//切换麦克风
SMeetingEngine_requestOpenMic();		//打开麦克风
SMeetingEngine_closeMic();					//关闭麦克风
```cpp

### 打开、关闭、切换扬声器
```typescript
//----------- c++ 语言----------
SMeeting::IMEETRemoteAudio* mc = nullptr;
_imeet->getRemoteAudio("", &mc);

mc->switchSpeaker(name.toLocal8Bit().data());
mc->openSpeaker();
mc->closeSpeaker();

//-----------其他语言----------
SMeetingEngine_switchSpeaker(name);		//切换扬声器
SMeetingEngine_openSpeaker();					//打开扬声器
SMeetingEngine_closeMic();						//关闭扬声器
```

### 请求打开、关闭共享
```typescript
//----------- c++ 语言----------
SMeeting::IMEETLocalScreen* mc = nullptr;
_imeet->getLocalScreen(&mc);

QString s = QString("%1,%2,%3,%4").arg(rect.x()).arg(rect.y()).arg(rect.width()).arg(rect.height());
mc->requestShare(tp, s.toStdString(), [&, tp](SMeeting::StatusCode Status, std::string msg) {
            qDebug() << tr("共享结果：") << (int)Status;
            });
mc->stopShare([&, tp](SMeeting::StatusCode Status, std::string msg) {
            qDebug() << tr("结束共享：") << (int)Status;
            });

//-----------其他语言----------
SMeetingEngine_requestShare(tp,data);		//请求共享
SMeetingEngine_stopShare();							//结束共享
```typescript

### 发送聊天消息
```typescript
//----------- c++ 语言----------
_imeet->sendRoomChatMessage(1,msg.toStdString(), [&,msg](SMeeting::StatusCode Status, std::string m) {
        qDebug() << tr("发送聊天消息：") << (int)Status;
    });

//-----------其他语言----------
SMeetingEngine_sendRoomChatMessage(1,msg);		//发送聊天消息
```



### 主持人请求远端用户打开摄像头、 关闭远端用户摄像头
```typescript
 //----------- c++ 语言----------
_imeet->adminRequestUserOpenCamera(uid.toStdString(), [&](SMeeting::StatusCode Status, std::string msg) {
            qDebug() << tr("请求打开发送结果：") << (int)Status;
            });
_imeet->adminCloseUserCamera(uid.toStdString(), [&](SMeeting::StatusCode Status, std::string msg) {
            qDebug() << tr("请求关闭发送结果：") << (int)Status;
            });

//-----------其他语言----------
SMeetingEngine_adminRequestUserOpenCamera(uid);		//请求打开
SMeetingEngine_adminCloseUserCamera(uid);					//请求关闭
```typescript

### 主持人请求远端用户打开麦克风、关闭远端用户麦克风
```typescript
 //----------- c++ 语言----------
_imeet->adminRequestUserOpenMic(uid.toStdString(), [&](SMeeting::StatusCode Status, std::string msg) {
            qDebug() << tr("请求打开发送结果：") << (int)Status;
            });
_imeet->adminCloseUserMic(uid.toStdString(), [&](SMeeting::StatusCode Status, std::string msg) {
            qDebug() << tr("请求关闭发送结果：") << (int)Status;
            });

//-----------其他语言----------
SMeetingEngine_adminRequestUserOpenMic(uid);		//请求打开
SMeetingEngine_adminCloseUserMic(uid);					//请求关闭
```

### 主持人将远端用户踢出房间
```typescript
 //----------- c++ 语言----------
    _imeet->adminKickUserOut(uid.toStdString(), [&](SMeeting::StatusCode Status, std::string msg) {
        qDebug() << tr("踢出用户结果：") << (int)Status;
        });

//-----------其他语言----------
SMeetingEngine_adminKickUserOut(uid);					//踢出用户
```typescript

### 主持人更新房间麦克风使用权限禁用状态(全体禁音和全体解除禁音)
```typescript
 //----------- c++ 语言----------
bool self_unmute_mic_disabled = true;	//是否不允许自行解除
bool mic_disabled = true;							//是否房间音频禁用状态
_imeet->adminUpdateRoomMicState(v, true, [&](SMeeting::StatusCode Status, std::string msg) {
  qDebug() << tr("设置房间麦克风结果：") << (int)Status;
});

//-----------其他语言----------
SMeetingEngine_adminUpdateRoomMicState(self_unmute_mic_disabled,mic_disabled);					//设置房间麦克风
```



### 远端合成视频
```typescript
 //----------- c++ 语言----------
SMeeting::IMEETRemoteVideo* mc = nullptr;
_imeet->getMcuVideo(&mc);

mc->loadRemoteVideo();			//取流
mc->addPlayView(hwnd);			//添加渲染
mc->unLoadRemoteVideo();		//停止取流
//-----------其他语言----------
SMeetingEngine_loadMcuVideo(hwnd);					//获取合成流
SMeetingEngine_unloadMcuVideo();					  //停止获取合成流
```cpp

