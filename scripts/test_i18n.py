#!/usr/bin/env python3
"""scripts/i18n.py 的单测（纯标准库 unittest）。

每个用例在临时目录里造一个最小文档仓（docs.json、nav.en.json、scope.json、zh/en 页、git 提交），
通过 I18N_ROOT 指向它跑真实命令行，覆盖 nav / lock / status / links / tm-merge / check 的正常与异常路径。
slug 规则另有直接调用函数的用例，期望值取自 mint CLI 自带的 @mintlify/common 实跑结果。

用法：
    python3 scripts/test_i18n.py
    python3 -m unittest scripts/test_i18n.py -v
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / 'i18n.py'
sys.path.insert(0, str(SCRIPT.parent))
import i18n  # noqa: E402

# 最小导航：两个 tab、嵌套子 group、一个服务端 API 生成页、一个不纳入范围的鸿蒙组
DOCS_JSON = {
    '$schema': 'https://mintlify.com/docs.json',
    'name': 'STMLink Docs',
    'navigation': {'languages': [{'language': 'zh', 'tabs': [
        {'tab': 'SRTC 音视频 SDK', 'groups': [
            {'group': '概览', 'pages': ['zh/rtc/overview', 'zh/choose']},
            {'group': 'Web SDK', 'pages': [
                'zh/rtc/web/integration',
                {'group': '进阶实践', 'pages': ['zh/rtc/web/advanced/multi']},
                {'group': '接口文档', 'pages': ['zh/rtc/web/api-reference/SRTC']},
                'zh/rtc/web/changelog',
            ]},
            {'group': '服务端 API', 'pages': ['zh/rtc/server-api/overview', 'zh/rtc/server-api/channel']},
        ]},
        {'tab': 'SMeeting 会议 SDK', 'groups': [
            {'group': '概览', 'pages': ['zh/meeting/overview', 'zh/choose']},
            {'group': 'HarmonyOS SDK', 'pages': ['zh/meeting/harmony/integration']},
        ]},
    ]}]},
    'redirects': [{'source': '/zh/rtc/old', 'destination': '/zh/rtc/overview'}],
}

# 故意不给「HarmonyOS SDK」译名：只有它出现在 en 导航里时才该报缺译
NAV_EN = {
    'tabs': {'SRTC 音视频 SDK': 'SRTC Audio & Video SDK', 'SMeeting 会议 SDK': 'SMeeting Conferencing SDK'},
    'groups': {'概览': 'Overview', 'Web SDK': 'Web SDK', '进阶实践': 'Advanced',
               '接口文档': 'API reference', '服务端 API': 'Server API'},
    'footer': {'links': [{'header': 'Products', 'items': [{'label': 'Website', 'href': 'https://www.stmlink.com/en/'}]}]},
}

SCOPE = {
    'excluded_prefixes': ['zh/meeting/harmony/'],
    'batches': [
        {'name': 'P1a', 'pages': ['zh/rtc/overview', 'zh/choose', 'zh/meeting/overview'],
         'prefixes': ['zh/rtc/server-api/']},
        {'name': 'P1b', 'pages': ['zh/rtc/web/integration'], 'prefixes': []},
        {'name': 'P2', 'pages': [], 'prefixes': ['zh/rtc/web/']},
    ],
}

ZH_OVERVIEW = """---
title: "SRTC 概览"
description: "产品架构与入门"
---

## 产品架构

![架构](images/arch.png)

## 快速开始（Web）

### `join()` 方法

## FAQ

## FAQ

```bash
## 代码块里的不是标题
```
"""

EN_OVERVIEW = """---
title: "SRTC overview"
description: "Architecture and getting started"
---

## Product architecture

## Quick start (Web)

## FAQ

## FAQ
"""

GENERATED = '{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。 */}\n\n## 创建频道\n'
GENERATED_EN = ('{/* This page is auto-generated from the backend source. Do not edit by hand. */}\n\n'
                '## Create a channel\n\n## Destroy a channel\n')


class Fixture(unittest.TestCase):
    """每个用例一个临时仓库。"""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.write('docs.json', json.dumps(DOCS_JSON, indent=2, ensure_ascii=False) + '\n')
        self.write('i18n/nav.en.json', json.dumps(NAV_EN, ensure_ascii=False))
        self.write('i18n/scope.json', json.dumps(SCOPE, ensure_ascii=False))
        self.write('zh/rtc/overview.md', ZH_OVERVIEW)
        self.write('zh/rtc/images/arch.png', 'png')
        self.write('zh/choose.md', '## 怎么选\n')
        self.write('zh/rtc/web/integration.md', '## 安装\n')
        self.write('zh/rtc/web/advanced/multi.md', '## 多频道\n')
        self.write('zh/rtc/web/api-reference/SRTC.md', '## SRTC\n')
        self.write('zh/rtc/web/changelog.mdx', '## 1.0.0\n')
        self.write('zh/rtc/server-api/overview.md', '## 签名\n')
        self.write('zh/rtc/server-api/channel.md', GENERATED)
        self.write('zh/meeting/overview.md', '## 会议概览\n')
        self.write('zh/meeting/harmony/integration.md', '## 集成\n')
        self.write('en/.gitkeep', '')
        self.git('init', '-q')
        self.git('config', 'user.email', 't@example.com')
        self.git('config', 'user.name', 't')
        self.commit('init')

    def tearDown(self):
        self._tmp.cleanup()

    # ── 工具 ──

    def write(self, path, text):
        f = self.root / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding='utf-8')

    def read(self, path):
        return (self.root / path).read_text(encoding='utf-8')

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], capture_output=True, text=True,
                              check=True).stdout.strip()

    def commit(self, msg):
        self.git('add', '-A')
        self.git('commit', '-q', '-m', msg)

    def run_cli(self, *args):
        env = dict(os.environ, I18N_ROOT=str(self.root))
        r = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=env)
        return r.returncode, r.stdout, r.stderr

    def docs(self):
        return json.loads(self.read('docs.json'))

    def en_lang(self):
        langs = self.docs()['navigation']['languages']
        return next((x for x in langs if x['language'] == 'en'), None)


# ───────────────────────────── slug ─────────────────────────────

class SlugTest(unittest.TestCase):
    # [标题, mint 原始 slug, cleanHeadingId 后] —— 同一计数器顺序调用，期望值由 @mintlify/common 实跑得到
    VECTORS = [
        ['Get a channel token', 'get-a-channel-token', 'get-a-channel-token'],
        ['新增设备', '%E6%96%B0%E5%A2%9E%E8%AE%BE%E5%A4%87', '新增设备'],
        ['新增设备', '%E6%96%B0%E5%A2%9E%E8%AE%BE%E5%A4%87-2', '新增设备-2'],
        ['`join()` 方法', '%60join-%60-%E6%96%B9%E6%B3%95', '`join-`-方法'],
        ['a/b & c', 'a%2Fb-%26-c', 'a/b-&-c'],
        ["It's ok", 'its-ok', 'its-ok'],
        ['It’s ok', 'it%E2%80%99s-ok', 'it’s-ok'],
        ['v1.2 版本', 'v1-2-%E7%89%88%E6%9C%AC', 'v1-2-版本'],
        ['SDK (iOS/macOS)', 'sdk-ios%2Fmacos', 'sdk-ios/macos'],
        ['join()', 'join', 'join'],
        ['Hello.World', 'hello-world', 'hello-world'],
        ['A & B', 'a-%26-b', 'a-&-b'],
        ['x', 'x', 'x'],
        ['x', 'x-2', 'x-2'],
        ['x-2', 'x-2', 'x-2'],
        ['步骤 1：安装', '%E6%AD%A5%E9%AA%A4-1%EF%BC%9A%E5%AE%89%E8%A3%85', '步骤-1：安装'],
        ['FAQ？', 'faq%EF%BC%9F', 'faq？'],
        ['😀 emoji', '%F0%9F%98%80-emoji', '-emoji'],
        ["don't", 'dont', 'dont'],
        ['JoinChannel', 'joinchannel', 'joinchannel'],
        ['  spaced   out  ', 'spaced-out', 'spaced-out'],
        ['C++ SDK', 'c%2B%2B-sdk', 'c++-sdk'],
        ['Q: what?', 'q%3A-what%3F', 'q-what'],
        ['100% ok', '100%25-ok', '100%-ok'],
        ['a_b', 'a_b', 'a_b'],
        ['已知问题 [2]', '%E5%B7%B2%E7%9F%A5%E9%97%AE%E9%A2%98-%5B2%5D', '已知问题-2'],
    ]

    def test_vectors_match_mintlify(self):
        counter = i18n.SlugCounter()
        for title, raw, cleaned in self.VECTORS:
            with self.subTest(title=title):
                slug = i18n.mintlify_slug(title, counter)
                self.assertEqual(slug, raw)
                self.assertEqual(i18n.clean_heading_id(slug), cleaned)

    def test_counter_third_duplicate(self):
        c = i18n.SlugCounter()
        self.assertEqual([i18n.mintlify_slug('FAQ', c) for _ in range(3)], ['faq', 'faq-2', 'faq-3'])

    def test_heading_text(self):
        self.assertEqual(i18n.heading_text('`join()` 方法'), 'join() 方法')
        self.assertEqual(i18n.heading_text('**加粗** 与 [链接](/zh/x)'), '加粗 与 链接')
        self.assertEqual(i18n.heading_text(r'RTCValueResultListener\<T\>'), 'RTCValueResultListener<T>')
        self.assertEqual(i18n.heading_text('`on_join` 与 _强调_'), 'on_join 与 强调')

    def test_page_anchors(self):
        text = '\n'.join([
            '---', 'title: "## 不是标题"', '---',
            '## 新增设备', '## 新增设备', '### `join()` 方法', '##### 五级标题不生成 id',
            '```md', '## 代码块里', '```',
            '#### ', '## [1.0.0] - 2026.09.07',
            '<ParamField body="appId" type="string">', '<ParamField body="appId" type="string">',
            '<Tab title="网页端">', '<Accordion title="How it works">', '<Update label="v1.0.0">',
            '<Note id="note-id">', '<div id="custom-id">',
        ])
        ids = i18n.page_anchors(text)
        # 标题里的行内代码只取其值（不带反引号），所以是 join-方法，不同于字面量 '`join()` 方法'
        for want in ['新增设备', '新增设备-2', 'join-方法', '', '1-0-0-2026-09-07', 'param-app-id',
                     'param-app-id-1', '%E7%BD%91%E9%A1%B5%E7%AB%AF', 'how-it-works', 'v1-0-0', 'custom-id']:
            self.assertIn(want, ids)
        for unwanted in ['五级标题不生成-id', '代码块里', '不是标题', 'note-id']:
            self.assertNotIn(unwanted, ids)

    def test_extract_links_skips_code(self):
        text = ('[a](/en/x)\n`[b](/en/inline)`\n```md\n[c](/en/fenced)\n```\n'
                '<Card href="/zh/card">\n![img](images/a.png "title")\n[ref]: /en/refdef\n')
        links = i18n.extract_links(text)
        self.assertEqual(sorted(x.url for x in links), ['/en/refdef', '/en/x', '/zh/card', 'images/a.png'])
        self.assertEqual([x.url for x in links if x.is_image], ['images/a.png'])
        self.assertEqual({x.url: x.kind for x in links},
                         {'/en/x': 'md', '/zh/card': 'tag', 'images/a.png': 'md', '/en/refdef': 'ref'})
        md = next(x for x in links if x.url == '/en/x')
        self.assertEqual((md.label, text[md.tail - 1]), ('a', ')'))

    def test_extract_links_label_keeps_inline_code(self):
        # 屏蔽行内代码只用于定位，label 取原文，这样才能认出「链接文字是代码」
        link = i18n.extract_links('[`join()`](/zh/x) (Chinese)\n')[0]
        self.assertEqual(link.label, '`join()`')

    def test_inline_components_have_no_id(self):
        # 同行夹带文字的标签在 mint 里是行内元素（mdxJsxTextElement），不生成 id；期望值由 mint 的 coreRemark 实测
        text = '\n'.join([
            '<Tabs>',
            '<Tab title="Inline">x</Tab>',
            '<Tab title="Empty"></Tab>',
            '<Tab title="Self" />',
            '<Tab title="Block">', 'x', '</Tab>',
            '<Tab', '  title="Multi">', 'x', '</Tab>',
            '<Tab title="I1" /> <Tab title="I2" />',
            '+ <Tab title="Listed">', '  x', '  </Tab>',
            '> <Tab title="Quoted">', '> x', '> </Tab>',
            '<Tab title="Commented">{/* c */}', 'x', '</Tab>',
            '</Tabs>',
            'text <Tab title="AfterText">x</Tab>',
            '<Accordion title="Inline acc">x</Accordion>',
            '<ParamField body="inlineParam">x</ParamField>',
            '<div id="inline-id">x</div>',
            '<Accordion title="Block acc">', 'x', '</Accordion>',
        ])
        ids = i18n.page_anchors(text)
        for want in ['empty', 'self', 'block', 'multi', 'i1', 'i2', 'listed', 'quoted', 'commented', 'block-acc']:
            self.assertIn(want, ids)
        for unwanted in ['inline', 'aftertext', 'inline-acc', 'param-inline-param', 'inline-id']:
            self.assertNotIn(unwanted, ids)


# ───────────────────────────── nav ─────────────────────────────

class NavTest(Fixture):
    def test_empty_en_is_consistent(self):
        rc, out, _ = self.run_cli('nav', '--check')
        self.assertEqual(rc, 0, out)
        rc, out, _ = self.run_cli('nav')
        self.assertIn('无变化', out)
        self.assertIsNone(self.en_lang())

    def test_generate_and_prune(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        self.write('en/rtc/web/advanced/multi.md', '## Multi-channel\n')
        self.write('en/rtc/web/changelog.mdx', '## 1.0.0\n')
        rc, out, err = self.run_cli('nav', '--check')
        self.assertEqual(rc, 1, out + err)

        rc, out, err = self.run_cli('nav')
        self.assertEqual(rc, 0, err)
        langs = self.docs()['navigation']['languages']
        self.assertEqual([x['language'] for x in langs], ['zh', 'en'])
        self.assertEqual(langs[0], DOCS_JSON['navigation']['languages'][0])  # zh 原样
        en = langs[1]
        self.assertEqual(en['footer'], NAV_EN['footer'])
        self.assertEqual(len(en['tabs']), 1)  # SMeeting 一个英文页都没有 → 整个 tab 剔除
        tab = en['tabs'][0]
        self.assertEqual(tab['tab'], 'SRTC Audio & Video SDK')
        self.assertEqual(tab['groups'], [
            {'group': 'Overview', 'pages': ['en/rtc/overview']},
            {'group': 'Web SDK', 'pages': [
                {'group': 'Advanced', 'pages': ['en/rtc/web/advanced/multi']},
                'en/rtc/web/changelog',
            ]},
        ])
        text = self.read('docs.json')
        self.assertTrue(text.endswith('}\n'))
        self.assertIn('"SRTC 音视频 SDK"', text)  # 中文不转义
        self.assertIn('\n  "navigation"', text)  # 2 空格缩进、键序不变
        self.assertLess(text.index('"name"'), text.index('"navigation"'))
        self.assertEqual(self.run_cli('nav', '--check')[0], 0)

    def test_remove_en_when_last_page_deleted(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        self.run_cli('nav')
        self.assertIsNotNone(self.en_lang())
        (self.root / 'en/rtc/overview.md').unlink()
        self.assertEqual(self.run_cli('nav', '--check')[0], 1)
        self.run_cli('nav')
        self.assertIsNone(self.en_lang())

    def test_missing_title_blocks_write(self):
        self.write('en/meeting/harmony/integration.md', '## Integration\n')
        before = self.read('docs.json')
        rc, _, err = self.run_cli('nav')
        self.assertEqual(rc, 1)
        self.assertIn('groups: HarmonyOS SDK', err)
        self.assertNotIn('概览', err)  # 只报缺的
        self.assertEqual(self.read('docs.json'), before)

    def test_tab_level_pages(self):
        # tab 直接挂 pages（没有 groups）的写法也要推导，缺译标题同样拦住
        cfg = json.loads(self.read('docs.json'))
        cfg['navigation']['languages'][0]['tabs'].append({'tab': 'AI', 'pages': ['zh/ai', 'zh/ai-faq']})
        self.write('docs.json', json.dumps(cfg, indent=2, ensure_ascii=False) + '\n')
        self.write('zh/ai.md', '## AI\n')
        self.write('zh/ai-faq.md', '## 问答\n')
        self.write('en/ai.md', '## AI\n')
        rc, _, err = self.run_cli('nav')
        self.assertEqual(rc, 1)
        self.assertIn('tabs: AI', err)
        titles = json.loads(self.read('i18n/nav.en.json'))
        titles['tabs']['AI'] = 'AI'
        self.write('i18n/nav.en.json', json.dumps(titles, ensure_ascii=False))
        rc, _, err = self.run_cli('nav')
        self.assertEqual(rc, 0, err)
        self.assertEqual(self.en_lang()['tabs'], [{'tab': 'AI', 'pages': ['en/ai']}])

    def test_stale_en_item_replaced_and_repositioned(self):
        cfg = json.loads(self.read('docs.json'))
        cfg['navigation']['languages'].insert(0, {'language': 'en', 'tabs': [{'tab': 'old', 'groups': []}]})
        self.write('docs.json', json.dumps(cfg, indent=2, ensure_ascii=False) + '\n')
        self.write('en/choose.md', '## How to choose\n')
        self.run_cli('nav')
        langs = self.docs()['navigation']['languages']
        self.assertEqual([x['language'] for x in langs], ['zh', 'en'])
        self.assertEqual([t['tab'] for t in langs[1]['tabs']],
                         ['SRTC Audio & Video SDK', 'SMeeting Conferencing SDK'])


# ───────────────────────────── lock ─────────────────────────────

class LockTest(Fixture):
    def test_keep_reviewed(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        self.run_cli('lock', 'en/rtc/overview', '--reviewed')
        # 默认重 lock：reviewed 被重置
        self.run_cli('lock', 'en/rtc/overview')
        self.assertIs(self.lock()['en/rtc/overview']['reviewed'], False)
        # 中文未变 + --keep-reviewed：保留已审校
        self.run_cli('lock', 'en/rtc/overview', '--reviewed')
        rc, out, err = self.run_cli('lock', 'en/rtc/overview', '--keep-reviewed')
        self.assertEqual(rc, 0, err)
        self.assertIn('（已审校）', out)
        self.assertIs(self.lock()['en/rtc/overview']['reviewed'], True)
        # 中文变了：--keep-reviewed 也要重置，并更新 zh_blob
        self.write('zh/rtc/overview.md', ZH_OVERVIEW + '\n## 新增\n')
        self.commit('zh 更新')
        # 中文变了但没声明 --synced：拒绝登记，保留过期状态（避免只改了链接就把过期页标成最新）
        rc, _, err = self.run_cli('lock', 'en/rtc/overview', '--keep-reviewed')
        self.assertEqual(rc, 1)
        self.assertIn('--synced', err)
        self.run_cli('lock', 'en/rtc/overview', '--keep-reviewed', '--synced')
        e = self.lock()['en/rtc/overview']
        self.assertIs(e['reviewed'], False)
        self.assertEqual(e['zh_blob'], self.git('hash-object', 'zh/rtc/overview.md'))
        # 从未审校过的页：--keep-reviewed 保持 false
        self.write('en/choose.md', '## How to choose\n')
        self.run_cli('lock', 'en/choose', '--keep-reviewed')
        self.assertIs(self.lock()['en/choose']['reviewed'], False)
        # 两个选项互斥
        rc, _, _ = self.run_cli('lock', 'en/choose', '--reviewed', '--keep-reviewed')
        self.assertEqual(rc, 2)

    def lock(self):
        return json.loads(self.read('i18n/en.lock.json'))

    def test_lock_records_blob_and_commit(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        self.write('en/choose.md', '## How to choose\n')
        rc, out, err = self.run_cli('lock', 'en/rtc/overview', 'zh/choose.md')
        self.assertEqual(rc, 0, err)
        data = self.lock()
        self.assertEqual(list(data), ['en/choose', 'en/rtc/overview'])
        e = data['en/rtc/overview']
        self.assertEqual(e['source'], 'zh/rtc/overview.md')
        self.assertEqual(e['zh_blob'], self.git('hash-object', 'zh/rtc/overview.md'))
        self.assertEqual(e['zh_commit'], self.git('log', '-1', '--format=%H', '--', 'zh/rtc/overview.md'))
        self.assertIs(e['reviewed'], False)
        text = self.read('i18n/en.lock.json')
        self.assertTrue(text.startswith('{\n  "en/choose"'))
        self.assertLess(text.index('"reviewed"'), text.index('"source"'))  # 键排序

    def test_reviewed_flag(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        self.run_cli('lock', 'en/rtc/overview')
        rc, _, err = self.run_cli('lock', '/en/rtc/overview.md', '--reviewed')
        self.assertEqual(rc, 0, err)
        self.assertIs(self.lock()['en/rtc/overview']['reviewed'], True)

    def test_reviewed_refused_when_zh_changed(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        self.run_cli('lock', 'en/rtc/overview')
        self.write('zh/rtc/overview.md', ZH_OVERVIEW + '\n## 新增一节\n')
        self.commit('zh 更新')
        rc, _, err = self.run_cli('lock', 'en/rtc/overview', '--reviewed')
        self.assertEqual(rc, 1)
        self.assertIn('增量翻译', err)

    def test_uncommitted_zh_refused(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        self.write('zh/rtc/overview.md', ZH_OVERVIEW + '改了没提交\n')
        rc, _, err = self.run_cli('lock', 'en/rtc/overview')
        self.assertEqual(rc, 1)
        self.assertIn('未提交', err)
        self.assertFalse((self.root / 'i18n/en.lock.json').exists())

    def test_missing_en_or_zh_refused(self):
        rc, _, err = self.run_cli('lock', 'en/rtc/overview')
        self.assertEqual(rc, 1)
        self.assertIn('en/rtc/overview 不存在', err)
        self.write('en/rtc/nozh.md', '## x\n')
        rc, _, err = self.run_cli('lock', 'en/rtc/nozh')
        self.assertEqual(rc, 1)
        self.assertIn('zh/rtc/nozh 不存在', err)
        rc, _, err = self.run_cli('lock', 'fr/rtc/overview')
        self.assertEqual(rc, 1)

    def test_never_committed_zh_refused(self):
        self.write('zh/rtc/brand-new.md', '## 新页\n')
        self.write('en/rtc/brand-new.md', '## New page\n')
        rc, _, err = self.run_cli('lock', 'en/rtc/brand-new')
        self.assertEqual(rc, 1)
        self.assertIn('zh/rtc/brand-new.md 从未提交过', err)
        self.assertFalse((self.root / 'i18n/en.lock.json').exists())

    def test_shallow_clone_refused(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        self.commit('en')
        self.write('zh/choose.md', '## 怎么选（改）\n')
        self.commit('second')
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(['git', 'clone', '-q', '--depth', '1', f'file://{self.root}', d], check=True)
            env = dict(os.environ, I18N_ROOT=d)
            r = subprocess.run([sys.executable, str(SCRIPT), 'lock', 'en/rtc/overview'],
                               capture_output=True, text=True, env=env)
            self.assertEqual(r.returncode, 1)
            self.assertIn('浅克隆', r.stderr)
            self.assertFalse((Path(d) / 'i18n/en.lock.json').exists())

    def test_generated_page_refused(self):
        self.write('en/rtc/server-api/channel.md', GENERATED)
        rc, _, err = self.run_cli('lock', 'en/rtc/server-api/channel')
        self.assertEqual(rc, 1)
        self.assertIn('生成页', err)


# ───────────────────────────── status ─────────────────────────────

class StatusTest(Fixture):
    def lock_commit(self, en_page):
        return json.loads(self.read('i18n/en.lock.json'))[en_page]['zh_commit']

    def test_tm_warning_needs_en_generated_page(self):
        # 缺失 > 0 但还没有 en 生成页：不告警（没有会被误提交的中文回退页）
        self.write('i18n/server-api/rtc.missing.json', json.dumps({'创建频道': ''}))
        rc, out, _ = self.run_cli('status')
        self.assertNotIn('⚠ rtc', out)
        # missing 为空对象：同样不告警
        self.write('en/rtc/server-api/channel.md', GENERATED_EN)
        self.write('i18n/server-api/rtc.missing.json', '{}')
        rc, out, _ = self.run_cli('status')
        self.assertNotIn('⚠ rtc', out)

    def test_empty_en(self):
        rc, out, _ = self.run_cli('status')
        self.assertEqual(rc, 0)
        # 范围内的手写页：rtc/overview、choose、meeting/overview、server-api/overview（P1a），
        # web/integration（P1b），web 下其余 3 页（P2）；鸿蒙不纳入，生成页不算缺译
        self.assertIn('## 缺译（8）', out)
        self.assertIn('### P1a（4）', out)
        self.assertIn('### P2（3）', out)
        self.assertNotIn('harmony', out)
        self.assertNotIn('zh/rtc/server-api/channel  →', out)
        self.assertIn('rtc：生成页 1，英文页缺 1；无翻译记忆表，缺失清单未生成', out)
        self.assertTrue(out.strip().splitlines()[-1].startswith('合计：缺译 8'))

    def test_all_kinds(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW)   # 登记后中文更新 → 过期 + 未审校
        self.write('en/choose.md', '## How to choose\n')  # 登记并审校 → 无问题
        self.write('en/rtc/web/integration.md', '## Install\n')  # 未登记
        self.write('en/rtc/gone.md', '## Gone\n')        # 孤儿
        self.write('en/rtc/server-api/channel.md', GENERATED.replace('由后端源码自动生成', 'auto-generated from the backend source'))
        self.run_cli('lock', 'en/rtc/overview')
        self.run_cli('lock', 'en/choose', '--reviewed')
        self.write('zh/rtc/overview.md', ZH_OVERVIEW + '\n## 新增一节\n\n正文\n')
        self.commit('zh 更新')
        self.write('i18n/server-api/rtc.en.json', json.dumps({'创建频道': 'Create a channel', 'a': 'b', 'c': 'd'}))
        self.write('i18n/server-api/rtc.missing.json', json.dumps(['x', 'y']))

        rc, out, _ = self.run_cli('status')
        self.assertEqual(rc, 0)
        commit = self.lock_commit('en/rtc/overview')
        self.assertIn(f'## 过期（1）\n  en/rtc/overview  zh/rtc/overview.md @ {commit[:12]}：1 file changed, 4 insertions(+)', out)
        self.assertEqual(self.git('diff', '--shortstat', commit[:12], '--', 'zh/rtc/overview.md'),
                         '1 file changed, 4 insertions(+)')  # 输出的 12 位前缀可直接用于 git diff
        self.assertIn('## 孤儿（1）\n  en/rtc/gone', out)
        self.assertIn('## 未登记（1）\n  en/rtc/web/integration', out)
        self.assertIn('## 未审校（1）\n  en/rtc/overview', out)
        self.assertIn('rtc：生成页 1，英文页缺 0；翻译记忆 3 条，缺失 2 条', out)
        self.assertIn('⚠ rtc：已有 1 个 en 生成页，但翻译记忆缺失 2 条', out)
        self.assertNotIn('⚠ meeting', out)
        self.assertIn('合计：缺译 5、过期 1、孤儿 1、未登记 1、未审校 1、未纳入范围 0、生成页缺英文 0、翻译记忆缺失 2 条', out)

    def test_batch_filter(self):
        self.write('en/rtc/web/integration.md', '## Install\n')
        rc, out, _ = self.run_cli('status', '--batch', 'P2')
        self.assertIn('## 缺译（3）', out)
        self.assertIn('## 未登记（0）', out)  # web/integration 属于 P1b
        self.assertNotIn('服务端 API 生成页', out)
        rc, out, _ = self.run_cli('status', '--batch', 'P1b')
        self.assertIn('## 缺译（0）', out)
        self.assertIn('## 未登记（1）', out)
        rc, _, err = self.run_cli('status', '--batch', 'P9')
        self.assertEqual(rc, 1)
        self.assertIn('P1a, P1b, P2', err)


    def test_unscoped_pages(self):
        # 导航里新加了一页，但 scope.json 没配：既不在批次也不在排除列表 → 报「未纳入范围」，不算缺译
        cfg = json.loads(self.read('docs.json'))
        cfg['navigation']['languages'][0]['tabs'][0]['groups'][0]['pages'].append('zh/rtc/misc')
        self.write('docs.json', json.dumps(cfg, indent=2, ensure_ascii=False) + '\n')
        self.write('zh/rtc/misc.md', '## 杂项\n')
        rc, out, _ = self.run_cli('status')
        self.assertEqual(rc, 0)
        self.assertIn('## 未纳入范围（1）\n  zh/rtc/misc  不在 i18n/scope.json 的任何批次或排除列表里', out)
        self.assertIn('## 缺译（8）', out)
        self.assertNotIn('meeting/harmony', out)  # 排除列表里的不报
        rc, out, _ = self.run_cli('status', '--batch', 'P1a')
        self.assertIn('## 未纳入范围（0）', out)  # 按批次看时不报
        rc, out, _ = self.run_cli('check')
        self.assertIn('[未纳入范围] zh/rtc/misc', out)

    def test_stale_with_missing_commit_falls_back(self):
        # zh_commit 在本仓不存在（如被 rebase 掉）：仍判过期，说明里提示无法取增量
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        self.write('i18n/en.lock.json', json.dumps({'en/rtc/overview': {
            'source': 'zh/rtc/overview.md', 'zh_blob': 'x' * 40, 'zh_commit': 'f' * 40, 'reviewed': True}}))
        rc, out, _ = self.run_cli('status')
        self.assertEqual(rc, 0)
        self.assertIn(f'## 过期（1）\n  en/rtc/overview  zh/rtc/overview.md @ {"f" * 12}：（该提交在本仓不存在，无法取增量）', out)


# ───────────────────────────── links ─────────────────────────────

EN_WITH_LINKS = """---
title: "Links"
---

## Get a channel token

[ok](/en/rtc/overview#product-architecture)
[self](#get-a-channel-token)
[zh only](/zh/rtc/web/integration#安装)
[broken en](/en/rtc/nope)
[untranslated](/en/rtc/web/advanced/multi)
[to en](/zh/rtc/overview)
[to en keep anchor](/zh/rtc/overview#faq-2)
[anchor by hand](/zh/rtc/overview#产品架构)
[bad self](#missing-anchor)
[bad zh anchor](/zh/rtc/overview#不存在)
[relative missing](web/integration)
[relative ok](./overview.md#faq-2)
[redirect](/zh/rtc/old)
[external](https://example.com/a#b)
![](images/arch.png)
<Card title="x" href="/zh/rtc/overview">card</Card>
<a href="/en/rtc/overview#不存在">a</a>
`[inline](/en/inline-nope)`

```md
[fenced](/en/fenced-nope)
```
"""


class LinksTest(Fixture):
    def setUp(self):
        super().setUp()
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        self.write('en/rtc/links.md', EN_WITH_LINKS)

    def test_empty_en(self):
        for p in ('en/rtc/overview.md', 'en/rtc/links.md'):
            (self.root / p).unlink()
        rc, out, _ = self.run_cli('links')
        self.assertEqual(rc, 0)
        self.assertIn('错误 0、告警 0', out)

    def test_report(self):
        rc, out, _ = self.run_cli('links')
        self.assertEqual(rc, 1)
        lines = [x for x in out.splitlines() if 'en/rtc/links.md' in x]

        def line_of(n):
            return next(x for x in lines if f'links.md:{n} ' in x)

        # 行号对应 EN_WITH_LINKS（frontmatter 占 3 行，第 5 行是标题）
        self.assertIn('[错误]', line_of(10))
        self.assertIn('/en/rtc/nope 不存在', line_of(10))
        self.assertIn('改为 /zh/rtc/web/advanced/multi）（可 --fix）', line_of(11))
        self.assertIn('[告警]', line_of(12))
        self.assertIn('应改为 /en/rtc/overview（可 --fix）', line_of(12))
        self.assertIn('应改为 /en/rtc/overview#faq-2（可 --fix）', line_of(13))
        self.assertIn('锚点 #产品架构 需按英文标题手工改', line_of(14))
        self.assertIn('本页找不到锚点 #missing-anchor', line_of(15))
        self.assertIn('/zh/rtc/overview 里找不到锚点 #不存在', line_of(16))
        self.assertIn('裸相对链接 web/integration 被 mint 按站点根解析为 /web/integration，该页不存在'
                      '（按所在目录解析应为 /zh/rtc/web/integration）（可 --fix）', line_of(17))
        self.assertIn('相对链接，应改为 /en/rtc/overview#faq-2', line_of(18))
        self.assertIn('应改为 /en/rtc/overview（可 --fix）', line_of(19))  # 重定向到 zh/rtc/overview
        self.assertIn('应改为 /zh/rtc/images/arch.png', line_of(21))
        self.assertIn('应改为 /en/rtc/overview', line_of(22))  # <Card href>
        self.assertIn('/en/rtc/overview 里找不到锚点 #不存在', line_of(23))
        for n in (7, 8, 20, 24, 27):  # 合法链接、外链、行内代码与代码块里的链接都不报
            self.assertFalse(any(f'links.md:{n} ' in x for x in lines), n)
        # 改写后仍指向未译中文页的 markdown 链接要加 (Chinese)；英文页已存在的 /zh 链接（:12 :14）与 <Card>（:22）不加
        suffix = [n for n in range(1, 30)
                  if any(f'links.md:{n} ' in x and '"(Chinese)"' in x for x in lines)]
        self.assertEqual(suffix, [9, 11, 17])
        self.assertIn('合计：错误 7、告警 9', out)

    def test_fix(self):
        rc, out, _ = self.run_cli('links', '--fix')
        self.assertEqual(rc, 1)  # 不能自动修的错误仍在
        text = self.read('en/rtc/links.md')
        for want in ['[zh only](/zh/rtc/web/integration#安装) (Chinese)\n',
                     '[untranslated](/zh/rtc/web/advanced/multi) (Chinese)\n', '[to en](/en/rtc/overview)\n',
                     '[to en keep anchor](/en/rtc/overview#faq-2)', '[relative missing](/zh/rtc/web/integration) (Chinese)',
                     '[relative ok](/en/rtc/overview#faq-2)', '[redirect](/en/rtc/overview)',
                     '![](/zh/rtc/images/arch.png)', '<Card title="x" href="/en/rtc/overview">']:
            self.assertIn(want, text)
        for unchanged in ['[anchor by hand](/zh/rtc/overview#产品架构)', '[broken en](/en/rtc/nope)',
                          '`[inline](/en/inline-nope)`', '[fenced](/en/fenced-nope)']:
            self.assertIn(unchanged, text)
        self.assertEqual(text.count('(Chinese)'), 3)
        rc, out, _ = self.run_cli('links')
        self.assertIn('合计：错误 4、告警 1', out)  # 剩 :10 :15 :16 :23 与手工改锚点的告警
        self.run_cli('links', '--fix')
        self.assertEqual(self.read('en/rtc/links.md'), text)  # 再跑一次 --fix 不重复加后缀

    def test_relative_image_with_en_copy(self):
        self.write('en/rtc/images/arch.png', 'png')
        self.write('en/rtc/links.md', '![](./images/arch.png)\n![](/zh/rtc/images/none.png)\n')
        rc, out, _ = self.run_cli('links')
        self.assertEqual(rc, 0)  # ./ 相对路径 mint 按所在目录解析，只是写法告警；绝对路径缺图也只告警
        self.assertIn('相对图片路径，应改为 /en/rtc/images/arch.png', out)
        self.assertIn('图片 /zh/rtc/images/none.png 不存在', out)

    def test_bare_relative_image(self):
        # 裸相对图片 mint 按站点根解析：根下没有就是断链，即使页面旁边有这个文件
        self.write('en/rtc/images/arch.png', 'png')
        self.write('en/rtc/links.md', '![](images/arch.png)\n![](zh/rtc/images/arch.png)\n')
        rc, out, _ = self.run_cli('links')
        self.assertEqual(rc, 1)
        self.assertIn('links.md:1  裸相对图片路径被 mint 按站点根解析、判为断链，应改为 /en/rtc/images/arch.png', out)
        self.assertIn('[告警] en/rtc/links.md:2  裸相对图片路径，应改为 /zh/rtc/images/arch.png', out)
        self.run_cli('links', '--fix')
        self.assertEqual(self.read('en/rtc/links.md'), '![](/en/rtc/images/arch.png)\n![](/zh/rtc/images/arch.png)\n')

    def test_bare_relative_links_resolve_from_root(self):
        self.write('en/rtc/links.md', '\n'.join([
            '[a](overview#faq-2)',          # 根下 /overview 不存在 → 错误，按目录推断为 /en/rtc/overview
            '[b](zh/rtc/web/integration)',  # 根下存在（中文页）→ 告警改绝对路径，且要加 (Chinese)
            '[c](zh/rtc/overview#faq)',     # 根下存在、英文页也在 → 改成 /en
            '[d](nothing/here)',            # 哪都解析不到 → 错误、不可修
            '[e](zh/rtc/overview#不存在)',   # 根下存在但锚点错 → 错误
            '',
        ]))
        rc, out, _ = self.run_cli('links')
        self.assertEqual(rc, 1)
        self.assertIn('links.md:1  裸相对链接 overview 被 mint 按站点根解析为 /overview，该页不存在'
                      '（按所在目录解析应为 /en/rtc/overview#faq-2）（可 --fix）', out)
        self.assertIn('[告警] en/rtc/links.md:2  裸相对链接，应改为 /zh/rtc/web/integration（可 --fix）', out)
        self.assertIn('[告警] en/rtc/links.md:3  英文页已存在，应改为 /en/rtc/overview#faq（可 --fix）', out)
        self.assertIn('[错误] en/rtc/links.md:4  裸相对链接 nothing/here 被 mint 按站点根解析为 /nothing/here，该页不存在\n', out)
        self.assertIn('[错误] en/rtc/links.md:5  /zh/rtc/overview 里找不到锚点 #不存在', out)
        self.run_cli('links', '--fix')
        self.assertEqual(self.read('en/rtc/links.md').splitlines()[:3], [
            '[a](/en/rtc/overview#faq-2)', '[b](/zh/rtc/web/integration) (Chinese)', '[c](/en/rtc/overview#faq)'])

    def test_chinese_suffix_rules(self):
        self.write('en/rtc/links.md', '\n'.join([
            '[done](/zh/rtc/web/integration) (Chinese)',       # 已有后缀
            '[Guide (Chinese)](/zh/rtc/web/integration)',      # 写在链接文字里也算有
            '[![img](/zh/rtc/images/arch.png)](/zh/rtc/web/integration)',  # 链接文字是图片：跳过
            '[`join()`](/zh/rtc/web/integration)',             # 链接文字是代码：跳过
            '<Card title="Guide" href="/zh/rtc/web/integration">x</Card>',  # 组件：只告警
            '<Card title="Guide (Chinese)" href="/zh/rtc/web/integration">x</Card>',  # 已注明
            '[now en](/en/rtc/overview) (Chinese)',            # 已指向英文页：后缀多余
            '[img](/zh/rtc/images/arch.png)',                  # 指向图片文件：不是页面，不加
            '',
        ]))
        rc, out, _ = self.run_cli('links')
        self.assertEqual(rc, 0, out)
        lines = [x for x in out.splitlines() if 'links.md:' in x]
        self.assertEqual(len(lines), 2, out)
        self.assertIn('links.md:5  组件 / HTML 链接指向未译的中文页，需在链接文字里手工注明 "(Chinese)"', lines[0])
        self.assertNotIn('可 --fix', lines[0])
        self.assertIn('links.md:7  已指向英文页，应删掉链接后的 "(Chinese)"（可 --fix）', lines[1])
        self.run_cli('links', '--fix')
        self.assertIn('\n[now en](/en/rtc/overview)\n', self.read('en/rtc/links.md'))


# ───────────────────────────── check ─────────────────────────────

class CheckTest(Fixture):
    def test_empty_en_passes(self):
        rc, out, err = self.run_cli('check')
        self.assertEqual(rc, 0, err)
        self.assertIn('错误 0', out)

    def test_warnings_do_not_fail(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW + '\n[x](/zh/rtc/overview)\n')
        self.run_cli('nav')
        self.run_cli('lock', 'en/rtc/overview')
        self.write('zh/rtc/overview.md', ZH_OVERVIEW + '\n## 新增\n')
        self.commit('zh 更新')
        rc, out, err = self.run_cli('check')
        self.assertEqual(rc, 0, err)
        self.assertIn('[过期] en/rtc/overview', out)
        self.assertIn('[未审校] en/rtc/overview', out)
        self.assertIn('应改为 /en/rtc/overview', out)

    def test_nav_mismatch_fails(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        rc, _, err = self.run_cli('check')
        self.assertEqual(rc, 1)
        self.assertIn('python3 scripts/i18n.py nav', err)

    def test_lock_without_en_fails(self):
        self.write('i18n/en.lock.json', json.dumps({'en/rtc/overview': {
            'source': 'zh/rtc/overview.md', 'zh_blob': 'x', 'zh_commit': 'y', 'reviewed': False}}))
        rc, _, err = self.run_cli('check')
        self.assertEqual(rc, 1)
        self.assertIn('英文页不存在', err)

    def test_lock_missing_field_or_invalid_json_fails(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW)
        self.run_cli('nav')
        self.write('i18n/en.lock.json', json.dumps({'en/rtc/overview': {'source': 'zh/rtc/overview.md'}}))
        rc, _, err = self.run_cli('check')
        self.assertEqual(rc, 1)
        self.assertIn('缺字段', err)
        self.write('i18n/en.lock.json', '{bad json')
        rc, _, err = self.run_cli('check')
        self.assertEqual(rc, 1)
        self.assertIn('不是合法 JSON', err)

    def test_broken_link_fails(self):
        self.write('en/rtc/overview.md', EN_OVERVIEW + '\n[x](#不存在)\n')
        self.run_cli('nav')
        rc, _, err = self.run_cli('check')
        self.assertEqual(rc, 1)
        self.assertIn('本页找不到锚点 #不存在', err)


# ───────────────────────────── tm-merge ─────────────────────────────

class TmMergeTest(Fixture):
    def test_merge_filled_only(self):
        self.write('i18n/server-api/rtc.en.json', json.dumps({'创建频道': 'Create a channel', '旧': 'Old'}))
        self.write('i18n/server-api/rtc.missing.json', json.dumps(
            {'销毁频道': 'Destroy a channel', '旧': 'Old (fixed)', '空': '', '空白': '  ', '中文': '张三'},
            ensure_ascii=False))
        rc, out, err = self.run_cli('tm-merge', 'rtc')
        self.assertEqual(rc, 0, err)
        self.assertIn('rtc：合并 3 条', out)
        self.assertIn('missing 剩 2 条', out)
        tm_text = self.read('i18n/server-api/rtc.en.json')
        self.assertEqual(json.loads(tm_text), {'创建频道': 'Create a channel', '旧': 'Old (fixed)',
                                               '销毁频道': 'Destroy a channel', '中文': '张三'})
        # 格式：不转义中文、2 空格缩进、键排序、结尾换行
        self.assertIn('"中文": "张三"', tm_text)
        self.assertTrue(tm_text.endswith('}\n'))
        self.assertEqual(list(json.loads(tm_text)), sorted(json.loads(tm_text)))
        self.assertEqual(json.loads(self.read('i18n/server-api/rtc.missing.json')), {'空': '', '空白': '  '})
        # 再跑一次：没有可合并的，幂等
        rc, out, _ = self.run_cli('tm-merge', 'rtc')
        self.assertIn('rtc：合并 0 条', out)

    def test_no_tm_file_and_skip_missing(self):
        self.write('i18n/server-api/meeting.missing.json', json.dumps({'进入会议': 'Enter the meeting'}))
        rc, out, err = self.run_cli('tm-merge')  # 不带参数：两个产品都处理，rtc 没有 missing 就跳过
        self.assertEqual(rc, 0, err)
        self.assertIn('rtc：没有 i18n/server-api/rtc.missing.json，跳过', out)
        self.assertEqual(json.loads(self.read('i18n/server-api/meeting.en.json')), {'进入会议': 'Enter the meeting'})
        rc, _, _ = self.run_cli('tm-merge', 'nope')
        self.assertEqual(rc, 2)

    def test_non_object_refused(self):
        self.write('i18n/server-api/rtc.missing.json', json.dumps(['x']))
        rc, _, err = self.run_cli('tm-merge', 'rtc')
        self.assertEqual(rc, 1)
        self.assertIn('顶层应为对象', err)


# ───────────────────────────── 生成页标题重名 ─────────────────────────────

class GeneratedHeadingTest(Fixture):
    def setUp(self):
        super().setUp()
        self.write('en/rtc/server-api/overview.md', '## Signing\n')
        self.write('en/rtc/server-api/channel.md', GENERATED_EN)
        self.run_cli('nav')

    def test_unique_headings_pass(self):
        rc, out, err = self.run_cli('check')
        self.assertEqual(rc, 0, err)

    def test_duplicate_headings_fail(self):
        # 按 slug 判重：大小写、标点不同也算撞；代码块里的 ## 不算
        self.write('en/rtc/server-api/channel.md', GENERATED_EN + '\n## Create a Channel!\n\n```md\n## Destroy a channel\n```\n')
        rc, _, err = self.run_cli('check')
        self.assertEqual(rc, 1)
        self.assertIn('en/rtc/server-api/channel.md：2 个 ## 标题锚点相同（#create-a-channel：'
                      'Create a channel / Create a Channel!）', err)
        self.assertNotIn('#destroy-a-channel', err)

    def test_handwritten_page_not_checked(self):
        # 手写页（无生成标记）重复标题是合法写法（如 FAQ），不报
        self.write('en/rtc/server-api/overview.md', '## FAQ\n\n## FAQ\n')
        rc, _, err = self.run_cli('check')
        self.assertEqual(rc, 0, err)

    def test_tm_fallback_is_warning_in_check(self):
        self.write('i18n/server-api/rtc.missing.json', json.dumps({'销毁频道': ''}, ensure_ascii=False))
        rc, out, err = self.run_cli('check')
        self.assertEqual(rc, 0, err)
        self.assertIn('[翻译记忆缺失] rtc：已有 1 个 en 生成页，但翻译记忆缺失 1 条', out)


if __name__ == '__main__':
    unittest.main()
