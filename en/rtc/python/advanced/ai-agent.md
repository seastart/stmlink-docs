---
title: "Voice AI agent guide"
description: "Key practices for building a voice bot with the SRTC Python SDK: segmenting speech per speaker, interrupting playback immediately when the user barges in, DTX silence filling and the timeline, choosing sample rates, and listening only to specific users. Read before building an ASR/LLM/TTS pipeline."
---

The main loop of a voice agent is: **receive PCM → segment into sentences → ASR → LLM → TTS → push PCM**. The SDK handles sending, receiving, encoding, and decoding at both ends; this page covers the things in between that are easiest to get wrong.

---

### Complete skeleton

```python
import asyncio

import numpy as np

import srtc

RATE = 16000


async def respond(uid: str, utterance: np.ndarray) -> bytes:
    """ASR → LLM → TTS; returns the PCM to play (16 kHz mono). Replace with your implementation."""
    text = await asr.transcribe(utterance, RATE)
    reply = await llm.chat(uid, text)
    return await tts.synthesize(reply, sample_rate=RATE)


async def main(token: str):
    async with await srtc.Channel.join(token, auto_subscribe_audio=True,
                                       audio_format=srtc.AudioFormat(RATE, 1)) as ch:
        speaker = await ch.publish_audio(desc="agent", audio_format=srtc.AudioFormat(RATE, 1))
        vad = MyVad()                      # Your VAD, keeping state per uid
        reply_task: asyncio.Task | None = None

        async def reply(uid, utterance):
            await speaker.write(await respond(uid, utterance))

        async for frame in ch.audio_frames():
            speaking, utterance = vad.feed(frame.uid, frame.to_numpy()[:, 0])

            # The user starts speaking while the agent is still playing: interrupt immediately
            if speaking and speaker.buffered_seconds > 0:
                speaker.clear()
                if reply_task:
                    reply_task.cancel()

            # A sentence is finished: generate the reply asynchronously without blocking audio reception
            if utterance is not None:
                reply_task = asyncio.create_task(reply(frame.uid, utterance))
```

<Tip>
**Always generate the reply in a separate Task** (`asyncio.create_task`). If you `await respond(...)` directly inside `async for`, no new audio frames arrive during the few seconds it takes to generate the reply, so you can't detect barge-in, and frames pile up in the buffer.
</Tip>

---

### Barge-in interruption

`AudioTrack.clear()` immediately discards all audio that hasn't been sent yet. Because the SDK sends only one frame every 20 ms and never sends the buffer ahead of time, **after you call `clear()`, the remote side hears at most a few tens of milliseconds of trailing audio**.

To decide "the user started speaking", we recommend a VAD rather than a volume threshold: ambient noise and the remote side's echo can both exceed a simple threshold, causing the agent to be falsely interrupted by itself.

Use `speaker.buffered_seconds > 0` to tell whether the agent is still playing; `await speaker.wait_for_playout()` waits until a sentence has finished playing completely (for example, to hang up after playback).

---

### Silence frames and the timeline

When the sender has DTX enabled, it sends almost no packets while the remote user isn't speaking. If you simply concatenate the packets you receive, **silent segments get squeezed out** and the timeline is wrong: the VAD never sees trailing silence and can't tell when a sentence ends, and recordings come out shorter.

The SDK fills these gaps automatically based on RTP timestamps:

+ Filled frames have `frame.is_silence` set to `True` and an all-zero `frame.pcm`, with a duration matching the real gap
+ `frame.pts` is the frame's position on this track's timeline (a sample index at the output sample rate), and consecutive frames join end to end exactly
+ At most 5 seconds are filled at a time. When the remote side has the microphone off for a long time, only 5 seconds are filled, and `pts` still advances by the real duration

<Warning>
Filling happens **when the next packet arrives**. While the remote side has the microphone fully off (sending no packets at all), you receive no frames. If your VAD relies on continuous silence to decide "they're done speaking", add a timeout: if no frames arrive from a given uid for a certain time, treat the sentence as finished.
</Warning>

---

### Choosing sample rates

+ **Receiving**: set `audio_format` to what your ASR model requires; most models use 16 kHz mono (which is also the default). The SDK resamples from 48 kHz internally, so you don't need to handle it
+ **Sending**: set the `audio_format` of `publish_audio` to **the format your TTS outputs** (commonly 16 / 24 / 44.1 kHz); the SDK resamples everything to 48 kHz internally for encoding. Don't resample yourself
+ Use stereo only when you really need it; mono is enough for voice scenarios

---

### Listening only to specific users

`auto_subscribe_audio=True` subscribes to everyone. When you only want to listen to certain users (for example, only the lecturer and not other agents), turn off auto-subscribe and decide yourself in the track event:

```python
class Router(srtc.ChannelHandler):
    def __init__(self):
        self.ch: srtc.Channel | None = None

    async def on_track_added(self, track: srtc.TrackInfo):
        if track.kind == srtc.TrackKind.AUDIO and track.uid.startswith("teacher"):
            await self.ch.subscribe_audio(track.uid, track.id)


router = Router()
ch = await srtc.Channel.join(token, handler=router)     # auto_subscribe_audio not enabled
router.ch = ch
for user in ch.users:                                   # Also subscribe to tracks published before you joined
    for track in user.stream_tracks:
        await router.on_track_added(track)
```

<Note>
`on_user_join` / `on_track_added` only notify you of changes that happen **after you join**. For users and tracks already in the channel before you joined, read `ch.users`.
</Note>

---

### Multiple sessions

One process can `join` multiple channels at the same time, and each `Channel` is independent—suitable for "one process serving multiple channels". Every `join` needs a separately issued token. For how concurrency relates to CPU, see [Integration · Deployment notes](/en/rtc/python/integration#deployment-notes).
