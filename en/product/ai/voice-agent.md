---
title: "AI voice agent and custom agents"
sidebarTitle: "Voice agent and custom agents"
description: "Three ways to have AI talk by voice in calls: the media gateway's built-in voice agent (web trial page, prompt / greeting / voice, interruptible, limits), your own agent with the Python SDK or pipecat, and phone lines to AI. Read to pick a route for AI customer service or calls."
---

There are three ways to let AI talk with people during calls, ordered from least to most development effort:

| Route | Best for | Development effort |
| --- | --- | --- |
| [Built-in AI voice agent](#built-in-ai-voice-agent) | Voice Q&A on a web page, customer service trials, internal assistants; seeing results quickly | No development; just configure a prompt in the console |
| [Build your own agent](#build-your-own-agent) | Connecting business systems, looking up orders, calling tools, or using real-time voice LLMs and custom conversation flows | Write a program with the Python SDK / pipecat |
| [Phone lines to AI](#connect-phone-calls-to-ai) | AI answering incoming calls, AI outbound calls | Phone lines connected to the device gateway + an agent you build yourself |

---

## Built-in AI voice agent

The media gateway has a built-in voice agent: a visitor clicks "Start conversation" on a web page, the AI greets them, and from then on they can chat as on a phone call;
**they can interrupt the AI at any time while it's speaking**. Recognition, LLM, and synthesis all use the services configured in the AI profile, and all of them can be self-hosted.

### What you can configure

| Setting | Where | Description |
| --- | --- | --- |
| Prompt | "Voice agent" in the AI profile | The AI's identity, knowledge, and answering rules. The system automatically appends voice-call requirements (short spoken sentences, no lists or emoji) |
| Greeting | Same place | The first thing the AI says before the visitor speaks |
| Voice, speaking rate | "Voice" and "Speaking rate" in the AI profile | Chosen per language |
| Which models to use | Speech recognition / LLM / speech synthesis in the AI profile | See [AI services and profiles](/en/product/ai/models) |

"Settings" on the trial page can also change the prompt, greeting, and voice; changes take effect from the next conversation, which makes on-site tuning easy.

<Note>
Changes made in "Settings" on the trial page are saved **locally on the media gateway**; with multiple media gateways, each saves its own. For production use, put everything in the AI profile.
</Note>

### Trial page

After deployment, open the trial page through the gateway's address, choose a profile, language (中文 / English), and microphone, and click "Start conversation".
The page shows both sides' text in real time and the AI's state (listening / thinking / speaking).

+ **HTTPS is required**: browsers only allow web pages to use the microphone over HTTPS, so the trial page must be opened over HTTPS through the reverse proxy at the platform entry point; we configure this at deployment
+ **We recommend setting an access passcode**: without one, anyone who can open the page can start conversations (consuming LLM quota) and change the prompt. With one, visitors enter the passcode the first time they open the page
+ We recommend wearing headphones: a computer's built-in microphone picks up people nearby, who may interrupt the AI or be taken as the visitor's speech

### How it decides "started speaking" and "finished speaking"

+ **Started speaking**: as soon as the recognition service returns its first interim result, the visitor is considered to have started speaking; if the AI is talking, it stops immediately (interruption)
+ **Finished speaking**: once the recognition service decides a sentence has ended (about 0.8 seconds of pause), the sentence is sent to the LLM for an answer
+ A separate **volume gate** blocks speech from people farther away, to avoid false interruptions

This avoids deploying a separate voice activity detection model and keeps the offline package smaller. The trade-offs: interruption is about 0.3 seconds slower than with a dedicated detection model; since "finished" is judged by pauses alone,
a slightly longer pause mid-sentence is taken as the end; **English conversations have no interim results, so the AI can only be interrupted after the visitor finishes a whole sentence**.

### Limits and duration

| Item | Default | Description |
| --- | --- | --- |
| Concurrent conversations | 5 | When full, the visitor is asked to try again later; adjustable to the server's and model's capacity |
| Duration per conversation | 10 minutes | The AI ends the conversation when time is up |
| Both sides silent | 90 seconds | The conversation ends after this |
| Conversation turns | 50 | Beyond this, the AI says a closing line and ends |

+ Each conversation uses **2 user concurrency** slots (visitor + AI)
+ When the visitor says goodbye, the AI says goodbye and hangs up automatically
+ Timeouts catch a stalled LLM or speech synthesis, so the AI never stays "thinking" forever; for voice scenarios, we recommend **turning off thinking mode** in the LLM service, otherwise the first sentence is noticeably slower

### Known limitations

+ Each AI sentence is played only after the whole sentence is synthesized; first-response time ≈ recognition finalization + LLM generating the first sentence + synthesizing one sentence
+ One conversation serves one visitor; multiple people can't talk to the AI in the same conversation
+ The web trial page is currently the only entry point; it doesn't answer phone calls directly—for phone calls, see below
+ Tool calling (such as querying business systems) isn't supported; if you need it, go with "Build your own agent"

---

## Build your own agent

When you need to connect business systems, look up data, call tools, or use real-time voice LLMs, use the **Python SDK** to have your program join the channel as a user,
receive audio itself, connect any recognition / LLM / synthesis service, and send the AI's voice back into the channel:

+ [Python SDK quickstart](/en/rtc/python/quickstart): install, join, send and receive audio
+ [Voice AI agent guide](/en/rtc/python/advanced/ai-agent): sentence segmentation per speaker, interruption, filling silent frames, choosing a sample rate
+ [Integrate pipecat](/en/rtc/python/advanced/pipecat): if you already have a pipecat voice pipeline, swap in one transport to join SRTC channels

The agent appears in the channel like any other user, and people on web, apps, and in meetings can all talk with it.

---

## Connect phone calls to AI

Once a carrier SIP trunk or the customer's existing IP-PBX is connected to the **device gateway**, each incoming call is a regular user in a channel.
Your backend creates a channel for each call and brings an agent you built into the same channel, enabling AI phone customer service and AI outbound calls.
See [Connect phone lines](/en/product/device-access/phone-lines).
