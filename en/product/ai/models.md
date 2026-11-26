---
title: "AI services and profiles (connecting models)"
sidebarTitle: "AI services and profiles"
description: "Admin console AI services and profiles: register speech recognition, LLM, and speech synthesis (templates, testing, encrypted keys), combine them into profiles (per-language recognition and voice, interpretation volume, voice agent prompt), plus built-in offline models and licenses."
---

The models used for captions, translation, minutes, interpretation, and the voice agent are all configured in the admin console under **AI capabilities → AI services and profiles**, not in configuration files.
The page has two tabs:

+ **AI services**: register individual model services—address, model name, key
+ **AI profiles**: combine services—which recognition service for each language, which LLM, which speech synthesis service and voice

Each app chooses a profile under **AI capabilities → App AI settings**; if none is chosen, the default profile is used. Every "Save" takes effect immediately, with no service restart.

---

## AI services

Click "Add service" and register it by **category**:

| Category | Used for | Connection type |
| --- | --- | --- |
| Speech recognition | Captions, transcription, interpretation, voice agent | FunASR (websocket) |
| LLM | Live translation, minutes, interpretation, voice agent | OpenAI-compatible LLM |
| Speech synthesis | Interpretation audio, voice agent | Generic HTTP TTS (request body template), OpenAI-compatible TTS |
| Real-time voice | — | Reserved, not yet supported |

### One-click templates

Choosing a "One-click template" fills in the connection type, address format, and parameters automatically; you then only change the address, key, and model name:

| Template | Category | Description |
| --- | --- | --- |
| FunASR Chinese 2pass | Speech recognition | Text as you speak + final full sentences; supports hot words |
| FunASR English (offline) | Speech recognition | Full sentences only; English results are cleaned up automatically; hot words aren't sent |
| OpenAI-compatible LLM / DeepSeek | LLM | Fill in the address, model name, and key |
| Freewind offline TTS | Speech synthesis | The offline speech synthesis image we provide; see "Built-in open-source models" below |
| IndexTTS | Speech synthesis | Connects to an IndexTTS service whose HTTP API returns base64 audio |
| OpenAI-compatible TTS | Speech synthesis | The `/v1/audio/speech` API |

### Supported connection types

**LLM: OpenAI-compatible API.** Anything that provides a `/chat/completions` API can be connected, such as DeepSeek, Qwen (compatible mode),
and self-hosted vLLM / Ollama. Key points:

+ **Get the model name exactly right**: some services don't return an error for a wrong model name but silently switch to a default model
+ **The key can be left empty**: LLM services on customers' internal networks often have no authentication; just leave it blank
+ **Thinking mode**: choose "On", "Off", or "Don't send". Translation and the voice agent are speed-sensitive, so we recommend Off; choose "Don't send" for services that don't recognize this parameter
+ Timeout, concurrency limit, sampling temperature, and output limit can be set

**Speech recognition: FunASR (websocket).** Enter a `ws://` or `wss://` address and choose the recognition mode: **2pass** (real-time interim results + final full sentences, for Chinese)
or **offline** (full sentences only, for English).

**Speech synthesis: two types.**

+ **Generic HTTP TTS (request body template)**: most synthesis services customers already have are "POST some JSON, get audio back"; fill in a request body template matching their API to connect,
  with no code changes on our side. The template can use `{{text}}` (text), `{{voice}}` (voice), `{{lang}}` (language), and `{{speed}}` (speaking rate);
  the response can be "audio returned directly" or "base64 in JSON", in wav or pcm format
+ **OpenAI-compatible TTS**: the `/v1/audio/speech` API, returning wav

### Testing and preview

Every service has a "Test" button:

| Category | What the test does |
| --- | --- |
| LLM | Sends one sentence (by default "请回复 OK", i.e. "Please reply OK") and shows the elapsed time and the model's raw reply; on error, shows the raw error returned by the service |
| Speech synthesis | Synthesizes a sentence and **plays it on the page**, showing the audio duration and sample rate; voice and speaking rate can be changed |
| Speech recognition | Upload a wav sample and see the recognition result |

### Key security

+ Keys (the API key, and every value in the extra request headers of HTTP TTS) are **stored encrypted**; the page and APIs only return masked values (such as `sk-****abcd`)
+ Leaving the key empty when editing a service means no change; to remove a stored key, use "Clear"
+ **When you change a service's address, the old key isn't carried over** and must be entered again, so an old key is never sent to a new address
+ Key fields in operation logs are always masked; prompts sent to the LLM and model output are not written to service logs by default

---

## AI profiles

A profile is "a combination of AI services". Click "Add profile" and fill in three sections:

| Section | Field | Description |
| --- | --- | --- |
| Services | Speech recognition | Choose one recognition service **per spoken language**, for example "FunASR Chinese" for Chinese and "FunASR English" for English. "Other languages (\*)" is the fallback; languages that aren't configured aren't recognized |
| | LLM | Shared by translation, minutes, and the voice agent |
| | Speech synthesis | Shared by interpretation and the voice agent |
| Speech synthesis and interpretation | Voice | Chosen **per language**; if not set, the speech synthesis service's default voice is used |
| | Speaking rate | 1 is normal speed |
| | Interpretation original-voice volume | The volume the speaker's original voice is turned down to while interpretation audio plays, 0–1, default 0.2; 0 = mute |
| Voice agent | Prompt, greeting | See [AI voice agent](/en/product/ai/voice-agent#built-in-ai-voice-agent) |

+ You can create multiple profiles and set one as the **default profile**, used by apps that haven't chosen one
+ For example, if different departments use different LLMs, create two profiles and assign each to the corresponding apps
+ A profile used by any app can't be deleted or renamed
+ When two people edit at the same time, the one who saves later is told "The configuration has been modified by someone else"; refresh and edit again, so nobody overwrites the other
+ For on-site troubleshooting, "Edit JSON" lets you change the whole configuration directly

---

## Built-in open-source models

To allow **fully offline** deployment, we provide ready-made offline images for speech recognition and speech synthesis; the models ship with the images and run on CPU. **No LLM is built in**—use the customer's own.

| Purpose | Model | License |
| --- | --- | --- |
| Chinese speech recognition | FunASR: Paraformer-large Chinese recognition (2pass: streaming + high-accuracy full sentences), FSMN endpoint detection, CT-Transformer real-time punctuation, Ngram language model (required for hot words) | FunASR Model Open Source License Agreement (requires crediting the source and authors and keeping the model names) |
| Chinese number normalization | The Chinese inverse text normalization bundled with the FunASR service ("一百二十" → "120") | Subject to the model publisher's license |
| English speech recognition | FunASR: Paraformer-large English offline recognition (vocab10020) | FunASR Model Open Source License Agreement |
| English speech synthesis | Piper `en_US-ljspeech-medium` (English female voice) | Model under MIT; training data LJ Speech is in the public domain |
| Chinese speech synthesis | MeloTTS `vits-melo-tts-zh_en` (Chinese female voice, can read mixed Chinese and English) | MIT |

<Note>
License information is compiled from each model's official release page; **the model's latest official license prevails**. The inference framework for offline speech synthesis is sherpa-onnx (Apache-2.0).
Voice models whose training data is restricted to non-commercial use were deliberately avoided.
</Note>

When the customer already has better models (such as IndexTTS on GPU, or larger recognition models), register them as services using the connection types above and swap them into the profile; nothing else on the platform needs to change.
For the resource usage of each service, see [Deployment and resource planning](/en/product/ai/deploy).
