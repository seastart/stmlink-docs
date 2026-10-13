---
title: "C# Quickstart"
description: "Get started with the Windows SRTC C# wrapper (srtcNet): initialize the engine, join a channel, publish local audio and video, subscribe to and render remote video, and share the screen."
---

`srtcNet` follows the same call order as C++, just in idiomatic C#: events are `event`s, tracks are
returned as strongly typed objects, and the engine/channel implement `IDisposable`. There are two layers:

+ `SrtcEngine`—process-wide, one is enough. Creates and leaves channels, enumerates devices, IM, log upload
+ `SrtcChannel`—one per meeting: member queries, tracks, publishing/subscribing, local recording

### Initialize the SDK

```csharp
using Srtc;

SrtcEngine.SetLanguage("en");                          // optional: language of error texts
using var engine = SrtcEngine.Init(new SrtcEngineOptions { EnableLog = 1 });
if (engine == null)
{
    return;      // initialization failed (environment/permissions)
}
Console.WriteLine(SrtcEngine.Version());               // e.g. 0.2.1-alpha.14
```

`EnableLog = 0` (or passing `null`) turns the SDK file log off. `Init` returns `null` on failure;
read `engine.LastErrorMessage` to diagnose.

### Register engine-level events

```csharp
engine.DeviceChanged += (s, e) => Console.WriteLine($"{e.Type} {e.Action} {e.Name}");
```

Only callbacks that **belong to no channel** live here: device changes, default device changes,
network probe, IM. Everything else is on `SrtcChannel`.

### Join a channel

Two steps: `CreateChannel` only creates the object **without joining**; configure it, then call `Join()`.
As in C++, **register the events before `Join()`**—`Joined` fires synchronously while `Join()` is
still running.

```csharp
var channel = engine.CreateChannel(token);             // token issued by your backend
if (channel == null)
{
    return;      // invalid token / decryption failed
}

// Handlers must be in place before Join(), or early events are lost
channel.Joined += (s, e) =>
{
    // e.ChannelJson / MeJson / MembersJson / OptionsJson are raw JSON
    Console.WriteLine("joined " + channel.ChannelId);
};
channel.UserJoined    += (s, e) => Console.WriteLine("user joined " + e.UserJson);
channel.UserStreamAdded += (s, e) => Console.WriteLine($"{e.Uid} published {e.StreamJson}");
channel.CustomMessage += (s, e) => Console.WriteLine($"[{e.Action}] {e.SenderId}: {e.Message}");

// Per-channel settings (stream_model / simple / mcu_track / enable_audio_record are read during Join)
channel.Setting.StreamModel = (int)SrtcStreamModel.Normal;

SrtcStatusCode st = channel.Join();
if (st != SrtcStatusCode.Ok)
{
    Console.WriteLine("join failed " + st + " " + engine.LastErrorMessage);
    return;
}
```

<Note>
`UserStreamAdded` **only covers tracks published after you joined**. For users who were already
publishing, walk their `stream_tracks` in the `Joined` event's `MembersJson` and subscribe explicitly.
</Note>

### Open the camera and publish

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
Local tracks must be `StartCapture`d **before** `Publish`; the order matters. `Publish` has a video
and an audio overload—pass `SrtcAudioPublishOptions` to publish audio.
</Warning>

### Open the microphone and publish

```csharp
var mic = channel.GetAudioTrack("mic");
mic.StartCapture(new SrtcMicCaptureOptions());          // 48 kHz mono by default
channel.Publish(mic, new SrtcAudioPublishOptions { Desc = "mic", Codec = (int)SrtcStreamCodec.Opus });
```

### Play the channel audio mix (hear everyone)

Remote audio is fetched with an **empty uid and track id** to get the channel-wide mix. After
`StartPlay` you hear everyone, with no explicit subscribe:

```csharp
var speaker = channel.GetRemoteAudioTrack("", "");
speaker.StartPlay(new SrtcAudioOutputOptions());         // null selects the default speaker
```

### Render remote video

```csharp
var remote = channel.GetRemoteVideoTrack(uid, trackId);  // uid / trackId come from the stream events
if (remote == null) return;

SrtcStatusCode st = remote.AddPlayView(new SrtcHwndView(hwnd));   // hwnd of your render control
if (st == SrtcStatusCode.Ok)
{
    channel.Subscribe(remote);                           // subscription is explicit
}

// To stop: detach the view first, then unsubscribe
remote.RemovePlayView(view);
channel.Unsubscribe(remote);
```

<Note>
For window rendering use the built-in `SrtcHwndView(handle)`. To render into your own surface, derive
from `SrtcView` and override `MakeCurrent` (`GetViewType` returns `SrtcViewType.CallBack`). A `SrtcView`
**must be removed from every track** (`RemovePlayView`) before it is disposed, or the render thread may
touch a freed object.
</Note>

### Screen sharing

```csharp
var screen = channel.GetScreenTrack("screen");
screen.AddScreenAudio(true);                             // include system audio

var cap = new SrtcScreenCaptureOptions { MaxFps = 10, ShowCursor = true };
cap.DeviceId = windowHwnd;                               // window capture: handle; monitor capture: set X/Y/Width/Height
// cap.X = x; cap.Y = y; cap.Width = w; cap.Height = h;

screen.StartCapture(cap);
channel.Publish(screen, new SrtcVideoPublishOptions { Desc = "screen", Width = 1920, Height = 1080, MaxFps = 10, MaxBitrate = 2000 });
```

In `EnumScreen()`, `Type == 5` is a monitor and `Type == 0` is a window. For window capture set
`DeviceId` to the `Hwnd`; for monitor capture set the `X/Y/Width/Height` rectangle.

### Leave the channel

```csharp
channel.Dispose();          // destroy just the channel, keep the engine
engine.Dispose();           // or dispose the engine, taking all channels with it
```

<Warning>
After `SrtcChannel.Dispose()` **every track it handed out is immediately invalid** (remote and custom
tracks are deleted natively). On exit, detach views from tracks (`RemovePlayView`) first, then dispose
the channel, then release the view objects.
</Warning>

### Events and threading

+ Except for `Joined` (raised synchronously on the calling thread inside `Join()`), **all events arrive
  on SDK internal threads**—marshal to your UI thread yourself (e.g. WinForms `BeginInvoke`)
+ `SrtcEngine.Init` makes the native side initialize on an STA thread, so calling it from an ordinary
  .NET thread (MTA by default) also works
+ Common strongly typed event args: `SrtcUserStreamEventArgs` (`Uid` / `StreamJson`),
  `SrtcJoinedEventArgs` (`ChannelJson` / `MeJson` / `MembersJson` / `OptionsJson`),
  `SrtcCustomMessageEventArgs` (`Action` / `SenderId` / `Name` / `Message`)

For a complete runnable example see the WinForms demo (3x3 grid with device pickers, paging, and IM).
