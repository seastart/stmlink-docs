---
examples:
  action: meeting_invite
  content: {"meeting_no": "818595664", "title": "项目周会"}
  uid: "1001"
  name: 张三
  ruids: ["1002", "1003"]
  important: true
---

通过 IM 通道给指定用户或设备推消息，接收方不需要在任何频道里。

### 收件人怎么指定

+ `ruids` —— 按**用户**发，该用户所有在线设备都会收到
+ `rsids` —— 按**会话**发，只发给特定设备
+ **`rsids` 有值时 `ruids` 会被忽略**，两者不叠加

### 其它字段

+ `action` 是你自定义的消息类型，客户端按它分发处理（如 `meeting_invite`、`call_ring`）
+ `content` 是任意 JSON，结构由你定
+ `uid` / `name` 是发送者信息，用于客户端展示"谁发来的"；服务端下发的系统消息可以留空
+ `important: true` 会在接收方断线重连后重发，确保收到——邀请、呼叫这类不能丢的消息应该开启；普通状态同步不必

消息不做持久化存储：`important` 只保证重连期间的补发，不是离线消息队列。接收方长时间离线的消息需要你自己的业务侧兜底。
