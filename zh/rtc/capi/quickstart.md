---
title: "快速开始"
description: "SRTC C SDK 快速集成，10 分钟跑通加入频道、接收远端音视频与推流"
---

本文用两个最小可运行的例子跑通 C SDK：先做**收流端**（加入频道并落盘远端音视频），再做**推流端**（把编码好的数据推上去）。

前置条件：

+ 已按 [集成方式](/zh/rtc/capi/integration) 拿到 `librtc.so` 和 `librtc.h`
+ 服务端已经能签发加入频道的 Token，见 [服务端 API · 获取加入频道 token](/zh/rtc/server-api/channel)

<Note>
Token 与一次会话绑定。进程离开频道后该会话即失效，再用同一个 Token 会返回 `1032 该会话不在线`。每起一个新进程都要重新签发一个 Token。
</Note>

---

## 收流端：加入频道并接收远端媒体

```c
#include "librtc.h"
#include <stdio.h>
#include <string.h>
#include <unistd.h>

// 连接状态回调：0=连接中 1=已连接 2=已断开 3=重连中
static void on_connection_state(void* ctx, int state) {
    const char* names[] = {"connecting", "connected", "disconnected", "reconnecting"};
    printf("[conn] %s\n", names[state]);
}

// 用户事件回调：0=加入 1=离开
static void on_user_event(void* ctx, const char* uid, int event_type) {
    printf("[user] %s %s\n", uid, event_type == 0 ? "join" : "leave");
}

// 轨道数据回调：所有已订阅轨道的编码数据都从这里出来
// 注意：data 指针只在回调期间有效，需要留存必须立刻拷贝
static void on_track_sample(void* ctx,
                            rtc_user_info_t* user, rtc_track_info_t* track,
                            uint8_t* data, int len,
                            int64_t timestamp, int64_t duration) {
    char filename[256];
    const char* ext = (track->kind == 0) ? "opus" : "h264";  // 0=音频 1=视频
    snprintf(filename, sizeof(filename), "%s_%s.%s", user->uid, track->track_id, ext);

    FILE* fp = fopen(filename, "ab");
    if (fp) {
        fwrite(data, 1, len, fp);
        fclose(fp);
    }
}

int main(int argc, char** argv) {
    const char* token = argv[1];

    // 1. 创建实例
    void* rtc = rtc_create();

    // 2. 设置回调（必须在加入频道前设置，否则会漏掉早期事件）
    rtc_set_connection_callback(rtc, on_connection_state, NULL);
    rtc_set_user_event_callback(rtc, on_user_event, NULL);
    rtc_set_track_sample_callback(rtc, on_track_sample, NULL);

    // 3. 开启自动订阅：新用户发布的音视频轨道会被自动订上，无需手动 subscribe
    rtc_set_auto_subscribe(rtc, 1, 1);

    // 4. 同步加入频道，10 秒超时
    int ret = rtc_join_channel_sync(rtc, token, 10000);
    if (ret != RTC_OK) {
        printf("join failed: %d\n", ret);
        rtc_destroy(rtc);
        return 1;
    }
    printf("joined\n");

    // 5. 保持运行，媒体数据持续从 on_track_sample 回调进来
    sleep(30);

    // 6. 清理
    rtc_leave_channel(rtc);
    rtc_destroy(rtc);
    return 0;
}
```

编译运行：

```bash
gcc -Wall -I/path/to/sdk -o subscriber main.c -L/path/to/sdk -lrtc -lpthread -lm
LD_LIBRARY_PATH=/path/to/sdk ./subscriber "your_token_here"
```

<Tip>
自动订阅适合录制、混音、AI 接入这类"全都要"的场景。如果只想订特定用户的特定轨道，改用 `rtc_set_track_event_callback` + `rtc_subscribe_video` / `rtc_subscribe_audio`，详见 [订阅与收流](/zh/rtc/capi/api-reference/subscribe)。
</Tip>

---

## 推流端：发布本地音视频轨道

SDK 只负责传输，采集和编码由业务方自己做。推流的流程是：创建轨道 → 配置发布选项 → 发布 → 循环 `rtc_write_sample` 喂编码后的裸数据。

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

    // 1. 创建本地轨道（按编码格式创建）
    void* video = rtc_create_local_track(RTC_CODEC_H264);
    void* audio = rtc_create_local_track(RTC_CODEC_OPUS);

    // 2. 配置发布选项：视频必填 desc/width/height/fps，音频必填 desc/sample_rate/channel_count
    rtc_publish_options_t vopts = {0};
    strcpy(vopts.desc, "camera");
    vopts.width   = 1280;
    vopts.height  = 720;
    vopts.fps     = 30;
    vopts.bitrate = 2000000;   // 2 Mbps，可选

    rtc_publish_options_t aopts = {0};
    strcpy(aopts.desc, "microphone");
    aopts.sample_rate   = 48000;
    aopts.channel_count = 2;
    aopts.bitrate       = 128000;

    // 3. 发布
    if (rtc_publish_local_track(rtc, video, &vopts) != RTC_OK) { /* 处理失败 */ }
    if (rtc_publish_local_track(rtc, audio, &aopts) != RTC_OK) { /* 处理失败 */ }

    // 4. 循环推数据。第 4 个参数是 RTP 时间戳增量：
    //    H264/H265 时钟 90000，30fps 每帧 3000；OPUS 时钟 48000，20ms 每帧 960
    while (running) {
        rtc_write_sample(video, h264_frame, h264_len, 3000);
        rtc_write_sample(audio, opus_frame, opus_len, 960);
    }

    // 5. 清理：先取消发布，再销毁轨道，最后销毁实例
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
发布视频后，SFU 会在需要时通过 RTCP（PLI/FIR）要求你立刻产出一个关键帧（例如有新观众起播）。请在发布前用 `rtc_set_keyframe_request_callback` 注册回调，并在回调里让编码器立即编一个 IDR，否则新加入的观众可能长时间黑屏。详见 [发布与推流](/zh/rtc/capi/api-reference/publish)。
</Warning>

---

## 开启日志

排查问题时把日志级别调到 `RTC_LOG_DEBUG`，需在 `rtc_create` 之前调用：

```c
rtc_set_log_level(RTC_LOG_DEBUG);   // 0=DEBUG 1=INFO 2=WARN 3=ERROR
```

---

## 常见问题

| 现象 | 排查方向 |
| --- | --- |
| `rtc_join_channel_sync` 返回 `RTC_TIMEOUT`（-4） | Token 过期、网络不通、服务端地址不可达 |
| `rtc_join_channel_sync` 返回 `RTC_ERROR`（-1） | Token 会话已被占用或已失效（`1032`），重新签发 |
| 订阅/发布返回 `RTC_NOT_CONNECTED`（-3） | 还没入会就调用了，需在 `join` 成功之后再调 |
| 收不到 `on_track_sample` | 没开自动订阅，也没手动 `rtc_subscribe_*` |
| 观众端画面迟迟不出来 | 推流端没实现关键帧请求回调 |

---

## 下一步

+ [接口文档](/zh/rtc/capi/api-reference/engine)：完整 API 参考
+ [合成流（program）](/zh/rtc/capi/advanced/mcu)：服务端统一合成的频道级音视频流
+ [SeaStart 进阶能力](/zh/rtc/capi/advanced/seastart)：切层、网络质量、活跃说话人
