---
title: "Enums"
description: "Enum values of the Windows SRTC C++ SDK: StreamCodec (AAC, Opus, H.264, H.265), StreamModelEnum media streaming modes, ViewEnumType render types, and LocalRecordStatusEnum local recording states. Read when setting a codec or mode, or handling recording status."
---

### Codec type StreamCodec
| Parameter name | Parameter type | Value |
| --- | --- | --- |
| AAC | int | 0xf |
| OPUS | int | 0x5355504F |
| H264 | int | 0x1b |
| H265 | int | 0x24 |


### Media streaming mode StreamModelEnum
| Parameter name | Parameter type | Value |
| --- | --- | --- |
| NoStream | int | 0 |
| Normal | int | 1 |
| Just_For_SendRecv | int | 2 |
| MutilsTreams | int | 3 |


### Render type ViewEnumType
| Parameter name | Parameter type | Value |
| --- | --- | --- |
| Hwnd | int | 0 - Render through an HWND window handle |
| CallBack | int | 1 - Render through data callbacks (recommended) |


### Local recording status LocalRecordStatusEnum
| Parameter name | Parameter type | Value |
| --- | --- | --- |
| none | int | 0 - Not recording |
| begin | int | 1 - Preparing to record |
| record | int | 2 - Recording |
| beginStop | int | 3 - Preparing to stop recording |
| stop | int | 4 - Recording stopped |
| cancel | int | 5 - Recording canceled |
| beginCreateMp4 | int | 6 - Started creating the MP4 |
| CreateMp4Finish | int | 7 - MP4 created |
| fail | int | 200 - Error (check msg for the error message) |

