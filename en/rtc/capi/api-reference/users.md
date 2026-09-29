---
title: "User info queries"
description: "C SDK functions for querying the channel's user list, a single user, the local user, and channel info, and the matching free functions you must call to avoid leaking the SDK-allocated props and stream_tracks memory."
---

The structs returned by the user info query functions contain memory allocated dynamically by the SDK (the `props` string and the `stream_tracks` array). You **must** release it with the matching free function; otherwise memory leaks.

---

## rtc_get_users_info

```c
int rtc_get_users_info(void* handle, rtc_user_info_t** users, int* count);
```

Gets info for every user in the channel.

| Parameter | Description |
| --- | --- |
| `users` | Output: address of the first element of the user array allocated by the SDK |
| `count` | Output: number of users |

**Returns**

| Return value | Meaning |
| --- | --- |
| `RTC_OK` | Success. When there are no users in the channel, `*count = 0` and `*users = NULL`; in that case you **don't need** to free anything |
| `RTC_INVALID_PARAM` | Invalid handle |
| `RTC_NOT_CONNECTED` | Not yet joined to the channel |
| `RTC_ERROR` | Memory allocation failed |

```c
rtc_user_info_t* users = NULL;
int count = 0;

if (rtc_get_users_info(rtc, &users, &count) == RTC_OK) {
    printf("Online users: %d\n", count);
    for (int i = 0; i < count; i++) {
        printf("- %s (%s), device type=%d, audience=%d, published tracks=%d\n",
               users[i].uid, users[i].name,
               users[i].device_type, users[i].is_audience,
               users[i].stream_track_count);

        // Iterate over the tracks this user has published
        for (int j = 0; j < users[i].stream_track_count; j++) {
            rtc_track_info_t* t = &users[i].stream_tracks[j];
            printf("    %s [%s] %s\n", t->track_id,
                   t->kind == 0 ? "audio" : "video",
                   rtc_codec_to_string(t->codec));
        }
    }
    rtc_free_users_info(users, count);   // You must pass count back
}
```

## rtc_free_users_info

```c
void rtc_free_users_info(rtc_user_info_t* users, int count);
```

Frees the user array returned by `rtc_get_users_info`, including each user's `props` and `stream_tracks` as well as the array itself.

<Warning>
`count` must be the value returned by `rtc_get_users_info`. Passing a smaller value leaks memory; passing a larger one goes out of bounds.
</Warning>

---

## rtc_get_user_info

```c
int rtc_get_user_info(void* handle, const char* uid, rtc_user_info_t* user);
```

Gets info for a single user. `user` is provided by the caller (a stack variable is fine), and the SDK fills in its fields.

**Returns**

| Return value | Meaning |
| --- | --- |
| `RTC_OK` | Success |
| `RTC_INVALID_PARAM` | Invalid handle, or `uid` / `user` is `NULL` |
| `RTC_NOT_CONNECTED` | Not yet joined to the channel |
| `RTC_ERROR` | User doesn't exist |

```c
rtc_user_info_t user;
if (rtc_get_user_info(rtc, "user123", &user) == RTC_OK) {
    printf("%s / %s / channel=%s / sid=%s\n",
           user.uid, user.name, user.channel, user.sid);
    rtc_free_user_info(&user);   // The struct itself is on the stack; this frees the dynamic memory inside it
} else {
    printf("User doesn't exist\n");
}
```

## rtc_free_user_info

```c
void rtc_free_user_info(rtc_user_info_t* user);
```

Frees the dynamic memory inside a single `rtc_user_info_t` (`props` and `stream_tracks`), but not the struct itself.

<Warning>
Even if `user` is a stack variable, as long as `rtc_get_user_info` returned `RTC_OK`, you must call `rtc_free_user_info` once.
</Warning>

---

For field descriptions, see [Types · rtc_user_info_t](/en/rtc/capi/types#rtc_user_info_t).

---

## rtc_get_local_user_info

```c
int rtc_get_local_user_info(void* handle, rtc_user_info_t* user);
```

Gets the local user's info (`uid`, `sid`, etc.), since 0.0.9. You also need to call `rtc_free_user_info` when you're done with it.

**Returns:** `RTC_OK` / `RTC_INVALID_PARAM` (invalid handle or `user`) / `RTC_NOT_CONNECTED` (not yet joined).

---

## rtc_get_channel_info

```c
int rtc_get_channel_info(void* handle, rtc_channel_info_t* info);
void rtc_free_channel_info(rtc_channel_info_t* info);
```

Gets channel info, since 0.0.9. For fields, see [Types · rtc_channel_info_t](/en/rtc/capi/types#rtc_channel_info_t). After it returns `RTC_OK`, you must call `rtc_free_channel_info` to free the `props` inside it.

**Returns:** `RTC_OK` / `RTC_INVALID_PARAM` / `RTC_NOT_CONNECTED` (not yet joined).
