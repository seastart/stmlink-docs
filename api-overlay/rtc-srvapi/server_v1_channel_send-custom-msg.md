---
examples:
  channel: fire
  action: chat
  content: i love srtc
  uid: "1001"
  important: false
---

通过信令通道向频道内广播一条自定义消息，客户端 SDK 会以事件形式收到。适合做聊天、举手、投票这类轻量业务信令，**不适合传大数据或高频消息**。

+ `action` 是你自定义的消息类型，客户端按它分发处理
+ `uid` 留空表示广播给频道内所有人；填写则只发给该成员
+ `important: true` 的消息会做可靠投递（代价是延迟略高），普通消息尽力而为
