---
title: "会控接口"
description: "SMeetingEngine 的 admin* 会控方法、等候室、子会议、录制、签到与资源接口"
---

本页的方法**都要求主持人或联席主持人身份**（`Role.host` / `Role.coHost`），
否则抛 `unauthorized`（`208004`）。

<Note>
**按角色隐藏 / 禁用按钮，不要靠捕获 `unauthorized`。**
后者的体验是"点了才知道不能点"。角色变化通过 `onUserRoleChange` 事件下发，
当前角色从 `getUserInfo(myUid).role` 读。
</Note>

---

## 房间级开关

```typescript
adminUpdateRoomMicState(selfUnmuteMicDisabled: boolean, micDisabled?: boolean): Promise<void>
adminUpdateRoomCameraState(selfUnmuteCameraDisabled: boolean, cameraDisabled?: boolean): Promise<void>
adminUpdateRoomShareState(shareDisabled: boolean): Promise<void>
adminUpdateRoomChatDisabled(chatDisabled: boolean): Promise<void>
adminUpdateRoomScreenshotDisabled(screenshotDisabled: boolean): Promise<void>
adminUpdateRoomWatermarkDisabled(watermarkDisabled: boolean): Promise<void>
adminUpdateRoomLocked(locked: boolean): Promise<void>
adminUpdateEnterBeforeHostDisabled(disabled: boolean): Promise<void>
```

<Warning>
**麦克风和摄像头这两个方法的第一个参数是 `selfUnmute*Disabled`，不是开关本身。**

```typescript
// 全体静音，且成员不可自行解除
await meeting.adminUpdateRoomMicState(true, true);

// 全体静音，但成员可以自己开麦
await meeting.adminUpdateRoomMicState(false, true);

// 解除全体静音
await meeting.adminUpdateRoomMicState(false, false);
```

参数顺序容易记反 —— 第一个是"能不能自己解除"，第二个才是"是否静音"。
</Warning>

其余几个都是单个布尔开关，语义直白。变化通过对应的 `onRoom*Change` 事件广播给所有人。

---

## 成员管理

```typescript
adminUpdateUserName(targetId: string, nickname: string): Promise<void>
adminUpdateUserRole(targetId: string, role: Role): Promise<void>
adminUpdateUserChatDisabled(targetId: string, chatDisabled: boolean): Promise<void>
adminMoveHost(targetId: string): Promise<void>
adminKickUserOut(targetId: string, joinDisabled?: boolean): Promise<void>
```

| 方法 | 说明 |
| --- | --- |
| `adminUpdateUserName` | 改某成员的会中昵称 |
| `adminUpdateUserRole` | 设为联席主持人 / 降为普通成员 |
| `adminUpdateUserChatDisabled` | 单独禁言某人 |
| `adminMoveHost` | **移交主持人**，调用后自己变成普通成员 |
| `adminKickUserOut` | 移出会议；`joinDisabled=true` 时禁止其再次加入 |

---

## 对成员的媒体操作

```typescript
adminRequestUserOpenMic(targetId: string): Promise<void>
adminCloseUserMic(targetId: string): Promise<void>
adminRequestUserOpenCamera(targetId: string): Promise<void>
adminCloseUserCamera(targetId: string): Promise<void>
adminStopRoomShare(): Promise<void>
```

<Note>
**"请求开"与"直接关"是不对称的**，这是有意的：

+ `adminRequestUserOpenMic` —— 只是**请求**。对端收到 `onAdminRequestOpenMic`，
  应当弹窗征求同意，SDK 不会自动开。隐私边界在这儿。
+ `adminCloseUserMic` —— 直接关，不需要对方同意。

`adminStopRoomShare()` 强制停止**当前正在进行的**共享（不指定 uid）。
</Note>

---

## 举手

```typescript
adminConfirmHandup(targetId: string, approve: boolean, code: HandupType): Promise<void>
```

处理成员的举手请求。`HandupType` 区分举手用途：`mic` / `camera` / `chat` / `share`。

成员举手走 `onUserHandup`（带 `UserHandupStep`：`request` / `cancel` /
`confirmOpen` / `rejectOpen`），处理结果广播 `onAdminConfirmHandup`。

详见[举手](/zh/meeting/harmony/advanced/handup)。

---

## 布局与 MCU

```typescript
adminUpdateLayout(layoutData: LayoutData): Promise<void>
mcuStart(meetingId: string, req: McuStartReq): Promise<void>
mcuStop(meetingId: string, taskType: McuTaskType): Promise<void>
mcuRecordConfig(): Promise<McuRecordConfig>
mcuRecordDetail(meetingId: string): Promise<McuRecordDetail>
```

`LayoutType` 提供 20 种预置布局：`auto` / `full` / `grids_2` … `grids_25` /
`right_4` / `top_4` / `br_7` / `tl_7` / `tb_8`。

`McuTaskType`：`record`（纯录制）/ `mix`（纯混流）/ `mixAndRecord`（两者）。

任务状态变化通过 `onRoomMcuTask` 上报，`taskStatus` 为 `exception` 时
`errDesc` 有原因 —— 这个要提示给用户，录制出问题他们需要知道。

详见[录制](/zh/meeting/harmony/advanced/recording)。

---

## 邀请与提醒

```typescript
adminCallUsers(conferee: string[]): Promise<void>
adminMeetRemind(uids: string[], useSms?: boolean): Promise<void>
adminUpdateConferee(meetingId: string, conferee: string[]): Promise<void>
adminInviteAgent(agents: AgentInvite[], no: string): Promise<void>
agentList(type: AgentType[], name?: string, page?: number, perPage?: number): Promise<PageResult<AgentInfo>>
adminListOnlineMember(page?: number, perPage?: number): Promise<PageResult<OnlineMemberInfo>>
```

| 方法 | 说明 |
| --- | --- |
| `adminCallUsers` | 呼叫成员（对端收到 `onImCallCalling`） |
| `adminMeetRemind` | 会议提醒；`useSms=true` 走短信 |
| `adminUpdateConferee` | 修改参会人名单 |
| `adminInviteAgent` | 邀请第三方接入设备 |
| `agentList` | 查询可用的接入设备 |
| `adminListOnlineMember` | 在线成员分页列表 |

`AgentType` 覆盖 `sip` / `h323` / `gb28181` / `rtsp` / `rtmp` / `filePlay` /
`tencentMeet` / `ai`。

---

## 等候室

```typescript
adminUpdateWaitingRoomDisabled(disabled: boolean): Promise<void>
adminWaitingRoomUsers(): Promise<WaitingRoomUserInfo[]>
adminMoveInWaitingRoom(userId: string, nickname: string): Promise<void>
adminMoveOutWaitingRoom(userId?: string, nickname?: string): Promise<void>
exitWaitingRoom(meetingId?: string, roomNo?: string): Promise<void>
```

`adminMoveOutWaitingRoom` 不传参数表示**放行全部**。

`exitWaitingRoom` 是**成员**调用的（不需要主持人权限）—— 在等候室里主动退出。

详见[等候室](/zh/meeting/harmony/advanced/waiting-room)。

---

## 子会议

```typescript
adminCreateSubMeeting(mainMeetingId: string, titles: string[]): Promise<void>
adminUpdateSubMeetingTitle(id: string, title: string): Promise<void>
adminUpdateSubMeetingUsers(id: string, users: SubMeetingUser[]): Promise<void>
adminDeleteSubMeeting(ids: string[]): Promise<void>
adminSubMeetingList(mainMeetingId: string): Promise<SubMeetingInfo[]>
adminStartSubMeeting(ids: string[]): Promise<void>
adminStopSubMeeting(ids: string[]): Promise<void>
adminMoveSubMeetingUser(fromId: string, toId: string, userId: string): Promise<void>
userHelpSubMeeting(): Promise<void>
```

`adminCreateSubMeeting` 一次传多个标题就一次建多个组。

`userHelpSubMeeting()` 是**成员**调用的 —— 在子会议里向主持人求助，
主持人收到 `onImUserHelpSubMeeting`。

详见[子会议](/zh/meeting/harmony/advanced/sub-meetings)。

---

## 签到

```typescript
signInCreate(dur: number, desc: string): Promise<void>
signInFinish(): Promise<void>
signInSign(): Promise<void>
signInList(): Promise<SignInListResult>
signInCount(epoch: number): Promise<number>
signInDetail(epoch: number, nickname?: string): Promise<SignDetailInfo[]>
```

| 方法 | 谁调 | 说明 |
| --- | --- | --- |
| `signInCreate(dur, desc)` | 主持人 | 发起签到，`dur` 是持续秒数 |
| `signInFinish()` | 主持人 | 提前结束 |
| `signInSign()` | **成员** | 签到 |
| `signInList` / `signInCount` / `signInDetail` | 主持人 | 查询结果 |

`epoch` 是某一轮签到的标识，从 `onSignInActivity` 事件里拿。

详见[签到](/zh/meeting/harmony/advanced/sign-in)。

---

## 资源与附件

```typescript
resourcesList(req: ResourceListReq): Promise<PageResult<ResourceInfo>>
resourcesCreate(req: ResourceCreateReq): Promise<void>
presignedPutObject(type: PresignedPutObjectType, meetingId: string, ext: string): Promise<PresignedPutObjectResult>
presignedGetObject(id?: string, resKey?: string): Promise<string>
updateBgAndAttach(meetingId: string, background: string, attachments: Attachment[]): Promise<void>
meetingBackgroundUrl(meetingId: string): Promise<string>
```

上传是**预签名直传**的两步式：

```typescript
// 1. 拿预签名上传地址
const put = await meeting.presignedPutObject(
  PresignedPutObjectType.attach, meetingId, 'pdf');

// 2. 用返回的地址自己 PUT 文件（SDK 不代理文件传输）

// 3. 登记为会议资源
await meeting.resourcesCreate(req);
```

`PresignedPutObjectType`：`attach`（附件）/ `background`（会议背景）/ `user`（用户资源）。

下载同理，用 `presignedGetObject` 换一个带签名的临时地址。

详见[资源与附件](/zh/meeting/harmony/advanced/resources)。

---

### 相关阅读

+ [SMeetingEngine](/zh/meeting/harmony/api-reference/SMeetingEngine)
+ [媒体控制接口](/zh/meeting/harmony/api-reference/media-control)
+ [会控](/zh/meeting/harmony/advanced/host-controls)
+ [事件参考](/zh/meeting/harmony/events)
