---
examples:
  channel: fire
  uid: "1001"
  app_id: 68b3ft51smhz0x5glscw9whm78bw57uu
  name: 张三
  device_type: 1
  device_id: aacc
  version: "1.0"
  props: {"avatar": "https://cdn.example.com/avatar/1001.png"}
  sid: p8ym6zzpzkzy0pedl97t
  is_audience: false
  join_at: 1717639307
  leave_at: 0
  updated_at: 1717639307
  link_id: 100000002
  upload_srv: sm0dx5
---

查询频道内单个成员的实时状态，包括他当前发布的流轨道（`stream_tracks`）。

同一个 `uid` 多端在线时，返回的是其中一个会话；需要区分具体设备请用「在线/离线成员列表」按 `sid` 取。
