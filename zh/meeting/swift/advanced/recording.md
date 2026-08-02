---
title: "录制与合屏布局"
description: "SMeeting Swift SDK 的服务端录制、合流任务控制、布局配置与录制状态事件"
---

### 概述

录制与合屏都由服务端完成，客户端只负责下发指令和展示状态。任务类型由 `McuTaskType` 区分：

| 类型 | 说明 |
| --- | --- |
| `.record` | 录像，产出录制文件 |
| `.mix` | 合流，把多路画面合成一路供拉流观看 |
| `.mixAndRecord` | 合流并录制 |

创建会议时也可以通过 `MeetingCreateReq.autoRecord` 让会议开始后自动录制。

---

### 构造布局与任务参数

`LayoutData`、`McuStartReq` 以及布局里的 `Watermark` / `Tag` / `Cell` / `DivList` 都可以直接构造，可选参数有默认值：

```swift
// 最简：四宫格，其余走默认
let layout = LayoutData(layout: .grids4)

// 带水印和名条
let layout = LayoutData(
    layout: .grids4,
    pollingDur: 0,
    watermark: Watermark(type: 2, text: "内部会议"),
    tag: Tag(type: "LB")
)

// 把指定成员钉到指定宫格
let layout = LayoutData(
    layout: .grids4,
    divList: [
        DivList(
            cell: [Cell(idx: 0, bindShare: true, tag: Tag(type: "LB"))],
            uids: ["u1001"]
        )
    ]
)
```

这些类型同时是 `Codable` 的，字段与 JSON 键的对应关系见下方表格 —— 如果你的布局配置是后端下发的 JSON，也可以直接 `JSONDecoder` 解码。

---

### 布局字段

`LayoutData`：

| 字段 | JSON 键 | 类型 | 说明 |
| --- | --- | --- | --- |
| `layout` | `layout` | `LayoutType` | 布局类型，例如 `auto`、`grids_4`、`right_4`、`full` |
| `pollingDur` | `polling_dur` | `Int?` | 轮询间隔，`0` 表示不轮询 |
| `watermark` | `watermark` | `Watermark?` | 水印配置 |
| `tag` | `tag` | `Tag?` | 画面标签（名条）配置 |
| `divList` | `div_list` | `[DivList]?` | 逻辑块，把指定成员钉到指定宫格 |

`Watermark`：

| 字段 | JSON 键 | 类型 | 说明 |
| --- | --- | --- | --- |
| `type` | `type` | `Int` | `0` 默认、`1` 无、`2` 单排、`3` 多排 |
| `text` | `text` | `String` | 指定内容，空表示自动取会议标题 |
| `size` | `size` | `Int?` | 字号，`0` 为默认 |
| `color` | `color` | `String?` | 字体颜色 |
| `olColor` | `ol_color` | `String?` | 轮廓颜色 |
| `olWidth` | `ol_width` | `Int?` | 轮廓线宽 |

`Tag`：

| 字段 | JSON 键 | 类型 | 说明 |
| --- | --- | --- | --- |
| `type` | `type` | `String` | 位置字母组合：`L` 左、`R` 右、`T` 上、`B` 下 |
| `text` | `text` | `String` | 指定内容，空表示自动取会中昵称 |
| `size` | `size` | `Int?` | 字号 |
| `color` | `color` | `String?` | 字体颜色 |
| `bgColor` | `bg_color` | `String?` | 背景颜色 |

`DivList` 与 `Cell`：

| 字段 | JSON 键 | 类型 | 说明 |
| --- | --- | --- | --- |
| `DivList.cell` | `cell` | `[Cell]` | 这一块包含的宫格 |
| `DivList.uids` | `uids` | `[String]` | 钉在这一块里的成员 |
| `Cell.idx` | `idx` | `Int` | 宫格序号 |
| `Cell.bindShare` | `bind_share` | `Bool` | 是否优先绑定共享画面 |
| `Cell.tag` | `tag` | `Tag` | 这一格的标签配置 |

完整 `LayoutType` 枚举值见 [类型定义](/zh/meeting/swift/types#layouttype)。

---

### 开始与停止任务

```swift
let req = McuStartReq(
    taskType: .mixAndRecord,
    title: "项目周会",
    userName: "张三",
    layoutData: LayoutData(layout: .grids4)
)

try await meeting.mcuStart(meetingId: meetingId, req: req)

// 停止时要指明停哪一类任务
try await meeting.mcuStop(meetingId: meetingId, taskType: .mixAndRecord)
```

`McuStartReq` 字段：

| 字段 | JSON 键 | 类型 | 说明 |
| --- | --- | --- | --- |
| `taskType` | `task_type` | `McuTaskType` | 任务类型 |
| `title` | `title` | `String` | 录制文件标题 |
| `userName` | `user_name` | `String` | 操作人名称 |
| `layoutData` | `layout_data` | `LayoutData` | 合成布局 |

---

### 会中调整合成布局

```swift
try await meeting.adminUpdateLayout(layout)
```

需要主持人 / 联席主持人身份。调整后服务端会按新布局重新合成，客户端如果正在拉合成画面不需要重新订阅。

---

### 查询录制配置与详情

```swift
// 应用维度的默认录制配置
let config = try await meeting.mcuRecordConfig()

// 某场会议的录制详情
let detail = try await meeting.mcuRecordDetail(meetingId: meetingId)
```

`McuRecordDetail` 中比较常用的字段：

| 字段 | 说明 |
| --- | --- |
| `taskStatus` | `McuTaskStatus`：`.running` 进行中 / `.normal` 正常结束 / `.exception` 异常结束 |
| `errDesc` | 异常结束时的原因 |
| `vodKey` | 录制文件的存储键，配合 `presignedGetObject(resKey:)` 换取下载地址 |
| `vodSize` | 文件大小 |
| `mcuAt` / `mcuDur` | 录制开始时间与时长 |

---

### 录制状态事件

任务状态变化时，会中所有成员都会收到：

```swift
func meeting(_ meeting: SMeeting, roomMcuTask data: RoomMcuTaskEventData) {
    // data.taskType   任务类型
    // data.taskStatus 任务状态
    // data.errDesc    异常描述
}
```

会议当前的录制状态也可以直接读 `RoomInfo.recordStatus`，适合在进入会议时初始化「正在录制」角标。

---

### 观看合成画面

开启了合流任务后，客户端可以只拉一路合成画面而不是逐个订阅成员视频，见 [视频渲染](/zh/meeting/swift/advanced/video-rendering)。

---

### 相关页面

+ [会议资料](/zh/meeting/swift/advanced/resources)
+ [视频渲染](/zh/meeting/swift/advanced/video-rendering)
+ [类型定义](/zh/meeting/swift/types)
