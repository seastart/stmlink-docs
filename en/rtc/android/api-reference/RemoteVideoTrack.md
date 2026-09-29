---
title: "RemoteVideoTrack"
description: "Android remote video track API: bind render views, monitor receive stalls with RTCRemoteVideoEvent, and configure the VcsPlayerGlTextureView / VcsPlayerGlSurfaceView render views (rotation, flip, scale type, updateFrame). Read when displaying remote or local video on Android."
---

## Description

`RemoteVideoTrack` renders remote video and monitors the status of the remote stream.

## RemoteVideoTrack methods

### setRemoteVideoEvent(event)
```kotlin
fun setRemoteVideoEvent(event: RTCRemoteVideoEvent)
```
Description: Sets the remote video stream status listener and registers the global clock check.  
Parameters:
- `event`: `RTCRemoteVideoEvent`, the remote stream status event callback implementation.
Returns: None (`Unit`).

When the status is reported:
- If no valid frame is received for about 3 consecutive seconds after subscribing, the callback reports `isChoke = true`.
- When valid frames resume, the callback reports `isChoke = false`.

### removeRemoteVideoEvent()
```kotlin
fun removeRemoteVideoEvent()
```
Description: Removes the remote stream status listener and cancels the global clock check.  
Parameters: None.  
Returns: None (`Unit`).

## Rendering methods inherited from VideoTrack

### addPlayView(view)
```kotlin
fun addPlayView(view: View): Boolean
```
Description: Adds a single render view. Only `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView` are supported.  
Parameters:
- `view`: `View`, the render view.
Returns: `Boolean`; `true` if the view was added, `false` if the type is unsupported or the view was already added.

### replacePlayView(views)
```kotlin
fun replacePlayView(views: MutableList<View>)
```
Description: Replaces the entire list of render views.  
Parameters:
- `views`: `MutableList<View>`, the render views; only `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView` are supported.
Returns: None (`Unit`).

### removePlayView(view)
```kotlin
fun removePlayView(view: View)
```
Description: Removes the specified render view.  
Parameters:
- `view`: `View`, the target render view.
Returns: None (`Unit`).

### removeAllPlayView()
```kotlin
fun removeAllPlayView()
```
Description: Removes all render views.  
Parameters: None.  
Returns: None (`Unit`).

## RTCRemoteVideoEvent callback interface

`RTCRemoteVideoEvent` is the remote video stream status callback interface, registered through `setRemoteVideoEvent(event)`.

### onReceiveStreamStatusChange(channel, uid, trackDesc, isChoke)
```kotlin
fun onReceiveStreamStatusChange(
    channel: String,
    uid: String,
    trackDesc: String,
    isChoke: Boolean
)
```
Description: Called when the status of a remote video stream changes.  
Parameters:
- `channel`: `String`, the ID of the channel the remote stream belongs to.
- `uid`: `String`, the remote user ID.
- `trackDesc`: `String`, the track description.
- `isChoke`: `Boolean`, whether the stream is stalled; `true` means stalled, `false` means back to normal.
Returns: None (`Unit`).

## Video render views

Display video with the SDK's `VcsPlayerGlTextureView` or `VcsPlayerGlSurfaceView`. The following usage applies to both remote video and local camera preview:

```kotlin
import cn.seastart.rtc.media.original.render.VcsPlayerGlTextureView
import cn.seastart.rtc.media.original.render.VcsPlayerGlSurfaceView
import cn.seastart.rtc.media.original.render.RenderConstants

val view = VcsPlayerGlTextureView(context)
view.setViewScaleType(RenderConstants.CENTERINSIDE)
remoteTrack.addPlayView(view)
```

XML example:

```xml
<cn.seastart.rtc.media.original.render.VcsPlayerGlTextureView
    android:layout_width="match_parent"
    android:layout_height="match_parent" />
```

Call the view's `onResume()` / `onPause()` along with the screen lifecycle. When a view is no longer needed, remove it from the track first, then call `onDestroy()` to release render resources. Don't reuse a destroyed view. The track feeds frames to the view, so you don't need to call `updateFrame` yourself for normal subscriptions or camera preview.

### Display configuration

The following methods are available on both views and all return `Unit`:

```kotlin
fun customDisplayCtrl(use: Boolean)
fun setViewRotate(rotateAngle: Int)
fun setViewflip(flipX: Boolean, flipY: Boolean)
fun setViewScaleType(ScaleType: Int)
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `use` | Boolean | Yes | Defaults to `false`, which uses the frame's own orientation and the SDK's preview mirroring configuration; `true` uses this view's custom rotation and flip. |
| `rotateAngle` | Int | Yes | Custom display angle; positive values are counterclockwise. Pass `0/90/180/270` or an equivalent value that differs by full turns. It overrides the frame orientation instead of adding to it; defaults to `0`. |
| `flipX` / `flipY` | Boolean | Yes | Horizontal / vertical flip along the display coordinates in custom mode; both default to `false`, and the default front-camera mirroring isn't applied on top. |
| `ScaleType` | Int | Yes | One of the `RenderConstants` scale constants in the table below; can be set in both normal and custom mode; defaults to `CENTERINSIDE`. |

Rotation, flip, and mode changes take effect from the **next frame**; if no new frame arrives, the displayed frame doesn't change. The scale type can apply to the current frame. The configuration belongs only to this view and doesn't change the video sent to remote users.

| Scale constant | Value | Effect |
| --- | --- | --- |
| `FITXY` | 0 | Stretches to fill the view; the aspect ratio may change. |
| `CENTERCROP` | 1 | Fills the view proportionally and crops from the center. |
| `CENTERINSIDE` | 2 | Shows the full frame proportionally and centered; may leave margins. |
| `FITSTART` | 3 | Shows the full frame proportionally, aligned left / top along the margin direction. |
| `FITEND` | 4 | Shows the full frame proportionally, aligned right / bottom along the margin direction. |

### updateFrame(y, u, v, width, height, format, rotationDegrees)

Use this only when your app submits raw frames directly to a render view:

```kotlin
fun updateFrame(
    y: ByteArray?, u: ByteArray?, v: ByteArray?,
    width: Int, height: Int, format: Int, rotationDegrees: Int
)
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `y` | ByteArray | Yes | Tightly packed Y plane, at least `width × height` bytes. |
| `u` | ByteArray | Yes | For I420, the U plane, at least `width × height / 4` bytes; for NV12 / NV21, the interleaved UV / VU plane, at least `width × height / 2` bytes. |
| `v` | ByteArray? | Required for I420 | For I420, the V plane, at least `width × height / 4` bytes; can be `null` for NV12 / NV21. |
| `width` / `height` | Int | Yes | Original pixel width and height, both positive even numbers; don't pass the rotated dimensions. Row-end padding isn't supported. |
| `format` | Int | Yes | `YuvFormat.I420`, `NV12`, or `NV21`; for the full constants, see [Types](/en/rtc/android/types). |
| `rotationDegrees` | Int | Yes | The **clockwise** rotation still to be applied to the pixels: `0/90/180/270` or an equivalent value that differs by full turns. |

Returns: `Unit`. Frame data is copied before the method returns, after which the app can reuse the arrays. An invalid size, data length, pixel format, or an angle that isn't a multiple of 90 degrees causes the frame to be rejected and the previous frame to be kept; there's no separate failure callback. Custom mode overrides the frame orientation, but the frame angle you pass must still be valid.
