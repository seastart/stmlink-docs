---
title: "Quickstart"
description: "Get started with the SRTC C SDK: two minimal runnable C programs that join a channel and write remote audio and video to disk, and publish encoded H.264 / Opus data, plus logging and common join and publish problems."
---

This page gets the C SDK working with two minimal runnable examples: first a **receiver** (join a channel and write remote audio and video to disk), then a **publisher** (push encoded data up).

Prerequisites:

+ You have `librtc.so` and `librtc.h` as described in [Integration](/en/rtc/capi/integration)
+ Your server can already issue channel join tokens; see [Server API · Get a channel join token](/en/rtc/server-api/channel)

<Note>
A token is bound to one session. Once the process leaves the channel, that session is no longer valid, and using the same token again returns `1032 该会话不在线` ("session is not online"). Issue a new token every time you start a new process.
</Note>

---

## Receiver: join a channel and receive remote media

```c
#include "librtc.h"
#include <stdio.h>
#include <string.h>
#include <unistd.h>

// Connection state callback: 0=connecting 1=connected 2=disconnected 3=reconnecting
static void on_connection_state(void* ctx, int state) {
    const char* names[] = {"connecting", "connected", "disconnected", "reconnecting"};
    printf("[conn] %s\n", names[state]);
}

// User event callback: 0=joined 1=left
static void on_user_event(void* ctx, const char* uid, int event_type) {
    printf("[user] %s %s\n", uid, event_type == 0 ? "join" : "leave");
}

// Track data callback: encoded data for every subscribed track comes out here
// Note: the data pointer is only valid during the callback; copy it right away if you need to keep it
static void on_track_sample(void* ctx,
                            rtc_user_info_t* user, rtc_track_info_t* track,
                            uint8_t* data, int len,
                            int64_t timestamp, int64_t duration) {
    char filename[256];
    const char* ext = (track->kind == 0) ? "opus" : "h264";  // 0=audio 1=video
    snprintf(filename, sizeof(filename), "%s_%s.%s", user->uid, track->track_id, ext);

    FILE* fp = fopen(filename, "ab");
    if (fp) {
        fwrite(data, 1, len, fp);
        fclose(fp);
    }
}

int main(int argc, char** argv) {
    const char* token = argv[1];

    // 1. Create an instance
    void* rtc = rtc_create();

    // 2. Set callbacks (must be done before joining the channel, or you'll miss early events)
    rtc_set_connection_callback(rtc, on_connection_state, NULL);
    rtc_set_user_event_callback(rtc, on_user_event, NULL);
    rtc_set_track_sample_callback(rtc, on_track_sample, NULL);

    // 3. Turn on auto-subscribe: audio and video tracks published by new users are subscribed automatically, no manual subscribe needed
    rtc_set_auto_subscribe(rtc, 1, 1);

    // 4. Join the channel synchronously, with a 10-second timeout
    int ret = rtc_join_channel_sync(rtc, token, 10000);
    if (ret != RTC_OK) {
        printf("join failed: %d\n", ret);
        rtc_destroy(rtc);
        return 1;
    }
    printf("joined\n");

    // 5. Keep running; media data keeps arriving through the on_track_sample callback
    sleep(30);

    // 6. Clean up
    rtc_leave_channel(rtc);
    rtc_destroy(rtc);
    return 0;
}
```

Compile and run:

```bash
gcc -Wall -I/path/to/sdk -o subscriber main.c -L/path/to/sdk -lrtc -lpthread -lm
LD_LIBRARY_PATH=/path/to/sdk ./subscriber "your_token_here"
```

<Tip>
Auto-subscribe suits "take everything" scenarios such as recording, audio mixing, and AI integration. If you only want specific tracks from specific users, use `rtc_set_track_event_callback` + `rtc_subscribe_video` / `rtc_subscribe_audio` instead—see [Subscribing and receiving](/en/rtc/capi/api-reference/subscribe).
</Tip>

---

## Publisher: publish local audio and video tracks

The SDK only handles transport; you do the capture and encoding yourself. The publishing flow is: create tracks → configure publish options → publish → call `rtc_write_sample` in a loop to feed encoded raw data.

```c
#include "librtc.h"
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
    const char* token = argv[1];

    void* rtc = rtc_create();
    if (rtc_join_channel_sync(rtc, token, 10000) != RTC_OK) {
        rtc_destroy(rtc);
        return 1;
    }

    // 1. Create local tracks (one per codec)
    void* video = rtc_create_local_track(RTC_CODEC_H264);
    void* audio = rtc_create_local_track(RTC_CODEC_OPUS);

    // 2. Configure publish options: video requires desc/width/height/fps, audio requires desc/sample_rate/channel_count
    rtc_publish_options_t vopts = {0};
    strcpy(vopts.desc, "camera");
    vopts.width   = 1280;
    vopts.height  = 720;
    vopts.fps     = 30;
    vopts.bitrate = 2000000;   // 2 Mbps, optional

    rtc_publish_options_t aopts = {0};
    strcpy(aopts.desc, "microphone");
    aopts.sample_rate   = 48000;
    aopts.channel_count = 2;
    aopts.bitrate       = 128000;

    // 3. Publish
    if (rtc_publish_local_track(rtc, video, &vopts) != RTC_OK) { /* Handle the failure */ }
    if (rtc_publish_local_track(rtc, audio, &aopts) != RTC_OK) { /* Handle the failure */ }

    // 4. Push data in a loop. The 4th argument is the RTP timestamp increment:
    //    H264/H265 clock is 90000, 3000 per frame at 30fps; OPUS clock is 48000, 960 per 20ms frame
    while (running) {
        rtc_write_sample(video, h264_frame, h264_len, 3000);
        rtc_write_sample(audio, opus_frame, opus_len, 960);
    }

    // 5. Clean up: unpublish first, then destroy the tracks, and finally destroy the instance
    rtc_unpublish_local_track(rtc, video);
    rtc_unpublish_local_track(rtc, audio);
    rtc_destroy_local_track(video);
    rtc_destroy_local_track(audio);
    rtc_leave_channel(rtc);
    rtc_destroy(rtc);
    return 0;
}
```

<Warning>
After you publish video, the SFU uses RTCP (PLI/FIR) to ask you to produce a keyframe immediately when needed (for example, when a new viewer starts playback). Register a callback with `rtc_set_keyframe_request_callback` before publishing, and have the encoder produce an IDR frame right away in the callback; otherwise newly joined viewers may see a black screen for a long time. See [Publishing](/en/rtc/capi/api-reference/publish).
</Warning>

---

## Turn on logging

When troubleshooting, set the log level to `RTC_LOG_DEBUG`. We recommend calling this before `rtc_create`:

```c
rtc_set_log_level(RTC_LOG_DEBUG);   // 0=DEBUG 1=INFO 2=WARN 3=ERROR
```

---

## FAQ

| Symptom | What to check |
| --- | --- |
| `rtc_join_channel_sync` returns `RTC_TIMEOUT` (-4) | Token expired, no network connectivity, server address unreachable |
| `rtc_join_channel_sync` returns `RTC_ERROR` (-1) | The token's session is already taken or no longer valid (`1032`); issue a new one |
| Subscribe/publish returns `RTC_NOT_CONNECTED` (-3) | Called before joining the channel; call it only after `join` succeeds |
| `on_track_sample` never fires | Auto-subscribe isn't on, and no manual `rtc_subscribe_*` was called |
| Viewers take a long time to see video | The publisher hasn't implemented the keyframe request callback |

---

## Next steps

+ [API reference](/en/rtc/capi/api-reference/engine): the complete API reference
+ [Composite stream (program)](/en/rtc/capi/advanced/mcu): the channel-level audio and video stream composited on the server
+ [SeaStart advanced features](/en/rtc/capi/advanced/seastart): layer switching, network quality, active speaker
