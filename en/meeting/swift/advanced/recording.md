---
title: "Recording and composite layout"
description: "Control server-side recording and stream mixing tasks from the SMeeting Swift SDK: build LayoutData and McuStartReq, start and stop tasks, change the composite layout during the meeting, query recording config and details, and handle recording state events. Read when adding a record button."
---

### Overview

Recording and compositing are both done on the server; the client only sends commands and shows the status. Task types are distinguished by `McuTaskType`:

| Type | Description |
| --- | --- |
| `.record` | Video recording, producing a recording file |
| `.mix` | Stream mixing, compositing multiple videos into one stream for viewers to pull |
| `.mixAndRecord` | Stream mixing plus recording |

You can also use `MeetingCreateReq.autoRecord` when creating the meeting so that recording starts automatically once the meeting begins.

---

### Build the layout and task parameters

`LayoutData`, `McuStartReq`, and the layout's `Watermark` / `Tag` / `Cell` / `DivList` can all be constructed directly; optional parameters have default values:

```swift
// Simplest: 4-grid, everything else uses defaults
let layout = LayoutData(layout: .grids4)

// With a watermark and name tags
let layout = LayoutData(
    layout: .grids4,
    pollingDur: 0,
    watermark: Watermark(type: 2, text: "Internal meeting"),
    tag: Tag(type: "LB")
)

// Pin specified members to specified grid cells
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

These types are also `Codable`; the mapping between fields and JSON keys is in the tables below—if your layout configuration is JSON delivered by your backend, you can also decode it directly with `JSONDecoder`.

---

### Layout fields

`LayoutData`:

| Field | JSON key | Type | Description |
| --- | --- | --- | --- |
| `layout` | `layout` | `LayoutType` | Layout type, such as `auto`, `grids_4`, `right_4`, `full` |
| `pollingDur` | `polling_dur` | `Int?` | Polling interval; `0` means no polling |
| `watermark` | `watermark` | `Watermark?` | Watermark configuration |
| `tag` | `tag` | `Tag?` | Video label (name tag) configuration |
| `divList` | `div_list` | `[DivList]?` | Logical blocks that pin specified members to specified grid cells |

`Watermark`:

| Field | JSON key | Type | Description |
| --- | --- | --- | --- |
| `type` | `type` | `Int` | `0` default, `1` none, `2` single row, `3` multiple rows |
| `text` | `text` | `String` | Specified content; empty means the meeting title is used automatically |
| `size` | `size` | `Int?` | Font size; `0` is the default |
| `color` | `color` | `String?` | Font color |
| `olColor` | `ol_color` | `String?` | Outline color |
| `olWidth` | `ol_width` | `Int?` | Outline width |

`Tag`:

| Field | JSON key | Type | Description |
| --- | --- | --- | --- |
| `type` | `type` | `String` | Combination of position letters: `L` left, `R` right, `T` top, `B` bottom |
| `text` | `text` | `String` | Specified content; empty means the in-meeting display name is used automatically |
| `size` | `size` | `Int?` | Font size |
| `color` | `color` | `String?` | Font color |
| `bgColor` | `bg_color` | `String?` | Background color |

`DivList` and `Cell`:

| Field | JSON key | Type | Description |
| --- | --- | --- | --- |
| `DivList.cell` | `cell` | `[Cell]` | Grid cells in this block |
| `DivList.uids` | `uids` | `[String]` | Members pinned in this block |
| `Cell.idx` | `idx` | `Int` | Grid cell index |
| `Cell.bindShare` | `bind_share` | `Bool` | Whether to bind the shared video first |
| `Cell.tag` | `tag` | `Tag` | Label configuration for this cell |

For all `LayoutType` enum values, see [Types](/en/meeting/swift/types#layouttype).

---

### Start and stop tasks

```swift
let req = McuStartReq(
    taskType: .mixAndRecord,
    title: "Weekly project sync",
    userName: "Alice",
    layoutData: LayoutData(layout: .grids4)
)

try await meeting.mcuStart(meetingId: meetingId, req: req)

// When stopping, specify which type of task to stop
try await meeting.mcuStop(meetingId: meetingId, taskType: .mixAndRecord)
```

`McuStartReq` fields:

| Field | JSON key | Type | Description |
| --- | --- | --- | --- |
| `taskType` | `task_type` | `McuTaskType` | Task type |
| `title` | `title` | `String` | Recording file title |
| `userName` | `user_name` | `String` | Operator name |
| `layoutData` | `layout_data` | `LayoutData` | Composite layout |

---

### Change the composite layout during the meeting

```swift
try await meeting.adminUpdateLayout(layout)
```

Requires the host / co-host role. After the change, the server recomposites with the new layout; clients currently pulling the composite video don't need to resubscribe.

---

### Query recording configuration and details

```swift
// Default recording configuration at the app level
let config = try await meeting.mcuRecordConfig()

// Recording details of a meeting
let detail = try await meeting.mcuRecordDetail(meetingId: meetingId)
```

Frequently used fields in `McuRecordDetail`:

| Field | Description |
| --- | --- |
| `taskStatus` | `McuTaskStatus`: `.running` in progress / `.normal` ended normally / `.exception` ended abnormally |
| `errDesc` | The reason when it ended abnormally |
| `vodKey` | Storage key of the recording file; use it with `presignedGetObject(resKey:)` to get a download URL |
| `vodSize` | File size |
| `mcuAt` / `mcuDur` | Recording start time and duration |

---

### Recording state events

When the task state changes, all members in the meeting receive:

```swift
func meeting(_ meeting: SMeetingEngine, roomMcuTask data: RoomMcuTaskEventData) {
    // data.taskType   task type
    // data.taskStatus task status
    // data.errDesc    error description
}
```

You can also read the meeting's current recording status directly from `RoomInfo.recordStatus`, which suits initializing a "recording" badge when entering the meeting.

---

### Watch the composite video

Once a stream mixing task is running, clients can pull a single composite video instead of subscribing to members' video one by one; see [Video rendering](/en/meeting/swift/advanced/video-rendering).

---

### Related pages

+ [Meeting materials](/en/meeting/swift/advanced/resources)
+ [Video rendering](/en/meeting/swift/advanced/video-rendering)
+ [Types](/en/meeting/swift/types)
