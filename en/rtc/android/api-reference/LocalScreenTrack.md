---
title: "LocalScreenTrack"
description: "Android screen sharing track API: request screen capture permission, start and stop screen capture, configure the foreground service notification, bind render views, and handle RTCScreenStateEvent. Read when implementing screen sharing on Android."
---

## Description

`LocalScreenTrack` requests screen capture permission, starts and stops screen capture, and can be used as the input track for `publishLocalVideo`.

## LocalScreenTrack methods

### setEvent(e)
```kotlin
fun setEvent(e: RTCScreenStateEvent?)
```
Description: Sets or clears the screen capture state callback. Pass `null` when the screen is destroyed to release the reference between the screen and the track.

Parameters:
- `e`: `RTCScreenStateEvent?`, the screen capture state callback implementation; `null` clears the callback.
Returns: None (`Unit`).

### request(result)
```kotlin
fun request(result: (Boolean, Intent?) -> Unit)
```
Description: Requests the system screen capture permission. The `Intent` returned on successful authorization must be passed to `startCapture`.  
Parameters:
- `result`: `(Boolean, Intent?) -> Unit`, the permission request result callback.
Returns: None (`Unit`).

### setRecordNotification(smallIcon, title, desc, buttonText)
```kotlin
fun setRecordNotification(smallIcon: Int, title: String?, desc: String?, buttonText: String?)
```
Description: Sets the style of the screen capture notification.  
Parameters:
- `smallIcon`: `Int`, the resource ID of the notification's small icon.
- `title`: `String?`, the notification title; can be `null`.
- `desc`: `String?`, the notification description; can be `null`.
- `buttonText`: `String?`, the notification button text; can be `null`.
Returns: None (`Unit`).

### startCapture(intent, resultListener)
```kotlin
fun startCapture(intent: Intent, resultListener: RTCResultListener?)
```
Description: Submits a request to start screen capture. `onSuccess()` only means the SDK accepted the request, not that capture is established; the actual state is reported through `RTCScreenStateEvent`. The result callback isn't guaranteed to run on the main thread.

Parameters:
- `intent`: `Intent`, the screen capture authorization data returned by the `request` success callback.
- `resultListener`: `RTCResultListener?`, whether the start request was accepted; `onFail(code)` means the request wasn't accepted, and no screen lifecycle event is produced for it. Can be `null`.
Returns: None (`Unit`).

### stopCapture()
```kotlin
fun stopCapture()
```
Description: Stops screen capture.  
Parameters: None.  
Returns: None (`Unit`).

## Rendering methods inherited from VideoTrack

Views are `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView` from the `cn.seastart.rtc.media.original.render` package; for display control and lifecycle, see [Video rendering](/en/rtc/android/api-reference/RemoteVideoTrack).

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

## RTCScreenStateEvent callback interface

`RTCScreenStateEvent` is the screen capture state callback interface, registered through `setEvent(e)`.

### onScreenCaptureStateChanged(state, args)
```kotlin
fun onScreenCaptureStateChanged(state: ScreenCaptureState, args: String?)
```
Description: Called when the actual screen capture lifecycle state changes. Whether the SDK accepted a start request is reported separately by the `RTCResultListener` of `startCapture`.

Parameters:
- `state`: `ScreenCaptureState`, one of `START`, `STOP`, and `ERROR`; for enum values, see [Enums](/en/rtc/android/enums).
- `args`: `String?`, extra information; can be `null`.
Returns: None (`Unit`).

> Since 2.0.29, `onScreenRecordStateChanged(ScreenRecordState, ...)` has been replaced by `onScreenCaptureStateChanged(ScreenCaptureState, ...)`, and `ScreenRecordState.AUDIO_ERROR` is no longer available.
