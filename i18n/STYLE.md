# 英文版写作规范（给翻译 agent 与审校读）

中文（`zh/`）是唯一源头，英文（`en/`）从中文派生。译之前先读 `i18n/glossary.yml`，术语以它为准；
本文件管「怎么写」，术语表管「用哪个词」。两者冲突时以术语表为准，并回头修正本文件。

## 1. 总原则

+ **美式英语**：color、behavior、initialize、canceled（单 l）、license（名词动词同形）
+ **忠实优先**：不增删技术事实，不补充中文没有的承诺或数字。中文有歧义时照译并在交付说明里列出，不要自己猜
+ **语气**：第二人称（you / your backend），简洁、直陈、不营销。去掉「非常」「轻松」「强大」这类修饰；
  中文里的口语化句子（「不用自己维护状态机去猜」）译成平实英文（"you don't need to track this state yourself"）
+ **祈使句写操作步骤**："Call `join()` with the token." 而不是 "You should call…"
+ **现在时**描述行为："The SDK retries three times." 不写 "will retry"
+ **不加冠词给产品名**：SRTC、SMeeting、STMLink 前不加 the

## 2. 标题

+ **Sentence case**：只有首词和专有名词大写 —— "Mute vs. unpublish"、"Get a channel token"、"Key concepts"
+ 产品名与固定名词（Server API、Web SDK、Swift SDK 等）保留原大小写，不受 sentence case 影响
+ **层级不变**：中文用 `###` 就还是 `###`，不合并、不拆分、不新增标题
+ 标题里的代码标识符保持反引号：`` ### `agent_join` — Device requests to join the channel ``
  （中文标题里的 ` — ` / ` —— ` 分隔统一写成 ` — `，前后各一个空格）
+ 标题不以句号结尾

## 3. Frontmatter

+ **只译 `title` 与 `description`**，其它键（若将来出现）原样保留
+ `title` / `description` 的值**一律用双引号包裹**（`title: "Key concepts"`）：`scripts/gen-llms-txt.py` 只剥双引号，
  单引号或裸值会原样漏进 llms.txt；裸值里出现 `: ` 还会让 YAML 解析失败
+ `title` 用 sentence case；是类名 / 接口名的（`SRTCEngine`、`media-tracks`）原样不译
+ `description` 要讲清「**这页干什么、什么时候该读它**」（见仓库 `CLAUDE.md`）。它是 llms.txt 里 AI 拿到的摘要：
  + 中文 description 是模板句（如「Web SRTC 音视频 SDK 核心概念与架构说明」）时，**允许按正文重写**成有信息量的英文，
    不必逐字对应 —— 这是唯一允许「不忠实于中文」的地方
  + 单行、不换行，≤ 300 字符，不写 "This page…" 开头，直接写内容
+ 不往 frontmatter 里加任何内部字段（版本标记放 `i18n/en.lock.json`）

## 4. 正文格式（结构逐项不变）

+ **列表符号与中文源文保持一致**（多数为 `+`），不自行替换成 `-` / `*`；有序列表保持 `1.`
+ **表格结构不变**：列数、行数、列顺序、对齐行 `| --- |` 都不动，只译单元格文字。空表头 `| | |` 保持为空
+ **强调保持**：中文加粗的地方英文也加粗，覆盖的是同一意群
+ 分隔线 `---`、空行布局与中文一致
+ `<br/>` 等内联 HTML 原样保留

## 5. 代码与标识符

+ **不译**：类名、方法名、属性名、事件名、枚举值、字段名、JSON 键、请求头名、URL / 路径、包名、命令、文件名、配置键与取值
+ **代码块语言标识符不变**（`typescript`、`kotlin`、`text`…）
+ **代码块里只译两类东西**：
  1. **注释**（`//`、`#`、`/* */`、`<!-- -->`）
  2. **纯展示用的人读字符串**：示例里的 UI 文案、`console.log` / `print` 的说明文字、用户自定义的示例值
     （如 `"display_name": "三楼会议室话机"` → `"3rd-floor meeting room phone"`）
+ **代码块里绝不能改的字符串**（改了会影响运行或误导读者）：
  + 任何会被程序比较、解析、拼接、作为 key 使用的字符串（事件名、`type` 取值、`desc` 取值如 `camera_big`、枚举字符串）
  + 签名 / 鉴权示例的待签名串（`app_id=1&nonce=2&timestamp=3&{}`）、HTTP 头、URL、JSON 键
  + **系统真实输出**：服务端 `msg`（如 `"请求头中的signature无效"`）、SDK 报错原文、日志原文 —— 它们实际就是中文，
    改成英文会让读者对不上真实返回。需要时在代码块外或行尾注释里补英文解释：`// "Invalid signature in request headers"`
  + 命令行、安装命令、版本号
+ **伪代码里的占位名可以译**：`HMACSHA256(key, 待签名字符串)` → `HMACSHA256(key, stringToSign)`
+ `text` 块里的中文示意图（生命周期、继承树）要译，保持箭头、缩进与对齐；对齐靠空格的，译后重新对齐
+ 正文里提到代码元素一律用反引号，与中文一致

## 6. Mintlify 组件

+ **标签名与属性名不动**：`<Note>`、`<Warning>`、`<Tip>`、`<Steps>` / `<Step>`、`<ParamField>`、`<ResponseField>`、
  `<Expandable>`、`<Card>`、`<Columns>` 等
+ **只译文字内容与人读属性**：`title="…"`（`<Step title>`、`<Expandable title>`、`<Card title>`）、`description` 类属性
+ **不译的属性**：`path` / `query` / `body` / `name` / `type` / `required` / `default` / `href` / `icon` 等 ——
  它们是参数名、类型或链接
+ 组件的开闭位置、嵌套关系不变；组件内的 markdown（列表、代码、加粗）照第 4、5 节处理
+ 正文里形如 `<UserTrackDesc>`、`List<String>` 的是**类型签名**不是组件，原样保留

## 7. 标点与中文排版符号

| 中文 | 英文 | 说明 |
| --- | --- | --- |
| 「X」（术语 / 引用词） | "X" | 直双引号；术语首次引出也可用斜体 *X*，同页统一 |
| 「X」（指某页 / 某节） | 有链接则直接用链接文字；无链接写 "X"（英文标题） | 如「设备接入指南」→ the "Device integration" guide |
| 「X」（界面按钮 / 菜单） | **X** | 加粗，保留界面上的原文；界面仍是中文时写 **创建应用** (*Create app*) |
| 《X》 | "X" 或链接 | 同上 |
| ——（破折号） | — | 正文用 em dash，**两侧不加空格**："SRTC only carries media—your backend owns the rules." 标题见第 2 节 |
| （ ） | ( ) | 半角，前面留一个空格 |
| ：；，、 | : ; , , | 顿号 `、` 译为逗号；三项以上用 serial comma（A, B, and C） |
| …… | ... 或 … | 列表未尽写 "and more" / "etc." |
| ~ / ～（范围） | – 或 to | 数字范围用 en dash（`1001–1010`）；文字里写 "from 1 to 5" |
| 中英文间空格 | 无需处理 | 英文本身有空格 |

## 8. 数字、单位、版本

+ 数字与单位间留空格：`2 hours`、`64 bytes`、`5 minutes`、`400 ms`、`30 fps`、`1 Mbps`、`16 characters`
+ 分辨率与码率档位原样：`720p`、`1080p`
+ 中文数量级换算成英文：`5 万` → `50,000`；`2 千` → `2,000`；千位用逗号
+ 0–9 在正文里可写作阿拉伯数字（技术文档惯例），与中文保持一致即可
+ 版本号、日期原样：`v0.5.7`、`0.0.11`、`2026-09-29`（ISO 格式，不改成 September 29）
+ 错误码原样，不加千位逗号：`1003`、`180001`

## 9. 链接

+ **站内链接 `/zh/x`**：
  + `en/x` 已存在 → 改成 `/en/x`
  + `en/x` 不存在 → **保留 `/zh/x`**，链接文字后加 ` (Chinese)`：`[Multi-channel](/zh/rtc/web/advanced/multi-channel) (Chinese)`
  + 以上可由 `python3 scripts/i18n.py links --fix` 自动处理（markdown 链接的 ` (Chinese)` 也由它补上，
    英文页译出后再跑会把链接改成 `/en/x` 并删掉多余的后缀）；`<Card href>` 这类组件链接没法自动加，
    脚本只告警，手工把 `(Chinese)` 写进 `title` 或链接文字里。手工译时也按这个规则写
+ **相对链接**（如 `./IRTCTrack.md`、`smeeting-channel`、`./enums.md#…`）：先按所在页位置解析成 `/zh/...` 绝对路径
  （去掉 `.md` 后缀），再按上面的规则改写。英文页里不要留相对链接：不以 `./`、`../` 开头的裸相对链接
  会被 `mint broken-links` 按站点根解析，基本都判为断链
+ **本页锚点** `(#xxx)`：改成本页对应英文标题的锚点
+ **锚点**：中文锚点（`#新增设备`）一律换成目标页**英文标题**的锚点。Mintlify 规则：全小写，空格与句点变连字符，
  去掉括号等标点。例：`## Get a channel token` → `#get-a-channel-token`。目标页还没英文版时保留中文锚点（链接仍指 /zh）
  + 标题中的 `(` `)` 并非总是去掉：如 `setRtcLocalAudioFrameEvent(e)` 的 slug 为 `setrtclocalaudioframeevent-e`
    （不是 `setrtclocalaudioframeevente`）。拿不准时以 `scripts/i18n.py` 的 `mintlify_slug` 计算结果为准
+ 外链原样；指向中文外部站点的可在文字后加 ` (Chinese)`
+ 链接文字要能独立读懂，不写 "click here"

## 10. 图片

+ en 页引用 zh 图片的**根绝对路径**：中文页 `zh/rtc/overview.md` 里的 `images/x.jpeg` → `/zh/rtc/images/x.jpeg`
+ 只有含中文界面、影响理解的关键截图才另拍英文版放 `en/**/images/`，由人工决定
+ alt 文本要译：`![SRTC 产品架构](…)` → `![SRTC architecture](…)`；原来为空的保持为空

## 11. 两层术语（最容易错，单独强调）

+ `zh/rtc/` 页：channel / join / leave / user / track。**不出现** room / meeting / host / enter / exit（源文显式类比或引用会议层除外）
+ `zh/meeting/` 页：room / meeting / enter / exit / member / host。**不出现** channel / join / leave 作为会议概念
  （讲底层 SRTC 的对照表、原样透传的 RTC 错误信息除外）
+ 同一个中文词在两层译法不同：「入会」在 SRTC 页 = join the channel，在 SMeeting 页 = enter the meeting；
  「退出」在 SRTC 页 = leave，在 SMeeting 页 = exit
+ 共用页（`zh/choose`、`zh/ai`）按段落所讲的层分别用词

## 12. 审校清单

逐页过一遍，出现任何一项即退回修复：

1. **术语**：对照 `glossary.yml`，逐个检查「禁止译法」一节；两层术语没有串（第 11 节）
2. **代码块逐字节一致**：去掉注释后，除第 5 节允许翻译的展示字符串与伪代码占位名外，与 zh 页逐字节一致（人工比对，可把两页的代码块分别摘出来 diff；`i18n.py` 不做这项检查）；`text` 示意图块不参与比对；系统真实输出未被翻译
3. **结构一致**：标题数量与层级、列表项数、表格行列数、组件数量与嵌套与 zh 页一致
4. **Frontmatter**：只有 `title` / `description`；description 讲清用途与阅读时机、单行、≤ 300 字符
5. **链接**：`/zh/` 链接已按规则改写或标了 (Chinese)；锚点是英文锚点且目标存在（`i18n.py links`、`mint broken-links --check-anchors` 无新增报错；mint 不加该参数不校验锚点）
6. **图片**：路径是 `/zh/...` 绝对路径或 `en/**/images/` 下真实存在的文件；alt 已译
7. **标点**：无残留全角标点（`，。：；（）「」、`）与中文字符（系统真实输出、界面原文除外）
8. **格式**：列表符号与中文源文保持一致（多数为 `+`），不自行替换；标题 sentence case；美式拼写；数字单位有空格
9. **语气**：第二人称、无营销词、无中文没有的承诺
10. **登记**：译完已跑 `i18n.py lock <page>`，审校通过后 `lock --reviewed`
