---
title: "Subscribing and receiving"
description: "C SDK functions for subscribing to remote audio and video tracks (auto-subscribe vs. manual subscription in the track event callback), unsubscribing, and rtc_request_key_frame, including when you should and shouldn't request a keyframe."
---

There are two ways to subscribe:

+ **Auto-subscribe**—call `rtc_set_auto_subscribe` before joining, and the SDK subscribes to every remote track automatically. Use this for "take everything" scenarios such as recording, audio mixing, and AI integration
+ **Manual subscription**—pick the tracks you need in the track event callback and subscribe to them one by one

Either way, media data goes through the same `rtc_set_track_sample_callback` callback.

---

## rtc_subscribe_audio

```c
int rtc_subscribe_audio(void* handle, const char* uid, const char* track_id);
```

Subscribes to a specific user's audio track.

| Parameter | Description |
| --- | --- |
| `uid` | Publisher uid. Pass `RTC_MCU_PUBLISHER_UID` to subscribe to the audio composite stream |
| `track_id` | Track ID. Pass `RTC_TRACK_AMCU_ID` to subscribe to the audio composite stream |

**Returns**

| Return value | Meaning |
| --- | --- |
| `RTC_OK` | Subscribed successfully |
| `RTC_INVALID_PARAM` | Invalid handle |
| `RTC_NOT_CONNECTED` | Not yet joined to the channel |
| `RTC_ERROR` | Subscribe failed (track doesn't exist, rejected by the engine, etc.) |

## rtc_subscribe_video

```c
int rtc_subscribe_video(void* handle, const char* uid, const char* track_id);
```

Subscribes to a specific user's video track. Parameters and return values are the same as `rtc_subscribe_audio`; to subscribe to the video composite stream, pass `RTC_MCU_PUBLISHER_UID` / `RTC_TRACK_MCU_ID`.

<Note>
There's no separate function for subscribing to the composite stream (program); use the two general functions above with the reserved constants. See [Composite stream (program)](/en/rtc/capi/advanced/mcu).
</Note>

## rtc_unsubscribe

```c
int rtc_unsubscribe(void* handle, const char* uid, const char* track_id);
```

Unsubscribes. For a composite stream, pass the publisher uid plus the corresponding reserved `track_id`. Return values are the same as above.

After you unsubscribe, the SDK automatically stops collecting data for that track, and the corresponding `track_sample` callbacks stop.

---

## Manual subscription example

```c
static void* g_rtc = NULL;

// Pick the tracks to subscribe to in the track event
static void on_track_event(void* ctx, const char* uid,
                           rtc_track_info_t* track, int event_type) {
    if (event_type != 0) return;   // Only handle "added"

    // Only subscribe to the target user's video
    if (strcmp(uid, "target_user_id") == 0 && track->kind == 1) {
        rtc_subscribe_video(g_rtc, uid, track->track_id);
    }
    // Subscribe to everyone's audio
    if (track->kind == 0) {
        rtc_subscribe_audio(g_rtc, uid, track->track_id);
    }
}

int main() {
    g_rtc = rtc_create();
    rtc_set_track_event_callback(g_rtc, on_track_event, NULL);
    rtc_set_track_sample_callback(g_rtc, on_track_sample, NULL);
    // Auto-subscribe is not turned on
    rtc_join_channel_sync(g_rtc, token, 10000);
    // ...
}
```

---

## rtc_request_key_frame

```c
int rtc_request_key_frame(void* handle, const char* uid, const char* track_id);
```

Asks a remote video track to send a keyframe immediately (sends RTCP PLI to the publisher).

| Parameter | Description |
| --- | --- |
| `uid` | Publisher uid |
| `track_id` | ID of a subscribed video track |

**Returns**

| Return value | Meaning |
| --- | --- |
| `RTC_OK` | Request sent |
| `RTC_INVALID_PARAM` | Invalid handle, an empty parameter, or the track doesn't support it (not video / not ready) |
| `RTC_NOT_CONNECTED` | Not yet joined to the channel |

**When to call it**

+ You just subscribed to a video track and want video to appear as soon as possible
+ The decoder reports errors, or the video is corrupted or gray, and you need to refresh the reference frame

**When not to call it**

<Note>
**You don't need to request keyframes for packet loss.** Light packet loss is recovered automatically by the SDK's NACK retransmission and doesn't corrupt the video. So the SDK doesn't request keyframes based on packet loss rate, and we don't recommend that you do—it only triggers unnecessary keyframes, which push up the bitrate and make congestion worse.

Only call it when **your decoder actually reports an error** or the video is already corrupted.

The function has built-in rate limiting (at most once per second), so calling it repeatedly on per-frame decode errors won't flood requests.
</Note>

---

## Related

+ How the publisher responds to keyframe requests: [Publishing](/en/rtc/capi/api-reference/publish)
+ Multi-layer simulcast subscription and manual layer switching: [SeaStart advanced features](/en/rtc/capi/advanced/seastart)
