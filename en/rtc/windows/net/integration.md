---
title: "C# Integration"
description: "The C# wrapper for the Windows SRTC SDK: where srtcNet.dll lives in the package, environment requirements, project reference, and runtime deployment. It is a C++/CLI mixed-mode assembly exposing a .NET API under the Srtc namespace."
---

`srtcNet` exposes the srtc C++ interfaces ([IRTCEngine](../api-reference/IRTCEngine.md) /
[IRTCChannel](../api-reference/IRTCChannel.md) / tracks / views) to C#, under the `Srtc` namespace.
On the C# side you get idiomatic `class` / `event` / `IDisposable`—no callback vtable to write by hand.

### Environment requirements

<Warning>
**`srtcNet.dll` is a C++/CLI mixed-mode assembly, not a pure managed DLL**: it links the native
`srtc.dll` directly, so **its bitness must match the native package you use**. A mismatch fails at
runtime with `BadImageFormatException`, not at compile time.
</Warning>

+ Target framework: **.NET Framework 4.7.2 or later** (the assembly targets 4.7.2 and runs on the 4.8 runtime)
+ Target platform: **must match the native package**—an x86 program uses `rtc_dll/net/srtcNet.dll` + `rtc_dll/bin`
  from the x86 package; an x64 program uses the same files from the x64 package
+ Language: C# (other .NET languages work too)
+ Runtime: the package already ships the required VC++ runtime DLLs; no separate install needed

---

### Download the SDK

The C# wrapper ships in the **same package** as the C++ SDK:

| Version | Architecture | Download |
| --- | --- | --- |
| 2.1 | x86 (32-bit) | [rtc-win-sdk-2.1.zip](https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-2.1.zip) |
| 2.1 | x64 (64-bit) | [rtc-win-sdk-x64-2.1.zip](https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-x64-2.1.zip) |

After extracting, the wrapper is under `rtc_dll/net/`:

```text
rtc_dll/
├── net/
│   └── srtcNet.dll   # the C# wrapper - reference this one
├── bin/              # native runtime dependencies, all of which must ship with your program
├── include/          # C++ headers (not needed from C#)
└── lib/              # C++ import library (not needed from C#)
```

---

### Project configuration

<Steps>
<Step title="Reference srtcNet.dll">
Add an assembly reference to `rtc_dll\net\srtcNet.dll`:

```xml
<Reference Include="srtcNet">
  <HintPath>...\rtc_dll\net\srtcNet.dll</HintPath>
  <SpecificVersion>false</SpecificVersion>
  <Private>true</Private>
</Reference>
```

With `Private` (Copy Local) set to `true`, `srtcNet.dll` lands next to your exe.
</Step>

<Step title="Deploy the native runtime dependencies">
Copy `rtc_dll/net/srtcNet.dll` **and everything** under `rtc_dll/bin` into the directory that
contains your executable:

```text
YourAppDir/
├── YourApp.exe
├── srtcNet.dll      ← the wrapper from rtc_dll/net
├── srtc.dll         ← the native core from rtc_dll/bin
├── ...              ← the other DLLs under bin
└── plugin/          ← keep the subdirectory structure unchanged
```

<Warning>
`net` and `bin` are **two separate directories** and the program needs both next to the exe. Missing
native DLLs from `bin` fail at load time or when joining a channel
(`DllNotFoundException` or a load failure).
</Warning>
</Step>
</Steps>

<Note>
The `plugin/` subdirectory and the `.xml` configuration files under it must be kept as-is—otherwise
features such as screen sharing don't work. Same as the C++ integration; see [Integration](./../integration).
</Note>

---

### Next steps

+ [C# quickstart](./quickstart): initialize, join a channel, and send and receive audio and video
+ [C++ integration](./../integration): download and project setup for the native API
+ [Key concepts](/en/rtc/key-concepts): the channel, user, and track model
+ [Token and authentication](/en/rtc/token): the token for joining a channel is issued by your backend
