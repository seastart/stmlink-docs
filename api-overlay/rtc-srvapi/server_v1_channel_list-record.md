---
examples:
  channel: fire
  begin_at: 0
  end_at: 0
  sort: -open_at
  page: 1
  per-page: 10
  id: snp3rp
  app_id: 68b3ft51smhz0x5glscw9whm78bw57uu
  props: {"watermark_disabled": true}
  open_at: 1718194666
  destroy_at: 1718194705
  destroy_reason: 1
---

查询频道的**历史**开启记录。同一个频道名多次开启会有多条记录，每条对应一个完整的生命周期（`open_at` → `destroy_at`）。

+ `begin_at` / `end_at` 为秒级时间戳，传 `0` 表示不限
+ `sort` 支持 `open_at` 与 `destroy_at`，前缀 `-` 表示倒序（如 `-open_at` 为最新在前）
+ `destroy_at` 为 `0` 表示该频道仍在进行中
