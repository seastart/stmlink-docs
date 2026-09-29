---
title: "Audio and video data"
description: "Media data types of the SRTC Python SDK: AudioTrack for publishing (write to push PCM, clear to interrupt, backpressure and real-time pacing), the fields, timeline, and silence-frame semantics of received AudioFrame / VideoFrame, and the AudioFormat format parameter."
---

## AudioFormat

```python
@dataclass(frozen=True)
class AudioFormat:
    sample_rate: int = 16000
    channels: int = 1
```

PCM format. All PCM sent and received by the SDK is **S16LE, interleaved**.

| Field | Description |
| --- | --- |
| `sample_rate` | Sample rate, any value (commonly 8000 / 16000 / 24000 / 44100 / 48000) |
| `channels` | Number of channels, 1 or 2 |

---

## AudioTrack

The local audio track returned by `Channel.publish_audio`.

### write

```python
async def write(pcm: bytes | np.ndarray) -> None
```

Writes PCM (in the `audio_format` specified when publishing) of any length. The SDK splits it into 20 ms frames and sends them **at real-time pace**.

+ `bytes`: S16LE interleaved PCM; the byte count must be a multiple of `2 × number of channels`, otherwise `ValueError` is raised
+ `np.ndarray`: converted to `int16`; for stereo, flatten it in interleaved order

When the audio not yet sent exceeds `max_buffer_seconds`, `write` waits until there's room in the buffer before returning (backpressure).

<Note>
**When idle, the SDK keeps sending silence frames**, keeping RTP timestamps in sync with real time. So however long the pause between two sentences, the next sentence isn't dropped by the remote side as late data.
</Note>

### clear

```python
def clear() -> None
```

Immediately discards all audio not yet sent. Call it when the user barges in; see [Voice AI agent guide](/en/rtc/python/advanced/ai-agent#barge-in-interruption).

### wait_for_playout

```python
async def wait_for_playout() -> None
```

Waits until all written audio has been sent.

### buffered_seconds

```python
@property
def buffered_seconds() -> float
```

Duration of audio not yet sent (seconds). Greater than 0 means the agent is still "speaking".

---

## AudioFrame

A decoded frame of remote audio.

| Field | Type | Description |
| --- | --- | --- |
| `uid` | `str` | Speaker's uid |
| `track_id` | `str` | Track ID (the same user may publish multiple audio tracks) |
| `pcm` | `bytes` | S16LE interleaved PCM |
| `sample_rate` | `int` | Sample rate (equal to the `audio_format` given when joining) |
| `channels` | `int` | Number of channels |
| `samples` | `int` | Samples per channel |
| `pts` | `int` | Position of the frame's first sample on this track's timeline (a sample index at `sample_rate`, starting from 0) |
| `is_silence` | `bool` | `True` means a silence frame filled in by the SDK during the remote side's DTX silence |
| `duration` | `float` | Frame duration (seconds), `samples / sample_rate` |

| Method | Description |
| --- | --- |
| `to_numpy()` | Converts to an `int16` array with shape `(samples, channels)`, zero-copy |

On the same track, two adjacent frames satisfy `next.pts == prev.pts + prev.samples`, so the timeline is continuous.

---

## VideoFrame

A frame of remote video.

| Field | Type | Description |
| --- | --- | --- |
| `uid` | `str` | Publisher's uid |
| `track_id` | `str` | Track ID |
| `codec` | `int` | Encoding format, a `Codec` enum value (commonly `H264` / `VP8`) |
| `encoded` | `bytes` | Encoded data (Annex-B for H264), always provided |
| `rtp_timestamp` | `int` | 90 kHz RTP timestamp |
| `image` | `np.ndarray \| None` | Decoded RGB24 image with shape `(height, width, 3)`. Only available with `decode_video=True` at join time |
| `width` / `height` | `int` | Image size; 0 when not decoded |

<Note>
A decoded image is provided for every frame. Vision models usually don't need such a high frame rate, so sample frames as needed (for example, one frame per second).
</Note>
