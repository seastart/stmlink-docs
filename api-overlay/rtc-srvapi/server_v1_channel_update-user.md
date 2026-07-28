---
examples:
  channel: fire
  uid: "1001"
  name: 张三
  is_audience: false
  props: {"avatar": "https://cdn.example.com/avatar/1001.png"}
---

更新会中成员的昵称、扩展属性或观众身份。变更会同步给会中其他成员。

`props` 与频道的 `props` 一样是**整体替换**语义。

把已在会中的成员改成 `is_audience: true` 会让他退化为只收流的观众，其已发布的流轨道会被停止。
