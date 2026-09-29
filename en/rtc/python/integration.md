---
title: "Integration"
description: "What the SRTC Python SDK is for, how to install it, and which platforms it supports, plus the asyncio threading model and deployment caveats around fork and capacity. Read this page before integrating the Python SDK."
---

The SRTC Python SDK (PyPI package `srtc`) targets **server-side AI scenarios**: your Python service joins a channel like any other user, receives the voice of everyone in the channel, and pushes synthesized audio back.

### Use cases

+ AI voice assistants / voice bots: connect an ASR → LLM → TTS pipeline to a channel
+ Server-side recording, quality inspection, and real-time transcription
+ You already have a [pipecat](https://github.com/pipecat-ai/pipecat) voice agent and want to connect it to an SRTC channel (see [Integrating pipecat](/zh/rtc/python/advanced/pipecat) (Chinese))

### Difference from the C SDK

Both share the same native core underneath and behave the same. The difference is the **data format**:

| | Python SDK | [C SDK](/zh/rtc/capi/integration) (Chinese) |
| --- | --- | --- |
| Received audio | Decoded **PCM**, with the sample rate / channel count you specify | Opus-encoded packets; you decode them yourself |
| Published audio | **PCM** at any sample rate; the SDK handles resampling, encoding, and pacing | Encoded Opus packets; you write them at real-time pace yourself |
| Programming model | `asyncio`: `async with` / `async for` | C callbacks + threads you manage |
| Video | Receive only (optionally decoded to RGB images) | Send and receive (encoded data) |

Model inputs and outputs are raw data, so with the Python SDK you rarely need to deal with codecs.

---

### Installation

```bash
pip install srtc                 # Core
pip install "srtc[pipecat]"      # Also install the pipecat integration
```

The only dependencies are `cffi`, `av` (bundles ffmpeg and libopus, so you **don't need** to install ffmpeg on the system separately), and `numpy`.

### Supported platforms

| Platform | Architecture | Notes |
| --- | --- | --- |
| Linux | x86_64, aarch64 | Installs directly on glibc 2.28 and above (Ubuntu 20.04+, Debian 10+, CentOS / Rocky 8+, etc.); for older systems, see below |
| macOS | Apple Silicon (arm64) | 11.0 and above, mainly for local development and debugging |
| Windows | x86_64 | |

Python 3.10 and above. The package for a given platform works with all Python 3.x minor versions.

<Warning>
**Systems with glibc below 2.28 (such as CentOS 7)**: the SDK itself supports glibc down to 2.17, but newer versions of the `av` dependency only ship packages for glibc 2.28+,
so pip falls back to building from source and fails. Pin the `av` version when installing:

```bash
pip install srtc "av>=12,<14"
```
</Warning>

<Note>
Python packages for Alpine (musl) aren't available yet. Contact us if you need them.
</Note>

---

### Threading model

The SDK is built on `asyncio`; call every API from within the event loop:

+ Signaling, reconnection, and audio/video send and receive all run in the SDK's built-in native library and **don't hold Python's GIL**, so they don't slow down your Python code
+ All event callbacks and the data frames you get from `async for` are handed to you on the **event loop thread**, so no locking is needed
+ APIs that wait for server negotiation—joining, subscribing, publishing—are `async` and don't block the event loop while waiting

<Warning>
Don't do slow synchronous work in event callbacks (such as synchronous model inference calls). It blocks the whole event loop and affects send and receive on every channel. Use `await` for asynchronous calls, or move slow processing to a thread pool / process pool.
</Warning>

---

### Deployment notes

**Don't fork in a process that has already used the SDK.** The native core doesn't work in forked child processes:

+ Fork after only `import srtc`, before any `Channel` is created: fine (works normally with gunicorn `--preload` and similar setups)
+ Fork after a `Channel` has been created: using the SDK in the child raises `RuntimeError` right away rather than hanging
+ When using `multiprocessing`, set `multiprocessing.set_start_method("spawn")`

**Capacity reference.** Measured in a single process (Apple M series, each channel receiving 1 audio track + sending 1 audio track): 20 channels online at once use about 61% of one CPU core and 181 MB of memory, with zero dropped frames. Python-side encoding and decoding sets the limit for a single process; with many sessions, scale out horizontally with multiple processes.

<Tip>
Every channel connection needs a **separately issued** token. A token is bound to one session; using the same token to join a second time is rejected by the server with `1032`.
</Tip>

---

### Next steps

+ [Quickstart](/en/rtc/python/quickstart): get listening and speaking working
+ [Voice AI agent guide](/zh/rtc/python/advanced/ai-agent) (Chinese): sentence segmentation, barge-in interruption, timeline
+ [API reference](/zh/rtc/python/api-reference/channel) (Chinese)
