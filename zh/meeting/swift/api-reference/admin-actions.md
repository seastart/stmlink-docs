---
title: "会议管理"
description: "SMeeting Swift SDK 管理类接口参考：房间管控、成员管理、等候室、分组讨论、录制、资源与签到"
---

本页接口都挂在 `SMeeting` 上。

---

### 错误约定

本页接口的抛错遵循两条统一规则，后文不再逐条重复：

| 前置条件 | 不满足时抛出 |
| --- | --- |
| 需要已登录 | `SMeetingError.notLoggedIn` |
| 需要在会议中 | `SMeetingError.notInMeeting` |

服务端拒绝时统一抛出 `SMeetingError.apiError(code:message:)`，其中 `code` 与 `message` 来自服务端。带 `admin` 前缀的接口需要主持人（`.host`）或联席主持人（`.coHost`）身份，普通成员调用会以 `apiError` 的形式返回权限错误。

有返回值的接口在服务端返回数据无法解析时会抛出解码错误。

---

### 房间管控

以下接口都需要**在会议中**，返回值均为无。

#### `adminDestroyRoom()`

结束整场会议，所有成员被断开。

#### `adminUpdateRoomMicState(selfUnmuteMicDisabled:micDisabled:)`

设置房间全体静音。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `selfUnmuteMicDisabled` | `Bool` | 是 | 是否禁止成员自我解除静音 |
| `micDisabled` | `Bool?` | 否 | 是否全体静音；不传表示不改动这一项 |

#### `adminUpdateRoomCameraState(selfUnmuteCameraDisabled:cameraDisabled:)`

设置房间全体禁画。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `selfUnmuteCameraDisabled` | `Bool` | 是 | 是否禁止成员自我解除禁画 |
| `cameraDisabled` | `Bool?` | 否 | 是否全体禁画；不传表示不改动这一项 |

#### `adminUpdateRoomShareState(shareDisabled:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `shareDisabled` | `Bool` | 是 | 是否禁止成员共享 |

#### `adminUpdateRoomChatDisabled(_:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `chatDisabled` | `Bool` | 是 | 是否全体禁言 |

#### `adminUpdateRoomScreenshotDisabled(_:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `screenshotDisabled` | `Bool` | 是 | 是否禁止截屏 |

#### `adminUpdateRoomWatermarkDisabled(_:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `watermarkDisabled` | `Bool` | 是 | 是否关闭水印 |

#### `adminUpdateRoomLocked(_:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `locked` | `Bool` | 是 | 是否锁定会议（锁定后新成员无法进入） |

#### `adminUpdateEnterBeforeHostDisabled(_:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `disabled` | `Bool` | 是 | 是否禁止在主持人到场前入会 |

#### `adminStopRoomShare()`

强制结束当前正在进行的共享。

---

### 成员管理

以下接口都需要**在会议中**，返回值均为无。

#### `adminUpdateUserName(targetId:nickname:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `targetId` | `String` | 是 | 目标成员 ID |
| `nickname` | `String` | 是 | 新的会中昵称 |

#### `adminUpdateUserRole(targetId:role:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `targetId` | `String` | 是 | 目标成员 ID |
| `role` | `Role` | 是 | `.member` / `.coHost` |

#### `adminUpdateUserChatDisabled(targetId:chatDisabled:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `targetId` | `String` | 是 | 目标成员 ID |
| `chatDisabled` | `Bool` | 是 | 是否禁言该成员 |

#### `adminMoveHost(targetId:)`

转移主持人身份。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `targetId` | `String` | 是 | 新主持人 ID |

#### `adminRequestUserOpenMic(targetId:)` / `adminRequestUserOpenCamera(targetId:)`

邀请成员开麦 / 开摄像头。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `targetId` | `String` | 是 | 目标成员 ID |

#### `adminCloseUserMic(targetId:)` / `adminCloseUserCamera(targetId:)`

直接关闭成员的麦克风 / 摄像头。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `targetId` | `String` | 是 | 目标成员 ID |

#### `adminKickUserOut(targetId:joinDisabled:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `targetId` | `String` | 是 | 目标成员 ID |
| `joinDisabled` | `Bool` | 否 | 是否同时禁止再次入会，默认 `false` |

#### `adminConfirmHandup(targetId:approve:code:)`

审批举手申请。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `targetId` | `String` | 是 | 举手的成员 ID |
| `approve` | `Bool` | 是 | 是否同意 |
| `code` | `HandupType` | 是 | 举手类型 |

---

### 参会人员与设备

#### `adminUpdateConferee(meetingId:conferee:)`

修改受邀人员名单。**需要已登录。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `meetingId` | `String` | 是 | 会议 ID |
| `conferee` | `[String]` | 是 | 受邀成员 ID 列表 |

**返回值：** 无

#### `adminCallUsers(conferee:)`

会中呼叫人员。**需要在会议中。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `conferee` | `[String]` | 是 | 被呼叫成员 ID 列表 |

**返回值：** 无

#### `meetNotEnter()`

查询尚未进入会议的受邀人员。**需要在会议中。**

**返回值：** `[NoEnterUserInfo]`

#### `adminMeetRemind(uids:useSms:)`

提醒入会。**需要在会议中。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uids` | `[String]` | 是 | 被提醒成员 ID 列表 |
| `useSms` | `Bool` | 否 | 是否同时发送短信，默认 `false` |

**返回值：** 无

#### `adminListOnlineMember(page:perPage:)`

在线人员列表。**需要在会议中。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `page` | `Int` | 否 | 页码，默认 `1` |
| `perPage` | `Int` | 否 | 每页条数，默认 `20` |

**返回值：** `PageResult<OnlineMemberInfo>`

#### `agentList(type:name:page:perPage:)`

可邀请的设备列表。**需要已登录。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `type` | `[AgentType]` | 是 | 设备类型过滤 |
| `name` | `String` | 否 | 名称过滤，默认空字符串（不过滤） |
| `page` | `Int` | 否 | 页码，默认 `1` |
| `perPage` | `Int` | 否 | 每页条数，默认 `20` |

**返回值：** `PageResult<AgentInfo>`

#### `adminInviteAgent(agents:no:)`

邀请设备入会。**需要已登录。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `agents` | `[(type: AgentType, contact: String)]` | 是 | 设备类型与联系地址 |
| `no` | `String` | 是 | 会议房间号 |

**返回值：** 无

---

### 等候室

#### `adminUpdateWaitingRoomDisabled(_:)`

**需要在会议中。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `disabled` | `Bool` | 是 | `true` 关闭等候室，`false` 启用 |

**返回值：** 无

#### `adminWaitingRoomUsers()`

**需要在会议中。**

**返回值：** `[WaitingRoomUserInfo]`

#### `adminMoveInWaitingRoom(userId:nickname:)`

把会议中的成员移回等候室。**需要在会议中。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `userId` | `String` | 是 | 成员 ID |
| `nickname` | `String` | 是 | 成员昵称 |

**返回值：** 无

#### `adminMoveOutWaitingRoom(userId:nickname:)`

把等候室成员放进会议。两个参数都不传表示全部放行。**需要在会议中。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `userId` | `String?` | 否 | 成员 ID |
| `nickname` | `String?` | 否 | 成员昵称 |

**返回值：** 无

#### `exitWaitingRoom(meetingId:roomNo:)`

成员主动离开等候室，两个参数二选一。**需要已登录。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `meetingId` | `String?` | 否 | 会议 ID |
| `roomNo` | `String?` | 否 | 房间号 |

**返回值：** 无

---

### 分组讨论

以下接口除 `userHelpSubMeeting()` 外都**只要求已登录**。

#### `adminCreateSubMeeting(mainMeetingId:titles:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `mainMeetingId` | `String` | 是 | 主会议 ID |
| `titles` | `[String]` | 是 | 要创建的小组名称列表 |

**返回值：** 无

#### `adminSubMeetingList(mainMeetingId:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `mainMeetingId` | `String` | 是 | 主会议 ID |

**返回值：** `[SubMeetingInfo]`

#### `adminUpdateSubMeetingTitle(id:title:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `id` | `String` | 是 | 小组 ID |
| `title` | `String` | 是 | 新名称 |

**返回值：** 无

#### `adminUpdateSubMeetingUsers(id:users:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `id` | `String` | 是 | 小组 ID |
| `users` | `[(uid: String, name: String)]` | 是 | 分配到这个小组的成员 |

**返回值：** 无

#### `adminDeleteSubMeeting(ids:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `ids` | `[String]` | 是 | 小组 ID 列表 |

**返回值：** 无

#### `adminStartSubMeeting(ids:)` / `adminStopSubMeeting(ids:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `ids` | `[String]` | 是 | 小组 ID 列表 |

**返回值：** 无

#### `adminMoveSubMeetingUser(fromId:toId:userId:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `fromId` | `String` | 是 | 源小组 ID |
| `toId` | `String` | 是 | 目标小组 ID |
| `userId` | `String` | 是 | 成员 ID |

**返回值：** 无

#### `userHelpSubMeeting()`

小组内成员向主会场求助。**需要在会议中。**

**返回值：** 无

---

### 布局与录制

#### `adminUpdateLayout(_:)`

修改合成会议的布局。**需要在会议中。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `layoutData` | `LayoutData` | 是 | 布局配置，字段见 [录制与合屏布局](/zh/meeting/swift/advanced/recording) |

**返回值：** 无

#### `mcuStart(meetingId:req:)`

开始录制 / 合流任务。**需要已登录。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `meetingId` | `String` | 是 | 会议 ID |
| `req` | `McuStartReq` | 是 | 任务参数 |

**返回值：** 无

#### `mcuStop(meetingId:taskType:)`

**需要已登录。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `meetingId` | `String` | 是 | 会议 ID |
| `taskType` | `McuTaskType` | 是 | 要停止的任务类型 |

**返回值：** 无

#### `mcuRecordConfig()`

**需要已登录。**

**返回值：** `McuRecordConfig`

#### `mcuRecordDetail(meetingId:)`

**需要已登录。**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `meetingId` | `String` | 是 | 会议 ID |

**返回值：** `McuRecordDetail`

---

### 资源

以下接口都**只要求已登录**。

#### `presignedPutObject(type:meetingId:ext:)`

获取上传地址。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `type` | `PresignedPutObjectType` | 是 | `.attach` / `.background` / `.user` |
| `meetingId` | `String` | 是 | 会议 ID |
| `ext` | `String` | 是 | 文件扩展名，例如 `pdf` |

**返回值：** `(url: String, key: String, ext: String)`

#### `presignedGetObject(id:resKey:)`

获取下载地址，两个参数二选一。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `id` | `String?` | 否 | 资源 ID |
| `resKey` | `String?` | 否 | 资源键 |

**返回值：** `String`（带签名的下载地址）

#### `resourcesList(req:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `req` | `ResourceListReq` | 是 | 查询条件 |

**返回值：** `PageResult<ResourceInfo>`

#### `resourcesCreate(req:)`

登记一条资源。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `req` | `ResourceCreateReq` | 是 | 资源信息 |

**返回值：** 无

---

### 签到

以下接口都**需要在会议中**，作用对象是当前会议。

#### `signInCreate(dur:desc:)`

发起一轮签到。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `dur` | `Int` | 是 | 签到持续时长，单位**分钟** |
| `desc` | `String` | 是 | 签到说明 |

**返回值：** 无

#### `signInFinish()`

提前结束当前这一轮签到。

**返回值：** 无

#### `signInSign()`

成员签到。

**返回值：** 无

#### `signInList()`

**返回值：** `(list: [SignInfo]?, now: Int)`，`now` 是服务端当前时间

#### `signInCount(epoch:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `epoch` | `Int` | 是 | 签到轮次 |

**返回值：** `Int`（已签到人数）

#### `signInDetail(epoch:nickname:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `epoch` | `Int` | 是 | 签到轮次 |
| `nickname` | `String?` | 否 | 按昵称过滤 |

**返回值：** `[SignDetailInfo]`

---

### 相关页面

+ [主持人管控](/zh/meeting/swift/advanced/host-controls)
+ [等候室](/zh/meeting/swift/advanced/waiting-room)
+ [分组讨论](/zh/meeting/swift/advanced/sub-meetings)
+ [录制与合屏布局](/zh/meeting/swift/advanced/recording)
+ [会议资料](/zh/meeting/swift/advanced/resources)
+ [签到与点名](/zh/meeting/swift/advanced/sign-in)
