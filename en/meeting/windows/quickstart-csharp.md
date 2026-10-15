---
title: "C# Quickstart"
sidebarTitle: "C#"
description: "The minimal Windows SMeeting C# flow with the SMeetingNet wrapper in about 10 minutes: initialize SMeetingEngine, log in, create and enter a meeting, control the camera and microphone, play the channel audio mix, render remote video, share the screen, chat, and leave."
---

`SMeetingNet` wraps the `SMeeting.h` C++ API in idiomatic C#: callbacks become `event`s, media becomes
strongly typed objects, and `SMeetingEngine` / `SMeetingChannel` implement `IDisposable`, so you never
write callback vtables yourself.

The call order is identical to the [C++ quickstart](/en/meeting/windows/quickstart). There are two layers:

+ `SMeetingEngine`—process-wide, one is enough. Login, the meeting management HTTP APIs, channel lifecycle, device enumeration, IM, resource drive
+ `SMeetingChannel`—one per meeting: entering, room and member data, in-meeting operations, media objects

### Initialize the SDK

```csharp
using SMeetingNet;

SMeetingEngine.SetLanguage("en");                 // optional: language of error texts (BCP 47)
var engine = SMeetingEngine.Init();
if (engine == null)
{
    return;      // initialization failed
}
Console.WriteLine(SMeetingEngine.Version());      // e.g. 1.0.0-alpha.9

// Engine-level settings must be in place before Login — the rtc engine is built inside Login
engine.Setting.EnableStreamLog = 1;
engine.Setting.SdkLogPath = @"D:\log\";
```

`SetLanguage` / `Version` / `GetStatusMessage` are static—no engine instance needed.
Use `SMeetingEngine.GetStatusMessage(code)` for the text of a status code; its language follows
`SetLanguage` (English until you call it).

### Register engine-level events

```csharp
engine.DeviceChanged += (s, e) => Console.WriteLine($"{e.Type} add={e.IsAdd} {e.Name}");
```

Only callbacks that **belong to no meeting** live here: device changes, default device changes, network
probe, IM, meeting-start reminder (`MeetingStartMessage`). Everything else is on `SMeetingChannel`.

### Log in

```csharp
SMeetingStatusCode st = engine.Login(token, (code, data) =>
{
    if (code == SMeetingStatusCode.Ok)
    {
        // data is the json returned by your backend
    }
});
```

`Login` is asynchronous—the result only arrives through the callback.

### Create a meeting

```csharp
var model = new SMeetingCreateMeetingModel
{
    Title = "My meeting",
    Content = "Meeting description",
    MeetingType = 1,   // 1 instant, 2 scheduled
    MeetingMode = 1,   // 1 normal
};

engine.CreateRoom(model, (code, data) =>
{
    if (code == SMeetingStatusCode.Ok)
    {
        // data is the meeting number
    }
});
```

If you already have a meeting id or room number, skip straight to the next step.

### Enter a meeting

Two steps: `CreateChannel` only creates the object **without entering**; configure it, then call `Enter()`.
As in C++, **register the events before `Enter()`**—the entering callbacks fire synchronously while
`enter` is still running.

```csharp
SMeetingChannel channel = engine.CreateChannel(roomNo);   // or CreateChannelByMeetingId(meetingId)
if (channel == null)
{
    return;      // invalid roomNo
}

// Events must be wired before Enter
channel.Disconnected           += (s, e) => Console.WriteLine($"disconnected {e.Reason} {e.Code} {e.Message}");
channel.Reconnected            += (s, e) => Console.WriteLine("reconnected");
channel.Reconnecting           += (s, e) => Console.WriteLine("reconnecting");
channel.UserEntered            += (s, e) => Console.WriteLine("user entered " + e.UserData);   // member json
channel.UserExited             += (s, e) => Console.WriteLine("user left " + e.UserData);
channel.UserCameraStateChanged += (s, e) => Console.WriteLine($"{e.Uid} camera {e.NewState}");

// Channel settings: stream_model / mcu_track / enable_audio_record are read while entering only
SMeetingChannelSetting setting = channel.Setting;
setting.StreamModel = 1;             // stream media mode
setting.SpeakerInterval = 500;       // audio-level callback period (ms)
setting.StatInterval = 10000;        // network-stat callback period (ms)
setting.RoomName = "Alice";          // display name in the meeting
setting.StreamVendor = "seastart";   // vendor string expected by the backend

st = channel.Enter(pass, (code, data) =>
{
    if (code != SMeetingStatusCode.Ok)
    {
        engine.LeaveChannel(channel);   // recycle the channel object even when entering failed
        return;
    }
    Console.WriteLine("entered " + channel.ChannelId);
});
```

<Warning>
Set both `RoomName` (the display name) and `StreamVendor` **before** `Enter()`.
When entering fails the `channel` object still exists and must be recycled with
`engine.LeaveChannel(channel)`.
</Warning>

### Get room and member data

```csharp
string me      = channel.GetMeJson();          // local member json
string room    = channel.GetRoomJson();        // room json
string members = channel.GetMembersJson();     // member json array
string member  = channel.GetMemberJson(uid);   // one member json
```

<Note>
These return **raw json** whose schema belongs to the backend—parse it yourself. Each member's published
tracks live in its `stream_tracks` field (`desc` / `kind` / `width` / `height` / `fps`).
</Note>

### Camera

```csharp
SMeetingLocalCamera camera = channel.GetLocalCamera();
if (camera == null) return;

camera.AddPlayView(new SMeetingHwndView(hwnd));        // hwnd is the render control's window handle
camera.SwitchCamera("Integrated Camera", 640, 480);    // optional: pick device and resolution
camera.RequestOpenCamera((code, data) => { /* result */ });
```

```csharp
camera.RemoveAllPlayView();
camera.CloseCamera((code, data) => { /* result */ });
```

### Microphone

```csharp
SMeetingLocalMic mic = channel.GetLocalMic();
if (mic == null) return;

mic.SwitchMic("Default Microphone");    // optional; pass "default" for the system default device
mic.RequestOpenMic((code, data) => { /* result */ });
```

```csharp
mic.CloseMic((code, data) => { /* result */ });
```

### Speaker (hear everyone)

Remote audio fetched with an **empty uid** is the channel mix, so opening it is enough to hear everyone—
no per-member subscription:

```csharp
SMeetingRemoteAudio speaker = channel.GetRemoteAudio(string.Empty);
if (speaker == null) return;

speaker.SwitchSpeaker("Default Speakers");     // optional; pass "default" for the system default device
speaker.OpenSpeaker();
```

```csharp
speaker.CloseSpeaker();
```

### Play remote video

```csharp
// uid / desc come from the member json stream_tracks: camera_big / camera_small for the camera, screen for sharing
SMeetingRemoteVideo remote = channel.GetRemoteVideo(uid, "camera_big");
if (remote == null) return;

remote.AddPlayView(new SMeetingHwndView(hwnd));
SMeetingStatusCode rst = remote.LoadRemoteVideo();      // subscribe and pull
```

```csharp
remote.RemovePlayView(view);
remote.UnloadRemoteVideo();
```

<Warning>
A remote track is **not** a long-lived handle: the SDK destroys it once the member leaves, and the same
`(uid, desc)` then resolves to `null`. Don't cache `SMeetingRemoteVideo`—re-fetch it through
`GetRemoteVideo` on every use. Local camera / screen objects are the opposite: they stay valid for the
lifetime of the channel.
</Warning>

<Note>
For window rendering just use the ready-made `SMeetingHwndView(handle)`; to render into your own surface
derive from `SMeetingView` and override `UpdatePlanes` (`GetViewType` returns `SMeetingViewType.CallBack`).
Always `RemovePlayView` before disposing a `SMeetingView`, or the render thread may touch a freed object.
</Note>

### Share the screen

```csharp
SMeetingLocalScreen screen = channel.GetLocalScreen();
if (screen == null) return;

screen.AddScreenAudio(true);                        // whether to include system sound

// tp: 1 screen share, 2 window share
// data: "x,y,width,height" for a monitor, "hwnd:<handle>" for a window
screen.RequestShare(1, "0,0,1920,1080", (code, data) => { /* result */ });
```

```csharp
screen.StopShare((code, data) => { /* result */ });
```

Enumerate share targets with `engine.EnumScreen()`: `Type == 5` is a monitor (build the rectangle from
`X` / `Y` / `Width` / `Height`), `Type == 0` is a window (use `Hwnd`).

### Chat and custom messages

```csharp
// public chat: tp 1 text, 2 file, 3 image, 4 sound
channel.SendRoomChatMessage(1, "Hello everyone!", (code, data) => { });

// point-to-point custom message: note the order — target id first, content second
channel.SendRoomCustomMessage(targetUid, "{\"cmd\":1}", (code, data) => { });
```

Incoming messages arrive in the `RoomChatMessage` / `RoomCustomMessage` events.

### Host operations

```csharp
channel.AdminRequestUserOpenCamera(uid, (code, data) => { });
channel.AdminCloseUserCamera(uid, (code, data) => { });
channel.AdminRequestUserOpenMic(uid, (code, data) => { });
channel.AdminCloseUserMic(uid, (code, data) => { });
channel.AdminKickUserOut(uid, (code, data) => { });
channel.AdminDestroyRoom((code, data) => { });          // end (dissolve) the meeting
```

### Local recording

```csharp
SMeetingRecord record = channel.GetLocalRecord();   // one recorder per channel
if (record == null) return;

record.SetRecordFileName(@"C:\record\meeting.mp4");
record.SetWaterMask("Meeting recording");
record.SetRecordHwnd(hwnd, 0, 0, 0, 0);
record.Start();

// record.Pause();
// record.Stop();
```

### Leave and release

```csharp
engine.LeaveChannel(channel);   // destroys the channel; its media objects become invalid at once
channel = null;                 // the object is gone, clear the reference yourself

// or leave every channel at once
engine.LeaveAllChannels();

engine.Dispose();               // release the engine
```

### Threading and lifetime

+ Except for the events raised while entering, **all events arrive on SDK internal threads**—marshal to
  your UI thread yourself (WinForms: `BeginInvoke`)
+ Async APIs taking an `SMeetingCallback` (`Login` / `Enter` / `RequestOpenCamera`, …) invoke the callback
  **once**, with `(SMeetingStatusCode code, string data)`
+ Every media object is a **handle borrowed from its channel**: valid only while that channel is alive,
  and never to be used after leaving
+ `SMeetingNet.dll` is a C++/CLI mixed-mode assembly, so its bitness must match `bin` and your project's
  target platform—see [Integration](/en/meeting/windows/integration)

A fuller runnable example is the WinForms demo (9-grid layout, with device pickers, paging, sharing and chat).
