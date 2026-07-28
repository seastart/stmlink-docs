---
examples:
  channel: fire
  uid: "1001"
  name: 张三
  props: {"avatar": "https://cdn.example.com/avatar/1001.png"}
  is_audience: false
  net: 内网
  sg: ""
  sid: co63jg6g54hu3b0xhtie
  token: wvYKytpMTsR2OK82ghVj1ZFAVCEtfMug...（实际长度约 300 字符，此处截断）
descriptions:
  sid: 本次会话 ID，由服务端生成。用于后续按会话维度查询与对账
  token: 入会凭证，下发给客户端调用 SDK 的 joinChannel
---

这是接入 RTC 的**第一个接口**。典型时序：

1. 你的业务后端确认用户有权进入某个频道
2. 调用本接口拿到 `token` 与 `sid`
3. 把 `token` 下发给你的客户端，客户端用它调 SDK 的 `joinChannel`

`token` 有效期有限且与 `channel` + `uid` 绑定，**不要缓存复用**，每次入会都重新获取。频道无需预先创建，第一个人成功加入时自动打开。

### 注意

+ `net` 的取值是**中文**的线路名（如 `内网` / `外网`），取值范围由你们的部署网络配置决定，不确定时留空由服务端选择
+ 同一个 `uid` 重复获取 token 会得到新的 `sid`；若该 `uid` 已在会中，新会话会把旧会话顶下线
+ `is_audience: true` 的用户只收流、不广播，也不出现在默认的成员列表里（需要 `with_audience` 才能查到）
