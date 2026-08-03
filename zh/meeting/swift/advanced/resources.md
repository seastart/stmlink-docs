---
title: "会议资料"
description: "SMeeting Swift SDK 的资源上传下载：预签名地址获取、资源登记与资源列表查询"
---

### 概述

会议资料（附件、背景图、头像等）走「预签名直传」模型：

```text
向 SDK 要一个上传地址  →  你的 App 直接 PUT 文件到该地址  →  把 resKey 登记为一条资源
```

文件本身不经过 SDK，SDK 只负责发放地址和维护资源记录。

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

返回的 `key` 就是这个文件的资源键，后面登记和下载都用它。

#### 2. 直传文件

```swift
var request = URLRequest(url: URL(string: url)!)
request.httpMethod = "PUT"
let (_, response) = try await URLSession.shared.upload(for: request, from: fileData)
```

#### 3. 登记资源

```swift
var req = ResourceCreateReq(resName: "会议材料.pdf", resType: "pdf")
req.meetingId = meetingId
req.resKey = key
try await meeting.resourcesCreate(req: req)
```

`ResourceCreateReq` 还有一个 `parentId` 字段，用于把资源放进某个目录。

---

### 下载

先换取一个带签名的下载地址，再自行下载：

```swift
// 按资源 ID
let url = try await meeting.presignedGetObject(id: resource.id)

// 或按资源键（例如录制文件的 vodKey）
let url = try await meeting.presignedGetObject(resKey: detail.vodKey)
```

两个参数二选一。

---

### 查询资源列表

```swift
var req = ResourceListReq(page: 1, perPage: 20)
req.meetingId = meetingId
req.resType = "pdf"

let page = try await meeting.resourcesList(req: req)
for item in page.data {
    print(item.resName, item.resSize)
}
```

`ResourceListReq` 支持的过滤条件：`parentId`（目录）、`meetingId`、`resName`（名称模糊匹配）、`resType`。

返回的 `ResourceInfo` 中 `isFolder` 为 `true` 表示这是一个目录节点，可以用它的 `id` 作为下一级查询的 `parentId`。

---

### 相关页面

+ [录制与合屏布局](/zh/meeting/swift/advanced/recording)
+ [接口文档 - 会议管理](/zh/meeting/swift/api-reference/admin-actions)
