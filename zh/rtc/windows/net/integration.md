---
title: "C# 集成"
description: "Windows SRTC 的 C# 封装 srtcNet：下载位置、环境要求、工程引用与运行时部署。它是 C++/CLI 混合程序集，Srtc 命名空间下的一套 .NET API。"
---

`srtcNet` 把 srtc 的 C++ 接口（[IRTCEngine](../api-reference/IRTCEngine.md) / [IRTCChannel](../api-reference/IRTCChannel.md) / 轨道 / 视图）
完整暴露给 C#，命名空间是 `Srtc`。C# 侧得到的是惯用的 `class` / `event` / `IDisposable`，
不需要自己写回调 vtable。

### 环境要求

<Warning>
**`srtcNet.dll` 是 C++/CLI 混合模式程序集，不是纯托管 DLL**：它内部直接链接原生 `srtc.dll`，
**位数必须与所用原生包一致**。位数不匹配会在运行期抛
`BadImageFormatException`，而不是编译报错。
</Warning>

+ 目标框架：**.NET Framework 4.7.2 及以上**（封装程序集以 4.7.2 为目标，可直接运行在 4.8 运行时上）
+ 目标平台：**与原生包一致** —— x86 程序用 `rtc_dll/net/srtcNet.dll` + `rtc_dll/bin`（x86 包）；
  x64 程序用 x64 包的同名文件
+ 语言：C#（其他 .NET 语言亦可）
+ 运行时：包内已附带所需 VC++ 运行库 DLL，无需单独安装

---

### 下载 SDK

C# 封装与 C++ SDK 在**同一个包**里，下载地址一致：

| 版本 | 架构 | 下载地址 |
| --- | --- | --- |
| 2.1 | x86（32 位） | [rtc-win-sdk-2.1.zip](https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-2.1.zip) |
| 2.1 | x64（64 位） | [rtc-win-sdk-x64-2.1.zip](https://repo.open.seastart.cn/repository/vcs-releases/rtc-win-sdk-x64-2.1.zip) |

解压后，C# 封装位于 `rtc_dll/net/`：

```text
rtc_dll/
├── net/
│   └── srtcNet.dll   # C# 封装，工程里引用它
├── bin/              # 原生运行时依赖，全部随程序分发
├── include/          # C++ 头文件（C# 用不到）
└── lib/              # C++ 导入库（C# 用不到）
```

---

### 工程配置

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
`plugin/` 子目录与其下的 `.xml` 配置必须保持原样，不要平铺或遗漏 —— 否则屏幕共享等功能不可用。
与 C++ 集成一致，详见[集成](./../integration)。
</Note>

---

### 下一步

+ [C# 快速开始](./quickstart) —— 初始化、加入频道、收发音视频
+ [C++ 集成](./../integration) —— 原生接口的下载与工程配置
+ [核心概念](/zh/rtc/key-concepts) —— 频道、用户、流轨道模型
+ [Token 与鉴权](/zh/rtc/token) —— 加入频道 token 由你的后端签发
