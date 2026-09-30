---
title: "Integration"
description: "Download links for the Windows SRTC C++ SDK (x86 and x64 packages), environment requirements, package layout, Visual Studio project configuration, and which runtime DLLs and plugins to ship. Read before adding the SDK to a Windows desktop project."
---

### Environment requirements

<Warning>
**The SDK comes in two packages, x86 (Win32 / 32-bit) and x64 (64-bit), and the one you use must match your project's target platform.**
Linking the x86 package into a 64-bit project (or the other way around) fails at link time with
`fatal error LNK1112: module machine type 'x86' conflicts with target machine type 'x64'`.
</Warning>

+ Target platform: Windows x86 (Win32 / 32-bit) or x64 (64-bit)—**choose the package that matches your project's target platform**
+ Language: C++
+ Runtime: the SDK package already ships the required VC++ runtime DLLs, so you **don't need** to install a runtime redistributable on the target machine

---

### Download the SDK

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
├── include/          # Header files
│   ├── srtc.h
│   └── srtc_def.h
├── lib/
│   └── srtc.lib      # Import library, used at link time
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

---

### Next steps

+ [Quickstart](/en/rtc/windows/quickstart): initialize, join a channel, and send and receive audio and video
+ [Key concepts](/en/rtc/key-concepts): the channel, user, and track model
+ [Token and authentication](/en/rtc/token): the token for joining a channel is issued by your backend
