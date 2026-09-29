---
title: "Types"
description: "Reference for everything librtc.h exposes: the rtc_track_info_t, rtc_user_info_t, rtc_channel_info_t, and rtc_publish_options_t structs, codec and log level constants, reserved composite stream identifiers, int enums in callback parameters, and all callback signatures."
---

This page summarizes the data structures and constants exposed in `librtc.h`.

---

## Data structures

### rtc_track_info_t

Track info. Appears in the track event callback, the track data callback, and the `stream_tracks` array of user info.

```c
typedef struct {
    char track_id[64];
    char uid[64];
    char desc[64];
    int kind;
    int codec;
    int width;
    int height;
    int fps;
    int angle;
    int bitrate;
    int sample_rate;
    int channel_count;
    const char* props;
} rtc_track_info_t;
```

| Field | Type | Description |
| --- | --- | --- |
| `track_id` | `char[64]` | Track ID |
| `uid` | `char[64]` | uid of the user the track belongs to |
| `desc` | `char[64]` | Track description, such as `camera` / `screen` / `microphone` |
| `kind` | `int` | `0`=audio, `1`=video |
| `codec` | `int` | Codec; for values see [Codecs](#codecs) below |
| `width` / `height` | `int` | Video resolution |
| `fps` | `int` | Frame rate |
| `angle` | `int` | Video angle |
| `bitrate` | `int` | Bitrate (bps) |
| `sample_rate` | `int` | Audio sample rate |
| `channel_count` | `int` | Number of audio channels |
| `props` | `const char*` | Custom business properties as a JSON string; may be `NULL` |

### rtc_user_info_t

User info. Returned by `rtc_get_user_info` / `rtc_get_users_info`, and also appears in the track data callback.

```c
typedef struct {
    char uid[64];
    char name[128];
    char device_id[128];
    char version[64];
    char channel[128];
    char sid[128];
    const char* props;
    int device_type;
    int is_audience;
    int64_t join_at;
    int64_t leave_at;
    int64_t updated_at;
    rtc_track_info_t* stream_tracks;
    int stream_track_count;
} rtc_user_info_t;
```

| Field | Type | Description |
| --- | --- | --- |
| `uid` | `char[64]` | User ID |
| `name` | `char[128]` | User name |
| `device_id` | `char[128]` | Device ID |
| `version` | `char[64]` | Client SDK version |
| `channel` | `char[128]` | Name of the channel the user is in |
| `sid` | `char[128]` | Session ID |
| `props` | `const char*` | Custom business properties as a JSON string; may be `NULL` |
| `device_type` | `int` | Device type |
| `is_audience` | `int` | `1`=audience (doesn't appear in other users' user lists), `0`=regular user |
| `join_at` / `leave_at` / `updated_at` | `int64_t` | Join / leave / update timestamps |
| `stream_tracks` | `rtc_track_info_t*` | Array of tracks this user has published |
| `stream_track_count` | `int` | Number of tracks |

<Warning>
`props` and `stream_tracks` are allocated dynamically by the SDK, so an `rtc_user_info_t` returned by a query function must be freed with `rtc_free_user_info` / `rtc_free_users_info`. See [User info queries](/en/rtc/capi/api-reference/users).
</Warning>

<Warning>
**The `link_id` field was removed in 0.0.9**, which changed the struct layout. When upgrading from an older version, you must **recompile** with the new `librtc.h`; replacing only the library files reads the wrong fields or even crashes. Just delete any code that references `link_id` (it was always 0 before).
</Warning>

### rtc_channel_info_t

Channel info, returned by `rtc_get_channel_info` (since 0.0.9).

```c
typedef struct {
    char app_id[64];
    char channel[128];
    const char* props;
    int64_t created_at;
    int64_t updated_at;
} rtc_channel_info_t;
```

| Field | Type | Description |
| --- | --- | --- |
| `app_id` | `char[64]` | App ID |
| `channel` | `char[128]` | Channel name |
| `props` | `const char*` | Custom channel properties as a JSON string; may be `NULL`. Call `rtc_free_channel_info` to free it when done |
| `created_at` / `updated_at` | `int64_t` | Creation / update timestamps |

### rtc_publish_options_t

Publish options; see [Publishing](/en/rtc/capi/api-reference/publish).

```c
typedef struct {
    char desc[64];         // Track description (required, can't be an empty string)
    int width;             // Video width (required for video)
    int height;            // Video height (required for video)
    int fps;               // Frame rate (required for video)
    int sample_rate;       // Sample rate (required for audio)
    int channel_count;     // Number of audio channels (required for audio)
    int angle;             // Video angle (optional)
    int bitrate;           // Bitrate in bps (optional)
    const char* props;     // Custom properties as a JSON string (optional)
} rtc_publish_options_t;
```

### SeaStart structs

For `rtc_layer_switched_t`, `rtc_quality_sample_t`, `rtc_connection_quality_t`, and `rtc_active_speaker_t`, see [SeaStart advanced features](/en/rtc/capi/advanced/seastart).

### rtc_custom_msg_t

See [Custom messages](/en/rtc/capi/advanced/custom-msg).

---

## Constants

### Codecs

```c
#define RTC_CODEC_H264  0x1b        // H264 video
#define RTC_CODEC_H265  0x24        // H265 video
#define RTC_CODEC_VP8   0x38        // VP8 video
#define RTC_CODEC_VP9   0x39        // VP9 video
#define RTC_CODEC_AV1   0x3a        // AV1 video
#define RTC_CODEC_AAC   0x0f        // AAC audio
#define RTC_CODEC_OPUS  0x5355504f  // OPUS audio
```

The header also provides an inline helper that converts a codec to a readable string:

```c
static inline const char* rtc_codec_to_string(int codec);
// Returns "UNKNOWN" for unknown values
```

### Log levels

```c
#define RTC_LOG_DEBUG  0
#define RTC_LOG_INFO   1
#define RTC_LOG_WARN   2
#define RTC_LOG_ERROR  3
```

### Reserved composite stream identifiers

```c
#define RTC_MCU_PUBLISHER_UID "__mcu__"   // uid of the composite stream publisher
#define RTC_TRACK_AMCU_ID     "__amcu__"  // trackId of the audio composite stream
#define RTC_TRACK_MCU_ID      "__mcu__"   // trackId of the video composite stream
```

---

## Callback parameter enums

These values appear as `int` in callback parameters; the header has no corresponding macros for them.

**Connection state** (`state` in `rtc_connection_callback`)

| Value | Meaning |
| --- | --- |
| `0` | connecting |
| `1` | connected |
| `2` | disconnected |
| `3` | reconnecting |

**Disconnect reason** (`reason` in `rtc_disconnected_callback`, since 0.0.9; the header does have corresponding macros)

| Macro | Value | Meaning |
| --- | --- | --- |
| `RTC_DISCONNECT_ERROR` | `-1` | Left due to an error; `code` / `msg` carry the specific error |
| `RTC_DISCONNECT_SELF` | `1` | Left voluntarily |
| `RTC_DISCONNECT_KICKED` | `2` | Removed from the channel |
| `RTC_DISCONNECT_REPLACE` | `3` | Replaced by another session with the same uid that joined elsewhere |
| `RTC_DISCONNECT_TIMEOUT` | `4` | Heartbeat timeout |
| `RTC_DISCONNECT_DESTROY` | `5` | The channel was destroyed |

**User event** (`event_type` in `rtc_user_event_callback`)

| Value | Meaning |
| --- | --- |
| `0` | join |
| `1` | leave |

**Track event** (`event_type` in `rtc_track_event_callback`)

| Value | Meaning |
| --- | --- |
| `0` | add |
| `1` | update |
| `2` | remove |

**Track kind** (`rtc_track_info_t.kind`)

| Value | Meaning |
| --- | --- |
| `0` | Audio |
| `1` | Video |

---

## Callback signatures

```c
typedef void (*rtc_connection_callback)(void* context, int state);

typedef void (*rtc_user_event_callback)(void* context, const char* uid, int event_type);

typedef void (*rtc_track_event_callback)(void* context, const char* uid,
                                         rtc_track_info_t* track_info, int event_type);

typedef void (*rtc_track_sample_callback)(void* context,
                                          rtc_user_info_t* user_info,
                                          rtc_track_info_t* track_info,
                                          uint8_t* data, int len,
                                          int64_t timestamp, int64_t duration);

typedef void (*rtc_layer_switched_callback)(void* context, const rtc_layer_switched_t* data);

typedef void (*rtc_connection_quality_callback)(void* context, const rtc_connection_quality_t* q);

typedef void (*rtc_active_speakers_callback)(void* context, int64_t ts,
                                             const rtc_active_speaker_t* speakers,
                                             int speakers_count);

typedef void (*rtc_custom_msg_callback)(void* context, const rtc_custom_msg_t* msg);

typedef void (*rtc_keyframe_request_callback)(void* context, const char* track_id);

typedef void (*rtc_disconnected_callback)(void* context, int reason, int code, const char* msg);
```
