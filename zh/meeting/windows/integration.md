---
title: "集成"
description: "Windows SMeeting 会议 SDK 的下载地址、环境要求、工程配置与运行时依赖部署"
---

### 环境要求

<Warning>
**SDK 为 x86（32 位）**。你的工程必须以 **Win32 / x86** 为目标平台编译 —— 64 位程序无法链接
32 位的 `SMeeting.lib`，表现为链接期报「模块计算机类型 x86 与目标计算机类型 x64 冲突」。
</Warning>

+ 目标平台：Windows x86（32 位）
+ 语言：C++
+ 运行时：SDK 包内已附带所需的 VC++ 运行库 DLL，**无需**在目标机器上单独安装运行库分发包

---

### 下载 SDK

| 版本 | 下载地址 |
| --- | --- |
| 2.0 | [meeting-win-sdk-2.0.zip](https://repo.open.seastart.cn/repository/vcs-releases/meeting-win-sdk-2.0.zip) |

新版本发布后按同样的命名规则取用，替换版本号即可：

```text
https://repo.open.seastart.cn/repository/vcs-releases/meeting-win-sdk-<版本号>.zip
```

<Note>
会议 SDK 包里**已经包含底层音视频库**（`srtc.dll` 等），不需要再单独下载 SRTC 的 Windows SDK。
</Note>

---

### 目录结构

解压后得到：

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
    └── plugin/           # 插件及其 xml 配置
```

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
    ├── *.dll
    └── *.xml
```

<Warning>
两个容易遗漏的点：

+ **`plugin/` 必须保持为子目录**，不能把里面的 DLL 平铺到根目录
+ **`plugin/` 下的 `.xml` 配置文件也要一起拷贝**（`conf.xml`、`cocktail_service.xml`、
  `linkmic_service.xml`），缺失会导致插件加载失败，表现为屏幕共享等功能不可用
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
