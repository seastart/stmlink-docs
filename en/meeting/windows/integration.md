---
title: "Integration"
description: "Download links for the x86 and x64 packages of the SMeeting Windows SDK, environment requirements, package layout, Visual Studio project setup, and how to deploy the runtime DLLs. Read this before writing any code, and again when upgrading the SDK."
---

### Environment requirements

<Warning>
**The SDK ships as two packages, x86 (Win32 / 32-bit) and x64 (64-bit), and the one you use must match your project's target platform.**
Linking the x86 package into a 64-bit project (or the other way around) fails at link time with
`fatal error LNK1112: module machine type 'x86' conflicts with target machine type 'x64'`.
</Warning>

+ Target platform: Windows x86 (Win32 / 32-bit) or x64 (64-bit)—**pick the package that matches your project's target platform**
+ Language: C++
+ Runtime: the SDK package already includes the VC++ runtime DLLs it needs, so you **don't** need to install a runtime redistributable on the target machine

---

### Download the SDK

| Version | Architecture | Download |
| --- | --- | --- |
| 2.0 | x86 (32-bit) | [meeting-win-sdk-2.0.zip](https://repo.open.seastart.cn/repository/vcs-releases/meeting-win-sdk-2.0.zip) |
| 2.0 | x64 (64-bit) | [meeting-win-sdk-x64-2.0.zip](https://repo.open.seastart.cn/repository/vcs-releases/meeting-win-sdk-x64-2.0.zip) |

When a new version is released, follow the same naming pattern and replace the version number. The x64 package has an extra `-x64` segment **before** the version number:

```text
https://repo.open.seastart.cn/repository/vcs-releases/meeting-win-sdk-<version>.zip
https://repo.open.seastart.cn/repository/vcs-releases/meeting-win-sdk-x64-<version>.zip
```

<Note>
The SMeeting Windows SDK package **already includes the underlying audio and video library** (`srtc.dll` and others), so you don't need to download the SRTC Windows SDK separately.
</Note>

---

### Directory structure

After unzipping you get the following (both packages have exactly the same layout, and the root directory inside is `meeting_dll/` in both):

```text
meeting_dll/
├── include/              # Header files
│   ├── SMeeting.h
│   └── SMeeting_def.h
├── lib/
│   └── SMeeting.lib      # Import library, used at link time
└── bin/                  # Runtime dependencies; ship all of them with your app
    ├── SMeeting.dll      # The conferencing SDK itself
    ├── srtc.dll          # Underlying audio and video library
    ├── ...               # Media, codec, networking, and other dependencies
    └── plugin/           # Plugins (keep the subdirectory structure)
```

<Warning>
Both packages unzip to a directory with the same name. **Don't unzip them into the same directory, where they overwrite each other**, and don't mix `lib` and `bin` across architectures
(the x86 `SMeeting.lib` / `SMeeting.dll` and the x64 ones are different binaries).
</Warning>

---

### Project setup

<Steps>
<Step title="Add the include directory">
Add `meeting_dll/include` to your project's additional include directories, then include the headers in your code:

```cpp
#include <SMeeting.h>
#include <SMeeting_def.h>
```
</Step>

<Step title="Link the import library">
Add `meeting_dll/lib` to the additional library directories and link `SMeeting.lib`.
</Step>

<Step title="Deploy the runtime dependencies">
Copy **everything** under `meeting_dll/bin` into the directory that contains your executable:

```text
YourAppDirectory/
├── YourApp.exe
├── SMeeting.dll
├── srtc.dll
├── ...              ← The other DLLs under bin
└── plugin/          ← Keep the subdirectory structure unchanged
    └── *.dll
```

<Warning>
Two things that are easy to miss:

+ **The DLLs' bitness must match `YourApp.exe`**: a 32-bit app uses the `bin` from the x86 package, and a 64-bit app uses the `bin` from the x64 package
+ **`plugin/` must stay a subdirectory**; don't flatten the DLLs inside it into the root directory
</Warning>

<Warning>
**The file list in `bin` changed starting with 1.0.0-alpha.6**: it no longer contains `DenModule.dll`, `pthreadGC2.dll`,
`pthreadVC2.dll`, `rtp.dll`, or `zlib.dll`, and adds `zlib1.dll`.

These are dependency changes in the underlying audio and video library. **Overwrite** your distribution directory with the whole `bin` from the new package instead of copying files incrementally by name,
so that old DLLs that are no longer needed don't linger.
</Warning>
</Step>
</Steps>

<Note>
The contents of the `bin` directory change between versions, so we recommend **copying it as a whole** rather than picking files one by one by name—when you pick files by hand, it's easy to miss newly added dependencies when you upgrade
the SDK.
</Note>

---

### Next steps

+ [Quickstart](/en/meeting/windows/quickstart)—log in, create a meeting, and enter it
+ [Key concepts](/en/meeting/key-concepts)—rooms, meetings, members, and roles
+ [Token and authentication](/en/meeting/token)—your backend issues the tokens
