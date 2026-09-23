---
title: "RollCallManager"
description: "会中点名管理器：发起与结束点名、主持人呼叫和确认、成员应答、详情查询与导出"
---

`RollCallManager` 通过 `MeetingEngine.rollCallManager` 获取，所有操作都绑定 Engine 当前的单场会议。

## 使用说明

+ 该属性是稳定门面，可以在会前保存；未入会时所有异步方法返回 `MeetingErrorCode.SESSION_NOT_ACTIVE`。
+ 列表和详情中的 `id` 含义不同：列表 `RollCallBean.id` 是点名活动 ID，详情用户 `RollCallUserBean.id` 是后续呼叫与应答使用的点名用户 ID。

+ `allMember` 为 `false` 时必须提供 `members`；成员项包含 UID 与昵称。
+ 结果回调保持网络来源线程，更新 UI 前应切换到主线程。

## 接口方法

### listRollCall(page, perPage, callback)

```kotlin
fun listRollCall(
    page: Int,
    perPage: Int,
    callback: MeetingValueResultCallback<MeetingPage<RollCallBean>>
)
```

方法说明：分页查询当前会议的点名活动。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `page` | 页码，从 `1` 开始。 |
| `perPage` | 每页最大条目数。 |
| `callback` | 成功返回点名活动分页结果的回调。 |

返回值说明：无（异步结果见回调）。

### startRollCall(method, allMember, members, callback)

```kotlin
fun startRollCall(
    method: RollCallMethod,
    allMember: Boolean,
    members: List<MemberRequestBean>?,
    callback: MeetingValueResultCallback<String>
)
```

方法说明：创建并开始一轮点名。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `method` | 自动或手动点名方式。 |
| `allMember` | `true` 对全体成员点名；`false` 只点名 `members`。 |
| `members` | 指定成员列表；`allMember=false` 时必填。 |
| `callback` | 成功返回新建点名活动 ID 的结果回调。 |

返回值说明：无（异步结果见回调）。

### stopRollCall(rollCallId, callback)

```kotlin
fun stopRollCall(rollCallId: String, callback: MeetingResultCallback)
```

方法说明：结束指定点名活动。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `rollCallId` | 点名活动 ID。 |
| `callback` | 结束结果回调。 |

返回值说明：无（异步结果见回调）。

### rollCallNamed(rollCallUserId, callback)

```kotlin
fun rollCallNamed(
    rollCallUserId: String,
    callback: MeetingResultCallback
)
```

方法说明：主持人呼叫点名详情中的指定用户。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `rollCallUserId` | `RollCallUserBean.id`，不是会议成员 UID。 |
| `callback` | 呼叫结果回调。 |

返回值说明：无（异步结果见回调）。

### adminRollCallAnswer(rollCallUserId, clear, callback)

```kotlin
fun adminRollCallAnswer(
    rollCallUserId: String,
    clear: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：主持人确认或清除指定用户的点名应答记录。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `rollCallUserId` | `RollCallUserBean.id`。 |
| `clear` | `true` 清除已有应答记录；`false` 确认应答。 |
| `callback` | 操作结果回调。 |

返回值说明：无（异步结果见回调）。

### detailRollCall(rollCallId, callback)

```kotlin
fun detailRollCall(
    rollCallId: String,
    callback: MeetingValueResultCallback<RollCallDetailBean>
)
```

方法说明：查询指定点名活动详情和成员应答状态。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `rollCallId` | 点名活动 ID。 |
| `callback` | 成功返回 `RollCallDetailBean` 的结果回调。 |

返回值说明：无（异步结果见回调）。

### exportRollCallDetail(rollCallId, callback)

```kotlin
fun exportRollCallDetail(
    rollCallId: String,
    callback: MeetingValueResultCallback<String>
)
```

方法说明：请求导出指定点名活动详情。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `rollCallId` | 点名活动 ID。 |
| `callback` | 成功返回服务端导出结果字符串的回调。 |

返回值说明：无（异步结果见回调）。

### userRollCallAnswer(rollCallUserId, callback)

```kotlin
fun userRollCallAnswer(
    rollCallUserId: String,
    callback: MeetingResultCallback
)
```

方法说明：当前用户回应点名。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `rollCallUserId` | 当前用户在点名详情中的 `RollCallUserBean.id`。 |
| `callback` | 应答结果回调。 |

返回值说明：无（异步结果见回调）。
