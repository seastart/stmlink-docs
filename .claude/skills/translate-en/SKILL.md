---
name: translate-en
description: "stmlink-docs 英文版（en/）的翻译规程：新译页面、按中文 diff 增量同步英文、补服务端 API 翻译记忆表（i18n/server-api/*.en.json）、审校英文页并登记。触发场景：翻译 / 译成英文 / 同步英文文档、`i18n.py status` 报缺译或过期、`sync-server-api.py` 提示翻译记忆缺失、SDK 发版后同步该平台英文页、用户审校完要标记已审校、批量翻译某批次（P1a/P1b/P2/P3）。"
---

# 英文版翻译规程

## 原则

+ **中文（zh/）是唯一源头**：先改中文并提交，再派生英文；不先改英文、不在英文里修中文没有的内容
+ **动笔前必读** `i18n/glossary.yml`（用哪个词）与 `i18n/STYLE.md`（怎么写），冲突以术语表为准
+ **只翻 scope 内的页**：范围与批次见 `i18n/scope.json`，鸿蒙、微信小程序不翻
+ 英文页与中文同路径：`zh/rtc/overview.md` → `en/rtc/overview.md`；版本登记在 `i18n/en.lock.json`，不写进 frontmatter
+ 服务端 API 生成页（`*/server-api/` 下带「由后端源码自动生成」标记的）**不手译、不 lock**，走下面的 TM 流程

## 新译流程

1. 选页：`python3 scripts/i18n.py status --batch P1a` 看缺译清单
2. 读术语表与 STYLE，再读 zh 页全文
3. 译出 `en/<同路径>`：
   + frontmatter 只译 `title` / `description`，值一律**双引号**包裹
   + 组件标签与非人读属性不动，结构（标题层级、列表、表格行列）逐项不变
   + 代码块只译注释与纯展示字符串；系统真实输出（中文 `msg`、报错原文）不译
   + 图片用根绝对路径 `/zh/.../images/x.png`
4. `python3 scripts/i18n.py links --fix`：自动改写 `/zh`→`/en`、给中文目标补 ` (Chinese)`
5. 手工修 `links` 仍报的：锚点（中文锚点换成目标英文标题的 slug）、`<Card href>` 这类组件链接
6. `python3 scripts/i18n.py lock en/<页>`（zh 必须已提交）
7. `python3 scripts/i18n.py nav`（刷新 docs.json 的 en 导航）
8. `python3 scripts/gen-llms-txt.py`
9. 校验：`python3 scripts/i18n.py check`；再跑 mint 的锚点校验，只看 en 页（zh 页有大量历史报错，不用管）：
   ```bash
   mint broken-links --check-anchors 2>&1 | awk '/^en\//{p=1} /^$/{p=0} p'
   ```
   输出按文件分块：文件路径独占一行、从行首开始（`en/rtc/overview.md`），下面缩进列出该页的断链，块间空一行；
   没有输出即 en 页无断链
10. 提交：en 页 + `i18n/en.lock.json` + `docs.json` + `llms.txt` 一起

## 增量流程（中文改了）

1. `python3 scripts/i18n.py status` → 「过期」一节每行形如
   `en/rtc/overview  zh/rtc/overview.md @ 1a2b3c4d5e6f：1 file changed, 4 insertions(+)`，`@` 后是登记时的 `zh_commit` 前 12 位
2. `git diff 1a2b3c4d5e6f -- zh/rtc/overview.md`（照抄上一步的 commit 与文件），**只改英文里对应的段落**，别整页重译
3. 链接有变动时跑 `links --fix`；再 `lock en/<页>`（中文变了，`reviewed` 会被重置为 false，需重新审校）
4. 标题或 description 变了要重跑 `gen-llms-txt.py`；照新译第 9、10 步校验提交

SDK 发版后的增量：`status --batch <批次>` 只看该平台；changelog 只译客户可感知的条目。

## 服务端 API 翻译记忆表（TM）流程

1. `python3 scripts/sync-server-api.py --tm-missing [rtc|meeting]` → 刷新 `i18n/server-api/<p>.missing.json`
2. 把 `<p>.missing.json` 里的 value 填成英文（key 是中文原文，不改），然后合并：
   ```bash
   python3 scripts/i18n.py tm-merge rtc        # 或 meeting；不带参数两个都合并
   ```
   只合并 value 非空的条目进 `<p>.en.json`，并把它们从 missing 里删掉（没填的留着）。
   **⚠ 必须先 tm-merge 再重跑**：`--tm-missing` 与 sync 都会按当前 `.en.json` 重写 missing.json、把 value 全部重置为空，
   填好没合并就重跑等于白填。填写规则：
   + **value 非空才生效**，空串等于缺失
   + 字段说明结尾**不加句号**；示例值也译（张三 → Alice）
   + TM 是扁平表：同一 key 在分组标题、字段说明等多处共用，译法要兼顾所有出处
   + **两个接口名不能译成同一英文**（会生成相同锚点）
   + 来自后端注释的 `/zh/...` 链接，在译文里改成 `/en/...`
3. `python3 scripts/sync-server-api.py` 生成 en 页；结尾不再提示缺失即补齐。
   **⚠ missing 未清零前不要提交 en 生成页**：sync 照样生成带中文回退的页、照样进 en 导航，`i18n.py check` 也不拦
   （只给 `[翻译记忆缺失]` 告警，`status` 里是 ⚠ 行）。`check` 会拦的是 en 生成页 `##` 标题锚点重名（两个接口名译成同一英文），
   改 `.en.json` 里的译名后重跑
4. 对已译的手写页跑 `python3 scripts/i18n.py links --fix`（生成页新出现后，指向它的 `/zh/...` 链接会改写成 `/en/...`），
   再跑 `python3 scripts/gen-llms-txt.py`
5. 生成页 `##` 标题即接口名，译后锚点变成英文 slug，`links --fix` **不会自动映射**。手工修这 7 个手写页里指向生成页的锚点：
   rtc `server-api/guides/callbacks`、`guides/agents`、`guides/recording`、`server-api/server-demo`；
   meeting `server-api/guides/callbacks`、`guides/recording`；`meeting/ui-sdk/server-integration`（P2）
6. 每个 en 生成页都链到 `/en/<p>/server-api/overview`：**en 生成页必须与 en overview 同一次提交**，否则 i18n-check 变红

## 审校流程

+ 审校清单见 `i18n/STYLE.md` §12（术语、代码块逐字节、结构、frontmatter、链接锚点、图片、标点、格式、语气、登记）
+ 用户审完：`python3 scripts/i18n.py lock --reviewed en/<页>...`；中文在登记后变过会被拒，先做增量
+ 交付审校时给 `mint dev` 预览地址与页面清单，列出中文有歧义、照译的地方

## 批量翻译的 agent 分工

+ **翻译 agent**：每个平台一个，并行；各自只写自己平台的 en 页，不跑 `nav` / `gen-llms-txt`（避免并发改 docs.json、llms.txt）
+ **审校 agent**：按平台串行，逐页对照 STYLE §12 出问题清单，不直接改
+ **修复 agent**：按清单改，完成后统一跑 `links --fix` → `lock` → `nav` → `gen-llms-txt` → 校验。
  **只 lock 本次改动过的页**，并带 `--keep-reviewed`：`lock en/<页> --keep-reviewed`（中文未变时保留已审校状态）；
  不要对整批页无差别重 lock

## 常见坑

+ **锚点**：Mintlify slug 全小写、空格与句点变 `-`、去括号；目标页还没英文时保留中文锚点（链接仍指 /zh）
+ **裸相对链接**（`smeeting-channel`、`./x.md`）：先解析成 `/zh/...` 绝对路径再改写，英文页不留相对链接
+ **(Chinese) 后缀**：markdown 链接由 `links --fix` 增删；组件链接脚本只告警，手工写进 title
+ **YAML `: `**：裸值里的冒号会让 frontmatter 解析失败，所以一律双引号
+ **.mintlify/skills/*/SKILL.md 是 MDX**：不能用 `<!-- -->`、未闭合 `<br>`
+ **.mintignore**：仓库里任何 md 都会被发布；新增内部 md 要加进 `.mintignore`，模式以 `/` 开头
+ `lock` 在浅克隆或 zh 有未提交改动时会拒绝，先 `git fetch --unshallow` / 提交中文
+ **重跑 `lock` 默认把 `reviewed` 重置为 false**：已审校页只改了链接、错字这类（中文没变）时用 `lock --keep-reviewed`；
  中文变了则 `--keep-reviewed` 也会重置，这是对的 —— 英文需要按增量重新审校
