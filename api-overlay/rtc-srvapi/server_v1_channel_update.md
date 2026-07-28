---
examples:
  channel: fire
  props: {"watermark_disabled": true}
---

更新频道的扩展属性 `props`。这是**整体替换**语义，不是字段级合并——传入的 `props` 会覆盖原有的整个对象，需要保留的字段请一并传入。

频道必须已打开，否则更新无效。变更会通过信令同步给会中所有客户端。
