---
title: "Integration"
description: "Download links, environment requirements, project configuration, and runtime deployment for the Windows SRTC SDK, covering both the C++ native API and the C# (srtcNet) wrapper."
---

The Windows SDK offers two ways in that share **the same package and the same runtime dependencies**: call the native API from C++, or use the bundled `srtcNet` wrapper from C# — it exposes the srtc C++ interfaces ([IRTCEngine](/en/rtc/windows/api-reference/IRTCEngine) / [IRTCChannel](/en/rtc/windows/api-reference/IRTCChannel) / tracks / views) as an idiomatic .NET API (`class` / `event` / `IDisposable`) under the `Srtc` namespace, so you never write a callback vtable. Pick your language:

### Environment requirements

<Tabs>
<Tab title="C++">

<Warning>
**The SDK comes in two packages, x86 (Win32 / 32-bit) and x64 (64-bit), and the one you use must match your project's target platform.**
Linking the x86 package into a 64-bit project (or the other way around) fails at link time with
`fatal error LNK1112: module machine type 'x86' conflicts with target machine type 'x64'`.
</Warning>

+ Target platform: Windows x86 (Win32 / 32-bit) or x64 (64-bit)—**choose the package that matches your project's target platform**
+ Language: C++
+ Runtime: the SDK package already ships the required VC++ runtime DLLs, so you **don't need** to install a runtime redistributable on the target machine

</Tab>
<Tab title="C#">

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

</Tab>
</Tabs>

---

### Download the SDK

The C++ SDK and the C# wrapper ship in the **same package**, so the download is the same:

| Version | Architecture | Download |
| --- | --- | --- |
| 2.1 | x86 (32-bit) | [rtc-win-sdk-2.1.zip](https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-2.1.zip) |
| 2.1 | x64 (64-bit) | [rtc-win-sdk-x64-2.1.zip](https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-x64-2.1.zip) |

When a new version is released, use the same naming pattern and replace the version number. The x64 package has an extra `-x64` segment **before** the version number:

```text
https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-<version>.zip
https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-x64-<version>.zip
```

---

### Directory structure

After extracting you get the following (both packages have exactly the same structure, and the root directory inside is `rtc_dll/` in both):

```text
rtc_dll/
├── include/          # Header files (C++)
│   ├── srtc.h
│   └── srtc_def.h
├── lib/
│   └── srtc.lib      # Import library, used at link time (C++)
├── net/
│   └── srtcNet.dll   # C# wrapper assembly (for C#; see "Project configuration" below)
└── bin/              # Runtime dependencies, all of which must ship with your program
    ├── srtc.dll      # SDK core
    ├── srtcLive.dll  # Capture / encoding and decoding / rendering
    ├── ...           # Media, codec, networking, and other dependencies
    └── plugin/       # Plugins and their xml configuration
```

<Warning>
Both packages extract to a directory with the same name, so **don't extract them into the same directory where they overwrite each other**, and don't mix
`lib` and `bin` across architectures (the x86 `srtc.lib` / `srtc.dll` are not the same binaries as the x64 ones).
</Warning>

<Note>
The file list in the package (number and names of files) changes between versions, so don't pick files one by one by name.
The AnyLive/OOK runtime isn't in the package; see the note under "Deploy runtime dependencies" below.
</Note>

---

### Project configuration

<Tabs>
<Tab title="C++">

<Steps>
<Step title="Add the include directory">
Add `rtc_dll/include` to your project's additional include directories, and include the headers in your code:

```cpp
#include <srtc.h>
#include <srtc_def.h>
```
</Step>

<Step title="Link the import library">
Add `rtc_dll/lib` to the additional library directories and link `srtc.lib`.
</Step>

<Step title="Deploy runtime dependencies">
Copy **everything** under `rtc_dll/bin` into the directory that contains your executable:

```text
YourAppDir/
├── YourApp.exe
├── srtc.dll
├── ...              ← the other DLLs under bin
└── plugin/          ← keep the subdirectory structure unchanged
    ├── *.dll
    └── *.xml
```

<Warning>
Three things that are easy to miss:

+ **The DLL bitness must match `YourApp.exe`**: a 32-bit program uses `bin` from the x86 package, and a 64-bit program uses `bin` from the x64 package
+ **`plugin/` must stay a subdirectory**; don't flatten the DLLs inside it into the root directory
+ **Also copy the `.xml` configuration files under `plugin/`** (`conf.xml`, `cocktail_service.xml`,
  `linkmic_service.xml`). If they're missing, plugins fail to load, and features such as screen sharing don't work
</Warning>

<Warning>
**Starting with 0.2.1-alpha.6, neither `rtc-win-sdk-2.1.zip` (x86) nor `rtc-win-sdk-x64-2.1.zip` (x64)
includes the AnyLive/OOK runtime**:
`AnyLiveMVSC.dll`, `libEGL.dll`, `libGLESv2.dll`, `libeay32.dll`, `ssleay32.dll`,
`stlport.5.1.dll`, plus `anyLiveM.dll`, `cocktail_service.dll`, `libmm.dll`,
`linkmic_service.dll`, `onvif_receiver.dll`, `transcoder.dll` under `plugin/`, and the three `.xml` files mentioned above.

These files haven't changed, but you need to **obtain them separately** (for example, from the SMeeting Windows SDK package or the previous SRTC package).
If they're missing, the program **fails to load them at runtime** rather than failing to compile—sending and receiving streams doesn't work after you join a channel.
When you upgrade to this version, make sure these files are still in your distribution directory.
</Warning>
</Step>
</Steps>

<Note>
The contents of the `bin` directory change between versions, so we recommend **copying it as a whole** rather than picking files one by one by name—picking files individually
makes it easy to miss newly added dependencies when you upgrade the SDK.
</Note>

</Tab>
<Tab title="C#">

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
features such as screen sharing don't work. The native dependency deployment is the same as for C++;
see "Deploy runtime dependencies" in the C++ tab above.
</Note>

</Tab>
</Tabs>

---

### Next steps

+ [C++ quickstart](/en/rtc/windows/quickstart-cpp) · [C# quickstart](/en/rtc/windows/quickstart-csharp): initialize, join a channel, and send and receive audio and video
+ [Key concepts](/en/rtc/key-concepts): the channel, user, and track model
+ [Token and authentication](/en/rtc/token): the token for joining a channel is issued by your backend
