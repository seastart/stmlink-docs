---
title: "自定义消息"
description: "SRTC C SDK 接收频道内自定义消息，以及 content JSON 的解析与内存规则"
---

频道内的自定义消息可以用来传业务信令，比如举手、白板同步、状态广播。C 接口目前只提供**接收**能力：其它端（Web / iOS / Android / Go SDK）通过 `SendCustomMsg` 发出的消息会透传到这个回调。

---

## rtc_set_custom_msg_callback

```c
typedef struct {
    char        action[64];      // 业务动作标识
    char        sid[128];        // 发送者会话 ID
    char        uid[64];         // 发送者用户 ID
    char        channel[128];    // 频道名
    int         is_private;      // 1=私有路由（点对点），0=公开路由（频道广播）
    const char* content_json;    // content 的 JSON 字符串；无 content 时为 NULL
} rtc_custom_msg_t;

typedef void (*rtc_custom_msg_callback)(void* context, const rtc_custom_msg_t* msg);
void rtc_set_custom_msg_callback(void* handle, rtc_custom_msg_callback callback, void* context);
```

`action`、`sid`、`uid`、`channel`、`is_private` 都是强类型字段，直接取用即可。

`content` 可以是任意 JSON 值（对象 / 数组 / 标量），C 接口统一把它序列化成 `content_json` 字符串透传，你用 cJSON、jansson 等库自行解析。

---

## 示例

```c
#include <cjson/cJSON.h>

static void on_custom_msg(void* ctx, const rtc_custom_msg_t* m) {
    printf("custom msg: action=%s uid=%s private=%d\n",
           m->action, m->uid, m->is_private);

    if (m->content_json) {
        cJSON* root = cJSON_Parse(m->content_json);
        if (root) {
            cJSON* v = cJSON_GetObjectItem(root, "some_field");
            if (cJSON_IsString(v)) {
                handle_business(m->action, v->valuestring);
            }
            cJSON_Delete(root);
        }
    }
}

rtc_set_custom_msg_callback(rtc, on_custom_msg, NULL);
```

---

## 内存与线程

<Warning>
`content_json` 由 SDK 在回调期间持有，**回调返回后立即 `free`**。需要跨回调保留必须自行 `strdup` 一份。

回调在 SDK 内部线程触发，不要在里面做耗时操作。
</Warning>

<Note>
`content` 为空或序列化失败时，`content_json` 为 `NULL`，解析前务必判空。
</Note>
