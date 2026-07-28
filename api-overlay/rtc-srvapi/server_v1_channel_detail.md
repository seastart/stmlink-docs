---
examples:
  channel: fire
  app_id: 68b3ft51smhz0x5glscw9whm78bw57uu
  created_at: 1718250917
  updated_at: 1718250921
  link_id: 100000036
  max_user: 1024
  max_audio: 0
  max_peer: 32
  max_video: 16
---

查询单个频道的当前状态与扩展属性。**只能查到已打开的频道**——频道未打开或已销毁时返回空，需要历史信息请用「频道记录」。

`max_user` / `max_audio` / `max_peer` / `max_video` 是流媒体侧的容量参数，由应用配置决定，一般不需要业务侧关心。
