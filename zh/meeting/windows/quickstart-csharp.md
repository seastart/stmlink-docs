---
title: "C# 快速开始"
sidebarTitle: "C#"
description: "Windows SMeeting C# 封装（SMeetingNet）的 10 分钟最小可跑流程：初始化 SMeetingEngine、登录、创建与进入会议、开关摄像头与麦克风、播放频道混音、渲染远端画面、屏幕共享、聊天与退出。"
---

`SMeetingNet` 把 `SMeeting.h` 的 C++ 接口包装成惯用的 C# 写法：回调变成 `event`，媒体变成强类型对象，
`SMeetingEngine` / `SMeetingChannel` 可以 `Dispose`，不需要自己写回调 vtable。

调用顺序与 [C++ 快速开始](/zh/meeting/windows/quickstart) 完全一致，先分清楚两层对象：

+ `SMeetingEngine` —— 进程级，一个就够。登录、会议管理 HTTP 接口、频道生命周期、设备枚举、IM、资源盘
+ `SMeetingChannel` —— 一个会议一个对象，入会、房间与成员数据、会中操作、媒体对象都在它上面

### 初始化 SDK

```csharp
using SMeetingNet;

SMeetingEngine.SetLanguage("zh-CN");              // 可选：错误文案语言（BCP 47）
var engine = SMeetingEngine.Init();
if (engine == null)
{
    return;      // 初始化失败
}
Console.WriteLine(SMeetingEngine.Version());      // 例：1.0.0-alpha.9

// 引擎级配置必须在 Login 之前设置——底层 rtc 引擎是在 Login 里建的
engine.Setting.EnableStreamLog = 1;
engine.Setting.SdkLogPath = @"D:\log\";
```

`SetLanguage` / `Version` / `GetStatusMessage` 都是静态方法，不必先有 engine 实例。
状态码文案用 `SMeetingEngine.GetStatusMessage(code)` 取，语言跟随 `SetLanguage`（未设置时为英文）。

### 注册引擎级事件

```csharp
engine.DeviceChanged += (s, e) => Console.WriteLine($"{e.Type} add={e.IsAdd} {e.Name}");
```

这里只有**不属于任何会议**的回调：设备变化、默认设备变化、网络探测、IM、会议开始提醒（`MeetingStartMessage`）。
会议内的回调都在 `SMeetingChannel` 上。

### 登录

```csharp
SMeetingStatusCode st = engine.Login(token, (code, data) =>
{
    if (code == SMeetingStatusCode.Ok)
    {
        // data 为后端返回的 json
    }
});
```

`Login` 是异步的，结果只能从回调里拿。

### 创建会议

```csharp
var model = new SMeetingCreateMeetingModel
{
    Title = "我的会议",
    Content = "会议说明",
    MeetingType = 1,   // 1 临时会议，2 预约会议
    MeetingMode = 1,   // 1 普通
};

engine.CreateRoom(model, (code, data) =>
{
    if (code == SMeetingStatusCode.Ok)
    {
        // data 为会议号
    }
});
```

已有会议号或房间号时，直接跳到下一步。

### 加入会议

分两步：`CreateChannel` **只创建对象、不入会**，配置好之后再 `Enter()`。
和 C++ 一样，**事件必须在 `Enter()` 之前订阅** —— 入会过程中的回调是在 `enter` 还没返回时就同步触发的。

```csharp
SMeetingChannel channel = engine.CreateChannel(roomNo);   // 也可是 CreateChannelByMeetingId(meetingId)
if (channel == null)
{
    return;      // roomNo 无效
}

// 事件必须在 Enter 之前接好
channel.Disconnected          += (s, e) => Console.WriteLine($"连接断开 {e.Reason} {e.Code} {e.Message}");
channel.Reconnected           += (s, e) => Console.WriteLine("连接已恢复");
channel.Reconnecting          += (s, e) => Console.WriteLine("连接重连中");
channel.UserEntered           += (s, e) => Console.WriteLine("用户进入 " + e.UserData);   // 成员 json
channel.UserExited            += (s, e) => Console.WriteLine("用户离开 " + e.UserData);
channel.UserCameraStateChanged += (s, e) => Console.WriteLine($"{e.Uid} 摄像头 {e.NewState}");

// 频道级配置：stream_model / mcu_track / enable_audio_record 只在 Enter 阶段读取
SMeetingChannelSetting setting = channel.Setting;
setting.StreamModel = 1;             // 流媒体模式
setting.SpeakerInterval = 500;       // 音柱回调周期 (ms)
setting.StatInterval = 10000;        // 网络统计回调周期 (ms)
setting.RoomName = "张三";            // 入会昵称
setting.StreamVendor = "seastart";   // 后端要求的 vendor 串

st = channel.Enter(pass, (code, data) =>
{
    if (code != SMeetingStatusCode.Ok)
    {
        engine.LeaveChannel(channel);   // 入会失败的频道对象也要回收
        return;
    }
    Console.WriteLine("已进入 " + channel.ChannelId);
});
```

<Warning>
`RoomName`（入会昵称）与 `StreamVendor` 都要在 `Enter()` 之前设置。
入会失败时 `channel` 对象依然存在，必须用 `engine.LeaveChannel(channel)` 回收。
</Warning>

### 获取房间与成员信息

```csharp
string me      = channel.GetMeJson();          // 本端成员 json
string room    = channel.GetRoomJson();        // 房间 json
string members = channel.GetMembersJson();     // 成员 json 数组
string member  = channel.GetMemberJson(uid);   // 指定成员 json
```

<Note>
这几个接口返回的都是**原始 json**，schema 由后端定义，需要你自己解析（每个成员的已发布轨道在
`stream_tracks` 字段里，含 `desc` / `kind` / `width` / `height` / `fps`）。
</Note>

### 摄像头

```csharp
SMeetingLocalCamera camera = channel.GetLocalCamera();
if (camera == null) return;

camera.AddPlayView(new SMeetingHwndView(hwnd));        // hwnd 为渲染控件的窗口句柄
camera.SwitchCamera("Integrated Camera", 640, 480);    // 可选：切换设备与分辨率
camera.RequestOpenCamera((code, data) => { /* 打开结果 */ });
```

```csharp
camera.RemoveAllPlayView();
camera.CloseCamera((code, data) => { /* 关闭结果 */ });
```

### 麦克风

```csharp
SMeetingLocalMic mic = channel.GetLocalMic();
if (mic == null) return;

mic.SwitchMic("Default Microphone");    // 可选；传 "default" 表示系统默认设备
mic.RequestOpenMic((code, data) => { /* 打开结果 */ });
```

```csharp
mic.CloseMic((code, data) => { /* 关闭结果 */ });
```

### 扬声器（听到所有人）

远端音频**传空 uid** 取的是频道混音，打开后即可听到所有人，无需逐个订阅：

```csharp
SMeetingRemoteAudio speaker = channel.GetRemoteAudio(string.Empty);
if (speaker == null) return;

speaker.SwitchSpeaker("Default Speakers");     // 可选；传 "default" 表示系统默认设备
speaker.OpenSpeaker();
```

```csharp
speaker.CloseSpeaker();
```

### 播放远端视频

```csharp
// uid / desc 来自成员 json 的 stream_tracks：摄像头是 camera_big / camera_small，屏幕共享是 screen
SMeetingRemoteVideo remote = channel.GetRemoteVideo(uid, "camera_big");
if (remote == null) return;

remote.AddPlayView(new SMeetingHwndView(hwnd));
SMeetingStatusCode rst = remote.LoadRemoteVideo();      // 订阅并拉流
```

```csharp
remote.RemovePlayView(view);
remote.UnloadRemoteVideo();
```

<Warning>
远端轨道**不是**可以长期持有的句柄：成员离开后 SDK 会销毁对应对象，届时再按同一个
`(uid, desc)` 取会得到 `null`。所以不要缓存 `SMeetingRemoteVideo`，每次使用都重新 `GetRemoteVideo`。
本地摄像头 / 屏幕共享对象相反，在频道存活期间可以一直持有。
</Warning>

<Note>
窗口渲染直接用现成的 `SMeetingHwndView(句柄)`；要渲染到自己的表面就从 `SMeetingView` 派生并重写
`UpdatePlanes`（`GetViewType` 返回 `SMeetingViewType.CallBack`）。`SMeetingView` 析构前**务必先
`RemovePlayView`**，否则渲染线程可能访问已释放对象。
</Note>

### 屏幕共享

```csharp
SMeetingLocalScreen screen = channel.GetLocalScreen();
if (screen == null) return;

screen.AddScreenAudio(true);                        // 是否带系统声音

// tp: 1 屏幕共享，2 窗口共享
// data: 显示器共享传 "x,y,width,height"；窗口共享传 "hwnd:句柄"
screen.RequestShare(1, "0,0,1920,1080", (code, data) => { /* 共享结果 */ });
```

```csharp
screen.StopShare((code, data) => { /* 停止结果 */ });
```

可共享的目标用 `engine.EnumScreen()` 枚举：`Type == 5` 是显示器（取 `X` / `Y` / `Width` / `Height` 拼矩形），
`Type == 0` 是窗口（取 `Hwnd`）。

### 聊天与自定义消息

```csharp
// 公开聊天：tp 1 文本，2 文件，3 图片，4 声音
channel.SendRoomChatMessage(1, "大家好！", (code, data) => { });

// 点对点自定义消息：注意顺序是「目标 id 在前、内容在后」
channel.SendRoomCustomMessage(targetUid, "{\"cmd\":1}", (code, data) => { });
```

收到的消息在 `RoomChatMessage` / `RoomCustomMessage` 事件里。

### 主持人操作

```csharp
channel.AdminRequestUserOpenCamera(uid, (code, data) => { });
channel.AdminCloseUserCamera(uid, (code, data) => { });
channel.AdminRequestUserOpenMic(uid, (code, data) => { });
channel.AdminCloseUserMic(uid, (code, data) => { });
channel.AdminKickUserOut(uid, (code, data) => { });
channel.AdminDestroyRoom((code, data) => { });          // 结束（解散）会议
```

### 本地录制

```csharp
SMeetingRecord record = channel.GetLocalRecord();   // 每个频道只有一个录制对象
if (record == null) return;

record.SetRecordFileName(@"C:\record\meeting.mp4");
record.SetWaterMask("会议录制");
record.SetRecordHwnd(hwnd, 0, 0, 0, 0);
record.Start();

// record.Pause();
// record.Stop();
```

### 退出与释放

```csharp
engine.LeaveChannel(channel);   // 销毁该频道，它借出的媒体对象立即失效
channel = null;                 // 对象已销毁，必须自己置空

// 或者一次退掉全部频道
engine.LeaveAllChannels();

engine.Dispose();               // 释放引擎
```

### 线程与生命周期

+ **除入会过程中的事件外，所有事件都在 SDK 内部线程触发**，界面更新请自己 marshal
  （WinForms 用 `BeginInvoke`）到 UI 线程
+ 带 `SMeetingCallback` 的异步接口（`Login` / `Enter` / `RequestOpenCamera` 等）回调只触发**一次**，
  参数是 `(SMeetingStatusCode code, string data)`
+ 媒体对象都是**频道借出的句柄**：只在频道存活期间有效，退出频道后一律不要再使用
+ `SMeetingNet.dll` 是 C++/CLI 混合模式程序集，位数必须与 `bin` 及工程目标平台一致，见[集成](/zh/meeting/windows/integration)

更完整的可运行示例见 WinForms Demo（九宫格布局，含设备选择、翻页、共享与聊天）。
