---
title: "订阅与收流"
description: "SRTC C SDK 订阅远端音视频轨道、取消订阅与主动请求关键帧"
---

订阅有两种方式：

+ **自动订阅** —— 入会前调 `rtc_set_auto_subscribe`，SDK 自动订上所有远端轨道。录制、混音、AI 接入这类"全都要"的场景用这个
+ **手动订阅** —— 在轨道事件回调里挑需要的轨道逐个订阅

两种方式的媒体数据都走同一个 `rtc_set_track_sample_callback` 回调。

---

## rtc_subscribe_audio

```c
int rtc_subscribe_audio(void* handle, const char* uid, const char* track_id);
```

订阅指定用户的音频轨道。

| 参数 | 说明 |
| --- | --- |
| `uid` | 发布者 uid。订阅音频合成流时传 `RTC_MCU_PUBLISHER_UID` |
| `track_id` | 轨道 ID。订阅音频合成流时传 `RTC_TRACK_AMCU_ID` |

**返回值**

| 返回值 | 含义 |
| --- | --- |
| `RTC_OK` | 订阅成功 |
| `RTC_INVALID_PARAM` | 句柄无效 |
| `RTC_NOT_CONNECTED` | 尚未加入频道 |
| `RTC_ERROR` | 订阅失败（轨道不存在、引擎拒绝等） |

## rtc_subscribe_video

```c
int rtc_subscribe_video(void* handle, const char* uid, const char* track_id);
```

订阅指定用户的视频轨道。参数与返回值同 `rtc_subscribe_audio`；订阅视频合成流时传 `RTC_MCU_PUBLISHER_UID` / `RTC_TRACK_MCU_ID`。

<Note>
合成流（program）的订阅不另设接口，统一用上面两个通用接口配合保留常量完成。详见 [合成流（program）](/zh/rtc/capi/advanced/mcu)。
</Note>

## rtc_unsubscribe

```c
int rtc_unsubscribe(void* handle, const char* uid, const char* track_id);
```

取消订阅。合成流传发布者 uid 加对应的保留 `track_id`。返回值同上。

取消订阅后，SDK 会自动停止该轨道的数据收集，对应的 `track_sample` 回调随之停止。

---

## 手动订阅示例

```c
static void* g_rtc = NULL;

// 在轨道事件里挑要订阅的轨道
static void on_track_event(void* ctx, const char* uid,
                           rtc_track_info_t* track, int event_type) {
    if (event_type != 0) return;   // 只处理"新增"

    // 只订阅目标用户的视频
    if (strcmp(uid, "target_user_id") == 0 && track->kind == 1) {
        rtc_subscribe_video(g_rtc, uid, track->track_id);
    }
    // 所有人的音频都订上
    if (track->kind == 0) {
        rtc_subscribe_audio(g_rtc, uid, track->track_id);
    }
}

int main() {
    g_rtc = rtc_create();
    rtc_set_track_event_callback(g_rtc, on_track_event, NULL);
    rtc_set_track_sample_callback(g_rtc, on_track_sample, NULL);
    // 不开自动订阅
    rtc_join_channel_sync(g_rtc, token, 10000);
    // ...
}
```

---

## rtc_request_key_frame

```c
int rtc_request_key_frame(void* handle, const char* uid, const char* track_id);
```

主动请求某条远端视频轨道立即下发关键帧（向发布端发送 RTCP PLI）。

| 参数 | 说明 |
| --- | --- |
| `uid` | 发布者 uid |
| `track_id` | 已订阅的视频轨道 ID |

**返回值**

| 返回值 | 含义 |
| --- | --- |
| `RTC_OK` | 请求已发出 |
| `RTC_INVALID_PARAM` | 句柄无效、参数为空，或该轨道不支持（非视频/未就绪） |
| `RTC_NOT_CONNECTED` | 尚未加入频道 |

**什么时候调用**

+ 刚订阅上一条视频、想尽快出画面
+ 解码器报错、画面花屏或灰屏，需要刷新参考帧

**什么时候不用调用**

<Note>
**丢包不需要你请求关键帧。** 少量丢包由 SDK 的 NACK 重传自动补回，不会导致画面损坏，因此 SDK 不会、也不建议你基于丢包率去请求关键帧 —— 那样只会触发不必要的关键帧，反而推高码率、加剧拥塞。

请只在**你的解码器真的报错**或画面已经花屏时才调用。

接口已内置限流（每秒最多 1 次），逐帧解码报错时反复调用也不会把请求刷爆。
</Note>

---

## 相关

+ 发布端如何响应关键帧请求：[发布与推流](/zh/rtc/capi/api-reference/publish)
+ simulcast 多层订阅与主动切层：[SeaStart 进阶能力](/zh/rtc/capi/advanced/seastart)
