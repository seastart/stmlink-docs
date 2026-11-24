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
| `delegates` | `MulticastDelegate<SMeetingDelegate>` | 事件回调容器 |
| `logLevel` | `LogLevel` | 读写 |
| `dispose()` | `void` | **必须调用**，摘掉全局单例上的监听 |

<Warning>
`dispose()` 漏掉会导致页面永不回收、摄像头指示灯一直亮 —— ArkTS 没有析构函数。
配套还要把注册过的 delegate `remove` 掉。
</Warning>

---

### 语言

```typescript
static setLanguage(lang?: string): void
static get language(): string
```

1.1.0 起提供。

| 成员 | 说明 |
| --- | --- |
| `SMeetingEngine.setLanguage(lang?)` | 设置 SDK 语言（BCP 47，如 `'zh-CN'`、`'en'`）；不传或传空恢复为跟随系统语言（缺省） |
| `SMeetingEngine.language` | 当前生效的语言：`setLanguage()` 的值 > 系统语言 > `'zh'` |

```typescript
SMeetingEngine.setLanguage('en');   // 建议在 login 之前设置
```

它直接透传给 SRTC 的 `SRTC.setLanguage` / `SRTC.language`，**会议层与 RTC 层共用这一个进程级设置**：
两层请求后端都带 `Accept-Language`，后端业务错误（码 ≥ 1000）的文案随之返回中文或英文，
音频路由显示名等也随之切换。SDK 自身的报错（`SMeetingError` / `SRTCError` 的 `detail`）一律英文，不受影响。

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

### 统计

```typescript
getStats(): Promise<RtcStatsSnapshot>
```

采集一次**本端** WebRTC 统计：实际编码分辨率与帧率、编码器降级原因、发送侧丢包、RTT 与可用上行带宽。做会中「网络状况」面板用它。

字段说明见 [SRTC 类型定义 · RtcStatsSnapshot](/zh/rtc/harmony/types#rtcstatssnapshot)。

与 `onQualityReport` 的分工：后者由 SFU 通过控制面下发，**只有 SeaStart 引擎有**，是服务端视角；`getStats()` 是本端观察，**两条引擎都有**，且能回答服务端答不了的问题（我实际编码出来是多少分辨率、编码器是被 CPU 还是被带宽限住了）。

<Warning>
**首次调用的码率恒为 0** —— 码率由两次采集的字节差算出。做面板要周期性调用，1 秒一次比较合适。
</Warning>

<Note>
与「会中查询」那一组不同，**不在会中时 `getStats()` 返回空快照而不抛错** —— 诊断能力不该让业务流程失败。
</Note>

---

### 会前网络检测

```typescript
networkCheck(options?: MeetingNetworkCheckOptions): Promise<MeetingNetworkCheckResult>
cancelNetworkCheck(): void
```

1.7.0 起提供，需搭配 SRTC 1.4.0。**入会前调用**，不需要入会，也不需要连 RTC。与 SRTC 的
[`networkCheck`](/zh/rtc/harmony/api-reference/SRTCEngine#networkcheckoptions) 同名同参：
`permission` → `connectivity` → `mtu` → `dns` → `server` 五项检测由 SRTC 完成、结果原样透传，
会议层只在 `server` 项的 `data` 里多一个子检查 `meeting_api`（会议接口是否可达），整体状态随之重算。

```typescript
import { SMeetingEngine, MeetingNetworkCheckResult, MeetingNetworkCheckItem, NetworkCheckStatus } from 'smeeting';

// 已登录：不用传 appId / serverUrl，SDK 从登录信息里取
const result: MeetingNetworkCheckResult = await meeting.networkCheck({
  onItem: (item: MeetingNetworkCheckItem) => {
    console.info(`${item.id} ${item.status} ${item.message}`);
  }
});
if (result.status === NetworkCheckStatus.fail) {
  // 各项的 message 是可直接展示给用户的中文说明
}
```

+ **参数来源**：`appId` / `serverUrl` 不传时从登录信息取（已启用 IM 用 IM token，在会中用频道 token，都没有时向会议后端申请一次 IM token，只取地址、不建连接）。**未登录时必须显式传**，`serverUrl` 是 SRTC 的 SDK 接口地址（RTC / IM token 里的 `client_api`，如 `https://host/sdkapi/`），不是会议接口地址。
+ **`meeting_api` 的判定**：已登录时调一次只读的会议接口，收到任何 HTTP 响应都算可达；网络错误或超时算不通，此时 `server` 记 `fail`、`reason` 为 `meeting_api_unreachable`。`server` 已因 SRTC 子检查失败时保留 SRTC 的 `reason`。未登录时不知道会议接口地址，`meeting_api` 记 `skipped`（`server_info_unavailable`）。
+ **耗时**：`meeting_api` 与 SRTC 检测并行，不额外拉长总耗时；单项超时默认 3000 毫秒（`timeoutMs` 可调，同时用作 `meeting_api` 的请求超时）。`onItem` 每完成一项回调一次，`server` 项等 `meeting_api` 合入后才回调。
+ **平台限制**同 SRTC：`mtu` 项在 HarmonyOS 固定为 `unsupported`（`df_not_supported`）。

| 错误码 | 场景 |
| --- | --- |
| `108005` | 已有检测在进行（同一实例同一时刻只允许一个） |
| `108026` | 被 `cancelNetworkCheck()` 取消 |
| `108031` | `appId` / `serverUrl` 非法，或已登录但解不出服务器地址 |
| `208001` | 未登录，且没传 `appId` / `serverUrl` |

前三个是透传的 SRTC 层码（`SRTCError`），与直接调 SRTC 时一致；只有未登录用会议层的 `SMeetingError.notLoggedIn`。

#### `MeetingNetworkCheckOptions`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `appId?` | `string` | 应用 ID。已登录可不传；未登录必须传 |
| `serverUrl?` | `string` | SRTC 的 SDK 接口地址（RTC / IM token 里的 `client_api`）。已登录可不传；未登录必须传 |
| `timeoutMs?` | `number` | 单项超时（毫秒），默认 `3000` |
| `onItem?` | `(item: MeetingNetworkCheckItem) => void` | 每完成一项回调一次 |

#### `MeetingNetworkCheckResult` / `MeetingNetworkCheckItem`

结构与 SRTC 的 `NetworkCheckResult` / `NetworkCheckItem` 一致：

| 接口 | 字段 |
| --- | --- |
| `MeetingNetworkCheckResult` | `status: NetworkCheckStatus`（`ok` / `warning` / `fail`，有 fail 即 fail）、`items`（固定 5 项、固定顺序）、`costMs` |
| `MeetingNetworkCheckItem` | `id: NetworkCheckItemId`、`status: NetworkCheckItemStatus`（`pass` / `warning` / `fail` / `skipped` / `unsupported`）、`reason`（原因码，通过时为空串）、`message`（中文说明）、`costMs`、`data` |

`server` 项的 `data` 有 `api`、`signal`、`media`（来自 SRTC）与 `meeting_api` 四个子检查，每个都是 `{ ok, status, reason, rttMs }`。
项 id、状态、SRTC 原因码这些枚举（`NetworkCheckItemId`、`NetworkCheckItemStatus`、`NetworkCheckStatus`、`NetworkCheckReason`）由 `smeeting` 直接转出；
会议层补充的原因码在 `MeetingNetworkCheckReason`：

| `reason` | 出现在 | 含义 |
| --- | --- | --- |
| `meeting_api_unreachable` | `server`、`data.meeting_api` | 会议接口连不上：网络不通或服务器地址不对 |
| `server_info_unavailable` | `data.meeting_api`（`skipped`） | 未登录，不知道会议接口地址 |

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
