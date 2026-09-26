---
title: "语音 AI Agent 实践"
description: "用 Python SDK 搭语音机器人时的关键做法：按说话人断句、用户插话时立即打断播报、DTX 静音补帧与时间轴、采样率怎么选、如何只听特定的人。做 ASR/LLM/TTS 管线前读这页。"
---

一个语音 agent 的主循环是：**收 PCM → 断句 → ASR → LLM → TTS → 推 PCM**。SDK 负责两头的收发与编解码，本页讲中间最容易做错的几件事。

---

### 完整骨架

```python
import asyncio

import numpy as np

import srtc

RATE = 16000


async def respond(uid: str, utterance: np.ndarray) -> bytes:
    """ASR → LLM → TTS，返回要播放的 PCM（16k 单声道）。替换成你的实现。"""
    text = await asr.transcribe(utterance, RATE)
    reply = await llm.chat(uid, text)
    return await tts.synthesize(reply, sample_rate=RATE)


async def main(token: str):
    async with await srtc.Channel.join(token, auto_subscribe_audio=True,
                                       audio_format=srtc.AudioFormat(RATE, 1)) as ch:
        speaker = await ch.publish_audio(desc="agent", audio_format=srtc.AudioFormat(RATE, 1))
        vad = MyVad()                      # 你的 VAD，按 uid 维护状态
        reply_task: asyncio.Task | None = None

        async def reply(uid, utterance):
            await speaker.write(await respond(uid, utterance))

        async for frame in ch.audio_frames():
            speaking, utterance = vad.feed(frame.uid, frame.to_numpy()[:, 0])

            # 用户开口时 agent 还在播：立即打断
            if speaking and speaker.buffered_seconds > 0:
                speaker.clear()
                if reply_task:
                    reply_task.cancel()

            # 一句话说完：异步生成回复，不阻塞收音
            if utterance is not None:
                reply_task = asyncio.create_task(reply(frame.uid, utterance))
```

<Tip>
**回复一定要放到独立的 Task 里生成**（`asyncio.create_task`）。如果在 `async for` 里直接 `await respond(...)`，生成回复的几秒里收不到新的音频帧，既无法检测插话，帧还会在缓冲里堆积。
</Tip>

---

### 插话打断（barge-in）

`AudioTrack.clear()` 会立即丢弃所有尚未发出的音频。由于 SDK 每 20ms 只发一帧、不会提前把缓冲发出去，**调用 `clear()` 后对端最多再听到几十毫秒的尾音**。

判断"用户开口"建议用 VAD 而不是音量阈值：环境噪声、对端的回声都可能超过简单阈值，导致 agent 被自己误打断。

用 `speaker.buffered_seconds > 0` 判断 agent 是否还在播；`await speaker.wait_for_playout()` 可以等一句话完整播完（例如播完再挂断）。

---

### 静音帧与时间轴

发送端开启 DTX 时，对端不说话就几乎不发包。如果直接把收到的包拼起来，**静音段会被压缩掉**，时间轴就错了：VAD 等不到尾部静音判断不了句子结束，录音时长也会变短。

SDK 按 RTP 时间戳自动补齐这些空洞：

+ 补出的帧 `frame.is_silence` 为 `True`，`frame.pcm` 全零，时长与真实空洞一致
+ `frame.pts` 是该帧在这条轨道时间轴上的位置（按输出采样率计的采样序号），前后帧严格首尾相接
+ 单次最多补 5 秒。对端长时间闭麦时只补 5 秒，`pts` 仍按真实时长推进

<Warning>
补帧发生在**下一个包到达时**。对端彻底闭麦（完全不发包）期间，你收不到任何帧。如果 VAD 需要靠持续的静音来判断"说完了"，请额外加一个超时：超过一定时间没收到某个 uid 的帧，就当作这句话已经结束。
</Warning>

---

### 采样率怎么选

+ **收**：按 ASR 模型的要求设 `audio_format`，大多数模型用 16k 单声道（这也是默认值）。SDK 内部从 48k 重采样，不需要你再处理
+ **发**：`publish_audio` 的 `audio_format` 设成 **TTS 输出的格式**（常见 16k / 24k / 44.1k），SDK 内部统一重采样到 48k 编码。不要自己重采样
+ 双声道只在确实需要立体声时使用，语音场景单声道即可

---

### 只听特定的人

`auto_subscribe_audio=True` 会订阅所有人。只想听某几个人（比如只听主讲人，不听其他 agent）时，关掉自动订阅，在轨道事件里自己决定：

```python
class Router(srtc.ChannelHandler):
    def __init__(self):
        self.ch: srtc.Channel | None = None

    async def on_track_added(self, track: srtc.TrackInfo):
        if track.kind == srtc.TrackKind.AUDIO and track.uid.startswith("teacher"):
            await self.ch.subscribe_audio(track.uid, track.id)


router = Router()
ch = await srtc.Channel.join(token, handler=router)     # 不开 auto_subscribe_audio
router.ch = ch
for user in ch.users:                                   # 入会前就已发布的轨道也要订
    for track in user.stream_tracks:
        await router.on_track_added(track)
```

<Note>
`on_user_join` / `on_track_added` 只通知**入会之后**发生的变化。入会前已经在频道里的用户和轨道，请用 `ch.users` 读取。
</Note>

---

### 多个会话

一个进程里可以同时 `join` 多个频道，每个 `Channel` 相互独立，适合"一个进程服务多个房间"。每次 `join` 都要用单独签发的 Token。并发量与 CPU 的关系见 [集成方式 · 部署注意](/zh/rtc/python/integration#部署注意)。
