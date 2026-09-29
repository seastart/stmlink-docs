---
title: "Meeting materials"
description: "Upload and download meeting materials with the SMeeting Swift SDK using presigned URLs: get an upload URL, PUT the file directly, register it as a resource, get a signed download URL, and query the resource list and folders. Read when your meetings need attachments, background images, or avatars."
---

### Overview

Meeting materials (attachments, background images, avatars, and so on) use a "presigned direct upload" model:

```text
Ask the SDK for an upload URL  →  Your app PUTs the file directly to that URL  →  Register the resKey as a resource
```

The file itself doesn't go through the SDK; the SDK only issues URLs and maintains resource records.

---

### Upload

#### 1. Get an upload URL

```swift
let (url, key, ext) = try await meeting.presignedPutObject(
    type: .attach,
    meetingId: meetingId,
    ext: "pdf"
)
```

`PresignedPutObjectType` values:

| Enum value | Raw value | Purpose |
| --- | --- | --- |
| `.attach` | `attach` | Meeting attachments |
| `.background` | `background` | Meeting background images |
| `.user` | `user` | User-related resources, such as avatars |

The returned `key` is the resource key of this file; you use it for both registering and downloading later.

#### 2. Upload the file directly

```swift
var request = URLRequest(url: URL(string: url)!)
request.httpMethod = "PUT"
let (_, response) = try await URLSession.shared.upload(for: request, from: fileData)
```

#### 3. Register the resource

```swift
var req = ResourceCreateReq(resName: "Meeting materials.pdf", resType: "pdf")
req.meetingId = meetingId
req.resKey = key
try await meeting.resourcesCreate(req: req)
```

`ResourceCreateReq` also has a `parentId` field for putting the resource into a folder.

---

### Download

First get a signed download URL, then download it yourself:

```swift
// By resource ID
let url = try await meeting.presignedGetObject(id: resource.id)

// Or by resource key (such as the vodKey of a recording file)
let url = try await meeting.presignedGetObject(resKey: detail.vodKey)
```

Provide one of the two parameters.

---

### Query the resource list

```swift
var req = ResourceListReq(page: 1, perPage: 20)
req.meetingId = meetingId
req.resType = "pdf"

let page = try await meeting.resourcesList(req: req)
for item in page.data {
    print(item.resName, item.resSize)
}
```

Filters supported by `ResourceListReq`: `parentId` (folder), `meetingId`, `resName` (fuzzy name match), `resType`.

In the returned `ResourceInfo`, `isFolder` set to `true` means this is a folder node; you can use its `id` as the `parentId` for querying the next level.

---

### Related pages

+ [Recording and composite layout](/en/meeting/swift/advanced/recording)
+ [API reference - Meeting management](/en/meeting/swift/api-reference/admin-actions)
