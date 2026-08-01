#!/usr/bin/env python3
"""把 rtc-backend 的对外接口（srvapi）同步成文档站页面。幂等，可反复执行。

    rtc-backend 源码 ──apidoc(AST+类型检查)──> zh/rtc/server-api/*.md + docs.json 导航

页面内容**全部**来自 rtc-backend 的源码：接口名在 router.go 的路由注释，接口简介在
controller 方法注释，字段说明与示例值在 DTO 字段的行尾注释，错误码在 errcode 常量。
本仓不存任何接口内容 —— 要改就去改代码。篇幅长的玩法说明写成 guides/ 下的手写指南页，
见下面的 MANUAL_GUIDES。

用法：
    python3 scripts/sync-server-api.py            # rtc-backend 在 ../rtc-backend
    RTC_BACKEND=/path/to/rtc-backend python3 scripts/sync-server-api.py
之后跑 `mint broken-links` 校验，再提交。
"""
import collections
import json
import os
import re
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
# 本脚本只管 SRTC tab。SMeeting tab 下的「服务端 API」是另一套（会议层，手写），不要碰
SRTC_TAB = 'SRTC 音视频 SDK'

# 自动生成页面的自描述标记，与 apidoc 的 writeFrontmatter 保持一致。
# 靠它识别哪些页面是生成的，而不是硬编码文件名清单 —— 这样新增或删除接口分组时本脚本无需改动。
GENERATED_MARK = '由后端源码自动生成'
# 导航顺序：概览 → 接入指南 → 接口文档 → 错误码。这里只是「排在哪」，不代表内容是
# 手写的 —— overview 与 guides/* 是手写页，error-codes 由生成器从 errcode 常量产出。
# 「接入指南」放长篇叙述性内容（怎么组合、什么时候用哪个），接口的参数与返回结构
# 一律在生成的参考页里；新增指南页时在这里加一行。
# 指南在参考页之前：先看懂玩法再查字段，比一上来就翻 61 个接口更容易上手。
MANUAL_HEAD = ['zh/rtc/server-api/overview']
MANUAL_GUIDES = {
    'group': '接入指南',
    'pages': [
        'zh/rtc/server-api/guides/recording',
        'zh/rtc/server-api/guides/callbacks',
        'zh/rtc/server-api/guides/agents',
    ],
}
TAIL = ['zh/rtc/server-api/error-codes', 'zh/rtc/server-api/server-demo']


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


def check_callback_guide():
    """校验回调指南与代码里的事件常量一一对应。

    接口页会跟着代码自动重生成，手写的指南页不会 —— talkrec 上线时代码里多了两个回调
    事件，指南却毫不知情，是人工比对才发现的。这里把 callback/types.go 的 TypeXxx 常量
    和指南里 `event_name` 形式的小节标题对一遍，两个方向都查：漏写会让客户收到文档里
    没有的事件，多写则是接口已下线而文档还在承诺。
    """
    types_go = BACKEND / 'app' / 'internal' / 'logic' / 'callback' / 'types.go'
    guide = DOCS / 'zh' / 'rtc' / 'server-api' / 'guides' / 'callbacks.md'
    if not types_go.is_file() or not guide.is_file():
        return []
    in_code = set(re.findall(r'^\s*Type\w+\s*=\s*"([a-z_]+)"',
                             types_go.read_text(encoding='utf-8'), re.M))
    # 一个小节可以同时讲多个事件（im_connect / im_disconnect 就合在一起），取标题里所有反引号词
    documented = set()
    for line in guide.read_text(encoding='utf-8').splitlines():
        if line.startswith('### '):
            documented.update(re.findall(r'`([a-z_]+)`', line))
    problems = []
    for e in sorted(in_code - documented):
        problems.append(f'代码里有回调事件 {e}，指南 guides/callbacks.md 里没写')
    for e in sorted(documented - in_code):
        problems.append(f'指南里写了回调事件 {e}，代码里已经没有了')
    return problems


def check_changelog_ext():
    """docs.json 引用的 changelog/readme 页必须是 .mdx。

    Mintlify 把任意目录下的 changelog.md / readme.md（不分大小写）当仓库元文件排除，
    用 .md 会导致线上 404。这个坑已经踩过两次（iOS 一次、Android 一次），加个断言。
    """
    d = json.loads((DOCS / 'docs.json').read_text(encoding='utf-8'))
    problems = []

    def walk(node):
        if isinstance(node, str):
            if Path(node).stem.lower() in ('changelog', 'readme') and not (DOCS / (node + '.mdx')).is_file():
                problems.append(f'导航引用 {node}，但缺 {node}.mdx（用 .md 会被 Mintlify 当元文件排除，线上 404）')
        elif isinstance(node, dict):
            walk(node.get('pages', []))
            walk(node.get('groups', []))
            walk(node.get('tabs', []))
            walk(node.get('languages', []))
        elif isinstance(node, list):
            for x in node:
                walk(x)

    walk(d['navigation'])
    return problems


def update_nav(out_dir):
    frag = json.loads((out_dir / 'nav-fragment.json').read_text(encoding='utf-8'),
                      object_pairs_hook=collections.OrderedDict)
    p = DOCS / 'docs.json'
    d = json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
    # 必须同时限定 tab：SMeeting tab 下也有一个同名的「服务端 API」分组（会议层的接口文档，
    # 手写维护），只按分组名匹配会把它一起覆盖掉 —— 这事真发生过一次
    hits = 0
    for lang in d['navigation']['languages']:
        for tab in lang['tabs']:
            if tab.get('tab') != SRTC_TAB:
                continue
            for g in tab.get('groups', []):
                if g.get('group') == '服务端 API':
                    g['pages'] = MANUAL_HEAD + [MANUAL_GUIDES, frag] + TAIL
                    hits += 1
    if hits != 1:
        sys.exit(f'docs.json 里「{SRTC_TAB}」下的「服务端 API」分组命中 {hits} 次（应为 1 次），导航未更新')
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

    # 生成的页面到这里已经写好了，下面查的是「手写页有没有跟上代码」——
    # 所以先落盘再校验，失败也不必回滚，改完手写页重跑即可
    problems = check_callback_guide() + check_changelog_ext()
    if problems:
        print('\n手写页与代码不一致（页面已同步，请修完再提交）:')
        for p in problems:
            print('  ✗ ' + p)
        sys.exit(1)

    print('\n下一步: mint broken-links')
