---
title: "Channel"
description: "Reference for Channel, the SRTC Python SDK's core entry point: joining and leaving a channel, querying users and channel info, subscribing to remote audio and video, publishing audio, and consuming media frame by frame via async for. Read to look up a method's parameters, returns, and exceptions."
---

`srtc.Channel` represents a joined channel connection. It's created with `await Channel.join(...)`, supports `async with`, and leaves the channel automatically on exit. One process can hold multiple `Channel` objects at the same time, independent of each other.

Call every method within the asyncio event loop. On failure, it raises [`srtc.SdkError`](/en/rtc/python/error-codes).

---

## Lifecycle

### Channel.join

```python
@classmethod
async def join(
    cls,
    token: str,
    *,
    handler: ChannelHandler | None = None,
    auto_subscribe_audio: bool = False,
    auto_subscribe_video: bool = False,
    audio_format: AudioFormat = AudioFormat(),
    decode_video: bool = False,
    timeout: float = 20.0,
) -> Channel
```

Joins a channel and returns once the connection is established.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `token` | `str` | Yes | Channel join token issued by your server; see [Server API · Get a channel join token](/en/rtc/server-api/channel). Every `join` needs a newly issued token |
| `handler` | `ChannelHandler` | No | Event handler; see [Event callbacks](/en/rtc/python/api-reference/events) |
| `auto_subscribe_audio` | `bool` | No | Automatically subscribe to everyone's audio (including users who join later). Usually enabled for voice agents |
| `auto_subscribe_video` | `bool` | No | Automatically subscribe to everyone's video |
| `audio_format` | `AudioFormat` | No | The PCM format in which decoded remote audio is handed to you; default 16 kHz mono |
| `decode_video` | `bool` | No | Whether to decode remote video into RGB images (`VideoFrame.image`). When off, only encoded data is provided |
| `timeout` | `float` | No | Join timeout (seconds) |

**Raises:** `SdkError`. Common ones include an invalid token (`1021` / `1032`), the concurrency limit being reached (`1033`), and no available node (`1034` / `1035`); see [Error codes](/en/rtc/python/error-codes).

```python
async with await srtc.Channel.join(token, auto_subscribe_audio=True) as ch:
    ...
```

### leave

```python
async def leave() -> None
```

Leaves the channel and releases resources. Safe to call more than once; with `async with`, it's called automatically on exit.

### wait_closed

```python
async def wait_closed() -> DisconnectReason | None
```

Waits until the channel is fully disconnected (leaving voluntarily, being removed from the channel, being replaced by another session with the same uid, the channel being destroyed, and so on), and returns the disconnect reason. Suitable for services that "keep running until the channel ends":

```python
reason = await ch.wait_closed()
if reason in (srtc.DisconnectReason.KICKED, srtc.DisconnectReason.REPLACE):
    return       # Removed from the channel / replaced: don't rejoin automatically
```

<Note>
Brief disconnects caused by network jitter are reconnected automatically by the SDK; `on_connection_state(RECONNECTING)` fires during that time, and `wait_closed` doesn't end. It returns only when reconnection is abandoned and the channel is fully left.
</Note>

### closed

```python
@property
def closed() -> bool
```

Whether the channel is fully disconnected.

### disconnect_reason

```python
disconnect_reason: DisconnectReason | None
```

The disconnect reason; `None` when not disconnected.

---

## Querying info

The following properties read the local cache without going over the network, so you can call them at any time.

| Member | Type | Description |
| --- | --- | --- |
| `me` | `UserInfo` | Local user info (`uid`, `sid`, etc.) |
| `info` | `ChannelInfo` | Channel info |
| `users` | `list[UserInfo]` | All users in the channel, **including the local user** |
| `get_user(uid)` | `UserInfo \| None` | The specified user; returns `None` if not in the channel |
| `connection_quality` | `ConnectionQuality \| None` | The latest uplink and downlink network quality; `None` if none has been received yet |

---

## Subscribing

When `auto_subscribe_audio` / `auto_subscribe_video` is enabled, you don't need to subscribe manually.

### subscribe_audio / subscribe_video

```python
async def subscribe_audio(uid: str, track_id: str) -> None
async def subscribe_video(uid: str, track_id: str) -> None
```

Subscribes to one remote audio / video track and returns after server negotiation completes. `uid` and `track_id` come from the `on_track_added` event or `UserInfo.stream_tracks`.

To subscribe to the channel's composite stream, pass `srtc.MCU_PUBLISHER_UID` as `uid`, and `srtc.TRACK_AMCU_ID` (audio) or `srtc.TRACK_MCU_ID` (video) as `track_id`.

<Warning>
To "hear the whole channel", use `auto_subscribe_audio=True` to receive each user's audio separately; **don't** subscribe to the audio composite stream: it contains the agent's own voice and causes echo.
</Warning>

### unsubscribe

```python
async def unsubscribe(uid: str, track_id: str) -> None
```

Unsubscribes.

### request_key_frame

```python
def request_key_frame(uid: str, track_id: str) -> None
```

Asks the remote video to send a key frame immediately; the SDK internally limits this to at most once per second. When `decode_video` is on, the SDK requests one automatically on decoding errors, so you usually don't need to call it manually.

### switch_layer

```python
async def switch_layer(pub_uid: str, track_id: str, target_track_id: str) -> None
```

When the remote side publishes multi-layer (simulcast) video, switches the subscribed layer manually; the result is notified through `on_layer_switched`.

---

## Publishing

### publish_audio

```python
async def publish_audio(
    *,
    desc: str = "mic",
    audio_format: AudioFormat = AudioFormat(sample_rate=48000),
    bitrate: int = 32000,
    max_buffer_seconds: float = 30.0,
    props: dict | None = None,
) -> AudioTrack
```

Publishes one audio track and returns an [`AudioTrack`](/en/rtc/python/api-reference/audio#audiotrack); then push data with `await track.write(pcm)`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `desc` | `str` | No | Track description, seen by other clients in `TrackInfo.desc`; at most 63 bytes |
| `audio_format` | `AudioFormat` | No | The PCM format accepted by `write()`: any sample rate, 1 or 2 channels. Just set it to your TTS output format |
| `bitrate` | `int` | No | Opus bitrate (bps) |
| `max_buffer_seconds` | `float` | No | Upper limit of buffered audio not yet sent; beyond it, `write()` waits |
| `props` | `dict` | No | Custom track properties, seen by other clients in `TrackInfo.props` |

**Raises:** `SdkError`, such as publishing negotiation failure (`180300`) or timeout (`180302`).

### unpublish

```python
async def unpublish(track: AudioTrack) -> None
```

Unpublishes. Audio not yet sent is discarded.

---

## Consuming media data

Choose either approach: implement `on_audio_frame` / `on_video_frame` in `ChannelHandler`, or use the `async for` below. The latter fits linear AI processing flows better.

### audio_frames

```python
async def audio_frames() -> AsyncIterator[AudioFrame]
```

Yields remote audio from all subscribed tracks frame by frame (use `frame.uid` to tell speakers apart), in the `audio_format` given when joining. Iteration ends naturally after the channel disconnects.

```python
async for frame in ch.audio_frames():
    asr.feed(frame.uid, frame.to_numpy())
```

### video_frames

```python
async def video_frames() -> AsyncIterator[VideoFrame]
```

Yields remote video from all subscribed tracks frame by frame.

<Note>
When consumption can't keep up, the SDK drops the oldest frames (the audio buffer holds about 10 seconds, video 60 frames), so latency doesn't grow without bound. You can run multiple `async for` loops at the same time, and each one gets all frames.
</Note>
