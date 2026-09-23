---
title: "资源与附件"
description: "预签名直传上传文件、资源列表与目录、会议背景与附件"
---

会议资源（附件、背景图、录制产物）走**预签名直传** —— SDK 不代理文件传输，
只负责给你换签名地址和登记元数据。

---

### 上传是三步

```typescript
import { PresignedPutObjectType, PresignedPutObjectResult } from 'smeeting';

// 1. 换预签名上传地址
const put: PresignedPutObjectResult = await meeting.presignedPutObject(
  PresignedPutObjectType.attach,   // 资源类别
  meetingId,
  'pdf'                            // 扩展名
);
// put.url  上传地址
// put.key  资源 key，第 3 步要用
// put.ext  扩展名

// 2. 自己 PUT 文件上去（SDK 不做这一步）
//    用 @ohos.net.http 或 request 上传到 put.url

// 3. 登记为会议资源
await meeting.resourcesCreate({
  meetingId: meetingId,
  resName: '需求文档.pdf',
  resType: 'pdf',
  resKey: put.key
});
```

<Warning>
**第 2 步是你自己的活。** SDK 只给地址，不传文件 —— 这样大文件不占 SDK 的内存，
也不受它的超时策略限制。

漏掉第 3 步的后果是：文件传上去了但会议里看不到（没登记）。
</Warning>

`PresignedPutObjectType`：

| 值 | 用途 |
| --- | --- |
| `attach` | 会议附件 |
| `background` | 会议背景图 |
| `user` | 用户资源 |

---

### 下载

```typescript
const url: string = await meeting.presignedGetObject(resourceId, resKey);
```

返回一个**带签名的临时地址**，用它去下载。两个参数都是可选的，按你手上有什么传。

<Note>
签名地址有有效期。不要缓存这个 URL 长期使用，需要时重新换一个。
</Note>

---

### 资源列表

```typescript
const page = await meeting.resourcesList({
  page: 1,
  perPage: 20,
  meetingId: meetingId,
  parentId: folderId,      // 按目录过滤
  resName: '需求',          // 按名字搜
  resType: 'pdf'
});
```

`ResourceInfo` 字段：

| 字段 | 说明 |
| --- | --- |
| `id` / `userId` / `meetingId` / `parentId` | 标识与归属 |
| `isFolder` | **是否是目录** |
| `resType` / `resKey` / `resName` / `resSize` | 资源本体 |
| `createdAt` / `updatedAt` | 时间 |

<Note>
资源是**树形**的 —— `isFolder` 为 `true` 的是目录，用 `parentId` 组织层级。
做文件浏览器 UI 时按 `parentId` 逐层查，不要一次拉全量。
</Note>

创建目录也是 `resourcesCreate`，只是不带 `resKey`。

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

### 一个最小的附件列表

```typescript
@State resources: ResourceInfo[] = [];

async loadResources(parentId?: string): Promise<void> {
  const page = await this.meeting.resourcesList({
    page: 1, perPage: 50, meetingId: this.meetingId, parentId: parentId
  });
  this.resources = page.list;         // 建新数组赋值
}

build() {
  ForEach(this.resources, (r: ResourceInfo) => {
    Row() {
      Text(r.resName)
      if (r.isFolder) {
        Button('打开').onClick(() => { this.loadResources(r.id); })
      } else {
        Button('下载').onClick(async () => {
          const url = await this.meeting.presignedGetObject(r.id, r.resKey);
          // 用 url 下载
        })
      }
    }
  }, (r: ResourceInfo) => r.id)
}
```

---

### 相关阅读

+ [会控接口](/zh/meeting/harmony/api-reference/admin-actions)
+ [录制与 MCU](/zh/meeting/harmony/advanced/recording) —— 录制产物也在资源里
+ [聊天与自定义消息](/zh/meeting/harmony/advanced/messaging) —— 发文件消息
