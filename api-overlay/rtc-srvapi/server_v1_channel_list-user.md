---
examples:
  channel: fire
  offline: false
  with_audience: true
  page: 1
  per-page: 10
  app_id: 68b3ft51smhz0x5glscw9whm78bw57uu
  uid: "1001"
  name: 张三
  device_type: 1
  device_id: aacc
  version: "1.0"
  props: {"avatar": "https://cdn.example.com/avatar/1001.png"}
  sid: bjcjlbz18tfhbscaz225
  is_audience: false
  join_at: 1718250918
  leave_at: 0
  updated_at: 1718250918
  link_id: 100000037
  upload_srv: sm0dx5
---

分页列出频道成员。同一个 `uid` 从多个端进入会有多条记录，用 `sid` 区分不同会话。

+ `offline: false`（默认）返回**当前在线**的成员；`offline: true` 返回**已离开**的成员
+ `is_audience: true` 的隐身观众默认**不返回**，需要显式传 `with_audience: true`
+ `stream_tracks` 是该成员当前发布的流轨道；未开麦、未开摄像头时为空
