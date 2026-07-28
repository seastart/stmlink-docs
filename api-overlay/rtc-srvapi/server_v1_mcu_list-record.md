---
examples:
  begin_at: 1718194666
  end_at: 1718799878
  page: 1
  per-page: 10
  task_id: sxjgwy
  channel: fire
  title: 项目周会 2024-06-12
  op_uid: "1001"
  op_name: 张三
  room_no: "818595664"
---

分页查询录像列表。

+ `begin_at` / `end_at` 为秒级时间戳，按任务创建时间过滤，传 `0` 表示不限
+ `search` 支持按 `channel`、`task_status`、`room_no`、`op_name`、`title`、`tags` 检索
+ `sort` 支持 `created_at`，前缀 `-` 表示倒序（最新在前）

只有**已完成**的任务才有可播放的录像文件；`task_status` 用于区分进行中与已结束（见响应字段说明）。
