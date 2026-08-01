#!/usr/bin/env python3
"""把后端的对外接口（srvapi）同步成文档站页面。幂等，可反复执行。

    后端源码 ──apidoc(AST+类型检查)──> zh/<产品>/server-api/*.md + docs.json 导航

页面内容**全部**来自后端源码：接口名在 router.go 的路由注释，接口简介在 controller
方法注释，字段说明与示例值在 DTO 字段的行尾注释，错误码在 errcode 常量。本仓不存任何
接口内容 —— 要改就去改代码。篇幅长的玩法说明写成手写页，见各项目的 manual_guides。

两个产品共用一套生成器（在 rtc-backend/tools/apidoc，独立 module）：
SRTC 出 zh/rtc/server-api，SMeeting 出 zh/meeting/server-api。

用法：
    python3 scripts/sync-server-api.py            # 两个都同步
    python3 scripts/sync-server-api.py rtc        # 只同步 SRTC
    python3 scripts/sync-server-api.py meeting    # 只同步 SMeeting
    RTC_BACKEND=/path MEETING_BACKEND=/path python3 scripts/sync-server-api.py
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
from dataclasses import dataclass, field
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent
RTC_BACKEND = Path(os.environ.get('RTC_BACKEND') or DOCS.parent / 'rtc-backend')
MEETING_BACKEND = Path(os.environ.get('MEETING_BACKEND') or DOCS.parent / 'meeting-backend')
# 生成器只有一份，放在 rtc-backend 里；同步 SMeeting 时也是跑它，只是换一套参数
TOOL_DIR = RTC_BACKEND / 'tools' / 'apidoc'

# 自动生成页面的自描述标记，与 apidoc 的 writeFrontmatter 保持一致。
# 靠它识别哪些页面是生成的，而不是硬编码文件名清单 —— 这样新增或删除接口分组时本脚本无需改动。
GENERATED_MARK = '由后端源码自动生成'


@dataclass
class Project:
    """一个产品的同步配置。

    导航顺序统一为：概览 → 接入指南 → 接口文档 → 错误码 → 其它。
    这里只是「排在哪」，不代表内容是手写的 —— 接口文档与错误码都由生成器产出。
    指南排在参考页之前：先看懂玩法再查字段，比一上来就翻几十个接口更容易上手。
    """
    key: str            # 命令行用的名字
    backend: Path       # 后端仓库根目录
    tab: str            # docs.json 里的 tab 名，必须限定，否则会串到另一个产品
    subdir: str         # 文档站下的目录名（zh/<subdir>/server-api）
    src_repo: str       # 页头「请勿手工编辑」提示里指向的仓名
    groups: str = ''    # 分组中文标题表(json)，相对 backend；空表示用生成器内置的 rtc 那份
    skip: str = ''      # 不进对外文档的分组或路由
    manual_head: list = field(default_factory=list)
    manual_guides: dict | None = None
    tail: list = field(default_factory=list)

    @property
    def target(self):
        return DOCS / 'zh' / self.subdir / 'server-api'

    @property
    def doc_base(self):
        return f'/zh/{self.subdir}/server-api'


PROJECTS = [
    Project(
        key='rtc',
        backend=RTC_BACKEND,
        tab='SRTC 音视频 SDK',
        subdir='rtc',
        src_repo='rtc-backend',
        manual_head=['zh/rtc/server-api/overview'],
        manual_guides={
            'group': '接入指南',
            'pages': [
                'zh/rtc/server-api/guides/recording',
                'zh/rtc/server-api/guides/callbacks',
                'zh/rtc/server-api/guides/agents',
            ],
        },
        tail=['zh/rtc/server-api/error-codes', 'zh/rtc/server-api/server-demo'],
    ),
    Project(
        key='meeting',
        backend=MEETING_BACKEND,
        tab='SMeeting 会议 SDK',
        subdir='meeting',
        src_repo='meeting-backend',
        groups='openapi/groups.json',
        # callback/rtc 是 RTC 调进来的入站回调，客户不会调；
        # im/agent 是原样转发到 RTC 的通配代理，真正的接口文档在 SRTC 那边，
        # 生成器只能从 *api 通配符里产出一个空壳，不如交给手写页说清楚指向。
        skip='callback,/server/v1/im/*api,/server/v1/agent/*api',
        manual_head=['zh/meeting/server-api/overview'],
        manual_guides={
            'group': '接入指南',
            'pages': ['zh/meeting/server-api/guides/agent-and-im'],
        },
        tail=['zh/meeting/server-api/error-codes'],
    ),
]


def check_env(proj):
    if not TOOL_DIR.is_dir():
        sys.exit(f'找不到生成器 {TOOL_DIR}\n请设置 RTC_BACKEND 指向 rtc-backend 仓库')
    if not proj.backend.is_dir():
        sys.exit(f'找不到后端 {proj.backend}\n请设置 {proj.key.upper()}_BACKEND 环境变量')


def generate(proj, out_dir):
    """跑生成器。GOWORK=off 是必须的 —— rtc-backend 的 go.work 不含 tools 目录，
    生成器是独立 module（刻意不让 x/tools 进主 go.mod）。"""
    args = ['go', 'run', '.', '-root', str(proj.backend), '-app', 'srvapi',
            '-split', '-docbase', proj.doc_base, '-srcrepo', proj.src_repo,
            # Mintlify 的 ParamField/ResponseField 组件：说明文字占整行宽度。
            # 不用 markdown 表格是因为 Mintlify 把表格列等宽均分（5 列各 150px），
            # 长说明会被压成竖条。生成器另有 -render table，输出不依赖 Mintlify 组件的
            # 通用 markdown，将来做纯文本产物时用那个。
            '-render', 'paramfield',
            '-out', str(out_dir)]
    if proj.groups:
        args += ['-groups', str(proj.backend / proj.groups)]
    if proj.skip:
        args += ['-skip', proj.skip]
    r = subprocess.run(args, cwd=TOOL_DIR, env={**os.environ, 'GOWORK': 'off'},
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('生成失败:\n' + r.stderr)
    print(r.stdout.rstrip())


def sync_pages(proj, out_dir):
    """拷贝新页面，并清理孤儿页。

    孤儿清理是必需的：接口从代码里删除后，文档站磁盘上的旧页面不会自己消失，
    否则会留下一个已下线接口的对外文档（删除 auth 组时就发生过）。
    """
    generated = sorted(p.name for p in out_dir.glob('*.md'))
    for name in generated:
        shutil.copy2(out_dir / name, proj.target / name)

    removed = []
    for p in sorted(proj.target.glob('*.md')):
        if p.name in generated:
            continue
        if GENERATED_MARK in p.read_text(encoding='utf-8'):
            p.unlink()
            removed.append(p.name)
    return generated, removed


def check_callback_guide(proj):
    """校验回调指南与代码里的事件常量一一对应（目前只有 SRTC 有这份指南）。

    接口页会跟着代码自动重生成，手写的指南页不会 —— talkrec 上线时代码里多了两个回调
    事件，指南却毫不知情，是人工比对才发现的。这里把 callback/types.go 的 TypeXxx 常量
    和指南里 `event_name` 形式的小节标题对一遍，两个方向都查：漏写会让客户收到文档里
    没有的事件，多写则是接口已下线而文档还在承诺。
    """
    types_go = proj.backend / 'app' / 'internal' / 'logic' / 'callback' / 'types.go'
    guide = proj.target / 'guides' / 'callbacks.md'
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
        problems.append(f'代码里有回调事件 {e}，指南 {guide.relative_to(DOCS)} 里没写')
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


def check_nav_pages_exist():
    """导航里引用的每个页面在磁盘上都得存在。

    生成页会自动增删，手写页不会 —— manual_guides 里写错一个路径，线上就是一个 404，
    而 mint broken-links 只查页面正文里的链接，查不到导航本身。
    """
    d = json.loads((DOCS / 'docs.json').read_text(encoding='utf-8'))
    problems = []

    def walk(node):
        if isinstance(node, str):
            if not any((DOCS / (node + ext)).is_file() for ext in ('.md', '.mdx')):
                problems.append(f'导航引用 {node}，但 .md/.mdx 都不存在')
        elif isinstance(node, dict):
            for k in ('pages', 'groups', 'tabs', 'languages'):
                walk(node.get(k, []))
        elif isinstance(node, list):
            for x in node:
                walk(x)

    walk(d['navigation'])
    return problems


def update_nav(proj, out_dir):
    frag = json.loads((out_dir / 'nav-fragment.json').read_text(encoding='utf-8'),
                      object_pairs_hook=collections.OrderedDict)
    p = DOCS / 'docs.json'
    d = json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
    # 必须同时限定 tab：两个 tab 下各有一个「服务端 API」分组，只按分组名匹配
    # 会把另一个产品的一起覆盖掉 —— 这事真发生过一次
    pages = list(proj.manual_head)
    if proj.manual_guides:
        pages.append(proj.manual_guides)
    pages += [frag] + list(proj.tail)
    hits = 0
    for lang in d['navigation']['languages']:
        for tab in lang['tabs']:
            if tab.get('tab') != proj.tab:
                continue
            for g in tab.get('groups', []):
                if g.get('group') == '服务端 API':
                    g['pages'] = pages
                    hits += 1
    if hits != 1:
        sys.exit(f'docs.json 里「{proj.tab}」下的「服务端 API」分组命中 {hits} 次（应为 1 次），导航未更新')
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return frag['pages']


def sync(proj):
    check_env(proj)
    print(f'=== {proj.tab} ===')
    # 每次用全新的临时目录：生成器只写不删，复用目录会让上一次的残留被当成本次产物，
    # 导致孤儿清理判断失效
    out_dir = Path(tempfile.mkdtemp(prefix=f'srvapi-{proj.key}-'))
    try:
        generate(proj, out_dir)
        pages, removed = sync_pages(proj, out_dir)
        nav = update_nav(proj, out_dir)
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)

    print(f'\n同步 {len(pages)} 个页面到 {proj.target.relative_to(DOCS)}')
    if removed:
        print('清理孤儿页(接口已从代码中删除):', ', '.join(removed))
    print(f'docs.json 导航 {len(nav)} 项已更新\n')
    return check_callback_guide(proj)


if __name__ == '__main__':
    wanted = sys.argv[1:]
    targets = [p for p in PROJECTS if not wanted or p.key in wanted]
    if not targets:
        sys.exit(f'未知项目 {wanted}，可选：{", ".join(p.key for p in PROJECTS)}')

    problems = []
    for proj in targets:
        problems += sync(proj)

    # 生成的页面到这里已经写好了，下面查的是「手写页有没有跟上代码」——
    # 所以先落盘再校验，失败也不必回滚，改完手写页重跑即可
    problems += check_changelog_ext() + check_nav_pages_exist()
    if problems:
        print('手写页与代码不一致（页面已同步，请修完再提交）:')
        for p in problems:
            print('  ✗ ' + p)
        sys.exit(1)

    print('下一步: mint broken-links')
