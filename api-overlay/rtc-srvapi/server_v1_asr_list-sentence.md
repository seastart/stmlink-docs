---
examples:
  channel: fire
  page: 1
  per-page: 50
  uid: "1001"
  name: 张三
  sentence: 我们下周把这个方案定下来
  created_at: 1718250918
descriptions:
  sentence: 转写出的一句话文本
  created_at: 该句话的产生时间（秒级时间戳）
---

分页查询频道的语音转写结果，每条是一句话，带说话人与时间。

+ 按 `created_at` 顺序取即可还原完整对话，是生成会议纪要的数据源
+ 支持 `search` 按内容检索、`sort` 排序
+ 频道销毁后结果仍然保留，可事后查询

一句话的切分由识别引擎按语音停顿决定，不保证与"一个完整语义单元"对应——做纪要摘要时建议把连续多句合并后再交给模型处理。
