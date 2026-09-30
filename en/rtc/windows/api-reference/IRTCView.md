---
title: "IRTCView"
description: "API reference for IRTCView, the Windows SRTC virtual base class for render targets: choose HWND rendering (the SDK draws into your window handle) or callback rendering (the SDK hands you YUV frames or a solid RGB fill). Read when rendering local or remote video."
---

## Description
The virtual render object, providing render data callbacks and render handle setup.

You can inherit from this class to receive the SDK's render data callbacks, which makes it easier to write your UI code and draw the UI.

Alternatively, you can set an hwnd to pass a window handle into the SDK, and the SDK renders with the best rendering method the computer supports. 

## Inheritance


## Methods
### Get the render type
```cpp
virtual ViewEnumType ViewType() = 0;
```

**Returns**

| ViewEnumType | Render type:<br/>Hwnd renders through an hwnd; the SDK uses getHwnd in this class and renders the data onto that hwnd.<br/>CallBack renders through YUV callbacks; the SDK calls back the data through updatePlanes and updateFull in this class, and your app renders the data (recommended) |
| --- | --- |




### Get the handle
```cpp
virtual void* getHwnd() = 0;
```

**Returns**

| void | Render handle |
| --- | --- |


Note: takes effect only when ViewType() returns HWND.



### Render data
```cpp
virtual void updatePlanes(const unsigned char* buf, int w, int h, int fourcc, int label) = 0;
```

**Parameters**

| buf | const unsigned char* | Render data |
| --- | --- | --- |
| w | int | Data width |
| h | int | Data height |
| fourcc | int | Data type, 0: yuv420 |
| label | int | Data rotation angle |


Note: takes effect only when ViewType() returns CallBack.



### Render a solid RGB color
```cpp
virtual void updateFull(int r, int g, int b) = 0;
```

**Parameters**

| r | int | Red (0–255) |
| --- | --- | --- |
| g | int | Green (0–255) |
| b | int | Blue (0–255) |


Note: takes effect only when ViewType() returns CallBack.
