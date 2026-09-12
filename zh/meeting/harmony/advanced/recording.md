---
title: "录制与 MCU"
description: "启动录制与混流、布局配置、任务状态监听与异常处理"
---

录制建在 **MCU 合流**之上 —— 服务端把多路画面合成一路，既可以下发给客户端订阅，
也可以录成文件。

---

### 三种任务类型

`McuTaskType` 决定服务端做什么：

| 值 | 说明 |
| --- | --- |
| `record = 1` | 纯录制 |
| `mix = 2` | 纯混流（合成一路给客户端订阅） |
| `mixAndRecord = 3` | 混流 + 录制 |

---

### 启动与停止

```typescript
import { McuTaskType, LayoutType, McuStartReq } from 'smeeting';

const req: McuStartReq = {
  taskType: McuTaskType.mixAndRecord as number,
  title: '产品评审录制',
  userName: '张三',
  layoutData: { layout: LayoutType.grids9 }
};

await meeting.mcuStart(meetingId, req);
await meeting.mcuStop(meetingId, McuTaskType.mixAndRecord);
```

<Note>
`mcuStop` 要传**同一个 `taskType`** —— 服务端按类型区分任务。
启的是 `mixAndRecord` 就不能用 `record` 去停。
</Note>

需要会议开始时自动录制的，在创建会议时设 `MeetingCreateReq.autoRecord = true`。

---

### 布局

```typescript
const layoutData: LayoutData = {
  layout: LayoutType.grids9,
  pollingDur: 30,                     // 轮播间隔（秒）
  watermark: { type: 1, text: '内部资料', size: 24, color: '#80FFFFFF' },
  divList: [/* 分区配置 */]
};
await meeting.adminUpdateLayout(layoutData);
```

`LayoutType` 有 20 种预置：

| 类别 | 值 |
| --- | --- |
| 自动 / 全屏 | `auto`、`full` |
| 等分宫格 | `grids_2` ~ `grids_25`（2/3/4/5/6/8/9/10/12/16/20/25） |
| 主次布局 | `right_4`、`top_4`、`br_7`、`tl_7`、`tb_8` |

`Cell.bindShare = true` 可以把某个格位绑定到共享画面。

<Note>
`adminUpdateLayout` 影响的是**服务端合流的布局**，不是客户端本地的排版。
本地宫格怎么摆是你自己的 UI 事。
</Note>

---

### 监听任务状态

```typescript
onRoomMcuTask: (m, data) => {
  // data.taskType: McuTaskType
  // data.taskStatus: McuTaskStatus
  // data.errDesc: string
  switch (data.taskStatus) {
    case McuTaskStatus.running:
      this.recordingBadge = true;
      break;
    case McuTaskStatus.normal:
      this.recordingBadge = false;
      break;
    case McuTaskStatus.exception:
      this.recordingBadge = false;
      toast(`录制异常：${data.errDesc}`);
      break;
  }
}
```

<Warning>
**`exception` 必须提示给用户。**

录制出问题时用户一定要知道 —— 否则他们会以为整场都录上了，
会后才发现没有。`errDesc` 里有原因，直接展示。
</Warning>

---

### 查询

```typescript
const config: McuRecordConfig = await meeting.mcuRecordConfig();
const detail: McuRecordDetail = await meeting.mcuRecordDetail(meetingId);
```

| 接口 | 用途 |
| --- | --- |
| `mcuRecordConfig()` | 应用级录制配置（默认布局、水印类型等） |
| `mcuRecordDetail(meetingId)` | 某场会议的录制明细（15 个字段） |

`RoomInfo.recordStatus` 也能读到当前录制状态，进会时用它初始化 UI。

---

### 客户端订阅合流画面

大型会议不要 N 路各自订阅，改订 MCU 合成的那一路：

```typescript
const mcu = await meeting.subscribeRemoteVideoMcu(hostUid);
// 渲染 meeting.mcuTrack
await meeting.unsubscribeRemoteVideoMcu();
```

客户端解码开销不随人数线性上升 —— 这是人多时的主要方案。

渲染就是把 `meeting.mcuTrack` 交给 `SRTCVideoView`：

```typescript
if (this.meeting.mcuTrack !== undefined) {
  SRTCVideoView({
    track: this.meeting.mcuTrack,
    trackKey: 'mcu'
  }).width('100%').height('100%')
}
```

<Note>
订了 MCU 就不要再逐路订阅同一批人的画面 —— 那是双份带宽。
两种模式应当是**互斥**的，切换时先退掉另一种。
</Note>

---

### 录制文件在哪

录制产物走**资源**体系，用 `resourcesList` 查、`presignedGetObject` 换下载地址。
见[资源与附件](/zh/meeting/harmony/advanced/resources)。

---

### 相关阅读

+ [会控接口](/zh/meeting/harmony/api-reference/admin-actions)
+ [资源与附件](/zh/meeting/harmony/advanced/resources)
+ [视频渲染](/zh/meeting/harmony/advanced/video-rendering)
