# StmLink 开发者文档

本仓库为 [StmLink](https://www.stmlink.com) 旗下 SDK 产品的开发者文档，通过 [Mintlify](https://mintlify.com) 发布。

## 产品覆盖

| 目录 | 产品 | 说明 |
|------|------|------|
| `zh/rtc/` | SRTC 音视频 SDK | 音视频流媒体底层 SDK |
| `zh/meeting/` | SMeeting 会议 SDK | 基于 SRTC 的会议业务 SDK |

## 本地预览

```bash
npm install -g mintlify
mintlify dev
```

## 目录结构

```
stmlink-docs/
├── mint.json          # Mintlify 配置（导航、主题）
├── zh/                # 中文文档
│   ├── rtc/           # SRTC SDK
│   └── meeting/       # SMeeting SDK
└── en/                # 英文文档（待补充）
```

## 贡献指南

- 所有文档使用 Markdown 格式（`.md`）
- 图片存放在对应文档同目录的 `images/` 子目录
- 文件路径即页面 URL，命名使用小写英文 + 连字符
