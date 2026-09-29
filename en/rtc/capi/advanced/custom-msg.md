---
title: "Custom messages"
description: "How the C SDK receives in-channel custom messages sent by other clients: the rtc_custom_msg_t fields, parsing content_json with a JSON library, and the memory and threading rules for the callback."
---

In-channel custom messages can carry your own signaling, such as hand raising, whiteboard sync, or status broadcasts. The C interface currently only supports **receiving**: messages sent by other clients (Web / iOS / Android / Go SDK) through `SendCustomMsg` are passed through to this callback.

---

## rtc_set_custom_msg_callback

```c
typedef struct {
    char        action[64];      // Business action identifier
    char        sid[128];        // Sender's session ID
    char        uid[64];         // Sender's user ID
    char        channel[128];    // Channel name
    int         is_private;      // 1=private routing (point-to-point), 0=public routing (channel broadcast)
    const char* content_json;    // content as a JSON string; NULL when there is no content
} rtc_custom_msg_t;

typedef void (*rtc_custom_msg_callback)(void* context, const rtc_custom_msg_t* msg);
void rtc_set_custom_msg_callback(void* handle, rtc_custom_msg_callback callback, void* context);
```

`action`, `sid`, `uid`, `channel`, and `is_private` are all strongly typed fields you can use directly.

`content` can be any JSON value (object / array / scalar). The C interface always serializes it into the `content_json` string and passes it through; parse it yourself with a library such as cJSON or jansson.

---

## Example

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

## Memory and threading

<Warning>
`content_json` is held by the SDK during the callback and **`free`d as soon as the callback returns**. To keep it beyond the callback, you must `strdup` a copy yourself.

The callback fires on an internal SDK thread; don't do slow work in it.
</Warning>

<Note>
When `content` is empty or serialization fails, `content_json` is `NULL`. Always check for `NULL` before parsing.
</Note>
