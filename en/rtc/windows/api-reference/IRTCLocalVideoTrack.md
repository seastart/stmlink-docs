---
title: "IRTCLocalVideoTrack"
description: "API reference for IRTCLocalVideoTrack, the Windows SRTC base class for local video tracks (camera and screen): add, remove, or clear IRTCView render targets for local preview. Read when showing a local preview."
---

## Description
The video track base class, providing publishing, unpublishing, render object binding, and other operations.



## Inheritance
[IRTCTrack](/en/rtc/windows/api-reference/IRTCTrack) -> IRTCLocalVideoTrack



## Methods
### Add a render object
```cpp
virtual StatusCode addPlayView(IRTCView* v) = 0;
```

**Parameters**

| v | Render object class; see [IRTCView](/en/rtc/windows/api-reference/IRTCView) |
| --- | --- |




### Remove a render object
```cpp
virtual StatusCode removePlayView(IRTCView* v) = 0;
```

**Parameters**

| v | Render object class; see [IRTCView](/en/rtc/windows/api-reference/IRTCView) |
| --- | --- |


Note: when removing a render object, a CallBack-type object is matched by object address, and an HWND-type object is matched by HWND.



### Remove all render objects
```cpp
virtual StatusCode removePlayView() = 0;
```
