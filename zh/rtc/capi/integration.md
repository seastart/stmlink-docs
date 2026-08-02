---
title: "集成方式"
description: "SRTC C SDK 的能力边界、支持平台、库文件说明与链接方式"
---

SRTC C SDK 是一套面向**服务端与嵌入式**场景的音视频 SDK，对外提供纯 C 接口（`rtc_*` 函数与 `rtc_*_t` 结构体，以 `extern "C"` 声明），C 和 C++ 项目都可以直接使用。

### 适用场景

+ 服务端旁路录制、转码、转推
+ MCU 合成流的推送端
+ AI Agent / 语音机器人接入频道
+ 嵌入式设备（Linux ARM 板卡）推流与收流

### 能力边界

本 SDK **不包含**摄像头采集、麦克风采集、视频渲染、设备管理、美颜等终端能力：

+ **推流**：由你完成采集与编码，把编码后的 H264 / H265 / OPUS / AAC 裸数据通过 `rtc_write_sample` 交给 SDK
+ **收流**：SDK 通过回调把远端的编码数据交给你，解码和渲染由你自行处理

如果你要做的是桌面客户端，请改用 [Windows SDK](/zh/rtc/windows/integration)，它是 C++ 接口且自带采集与渲染。

---

### SDK 包内容

| 文件 | 说明 |
| --- | --- |
| `librtc.h` | C 接口头文件 |
| `librtc.so` | 动态库（Linux） |
| `librtc.a` | 静态库（Linux / Windows，GNU ar 格式，适用于 GCC、MinGW 工具链） |
| `librtc.dll` | 动态库（Windows） |
| `librtc.lib` | 导入库（Windows），MSVC 链接 `librtc.dll` 时使用 |

<Note>
MSVC（Visual Studio）项目请使用 `librtc.dll` + `librtc.lib`，不能直接链接 `librtc.a`。
</Note>

---

### 支持平台

| 平台 | 架构 | 提供的库文件 |
| --- | --- | --- |
| Linux（glibc） | x86_64 | `librtc.so`、`librtc.a` |
| Linux（glibc） | aarch64 | `librtc.so`、`librtc.a` |
| Linux（musl / Alpine） | aarch64 | `librtc.so` |
| Linux | armv7（32 位） | `librtc.so`、`librtc.a` |
| Windows | x86_64 | `librtc.dll`、`librtc.lib`、`librtc.a` |

<Warning>
**请按目标系统的 libc 选择对应的库。** 主流发行版（CentOS / Ubuntu / Debian 等）用 glibc 版本，Alpine 用 musl 版本，两者不能混用。

Alpine（musl）平台只提供动态库 `librtc.so`，不提供静态库。
</Warning>

需要上表以外的平台或架构，请联系我们。

---

### 编译与链接

引入头文件：

```c
#include "librtc.h"
```

GCC / Clang 链接动态库：

```bash
gcc -Wall -I/path/to/sdk -o myapp main.c \
    -L/path/to/sdk -lrtc -lpthread -lm
```

运行时需要让系统找得到 `librtc.so`：

```bash
export LD_LIBRARY_PATH=/path/to/sdk:$LD_LIBRARY_PATH
```

也可以在链接时写死查找路径，免去每次设置环境变量：

```bash
gcc -o myapp main.c -L/path/to/sdk -lrtc -lpthread -lm -Wl,-rpath,/path/to/sdk
```

<Tip>
若运行时报 `error while loading shared libraries: librtc.so`，说明库查找路径没设对：检查 `LD_LIBRARY_PATH` 或 `-rpath`，或把 `librtc.so` 复制到系统库目录。
</Tip>

---

### 流媒体引擎

频道使用哪个流媒体引擎由服务端下发的频道配置决定，你的代码无需关心，也不需要做任何配置。

部分能力（simulcast 切层、网络质量上报、活跃说话人）仅在 SeaStart 引擎下可用，其它引擎下对应回调不会触发 —— 详见 [SeaStart 进阶能力](/zh/rtc/capi/advanced/seastart)。请确保业务在没有这些回调时也能正常工作。

---

### 下一步

+ [快速开始](/zh/rtc/capi/quickstart)：10 分钟跑通收流与推流
+ [接口文档](/zh/rtc/capi/api-reference/engine)：完整 API 参考
