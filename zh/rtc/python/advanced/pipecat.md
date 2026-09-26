---
title: "接入 pipecat"
description: "用 SRTCTransport 把现有的 pipecat 语音 agent 管线接进 SRTC 频道：安装、参数、事件、插话打断的行为，以及与 pipecat 其它 transport 的差异。"
---

[pipecat](https://github.com/pipecat-ai/pipecat) 是常用的开源语音 agent 框架。SDK 内置了 pipecat transport，**把示例里的 Daily / LiveKit transport 换成 `SRTCTransport` 即可**，管线其余部分不用改。

### 安装

```bash
pip install "srtc[pipecat]"
```

需要 pipecat 1.0 及以上。

---

### 用法

```python
from pipecat.frames.frames import EndFrame, TTSSpeakFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask

from srtc.pipecat_transport import SRTCParams, SRTCTransport

transport = SRTCTransport(
    token,                                   # 服务端签发的加入频道 Token
    SRTCParams(audio_in_enabled=True, audio_out_enabled=True),
)

pipeline = Pipeline([
    transport.input(),
    stt,
    context_aggregator.user(),
    llm,
    tts,
    transport.output(),
    context_aggregator.assistant(),
])
task = PipelineTask(pipeline, params=PipelineParams(audio_in_sample_rate=16000))


@transport.event_handler("on_first_participant_joined")
async def on_joined(transport, uid):
    await task.queue_frame(TTSSpeakFrame("你好，我是 AI 助手"))


@transport.event_handler("on_participant_disconnected")
async def on_left(transport, uid):
    await task.queue_frame(EndFrame())


await PipelineRunner().run(task)
```

---

### 行为说明

+ **输入**：自动订阅频道里所有人的音频，按管线的输入采样率解码，以 `UserAudioRawFrame(user_id=uid)` 推出。对端 DTX 静音期间 SDK 补的静音帧也照常推出，VAD 才能正确判断句子结束
+ **输出**：发布一路音频轨道。`write_audio_frame` 按实时节奏阻塞，与 pipecat 其它 transport 语义一致
+ **插话打断**：收到 `InterruptionFrame` 时立即清掉尚未发出的音频，对端最多再听到约 100ms 尾音
+ **离开**：管线结束（`EndFrame` / `CancelFrame`）时自动离开频道

---

### 参数

`SRTCParams` 继承 pipecat 的 `TransportParams`，常用项：

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `audio_in_enabled` | `bool` | `False` | 是否接收频道音频 |
| `audio_out_enabled` | `bool` | `False` | 是否发布 bot 音频 |
| `audio_in_sample_rate` | `int` | 取管线参数 | 输入 PCM 采样率 |
| `audio_out_sample_rate` | `int` | 取管线参数 | 输出 PCM 采样率 |
| `audio_out_bitrate` | `int` | `96000` | 发送码率（bps） |
| `audio_out_desc` | `str` | `"agent"` | 发布轨道的描述，其他端在 `TrackInfo.desc` 里看到 |
| `join_timeout` | `float` | `20.0` | 入会超时（秒） |

---

### 事件

用 `@transport.event_handler("事件名")` 注册，处理函数的第一个参数是 transport：

| 事件 | 参数 | 触发时机 |
| --- | --- | --- |
| `on_connected` | — | 已加入频道 |
| `on_disconnected` | `reason: DisconnectReason` | 离开频道（含被踢、频道销毁） |
| `on_first_participant_joined` | `uid: str` | 第一个其他参会者出现（入会前已在频道的人也算） |
| `on_participant_connected` | `uid: str` | 有人加入 |
| `on_participant_disconnected` | `uid: str` | 有人离开 |
| `on_custom_msg` | `msg: CustomMsg` | 收到频道内自定义消息 |

需要更多能力（查询成员、订阅视频等）时，入会后可以通过 `transport.channel` 拿到底层的 [`srtc.Channel`](/zh/rtc/python/api-reference/channel)。

---

### 与其它 transport 的差异

<Warning>
**不支持发送消息。** SRTC 客户端只收不发消息，`OutputTransportMessageFrame` 会被忽略（打一次警告日志）。需要向频道内发消息时，请由你的业务服务端调用 [服务端 API · 发送自定义消息](/zh/rtc/server-api/channel)。
</Warning>

本 transport 目前只处理音频，不收发视频帧。
