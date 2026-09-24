---
title: "集成"
description: "Windows SMeeting 会议 SDK 的下载地址、环境要求、工程配置与运行时依赖部署"
---

### 环境要求

<Warning>
**SDK 提供 x86（Win32 / 32 位）与 x64（64 位）两个包，必须与你的工程目标平台一致。**
用 x86 包链接 64 位工程（或反过来）会在链接期报
「模块计算机类型 x86 与目标计算机类型 x64 冲突」。
</Warning>

+ 目标平台：Windows x86（Win32 / 32 位）或 x64（64 位）—— **按工程的目标平台选对应的包**
+ 语言：C++
+ 运行时：SDK 包内已附带所需的 VC++ 运行库 DLL，**无需**在目标机器上单独安装运行库分发包

---

### 下载 SDK

| 版本 | 架构 | 下载地址 |
| --- | --- | --- |
| 2.0 | x86（32 位） | [meeting-win-sdk-2.0.zip](https://repo.open.seastart.cn/repository/vcs-releases/meeting-win-sdk-2.0.zip) |
| 2.0 | x64（64 位） | [meeting-win-sdk-x64-2.0.zip](https://repo.open.seastart.cn/repository/vcs-releases/meeting-win-sdk-x64-2.0.zip) |

新版本发布后按同样的命名规则取用，替换版本号即可。x64 包是在版本号**前面**多一段 `-x64`：

```text
https://repo.open.seastart.cn/repository/vcs-releases/meeting-win-sdk-<版本号>.zip
https://repo.open.seastart.cn/repository/vcs-releases/meeting-win-sdk-x64-<版本号>.zip
```

<Note>
会议 SDK 包里**已经包含底层音视频库**（`srtc.dll` 等），不需要再单独下载 SRTC 的 Windows SDK。
</Note>

---

### 目录结构

解压后得到（两个包的结构完全一样，内部根目录都是 `meeting_dll/`）：

```text
meeting_dll/
├── include/              # 头文件
│   ├── SMeeting.h
│   └── SMeeting_def.h
├── lib/
│   └── SMeeting.lib      # 导入库，链接时用
└── bin/                  # 运行时依赖，全部需要随程序分发
    ├── SMeeting.dll      # 会议 SDK 主体
    ├── srtc.dll          # 底层音视频库
    ├── ...               # 媒体、编解码、网络等依赖库
    └── plugin/           # 插件（保持子目录结构）
```

<Warning>
两个包解压后目录名相同，**不要解压到同一个目录互相覆盖**，也不要跨架构混用 `lib` 与 `bin`
（x86 的 `SMeeting.lib` / `SMeeting.dll` 与 x64 的不是同一套二进制）。
</Warning>

---

### 工程配置

<Steps>
<Step title="添加头文件目录">
把 `meeting_dll/include` 加入工程的附加包含目录，代码中引入：

```cpp
#include <SMeeting.h>
#include <SMeeting_def.h>
```
</Step>

<Step title="链接导入库">
把 `meeting_dll/lib` 加入附加库目录，并链接 `SMeeting.lib`。
</Step>

<Step title="部署运行时依赖">
把 `meeting_dll/bin` 目录下的**全部内容**拷贝到可执行文件所在目录：

```text
你的程序目录/
├── YourApp.exe
├── SMeeting.dll
├── srtc.dll
├── ...              ← bin 下其余 DLL
└── plugin/          ← 保持子目录结构不变
    └── *.dll
```

<Warning>
两个容易遗漏的点：

+ **DLL 的位数必须与 `YourApp.exe` 一致**：32 位程序配 x86 包的 `bin`，64 位程序配 x64 包的 `bin`
+ **`plugin/` 必须保持为子目录**，不能把里面的 DLL 平铺到根目录
</Warning>

<Warning>
**1.0.0-alpha.6 起 `bin` 的文件清单有变化**：不再包含 `DenModule.dll`、`pthreadGC2.dll`、
`pthreadVC2.dll`、`rtp.dll`、`zlib.dll`，新增 `zlib1.dll`。

这些是底层音视频库的依赖调整。请用新包 `bin` **整包覆盖**你的分发目录，不要按文件名增量拷贝，
以免残留已不再需要的旧 DLL。
</Warning>
</Step>
</Steps>

<Note>
`bin` 目录的内容会随版本调整，所以推荐**整体拷贝**而不是按文件名逐个挑选 —— 逐个挑选在升级
SDK 时很容易漏掉新增的依赖库。
</Note>

---

### 下一步

+ [快速开始](/zh/meeting/windows/quickstart) —— 登录、创建会议、进入会议
+ [核心概念](/zh/meeting/key-concepts) —— 房间、会议、成员与角色
+ [Token 与鉴权](/zh/meeting/token) —— token 由你的后端签发
