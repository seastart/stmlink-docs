---
title: "集成"
description: "Windows SRTC 音视频 SDK 的下载地址、环境要求、工程配置与运行时依赖部署，含 C++ 与 C#（srtcNet 封装）两种接入方式。"
---

Windows 端两种接入方式共用**同一个包、同一套运行时依赖**：C++ 直接调用原生接口；C# 走包内的 `srtcNet` 封装，它把 srtc 的 C++ 接口（[IRTCEngine](./api-reference/IRTCEngine.md) / [IRTCChannel](./api-reference/IRTCChannel.md) / 轨道 / 视图）完整暴露为 `Srtc` 命名空间下惯用的 `class` / `event` / `IDisposable`，不需要自己写回调 vtable。按语言选对应标签：

### 环境要求

<Tabs>
<Tab title="C++">

<Warning>
**SDK 提供 x86（Win32 / 32 位）与 x64（64 位）两个包，必须与你的工程目标平台一致。**
用 x86 包链接 64 位工程（或反过来）会在链接期报
「模块计算机类型 x86 与目标计算机类型 x64 冲突」。
</Warning>

+ 目标平台：Windows x86（Win32 / 32 位）或 x64（64 位）—— **按工程的目标平台选对应的包**
+ 语言：C++
+ 运行时：SDK 包内已附带所需的 VC++ 运行库 DLL，**无需**在目标机器上单独安装运行库分发包

</Tab>
<Tab title="C#">

<Warning>
**`srtcNet.dll` 是 C++/CLI 混合模式程序集，不是纯托管 DLL**：它内部直接链接原生 `srtc.dll`，
**位数必须与所用原生包一致**。位数不匹配会在运行期抛
`BadImageFormatException`，而不是编译报错。
</Warning>

+ 目标框架：**.NET Framework 4.7.2 及以上**（封装程序集以 4.7.2 为目标，可直接运行在 4.8 运行时上）
+ 目标平台：**与原生包一致** —— x86 程序用 x86 包的 `rtc_dll/net/srtcNet.dll` + `rtc_dll/bin`；
  x64 程序用 x64 包的同名文件
+ 语言：C#（其他 .NET 语言亦可）
+ 运行时：包内已附带所需 VC++ 运行库 DLL，无需单独安装

</Tab>
</Tabs>

---

### 下载 SDK

C++ 与 C# 封装在**同一个包**里，下载地址一致：

| 版本 | 架构 | 下载地址 |
| --- | --- | --- |
| 2.1 | x86（32 位） | [rtc-win-sdk-2.1.zip](https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-2.1.zip) |
| 2.1 | x64（64 位） | [rtc-win-sdk-x64-2.1.zip](https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-x64-2.1.zip) |

新版本发布后按同样的命名规则取用，替换版本号即可。x64 包是在版本号**前面**多一段 `-x64`：

```text
https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-<版本号>.zip
https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-x64-<版本号>.zip
```

---

### 目录结构

解压后得到（两个包的结构完全一样，内部根目录都是 `rtc_dll/`）：

```text
rtc_dll/
├── include/          # 头文件（C++）
│   ├── srtc.h
│   └── srtc_def.h
├── lib/
│   └── srtc.lib      # 导入库，链接时用（C++）
├── net/
│   └── srtcNet.dll   # C# 封装程序集（C# 用，见下方「工程配置」）
└── bin/              # 运行时依赖，全部需要随程序分发
    ├── srtc.dll      # SDK 主体
    ├── srtcLive.dll  # 采集/编解码/渲染
    ├── ...           # 媒体、编解码、网络等依赖库
    └── plugin/       # 插件及其 xml 配置
```

<Warning>
两个包解压后目录名相同，**不要解压到同一个目录互相覆盖**，也不要跨架构混用
`lib` 与 `bin`（x86 的 `srtc.lib` / `srtc.dll` 与 x64 的不是同一套二进制）。
</Warning>

<Note>
包内的文件清单（数量和名称）会随版本调整，不要按文件名逐个挑选。
AnyLive/ook 运行时不在包内，见下面「部署运行时依赖」的说明。
</Note>

---

### 工程配置

<Tabs>
<Tab title="C++">

<Steps>
<Step title="添加头文件目录">
把 `rtc_dll/include` 加入工程的附加包含目录，代码中引入：

```cpp
#include <srtc.h>
#include <srtc_def.h>
```
</Step>

<Step title="链接导入库">
把 `rtc_dll/lib` 加入附加库目录，并链接 `srtc.lib`。
</Step>

<Step title="部署运行时依赖">
把 `rtc_dll/bin` 目录下的**全部内容**拷贝到可执行文件所在目录：

```text
你的程序目录/
├── YourApp.exe
├── srtc.dll
├── ...              ← bin 下其余 DLL
└── plugin/          ← 保持子目录结构不变
    ├── *.dll
    └── *.xml
```

<Warning>
三个容易遗漏的点：

+ **DLL 的位数必须与 `YourApp.exe` 一致**：32 位程序配 x86 包的 `bin`，64 位程序配 x64 包的 `bin`
+ **`plugin/` 必须保持为子目录**，不能把里面的 DLL 平铺到根目录
+ **`plugin/` 下的 `.xml` 配置文件也要一起拷贝**（`conf.xml`、`cocktail_service.xml`、
  `linkmic_service.xml`），缺失会导致插件加载失败，表现为屏幕共享等功能不可用
</Warning>

<Warning>
**0.2.1-alpha.6 起，`rtc-win-sdk-2.1.zip`（x86）与 `rtc-win-sdk-x64-2.1.zip`（x64）
都不再包含 AnyLive/ook 运行时**：
`AnyLiveMVSC.dll`、`libEGL.dll`、`libGLESv2.dll`、`libeay32.dll`、`ssleay32.dll`、
`stlport.5.1.dll`，以及 `plugin/` 下的 `anyLiveM.dll`、`cocktail_service.dll`、`libmm.dll`、
`linkmic_service.dll`、`onvif_receiver.dll`、`transcoder.dll` 和上面提到的三个 `.xml`。

这些文件本身没有变化，但需要**另行获取**（例如从 meeting SDK 包，或上一版 rtc 包中取）。
缺失时程序是**运行期加载失败**而不是编译报错 —— 表现为进入频道后收发流不可用。
升级到本版本时请确认这批文件仍在你的分发目录里。
</Warning>
</Step>
</Steps>

<Note>
`bin` 目录的内容会随版本调整，所以推荐**整体拷贝**而不是按文件名逐个挑选 —— 逐个挑选在升级
SDK 时很容易漏掉新增的依赖库。
</Note>

</Tab>
<Tab title="C#">

<Steps>
<Step title="引用 srtcNet.dll">
在 C# 工程里添加对 `rtc_dll\net\srtcNet.dll` 的程序集引用：

```xml
<Reference Include="srtcNet">
  <HintPath>...\rtc_dll\net\srtcNet.dll</HintPath>
  <SpecificVersion>false</SpecificVersion>
  <Private>true</Private>
</Reference>
```

`Private`（复制本地）设为 `true`，生成的 exe 目录里就会带上 `srtcNet.dll`。
</Step>

<Step title="部署原生运行时依赖">
把 `rtc_dll/net/srtcNet.dll` **以及** `rtc_dll/bin` 下的**全部内容**一起拷到可执行文件所在目录：

```text
你的程序目录/
├── YourApp.exe
├── srtcNet.dll      ← rtc_dll/net 下的封装
├── srtc.dll         ← rtc_dll/bin 下的原生主体
├── ...              ← bin 下其余 DLL
└── plugin/          ← 保持子目录结构不变
```

<Warning>
`net` 与 `bin` 是**两层目录**，程序运行需要两者都在 exe 目录下。缺 `bin` 里的原生 DLL 会在
加载/进入频道时报错（`DllNotFoundException` 或加载失败）。
</Warning>
</Step>
</Steps>

<Note>
`plugin/` 子目录与其下的 `.xml` 配置必须保持原样，不要平铺或遗漏 —— 否则屏幕共享等功能不可用；
原生依赖的部署要点与 C++ 一致，参见上方 C++ 标签的「部署运行时依赖」。
</Note>

</Tab>
</Tabs>

---

### 下一步

+ [C++ 快速开始](/zh/rtc/windows/quickstart-cpp) · [C# 快速开始](/zh/rtc/windows/quickstart-csharp) —— 初始化、加入频道、收发音视频
+ [核心概念](/zh/rtc/key-concepts) —— 频道、用户、流轨道模型
+ [Token 与鉴权](/zh/rtc/token) —— 加入频道 token 由你的后端签发
