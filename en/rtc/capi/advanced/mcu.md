---
title: "Composite stream (program)"
description: "How the C SDK publishes the channel-level composite stream from the MCU side under the reserved __mcu__ identity, how viewers subscribe to it with the reserved constants, and when you should not use it. Read this when building an MCU publisher or a viewer that needs only one mixed stream."
---

The composite stream (program) is a **channel-level** audio and video stream: a server-side MCU program composites everyone in the channel into a single stream, and every subscriber receives exactly the same video and audio.

Typical uses:

+ Viewers who don't speak subscribe to just one stream, saving bandwidth and decoding overhead
+ Server-side recording / re-streaming

---

## Reserved identifiers

The composite stream doesn't belong to any regular user; it lives under a system identity. The header exposes these three reserved constants:

```c
#define RTC_MCU_PUBLISHER_UID "__mcu__"   // uid of the composite stream publisher (shared by audio and video)
#define RTC_TRACK_AMCU_ID     "__amcu__"  // trackId of the audio composite stream
#define RTC_TRACK_MCU_ID      "__mcu__"   // trackId of the video composite stream
```

---

## Publishing (MCU program side)

<Warning>
Publishing the composite stream requires **connecting with the MCU identity**: the `uid` in the token issued by the server must be `__mcu__`; otherwise the publish functions return `RTC_ERROR`.
</Warning>

### rtc_publish_mcu_video_track

```c
int rtc_publish_mcu_video_track(void* handle, void* track_handle, rtc_publish_options_t* options);
```

Publishes the video composite stream. It differs from `rtc_publish_local_track` in only two ways: it always uses the reserved `trackId` internally (you can't customize it), and it requires the MCU identity. `track_handle` must be created with a video codec, and `options` must fill in `desc` / `width` / `height` / `fps`.

### rtc_publish_mcu_audio_track

```c
int rtc_publish_mcu_audio_track(void* handle, void* track_handle, rtc_publish_options_t* options);
```

Publishes the audio composite stream (the mixed audio stream), with the same semantics as above. `track_handle` must be created with an audio codec, and `options` must fill in `desc` / `sample_rate` / `channel_count`.

**Returns** (same for both functions)

| Return value | Meaning |
| --- | --- |
| `RTC_OK` | Published successfully |
| `RTC_INVALID_PARAM` | Invalid handle, invalid track handle, or `options` is `NULL` |
| `RTC_NOT_CONNECTED` | Not yet joined to the channel |
| `RTC_ERROR` | Publish failed; the most common cause is that **the current identity is not `__mcu__`** |

### Example

```c
// Video composite stream
void* v = rtc_create_local_track(RTC_CODEC_H264);
rtc_publish_options_t vopts = {0};
strcpy(vopts.desc, "mcu_video");
vopts.width = 1280; vopts.height = 720; vopts.fps = 25;
rtc_publish_mcu_video_track(rtc, v, &vopts);      // trackId is fixed to __mcu__

// Mixed audio stream
void* a = rtc_create_local_track(RTC_CODEC_OPUS);
rtc_publish_options_t aopts = {0};
strcpy(aopts.desc, "mcu_audio");
aopts.sample_rate = 48000; aopts.channel_count = 2;
rtc_publish_mcu_audio_track(rtc, a, &aopts);      // trackId is fixed to __amcu__

// Pushing data works exactly like a regular track
rtc_write_sample(v, h264_frame, h264_len, 3600);  // 25fps: 90000/25
rtc_write_sample(a, opus_frame, opus_len, 960);
```

---

## Subscribing (viewer side)

The C interface has no RemoteTrack handle, so there's no separate subscribe function for the composite stream—use the general subscribe functions with the reserved constants:

```c
rtc_subscribe_video(rtc, RTC_MCU_PUBLISHER_UID, RTC_TRACK_MCU_ID);   // Subscribe to the video composite stream
rtc_subscribe_audio(rtc, RTC_MCU_PUBLISHER_UID, RTC_TRACK_AMCU_ID);  // Subscribe to the audio composite stream

// Data comes out of the rtc_set_track_sample_callback callback as usual

// Unsubscribing also takes the reserved constants
rtc_unsubscribe(rtc, RTC_MCU_PUBLISHER_UID, RTC_TRACK_MCU_ID);
rtc_unsubscribe(rtc, RTC_MCU_PUBLISHER_UID, RTC_TRACK_AMCU_ID);
```

---

## When not to use the composite stream

<Warning>
**If a user in the channel wants to "hear everyone," don't subscribe to the audio composite stream.** The composite stream includes your own voice, so subscribing to it causes echo.

The right approach is `rtc_set_auto_subscribe(rtc, 1, 0)` to auto-subscribe to everyone's audio; once each track's data arrives through the `track_sample` callback, mix it yourself (excluding your own track when mixing).

The composite stream is meant for **viewers who don't speak** and for **recording / re-streaming**.
</Warning>
