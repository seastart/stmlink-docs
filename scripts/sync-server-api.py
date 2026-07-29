#!/usr/bin/env python3
"""把 rtc-backend 的对外接口（srvapi）同步成文档站页面。幂等，可反复执行。

    rtc-backend 源码 ──apidoc(AST+类型检查)──> zh/rtc/server-api/*.md + docs.json 导航

页面内容**全部**来自 rtc-backend 的代码注释（接口名在 router.go，简介在请求 DTO 的
类型注释，字段说明与示例值在字段行尾注释），本仓不存任何接口内容 —— 要改就去改代码。
篇幅长的玩法说明写成 guides/ 下的手写指南页，见下面的 MANUAL_GUIDES。

用法：
    python3 scripts/sync-server-api.py            # rtc-backend 在 ../rtc-backend
    RTC_BACKEND=/path/to/rtc-backend python3 scripts/sync-server-api.py
之后跑 `mint broken-links` 校验，再提交。
"""
import collections
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent
BACKEND = Path(os.environ.get('RTC_BACKEND') or DOCS.parent / 'rtc-backend')
TOOL_DIR = BACKEND / 'tools' / 'apidoc'
TARGET = DOCS / 'zh' / 'rtc' / 'server-api'
DOC_BASE = '/zh/rtc/server-api'

# 自动生成页面的自描述标记，与 apidoc 的 writeFrontmatter 保持一致。
# 靠它识别哪些页面是生成的，而不是硬编码文件名清单 —— 这样新增或删除接口分组时本脚本无需改动。
GENERATED_MARK = '本页接口结构由后端源码自动生成'
# 人工维护的页面，不参与自动增删。
# 「接入指南」放长篇叙述性内容（怎么组合、什么时候用哪个），接口的参数与返回结构
# 一律在生成的参考页里；新增指南页时在这里加一行。
MANUAL_HEAD = ['zh/rtc/server-api/overview']
MANUAL_GUIDES = {
    'group': '接入指南',
    'pages': [
        'zh/rtc/server-api/guides/recording',
        'zh/rtc/server-api/guides/callbacks',
        'zh/rtc/server-api/guides/agents',
    ],
}
MANUAL_TAIL = ['zh/rtc/server-api/error-codes', 'zh/rtc/server-api/server-demo']


def check_env():
    if not TOOL_DIR.is_dir():
        sys.exit(f'找不到生成器 {TOOL_DIR}\n请设置 RTC_BACKEND 指向 rtc-backend 仓库')


def generate(out_dir):
    """跑生成器。GOWORK=off 是必须的 —— rtc-backend 的 go.work 不含 tools 目录，
    生成器是独立 module（刻意不让 x/tools 进主 go.mod）。"""
    env = {**os.environ, 'GOWORK': 'off'}
    r = subprocess.run(
        ['go', 'run', '.', '-root', str(BACKEND), '-app', 'srvapi',
         '-split', '-docbase', DOC_BASE,
         # Mintlify 的 ParamField/ResponseField 组件：说明文字占整行宽度。
         # 不用 markdown 表格是因为 Mintlify 把表格列等宽均分（5 列各 150px），
         # 长说明会被压成竖条。生成器另有 -render table，输出不依赖 Mintlify 组件的
         # 通用 markdown，将来做 llms.txt 这类纯文本产物时用那个。
         '-render', 'paramfield',
         '-out', str(out_dir)],
        cwd=TOOL_DIR, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('生成失败:\n' + r.stderr)
    print(r.stdout.rstrip())


def sync_pages(out_dir):
    """拷贝新页面，并清理孤儿页。

    孤儿清理是必需的：接口从代码里删除后，文档站磁盘上的旧页面不会自己消失，
    否则会留下一个已下线接口的对外文档（删除 auth 组时就发生过）。
    """
    generated = sorted(p.name for p in out_dir.glob('*.md'))
    for name in generated:
        shutil.copy2(out_dir / name, TARGET / name)

    removed = []
    for p in sorted(TARGET.glob('*.md')):
        if p.name in generated:
            continue
        if GENERATED_MARK in p.read_text(encoding='utf-8'):
            p.unlink()
            removed.append(p.name)
    return generated, removed


def update_nav(out_dir):
    frag = json.loads((out_dir / 'nav-fragment.json').read_text(encoding='utf-8'),
                      object_pairs_hook=collections.OrderedDict)
    p = DOCS / 'docs.json'
    d = json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
    hit = False
    for lang in d['navigation']['languages']:
        for tab in lang['tabs']:
            for g in tab.get('groups', []):
                if g.get('group') == '服务端 API':
                    g['pages'] = MANUAL_HEAD + [frag, MANUAL_GUIDES] + MANUAL_TAIL
                    hit = True
    if not hit:
        sys.exit('docs.json 里找不到「服务端 API」分组，导航未更新')
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return frag['pages']


if __name__ == '__main__':
    check_env()
    # 每次用全新的临时目录：生成器只写不删，复用目录会让上一次的残留被当成本次产物，
    # 导致孤儿清理判断失效
    out_dir = Path(tempfile.mkdtemp(prefix='srvapi-docs-'))
    try:
        generate(out_dir)
        pages, removed = sync_pages(out_dir)
        nav = update_nav(out_dir)
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)

    print(f'\n同步 {len(pages)} 个页面到 {TARGET.relative_to(DOCS)}')
    if removed:
        print('清理孤儿页(接口已从代码中删除):', ', '.join(removed))
    print(f'docs.json 导航 {len(nav)} 项已更新')
    print('\n下一步: mint broken-links')
