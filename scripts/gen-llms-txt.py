#!/usr/bin/env python3
"""按导航结构生成 llms.txt，覆盖 Mintlify 自动生成的版本。

Mintlify 自动生成的 llms.txt 是**按仓库路径字母序平铺**的一长串页面，
AI 读到时看不出哪些是入口页、哪些是深层参考页，顺序也和侧边栏无关。
官方允许在项目根目录放一份自定义 llms.txt 覆盖它（见 mintlify.com/docs/ai/llmstxt
「Custom files」一节），所以这里按 docs.json 的导航顺序重新生成，并用
`## {产品} · {分组}` 做分节，让 AI 拿到和开发者一样的层级信息。

用法：
    python3 scripts/gen-llms-txt.py          # 生成 llms.txt
    python3 scripts/gen-llms-txt.py --check  # 只校验是否与当前导航一致（CI 用）

改了 docs.json 导航或页面 frontmatter 后，重跑一次即可。
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_JSON = ROOT / "docs.json"
OUT = ROOT / "llms.txt"
SITE = "https://docs.stmlink.com"

# 各页 frontmatter 里没有 description 时的兜底提示，避免 AI 拿到空摘要
NO_DESC = ""


def read_frontmatter(page: str):
    """返回 (title, description)。page 是 docs.json 里的无扩展名路径。"""
    for ext in (".md", ".mdx"):
        f = ROOT / (page + ext)
        if f.exists():
            break
    else:
        return None, None

    text = f.read_text(encoding="utf-8-sig")
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return None, None
    fm = m.group(1)

    def field(name):
        mm = re.search(rf'^{name}:\s*"?(.*?)"?\s*$', fm, re.M)
        return mm.group(1).strip() if mm else None

    return field("title"), field("description")


def walk(pages, section_path, out):
    """递归展开 pages；嵌套 group 追加到 section 名后面，保持层级可见。"""
    for item in pages:
        if isinstance(item, str):
            out.setdefault(section_path, []).append(item)
        else:
            walk(item["pages"], section_path + (item["group"],), out)


def build():
    cfg = json.loads(DOCS_JSON.read_text(encoding="utf-8"))

    lines = [f"# {cfg['name']}", "", f"> {cfg['description']}", ""]

    instructions = (cfg.get("markdown") or {}).get("instructions") or []
    if instructions:
        lines.append("> ## Agent Instructions")
        for ins in instructions:
            lines.append(f"> {ins}")
        lines.append("")

    missing = []
    for lang in cfg["navigation"]["languages"]:
        # 目前只有 zh 有内容，en 为空目录；空语言直接跳过
        for tab in lang.get("tabs", []):
            for group in tab.get("groups", []):
                sections = {}
                walk(group["pages"], (tab["tab"], group["group"]), sections)
                for section_path, pages in sections.items():
                    lines.append("## " + " · ".join(section_path))
                    lines.append("")
                    for page in pages:
                        title, desc = read_frontmatter(page)
                        if title is None:
                            missing.append(page)
                            continue
                        url = f"{SITE}/{page}.md"
                        suffix = f": {desc}" if desc else NO_DESC
                        lines.append(f"- [{title}]({url}){suffix}")
                    lines.append("")

    if missing:
        print("警告：以下导航页缺少文件或 frontmatter，已跳过：", file=sys.stderr)
        for p in missing:
            print("  " + p, file=sys.stderr)

    return "\n".join(lines).rstrip() + "\n"


def main():
    content = build()
    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != content:
            print("llms.txt 与当前导航不一致，请重跑 python3 scripts/gen-llms-txt.py", file=sys.stderr)
            sys.exit(1)
        print("llms.txt 与导航一致")
        return
    OUT.write_text(content, encoding="utf-8")
    pages = content.count("\n- [")
    sections = content.count("\n## ")
    print(f"已生成 {OUT.relative_to(ROOT)}：{sections} 个分节，{pages} 个页面，{len(content)} 字符")


if __name__ == "__main__":
    main()
