---
title: "事件回调"
description: "Python SDK 的 ChannelHandler 事件列表：连接状态、断线原因、成员进出、轨道增删、音视频帧、说话人、网络质量、自定义消息，各自的触发时机、参数和顺序保证。"
---

继承 `srtc.ChannelHandler`，覆写需要的方法，在 `Channel.join(token, handler=...)` 时传入。未覆写的事件会被忽略。

```python
class MyHandler(srtc.ChannelHandler):
    def on_user_join(self, user: srtc.UserInfo):          # 普通函数
        print("加入:", user.uid)

    async def on_disconnected(self, reason, error):       # 也可以是 async 函数
        await notify_ops(reason)
```

+ 所有方法都在 **asyncio 事件循环线程**里调用，不需要加锁
+ `async` 方法会作为 Task 调度，不会阻塞后续事件
+ 方法里抛出的异常会被记录到 `srtc` logger，不会中断 SDK

---

## 事件列表

| 方法 | 参数 | 触发时机 |
| --- | --- | --- |
| `on_connection_state` | `state: ConnectionState` | 连接状态变化：`CONNECTED`（已连接 / 重连成功）、`RECONNECTING`（网络中断，SDK 自动重连中）、`DISCONNECTED`（已断开） |
| `on_disconnected` | `reason: DisconnectReason`，`error: SdkError \| None` | 彻底离开频道，不会再自动重连。`reason` 见 [DisconnectReason](/zh/rtc/python/types#disconnectreason) |
| `on_user_join` | `user: UserInfo` | 有远端用户加入 |
| `on_user_leave` | `uid: str` | 有远端用户离开 |
| `on_track_added` | `track: TrackInfo` | 远端发布了新轨道。未开自动订阅时，在这里决定是否订阅 |
| `on_track_updated` | `track: TrackInfo` | 远端轨道信息变化 |
| `on_track_removed` | `track: TrackInfo` | 远端取消发布某路轨道 |
| `on_audio_frame` | `frame: AudioFrame` | 收到一帧已解码的远端音频（每路约每 20ms 一次） |
| `on_video_frame` | `frame: VideoFrame` | 收到一帧远端视频 |
| `on_active_speakers` | `speakers: list[ActiveSpeaker]` | 说话人变化，全量快照、按音量降序；空列表表示无人说话 |
| `on_connection_quality` | `quality: ConnectionQuality` | 上下行网络质量，约每秒一次 |
| `on_layer_switched` | `event: LayerSwitched` | 订阅的多层视频切层完成 |
| `on_custom_msg` | `msg: CustomMsg` | 收到频道内自定义消息（由业务服务端发出） |

<Note>
`on_active_speakers`、`on_connection_quality`、`on_layer_switched` 依赖频道的流媒体引擎，部分部署下不会触发。业务逻辑请不要依赖它们一定到达。
</Note>

---

## 顺序与时机

<Warning>
**用户类、轨道类事件之间不保证先后顺序**。例如某个用户的 `on_track_added` 可能先于他的 `on_user_join` 到达。按 `uid` 做幂等处理即可，不要假设"先加入、后发布"。
</Warning>

+ **入会前已经在频道里的用户和轨道不会触发 `on_user_join` / `on_track_added`**，请在入会后读取 `ch.users`
+ 同一路轨道的 `on_audio_frame` / `on_video_frame` 严格按顺序到达
+ `on_audio_frame` 是高频事件，请用普通函数并尽快返回；需要做耗时处理时，更推荐用 `ch.audio_frames()` 的 `async for` 方式消费

---

## 断线处理

区分三种情况：

| 情况 | 你会收到 | 建议 |
| --- | --- | --- |
| 网络短暂中断 | `on_connection_state(RECONNECTING)`，恢复后 `CONNECTED` | 什么都不用做，SDK 自动重连 |
| 被踢 / 被顶号 / 频道销毁 | `on_disconnected(KICKED / REPLACE / DESTROY, ...)` | 结束该会话，**不要自动重进** |
| 重连失败、心跳超时 | `on_disconnected(ERROR / TIMEOUT, error)` | 按业务需要用**新签发的 Token** 重新 `join` |
