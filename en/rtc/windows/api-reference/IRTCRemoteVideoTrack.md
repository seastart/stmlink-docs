---
title: "IRTCRemoteVideoTrack"
description: "API reference for IRTCRemoteVideoTrack, the Windows SRTC remote video object (a user's video or the composite stream): add, remove, or clear IRTCView render targets. Read when rendering remote video."
---

## Description
The remote video object.



## Inheritance
[IRTCTrack](/en/rtc/windows/api-reference/IRTCTrack) ->IRTCRemoteVideoTrack



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





