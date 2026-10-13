---
title: "C# 快速开始"
description: "Windows SRTC C# 封装（srtcNet）快速集成：初始化引擎、加入频道、发布本地音视频、订阅并渲染远端画面、屏幕共享。"
---

`srtcNet` 的调用顺序和 C++ 一致，只是换成了惯用的 C# 写法：事件是 `event`，
轨道返回强类型对象，频道/引擎实现 `IDisposable`。先分清楚两层对象：

+ `SrtcEngine` —— 进程级，一个就够。创建/退出频道、设备枚举、IM、日志上传
+ `SrtcChannel` —— 一个频道一个对象，成员查询、轨道、推拉流、本地录制都在它上面

### 初始化 SDK

```csharp
using Srtc;

SrtcEngine.SetLanguage("zh-CN");                       // 可选：错误文案语言
using var engine = SrtcEngine.Init(new SrtcEngineOptions { EnableLog = 1 });
if (engine == null)
{
    return;      // 初始化失败（环境/权限问题）
}
Console.WriteLine(SrtcEngine.Version());               // 例：0.2.1-alpha.14
```

`EnableLog = 0`（或传 `null`）会关掉 SDK 文件日志。初始化失败时 `Init` 返回 `null`，
可配合 `engine.LastErrorMessage` 排查。

### 注册引擎级事件

```csharp
engine.DeviceChanged += (s, e) => Console.WriteLine($"{e.Type} {e.Action} {e.Name}");
```

这里只有**不属于任何频道**的回调：设备变化、默认设备变化、网络探测、IM。
其余回调都在 `SrtcChannel` 上。

### 加入频道

分两步：`CreateChannel` 只创建对象**不入会**，配置好之后再 `Join()`。
和 C++ 一样，**事件必须在 `Join()` 之前订阅** —— `Joined` 是在 `Join()` 还没返回时同步触发的。

```csharp
var channel = engine.CreateChannel(token);             // token 由你的后端签发
if (channel == null)
{
    return;      // token 无效 / 解码失败
}

// 事件必须在 Join 之前接好，否则会漏掉加入瞬间的事件
channel.Joined += (s, e) =>
{
    // e.ChannelJson / MeJson / MembersJson / OptionsJson 均为原始 JSON
    Console.WriteLine("已加入 " + channel.ChannelId);
};
channel.UserJoined    += (s, e) => Console.WriteLine("用户加入 " + e.UserJson);
channel.UserStreamAdded += (s, e) => Console.WriteLine($"{e.Uid} 发布流 {e.StreamJson}");
channel.CustomMessage += (s, e) => Console.WriteLine($"[{e.Action}] {e.SenderId}: {e.Message}");

// 频道级配置（stream_model / simple / mcu_track / enable_audio_record 在 Join 阶段读取）
channel.Setting.StreamModel = (int)SrtcStreamModel.Normal;

SrtcStatusCode st = channel.Join();
if (st != SrtcStatusCode.Ok)
{
    Console.WriteLine("join 失败 " + st + " " + engine.LastErrorMessage);
    return;
}
```

<Note>
`UserStreamAdded` **只覆盖加入之后新发布的轨道**。比自己先进频道的人，要在 `Joined` 的
`MembersJson` 里遍历其 `stream_tracks` 主动补订阅。
</Note>

### 打开摄像头并发布

```csharp
var cam = channel.GetCameraTrack("camera");
if (cam == null) return;

SrtcStatusCode st = cam.StartCapture(new SrtcCameraCaptureOptions
{
    Width = 640, Height = -1, MaxFps = -1
});
if (st != SrtcStatusCode.Ok) return;

st = channel.Publish(cam, new SrtcVideoPublishOptions
{
    Desc = "camera_big", MaxFps = 25,
    Simucast = new[] { new SrtcVideoPublishOptions { Desc = "camera_small", Width = 320, Height = 180, MaxFps = 15, MaxBitrate = 128 } }
});
```

<Warning>
本地轨道**先 `StartCapture` 再 `Publish`**，顺序不能反。`Publish` 有视频/音频两个重载，
要发布音频请传 `SrtcAudioPublishOptions`。
</Warning>

### 打开麦克风并发布

```csharp
var mic = channel.GetAudioTrack("mic");
mic.StartCapture(new SrtcMicCaptureOptions());          // 默认 48kHz 单声道
channel.Publish(mic, new SrtcAudioPublishOptions { Desc = "mic", Codec = (int)SrtcStreamCodec.Opus });
```

### 播放频道混音（听到所有人）

远端音频用**空 uid、空 trackId** 取频道级混音，`StartPlay` 之后即可听到所有人，无需单独订阅：

```csharp
var speaker = channel.GetRemoteAudioTrack("", "");
speaker.StartPlay(new SrtcAudioOutputOptions());         // 传 null 表示用默认扬声器
```

### 播放远端视频

```csharp
var remote = channel.GetRemoteVideoTrack(uid, trackId);  // uid / trackId 来自流事件
if (remote == null) return;

SrtcStatusCode st = remote.AddPlayView(new SrtcHwndView(hwnd));   // hwnd 为渲染控件的窗口句柄
if (st == SrtcStatusCode.Ok)
{
    channel.Subscribe(remote);                           // 订阅是显式的，必须自己调
}

// 取消时：先摘视图，再退订
remote.RemovePlayView(view);
channel.Unsubscribe(remote);
```

<Note>
窗口渲染用现成的 `SrtcHwndView(句柄)`；要渲染到自己的表面就从 `SrtcView` 派生并重写
`MakeCurrent`（`GetViewType` 返回 `SrtcViewType.CallBack`）。`SrtcView` 析构前**必须先从所有轨道
`RemovePlayView`**，否则渲染线程可能访问已释放对象。
</Note>

### 共享屏幕

```csharp
var screen = channel.GetScreenTrack("screen");
screen.AddScreenAudio(true);                             // 是否带系统声音

var cap = new SrtcScreenCaptureOptions { MaxFps = 10, ShowCursor = true };
cap.DeviceId = windowHwnd;                               // 窗口共享：句柄；显示器共享：填 X/Y/Width/Height
// cap.X = x; cap.Y = y; cap.Width = w; cap.Height = h;

screen.StartCapture(cap);
channel.Publish(screen, new SrtcVideoPublishOptions { Desc = "screen", Width = 1920, Height = 1080, MaxFps = 10, MaxBitrate = 2000 });
```

屏幕枚举 `EnumScreen()` 里 `Type == 5` 是显示器、`Type == 0` 是窗口。窗口共享把 `DeviceId`
设为 `Hwnd`；显示器共享设置 `X/Y/Width/Height` 矩形。

### 退出频道

```csharp
channel.Dispose();          // 若还想复用 engine，只销毁频道
engine.Dispose();           // 或释放引擎，连带所有频道
```

<Warning>
`SrtcChannel.Dispose()` 之后它交出的**所有轨道引用立即作废**（远端/自定义轨道在原生侧就被删了）。
退出时先把视图从轨道上摘掉（`RemovePlayView`），再销毁频道，最后释放视图对象。
</Warning>

### 订阅与线程

+ 除 `Joined`（在 `Join()` 内、调用线程上同步触发）外，**其余事件都来自 SDK 内部线程**，
  界面更新请自行 marshal（WinForms 用 `BeginInvoke`）到 UI 线程
+ `SrtcEngine.Init` 内部会让原生在 STA 线程初始化，因此从普通 .NET 线程（默认 MTA）调用也能成功
+ 常用强类型事件参数：`SrtcUserStreamEventArgs`（`Uid` / `StreamJson`）、
  `SrtcJoinedEventArgs`（`ChannelJson` / `MeJson` / `MembersJson` / `OptionsJson`）、
  `SrtcCustomMessageEventArgs`（`Action` / `SenderId` / `Name` / `Message`）

更完整的可运行示例见 WinForms Demo（九宫格布局，含设备选择、翻页、IM）。
