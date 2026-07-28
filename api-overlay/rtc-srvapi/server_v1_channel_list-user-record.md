---
examples:
  channel: fire
  uid: "1001"
  begin_at: 0
  end_at: 0
  sort: -join_at
  page: 1
  per-page: 10
  id: syd30d
  app_id: 68b3ft51smhz0x5glscw9whm78bw57uu
  sid: ff6u9joh5c1a0toa7dj1
  name: 张三
  is_audience: false
  device_type: 1
  device_id: aacc
  version: "1.0"
  props: {"avatar": "https://cdn.example.com/avatar/1001.png"}
  join_at: 1718194697
  leave_at: 1718194700
  leave_reason: 1
---

查询成员的进出频道记录，**单人多次进入会有多条记录**，用 `sid` 区分。这是做时长计费、参会审计的主要数据源。

+ `sort` 支持 `join_at` 与 `leave_at`，前缀 `-` 表示倒序
+ `leave_at` 为 `0` 表示该成员仍在会中
+ 单次参会时长 = `leave_at - join_at`（秒）
