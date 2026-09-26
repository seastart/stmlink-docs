---
title: "快速开始"
description: "SRTC Python SDK 快速上手：加入频道、逐帧拿到每个人的 PCM 音频、把 TTS 音频推回频道，附可直接运行的最小示例。"
---

本文用两个最小例子跑通 Python SDK：先**收听**（加入频道，把每个人的声音录成 wav），再**播报**（把一段 PCM 推进频道，让其他人听到）。

前置条件：

+ 已 `pip install srtc`，见 [集成方式](/zh/rtc/python/integration)
+ 你的服务端已经能签发加入频道的 Token，见 [服务端 API · 获取加入频道 token](/zh/rtc/server-api/channel)
+ 用 Web / App 等任意一端加入同一个频道，用来说话和收听

<Note>
Token 与一次会话绑定，**每次 `Channel.join` 都要用新签发的 Token**。复用同一个 Token 会被服务端以 `1032 该会话不在线` 拒绝。
</Note>

---

## 收听：把每个人的声音录成 wav

```python
import asyncio
import wave

import srtc


async def main(token: str):
    files: dict[str, wave.Wave_write] = {}
    fmt = srtc.AudioFormat(sample_rate=16000, channels=1)      # 收到的 PCM 格式，默认就是 16k 单声道

    async with await srtc.Channel.join(token, auto_subscribe_audio=True, audio_format=fmt) as ch:
        print(f"已加入 {ch.info.channel}，我是 {ch.me.uid}")

        async for frame in ch.audio_frames():               # 所有已订阅的远端音频，逐帧到达
            wf = files.get(frame.uid)
            if wf is None:
                wf = files[frame.uid] = wave.open(f"{frame.uid}.wav", "wb")
                wf.setnchannels(fmt.channels)
                wf.setsampwidth(2)                          # S16LE
                wf.setframerate(fmt.sample_rate)
            wf.writeframes(frame.pcm)


asyncio.run(main("<你的服务端签发的 token>"))
```

要点：

+ `auto_subscribe_audio=True` 会自动订阅频道里**所有人**（包括之后才加入的人）的音频
+ `frame.uid` 区分说话人，`frame.pcm` 是 S16LE 交错排列的 PCM，`frame.to_numpy()` 可以直接拿到 `int16` 数组
+ 对端静音时不发包，SDK 会补上等长的静音帧（`frame.is_silence` 为 `True`），所以录出来的时长和真实时长一致
+ `async with` 退出时自动离开频道；频道被销毁、被踢等情况下 `async for` 会自然结束

---

## 播报：把 PCM 推进频道

```python
import asyncio

import numpy as np

import srtc


async def main(token: str):
    async with await srtc.Channel.join(token) as ch:
        # 发布一路音频，write() 接收 24k 单声道 PCM（任意采样率都行，SDK 内部会重采样）
        tts = await ch.publish_audio(desc="tts", audio_format=srtc.AudioFormat(24000, 1))

        # 这里用 3 秒 440Hz 正弦波代替 TTS 输出
        t = np.arange(24000 * 3) / 24000
        pcm = (np.sin(2 * np.pi * 440 * t) * 8000).astype(np.int16)

        await tts.write(pcm)              # 一次写入任意长度，SDK 按实时节奏每 20ms 发一帧
        await tts.wait_for_playout()      # 等全部发完再离开


asyncio.run(main("<你的服务端签发的 token>"))
```

要点：

+ **不用自己控速**：TTS 生成速度远快于实时，一次性 `write` 几秒的音频是正常用法，SDK 会按实时节奏发出去
+ 缓冲超过 `max_buffer_seconds`（默认 30 秒）时 `write` 会等待，天然形成背压
+ 用户插话时调用 `tts.clear()`，未播完的部分立即丢弃，见 [语音 AI Agent 实践](/zh/rtc/python/advanced/ai-agent)

---

## 监听频道事件

需要知道谁进来了、谁发布了什么时，继承 `ChannelHandler`，覆写需要的方法即可：

```python
class Printer(srtc.ChannelHandler):
    def on_user_join(self, user: srtc.UserInfo):
        print("加入:", user.uid, user.name)

    def on_user_leave(self, uid: str):
        print("离开:", uid)

    async def on_disconnected(self, reason: srtc.DisconnectReason, error):
        print("已断开:", reason.name, error or "")


ch = await srtc.Channel.join(token, handler=Printer())
```

方法可以是普通函数，也可以是 `async` 函数。完整列表见 [事件回调](/zh/rtc/python/api-reference/events)。

---

### 下一步

+ [语音 AI Agent 实践](/zh/rtc/python/advanced/ai-agent)：断句、插话打断、延迟
+ [接入 pipecat](/zh/rtc/python/advanced/pipecat)
+ [接口文档](/zh/rtc/python/api-reference/channel)
