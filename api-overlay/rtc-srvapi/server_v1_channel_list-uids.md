---
examples:
  channel: fire
  offline: false
  with_audience: true
  page: 1
  per-page: 10
---

与「在线/离线成员列表」的筛选条件完全一致，但只返回 `uid` 字符串数组，不含成员详情。

适合只需要判断"谁在会中"的场景（如权限校验、名单比对），响应体积比完整列表小一个数量级。
