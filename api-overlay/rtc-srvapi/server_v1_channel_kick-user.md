---
examples:
  channel: fire
  uid: "1001"
---

把指定成员踢出频道。该成员的客户端会收到被踢事件，并触发 `user_leave` 回调（`reason` 标识为被踢）。

踢出是**一次性**操作，不会拉黑——被踢的 `uid` 重新获取 token 后仍可再次进入。需要禁止再入请在你自己的业务侧拦截 token 发放。
