---
title: "Quickstart"
description: "Get started with the SRTC Python SDK: join a channel, receive each user's PCM audio frame by frame, and push TTS audio back into the channel, with minimal runnable examples."
---

This page gets the Python SDK working with two minimal examples: first **listening** (join a channel and record each person's voice to a wav file), then **speaking** (push a chunk of PCM into the channel so others can hear it).

Prerequisites:

+ You have run `pip install srtc`; see [Integration](/en/rtc/python/integration)
+ Your server can already issue channel join tokens; see [Server API · Get a channel join token](/en/rtc/server-api/channel)
+ Join the same channel from any other client, such as Web or an app, to talk and listen

<Note>
A token is bound to one session, so **every `Channel.join` needs a freshly issued token**. Reusing the same token is rejected by the server with `1032` (session is not online).
</Note>

---

## Listening: record each person's voice to wav

```python
import asyncio
import wave

import srtc


async def main(token: str):
    files: dict[str, wave.Wave_write] = {}
    fmt = srtc.AudioFormat(sample_rate=16000, channels=1)      # Format of received PCM; 16 kHz mono is the default

    async with await srtc.Channel.join(token, auto_subscribe_audio=True, audio_format=fmt) as ch:
        print(f"Joined {ch.info.channel}, I am {ch.me.uid}")

        async for frame in ch.audio_frames():               # All subscribed remote audio, arriving frame by frame
            wf = files.get(frame.uid)
            if wf is None:
                wf = files[frame.uid] = wave.open(f"{frame.uid}.wav", "wb")
                wf.setnchannels(fmt.channels)
                wf.setsampwidth(2)                          # S16LE
                wf.setframerate(fmt.sample_rate)
            wf.writeframes(frame.pcm)


asyncio.run(main("<token issued by your server>"))
```

Key points:

+ `auto_subscribe_audio=True` automatically subscribes to the audio of **everyone** in the channel (including people who join later)
+ `frame.uid` identifies the speaker; `frame.pcm` is S16LE interleaved PCM, and `frame.to_numpy()` gives you an `int16` array directly
+ When the remote side is silent it sends no packets; the SDK fills in silence frames of equal length (`frame.is_silence` is `True`), so the recorded duration matches the real duration
+ Exiting `async with` leaves the channel automatically; `async for` ends naturally when, for example, the channel is destroyed or you are removed from the channel

---

## Speaking: push PCM into the channel

```python
import asyncio

import numpy as np

import srtc


async def main(token: str):
    async with await srtc.Channel.join(token) as ch:
        # Publish an audio track; write() accepts 24 kHz mono PCM (any sample rate works, the SDK resamples internally)
        tts = await ch.publish_audio(desc="tts", audio_format=srtc.AudioFormat(24000, 1))

        # A 3-second 440 Hz sine wave stands in for TTS output here
        t = np.arange(24000 * 3) / 24000
        pcm = (np.sin(2 * np.pi * 440 * t) * 8000).astype(np.int16)

        await tts.write(pcm)              # Write any length at once; the SDK sends one frame every 20 ms at real-time pace
        await tts.wait_for_playout()      # Wait until everything is sent before leaving


asyncio.run(main("<token issued by your server>"))
```

Key points:

+ **You don't pace it yourself**: TTS generates much faster than real time, so writing several seconds of audio in one `write` is normal usage; the SDK sends it out at real-time pace
+ When the buffer exceeds `max_buffer_seconds` (30 seconds by default), `write` waits, which naturally provides backpressure
+ When the user barges in, call `tts.clear()` to discard whatever hasn't played yet immediately; see [Voice AI agent guide](/en/rtc/python/advanced/ai-agent)

---

## Listening for channel events

When you need to know who joined and who published what, subclass `ChannelHandler` and override the methods you need:

```python
class Printer(srtc.ChannelHandler):
    def on_user_join(self, user: srtc.UserInfo):
        print("Joined:", user.uid, user.name)

    def on_user_leave(self, uid: str):
        print("Left:", uid)

    async def on_disconnected(self, reason: srtc.DisconnectReason, error):
        print("Disconnected:", reason.name, error or "")


ch = await srtc.Channel.join(token, handler=Printer())
```

Methods can be regular functions or `async` functions. For the full list, see [Event callbacks](/en/rtc/python/api-reference/events).

---

### Next steps

+ [Voice AI agent guide](/en/rtc/python/advanced/ai-agent): sentence segmentation, barge-in interruption, latency
+ [Integrating pipecat](/en/rtc/python/advanced/pipecat)
+ [API reference](/en/rtc/python/api-reference/channel)
