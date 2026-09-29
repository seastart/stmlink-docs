---
title: "Event callbacks"
description: "The ChannelHandler event list of the SRTC Python SDK: connection state, disconnect reasons, users joining and leaving, tracks added and removed, audio and video frames, active speakers, network quality, and custom messages, with when each fires, its parameters, and ordering guarantees."
---

Subclass `srtc.ChannelHandler`, override the methods you need, and pass it in with `Channel.join(token, handler=...)`. Events you don't override are ignored.

```python
class MyHandler(srtc.ChannelHandler):
    def on_user_join(self, user: srtc.UserInfo):          # A regular function
        print("Joined:", user.uid)

    async def on_disconnected(self, reason, error):       # It can also be an async function
        await notify_ops(reason)
```

+ All methods are called on the **asyncio event loop thread**, so no locking is needed
+ `async` methods are scheduled as Tasks and don't block subsequent events
+ Exceptions raised in the methods are logged to the `srtc` logger and don't interrupt the SDK

---

## Event list

| Method | Parameters | When it fires |
| --- | --- | --- |
| `on_connection_state` | `state: ConnectionState` | Connection state changed: `CONNECTED` (connected / reconnected), `RECONNECTING` (network interrupted, the SDK is reconnecting automatically), `DISCONNECTED` (disconnected) |
| `on_disconnected` | `reason: DisconnectReason`, `error: SdkError \| None` | Fully left the channel and won't reconnect automatically. For `reason`, see [DisconnectReason](/en/rtc/python/types#disconnectreason) |
| `on_user_join` | `user: UserInfo` | A remote user joined |
| `on_user_leave` | `uid: str` | A remote user left |
| `on_track_added` | `track: TrackInfo` | A remote user published a new track. When auto-subscribe is off, decide here whether to subscribe |
| `on_track_updated` | `track: TrackInfo` | A remote track's info changed |
| `on_track_removed` | `track: TrackInfo` | A remote user unpublished a track |
| `on_audio_frame` | `frame: AudioFrame` | A decoded frame of remote audio was received (about once every 20 ms per track) |
| `on_video_frame` | `frame: VideoFrame` | A frame of remote video was received |
| `on_active_speakers` | `speakers: list[ActiveSpeaker]` | Active speakers changed; a full snapshot sorted by volume in descending order; an empty list means nobody is speaking |
| `on_connection_quality` | `quality: ConnectionQuality` | Uplink and downlink network quality, about once per second |
| `on_layer_switched` | `event: LayerSwitched` | A layer switch of subscribed multi-layer video completed |
| `on_custom_msg` | `msg: CustomMsg` | An in-channel custom message was received (sent by your backend) |

<Note>
`on_active_speakers`, `on_connection_quality`, and `on_layer_switched` depend on the channel's media streaming engine and don't fire in some deployments. Don't make your business logic rely on them always arriving.
</Note>

---

## Ordering and timing

<Warning>
**There's no ordering guarantee between user events and track events.** For example, a user's `on_track_added` may arrive before their `on_user_join`. Just handle them idempotently by `uid`, and don't assume "join first, publish later".
</Warning>

+ **Users and tracks already in the channel before you joined don't trigger `on_user_join` / `on_track_added`**; read `ch.users` after joining
+ `on_audio_frame` / `on_video_frame` for the same track arrive strictly in order
+ `on_audio_frame` is a high-frequency event, so use a regular function and return as quickly as possible; for time-consuming processing, we recommend consuming with `async for` over `ch.audio_frames()` instead

---

## Handling disconnects

Distinguish three cases:

| Case | What you receive | Recommendation |
| --- | --- | --- |
| Brief network interruption | `on_connection_state(RECONNECTING)`, then `CONNECTED` after recovery | Do nothing; the SDK reconnects automatically |
| Removed from the channel / replaced by another session with the same uid / channel destroyed | `on_disconnected(KICKED / REPLACE / DESTROY, ...)` | End the session; **don't rejoin automatically** |
| Reconnection failed, heartbeat timed out | `on_disconnected(ERROR / TIMEOUT, error)` | If needed, `join` again with a **newly issued token** |
