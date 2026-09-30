---
title: "IRTCRecord"
description: "API reference for IRTCRecord, the Windows SRTC local recording object (one per channel): output file name, watermark, output size, recording a window region, the user view layout, and starting, pausing, and stopping recording. Read when implementing local recording."
---

## Description
The local recording interface, used to control local recording of channel content.

## Inheritance
None

## Methods

### Set the recording file name
```cpp
virtual StatusCode setRecordFileName(const char* filepath) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| filepath | const char* | Path where the recording file is saved |

**Returns**

| Return value | Description |
| --- | --- |
| StatusCode | Status code of the operation result |

### Set the watermark
```cpp
virtual StatusCode setWaterMask(const char* mask) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| mask | const char* | Watermark configuration |

**Returns**

| Return value | Description |
| --- | --- |
| StatusCode | Status code of the operation result |

### Set the output size
```cpp
virtual StatusCode setOutputSize(int w, int h) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| w | int | Output video width |
| h | int | Output video height |

**Returns**

| Return value | Description |
| --- | --- |
| StatusCode | Status code of the operation result |

### Start recording
```cpp
virtual StatusCode startRecord() = 0;
```

**Returns**

| Return value | Description |
| --- | --- |
| StatusCode | Status code of the operation result |

### Set the recording window
```cpp
virtual StatusCode setRecordHwnd(void* hwnd, int x, int y, int w, int h) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| hwnd | void* | Handle of the window to record |
| x | int | x coordinate of the recording area |
| y | int | y coordinate of the recording area |
| w | int | Width of the recording area |
| h | int | Height of the recording area |

**Returns**

| Return value | Description |
| --- | --- |
| StatusCode | Status code of the operation result |

### Set the user view layout
```cpp
virtual StatusCode setRecordLayoutMemberView(const char* layout_json, int json_len) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| layout_json | const char* | Layout configuration JSON string; see [Recording layout user view configuration](/en/rtc/windows/types#recording-layout-user-view-configuration) |
| json_len | int | Length of the JSON string |

**Returns**

| Return value | Description |
| --- | --- |
| StatusCode | Status code of the operation result |

### Pause recording
```cpp
virtual StatusCode pauseRecord() = 0;
```

**Returns**

| Return value | Description |
| --- | --- |
| StatusCode | Status code of the operation result |

### Stop recording
```cpp
virtual StatusCode stopRecord() = 0;
```

**Returns**

| Return value | Description |
| --- | --- |
| StatusCode | Status code of the operation result |
