---
title: "SeaStart 进阶能力"
description: "SRTC C SDK 在 SeaStart 引擎下的 simulcast 切层、网络质量上报与活跃说话人"
---

以下能力仅在频道使用 **SeaStart 引擎**时可用。其它引擎下这些回调不会触发，主动接口会返回错误 —— 引擎由服务端下发的频道配置决定，业务代码无需判断，做好"没有回调也能正常工作"的兜底即可。

三个能力对应三个独立的强类型回调，与 `track_event` / `track_sample` 风格一致，C 侧无需解析 JSON。

---

## 切层（simulcast）

当发布端推了 simulcast 多层流时，订阅侧的层切换是**全自动**的：SDK 会自动把可用的各层登记为候选，SFU 根据带宽估计（BWE）在候选层之间切换。你不需要做任何配置，通常只需要监听切层结果。

### 切层完成回调

```c
typedef struct {
    char    sub_key[128];        // 稳定订阅句柄 "pub_uid:track_id"
    char    from_track_id[64];   // 切层前命中层；首次起播时为空字符串
    char    to_track_id[64];     // 切层后命中层
    char    reason[32];          // 切层原因，见下表
    int64_t latency_ms;          // 从发起切层到真正切到目标层的耗时
} rtc_layer_switched_t;

typedef void (*rtc_layer_switched_callback)(void* context, const rtc_layer_switched_t* data);
void rtc_set_layer_switched_callback(void* handle, rtc_layer_switched_callback callback, void* context);
```

`reason` 取值：

| 值 | 含义 |
| --- | --- |
| `bwe_down` | 带宽下降，SFU 自动降层 |
| `bwe_up` | 带宽恢复，SFU 自动升层 |
| `track_refresh` | 轨道刷新 |
| `track_upgrade` | 轨道升级 |
| `track_ended` | 当前层结束，回退到其它层 |
| `client` | 客户端主动调用 `rtc_switch_layer` |

```c
static void on_layer_switched(void* ctx, const rtc_layer_switched_t* d) {
    printf("layer %s -> %s (%s, %lldms)\n",
           d->from_track_id[0] ? d->from_track_id : "-",
           d->to_track_id, d->reason, (long long)d->latency_ms);
}

rtc_set_layer_switched_callback(rtc, on_layer_switched, NULL);
```

<Note>
**当前命中的是哪一层？** 订阅句柄（`sub_key` 里的 `track_id`）在整个订阅期间保持稳定，但实际命中的层会被动态切换。监听 `layer_switched` 拿到的 `to_track_id` 就是当前命中层，需要的话自行缓存一份 `sub_key → 当前层` 的映射即可。
</Note>

### rtc_switch_layer

```c
int rtc_switch_layer(void* handle, const char* pub_uid,
                     const char* track_id, const char* target_track_id);
```

主动请求 SFU 切到指定层。适合大小窗切换、窗口进入后台时主动降级这类场景。

| 参数 | 说明 |
| --- | --- |
| `pub_uid` | 发布者 uid |
| `track_id` | 订阅时使用的稳定句柄 trackId（一般是主层 ID） |
| `target_track_id` | 目标层 trackId，**必须在订阅时的候选池内** |

**返回值**：`RTC_OK`（请求已发出）/ `RTC_INVALID_PARAM`（句柄无效或参数为 `NULL`）/ `RTC_NOT_CONNECTED`（未入会）/ `RTC_ERROR`（引擎拒绝）。

```c
// 把订阅 u1001 的主层切到最小层
rtc_switch_layer(rtc, "u1001", big_track_id, small_track_id);
// 切层结果通过 on_layer_switched 通知，reason = "client"
```

<Note>
请求成功只代表请求已发出，真正切到目标层要等 `layer_switched` 回调。

本 SDK 只支持订阅侧的多层切换，不支持**发布** simulcast 多层流。
</Note>

---

## 网络质量

### 周期上报回调

SFU 周期性（典型 1Hz）上报上下行质量。

```c
// 单方向的质量样本
typedef struct {
    double  score;      // 质量分 0-100
    char    level[16];  // "excellent" | "good" | "poor" | "lost"
    double  mos;        // 1.0-4.5
    double  loss;       // 丢包率 0-1
    double  rtt;        // 毫秒
    double  jitter;     // 毫秒
    int64_t packets;    // 本轮参与统计的包数
    double  bitrate;    // 平均码率 kbps（不参与 score 计算）
    int64_t bytes;      // 本窗口字节数
} rtc_quality_sample_t;

typedef struct {
    int64_t              ts;   // SFU 生成报告的 Unix 毫秒时间戳
    rtc_quality_sample_t pub;  // 上行（本端 → SFU）
    rtc_quality_sample_t sub;  // 下行（SFU → 本端）
} rtc_connection_quality_t;

typedef void (*rtc_connection_quality_callback)(void* context, const rtc_connection_quality_t* q);
void rtc_set_connection_quality_callback(void* handle, rtc_connection_quality_callback callback, void* context);
```

```c
static void on_connection_quality(void* ctx, const rtc_connection_quality_t* q) {
    // 画信号塔看 q->pub.level / q->sub.level
    // 数值面板看 mos / loss / rtt / jitter / bitrate
    printf("pub=%s(%.1f) sub=%s(%.1f) rtt=%.0fms\n",
           q->pub.level, q->pub.score, q->sub.level, q->sub.score, q->sub.rtt);
}

rtc_set_connection_quality_callback(rtc, on_connection_quality, NULL);
```

<Warning>
每一帧上报都会触发回调，**节流由业务方自己做**。要写日志或落监控的话请自行降采样。
</Warning>

### rtc_get_connection_quality

```c
int rtc_get_connection_quality(void* handle, rtc_connection_quality_t* out);
```

主动拉取最近一帧质量数据。适合刚入会、还没等到第一次周期上报时先把 UI / 监控指标填上。

`out` 由调用方提供，SDK 直接填字段，无需释放。

**返回值**

| 返回值 | 含义 |
| --- | --- |
| `RTC_OK` | 已写入 `out` |
| `RTC_NOT_CONNECTED` | 尚未入会，或还没收到第一帧质量数据 |
| `RTC_INVALID_PARAM` | 句柄无效，或 `out` 为 `NULL` |

```c
rtc_connection_quality_t q;
int ret = rtc_get_connection_quality(rtc, &q);
if (ret == RTC_OK) {
    printf("pub=%s loss=%.2f sub=%s loss=%.2f rtt=%.0f\n",
           q.pub.level, q.pub.loss, q.sub.level, q.sub.loss, q.sub.rtt);
} else if (ret == RTC_NOT_CONNECTED) {
    // 还没有数据，等回调即可
}
```

---

## 活跃说话人

```c
typedef struct {
    char   uid[64];
    char   track_id[64];  // 同一用户有多路音频时用于区分
    double level;         // 0.0-1.0，越大越响
} rtc_active_speaker_t;

typedef void (*rtc_active_speakers_callback)(void* context, int64_t ts,
                                             const rtc_active_speaker_t* speakers,
                                             int speakers_count);
void rtc_set_active_speakers_callback(void* handle, rtc_active_speakers_callback callback, void* context);
```

SDK 会把 SFU 的增量事件合并成**全量快照**再抛上来，按 `level` 降序排列，业务侧直接整体覆盖 UI 即可，不需要自己做差量合并。无人说话时 `speakers_count = 0`、`speakers = NULL`。

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
`speakers` 数组由 SDK 在回调期间持有，**回调返回后立即释放**。需要跨回调保留必须自行拷贝。
</Warning>
