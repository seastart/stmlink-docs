---
title: "Publishing"
description: "C SDK functions for creating and publishing local tracks, rtc_publish_options_t fields, pushing encoded frames with rtc_write_sample (RTP timestamp increments and pacing), and responding to keyframe requests from the SFU."
---

The C SDK does neither capture nor encoding. The complete publishing pipeline is: **you capture → you encode → feed raw data with `rtc_write_sample` → the SDK packetizes and sends**.

Standard flow:

```text
rtc_create_local_track  →  rtc_set_keyframe_request_callback  →  rtc_publish_local_track
        →  rtc_write_sample in a loop  →  rtc_unpublish_local_track  →  rtc_destroy_local_track
```

---

## rtc_create_local_track

```c
void* rtc_create_local_track(int codec);
```

Creates a local track and returns the track handle; returns `NULL` on failure.

| Parameter | Description |
| --- | --- |
| `codec` | Codec constant: `RTC_CODEC_H264` / `RTC_CODEC_H265` / `RTC_CODEC_VP8` / `RTC_CODEC_VP9` / `RTC_CODEC_AV1` / `RTC_CODEC_OPUS` / `RTC_CODEC_AAC` |

Whether the track is audio or video is determined by the codec; you don't need to specify it separately.

## rtc_destroy_local_track

```c
void rtc_destroy_local_track(void* track_handle);
```

Destroys a local track. A published track should be unpublished with `rtc_unpublish_local_track` before it's destroyed.

**Starting with 0.0.11**, it first removes the keyframe request callback and waits for any running keyframe callback to return before returning; after that you can safely free the `context` passed to `rtc_set_keyframe_request_callback`. In 0.0.10 and earlier, the keyframe callback may still fire after the track is destroyed.

---

## rtc_publish_local_track

```c
int rtc_publish_local_track(void* handle, void* track_handle, rtc_publish_options_t* options);
```

Publishes a local track to the channel.

| Parameter | Description |
| --- | --- |
| `handle` | Instance handle |
| `track_handle` | Track handle returned by `rtc_create_local_track` |
| `options` | Publish options, see below |

**Publish options `rtc_publish_options_t`**

| Field | Type | Description |
| --- | --- | --- |
| `desc` | `char[64]` | Track description, **required and can't be an empty string**, such as `"camera"` / `"screen"` / `"microphone"` |
| `width` | `int` | Video width, required for video tracks |
| `height` | `int` | Video height, required for video tracks |
| `fps` | `int` | Frame rate, required for video tracks |
| `sample_rate` | `int` | Sample rate, required for audio tracks |
| `channel_count` | `int` | Number of audio channels, required for audio tracks |
| `angle` | `int` | Video angle, optional |
| `bitrate` | `int` | Bitrate (bps), optional |
| `props` | `const char*` | Custom business properties as a JSON object string, optional |

<Note>
If `props` fails to parse, the SDK only logs a warning and continues publishing as if there were no custom properties; it doesn't fail the publish.
</Note>

**Returns**

| Return value | Meaning |
| --- | --- |
| `RTC_OK` | Published successfully |
| `RTC_INVALID_PARAM` | Invalid handle, invalid track handle, or `options` is `NULL` |
| `RTC_NOT_CONNECTED` | Not yet joined to the channel |
| `RTC_ERROR` | Publish failed (missing required parameters, rejected by the engine, negotiation failed, etc.) |

## rtc_unpublish_local_track

```c
int rtc_unpublish_local_track(void* handle, void* track_handle);
```

Unpublishes. Return values are the same as above.

## rtc_publish_mcu_video_track / rtc_publish_mcu_audio_track

Publishes the channel-level composite stream; see [Composite stream (program)](/en/rtc/capi/advanced/mcu).

---

## rtc_write_sample

```c
int rtc_write_sample(void* track_handle, uint8_t* data, int length, uint32_t samples);
```

Pushes one frame of encoded data to a published track.

| Parameter | Description |
| --- | --- |
| `data` | Encoded raw data. For video, one complete frame (Annex-B NALUs); for audio, one encoded packet |
| `length` | Data length in bytes |
| `samples` | **RTP timestamp increment**—neither a byte count nor milliseconds |

Compute `samples` from each codec's clock rate:

| Codec | Clock rate | Common values |
| --- | --- | --- |
| H.264 / H.265 / VP8 / VP9 / AV1 | 90000 | 30 fps → `90000/30 = 3000`; 25 fps → `3600` |
| Opus | 48000 | 20 ms per packet → `48000 * 0.02 = 960` |

**Returns**

| Return value | Meaning |
| --- | --- |
| `RTC_OK` | Written successfully |
| `RTC_INVALID_PARAM` | Invalid track handle, or `data` is `NULL` / `length <= 0` |
| `RTC_ERROR` | Write failed (track not published, underlying send error, etc.) |

<Note>
The SDK copies the data you pass in, so you can reuse or free the `data` buffer as soon as the call returns.
</Note>

<Warning>
**The SDK doesn't control send pacing**—each frame is sent as soon as it's written. When your data source is faster than real time (reading a file, TTS synthesis), you must write at the pace of the frame duration (for example, one audio packet every 20 ms). Otherwise several seconds of data go out in an instant, the remote jitter buffer can't hold it and drops some, and it sounds like swallowed words or sped-up audio.
</Warning>

---

## rtc_set_keyframe_request_callback

```c
typedef void (*rtc_keyframe_request_callback)(void* context, const char* track_id);
void rtc_set_keyframe_request_callback(void* track_handle,
                                       rtc_keyframe_request_callback callback,
                                       void* context);
```

Sets the keyframe request callback. It fires when the SFU uses RTCP (PLI / FIR) to ask this track to produce a keyframe immediately; in the callback, have the encoder produce an IDR frame right away and send it with `rtc_write_sample`.

<Warning>
**You must set it on the track before publishing.** Without it, newly joined viewers don't see video until the encoder's next natural GOP—with a long GOP, that's several seconds of black screen.

The callback fires on a separate thread, so synchronize with your encoding thread. Pass `NULL` to clear the callback.
</Warning>

```c
static void on_keyframe_request(void* ctx, const char* track_id) {
    // Don't do heavy work here; set a flag so the encoding thread encodes an IDR on the next frame
    encoder_request_idr(track_id);
}

void* video = rtc_create_local_track(RTC_CODEC_H264);
rtc_set_keyframe_request_callback(video, on_keyframe_request, NULL);
rtc_publish_local_track(rtc, video, &vopts);   // Publish after setting the callback
```

---

## Complete example

```c
// 1. Create tracks
void* video = rtc_create_local_track(RTC_CODEC_H264);
void* audio = rtc_create_local_track(RTC_CODEC_OPUS);

// 2. Register the keyframe request callback on the video track (before publishing)
rtc_set_keyframe_request_callback(video, on_keyframe_request, NULL);

// 3. Configure publish options
rtc_publish_options_t vopts = {0};
strcpy(vopts.desc, "camera");
vopts.width = 1280; vopts.height = 720; vopts.fps = 30;

rtc_publish_options_t aopts = {0};
strcpy(aopts.desc, "microphone");
aopts.sample_rate = 48000; aopts.channel_count = 2;

// 4. Publish
rtc_publish_local_track(rtc, video, &vopts);
rtc_publish_local_track(rtc, audio, &aopts);

// 5. Push data
rtc_write_sample(video, h264_frame, h264_len, 3000);  // 30fps
rtc_write_sample(audio, opus_frame, opus_len, 960);   // 20ms

// 6. Clean up
rtc_unpublish_local_track(rtc, video);
rtc_unpublish_local_track(rtc, audio);
rtc_destroy_local_track(video);
rtc_destroy_local_track(audio);
```

---

<Note>
The C interface doesn't support publishing multi-layer simulcast streams—server-side scenarios (recording / MCU / AI agents) almost never need to publish multiple layers. Multi-layer switching on the subscriber side is done automatically by the SDK with no configuration. If you do need to publish multiple layers, contact us.
</Note>
