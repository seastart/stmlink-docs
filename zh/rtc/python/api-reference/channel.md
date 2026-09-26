---
title: "Channel"
description: "Python SDK 的核心入口 Channel：加入与离开频道、查询成员与频道信息、订阅远端音视频、发布音频、用 async for 逐帧消费媒体数据。查某个方法的参数、返回值和异常时读这页。"
---

`srtc.Channel` 代表一个已加入的频道连接。通过 `await Channel.join(...)` 创建，支持 `async with`，退出时自动离开。一个进程里可以同时存在多个 `Channel`，彼此独立。

所有方法都要在 asyncio 事件循环里调用。失败时抛出 [`srtc.SdkError`](/zh/rtc/python/error-codes)。

---

## 生命周期

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

加入频道，连接建立后返回。

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | `str` | 是 | 服务端签发的加入频道 Token，见 [服务端 API · 获取加入频道 token](/zh/rtc/server-api/channel)。每次 `join` 都要用新签发的 Token |
| `handler` | `ChannelHandler` | 否 | 事件处理器，见 [事件回调](/zh/rtc/python/api-reference/events) |
| `auto_subscribe_audio` | `bool` | 否 | 自动订阅所有人（含之后加入者）的音频。语音 agent 通常开启 |
| `auto_subscribe_video` | `bool` | 否 | 自动订阅所有人的视频 |
| `audio_format` | `AudioFormat` | 否 | 远端音频解码后交给你的 PCM 格式，默认 16k 单声道 |
| `decode_video` | `bool` | 否 | 是否把远端视频解码成 RGB 图像（`VideoFrame.image`）。关闭时只提供编码数据 |
| `timeout` | `float` | 否 | 入会超时（秒） |

**异常**：`SdkError`。常见的有 Token 失效（`1021` / `1032`）、并发已达上限（`1033`）、无可用节点（`1034` / `1035`），见 [错误码](/zh/rtc/python/error-codes)。

```python
async with await srtc.Channel.join(token, auto_subscribe_audio=True) as ch:
    ...
```

### leave

```python
async def leave() -> None
```

离开频道并释放资源。可重复调用；使用 `async with` 时退出会自动调用。

### wait_closed

```python
async def wait_closed() -> DisconnectReason | None
```

等待频道彻底断开（主动离开、被踢、被顶号、频道销毁等），返回断线原因。适合"一直运行到频道结束"的服务：

```python
reason = await ch.wait_closed()
if reason in (srtc.DisconnectReason.KICKED, srtc.DisconnectReason.REPLACE):
    return       # 被踢 / 顶号，不要自动重进
```

<Note>
网络抖动引起的短暂断线由 SDK 自动重连，期间触发 `on_connection_state(RECONNECTING)`，不会结束 `wait_closed`。只有放弃重连、彻底离开时才会返回。
</Note>

### closed

```python
@property
def closed() -> bool
```

频道是否已彻底断开。

### disconnect_reason

```python
disconnect_reason: DisconnectReason | None
```

断开原因，未断开时为 `None`。

---

## 信息查询

以下属性读取的是本地缓存，不走网络，可以随时调用。

| 成员 | 类型 | 说明 |
| --- | --- | --- |
| `me` | `UserInfo` | 本端信息（`uid`、`sid` 等） |
| `info` | `ChannelInfo` | 频道信息 |
| `users` | `list[UserInfo]` | 频道内所有用户，**含本端** |
| `get_user(uid)` | `UserInfo \| None` | 指定用户，不在频道内返回 `None` |
| `connection_quality` | `ConnectionQuality \| None` | 最近一次上下行网络质量，尚未收到时为 `None` |

---

## 订阅

开启了 `auto_subscribe_audio` / `auto_subscribe_video` 时不需要手动订阅。

### subscribe_audio / subscribe_video

```python
async def subscribe_audio(uid: str, track_id: str) -> None
async def subscribe_video(uid: str, track_id: str) -> None
```

订阅远端的某一路音频 / 视频，等待服务端协商完成后返回。`uid` 与 `track_id` 来自 `on_track_added` 事件或 `UserInfo.stream_tracks`。

订阅频道的合成流时，`uid` 传 `srtc.MCU_PUBLISHER_UID`，`track_id` 传 `srtc.TRACK_AMCU_ID`（音频）或 `srtc.TRACK_MCU_ID`（视频）。

<Warning>
想"听全场"请用 `auto_subscribe_audio=True` 分别收每个人的音频，**不要**订阅音频合成流：合成流里包含 agent 自己的声音，会形成回声。
</Warning>

### unsubscribe

```python
async def unsubscribe(uid: str, track_id: str) -> None
```

取消订阅。

### request_key_frame

```python
def request_key_frame(uid: str, track_id: str) -> None
```

请求远端视频立即发送关键帧，SDK 内部限制每秒最多一次。开启 `decode_video` 时，解码出错 SDK 会自动请求，一般无需手动调用。

### switch_layer

```python
async def switch_layer(pub_uid: str, track_id: str, target_track_id: str) -> None
```

对方发布了多层（simulcast）视频时，主动切换订阅的层，结果通过 `on_layer_switched` 通知。

---

## 发布

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

发布一路音频，返回 [`AudioTrack`](/zh/rtc/python/api-reference/audio#audiotrack)，之后用 `await track.write(pcm)` 推送数据。

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `desc` | `str` | 否 | 轨道描述，其他端在 `TrackInfo.desc` 里看到，最长 63 字节 |
| `audio_format` | `AudioFormat` | 否 | `write()` 接收的 PCM 格式，任意采样率，声道数 1 或 2。设成你的 TTS 输出格式即可 |
| `bitrate` | `int` | 否 | Opus 码率（bps） |
| `max_buffer_seconds` | `float` | 否 | 尚未发送的音频的缓冲上限，超过后 `write()` 会等待 |
| `props` | `dict` | 否 | 轨道自定义属性，其他端在 `TrackInfo.props` 里看到 |

**异常**：`SdkError`，如发布协商失败（`180300`）或超时（`180302`）。

### unpublish

```python
async def unpublish(track: AudioTrack) -> None
```

取消发布。未发出的音频会被丢弃。

---

## 消费媒体数据

两种方式任选：在 `ChannelHandler` 里实现 `on_audio_frame` / `on_video_frame`，或者用下面的 `async for`。后者更适合线性的 AI 处理流程。

### audio_frames

```python
async def audio_frames() -> AsyncIterator[AudioFrame]
```

逐帧产出所有已订阅轨道的远端音频（用 `frame.uid` 区分说话人），格式为入会时的 `audio_format`。频道断开后迭代自然结束。

```python
async for frame in ch.audio_frames():
    asr.feed(frame.uid, frame.to_numpy())
```

### video_frames

```python
async def video_frames() -> AsyncIterator[VideoFrame]
```

逐帧产出所有已订阅轨道的远端视频。

<Note>
消费速度跟不上时，SDK 会丢掉最旧的帧（音频缓冲约 10 秒，视频 60 帧），保证延迟不会无限增长。可以同时开多个 `async for`，每个都会拿到全部帧。
</Note>
