---
title: "Build with AI"
description: "Connect the SRTC / SMeeting docs to AI coding tools such as Claude Code and Cursor: install the integration skills with one command, or connect the docs MCP server. Also covers llms.txt, per-page Markdown, and how to prompt for better results."
---

If you write code with an AI coding tool, you can connect our docs to it so that it generates code against our actual APIs and conventions instead of guessing from its training data.

There are two ways to do this. **We recommend the first one**—it takes a single command.

---

## Option 1: Install the skills (recommended)

Run this in your project directory:

```bash
npx skills add https://docs.stmlink.com
```

This creates `.agents/skills/` in your project. It works with Claude Code, Cursor, Codex, Gemini CLI, Devin, and other mainstream tools, and your AI reads it automatically.

It installs three skills, each for a different scenario:

| Name | When it is used |
| --- | --- |
| **SRTC 音视频接入** (*SRTC audio and video integration*) | Real-time audio and video: joining a channel, publishing and subscribing to tracks, screen sharing, recording |
| **SMeeting 会议接入** (*SMeeting conferencing integration*) | Video conferencing: choosing an integration option, meeting controls, raise hand, waiting room, in-meeting messages |
| **SRTC / SMeeting 服务端接入** (*SRTC / SMeeting server integration*) | Calling the APIs from your backend: how to compute the signature, how to issue tokens, how to receive callbacks |

They are not copies of the docs. They cover **the places where integrations most often go wrong**: call order, the difference between the terms of the two layers, the three common causes of signature failures, and what our design does not support (for example, a host cannot force another member's camera on).

<Tip>
After installing, you can ask right away: "I want to build a video meeting with a host and raise hand on Web. Help me plan the integration."
The AI first decides which integration option to use and then gives you the steps—instead of dumping code that may target the wrong layer.
</Tip>

---

## Option 2: Connect the docs MCP server

When you need the AI to look up the full docs in real time (not just the skills), configure our MCP server:

```
https://docs.stmlink.com/mcp
```

It provides docs search and reads whole pages by path. For how to configure it, see the MCP documentation of the tool you use. Once connected, the three skills above are also discovered automatically, so you don't need to install them separately.

---

## Give the AI context directly

If you don't want to install anything, you can give these URLs to the AI directly:

| URL | Content |
| --- | --- |
| `https://docs.stmlink.com/llms.txt` | Index of all pages on the site, grouped by product and platform; the AI uses it to decide which page to read |
| Any doc page URL plus `.md` | The Markdown source of that page, for example `/zh/rtc/web/quickstart.md` |

Each page also has **Copy page** and **Open in ChatGPT / Claude** buttons in the top-right corner.

---

## Results depend on how you ask

These points noticeably improve the quality of generated code:

+ **Say which layer.** "Build a meeting with SMeeting" and "build an audio/video call with SRTC" use completely different APIs, and their terms don't carry over.
+ **Say which platform.** The same capability has different class and method names on Web, Android, and Swift.
+ **Say whether you are building your own UI.** This determines which SMeeting integration option to use; picking the wrong one wastes a lot of work.

<Warning>
**Review the code the AI generates, especially anything involving keys.** `app_key` must stay on your own backend.
Any approach that puts it in frontend code, a configuration file, or a mobile app is wrong—even if the AI generated it that way.
See [Token and authentication](/en/rtc/token).
</Warning>

---

## Having problems

If the AI-generated code uses the wrong API, it usually means the docs don't explain that part clearly enough. Let us know—we'll fix the docs. That is more valuable than working around it on your own.
