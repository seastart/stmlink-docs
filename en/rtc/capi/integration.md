---
title: "Integration"
description: "What the SRTC C SDK does and doesn't do, supported platforms and architectures, the library files in the package, and how to compile and link them. Read this page before integrating the C SDK into a server-side or embedded project."
---

The SRTC C SDK is an audio and video SDK for **server-side and embedded** scenarios. It exposes a pure C interface (`rtc_*` functions and `rtc_*_t` structs, declared with `extern "C"`), so both C and C++ projects can use it directly.

### Use cases

+ Server-side recording, transcoding, and re-streaming
+ The publishing side of an MCU composite stream
+ Connecting AI agents / voice bots to a channel
+ Publishing and receiving on embedded devices (Linux ARM boards)

### What the SDK does and doesn't do

This SDK **doesn't include** client-side capabilities such as camera capture, microphone capture, video rendering, device management, or beauty filters:

+ **Publishing**: you handle capture and encoding, and hand the encoded H.264 / H.265 / Opus / AAC raw data to the SDK through `rtc_write_sample`
+ **Receiving**: the SDK hands you the remote encoded data through callbacks; decoding and rendering are up to you

If you're building a desktop client, use the [Windows SDK](/en/rtc/windows/integration) instead. It has a C++ interface and includes capture and rendering.

---

### SDK package contents

| File | Description |
| --- | --- |
| `librtc.h` | C interface header |
| `librtc.so` | Dynamic library (Linux) |
| `librtc.a` | Static library (Linux / Windows, GNU ar format, for the GCC and MinGW toolchains) |
| `librtc.dll` | Dynamic library (Windows) |
| `librtc.lib` | Import library (Windows), used by MSVC to link against `librtc.dll` |
| `librtc.dylib` | Dynamic library (macOS) |

<Note>
For MSVC (Visual Studio) projects, use `librtc.dll` + `librtc.lib`. You can't link `librtc.a` directly.
</Note>

---

### Supported platforms

| Platform | Architecture | Library files provided |
| --- | --- | --- |
| Linux (glibc) | x86_64 | `librtc.so`, `librtc.a` |
| Linux (glibc) | aarch64 | `librtc.so`, `librtc.a` |
| Linux (musl / Alpine) | aarch64 | `librtc.so` |
| Linux | armv7 (32-bit) | `librtc.so`, `librtc.a` |
| Windows | x86_64 | `librtc.dll`, `librtc.lib`, `librtc.a` |
| macOS | Apple Silicon (arm64) | `librtc.dylib` (for local development and debugging) |

<Warning>
**Choose the library that matches the target system's libc.** Mainstream distributions (CentOS / Ubuntu / Debian, etc.) use the glibc build, and Alpine uses the musl build. The two can't be mixed.

The Alpine (musl) platform only provides the dynamic library `librtc.so`, not a static library.
</Warning>

If you need a platform or architecture not listed above, contact us.

<Warning>
**When upgrading the SDK, recompile with the new `librtc.h`**—don't just replace the library files. When struct fields are added or removed (for example, 0.0.9 removed `rtc_user_info_t.link_id`), a program built with the old header reads the wrong fields. For changes in each version, see the [Changelog](/en/rtc/capi/changelog).
</Warning>

---

### Compiling and linking

Include the header:

```c
#include "librtc.h"
```

Link the dynamic library with GCC / Clang:

```bash
gcc -Wall -I/path/to/sdk -o myapp main.c \
    -L/path/to/sdk -lrtc -lpthread -lm
```

At runtime the system needs to be able to find `librtc.so`:

```bash
export LD_LIBRARY_PATH=/path/to/sdk:$LD_LIBRARY_PATH
```

You can also hard-code the search path at link time so you don't have to set the environment variable every time:

```bash
gcc -o myapp main.c -L/path/to/sdk -lrtc -lpthread -lm -Wl,-rpath,/path/to/sdk
```

<Tip>
If you get `error while loading shared libraries: librtc.so` at runtime, the library search path isn't set correctly: check `LD_LIBRARY_PATH` or `-rpath`, or copy `librtc.so` into a system library directory.
</Tip>

---

### Media streaming engine

Which media streaming engine a channel uses is determined by the channel configuration sent down by the server. Your code doesn't need to care about it or configure anything.

Some capabilities (simulcast layer switching, network quality reporting, active speaker) are only available with the SeaStart engine; with other engines the corresponding callbacks never fire—see [SeaStart advanced features](/en/rtc/capi/advanced/seastart). Make sure your application still works without these callbacks.

---

### Next steps

+ [Quickstart](/en/rtc/capi/quickstart): get receiving and publishing working in 10 minutes
+ [API reference](/en/rtc/capi/api-reference/engine): the complete API reference
