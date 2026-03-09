---
title: "枚举类型"
description: "Windows SRTC 音视频 SDK 枚举值定义"
---

### 数据编码类型 StreamCodec
| 参数名称 | 参数类型 | 值定义 |
| --- | --- | --- |
| AAC | int | 0xf |
| OPUS | int | 0x5355504F |
| H264 | int | 0x1b |
| H265 | int | 0x24 |


### 流媒体类型 StreamModelEnum
| 参数名称 | 参数类型 | 值定义 |
| --- | --- | --- |
| NoStream | int | 0 |
| Normal | int | 1 |
| Just_For_SendRecv | int | 2 |
| MutilsTreams | int | 3 |


### 渲染类型 ViewEnumType
| 参数名称 | 参数类型 | 值定义 |
| --- | --- | --- |
| Hwnd | int | 0 - 通过 HWND 窗口句柄渲染 |
| CallBack | int | 1 - 通过数据回调渲染（推荐） |


### 本地录制状态 LocalRecordStatusEnum
| 参数名称 | 参数类型 | 值定义 |
| --- | --- | --- |
| none | int | 0 - 没有录制 |
| begin | int | 1 - 准备录制 |
| record | int | 2 - 正在录制 |
| beginStop | int | 3 - 准备停止录制 |
| stop | int | 4 - 停止录制 |
| cancel | int | 5 - 取消录制 |
| beginCreateMp4 | int | 6 - 开始创建 MP4 |
| CreateMp4Finish | int | 7 - 创建 MP4 完成 |
| fail | int | 200 - 异常（查看 msg 获取错误信息） |

