---
title: "Integrating pipecat"
description: "Connect an existing pipecat voice agent pipeline to an SRTC channel with SRTCTransport: installation, parameters, events, barge-in interruption behavior, and how it differs from pipecat's other transports."
---

[pipecat](https://github.com/pipecat-ai/pipecat) is a widely used open-source voice agent framework. The SDK has a built-in pipecat transport: **replace the Daily / LiveKit transport in the examples with `SRTCTransport`**, and the rest of the pipeline stays unchanged.

### Installation

```bash
pip install "srtc[pipecat]"
```

Requires pipecat 1.0 or later.

---

### Usage

```python
from pipecat.frames.frames import EndFrame, TTSSpeakFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask

from srtc.pipecat_transport import SRTCParams, SRTCTransport

transport = SRTCTransport(
    token,                                   # Channel join token issued by your server
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
    await task.queue_frame(TTSSpeakFrame("Hi, I'm your AI assistant"))


@transport.event_handler("on_participant_disconnected")
async def on_left(transport, uid):
    await task.queue_frame(EndFrame())


await PipelineRunner().run(task)
```

---

### Behavior

+ **Input**: automatically subscribes to the audio of everyone in the channel, decodes it at the pipeline's input sample rate, and pushes it out as `UserAudioRawFrame(user_id=uid)`. Silence frames that the SDK fills in during the remote side's DTX silence are pushed out as usual, so the VAD can correctly tell when a sentence ends
+ **Output**: publishes one audio track. `write_audio_frame` blocks at real-time pace, with the same semantics as pipecat's other transports
+ **Barge-in interruption**: when an `InterruptionFrame` is received, audio that hasn't been sent yet is cleared immediately, and the remote side hears at most about 100 ms of trailing audio
+ **Leaving**: when the pipeline ends (`EndFrame` / `CancelFrame`), it leaves the channel automatically

---

### Parameters

`SRTCParams` inherits pipecat's `TransportParams`. Common options:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `audio_in_enabled` | `bool` | `False` | Whether to receive channel audio |
| `audio_out_enabled` | `bool` | `False` | Whether to publish bot audio |
| `audio_in_sample_rate` | `int` | From pipeline params | Input PCM sample rate |
| `audio_out_sample_rate` | `int` | From pipeline params | Output PCM sample rate |
| `audio_out_bitrate` | `int` | `96000` | Sending bitrate (bps) |
| `audio_out_desc` | `str` | `"agent"` | Description of the published track, seen by other clients in `TrackInfo.desc` |
| `join_timeout` | `float` | `20.0` | Join timeout (seconds) |

---

### Events

Register with `@transport.event_handler("event_name")`; the handler's first parameter is the transport:

| Event | Parameters | When it fires |
| --- | --- | --- |
| `on_connected` | — | Joined the channel |
| `on_disconnected` | `reason: DisconnectReason` | Left the channel (including being removed from the channel and the channel being destroyed) |
| `on_first_participant_joined` | `uid: str` | The first other user appears (users already in the channel before you joined count too) |
| `on_participant_connected` | `uid: str` | Someone joined |
| `on_participant_disconnected` | `uid: str` | Someone left |
| `on_custom_msg` | `msg: CustomMsg` | An in-channel custom message was received |

When you need more capabilities (querying users, subscribing to video, and so on), after joining you can get the underlying [`srtc.Channel`](/en/rtc/python/api-reference/channel) through `transport.channel`.

---

### Differences from other transports

<Warning>
**Sending messages isn't supported.** The SRTC client only receives messages and doesn't send them; `OutputTransportMessageFrame` is ignored (with a one-time warning log). To send messages into the channel, have your backend call [Server API · Send a custom message](/en/rtc/server-api/channel).
</Warning>

This transport currently handles audio only and doesn't send or receive video frames.
