---
title: "ISMeetingEngine"
description: "Windows SMeeting 会议 SDK ISMeetingEngine 接口参考"
---

# ISMeetingEngine 创建
### 创建ISMeetingEngine
```cpp
//----------- c++ 语言----------
SMEETING_API StatusCode SMEETING_CALL SMeetingEngine_Init(ISMeetingEngine** meet);

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_Init_C();
```typescript

**参数**

| meet | ISMeetingEngine 对象类 |
| --- | --- |


### 获取sdk版本信息
```cpp
//----------- c++ 语言----------
SMEETING_API StatusCode SMEETING_CALL SMeetingEngine_Version(std::string& s);

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_Version_C(char* c,int len);
```

**参数**

| s | 信息返回值 |
| --- | --- |
| c | 返回内存（此函数不分配内存，需要申请内存后调用） |
| len | 内存长度 |


### 获取错误码描述信息
```cpp
//----------- c++ 语言----------
SMEETING_API void SMEETING_CALL SMeetingEngine_GetStatusMsg(StatusCode code, std::string & msg);

//----------其他语言或便捷调用----------
SMEETING_API_C void SMEETING_CALL_C SMeetingEngine_GetStatusMsg_C(StatusCodeC code, char* msg,int len);
```typescript

**参数**

| s | 信息返回值 |
| --- | --- |
| c | 返回内存（此函数不分配内存，需要申请内存后调用） |
| len | 内存长度 |


# ISMeetingEngine
## 会前接口
### 获取配置信息
```cpp
//----------- c++ 语言----------
virtual StatusCode getSetting(ISMeetingSetting** sett) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_settingStream_model(int);
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_settingSdk_log_path(const char*);
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_settingStat_interval(int);
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_settingSpeaker_interval(int);
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_settingEnable_stream_log(int);
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_settingEnable_audio_record(int);
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_settingMcu_track(int);
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_settingDen_model(int);
```

**参数**

| sett | 参数配置信息 |
| --- | --- |


### 设置回调句柄
```cpp
//----------- c++ 语言----------
virtual StatusCode setEventHandler(ISMeetingEngineEvent* e) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_setEventHandler(SMeet_CBF_RoomEvent e,void* t);
```typescript

**参数**

| e | 回调对象（错误码，错误描述&数据信息） |
| --- | --- |


### 用户登录
```cpp
//----------- c++ 语言----------
virtual StatusCode login(std::string token, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_login(const char* token);
```

**参数**

| token | token 登录信息 |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 用户登出
```cpp
//----------- c++ 语言----------
virtual StatusCode logout(Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_logout();
```cpp

**参数**

| back | 异步回调（错误码，错误描述&数据信息） |
| --- | --- |


### 获取自身信息
```cpp
//----------- c++ 语言----------
virtual StatusCode getSelf(Callback back) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_getSelf(char** out_put, int* out_put_len);
```

**参数**

| back | 异步回调（错误码，错误描述&数据信息） |
| --- | --- |


### 获取设备列表
```cpp
//----------- c++ 语言----------
virtual StatusCode listAgent(std::vector<int> type, int page,std::string find_key = "", Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_listAgent(char* types, int page,const char* find_key,char** out_put,int* out_put_len);
```typescript

**参数**

| type | 设备类型 |
| --- | --- |
| page | 页码 |
| find_key | 搜索关键词 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 更新房间信息
```cpp
//----------- c++ 语言----------
virtual StatusCode updateRoom(SMeetingCreateMeetingModel model, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_updateRoom(const char* json);
```

**参数**

| model | 房间类型结构体 |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取正在进行中的会议
```cpp
//----------- c++ 语言----------
virtual StatusCode attendeeRoom(int page, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_attendeeRoom(int page, char** out_put, int* out_put_len);
```cpp

**参数**

| page | 页码 |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取历史会议
```cpp
//----------- c++ 语言----------
virtual StatusCode attendedRoom(int page, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_attendedRoom(int page, char** out_put, int* out_put_len);
```

**参数**

| page | 页码 |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取会议信息
```cpp
//----------- c++ 语言----------
virtual StatusCode detailRoom(std::string meeting_id, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_detailRoom(const char* meeting_id, char** out_put, int* out_put_len);
```typescript

**参数**

| meeting_id | 会议id |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 取消会议
```cpp
//----------- c++ 语言----------
virtual StatusCode cancelRoom(std::string meeting_id, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_cancelRoom(const char* meeting_id, char** out_put, int* out_put_len);
```

**参数**

| meeting_id | 会议id |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取会议成员信息
```cpp
//----------- c++ 语言----------
virtual StatusCode participantRoom(std::string meeting_id, int page, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_participantRoom(const char* meeting_id,int page, char** out_put, int* out_put_len);
```typescript

**参数**

| meeting_id | 会议id |
| --- | --- |
| page | 页码 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 创建会议
```cpp
//----------- c++ 语言----------
virtual StatusCode createRoom(SMeetingCreateMeetingModel model, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_participantRoom(const char* json, char** out_put, int* out_put_len);
```

**参数**

| model | 房间类型结构体 |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 加入房间
```cpp
//----------- c++ 语言----------
virtual StatusCode enterRoom(std::string roomno, std::string name, std::string pass = "", Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_enterRoom(const char* roomno, const char* name, const char* pass);
```cpp

**参数**

| roomno | 房间号 |
| --- | --- |
| name | 会中昵称 |
| pass | 会议加入密码 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 离开会议
```cpp
//----------- c++ 语言----------
virtual StatusCode exitRoom(Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_exitRoom();
```

**参数**

| back | 异步回调（错误码，错误描述&数据信息） |
| --- | --- |


## 会中接口
### 主持人结束会议
```cpp
//----------- c++ 语言----------
virtual StatusCode adminDestroyRoom(Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminDestroyRoom();
```cpp

**参数**

| back | 异步回调（错误码，错误描述&数据信息） |
| --- | --- |


### 主持人修改房间视频状态
```cpp
//----------- c++ 语言----------
virtual StatusCode adminUpdateRoomCameraState(bool self_unmute_camera_disabled, bool camera_disabled, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomCameraState(bool self_unmute_camera_disabled, bool camera_disabled);
```

**参数**

| self_unmute_camera_disabled | 是否不允许自行打开 |
| --- | --- |
| camera_disabled | 是否禁用视频 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人修改房间音频状态
```cpp
//----------- c++ 语言----------
		virtual StatusCode adminUpdateRoomMicState(bool self_unmute_mic_disabled, bool mic_disabled, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomMicState(bool self_unmute_mic_disabled, bool mic_disabled);
```cpp

**参数**

| self_unmute_mic_disabled | 是否不允许自行打开 |
| --- | --- |
| mic_disabled | 是否禁用音频 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人修改房间聊天状态
```cpp
//----------- c++ 语言----------
virtual StatusCode adminUpdateRoomChatDisabled(bool chat_disabled, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomChatDisabled(bool chat_disabled);
```

**参数**

| mic_disabled | 是否禁用聊天 |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人修改房间共享状态
```cpp
//----------- c++ 语言----------
virtual StatusCode adminUpdateRoomScreenshotDisabled(bool screenshot_disabled, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomScreenshotDisabled(bool screenshot_disabled);
```cpp

**参数**

| screenshot_disabled | 是否禁用共享 |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人修改会议锁定
```cpp
//----------- c++ 语言----------
virtual StatusCode adminUpdateRoomLocked(bool locked, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateRoomLocked(bool locked);
```

**参数**

| locked | 是否锁定会议 |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人停止共享
```cpp
//----------- c++ 语言----------
virtual StatusCode adminStopRoomShare(Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminStopRoomShare();
```typescript

**参数**

| back | 异步回调（错误码，错误描述&数据信息） |
| --- | --- |


### 主持人更新用户昵称
```cpp
//----------- c++ 语言----------
virtual StatusCode adminUpdateUserName(std::string uid, std::string name, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人关闭用户视频
```cpp
//----------- c++ 语言----------
virtual StatusCode adminCloseUserCamera(std::string uid, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminCloseUserCamera(const char* uid);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人关闭用户音频
```cpp
//----------- c++ 语言----------
virtual StatusCode adminCloseUserMic(std::string uid, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminCloseUserMic(const char* uid);
```

**参数**

| uid | 用户id |
| --- | --- |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人请求用户打开视频
```cpp
//----------- c++ 语言----------
virtual StatusCode adminRequestUserOpenCamera(std::string uid, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminRequestUserOpenCamera(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人请求用户打开音频
```cpp
//----------- c++ 语言----------
virtual StatusCode adminRequestUserOpenMic(std::string uid, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人踢出成员
```cpp
//----------- c++ 语言----------
virtual StatusCode adminKickUserOut(std::string uid, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人邀请设备入会
```cpp
//----------- c++ 语言----------
virtual StatusCode adminInviteAgent(std::string no ,int tp,std::vector<std::string> devs, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人更新会议成员
```cpp
//----------- c++ 语言----------
virtual StatusCode adminUpdateConferee(std::vector<std::string> conferee, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 主持人更新会议MCU布局
```cpp
//----------- c++ 语言----------
virtual StatusCode adminUpdateLayout(std::string layout, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 修改自身昵称
```cpp
//----------- c++ 语言----------
virtual StatusCode updateName(std::string name, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 发送聊天消息
```cpp
//----------- c++ 语言----------
virtual StatusCode sendRoomChatMessage(int tp,std::string msg, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 发送房间自定义消息
```cpp
//----------- c++ 语言----------
virtual StatusCode sendRoomCustomMessage(std::string, std::string, Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 开启远端录制
```cpp
//----------- c++ 语言----------
virtual StatusCode mcuStart(std::string laydata,Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 关闭远端录制
```cpp
//----------- c++ 语言----------
virtual StatusCode mcuStop(Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 查询录制配置
```cpp
//----------- c++ 语言----------
virtual StatusCode mcuRecordConfig(Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 查询录制详情
```cpp
//----------- c++ 语言----------
virtual StatusCode mcuRecordDetail(Callback back = NULL) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取会中自身信息
```cpp
//----------- c++ 语言----------
virtual StatusCode getMe(std::string& s) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取房间信息
```cpp
//----------- c++ 语言----------
virtual StatusCode getRoom(std::string& s) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取房间所有成员信息
```cpp
//----------- c++ 语言----------
virtual StatusCode getMembers(std::string& s) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |




### 获取指定成员信息
```cpp
//----------- c++ 语言----------
virtual StatusCode getMember(std::string uid, std::string& s) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取扩展信息
```cpp
//----------- c++ 语言----------
virtual StatusCode getOpt(std::string& opt) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取视频设备信息
```cpp
//----------- c++ 语言----------
virtual StatusCode getEnumVideo(std::string& dev) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取屏幕设备信息
```cpp
//----------- c++ 语言----------
virtual StatusCode getEnumScreen(std::string& dev) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取音频设备信息
```cpp
//----------- c++ 语言----------
virtual StatusCode getEnumAudio(std::string& dev) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取扬声器设备信息
```cpp
//----------- c++ 语言----------
virtual StatusCode getEnumSpeaker(std::string& dev) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取本地音频推流对象
```cpp
//----------- c++ 语言----------
virtual StatusCode getLocalMic(IMEETLocalMic**) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取本地视频推流对象
```cpp
//----------- c++ 语言----------
virtual StatusCode getLocalCamera(IMEETLocalCamera**) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取本地共享流推流对象
```cpp
//----------- c++ 语言----------
virtual StatusCode getLocalScreen(IMEETLocalScreen**) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取远端流对象
```cpp
//----------- c++ 语言----------
virtual StatusCode getRemoteVideo(std::string uid,std::string track_desc, IMEETRemoteVideo**) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取远端音频对象
```cpp
//----------- c++ 语言----------
virtual StatusCode getRemoteAudio(std::string uid, IMEETRemoteAudio**) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```typescript

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 获取远端合成流对象
```cpp
//----------- c++ 语言----------
virtual StatusCode getMcuVideo(IMEETRemoteVideo**) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 添加日志信息
```cpp
//----------- c++ 语言----------
virtual StatusCode addUploadLog(const char* type, const char* msg) = 0;

//----------其他语言或便捷调用----------
SMEETING_API_C StatusCodeC SMEETING_CALL_C SMeetingEngine_adminUpdateUserName(const char* uid, const char* name);
```cpp

**参数**

| uid | 用户id |
| --- | --- |
| name | 昵称 |
| back | 异步回调（错误码，错误描述&数据信息） |


### 
