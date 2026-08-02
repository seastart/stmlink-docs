---
title: "用户信息查询"
description: "SRTC C SDK 查询频道内用户列表与单个用户信息，以及对应的内存释放规则"
---

用户信息查询接口返回的结构体里含有 SDK 动态分配的内存（`props` 字符串和 `stream_tracks` 数组），**必须**用配套的 free 接口释放，否则内存泄漏。

---

## rtc_get_users_info

```c
int rtc_get_users_info(void* handle, rtc_user_info_t** users, int* count);
```

获取频道内全部用户信息。

| 参数 | 说明 |
| --- | --- |
| `users` | 出参，SDK 分配的用户数组首地址 |
| `count` | 出参，用户数量 |

**返回值**

| 返回值 | 含义 |
| --- | --- |
| `RTC_OK` | 成功。频道内无用户时 `*count = 0`、`*users = NULL`，此时**不需要**释放 |
| `RTC_INVALID_PARAM` | 句柄无效 |
| `RTC_NOT_CONNECTED` | 尚未加入频道 |
| `RTC_ERROR` | 内存分配失败 |

```c
rtc_user_info_t* users = NULL;
int count = 0;

if (rtc_get_users_info(rtc, &users, &count) == RTC_OK) {
    printf("在线用户: %d\n", count);
    for (int i = 0; i < count; i++) {
        printf("- %s (%s), 设备类型=%d, 观众=%d, 发布轨道数=%d\n",
               users[i].uid, users[i].name,
               users[i].device_type, users[i].is_audience,
               users[i].stream_track_count);

        // 遍历该用户发布的轨道
        for (int j = 0; j < users[i].stream_track_count; j++) {
            rtc_track_info_t* t = &users[i].stream_tracks[j];
            printf("    %s [%s] %s\n", t->track_id,
                   t->kind == 0 ? "audio" : "video",
                   rtc_codec_to_string(t->codec));
        }
    }
    rtc_free_users_info(users, count);   // 必须传回 count
}
```

## rtc_free_users_info

```c
void rtc_free_users_info(rtc_user_info_t* users, int count);
```

释放 `rtc_get_users_info` 返回的用户数组，包括每个用户的 `props`、`stream_tracks` 以及数组本身。

<Warning>
`count` 必须传 `rtc_get_users_info` 返回的那个值。传小了会漏释放，传大了会越界。
</Warning>

---

## rtc_get_user_info

```c
int rtc_get_user_info(void* handle, const char* uid, rtc_user_info_t* user);
```

获取单个用户信息。`user` 由调用方提供（栈上变量即可），SDK 填充其字段。

**返回值**

| 返回值 | 含义 |
| --- | --- |
| `RTC_OK` | 成功 |
| `RTC_INVALID_PARAM` | 句柄无效，或 `uid` / `user` 为 `NULL` |
| `RTC_NOT_CONNECTED` | 尚未加入频道 |
| `RTC_ERROR` | 用户不存在 |

```c
rtc_user_info_t user;
if (rtc_get_user_info(rtc, "user123", &user) == RTC_OK) {
    printf("%s / %s / channel=%s / sid=%s\n",
           user.uid, user.name, user.channel, user.sid);
    rtc_free_user_info(&user);   // 结构体本身在栈上，释放的是里面的动态内存
} else {
    printf("用户不存在\n");
}
```

## rtc_free_user_info

```c
void rtc_free_user_info(rtc_user_info_t* user);
```

释放单个 `rtc_user_info_t` 内部的动态内存（`props` 和 `stream_tracks`），不释放结构体本身。

<Warning>
即使 `user` 是栈上变量，只要 `rtc_get_user_info` 返回了 `RTC_OK`，就必须调用一次 `rtc_free_user_info`。
</Warning>

---

字段说明见 [类型定义 · rtc_user_info_t](/zh/rtc/capi/types#rtc_user_info_t)。
