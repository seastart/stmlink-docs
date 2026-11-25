---
title: "会议资料"
description: "SMeeting Swift SDK 的资源上传下载：换预签名上传地址后自己 PUT 文件、凭资源键换下载地址"
---

### 概述

会议资料（附件、背景图、头像等）走「预签名直传」模型：

```text
向 SDK 要一个上传地址  →  你的 App 直接 PUT 文件到该地址  →  保存返回的资源键 key
```

文件本身不经过 SDK，SDK 只负责发放带签名的上传 / 下载地址。

---

### 上传

#### 1. 获取上传地址

```swift
let (url, key, ext) = try await meeting.presignedPutObject(
    type: .attach,
    meetingId: meetingId,
    ext: "pdf"
)
```

`PresignedPutObjectType` 可选值：

| 枚举值 | 原始值 | 用途 |
| --- | --- | --- |
| `.attach` | `attach` | 会议附件 |
| `.background` | `background` | 会议背景图 |
| `.user` | `user` | 用户相关资源，例如头像 |
| `.chat` | `chat` | 聊天文件（1.12.0 起），用法见 [会中消息](/zh/meeting/swift/advanced/messaging#发送文件消息) |

返回的 `key` 就是这个文件的资源键，上传成功后保存或传给对方（例如随聊天文件消息发出），下载时用它换地址。

#### 2. 直传文件

```swift
var request = URLRequest(url: URL(string: url)!)
request.httpMethod = "PUT"
let (_, response) = try await URLSession.shared.upload(for: request, from: fileData)
```

---

### 下载

先换取一个带签名的下载地址，再自行下载：

```swift
// 按资源键（例如 presignedPutObject 返回的 key、聊天文件消息里的 key）
let url = try await meeting.presignedGetObject(resKey: key)
```

请传 `resKey`；`id` 参数目前服务端不支持。签名地址有有效期，不要长期缓存，需要时重新换。

录制文件不走这里：从 `mcuRecordDetail` 返回的 `records[].addr` 直接取播放地址，见 [录制与合屏布局](/zh/meeting/swift/advanced/recording)。

---

### 会议背景与附件（1.13.0 起）

```swift
try await meeting.updateBgAndAttach(meetingId: meetingId, background: backgroundKey, attachments: [
    Attachment(name: "议程.pdf", key: attachKey),
])
let bgUrl = try await meeting.meetingBackgroundUrl(meetingId: meetingId)
```

`updateBgAndAttach` 是**整体覆盖**，不是追加 —— 传进去的数组就是最终的附件列表，要加一个附件得把现有的一起传。

---

### 相关页面

+ [录制与合屏布局](/zh/meeting/swift/advanced/recording)
+ [接口文档 - 会议管理](/zh/meeting/swift/api-reference/admin-actions)
