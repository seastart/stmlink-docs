---
title: "Integration"
description: "Download links for the x86 and x64 packages of the SMeeting Windows SDK, environment requirements, package layout, project setup, and how to deploy the runtime DLLs—for C++, C, and C# (the SMeetingNet wrapper). Read this before writing any code, and again when upgrading the SDK."
---

On Windows all three integrations share **one package and one set of runtime dependencies**: C++ calls the
native API directly, C uses the `SMeetingEngine_*` functions from `SMeeting_C.h`, and C# goes through the
bundled `SMeetingNet` wrapper, which exposes the `SMeeting.h` C++ API
([ISMeetingEngine](/en/meeting/windows/api-reference/smeeting-engine) /
[ISMeetingChannel](/en/meeting/windows/api-reference/smeeting-channel) / the media objects) as idiomatic
`SMeetingNet`-namespace `class` / `event` / `IDisposable` types, so you never write callback vtables.
Pick the tab for your language:

### Environment requirements

<Tabs>
<Tab title="C++">

<Warning>
**The SDK ships as two packages, x86 (Win32 / 32-bit) and x64 (64-bit), and the one you use must match your project's target platform.**
Linking the x86 package into a 64-bit project (or the other way around) fails at link time with
`fatal error LNK1112: module machine type 'x86' conflicts with target machine type 'x64'`.
</Warning>

+ Target platform: Windows x86 (Win32 / 32-bit) or x64 (64-bit)—**pick the package that matches your project's target platform**
+ Language: C++, or C (the C interface uses the `SMeetingEngine_*` functions in `SMeeting_C.h`; headers, import library and deployment are identical to C++—see the [C quickstart](/en/meeting/windows/quickstart-c))
+ Runtime: the SDK package already includes the VC++ runtime DLLs it needs, so you **don't** need to install a runtime redistributable on the target machine

</Tab>
<Tab title="C#">

<Warning>
**`SMeetingNet.dll` is a C++/CLI mixed-mode assembly, not a purely managed DLL**: it links the native `SMeeting.dll` directly, so its **bitness must match the native package you use**. A mismatch throws `BadImageFormatException` at runtime rather than failing the build.
</Warning>

+ Target framework: **.NET Framework 4.7.2 or later** (the assembly targets 4.7.2 and runs fine on the 4.8 runtime)
+ Target platform: **the same as the native package**—an x86 app uses `meeting_dll/net/SMeetingNet.dll` + `meeting_dll/bin` from the x86 package, an x64 app uses the same files from the x64 package. Set your project's platform explicitly to x86 / x64; **don't use `Any CPU`**
+ Language: C# (other .NET languages work too)
+ Runtime: the package already includes the VC++ runtime DLLs it needs

</Tab>
</Tabs>

---

### Download the SDK

All three integrations live in the **same package**, so the download links are identical:

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
├── include/              # Headers (C++ / C)
│   ├── SMeeting.h
│   ├── SMeeting_def.h
│   └── SMeeting_C.h
├── lib/
│   └── SMeeting.lib      # Import library, used at link time (C++ / C)
├── net/
│   └── SMeetingNet.dll   # C# wrapper assembly (for C#, see "Project setup" below)
└── bin/                  # Runtime dependencies; ship all of them with your app
    ├── SMeeting.dll      # The conferencing SDK itself
    ├── srtc.dll          # Underlying audio and video library
    ├── ...               # Media, codec, networking, and other dependencies
    └── plugin/           # Plugins (keep the subdirectory structure)
```

<Warning>
Both packages unzip to a directory with the same name. **Don't unzip them into the same directory, where they overwrite each other**, and don't mix `lib` / `bin` / `net` across architectures
(the x86 `SMeeting.lib` / `SMeeting.dll` / `SMeetingNet.dll` and the x64 ones are different binaries).
</Warning>

<Note>
The file list inside the package (count and names) changes between versions—never pick files one by one by name.
</Note>

---

### Project setup

<Tabs>
<Tab title="C++">

<Steps>
<Step title="Add the include directory">
Add `meeting_dll/include` to your project's additional include directories, then include the headers in your code:

```cpp
#include <SMeeting.h>
#include <SMeeting_def.h>
```

For the C interface, also include `SMeeting_C.h`.
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

</Tab>
<Tab title="C#">

<Steps>
<Step title="Reference SMeetingNet.dll">
Add an assembly reference to `meeting_dll\net\SMeetingNet.dll` in your C# project:

```xml
<Reference Include="SMeetingNet">
  <HintPath>...\meeting_dll\net\SMeetingNet.dll</HintPath>
  <SpecificVersion>false</SpecificVersion>
  <Private>true</Private>
</Reference>
```

With `Private` (copy local) set to `true`, `SMeetingNet.dll` is copied into the output directory alongside your exe.

<Warning>
Set the project's target platform explicitly to `x86` or `x64` and **don't use `Any CPU`**—`SMeetingNet.dll` is a mixed-mode assembly, so its bitness is fixed.
</Warning>
</Step>

<Step title="Deploy the native runtime dependencies">
Copy `meeting_dll/net/SMeetingNet.dll` **and** everything under `meeting_dll/bin` into the directory that contains your executable:

```text
YourAppDirectory/
├── YourApp.exe
├── SMeetingNet.dll  ← the wrapper from meeting_dll/net
├── SMeeting.dll     ← the native SDK from meeting_dll/bin
├── srtc.dll
├── ...              ← The other DLLs under bin
└── plugin/          ← Keep the subdirectory structure unchanged
```

<Warning>
`net` and `bin` are **two separate directories** and both must sit next to your exe at runtime. Without the native DLLs from `bin`, loading or entering a meeting fails (`DllNotFoundException` or a load error).
</Warning>
</Step>
</Steps>

<Note>
`SMeetingNet.dll` is only a thin wrapper—the real implementation still lives in `SMeeting.dll`, so the native deployment rules are the same as for C++. See the C++ tab's "Deploy the runtime dependencies" above.
</Note>

</Tab>
</Tabs>

---

### Next steps

+ [C++ quickstart](/en/meeting/windows/quickstart)—log in, create a meeting, and enter it
+ [C# quickstart](/en/meeting/windows/quickstart-csharp)—the same flow through SMeetingNet
+ [C quickstart](/en/meeting/windows/quickstart-c)—the C interface (`SMeetingEngine_*`)
+ [Key concepts](/en/meeting/key-concepts)—rooms, meetings, members, and roles
+ [Token and authentication](/en/meeting/token)—your backend issues the tokens
