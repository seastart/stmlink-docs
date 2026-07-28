---
examples:
  channel: fire
  begin_at: 1718799878
  end_at: 0
  with_audience: false
  user_num: 60
  user_times: 1935
descriptions:
  user_num: 参会人数（按 uid 去重）
  user_times: 参会人次（同一人多次进入累计）
---

统计一个频道在指定时间范围内的历史参与规模。

+ `user_num` 按 `uid` 去重，回答"有多少人参加过"
+ `user_times` 不去重，回答"一共进出了多少次"
+ `end_at` 传 `0` 表示统计到当前时刻
