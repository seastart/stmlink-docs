---
title: "音视频数据"
description: "Python SDK 的媒体数据类型：发布用的 AudioTrack（write 推 PCM、clear 打断、背压与实时控速），以及收到的 AudioFrame / VideoFrame 的字段、时间轴与静音帧语义，和格式参数 AudioFormat。"
---

## AudioFormat

```python
@dataclass(frozen=True)
class AudioFormat:
    sample_rate: int = 16000
    channels: int = 1
```

PCM 格式。SDK 收发的 PCM 一律是 **S16LE、交错排列**。

| 字段 | 说明 |
| --- | --- |
| `sample_rate` | 采样率，任意值（常见 8000 / 16000 / 24000 / 44100 / 48000） |
| `channels` | 声道数，1 或 2 |

---

## AudioTrack

`Channel.publish_audio` 返回的本地音频轨道。

### write

```python
async def write(pcm: bytes | np.ndarray) -> None
```

写入 PCM（格式为发布时指定的 `audio_format`），长度任意。SDK 切成 20ms 一帧，**按实时节奏**发送。

+ `bytes`：S16LE 交错 PCM，字节数必须是 `2 × 声道数` 的整数倍，否则抛 `ValueError`
+ `np.ndarray`：会转成 `int16`，双声道请按交错顺序展平

尚未发送的音频超过 `max_buffer_seconds` 时，`write` 会等待到缓冲有空位再返回（背压）。

<Note>
**空闲时 SDK 会持续发送静音帧**，保持 RTP 时间戳与真实时间同步。所以两句话之间停顿多久都没关系，下一句不会被对端当成迟到的数据丢掉。
</Note>

### clear

```python
def clear() -> None
```

立即丢弃所有尚未发送的音频。用户插话时调用，见 [语音 AI Agent 实践](/zh/rtc/python/advanced/ai-agent#插话打断（barge-in）)。

### wait_for_playout

```python
async def wait_for_playout() -> None
```

等待已写入的音频全部发送完毕。

### buffered_seconds

```python
@property
def buffered_seconds() -> float
```

尚未发送的音频时长（秒）。大于 0 表示 agent 还在"说话"。

---

## AudioFrame

一帧已解码的远端音频。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `str` | 说话人 uid |
| `track_id` | `str` | 轨道 ID（同一个人可能发布多路音频） |
| `pcm` | `bytes` | S16LE 交错 PCM |
| `sample_rate` | `int` | 采样率（等于入会时的 `audio_format`） |
| `channels` | `int` | 声道数 |
| `samples` | `int` | 每声道采样数 |
| `pts` | `int` | 该帧第一个采样在这条轨道时间轴上的位置（按 `sample_rate` 计的采样序号，从 0 开始） |
| `is_silence` | `bool` | `True` 表示对端 DTX 静音期间由 SDK 补出的静音帧 |
| `duration` | `float` | 帧时长（秒），`samples / sample_rate` |

| 方法 | 说明 |
| --- | --- |
| `to_numpy()` | 转为 `int16` 数组，形状 `(samples, channels)`，零拷贝 |

同一条轨道上，相邻两帧满足 `下一帧.pts == 上一帧.pts + 上一帧.samples`，时间轴连续。

---

## VideoFrame

一帧远端视频。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `str` | 发布者 uid |
| `track_id` | `str` | 轨道 ID |
| `codec` | `int` | 编码格式，`Codec` 枚举值（常见 `H264` / `VP8`） |
| `encoded` | `bytes` | 编码数据（H264 为 Annex-B），始终提供 |
| `rtp_timestamp` | `int` | 90kHz RTP 时间戳 |
| `image` | `np.ndarray \| None` | 解码后的 RGB24 图像，形状 `(高, 宽, 3)`。仅在入会时 `decode_video=True` 才有 |
| `width` / `height` | `int` | 图像尺寸，未解码时为 0 |

<Note>
解码后的图像是每一帧都给的。给视觉模型用时通常不需要这么高的帧率，按需抽帧即可（例如每秒取一帧）。
</Note>
