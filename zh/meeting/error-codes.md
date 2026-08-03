---
title: "错误码规则"
description: "SMeeting 错误码的编号规则，以及为什么你会同时看到 2xxxxx 和 1xxxxx 两类错误码"
---

`0` 代表成功，非 0 都是错误。

所有错误码都是 **前缀 + 3 位具体码（001-999）** 的结构。看懂前缀，你就能立刻判断这个错误来自**哪一层**、**哪个平台**。

---

## 怎么读一个错误码

```text
  2 0 3 0 0 1
  │ │ │ └─┴─┴── 具体码 001-999
  │ │ └──────── 端侧类型：3 = iOS
  └─┴────────── 业务层：2 = SMeeting
```

分三种情况：

| 位数 | 来源 | 前缀 | 示例 |
| --- | --- | --- | --- |
| 4 位 | **服务端**返回 | `2` | `2xxx` 会议服务的业务错误 |
| 6 位，第 3 位为 `0` | 客户端 SDK **各端通用** | `200` | `200xxx` |
| 6 位 | 客户端 SDK **特定平台** | `20` + 端侧类型 | `203001` iOS 端错误 |

---

## 端侧类型

| 类型 | 平台 | SMeeting 前缀 |
| :---: | --- | --- |
| 1 | Windows | `201` |
| 2 | Android 手机 | `202` |
| 3 | iOS 手机 | `203` |
| 4 | Linux C/C++ | `204` |
| 5 | macOS | `205` |
| 6 | Web | `206` |
| 7 | 小程序 | `207` |
| 8 | Android 盒子 | `208` |
| 9 | Android 嵌入式 | `209` |

<Note>
Swift SDK 同时支持 iOS 和 macOS，会按运行平台自动使用 `203` 或 `205` 前缀。
</Note>

---

## 为什么会看到 1xxxxx 开头的错误码

**这是正常的，不是 bug。**

SMeeting 建在 SRTC 之上。当错误发生在底层音视频通道时，SMeeting 会把 SRTC 的原始错误码**原样透传**给你，而不是包装成自己的码 —— 这样你能直接定位到问题出在哪一层。

| 你看到的 | 含义 | 去哪儿查 |
| --- | --- | --- |
| `2xxx` | 会议服务端拒绝了请求（无权限、会议不存在……） | [服务端 API 错误码](/zh/meeting/server-api/error-codes) |
| `20Nxxx` | 会议层 SDK 的错误 | 对应平台的错误码页 |
| `1xxx` | 底层 SRTC **服务端**错误 | [SRTC 错误码规则](/zh/rtc/error-codes) |
| `10Nxxx` | 底层 SRTC **客户端**错误（如「未加入频道」） | [SRTC 错误码规则](/zh/rtc/error-codes) |

所以在 iOS 会议 SDK 里同时看到 `203002` 和 `103002` 并不矛盾：前者是会议层的第 002 号错误，后者是 SRTC 层的第 002 号错误，两者互不相干。

<Tip>
排查时先看前两位：`2` 开头找会议层的原因（权限、会议状态、成员角色），`1` 开头找音视频层的原因（Token、频道、网络）。
</Tip>

---

## 各平台完整错误码表

[Web](/zh/meeting/web/types) · [Android](/zh/meeting/android/error-codes) · [Windows](/zh/meeting/windows/error-codes) · [Swift](/zh/meeting/swift/error-codes) · [iOS](/zh/meeting/ios/error-codes)

<Warning>
不要按错误**文案**做分支判断 —— 文案会随版本调整，错误码不会。
</Warning>
