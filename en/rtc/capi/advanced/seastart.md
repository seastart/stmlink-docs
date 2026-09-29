---
title: "SeaStart advanced features"
description: "C SDK features available only with the SeaStart engine: simulcast layer switching callbacks and rtc_switch_layer, periodic and on-demand network quality reports, and active speaker snapshots. Read this when you need layer control, quality indicators, or speaking indicators."
---

The following features are only available when the channel uses the **SeaStart engine**. With other engines these callbacks never fire and the functions you call directly (such as `rtc_switch_layer`) return an error. The engine is determined by the channel configuration sent down by the server, so your code doesn't need to check it—just make sure it still works without these callbacks.

The three features map to three separate strongly typed callbacks, in the same style as `track_event` / `track_sample`, so there's no JSON to parse on the C side.

---

## Layer switching (simulcast)

When the publisher pushes a multi-layer simulcast stream, layer switching on the subscriber side is **fully automatic**: the SDK registers the available layers as candidates, and the SFU switches between them based on bandwidth estimation (BWE). You don't need to configure anything; usually you only listen for the switching results.

### Layer switched callback

```c
typedef struct {
    char    sub_key[128];        // Stable subscription handle "pub_uid:track_id"
    char    from_track_id[64];   // Layer in use before the switch; empty string on first playback
    char    to_track_id[64];     // Layer in use after the switch
    char    reason[32];          // Reason for the switch, see the table below
    int64_t latency_ms;          // Time from initiating the switch to actually reaching the target layer
} rtc_layer_switched_t;

typedef void (*rtc_layer_switched_callback)(void* context, const rtc_layer_switched_t* data);
void rtc_set_layer_switched_callback(void* handle, rtc_layer_switched_callback callback, void* context);
```

`reason` values:

| Value | Meaning |
| --- | --- |
| `bwe_down` | Bandwidth dropped; the SFU switched down a layer automatically |
| `bwe_up` | Bandwidth recovered; the SFU switched up a layer automatically |
| `track_refresh` | Track refreshed |
| `track_upgrade` | Track upgraded |
| `track_ended` | The current layer ended; fell back to another layer |
| `client` | The client called `rtc_switch_layer` |

```c
static void on_layer_switched(void* ctx, const rtc_layer_switched_t* d) {
    printf("layer %s -> %s (%s, %lldms)\n",
           d->from_track_id[0] ? d->from_track_id : "-",
           d->to_track_id, d->reason, (long long)d->latency_ms);
}

rtc_set_layer_switched_callback(rtc, on_layer_switched, NULL);
```

<Note>
**Which layer is currently in use?** The subscription handle (the `track_id` in `sub_key`) stays stable for the whole subscription, but the layer actually in use is switched dynamically. The `to_track_id` you get from `layer_switched` is the current layer; if you need it, cache a `sub_key → current layer` mapping yourself.
</Note>

### rtc_switch_layer

```c
int rtc_switch_layer(void* handle, const char* pub_uid,
                     const char* track_id, const char* target_track_id);
```

Asks the SFU to switch to a specific layer. Useful for switching between large and small windows, or proactively downgrading when a window goes to the background.

| Parameter | Description |
| --- | --- |
| `pub_uid` | Publisher uid |
| `track_id` | The stable handle trackId used when subscribing (usually the main layer's ID) |
| `target_track_id` | Target layer trackId; **must be in the candidate pool registered at subscription time** |

**Returns:** `RTC_OK` (request sent) / `RTC_INVALID_PARAM` (invalid handle or a parameter is `NULL`) / `RTC_NOT_CONNECTED` (not joined) / `RTC_ERROR` (rejected by the engine).

```c
// Switch u1001's subscribed main layer to the smallest layer
rtc_switch_layer(rtc, "u1001", big_track_id, small_track_id);
// The result is reported through on_layer_switched, with reason = "client"
```

<Note>
A successful return only means the request was sent; the switch to the target layer is complete when the `layer_switched` callback fires.

This SDK only supports multi-layer switching on the subscriber side; it doesn't support **publishing** multi-layer simulcast streams.
</Note>

---

## Network quality

### Periodic report callback

The SFU periodically (typically at 1 Hz) reports uplink and downlink quality.

```c
// Quality sample for one direction
typedef struct {
    double  score;      // Quality score 0–100
    char    level[16];  // "excellent" | "good" | "poor" | "lost"
    double  mos;        // 1.0-4.5
    double  loss;       // Packet loss rate 0–1
    double  rtt;        // Milliseconds
    double  jitter;     // Milliseconds
    int64_t packets;    // Number of packets counted in this round
    double  bitrate;    // Average bitrate in kbps (not used in the score)
    int64_t bytes;      // Bytes in this window
} rtc_quality_sample_t;

typedef struct {
    int64_t              ts;   // Unix timestamp in milliseconds when the SFU generated the report
    rtc_quality_sample_t pub;  // Uplink (local → SFU)
    rtc_quality_sample_t sub;  // Downlink (SFU → local)
} rtc_connection_quality_t;

typedef void (*rtc_connection_quality_callback)(void* context, const rtc_connection_quality_t* q);
void rtc_set_connection_quality_callback(void* handle, rtc_connection_quality_callback callback, void* context);
```

```c
static void on_connection_quality(void* ctx, const rtc_connection_quality_t* q) {
    // For a signal-bars indicator, use q->pub.level / q->sub.level
    // For a numeric panel, use mos / loss / rtt / jitter / bitrate
    printf("pub=%s(%.1f) sub=%s(%.1f) rtt=%.0fms\n",
           q->pub.level, q->pub.score, q->sub.level, q->sub.score, q->sub.rtt);
}

rtc_set_connection_quality_callback(rtc, on_connection_quality, NULL);
```

<Warning>
The callback fires for every report, so **throttling is up to you**. If you write logs or feed monitoring, downsample yourself.
</Warning>

### rtc_get_connection_quality

```c
int rtc_get_connection_quality(void* handle, rtc_connection_quality_t* out);
```

Fetches the most recent quality report on demand. Useful right after joining, to populate the UI / monitoring metrics before the first periodic report arrives.

`out` is provided by the caller; the SDK fills in the fields directly, and nothing needs to be freed.

**Returns**

| Return value | Meaning |
| --- | --- |
| `RTC_OK` | Written to `out` |
| `RTC_NOT_CONNECTED` | Not yet joined, or no quality report received yet |
| `RTC_INVALID_PARAM` | Invalid handle, or `out` is `NULL` |

```c
rtc_connection_quality_t q;
int ret = rtc_get_connection_quality(rtc, &q);
if (ret == RTC_OK) {
    printf("pub=%s loss=%.2f sub=%s loss=%.2f rtt=%.0f\n",
           q.pub.level, q.pub.loss, q.sub.level, q.sub.loss, q.sub.rtt);
} else if (ret == RTC_NOT_CONNECTED) {
    // No data yet; just wait for the callback
}
```

---

## Active speaker

```c
typedef struct {
    char   uid[64];
    char   track_id[64];  // Distinguishes tracks when a user has multiple audio tracks
    double level;         // 0.0–1.0, higher is louder
} rtc_active_speaker_t;

typedef void (*rtc_active_speakers_callback)(void* context, int64_t ts,
                                             const rtc_active_speaker_t* speakers,
                                             int speakers_count);
void rtc_set_active_speakers_callback(void* handle, rtc_active_speakers_callback callback, void* context);
```

The SDK merges the SFU's incremental events into a **full snapshot** before passing it up, sorted by `level` in descending order, so you can simply overwrite the whole UI without merging deltas yourself. When no one is speaking, `speakers_count = 0` and `speakers = NULL`.

```c
static void on_active_speakers(void* ctx, int64_t ts,
                               const rtc_active_speaker_t* speakers, int count) {
    clear_speaking_indicators();
    for (int i = 0; i < count; i++) {
        update_ui(speakers[i].uid, speakers[i].level);
    }
}

rtc_set_active_speakers_callback(rtc, on_active_speakers, NULL);
```

<Warning>
The `speakers` array is held by the SDK during the callback and **freed as soon as the callback returns**. To keep it beyond the callback, you must copy it yourself.
</Warning>
