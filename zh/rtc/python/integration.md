---
title: "集成方式"
description: "SRTC Python SDK 适合什么场景、怎么安装、支持哪些平台，以及 asyncio 线程模型与部署时的 fork、容量注意事项。接入 Python SDK 前先读这页。"
---

SRTC Python SDK（PyPI 包名 `srtc`）面向**服务端 AI 场景**：让你的 Python 服务以一个"参会者"的身份加入频道，收到频道里每个人的声音，再把合成好的声音推回去。

### 适用场景

+ AI 语音助手 / 语音机器人：ASR → LLM → TTS 管线接入频道
+ 服务端录音、质检、实时转写
+ 已有 [pipecat](https://github.com/pipecat-ai/pipecat) 语音 agent，想接到 SRTC 频道里（见 [接入 pipecat](/zh/rtc/python/advanced/pipecat)）

### 和 C SDK 的区别

两者底层是同一套原生内核，行为一致。区别在于**数据形态**：

| | Python SDK | [C SDK](/zh/rtc/capi/integration) |
| --- | --- | --- |
| 收到的音频 | 解码好的 **PCM**，采样率 / 声道数由你指定 | Opus 编码包，需自行解码 |
| 推送的音频 | 任意采样率的 **PCM**，SDK 负责重采样、编码、控速 | 编码好的 Opus 包，需自行按实时节奏写入 |
| 编程模型 | `asyncio`：`async with` / `async for` | C 回调 + 自管线程 |
| 视频 | 只收不发（可选解码成 RGB 图像） | 收发都支持（编码数据） |

模型的输入输出都是原始数据，所以 AI 场景用 Python SDK 基本不用碰编解码。

---

### 安装

```bash
pip install srtc                 # 核心
pip install "srtc[pipecat]"      # 同时安装 pipecat 集成
```

依赖只有 `cffi`、`av`（自带 ffmpeg 与 libopus，**不需要**在系统里另装 ffmpeg）、`numpy`。

### 支持平台

| 平台 | 架构 | 说明 |
| --- | --- | --- |
| Linux | x86_64、aarch64 | glibc 2.28 及以上可直接安装（Ubuntu 20.04+、Debian 10+、CentOS / Rocky 8+ 等）；更老的系统见下方说明 |
| macOS | Apple Silicon（arm64） | 11.0 及以上，主要用于本地开发调试 |
| Windows | x86_64 | |

Python 3.10 及以上。同一平台的安装包对所有 Python 3.x 小版本通用。

<Warning>
**glibc 低于 2.28 的系统（如 CentOS 7）**：SDK 本身支持到 glibc 2.17，但依赖 `av` 的新版本只提供 glibc 2.28+ 的安装包，
pip 会转而尝试从源码编译并失败。请固定 `av` 的版本安装：

```bash
pip install srtc "av>=12,<14"
```
</Warning>

<Note>
Alpine（musl）暂未提供 Python 安装包，需要的话请联系我们。
</Note>

---

### 线程模型

SDK 基于 `asyncio`，所有接口都要在事件循环里调用：

+ 信令、断线重连、音视频收发都在 SDK 内置的原生库里运行，**不占用 Python 的 GIL**，不会拖慢你的 Python 代码
+ 所有事件回调、`async for` 拿到的数据帧，都在**事件循环线程**里交给你，不需要加锁
+ 入会、订阅、发布这类要等服务端协商的接口是 `async` 的，等待期间不阻塞事件循环

<Warning>
事件回调里不要做同步的耗时操作（比如同步调用模型推理），那会卡住整个事件循环，所有频道的收发都会受影响。耗时处理请用 `await` 异步调用，或放到线程池 / 进程池里。
</Warning>

---

### 部署注意

**不要在已经使用过 SDK 的进程里 fork。** 原生内核在 fork 出的子进程里无法工作：

+ 只 `import srtc`、还没创建过 `Channel` 就 fork：没问题（gunicorn `--preload` 等场景可以正常用）
+ 已经创建过 `Channel` 再 fork：子进程里再用会直接抛 `RuntimeError`，不会卡死
+ 用 `multiprocessing` 时请设置 `multiprocessing.set_start_method("spawn")`

**容量参考。** 单进程实测（Apple M 系列，每个频道收 1 路 + 发 1 路音频）：20 个频道同时在线约占 61% 单核 CPU、181 MB 内存，零丢帧。Python 侧的编解码是单进程的上限所在，会话多时请多进程横向扩展。

<Tip>
每个频道连接都要用**单独签发**的 Token。Token 与一次会话绑定，同一个 Token 加入第二次会被服务端以 `1032` 拒绝。
</Tip>

---

### 下一步

+ [快速开始](/zh/rtc/python/quickstart)：跑通收听与播报
+ [语音 AI Agent 实践](/zh/rtc/python/advanced/ai-agent)：断句、插话打断、时间轴
+ [接口文档](/zh/rtc/python/api-reference/channel)
