---
title: "资源与附件"
description: "预签名直传上传与下载文件（换地址 + 自己 PUT）、会议背景与附件"
---

会议资源（附件、背景图、聊天文件）走**预签名直传** —— SDK 不代理文件传输，
只负责给你换带签名的上传 / 下载地址。

---

### 上传是两步

```typescript
import { PresignedPutObjectType, PresignedPutObjectResult } from 'smeeting';

// 1. 换预签名上传地址
const put: PresignedPutObjectResult = await meeting.presignedPutObject(
  PresignedPutObjectType.attach,   // 资源类别
  meetingId,
  'pdf'                            // 扩展名
);
// put.url  上传地址
// put.key  资源 key，上传成功后保存 / 传递它，下载时用
// put.ext  扩展名

// 2. 自己 PUT 文件上去（SDK 不做这一步）
//    用 @ohos.net.http 或 request 上传到 put.url
```

<Warning>
**第 2 步是你自己的活。** SDK 只给地址，不传文件 —— 这样大文件不占 SDK 的内存，
也不受它的超时策略限制。

上传成功后没有「登记」这一步：要让别人看到这个文件，把 `put.key` 交给对应的业务接口，
如会议附件用下文的 `updateBgAndAttach`，聊天文件随消息发出。
</Warning>

`PresignedPutObjectType`：

| 值 | 用途 |
| --- | --- |
| `attach` | 会议附件 |
| `background` | 会议背景图 |
| `user` | 用户资源 |
| `chat` | 会中聊天文件（1.8.0 起），用法见[聊天与自定义消息](/zh/meeting/harmony/advanced/messaging#发文件消息) |

---

### 下载

```typescript
const url: string = await meeting.presignedGetObject(undefined, resKey);
```

返回一个**带签名的临时地址**，用它去下载。请传 `resKey`（第二个参数）；第一个参数 `id` 目前服务端不支持，传 `undefined` 即可。

<Note>
签名地址有有效期。不要缓存这个 URL 长期使用，需要时重新换一个。
</Note>

---

### 会议背景与附件

```typescript
await meeting.updateBgAndAttach(meetingId, backgroundKey, [
  { name: '议程.pdf', key: 'xxx' },
  { name: '参考资料.docx', key: 'yyy' }
]);

const bgUrl: string = await meeting.meetingBackgroundUrl(meetingId);
```

`Attachment` 只有两个字段：`name`、`key`。

<Warning>
`updateBgAndAttach` 是**整体覆盖**，不是追加 —— 传进去的数组就是最终的附件列表。
要加一个附件，得把现有的一起传。
</Warning>

创建会议时也可以直接带上：`MeetingCreateReq.background` 与
`MeetingCreateReq.attachments`。

---

### 相关阅读

+ [会控接口](/zh/meeting/harmony/api-reference/admin-actions)
+ [录制与 MCU](/zh/meeting/harmony/advanced/recording) —— 录制文件不走这里，从录制详情取播放地址
+ [聊天与自定义消息](/zh/meeting/harmony/advanced/messaging) —— 发文件消息
