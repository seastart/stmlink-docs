---
title: "发布与推流"
description: "SRTC C SDK 本地轨道的创建、发布、推送编码数据与关键帧请求响应"
---

C SDK 不做采集也不做编码。推流的完整链路是：**业务方采集 → 业务方编码 → `rtc_write_sample` 喂裸数据 → SDK 打包发送**。

标准流程：

```text
rtc_create_local_track  →  rtc_set_keyframe_request_callback  →  rtc_publish_local_track
        →  循环 rtc_write_sample  →  rtc_unpublish_local_track  →  rtc_destroy_local_track
```

---

## rtc_create_local_track

```c
void* rtc_create_local_track(int codec);
```

创建一条本地轨道，返回轨道句柄；失败返回 `NULL`。

| 参数 | 说明 |
| --- | --- |
| `codec` | 编码格式常量：`RTC_CODEC_H264` / `RTC_CODEC_H265` / `RTC_CODEC_VP8` / `RTC_CODEC_VP9` / `RTC_CODEC_AV1` / `RTC_CODEC_OPUS` / `RTC_CODEC_AAC` |

轨道是音频还是视频由 codec 决定，不需要额外指定。

## rtc_destroy_local_track

```c
void rtc_destroy_local_track(void* track_handle);
```

销毁本地轨道。已发布的轨道应先 `rtc_unpublish_local_track` 再销毁。

---

## rtc_publish_local_track

```c
int rtc_publish_local_track(void* handle, void* track_handle, rtc_publish_options_t* options);
```

发布本地轨道到频道。

| 参数 | 说明 |
| --- | --- |
| `handle` | 实例句柄 |
| `track_handle` | `rtc_create_local_track` 返回的轨道句柄 |
| `options` | 发布选项，见下方 |

**发布选项 `rtc_publish_options_t`**

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `desc` | `char[64]` | 轨道描述，**必填且不能为空串**，如 `"camera"` / `"screen"` / `"microphone"` |
| `width` | `int` | 视频宽度，视频轨道必填 |
| `height` | `int` | 视频高度，视频轨道必填 |
| `fps` | `int` | 帧率，视频轨道必填 |
| `sample_rate` | `int` | 采样率，音频轨道必填 |
| `channel_count` | `int` | 声道数，音频轨道必填 |
| `angle` | `int` | 视频角度，可选 |
| `bitrate` | `int` | 码率（bps），可选 |
| `props` | `const char*` | 自定义业务属性，JSON 对象字符串，可选 |

<Note>
`props` 解析失败时 SDK 只打一条告警日志、按无自定义属性继续发布，不会让发布失败。
</Note>

**返回值**

| 返回值 | 含义 |
| --- | --- |
| `RTC_OK` | 发布成功 |
| `RTC_INVALID_PARAM` | 句柄无效、轨道句柄无效，或 `options` 为 `NULL` |
| `RTC_NOT_CONNECTED` | 尚未加入频道 |
| `RTC_ERROR` | 发布失败（必填参数缺失、引擎拒绝、协商失败等） |

## rtc_unpublish_local_track

```c
int rtc_unpublish_local_track(void* handle, void* track_handle);
```

取消发布。返回值同上。

## rtc_publish_mcu_video_track / rtc_publish_mcu_audio_track

发布频道级合成流，见 [合成流（program）](/zh/rtc/capi/advanced/mcu)。

---

## rtc_write_sample

```c
int rtc_write_sample(void* track_handle, uint8_t* data, int length, uint32_t samples);
```

向已发布的轨道推送一帧编码数据。

| 参数 | 说明 |
| --- | --- |
| `data` | 编码后的裸数据。视频为一个完整帧（Annex-B NALU），音频为一个编码包 |
| `length` | 数据字节数 |
| `samples` | **RTP 时间戳增量**，不是字节数也不是毫秒数 |

`samples` 按各编码的时钟频率算：

| 编码 | 时钟频率 | 常见取值 |
| --- | --- | --- |
| H264 / H265 / VP8 / VP9 / AV1 | 90000 | 30fps → `90000/30 = 3000`；25fps → `3600` |
| OPUS | 48000 | 20ms 一包 → `48000 * 0.02 = 960` |

**返回值**

| 返回值 | 含义 |
| --- | --- |
| `RTC_OK` | 写入成功 |
| `RTC_INVALID_PARAM` | 轨道句柄无效，或 `data` 为 `NULL` / `length <= 0` |
| `RTC_ERROR` | 写入失败（轨道未发布、底层发送出错等） |

<Note>
SDK 会拷贝一份传入的数据，调用返回后你可以立即复用或释放 `data` 缓冲区。
</Note>

---

## rtc_set_keyframe_request_callback

```c
typedef void (*rtc_keyframe_request_callback)(void* context, const char* track_id);
void rtc_set_keyframe_request_callback(void* track_handle,
                                       rtc_keyframe_request_callback callback,
                                       void* context);
```

设置关键帧请求回调。当 SFU 通过 RTCP（PLI / FIR）要求这条轨道立即产出关键帧时触发，业务方应在回调里让编码器立刻编一个 IDR 并通过 `rtc_write_sample` 发出去。

<Warning>
**必须在发布之前对该轨道设置。** 不设置的话，新加入的观众要等到编码器下一个自然 GOP 才出画面 —— GOP 长的话就是几秒钟黑屏。

回调在独立线程触发，注意与编码线程的同步。传 `NULL` 可清除回调。
</Warning>

```c
static void on_keyframe_request(void* ctx, const char* track_id) {
    // 不要在这里做重活，置个标志让编码线程下一帧编 IDR
    encoder_request_idr(track_id);
}

void* video = rtc_create_local_track(RTC_CODEC_H264);
rtc_set_keyframe_request_callback(video, on_keyframe_request, NULL);
rtc_publish_local_track(rtc, video, &vopts);   // 设置完回调再发布
```

---

## 完整示例

```c
// 1. 创建轨道
void* video = rtc_create_local_track(RTC_CODEC_H264);
void* audio = rtc_create_local_track(RTC_CODEC_OPUS);

// 2. 视频轨道注册关键帧请求回调（发布前）
rtc_set_keyframe_request_callback(video, on_keyframe_request, NULL);

// 3. 配置发布选项
rtc_publish_options_t vopts = {0};
strcpy(vopts.desc, "camera");
vopts.width = 1280; vopts.height = 720; vopts.fps = 30;

rtc_publish_options_t aopts = {0};
strcpy(aopts.desc, "microphone");
aopts.sample_rate = 48000; aopts.channel_count = 2;

// 4. 发布
rtc_publish_local_track(rtc, video, &vopts);
rtc_publish_local_track(rtc, audio, &aopts);

// 5. 推数据
rtc_write_sample(video, h264_frame, h264_len, 3000);  // 30fps
rtc_write_sample(audio, opus_frame, opus_len, 960);   // 20ms

// 6. 收尾
rtc_unpublish_local_track(rtc, video);
rtc_unpublish_local_track(rtc, audio);
rtc_destroy_local_track(video);
rtc_destroy_local_track(audio);
```

---

<Note>
C 接口不支持发布 simulcast 多层流 —— 服务端场景（录制 / MCU / AI Agent）几乎不需要主动发多层。订阅侧的多层自动切换由 SDK 自动完成，无需任何配置。确有发多层的需求请联系我们。
</Note>
