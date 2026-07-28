---
examples:
  with_detail: true
  page: 1
  per-page: 10
  app_id: 68b3ft51smhz0x5glscw9whm78bw57uu
  channel: fire
  created_at: 1718250917
  updated_at: 1718250921
  link_id: 100000036
  max_user: 1024
  max_audio: 0
  max_peer: 32
  max_video: 16
---

分页列出当前**已打开**的频道。频道在第一个用户加入时自动打开，最后一人离开 2 小时后自动销毁，因此这里只反映当下的活跃情况；要查历史请用「频道记录」。

`with_detail` 为 `false` 时只返回频道名等基础字段，可显著降低响应体积；需要 `props`、流媒体参数等再置为 `true`。
