---
title: "合成流（program）"
description: "SRTC C SDK 中频道级合成流的发布（MCU 侧）与订阅（观众侧）"
---

合成流（program）是**频道级**的音视频流：由服务端 MCU 程序把频道内所有人合成为一路，所有订阅者收到的画面和声音完全一致。

典型用途：

+ 不发言的观众只订一路流，省带宽也省解码开销
+ 旁路录制 / 转推直播

---

## 保留标识

合成流不属于任何普通用户，它挂在一个系统身份下。头文件里已把这三个保留常量开放出来：

```c
#define RTC_MCU_PUBLISHER_UID "__mcu__"   // 合成流发布者 uid（音视频共用此身份）
#define RTC_TRACK_AMCU_ID     "__amcu__"  // 音频合成流 trackId
#define RTC_TRACK_MCU_ID      "__mcu__"   // 视频合成流 trackId
```

---

## 发布（MCU 程序侧）

<Warning>
发布合成流必须**以 MCU 身份接入**：服务端签发的 Token 里 `uid` 必须是 `__mcu__`，否则发布接口返回 `RTC_ERROR`。
</Warning>

### rtc_publish_mcu_video_track

```c
int rtc_publish_mcu_video_track(void* handle, void* track_handle, rtc_publish_options_t* options);
```

发布视频合成流。与 `rtc_publish_local_track` 的区别只有两点：内部强制使用保留 `trackId`（不可自定义），以及要求 MCU 身份。`track_handle` 须用视频 codec 创建，`options` 填 `desc` / `width` / `height` / `fps`。

### rtc_publish_mcu_audio_track

```c
int rtc_publish_mcu_audio_track(void* handle, void* track_handle, rtc_publish_options_t* options);
```

发布音频合成流（混音流），语义同上。`track_handle` 须用音频 codec 创建，`options` 填 `desc` / `sample_rate` / `channel_count`。

**返回值**（两个接口相同）

| 返回值 | 含义 |
| --- | --- |
| `RTC_OK` | 发布成功 |
| `RTC_INVALID_PARAM` | 句柄无效、轨道句柄无效，或 `options` 为 `NULL` |
| `RTC_NOT_CONNECTED` | 尚未加入频道 |
| `RTC_ERROR` | 发布失败，最常见的原因是**当前身份不是 `__mcu__`** |

### 示例

```c
// 视频合成流
void* v = rtc_create_local_track(RTC_CODEC_H264);
rtc_publish_options_t vopts = {0};
strcpy(vopts.desc, "mcu_video");
vopts.width = 1280; vopts.height = 720; vopts.fps = 25;
rtc_publish_mcu_video_track(rtc, v, &vopts);      // trackId 固定为 __mcu__

// 音频混音流
void* a = rtc_create_local_track(RTC_CODEC_OPUS);
rtc_publish_options_t aopts = {0};
strcpy(aopts.desc, "mcu_audio");
aopts.sample_rate = 48000; aopts.channel_count = 2;
rtc_publish_mcu_audio_track(rtc, a, &aopts);      // trackId 固定为 __amcu__

// 推数据与普通轨道完全一致
rtc_write_sample(v, h264_frame, h264_len, 3600);  // 25fps: 90000/25
rtc_write_sample(a, opus_frame, opus_len, 960);
```

---

## 订阅（观众侧）

C 接口没有 RemoteTrack 句柄，所以合成流不另设订阅接口 —— 用通用的订阅接口配合保留常量即可：

```c
rtc_subscribe_video(rtc, RTC_MCU_PUBLISHER_UID, RTC_TRACK_MCU_ID);   // 订视频合成流
rtc_subscribe_audio(rtc, RTC_MCU_PUBLISHER_UID, RTC_TRACK_AMCU_ID);  // 订音频合成流

// 数据照常从 rtc_set_track_sample_callback 回调出来

// 取消订阅同样传保留常量
rtc_unsubscribe(rtc, RTC_MCU_PUBLISHER_UID, RTC_TRACK_MCU_ID);
rtc_unsubscribe(rtc, RTC_MCU_PUBLISHER_UID, RTC_TRACK_AMCU_ID);
```

---

## 什么时候不该用合成流

<Warning>
**参与会话的人想"听全场"，不要订阅音频合成流。** 合成流里包含你自己的声音，订了就会有回声。

正确做法是 `rtc_set_auto_subscribe(rtc, 1, 0)` 自动订阅所有人的音频，各路数据从 `track_sample` 回调进来后由业务侧自行混音（混的时候把自己那一路排除掉）。

合成流是给**不发声的观众**和**录制/转推**用的。
</Warning>
