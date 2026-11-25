---
title: "Meeting materials"
description: "Upload and download meeting materials with the SMeeting Swift SDK using presigned URLs: get an upload URL, PUT the file directly, keep the returned resource key, and exchange it for a signed download URL. Read when your meetings need attachments, background images, or avatars."
---

### Overview

Meeting materials (attachments, background images, avatars, and so on) use a "presigned direct upload" model:

```text
Ask the SDK for an upload URL  →  Your app PUTs the file directly to that URL  →  Keep the returned resource key
```

The file itself doesn't go through the SDK; the SDK only issues signed upload and download URLs.

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
| `.chat` | `chat` | Chat files (since 1.12.0); see [In-meeting messages](/en/meeting/swift/advanced/messaging#send-file-messages) for usage |

The returned `key` is the resource key of this file. After the upload succeeds, keep it or pass it on (for example, send it in a chat file message), and use it to get a download URL.

#### 2. Upload the file directly

```swift
var request = URLRequest(url: URL(string: url)!)
request.httpMethod = "PUT"
let (_, response) = try await URLSession.shared.upload(for: request, from: fileData)
```

---

### Download

First get a signed download URL, then download it yourself:

```swift
// By resource key (such as the key returned by presignedPutObject, or the key in a chat file message)
let url = try await meeting.presignedGetObject(resKey: key)
```

Pass `resKey`; the server doesn't support the `id` parameter yet. Signed URLs expire, so don't cache them for long; get a new one when you need it.

Recording files don't go through this flow: take the playback URL directly from `records[].addr` returned by `mcuRecordDetail`. See [Recording and composite layout](/en/meeting/swift/advanced/recording).

---

### Meeting background and attachments (since 1.13.0)

```swift
try await meeting.updateBgAndAttach(meetingId: meetingId, background: backgroundKey, attachments: [
    Attachment(name: "Agenda.pdf", key: attachKey),
])
let bgUrl = try await meeting.meetingBackgroundUrl(meetingId: meetingId)
```

`updateBgAndAttach` **replaces everything** rather than appending: the array you pass is the final attachment list, so to add one attachment, pass the existing ones along with it.

---

### Related pages

+ [Recording and composite layout](/en/meeting/swift/advanced/recording)
+ [API reference - Meeting management](/en/meeting/swift/api-reference/admin-actions)
