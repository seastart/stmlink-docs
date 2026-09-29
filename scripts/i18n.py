#!/usr/bin/env python3
"""英文版（en/）的导航、版本登记与链接校验工具。

中文（zh/）是唯一源头，英文页从中文派生、与中文同路径（zh/rtc/overview.md → en/rtc/overview.md）。
本脚本负责让「英文页有哪些、对应哪个中文版本、链接对不对」这三件事可以机器校验：

    nav     由 docs.json 里 zh 的导航推导 en 导航并写回（en 文件不存在的页自动剔除）
    lock    翻译完成后登记该页对应的中文版本（i18n/en.lock.json）
    status  列出 缺译 / 过期 / 孤儿 / 未登记 / 未审校 / 未纳入范围，以及服务端 API 生成页的翻译记忆缺口
    links   校验 en 页内的链接、锚点与图片路径，--fix 自动改写能确定的那部分（含给指向中文页的链接加 (Chinese)）
    tm-merge 把 i18n/server-api/<产品>.missing.json 里已填的译文合并进 <产品>.en.json
    check   CI 用：只对硬错误退出 1（导航不一致、lock 与文件不符、链接目标或锚点不存在、
            en 生成页 ## 标题重名），过期、未审校、翻译记忆缺失这类只打印告警 —— 中文更新不能被翻译卡住

用法：
    python3 scripts/i18n.py nav [--check]
    python3 scripts/i18n.py lock en/rtc/overview [zh/rtc/token.md ...] [--reviewed | --keep-reviewed] [--synced]
    python3 scripts/i18n.py status [--batch P1a]
    python3 scripts/i18n.py links [--fix]
    python3 scripts/i18n.py tm-merge [rtc|meeting]
    python3 scripts/i18n.py check
    I18N_ROOT=/path/to/fixture python3 scripts/i18n.py status   # 或 --root，指向别的仓库根（测试用）

版本标记为什么放 lock 文件而不是 frontmatter：frontmatter 会进 Markdown 导出与 llms.txt，
内部字段会被客户的 AI 读到。
"""

import argparse
import html
import json
import os
import posixpath
import re
import subprocess
import sys
import unicodedata
import urllib.parse
from collections import OrderedDict, namedtuple
from pathlib import Path

# 仓库根目录；main() 里按 --root / I18N_ROOT 覆盖，测试直接改这个模块变量
ROOT = Path(__file__).resolve().parent.parent

PAGE_EXTS = ('.md', '.mdx')
IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico')

# 服务端 API 生成页的自描述标记（中文与 sync-server-api.py 的 GENERATED_MARK 一致，英文是步骤 4 生成器的写法）。
# 生成页不走 lock：它的英文来自翻译记忆表 i18n/server-api/*.en.json，由 sync 重新生成
GENERATED_MARKS = ('由后端源码自动生成', 'auto-generated from the backend source')
# 生成页所属产品 → 目录前缀；翻译记忆表与缺失清单按产品各一份
SERVER_API_PRODUCTS = {'rtc': 'rtc/server-api/', 'meeting': 'meeting/server-api/'}

# 状态报告里各类问题的中文名，顺序即输出顺序
STATUS_KINDS = OrderedDict([
    ('missing', '缺译'),
    ('stale', '过期'),
    ('orphan', '孤儿'),
    ('unlocked', '未登记'),
    ('unreviewed', '未审校'),
    ('unscoped', '未纳入范围'),  # zh 导航里既不在任何批次、也不在排除列表的页：scope.json 漏配
])

# STYLE §9：保留 /zh 链接时，链接后追加的语言标注
CHINESE_SUFFIX = ' (Chinese)'


# ───────────────────────────── 通用 ─────────────────────────────

def die(msg):
    """打印错误并以 1 退出；msg 里应给出下一步该跑的命令。"""
    print(msg, file=sys.stderr)
    sys.exit(1)


def rel(p):
    """仓库内相对路径（posix 形式），用于输出。"""
    return Path(p).resolve().relative_to(ROOT.resolve()).as_posix()


def load_json(path, default=None):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=OrderedDict)
    except json.JSONDecodeError as e:
        die(f'{rel(path)} 不是合法 JSON：{e}')


def dump_json(obj, sort_keys=False):
    """与 docs.json 现有格式一致：2 空格缩进、不转义中文、结尾换行。"""
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=sort_keys) + '\n'


def page_file(page):
    """page 是无扩展名路径（如 'en/rtc/overview'），返回存在的 .md/.mdx 文件或 None。"""
    for ext in PAGE_EXTS:
        f = ROOT / (page + ext)
        if f.is_file():
            return f
    return None


def strip_page_ext(path):
    for ext in PAGE_EXTS:
        if path.endswith(ext):
            return path[: -len(ext)]
    return path


def normalize_page_arg(arg):
    """把命令行给的页路径（en 或 zh、带不带扩展名与前导 /）规整成 (lang, 语言内路径)。"""
    p = strip_page_ext(arg.strip().lstrip('./').lstrip('/'))
    lang, _, sub = p.partition('/')
    if lang not in ('zh', 'en') or not sub:
        die(f'无法识别的页路径：{arg}（应形如 en/rtc/overview 或 zh/rtc/overview.md）')
    return lang, sub


def list_en_pages():
    """en/ 下所有页（无扩展名路径，已排序）。en 为空时返回空列表。"""
    en = ROOT / 'en'
    if not en.is_dir():
        return []
    pages = set()
    for f in en.rglob('*'):
        if f.is_file() and f.suffix in PAGE_EXTS:
            pages.add(strip_page_ext(rel(f)))
    return sorted(pages)


def is_generated(page):
    """该页（zh 或 en）是否为服务端 API 生成页。"""
    f = page_file(page)
    if not f:
        return False
    text = f.read_text(encoding='utf-8')
    return any(m in text for m in GENERATED_MARKS)


def git(*args, check=True):
    r = subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        die(f'git {" ".join(args)} 失败：\n{r.stderr.strip()}')
    return r


def hash_objects(files):
    """批量取 git blob hash（git hash-object 不要求文件已提交）。返回 {相对路径: hash}。"""
    files = [rel(f) for f in files]
    if not files:
        return {}
    r = subprocess.run(['git', '-C', str(ROOT), 'hash-object', '--stdin-paths'],
                       input='\n'.join(files) + '\n', capture_output=True, text=True)
    if r.returncode != 0:
        die(f'git hash-object 失败：\n{r.stderr.strip()}')
    return dict(zip(files, r.stdout.split()))


# ───────────────────────────── nav ─────────────────────────────

def zh_nav_pages(cfg):
    """zh 导航里的全部页（去重、保持导航顺序）。"""
    zh = find_language(cfg, 'zh')
    out = []

    def walk(items):
        for it in items:
            if isinstance(it, str):
                if it not in out:
                    out.append(it)
            else:
                walk(it.get('pages', []))

    for tab in zh.get('tabs', []):
        for g in tab.get('groups', []):
            walk(g.get('pages', []))
        walk(tab.get('pages', []))
    return out


def find_language(cfg, lang):
    for item in cfg['navigation'].get('languages', []):
        if item.get('language') == lang:
            return item
    if lang == 'zh':
        die('docs.json 的 navigation.languages 里没有 language=="zh" 的语言项')
    return None


def build_en_language(zh, titles):
    """由 zh 语言项推导 en 语言项。

    返回 (en 语言项或 None, 缺译标题列表)。只保留 en 文件存在的页；空的子 group / group / tab 整个剔除。
    缺译只统计「会出现在 en 导航里」的标题 —— 新增的中文分组还没有任何英文页时不必先补译名。
    """
    missing = []

    def tr(kind, name):
        table = titles.get(kind) or {}
        if name in table:
            return table[name]
        missing.append(f'{kind}: {name}')
        return name

    def map_pages(items):
        out = []
        for it in items:
            if isinstance(it, str):
                if not it.startswith('zh/'):
                    continue  # 非 zh 路径没法映射到英文页
                en = 'en/' + it[len('zh/'):]
                if page_file(en):
                    out.append(en)
            else:
                sub = map_pages(it.get('pages', []))
                if sub:
                    out.append(map_group(it, sub))
        return out

    def map_group(g, pages):
        ng = OrderedDict()
        for k, v in g.items():
            if k == 'group':
                ng[k] = tr('groups', v)
            elif k == 'pages':
                ng[k] = pages
            else:
                ng[k] = v
        return ng

    tabs = []
    for tab in zh.get('tabs', []):
        groups = []
        for g in tab.get('groups', []):
            pages = map_pages(g.get('pages', []))
            if pages:
                groups.append(map_group(g, pages))
        tab_pages = map_pages(tab.get('pages', [])) if 'pages' in tab else []
        if not groups and not tab_pages:
            continue
        nt = OrderedDict()
        for k, v in tab.items():
            if k == 'tab':
                nt[k] = tr('tabs', v)
            elif k == 'groups':
                nt[k] = groups
            elif k == 'pages':
                nt[k] = tab_pages
            else:
                nt[k] = v
        tabs.append(nt)

    if not tabs:
        return None, missing  # 一个英文页都没有：不生成空语言项（mint validate 会失败）
    en = OrderedDict([('language', 'en'), ('tabs', tabs)])
    if titles.get('footer'):
        en['footer'] = titles['footer']
    return en, missing


def render_nav():
    """返回 (当前 docs.json 文本, 推导后的文本, 缺译列表)。"""
    docs = ROOT / 'docs.json'
    old = docs.read_text(encoding='utf-8')
    cfg = json.loads(old, object_pairs_hook=OrderedDict)
    titles = load_json(ROOT / 'i18n' / 'nav.en.json', OrderedDict())
    zh = find_language(cfg, 'zh')
    en, missing = build_en_language(zh, titles)

    langs = [x for x in cfg['navigation']['languages'] if x.get('language') != 'en']
    if en is not None:
        langs.insert(langs.index(zh) + 1, en)  # en 紧跟在 zh 之后
    cfg['navigation']['languages'] = langs
    return old, dump_json(cfg), missing


def nav_problems():
    """nav --check 的判定，供 check 复用。返回错误信息列表。"""
    old, new, missing = render_nav()
    if missing:
        return [missing_titles_msg(missing)]
    if old != new:
        return ['docs.json 的 en 导航与由 zh 导航推导的结果不一致，请运行：python3 scripts/i18n.py nav']
    return []


def missing_titles_msg(missing):
    lines = '\n'.join(f'  {m}' for m in sorted(set(missing)))
    return f'i18n/nav.en.json 缺少以下导航标题的英文（补上后重跑 python3 scripts/i18n.py nav）：\n{lines}'


def cmd_nav(args):
    old, new, missing = render_nav()
    if missing:
        die(missing_titles_msg(missing))
    if args.check:
        if old != new:
            die('docs.json 的 en 导航与由 zh 导航推导的结果不一致，请运行：python3 scripts/i18n.py nav')
        print('en 导航与 zh 导航一致')
        return
    if old == new:
        print('docs.json 无变化')
        return
    (ROOT / 'docs.json').write_text(new, encoding='utf-8')
    n = len(json.loads(new)['navigation']['languages'])
    print(f'已更新 docs.json 的 en 导航（当前 {n} 个语言项）')


# ───────────────────────────── lock ─────────────────────────────

LOCK_FIELDS = ('source', 'zh_blob', 'zh_commit', 'reviewed')


def lock_path():
    return ROOT / 'i18n' / 'en.lock.json'


def load_lock():
    """en.lock.json：{"en/<页>": {source, zh_blob, zh_commit, reviewed}}。不存在视为空。"""
    data = load_json(lock_path(), OrderedDict())
    if not isinstance(data, dict):
        die(f'{rel(lock_path())} 顶层应为对象')
    return data


def save_lock(data):
    lock_path().parent.mkdir(parents=True, exist_ok=True)
    lock_path().write_text(dump_json(data, sort_keys=True), encoding='utf-8')


def cmd_lock(args):
    # 浅克隆里 git log -1 -- <文件> 拿到的是截断处的边界提交，而不是真正最后改动该文件的提交，
    # 记进 lock 的 zh_commit 会让日后的增量 diff 基线错位
    if git('rev-parse', '--is-shallow-repository').stdout.strip() == 'true':
        die('当前是浅克隆，取不到中文页真实的最后提交：先运行 git fetch --unshallow 再登记')
    data = load_lock()
    entries = []
    for arg in args.pages:
        _, sub = normalize_page_arg(arg)
        en_page, zh_page = 'en/' + sub, 'zh/' + sub
        en_file, zh_file = page_file(en_page), page_file(zh_page)
        if not en_file:
            die(f'{en_page} 不存在：先翻译出英文页再登记')
        if not zh_file:
            die(f'{zh_page} 不存在：lock 只能登记有中文源头的英文页')
        if is_generated(zh_page):
            die(f'{zh_page} 是服务端 API 生成页，不走 lock —— 补 i18n/server-api/*.en.json 后重跑 '
                'python3 scripts/sync-server-api.py')
        zh_rel = rel(zh_file)
        st = git('status', '--porcelain', '--', zh_rel).stdout.strip()
        if st.startswith('??'):
            die(f'{zh_rel} 从未提交过：先提交中文再登记（lock 记录的是提交过的中文版本）')
        if st:
            die(f'{zh_rel} 有未提交的改动：先提交中文再登记（lock 记录的是提交过的中文版本）')
        commit = git('log', '-1', '--format=%H', '--', zh_rel).stdout.strip()
        if not commit:
            die(f'{zh_rel} 没有任何提交记录：先提交中文再登记')
        entries.append((en_page, zh_rel, commit))

    blobs = hash_objects([ROOT / z for _, z, _ in entries])
    for en_page, zh_rel, commit in entries:
        old = data.get(en_page)
        # 中文在上次登记后变过：lock 会把新的中文版本记成「英文已同步到这一版」，过期状态随之消失。
        # 只改了英文链接就顺手重 lock，会把真正过期的页静默标成最新（2026-09-29 批量 --fix 后踩过），
        # 所以必须显式 --synced 声明「已按 diff 同步过英文」
        if old and old.get('zh_blob') != blobs[zh_rel] and not args.synced:
            die(f'{en_page}：中文在上次登记后已变化，先按 git diff {old.get("zh_commit", "")[:12]} -- {zh_rel} '
                '做增量翻译，确认英文已同步后加 --synced 再登记')
        # 标审校时中文若已在翻译后变过，说明英文已过期，不能直接标成「已审校的最新版」
        if args.reviewed and old and old.get('zh_blob') != blobs[zh_rel]:
            die(f'{en_page}：中文在上次登记后已变化，先按 git diff {old.get("zh_commit", "")[:12]} -- {zh_rel} '
                '做增量翻译，再 lock --reviewed')
        # --keep-reviewed：中文没变（zh_blob 相同）时保留原审校状态 —— 批量流程里修复 agent 只改了
        # 链接这类不涉及中文版本的内容，重 lock 不该把已审校页打回未审校；中文变了则照常重置
        reviewed = bool(args.reviewed) or bool(
            args.keep_reviewed and old and old.get('zh_blob') == blobs[zh_rel] and old.get('reviewed'))
        data[en_page] = OrderedDict([
            ('source', zh_rel),
            ('zh_blob', blobs[zh_rel]),
            ('zh_commit', commit),
            ('reviewed', reviewed),
        ])
        print(f'已登记 {en_page} ← {zh_rel} @ {commit[:12]}' + ('（已审校）' if reviewed else ''))
    save_lock(data)


def lock_problems(data):
    """lock 与文件是否一致（硬错误）。"""
    errs = []
    for key, v in data.items():
        if not isinstance(v, dict) or any(f not in v for f in LOCK_FIELDS):
            errs.append(f'lock 条目 {key} 缺字段（应含 {", ".join(LOCK_FIELDS)}），重跑 python3 scripts/i18n.py lock {key}')
            continue
        if not page_file(key):
            errs.append(f'lock 里登记了 {key}，但英文页不存在：删掉该条目，或恢复英文页')
    return errs


# ───────────────────────────── scope / status ─────────────────────────────

def load_scope():
    """i18n/scope.json：按批次列出纳入翻译的 zh 页（精确页 + 目录前缀），首个命中的批次生效。"""
    scope = load_json(ROOT / 'i18n' / 'scope.json')
    if scope is None:
        die('缺少 i18n/scope.json（翻译范围定义）')
    return scope


def is_excluded(zh_page, scope):
    """是否在 scope.json 的排除列表里（明确不译，如鸿蒙）。"""
    return any(zh_page.startswith(p) for p in scope.get('excluded_prefixes', []))


def batch_of(zh_page, scope):
    """zh 页属于哪个批次；被排除或不在任何批次里都返回 None（两者用 is_excluded 区分）。"""
    if is_excluded(zh_page, scope):
        return None
    for b in scope['batches']:
        if zh_page in b.get('pages', []) or any(zh_page.startswith(p) for p in b.get('prefixes', [])):
            return b['name']
    return None


def diff_shortstat(commit, zh_rel):
    r = git('diff', '--shortstat', commit, '--', zh_rel, check=False)
    if r.returncode != 0:
        return '（该提交在本仓不存在，无法取增量）'
    return r.stdout.strip() or '（无文本差异）'


def count_entries(path):
    """翻译记忆表 / 缺失清单的条数（数组按元素、对象按键；约定见 sync-server-api.py）。"""
    data = load_json(path)
    if data is None:
        return None
    return len(data)


def collect_status(batch=None):
    """返回 (问题字典 {kind: [(页, 说明)]}, 生成页统计列表)。缺译条目多一个批次名：(页, 说明, 批次)。"""
    scope = load_scope()
    names = [b['name'] for b in scope['batches']]
    if batch and batch not in names:
        die(f'未知批次 {batch}，可选：{", ".join(names)}')

    cfg = json.loads((ROOT / 'docs.json').read_text(encoding='utf-8'))
    lock = load_lock()
    issues = OrderedDict((k, []) for k in STATUS_KINDS)

    def want(sub):
        return batch is None or batch_of('zh/' + sub, scope) == batch

    # 缺译：zh 导航里在范围内、en 不存在的手写页
    gen_pages = {k: [] for k in SERVER_API_PRODUCTS}  # 产品 → 在范围内的生成页（语言内路径）
    for zh_page in zh_nav_pages(cfg):
        if not page_file(zh_page):
            continue
        b = batch_of(zh_page, scope)
        if b is None:
            # 未纳入范围只在看全部批次时报：它不属于任何批次，按批次过滤时无从归属
            if not batch and not is_excluded(zh_page, scope):
                issues['unscoped'].append((zh_page, '不在 i18n/scope.json 的任何批次或排除列表里'))
            continue
        if batch and b != batch:
            continue
        sub = zh_page[len('zh/'):]
        if is_generated(zh_page):
            for prod, prefix in SERVER_API_PRODUCTS.items():
                if sub.startswith(prefix):
                    gen_pages[prod].append(sub)
            continue
        if not page_file('en/' + sub):
            issues['missing'].append((zh_page, f'→ en/{sub}', b))
    issues['missing'].sort(key=lambda x: names.index(x[2]))  # 按批次分组，批次内保持导航顺序

    # 已有英文页：孤儿 / 未登记 / 过期 / 未审校
    en_pages = [p for p in list_en_pages() if want(p[len('en/'):])]
    checkable = []
    for en_page in en_pages:
        sub = en_page[len('en/'):]
        if not page_file('zh/' + sub):
            issues['orphan'].append((en_page, f'zh/{sub} 已不存在'))
        elif is_generated(en_page) or is_generated('zh/' + sub):
            continue  # 生成页不走 lock
        elif en_page not in lock:
            issues['unlocked'].append((en_page, f'翻译完成后运行 python3 scripts/i18n.py lock {en_page}'))
        else:
            checkable.append(en_page)

    blobs = hash_objects([page_file('zh/' + p[len('en/'):]) for p in checkable])
    for en_page in checkable:
        entry = lock[en_page]
        zh_rel = rel(page_file('zh/' + en_page[len('en/'):]))
        if entry.get('zh_blob') != blobs.get(zh_rel):
            # 带上登记时的 zh_commit（前 12 位），增量翻译直接 git diff <zh_commit> -- <zh 文件>
            commit = entry.get('zh_commit', '')
            issues['stale'].append((en_page, f'{zh_rel} @ {commit[:12]}：{diff_shortstat(commit, zh_rel)}'))
        if not entry.get('reviewed'):
            issues['unreviewed'].append((en_page, ''))

    # 服务端 API 生成页：看英文页是否已生成，以及翻译记忆表缺多少条
    gen_stats = []
    for prod, subs in gen_pages.items():
        if not subs and batch:
            continue
        tm_dir = ROOT / 'i18n' / 'server-api'
        gen_stats.append({
            'product': prod,
            'pages': len(subs),                                       # 范围内的 zh 生成页数
            'no_en': ['en/' + s for s in subs if not page_file('en/' + s)],  # 还没生成英文的页
            'tm': count_entries(tm_dir / f'{prod}.en.json'),
            'tm_missing': count_entries(tm_dir / f'{prod}.missing.json'),
        })
    return issues, gen_stats


def tm_fallback_warnings(gen_stats):
    """翻译记忆有缺失、却已有 en 生成页：这些页里含中文回退，sync 照样生成并进导航、check 也不拦，
    容易被当成译完提交。返回告警文本列表（status 与 check 共用）。"""
    out = []
    for s in gen_stats:
        en_pages = s['pages'] - len(s['no_en'])
        if s['tm_missing'] and en_pages:
            out.append(f'{s["product"]}：已有 {en_pages} 个 en 生成页，但翻译记忆缺失 {s["tm_missing"]} 条 —— '
                       '页内含中文回退，补齐前不要提交 en 生成页')
    return out


def cmd_status(args):
    issues, gen_stats = collect_status(args.batch)
    title = f'英文版状态（批次 {args.batch}）' if args.batch else '英文版状态（全部批次）'
    print(title)
    for kind, label in STATUS_KINDS.items():
        items = issues[kind]
        print(f'\n## {label}（{len(items)}）')
        last_batch = None
        for page, note, *batch in items:
            if batch and batch[0] != last_batch:
                last_batch = batch[0]
                print(f'  ### {last_batch}（{sum(1 for x in items if x[2] == last_batch)}）')
            print(f'  {page}' + (f'  {note}' if note else ''))

    gen_no_en = tm_missing = 0
    if gen_stats:
        print('\n## 服务端 API 生成页（走翻译记忆表，不走 lock）')
        for s in gen_stats:
            tm = '无翻译记忆表' if s['tm'] is None else f'翻译记忆 {s["tm"]} 条'
            miss = '缺失清单未生成' if s['tm_missing'] is None else f'缺失 {s["tm_missing"]} 条'
            print(f'  {s["product"]}：生成页 {s["pages"]}，英文页缺 {len(s["no_en"])}；{tm}，{miss}')
            for p in s['no_en']:
                print(f'    {p}')
            gen_no_en += len(s['no_en'])
            tm_missing += s['tm_missing'] or 0
        if gen_no_en or tm_missing:
            print('  补 i18n/server-api/*.en.json 后运行 python3 scripts/sync-server-api.py')
        for w in tm_fallback_warnings(gen_stats):
            print(f'  ⚠ {w}')

    summary = '、'.join(f'{label} {len(issues[k])}' for k, label in STATUS_KINDS.items())
    print(f'\n合计：{summary}、生成页缺英文 {gen_no_en}、翻译记忆缺失 {tm_missing} 条')


# ───────────────────────────── slug（对齐 Mintlify） ─────────────────────────────
#
# 锚点生成以 mint CLI 自带的源码为准（mint 全局安装目录下 node_modules/@mintlify/，
# @mintlify/common 1.0.779、@sindresorhus/slugify 2.2.0）：
#   common/dist/slugify.js                          slugify() / cleanHeadingId()
#   common/dist/mdx/lib/remark-utils.js             getUnicodeId() / getTableOfContentsTitle()
#   common/dist/mdx/plugins/remark/remarkComponentIds.js   标题 id（h1~h4、全页计数）、Tab、Accordion id
#   common/dist/mdx/plugins/remark/remarkExtractTableOfContents.js   Update / Step 的 id
#   common/dist/mdx/plugins/rehype/rehypeParamFieldIds.js  ParamField 的 id
#   common/dist/mdx/componentIds.js                 哪些组件的 id 会被 cleanHeadingId、哪些不透传 id
#   link-rot/dist/graph.js、static-checking/getBrokenInternalLinks.js   mint broken-links 如何比对锚点
#   @sindresorhus/slugify/index.js                  slugify() / slugifyWithCounter()
#
# 流程：标题 → 小写、trim、空白变 - → encodeURIComponent → 若含 %XX（中文、/、&、反引号等）
# 则按「保留 % 与 _、不转小写」slugify，否则按「保留 _」slugify → 同页重复加 -2/-3 →
# 比对时两边都做 cleanHeadingId（URL 解码 + 去掉 ?,;:!'"()[]{} 与 emoji）。
# 所以 '新增设备' → '新增设备'，'a/b & c' → 'a/b-&-c'，"It's" → 'its'，'It’s' → 'it’s'，'v1.2' → 'v1-2'。

_SLUG_REPLACEMENTS = [('&', ' and '), ('🦄', ' unicorn '), ('♥', ' love ')]


def _transliterate(s):
    """@sindresorhus/transliterate 的近似：只去掉变音符号（é→e）。标题路径下输入已是纯 ASCII，不受影响。"""
    for a, b in _SLUG_REPLACEMENTS:
        s = s.replace(a, b)
    s = unicodedata.normalize('NFKD', s)
    return unicodedata.normalize('NFC', ''.join(c for c in s if not unicodedata.combining(c)))


def _decamelize(s):
    s = re.sub(r'([A-Z]{2,})(\d+)', r'\1 \2', s)
    s = re.sub(r'([a-z\d]+)([A-Z]{2,})', r'\1 \2', s)
    s = re.sub(r'([a-z\d])([A-Z])', r'\1 \2', s)
    return re.sub(r'([A-Z]+)([A-Z][a-rt-z\d]+)', r'\1 \2', s)


def sindre_slugify(s, lowercase=True, decamelize=True, preserve=()):
    """@sindresorhus/slugify 的 slugify()，separator 固定为 '-'。"""
    s = _transliterate(s)
    if decamelize:
        s = _decamelize(s)
    keep = 'a-z0-9' + ('' if lowercase else 'A-Z') + ''.join(re.escape(c) for c in preserve)
    if lowercase:
        s = s.lower()
    s = re.sub(f'[^{keep}]+', '-', s)
    s = s.replace('\\', '')
    s = re.sub(r'([a-zA-Z0-9]+)-([ts])(-|$)', r'\1\2\3', s)  # 缩写/所有格：dont、its
    s = re.sub(r'-{2,}', '-', s)
    return re.sub(r'^-|-$', '', s)


class SlugCounter:
    """@sindresorhus/slugify 的 slugifyWithCounter()：同一计数器内重复的 slug 追加 -2、-3……"""

    def __init__(self):
        self.occurrences = {}

    def __call__(self, slug):
        if not slug:
            return ''
        low = slug.lower()
        numberless = self.occurrences.get(re.sub(r'(?:-\d+?)+?$', '', low), 0)
        counter = self.occurrences.get(low)
        self.occurrences[low] = counter + 1 if counter is not None else 1
        new = self.occurrences[low] or 2
        if new >= 2 or numberless > 2:
            slug = f'{slug}-{new}'
        return slug


def encode_uri_component(s):
    return urllib.parse.quote(s, safe="!*'()")  # quote 本身已保留字母数字与 _.-~


def mintlify_slug(title, counter=None):
    """@mintlify/common 的 slugify(title, counter)：返回原始 slug（中文等为 %XX 形式）。"""
    enc = encode_uri_component(re.sub(r'\s+', '-', title.lower().strip()))
    if re.search(r'%[0-9A-F]{2}', enc):
        slug = sindre_slugify(enc, lowercase=False, decamelize=False, preserve=('%', '_'))
    else:
        slug = sindre_slugify(enc, decamelize=False, preserve=('_',))
    return (counter or SlugCounter())(slug)


_EMOJI_RE = re.compile(
    '[\u200d\ufe0e\ufe0f\u00a9\u00ae\u203c\u2049\u2122\u2139\u2194-\u21aa\u231a-\u23ff\u24c2'
    '\u25aa-\u25fe\u2600-\u27bf\u2934\u2935\u2b05-\u2b55\u3030\u303d\u3297\u3299\U0001f000-\U0001faff]')


def clean_heading_id(slug):
    """@mintlify/common 的 cleanHeadingId：URL 解码，去掉 ?,;:!'"()[]{} 与 emoji（emoji 区间为近似）。"""
    s = urllib.parse.unquote(slug)
    s = re.sub(r'''[?,;:!'"()\[\]{}]''', '', s)
    return _EMOJI_RE.sub('', s)


def heading_text(raw):
    """getTableOfContentsTitle 的近似：拼接标题里的纯文本与行内代码，去掉强调、链接地址、图片与标签。"""
    parts = re.split(r'(`+)(.+?)\1', raw)
    out = []
    for i in range(0, len(parts), 3):
        # 反斜杠转义先换成占位符，免得 `\<T\>` 这类被当成标签删掉
        escaped = []

        def hold(m):
            escaped.append(m.group(1))
            return f'\ue000{len(escaped) - 1}\ue001'

        t = re.sub(r'\\([!-/:-@\[-`{-~])', hold, parts[i])
        t = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', t)
        t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
        t = re.sub(r'</?[A-Za-z][^>]*>', '', t)
        t = re.sub(r'\*\*|__|~~|\*', '', t)
        t = re.sub(r'(?<![A-Za-z0-9])_(?=\S)(.+?)(?<=\S)_(?![A-Za-z0-9])', r'\1', t)
        t = re.sub('\ue000(\\d+)\ue001', lambda m: escaped[int(m.group(1))], html.unescape(t))
        out.append(t)
        if i + 2 < len(parts):
            code = parts[i + 2]
            if len(code) > 1 and code.startswith(' ') and code.endswith(' '):
                code = code[1:-1]
            out.append(code)
    return ''.join(out)


# ───────────────────────────── 页面解析 ─────────────────────────────

def _blank(m):
    """把匹配段替换成等长空白（保留换行），这样屏蔽后的文本与原文位置一一对应。"""
    return re.sub(r'[^\n]', ' ', m.group(0))


def mask_blocks(text):
    """屏蔽 frontmatter、``` / ~~~ 代码块、MDX 与 HTML 注释。"""
    text = re.sub(r'\A---\n.*?\n---(?=\n|\Z)', _blank, text, flags=re.S)
    lines = text.split('\n')
    fence = None  # 当前代码块的围栏（字符, 长度）
    for i, line in enumerate(lines):
        m = re.match(r'^[ \t]*(`{3,}|~{3,})', line)
        if fence is None:
            if m:
                fence = (m.group(1)[0], len(m.group(1)))
                lines[i] = ' ' * len(line)
        else:
            lines[i] = ' ' * len(line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] \
                    and not line.strip()[len(m.group(1)):].strip():
                fence = None
    text = '\n'.join(lines)
    text = re.sub(r'\{/\*.*?\*/\}', _blank, text, flags=re.S)
    return re.sub(r'<!--.*?-->', _blank, text, flags=re.S)


def mask_inline_code(text):
    return re.sub(r'(`+)[^\n]*?\1', _blank, text)


_TAG_RE = re.compile(r'''<([A-Za-z][A-Za-z0-9]*)\b((?:[^>"'{}]|"[^"]*"|'[^']*'|\{[^{}]*\})*)/?>''')
_ATTR_RE = re.compile(r'''([A-Za-z_][\w-]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|\{\s*["']([^"']*)["']\s*\})''')

# componentIds.js：这些组件不把 id 透传到 DOM，指向它们的锚点在 mint broken-links 眼里是断的
COMPONENTS_WITHOUT_ID = {
    'Info', 'Warning', 'Note', 'Tip', 'Check', 'Danger', 'Callout', 'AccordionGroup', 'Card', 'CardGroup',
    'Tabs', 'CodeGroup', 'Column', 'Columns', 'CustomCode', 'CustomComponent', 'DynamicCustomComponent',
    'Expandable', 'Frame', 'Icon', 'Latex', 'Mermaid', 'Panel', 'Popup', 'Prompt', 'RequestExample',
    'ResponseExample', 'SnippetGroup', 'Steps', 'Tile', 'Tooltip', 'Tree', 'Badge', 'Color', 'ZoomImage',
}
COMPONENTS_WITH_CLEANED_ID = {'Heading', 'Step', 'Update'}
PARAM_FIELD_NAMES = {'ParamField', 'Param', 'ResponseField'}
PARAM_FIELD_ATTRS = ('query', 'path', 'body', 'header', 'name')


_CLOSE_TAG_RE = re.compile(r'</[A-Za-z][\w.:-]*\s*>')
# 行首的列表 / 引用标记：`+ <Tab>`、`> <Tab>` 里的标签仍是块级
_BLOCK_PREFIX_RE = re.compile(r'^[ \t]*(?:(?:>|[+*-]|\d{1,9}[.)])[ \t]+)*')


def is_flow_tag(masked, m):
    """标签 m 在 mint 里是否被解析成块级元素（mdxJsxFlowElement）。

    依据：mint 的 id 全部只从 mdxJsxFlowElement 上取（remarkComponentIds.js 的 Tab/Accordion、
    remarkExtractTableOfContents.js 的 Update/Step/显式 id、getBrokenInternalLinks.js 的
    extractComponentAnchorIds）；而 micromark 的 mdx-jsx 只在「标签所在行除了标签、空白、{表达式}
    外别无内容」时才解析成块级，否则是行内的 mdxJsxTextElement。用 mint 自带的 coreRemark 实测：
      <Tab title="A">x</Tab>          → 行内（同行夹带文字，不生成 id）
      <Tab title="A"></Tab>、<Tab title="A" />、<Tab title="A"> 独占一行（内容在下一行）→ 块级
      <Tab title="I" /> <Tab title="J" />  → 两个都是块级（一行里只有标签）
      + <Tab title="M">、> <Tab title="N">  → 块级（列表 / 引用标记不算内容）
    """
    start = masked.rfind('\n', 0, m.start()) + 1
    end = masked.find('\n', m.end())
    seg = masked[start:end if end >= 0 else len(masked)]  # 标签跨行时 seg 也跨行，整段一起判断
    seg = _CLOSE_TAG_RE.sub('', _TAG_RE.sub('', seg))
    seg = re.sub(r'\{[^{}]*\}', '', seg)
    return not _BLOCK_PREFIX_RE.sub('', seg).strip()


def tag_attrs(attr_text):
    """标签属性 → 有序 [(名, 值)]，只取字符串值。"""
    return [(m.group(1), next(g for g in m.groups()[1:] if g is not None)) for m in _ATTR_RE.finditer(attr_text)]


def page_anchors(text):
    """一页可被 #锚点 指向的全部 id（已做 cleanHeadingId，可与链接锚点直接比对）。"""
    masked = mask_blocks(text)
    ids = set()

    # 标题：h1~h4，全页一个计数器（remarkComponentIds）
    counter = SlugCounter()
    for line in masked.split('\n'):
        m = re.match(r'^[ \t]*(#{1,6})(?:[ \t]+(.*?))?[ \t]*$', line)
        if not m or len(m.group(1)) > 4:
            continue
        raw = re.sub(r'(?:^|[ \t]+)#+$', '', m.group(2) or '')
        # 空标题的 slug 为 ''，mint 同样会收进集合（无害，保持一致）
        ids.add(clean_heading_id(mintlify_slug(heading_text(raw), counter)))

    # 组件：Tab / Accordion / ParamField / Update / Step / 显式 id —— 只有块级标签生成 id（见 is_flow_tag）
    tab_counter, toc_counter = SlugCounter(), SlugCounter()
    accordion_counts, param_counts = {}, {}
    for m in _TAG_RE.finditer(masked):
        if not is_flow_tag(masked, m):
            continue
        name, attrs = m.group(1), tag_attrs(m.group(2))
        a = dict(attrs)
        if name in PARAM_FIELD_NAMES:
            key = next((v for k, v in attrs if k in PARAM_FIELD_ATTRS and v), None)
            if key:
                n = param_counts.get(key, 0)
                param_counts[key] = n + 1
                ids.add(sindre_slugify(f'param-{key}' + (f'_{n}' if n else '')))
            continue
        if name in COMPONENTS_WITHOUT_ID:
            continue
        if name == 'Tab' and a.get('title'):
            ids.add(mintlify_slug(a['title'], tab_counter))  # Tab 的 id 不做 cleanHeadingId
        if name == 'Accordion' and a.get('title') and 'id' not in a:
            n = accordion_counts.get(a['title'], 0)
            accordion_counts[a['title']] = n + 1
            base = sindre_slugify(a['title'].replace(':', '-', 1), decamelize=False)
            ids.add(f'{base}-{n}' if n else base)
        toc_title = None
        if name == 'Update' and 'label' in a:
            toc_title = a['label']
        elif name == 'Step' and a.get('titleSize') in ('h2', 'h3') and a.get('title', '').strip():
            toc_title = a['title']
        if toc_title is not None:
            ids.add(clean_heading_id(a['id'] if 'id' in a else mintlify_slug(toc_title, toc_counter)))
        elif 'id' in a and a['id']:
            ids.add(clean_heading_id(a['id']) if name in COMPONENTS_WITH_CLEANED_ID else a['id'])
    return ids


_MD_LINK_RE = re.compile(
    r'(?P<bang>!?)\[(?P<text>(?:[^\[\]\n]|\[[^\[\]\n]*\])*)\]'
    r'\(\s*(?P<url><[^>\n]*>|[^\s()]*(?:\([^\s()]*\)[^\s()]*)*)'
    r'(?:\s+(?:"[^"\n]*"|\'[^\'\n]*\'))?\s*\)')
_REF_DEF_RE = re.compile(r'^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*(\S+)', re.M)
_URL_ATTR_RE = re.compile(r'''\b(href|src)\s*=\s*(?:"([^"]*)"|'([^']*)')''')

# 一条链接。start/end 是 url 在原文里的位置（--fix 按位置改写）
Link = namedtuple('Link', [
    'start', 'end', 'url', 'is_image',
    'kind',   # md = [文字](url)；ref = [x]: url 引用定义；tag = HTML / 组件的 href、src 属性
    'label',  # md：链接文字原文；tag：从开标签到闭合标签（再多带后缀长度）的原文，用来判断是否已注明 (Chinese)
    'tail',   # md：整个链接（右括号）之后的位置，(Chinese) 从这里插入；其它为 None
])


def extract_links(text):
    """页内全部链接（Link 列表，按位置排序）。代码块、行内代码、注释里的不算。"""
    masked = mask_inline_code(mask_blocks(text))
    out = []
    for m in _MD_LINK_RE.finditer(masked):
        start, end = m.span('url')
        url = text[start:end]
        if url.startswith('<') and url.endswith('>'):
            start, end, url = start + 1, end - 1, url[1:-1]
        label = text[m.start('text'):m.end('text')]  # 取原文：屏蔽后行内代码已成空白
        out.append(Link(start, end, url, m.group('bang') == '!', 'md', label, m.end()))
    for m in _REF_DEF_RE.finditer(masked):
        out.append(Link(m.start(1), m.end(1), m.group(1), False, 'ref', None, None))
    for t in _TAG_RE.finditer(masked):
        close = -1 if t.group(0).endswith('/>') else masked.find(f'</{t.group(1)}', t.end())
        close = masked.find('>', close) + 1 if close >= 0 else t.end()
        label = text[t.start():close + len(CHINESE_SUFFIX)]
        for a in _URL_ATTR_RE.finditer(t.group(0)):
            g = 2 if a.group(2) is not None else 3
            start = t.start() + a.start(g)
            end = t.start() + a.end(g)
            out.append(Link(start, end, text[start:end], a.group(1) == 'src', 'tag', label, None))
    return sorted(out)


# ───────────────────────────── links ─────────────────────────────
#
# 相对路径的解析规则以 mint broken-links 为准（link-rot/dist/graph.js 的 MdxPath.constructParsedPath）：
#   以 . 开头（./x、../x）→ 按所在页目录解析：resolve(relativeDir, path)
#   其它不以 / 开头的「裸相对路径」（x、server-api/overview#y、images/a.png）→ 只去掉前导 /，
#     即**按站点根解析**，与所在目录无关
# 浏览器对裸相对路径是按当前 URL 的目录解析的，所以同一个链接在线上可能能点、mint 却判断链
# （zh 页现有的 smeeting-channel 这类链接就是这样被 mint broken-links 报出来的）。
# 英文页以 mint 的判断为准：裸相对路径按站点根解析不到就是错误，--fix 按所在目录推断作者本意改成绝对路径。

class LinkChecker:
    """校验 en 页链接。每条问题：(页, 行号, 级别, 说明, 替换后的 url 或 None)。

    级别：error = 硬错误（check 会失败）；warn = 告警；fix 的 url 非空表示 --fix 可自动改写。
    """

    def __init__(self):
        self._anchors = {}
        cfg = json.loads((ROOT / 'docs.json').read_text(encoding='utf-8'))
        self.redirects = {r['source'].rstrip('/'): r['destination'] for r in cfg.get('redirects', [])}

    def anchors(self, page):
        if page not in self._anchors:
            f = page_file(page)
            self._anchors[page] = page_anchors(f.read_text(encoding='utf-8')) if f else set()
        return self._anchors[page]

    def has_anchor(self, page, anchor):
        return clean_heading_id(anchor) in self.anchors(page)

    def check_page(self, en_page):
        """返回 (原文, 问题列表)。问题：(起, 止, 行号, 级别, 说明, 替换文本或 None)，--fix 把 [起, 止) 换成替换文本。"""
        text = page_file(en_page).read_text(encoding='utf-8')
        issues = []
        for link in extract_links(text):
            line = text.count('\n', 0, link.start) + 1
            url_issues = self.check_url(en_page, link.url, link.is_image)
            for level, msg, new in url_issues:
                issues.append((link.start, link.end, line, level, msg, new))
            if not link.is_image:
                # 按 --fix 之后的 url 判断要不要 (Chinese)：改写后仍指向 /zh 的才需要
                final = next((new for _, _, new in url_issues if new), link.url)
                for start, end, level, msg, new in self.check_chinese_suffix(text, link, final):
                    issues.append((start, end, line, level, msg, new))
        return text, issues

    def site_page(self, url):
        """url 若是指向站内 en / zh 页的绝对路径，返回 (语言, 语言内路径)（已套用重定向）；否则 None。"""
        path = url.strip().partition('#')[0].split('?', 1)[0]
        if not path.startswith('/') or path.lower().endswith(IMAGE_EXTS):
            return None
        target = strip_page_ext(path).rstrip('/')
        if target in self.redirects:
            target = self.redirects[target].partition('#')[0].rstrip('/')
        lang, _, sub = target.lstrip('/').partition('/')
        if lang not in ('en', 'zh') or not sub:
            return None
        return lang, sub

    def check_chinese_suffix(self, text, link, final_url):
        """STYLE §9：指向未译中文页的链接要在链接后注明 (Chinese)。返回 [(起, 止, 级别, 说明, 替换文本)]。

        markdown 链接可自动修：缺了在右括号后插入，指向的页已有英文版（改写成 /en 之后）则删掉多余的后缀。
        HTML / 组件的 href（<Card>、<a>）和引用式链接没有固定的地方可插，只告警、由人工写进文字里。
        """
        target = self.site_page(final_url)
        # 指向 /zh 且英文页还不存在；英文页已存在的 /zh 链接会被改写或另有「应改为 /en」的告警，不在这里管
        untranslated = target is not None and target[0] == 'zh' and not page_file('en/' + target[1])
        if link.kind == 'md':
            label = link.label.strip()
            if label.startswith('![') or re.fullmatch(r'(`+)[^`](?:.*[^`])?\1', label):
                return []  # 链接文字是图片或代码：加后缀会破坏排版
            has_suffix = text.startswith(CHINESE_SUFFIX, link.tail)
            if untranslated and not has_suffix and not label.endswith('(Chinese)'):
                return [(link.tail, link.tail, 'warn', f'指向未译的中文页，链接后应加 "{CHINESE_SUFFIX.strip()}"',
                         CHINESE_SUFFIX)]
            if has_suffix and target is not None and target[0] == 'en' and page_file('en/' + target[1]):
                return [(link.tail, link.tail + len(CHINESE_SUFFIX), 'warn',
                         f'已指向英文页，应删掉链接后的 "{CHINESE_SUFFIX.strip()}"', '')]
            return []
        if untranslated and not (link.label and '(Chinese)' in link.label):
            where = '组件 / HTML 链接' if link.kind == 'tag' else '引用式链接'
            return [(link.start, link.end, 'warn',
                     f'{where}指向未译的中文页，需在链接文字里手工注明 "{CHINESE_SUFFIX.strip()}"', None)]
        return []

    def check_url(self, en_page, url, is_image):
        """返回 [(级别, 说明, 替换 url 或 None)]。"""
        url = url.strip()
        if not url or url.startswith(('//', '{', 'mailto:')) or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', url):
            return []
        path, _, anchor = url.partition('#')
        path = path.split('?', 1)[0]
        is_image = is_image or path.lower().endswith(IMAGE_EXTS)

        if is_image:
            return self.check_image(en_page, path)
        if not path:  # 本页锚点
            if anchor and not self.has_anchor(en_page, anchor):
                return [('error', f'本页找不到锚点 #{anchor}（按英文标题重算锚点）', None)]
            return []
        if path.startswith('/'):
            return self.check_target(path, anchor, relative=False)

        by_dir = posixpath.normpath(posixpath.join(posixpath.dirname('/' + en_page), path))
        if path.startswith('.'):  # ./x、../x：mint 按所在目录解析
            return self.check_target(by_dir, anchor, relative=True)

        # 裸相对路径：mint 按站点根解析（见本节开头）
        by_root = posixpath.normpath('/' + path)
        if self.target_exists(by_root):
            issues = self.check_target(by_root, anchor, relative=False)
            if not any(new for _, _, new in issues) and not any(lv == 'error' for lv, _, _ in issues):
                new = strip_page_ext(by_root) + ('#' + anchor if anchor else '')
                issues.append(('warn', f'裸相对链接，应改为 {new}', new))
            return issues
        guess = next((new for _, _, new in self.check_target(by_dir, anchor, relative=True) if new), None)
        hint = f'（按所在目录解析应为 {guess}）' if guess else ''
        return [('error', f'裸相对链接 {path} 被 mint 按站点根解析为 {strip_page_ext(by_root)}，该页不存在{hint}', guess)]

    def target_exists(self, path):
        """站内绝对路径（可带 .md 后缀）是否能解析到页面、静态文件或重定向。"""
        target = strip_page_ext(path).rstrip('/') or '/'
        page = target.lstrip('/')
        return target in self.redirects or page_file(page) is not None or (ROOT / page).is_file()

    def check_target(self, path, anchor, relative):
        """校验已解析成站内绝对路径的链接。relative=True 表示原文是按所在目录解析的相对链接（./x）。"""
        suffix = '#' + anchor if anchor else ''
        target = strip_page_ext(path).rstrip('/') or '/'
        if target in self.redirects:
            dest, _, dest_anchor = self.redirects[target].partition('#')
            target, anchor = dest.rstrip('/'), anchor or dest_anchor
            suffix = '#' + anchor if anchor else ''
        page = target.lstrip('/')
        lang, _, sub = page.partition('/')

        if lang not in ('en', 'zh'):  # 静态文件等
            if (ROOT / page).is_file() or page_file(page):
                return []
            return [('error', f'链接目标 {target} 不存在', None)]

        en, zh = 'en/' + sub, 'zh/' + sub
        if relative:
            # 相对链接在英文页里解析到 /en/...：英文页有就改成绝对路径，没有就指回中文页
            if page_file(en):
                return self.anchor_issue(en, anchor) or [
                    ('warn', f'相对链接，应改为 /{en}{suffix}', f'/{en}{suffix}')]
            if page_file(zh):
                if anchor and not self.has_anchor(zh, anchor):
                    return [('error', f'/{en} 不存在；/{zh} 里也没有锚点 #{anchor}', None)]
                return [('error', f'相对链接解析为 /{en}，该页不存在（应改为 /{zh}{suffix}）', f'/{zh}{suffix}')]
            return [('error', f'链接目标 /{en} 不存在（中文页也不存在）', None)]

        if lang == 'en':
            if page_file(en):
                return self.anchor_issue(en, anchor)
            if page_file(zh) and (not anchor or self.has_anchor(zh, anchor)):
                return [('error', f'链接目标 /{en} 不存在（英文页未译，应改为 /{zh}{suffix}）', f'/{zh}{suffix}')]
            return [('error', f'链接目标 /{en} 不存在', None)]

        # /zh/...
        if not page_file(zh):
            return [('error', f'链接目标 /{zh} 不存在', None)]
        problems = self.anchor_issue(zh, anchor)
        if problems:
            return problems
        if page_file(en):
            if not anchor or self.has_anchor(en, anchor):
                return [('warn', f'英文页已存在，应改为 /{en}{suffix}', f'/{en}{suffix}')]
            return [('warn', f'英文页已存在，应改为 /{en}，锚点 #{anchor} 需按英文标题手工改', None)]
        return []

    def anchor_issue(self, page, anchor):
        if anchor and not self.has_anchor(page, anchor):
            return [('error', f'/{page} 里找不到锚点 #{anchor}', None)]
        return []

    def check_image(self, en_page, path):
        if path.startswith('/'):
            # 绝对路径图片缺失只告警、不算硬错误：en 页按 STYLE §10 直接引用 zh 的图片（/zh/**/images/…），
            # 图缺了是中文侧的问题，不该卡住翻译（与「中文更新不能被翻译卡住」同一原则），
            # 实现计划也明确把历史缺图排除在外。注意计划里说的「导航里 130+ 处历史缺图」其实是
            # mint broken-links 对 zh 页裸相对图片（images/x.png）的误报 —— 它按站点根解析，而文件就在
            # 页面旁边；2026-09-29 实测 zh 页 134 处图片引用按所在目录解析全部存在、真缺 0 处。
            if not (ROOT / path.lstrip('/')).is_file():
                return [('warn', f'图片 {path} 不存在', None)]
            return []
        if not path.startswith('.'):
            # 裸相对路径：mint 按站点根解析（见本节开头），根下有这个文件就只是写法问题
            by_root = posixpath.normpath(path)
            if (ROOT / by_root).is_file():
                return [('warn', f'裸相对图片路径，应改为 /{by_root}', f'/{by_root}')]
        en_path = posixpath.normpath(posixpath.join(posixpath.dirname(en_page), path))
        zh_path = 'zh/' + en_path.partition('/')[2]
        if (ROOT / en_path).is_file():
            if path.startswith('.'):
                return [('warn', f'相对图片路径，应改为 /{en_path}', f'/{en_path}')]
            return [('error', f'裸相对图片路径被 mint 按站点根解析、判为断链，应改为 /{en_path}', f'/{en_path}')]
        if (ROOT / zh_path).is_file():
            return [('error', f'相对图片路径在英文页里无效，应改为 /{zh_path}（见 STYLE §10）', f'/{zh_path}')]
        return [('error', f'相对图片路径在英文页里无效，且 /{zh_path} 也不存在', None)]


def run_links(fix=False):
    """校验全部 en 页链接。返回 (错误数, 告警数, 修复数, 输出行)。"""
    checker = LinkChecker()
    errors = warns = fixed = 0
    lines = []
    for en_page in list_en_pages():
        text, issues = checker.check_page(en_page)
        f = page_file(en_page)
        edits = []
        for start, end, line, level, msg, new in issues:
            loc = f'{rel(f)}:{line}'
            if fix and new is not None:  # new 为 '' 表示删除（如多余的 (Chinese)）
                edits.append((start, end, new))
                lines.append(f'  [已修复] {loc}  {msg}')
                fixed += 1
                continue
            tag = '错误' if level == 'error' else '告警'
            hint = '（可 --fix）' if new is not None else ''
            lines.append(f'  [{tag}] {loc}  {msg}{hint}')
            if level == 'error':
                errors += 1
            else:
                warns += 1
        if edits:
            for start, end, new in sorted(set(edits), reverse=True):
                text = text[:start] + new + text[end:]
            f.write_text(text, encoding='utf-8')
    return errors, warns, fixed, lines


def cmd_links(args):
    errors, warns, fixed, lines = run_links(args.fix)
    print('\n'.join(lines) if lines else '  （无问题）')
    print(f'\n合计：错误 {errors}、告警 {warns}' + (f'、已修复 {fixed}' if args.fix else ''))
    if errors:
        sys.exit(1)


# ───────────────────────────── tm-merge ─────────────────────────────

def cmd_tm_merge(args):
    """把 <产品>.missing.json 里已填（非空）的译文合并进 <产品>.en.json，并从 missing 里删掉这些条目。

    为什么要有这一步：sync-server-api.py --tm-missing 每次都会把 missing.json 重置成空值，
    填好的译文没先合并进 .en.json 就重跑，等于白填。
    """
    tm_dir = ROOT / 'i18n' / 'server-api'
    for prod in args.products or list(SERVER_API_PRODUCTS):
        miss_path, tm_path = tm_dir / f'{prod}.missing.json', tm_dir / f'{prod}.en.json'
        missing = load_json(miss_path)
        if missing is None:
            print(f'{prod}：没有 {rel(miss_path)}，跳过（先运行 python3 scripts/sync-server-api.py --tm-missing {prod}）')
            continue
        if not isinstance(missing, dict):
            die(f'{rel(miss_path)} 顶层应为对象 {{中文原文: 英文}}')
        tm = load_json(tm_path, OrderedDict())
        if not isinstance(tm, dict):
            die(f'{rel(tm_path)} 顶层应为对象 {{中文原文: 英文}}')
        # 只合并填了译文的条目：空串 / 纯空白等于没译，留在 missing 里
        filled = {k: v for k, v in missing.items() if isinstance(v, str) and v.strip()}
        tm.update(filled)
        rest = OrderedDict((k, v) for k, v in missing.items() if k not in filled)
        tm_path.write_text(dump_json(tm, sort_keys=True), encoding='utf-8')
        miss_path.write_text(dump_json(rest, sort_keys=True), encoding='utf-8')
        print(f'{prod}：合并 {len(filled)} 条进 {rel(tm_path)}（现 {len(tm)} 条），missing 剩 {len(rest)} 条')
    print('下一步：python3 scripts/sync-server-api.py')


# ───────────────────────────── 生成页标题重名 ─────────────────────────────

def generated_heading_problems():
    """en 生成页里同页 ## 标题（即接口名）的锚点撞车（硬错误）。

    两个接口名译成同一英文时，mint 会给后一个锚点加 -2 后缀，手写页里指向它的锚点就指错了接口，
    而 links / mint broken-links 都看不出来（锚点本身存在）。按 slug 比而不是按原文比：
    大小写、标点不同但 slug 相同的也会撞。
    """
    errs = []
    for en_page in list_en_pages():
        if not is_generated(en_page):
            continue
        f = page_file(en_page)
        seen = OrderedDict()  # slug → [标题原文]
        for line in mask_blocks(f.read_text(encoding='utf-8')).split('\n'):
            m = re.match(r'^##[ \t]+(.*?)[ \t]*$', line)
            if not m:
                continue
            title = heading_text(re.sub(r'(?:^|[ \t]+)#+$', '', m.group(1)))
            seen.setdefault(clean_heading_id(mintlify_slug(title)), []).append(title)
        for slug, titles in seen.items():
            if len(titles) > 1:
                errs.append(f'{rel(f)}：{len(titles)} 个 ## 标题锚点相同（#{slug}：{" / ".join(titles)}），'
                            '两个接口名译成了同一英文 —— 改 i18n/server-api/*.en.json 里的译名后重跑 sync')
    return errs


# ───────────────────────────── check ─────────────────────────────

def cmd_check(args):
    errors = [f'[错误] {e}' for e in nav_problems() + lock_problems(load_lock()) + generated_heading_problems()]
    warnings = []

    _, _, _, link_lines = run_links(fix=False)
    errors += [x.strip() for x in link_lines if x.strip().startswith('[错误]')]
    warnings += [x.strip() for x in link_lines if x.strip().startswith('[告警]')]

    issues, gen_stats = collect_status()
    for w in tm_fallback_warnings(gen_stats):
        warnings.append(f'[翻译记忆缺失] {w}')
    for page, note in issues['stale']:
        warnings.append(f'[过期] {page}  {note}')
    for page, _ in issues['unreviewed']:
        warnings.append(f'[未审校] {page}')
    for page, note in issues['unlocked']:
        warnings.append(f'[未登记] {page}  {note}')
    for page, note in issues['orphan']:
        warnings.append(f'[孤儿] {page}  {note}')
    for page, note in issues['unscoped']:
        warnings.append(f'[未纳入范围] {page}  {note}')

    for w in warnings:
        print(w)
    for e in errors:
        print(e, file=sys.stderr)
    print(f'i18n check：错误 {len(errors)}、告警 {len(warnings)}')
    if errors:
        sys.exit(1)


# ───────────────────────────── main ─────────────────────────────

def main(argv=None):
    global ROOT
    ap = argparse.ArgumentParser(description='英文版导航 / 版本登记 / 链接校验')
    ap.add_argument('--root', help='仓库根目录（默认本脚本所在仓库，也可用环境变量 I18N_ROOT）')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('nav', help='由 zh 导航推导 en 导航并写回 docs.json')
    p.add_argument('--check', action='store_true', help='只比较不写入，不一致退出 1')
    p.set_defaults(func=cmd_nav)

    p = sub.add_parser('lock', help='登记英文页对应的中文版本')
    p.add_argument('pages', nargs='+', help='en 或 zh 页路径，如 en/rtc/overview、zh/rtc/overview.md')
    g = p.add_mutually_exclusive_group()
    g.add_argument('--reviewed', action='store_true', help='同时标记为已审校')
    g.add_argument('--keep-reviewed', action='store_true',
                   help='中文未变（zh_blob 相同）时保留原审校状态；默认重 lock 会把 reviewed 重置为 false')
    p.add_argument('--synced', action='store_true',
                   help='声明已按 git diff 把中文的变化同步进英文；已登记页的中文变过时必须带上，否则拒绝登记')
    p.set_defaults(func=cmd_lock)

    p = sub.add_parser('status', help='缺译 / 过期 / 孤儿 / 未登记 / 未审校 / 未纳入范围')
    p.add_argument('--batch', help='只看某个批次，如 P1a（见 i18n/scope.json）')
    p.set_defaults(func=cmd_status)

    p = sub.add_parser('links', help='校验 en 页链接、锚点与图片')
    p.add_argument('--fix', action='store_true', help='自动改写可确定的链接')
    p.set_defaults(func=cmd_links)

    p = sub.add_parser('tm-merge', help='把 missing.json 里已填的译文合并进服务端 API 翻译记忆表')
    p.add_argument('products', nargs='*', choices=list(SERVER_API_PRODUCTS), metavar='product',
                   help='rtc / meeting，不填表示全部')
    p.set_defaults(func=cmd_tm_merge)

    p = sub.add_parser('check', help='CI：只对硬错误退出 1')
    p.set_defaults(func=cmd_check)

    args = ap.parse_args(argv)
    root = args.root or os.environ.get('I18N_ROOT')
    if root:
        ROOT = Path(root).resolve()
    if not (ROOT / 'docs.json').is_file():
        die(f'{ROOT} 下没有 docs.json：--root / I18N_ROOT 应指向文档仓库根目录')
    args.func(args)


if __name__ == '__main__':
    main()
