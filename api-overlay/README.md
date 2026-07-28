# 服务端 API 散文层（overlay）

`zh/rtc/server-api/` 下的接口页面（`common` / `channel` / `mcu` / `agent` / `im` / `white-board` / `asr`）
**由脚本生成，不要手工编辑** —— 改了会在下次同步时被覆盖。

要改内容，改这两处之一：

| 改什么 | 改哪里 |
| --- | --- |
| 接口路径、参数、类型、必填、校验规则、响应结构 | **rtc-backend 的源码**（这些一律从代码提取，不手写） |
| 业务说明、调用时序、注意事项、示例值、字段补充说明 | **本目录下的 overlay 文件** |

这么分的原因很简单：结构会随代码变，手写必然漂移；而"这个接口什么时候用、参数填什么"代码里没有，只能人写。

## 目录结构

```
api-overlay/rtc-srvapi/
├── _global.md                          # 通用说明（鉴权与签名），单独成一页
├── server_v1_channel_grant.md          # 一个接口一个文件
└── server_v1_channel_set-callback.md
```

文件名由接口路径转写而来：去掉首尾 `/`，把 `/` 换成 `_`。

```
/server/v1/channel/grant  →  server_v1_channel_grant.md
```

没有 overlay 文件的接口照常生成页面，只是没有业务说明。同步脚本会打印待补清单。

## 文件格式

frontmatter（可选）+ 正文（markdown 散文）：

```markdown
---
title: "今日频道统计"
examples:
  channel: fire
  uid: "1001"
  props: {"avatar": "https://cdn.example.com/avatar/1001.png"}
  begin_at: 1718194666
  is_audience: false
descriptions:
  sid: 本次会话 ID，由服务端生成
---

这是接入 RTC 的**第一个接口**。典型时序：

1. 你的业务后端确认用户有权进入某个频道
2. 调用本接口拿到 `token` 与 `sid`
3. 把 `token` 下发给客户端，客户端用它调 SDK 的 `joinChannel`

### 注意

+ `net` 的取值是**中文**的线路名（如 `内网` / `外网`）
```

**frontmatter 字段**

+ `title` —— 覆盖接口标题。用于代码注释不适合当对外文案、或路由上方没有注释的情况
+ `examples` —— 字段名 → 示例值。请求和响应的字段共用一张表，同名即命中
+ `descriptions` —— 字段名 → 说明。**仅用于代码里拿不到注释的字段**（例如响应用 `gin.H` 手工组装的）；
  能在代码里加注释的一律加在代码里

**正文**会插在接口标题之后、参数表之前 —— 开发者和 AI 都先读"这是干什么的"。

## 写 example 的重点

不必给每个字段都写。真正需要的是这三类，其余靠字段说明就够：

1. **单位有歧义**：`begin_at: 起始时间` 看不出是秒还是毫秒，`1718194666` 一眼就知道是秒
2. **值域不明**：`net: 线路` 的实际取值是中文的 `内网` / `外网`，谁都猜不到
3. **自由结构**：`props: 用户扩展属性` 完全不告诉你怎么填

第 2 类如果是数字枚举，更好的做法是**在代码的字段注释里写值域**（如
`// 水印类型 1无,2单排,3多排`），生成器会自动识别成 `enum`，不需要写在这里。

## 同步

```bash
python3 scripts/sync-server-api.py    # rtc-backend 默认在 ../rtc-backend
RTC_BACKEND=/path/to/rtc-backend python3 scripts/sync-server-api.py
mint broken-links                      # 提交前校验
```

脚本会重新生成页面、清理已下线接口的孤儿页、并更新 `docs.json` 导航。

## 两个坑

**MDX 转义**：页面由 Mintlify 以 MDX 解析，表格单元格里的 `< > { } |` 会被误当语法。
生成器已对代码注释自动转义（曾有个字段注释写着「排序规则按HTML中`<td>`标签的顺序」，
导致整站构建失败）。但 overlay 正文是**完整 markdown、不做转义** —— 正文里要写这类字符请自己用反引号包起来。

**别在 router.go 的路由行上方写内部备注**：那里的注释会被直接当成对外文档的接口名。
写 TODO 或临时说明会直接漏进对外文档。分组性注释（如 `// 统计相关`）同理会被误当接口名，
这种情况用 overlay 的 `title` 覆盖。
