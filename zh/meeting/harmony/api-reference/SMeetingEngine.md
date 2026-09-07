---
title: "SMeetingEngine"
description: "SMeeting HarmonyOS SDK 主入口：登录、会议管理、入会离会与查询接口"
---

会议 SDK 的唯一入口。会控、媒体、等候室、子会议、录制、签到等方法也都挂在它上面，
按主题拆到了几个页面：

+ 本页：**登录、会议 CRUD、入会离会、查询**
+ [媒体控制](/zh/meeting/harmony/api-reference/media-control)：开麦、摄像头、共享、订阅
+ [会控接口](/zh/meeting/harmony/api-reference/admin-actions)：`admin*`、等候室、子会议、录制、签到
+ [设备与路由](/zh/meeting/harmony/api-reference/devices)：设备枚举与音频路由

---

### 构造与释放

```typescript
constructor(logLevel?: LogLevel)
```

```typescript
import { SMeetingEngine } from 'smeeting';
import { LogLevel } from 'srtc';

const meeting: SMeetingEngine = new SMeetingEngine(LogLevel.info);
```

| 成员 | 类型 | 说明 |
| --- | --- | --- |
| `SMeetingEngine.version` | `string`（静态只读） | SDK 版本，等同 `SMEETING_VERSION` |
| `srtc` | `SRTCEngine`（只读） | 底层 RTC 引擎，可直接使用 |
| `delegates` | `MulticastDelegate<SMeetingDelegate>` | 事件回调容器 |
| `logLevel` | `LogLevel` | 读写 |
| `dispose()` | `void` | **必须调用**，摘掉全局单例上的监听 |

<Warning>
`dispose()` 漏掉会导致页面永不回收、摄像头指示灯一直亮 —— ArkTS 没有析构函数。
配套还要把注册过的 delegate `remove` 掉。
</Warning>

---

### 登录

```typescript
login(token: string): Promise<void>
logout(): Promise<void>
```

Token 由**业务后端**签发，SDK 不负责发号。

**抛出**：`tokenInvalid`（`208005`）/ `tokenExpired`（`208002`）

未登录就调其它接口会抛 `notLoggedIn`（`208001`）。

---

### 会议管理

这一组**不要求在会中**，登录后即可调用。

#### `createRoom(req)`

```typescript
createRoom(req: MeetingCreateReq): Promise<string[]>
```

创建会议。返回 `[roomNo, meetingId]` —— **两个元素的数组**。

```typescript
const result: string[] = await meeting.createRoom({ title: '产品评审' });
const roomNo: string = result[0];
const meetingId: string = result[1];
```

`MeetingCreateReq` 的常用字段（完整清单见[类型定义](/zh/meeting/harmony/types)）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `title` | `string` | **必填**，会议标题 |
| `roomNo?` | `string` | 指定房间号 |
| `content?` | `string` | 会议说明 |
| `attendType?` | `AttendType` | 入会限制：无限制 / 密码 / 邀请 / 密码+邀请 |
| `conferee?` | `string[]` | 参会人员用户 ID |
| `coHosts?` | `string[]` | 联席主持人 |
| `maximum?` | `number` | 最大参会人数 |
| `endType?` | `EndType` | 结束方式 |

预约会议就是在 `req` 里带上 `planTime` / `planDur`。

#### `updateRoom` / `cancelRoom`

```typescript
updateRoom(meetingId: string, req: MeetingCreateReq): Promise<void>
cancelRoom(meetingId: string): Promise<void>
```

#### `detailRoom(meetingId?, roomNo?)`

```typescript
detailRoom(meetingId?: string, roomNo?: string): Promise<MeetingInfo>
```

查会议详情。两个参数二选一。

---

### 会议列表

```typescript
attendeeRoom(page?: PageParam): Promise<PageResult<MeetingInfo>>
attendedRoom(page?: PageParam): Promise<PageResult<MeetingInfo>>
roomParticipant(meetingId: string, page?: number, perPage?: number): Promise<PageResult<ParticipantInfo>>
```

| 方法 | 返回 |
| --- | --- |
| `attendeeRoom` | 我的**即将开始**的会议 |
| `attendedRoom` | 我**参加过**的历史会议 |
| `roomParticipant` | 某个会议的参会人列表 |

分页参数用 `PageParam`（`defaultPageParam()` 给一份默认值）。

---

### 入会与离会

#### `enterRoom(req)`

```typescript
enterRoom(req: MeetingEnterReq): Promise<void>
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `nickname` | `string` | **必填**，会中昵称 |
| `meetingId?` | `string` | 与 `roomNo` **二选一** |
| `roomNo?` | `string` | 与 `meetingId` 二选一 |
| `password?` | `string` | 会议有密码时必填 |
| `avatar?` | `string` | 会中头像 |
| `extendInfo?` | `string` | 扩展字段 |

**抛出**：`alreadyInMeeting`（`208006`）/ `apiError`

<Warning>
**入会失败有两条通路，必须都处理。**

`enterRoom()` 抛错只覆盖"请求阶段就失败"。请求成功但被服务端拒绝
（会议已锁定、被移入等候室等）走的是事件：

```typescript
onRoomJoinFailed: (meeting, data) => {
  console.error(`入会失败(${data.failedType}): ${data.errDesc}`);
}
```

只写 `try/catch` 会漏掉后一种。
</Warning>

#### `exitRoom()`

```typescript
exitRoom(): Promise<void>
```

离会。建议先关掉媒体再离会：

```typescript
await meeting.closeCamera();
await meeting.closeMic();
await meeting.stopShare();
await meeting.exitRoom();
```

---

### 会中查询

这一组要求**在会中**，否则抛 `notInMeeting`（`208003`）。

```typescript
getRoomInfo(): RoomInfo | undefined
getWhiteBoard(): string | undefined
getUserInfo(uid: string): MeetingUserInfo
getUsersInfo(): Map<string, MeetingUserInfo>
getUsersInfoList(): MeetingUserInfo[]
```

| 方法 | 说明 |
| --- | --- |
| `getRoomInfo()` | 当前房间状态（含所有会控开关，30 个字段） |
| `getWhiteBoard()` | 白板地址 |
| `getUserInfo(uid)` | 单个成员 |
| `getUsersInfo()` | 全部成员的 Map |
| `getUsersInfoList()` | 全部成员的数组，**做列表 UI 用这个** |

<Note>
`getRoomInfo()` 返回的 `RoomInfo` 是判断"按钮能不能点"的依据 ——
里面有 `micDisabled` / `selfUnmuteMicDisabled` / `locked` / `shareDisabled` 等全部开关。

进会后先读一次它初始化 UI，之后靠 `onRoom*Change` 事件增量更新。
</Note>

---

### 聊天与自定义消息

```typescript
sendRoomChatMessage(msg: string, type?: ChatMsgType, targetId?: string): Promise<void>
```

| 参数 | 说明 |
| --- | --- |
| `msg` | 消息内容（字符串；结构化内容自己序列化） |
| `type` | `ChatMsgType`，默认 `text` |
| `targetId` | 传了就是**私聊**，不传是群发 |

收消息走 `onChatMessage` / `onCustomMessage` 事件。

---

### 其它

```typescript
meetNotEnter(): Promise<NoEnterUserInfo[]>
```

查询"应到未到"的成员，用于会议开始后提醒。

---

### 相关阅读

+ [媒体控制](/zh/meeting/harmony/api-reference/media-control)
+ [会控接口](/zh/meeting/harmony/api-reference/admin-actions)
+ [事件参考](/zh/meeting/harmony/events)
+ [错误码](/zh/meeting/harmony/error-codes)
