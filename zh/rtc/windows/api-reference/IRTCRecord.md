---
title: "IRTCRecord"
description: "Windows SRTC 音视频 SDK IRTCRecord 本地录制接口参考"
---

## 函数说明
本地录制接口，用于控制频道内容的本地录制功能。

## 继承关系
无

## 函数方法

### 设置录制文件名
```cpp
virtual StatusCode setRecordFileName(const char* filepath) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| filepath | const char* | 录制文件保存路径 |

**返回值**

| 返回值 | 说明 |
| --- | --- |
| StatusCode | 操作结果状态码 |

### 设置水印
```cpp
virtual StatusCode setWaterMask(const char* mask) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| mask | const char* | 水印配置信息 |

**返回值**

| 返回值 | 说明 |
| --- | --- |
| StatusCode | 操作结果状态码 |

### 设置输出尺寸
```cpp
virtual StatusCode setOutputSize(int w, int h) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| w | int | 输出视频宽度 |
| h | int | 输出视频高度 |

**返回值**

| 返回值 | 说明 |
| --- | --- |
| StatusCode | 操作结果状态码 |

### 开始录制
```cpp
virtual StatusCode startRecord() = 0;
```

**返回值**

| 返回值 | 说明 |
| --- | --- |
| StatusCode | 操作结果状态码 |

### 设置录制窗口
```cpp
virtual StatusCode setRecordHwnd(void* hwnd, int x, int y, int w, int h) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| hwnd | void* | 录制窗口句柄 |
| x | int | 录制区域 x 坐标 |
| y | int | 录制区域 y 坐标 |
| w | int | 录制区域宽度 |
| h | int | 录制区域高度 |

**返回值**

| 返回值 | 说明 |
| --- | --- |
| StatusCode | 操作结果状态码 |

### 设置成员视图布局
```cpp
virtual StatusCode setRecordLayoutMemberView(const char* layout_json, int json_len) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| layout_json | const char* | 布局配置 JSON 字符串 [查看](../types.md#录制布局成员视图配置) |
| json_len | int | JSON 字符串长度 |

**返回值**

| 返回值 | 说明 |
| --- | --- |
| StatusCode | 操作结果状态码 |

### 暂停录制
```cpp
virtual StatusCode pauseRecord() = 0;
```

**返回值**

| 返回值 | 说明 |
| --- | --- |
| StatusCode | 操作结果状态码 |

### 停止录制
```cpp
virtual StatusCode stopRecord() = 0;
```

**返回值**

| 返回值 | 说明 |
| --- | --- |
| StatusCode | 操作结果状态码 |
