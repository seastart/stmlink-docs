---
title: "AudioRouterManager"
description: "Android API for switching audio output routes between the speaker, earpiece, wired headset, and Bluetooth headset: getting the singleton, auto-switch policies, manual switching, audio focus, device queries, and callbacks. Read when controlling audio output devices on Android."
---

`AudioRouterManager` manages audio output routing between the speaker / earpiece / wired headset / Bluetooth headset. This page is the API reference; for the full initialization order, auto-switch policies, and best practices, see [Audio routing](/en/rtc/android/advanced/audio-routing).

## Getting and releasing

Get the singleton through `RTCEngine`; don't create it yourself with `new`:

```kotlin
val audioRouterManager = rtcEngine.getAudioRouterManager()
// ...
rtcEngine.releaseAudioRouterManager()
```

## Instance methods

### setAudioRouterCalllback(callback)
```java
public void setAudioRouterCalllback(AudioRouterCallback callback)
```
Description: Sets the audio routing callback listener.  
Parameters:
- `callback`: `AudioRouterCallback`, the route change callback implementation.

Returns: None (`void`).

> The method name is `setAudioRouterCalllback` (`Calllback` has 3 `l`s); call it exactly as spelled in the source.

### setAutoChangeAudioRouter(isAutoChange)
```java
public void setAutoChangeAudioRouter(boolean isAutoChange)
```
Description: Sets whether to switch audio routes automatically (simple version). Equivalent to `setAutoChangeAudioRouter(isAutoChange, false, false)`, meaning the earpiece has priority over the speaker and a Bluetooth headset has priority over a wired headset.  
Parameters:
- `isAutoChange`: `boolean`; `true` lets the SDK choose the route automatically, `false` only listens without switching automatically.

Returns: None (`void`).

### setAutoChangeAudioRouter(isAutoChange, isPrioritySpeaker, isPriorityWiredEarphone)
```java
public void setAutoChangeAudioRouter(boolean isAutoChange, boolean isPrioritySpeaker, boolean isPriorityWiredEarphone)
```
Description: Sets the auto-switch policy (full version).  
Parameters:
- `isAutoChange`: `boolean`, whether to switch routes automatically.
- `isPrioritySpeaker`: `boolean`; `true` gives the speaker priority over the earpiece, `false` gives the earpiece priority over the speaker.
- `isPriorityWiredEarphone`: `boolean`; `true` gives a wired headset priority over a Bluetooth headset, `false` gives a Bluetooth headset priority over a wired headset.

Returns: None (`void`).

### setMode(mode)
```java
public void setMode(int mode)
```
Description: Sets the audio mode. Values follow `AudioManager` (such as `MODE_IN_COMMUNICATION`). On Android 6.0+, `init()` doesn't set the mode automatically, so call it again every time you switch app scenarios.  
Parameters:
- `mode`: `int`, the `AudioManager` audio mode.

Returns: None (`void`).

### init()
```java
public void init()
```
Description: Starts audio route monitoring. Call it after getting the instance and setting the callback and policy.  
Parameters: None.  
Returns: None (`void`).

### switchAudioRouter(type)
```java
public void switchAudioRouter(AudioOutputDeviceType type)
```
Description: Manually switches to the specified output device. Passing `UN_KNOW` reselects the most suitable route according to the current auto-switch policy.  
Parameters:
- `type`: `AudioOutputDeviceType`, the target output device type.

Returns: None (`void`).

### release(changeMode)
```java
public void release(boolean changeMode)
```
Description: Releases audio routing resources, stops monitoring, and unregisters the callback.  
Parameters:
- `changeMode`: `boolean`; `true` restores the audio mode to `MODE_NORMAL` and switches back to the speaker on release; `false` doesn't restore the mode.

Returns: None (`void`).

> `rtcEngine.releaseAudioRouterManager()` calls `release(true)` internally.

### getExitAudioOutputDevices()
```java
public HashMap<AudioOutputDeviceType, AudioDeviceInfo> getExitAudioOutputDevices()
```
Description: Gets the set of output devices currently present (selectable).  
Parameters: None.  
Returns: `HashMap<AudioOutputDeviceType, AudioDeviceInfo>`, a map from device type to device info.

### getActiveAudioOutputDevice()
```java
public Pair<AudioOutputDeviceType, AudioDeviceInfo> getActiveAudioOutputDevice()
```
Description: Gets the output device currently in effect.  
Parameters: None.  
Returns: `Pair<AudioOutputDeviceType, AudioDeviceInfo>`; `first` is the device type, `second` is the device info.

### getAudioRouterCallback()
```java
public AudioRouterCallback getAudioRouterCallback()
```
Description: Gets the currently set route callback.  
Parameters: None.  
Returns: `AudioRouterCallback`, the current callback instance; may be `null`.

### getAudioManager()
```java
public AudioManager getAudioManager()
```
Description: Gets the system `AudioManager` held internally.  
Parameters: None.  
Returns: `AudioManager`.

### requestAudioFocus()
```java
public int requestAudioFocus()
```
Description: Requests audio focus.  
Parameters: None.  
Returns: `int`, the request result (same as the return value of the system `AudioManager.requestAudioFocus`).

### releaseAudioFocus()
```java
public int releaseAudioFocus()
```
Description: Releases audio focus.  
Parameters: None.  
Returns: `int`, the release result.

### setFocusChangeListener(listener)
```java
public void setFocusChangeListener(AudioManager.OnAudioFocusChangeListener listener)
```
Description: Sets an external audio focus change listener.  
Parameters:
- `listener`: `AudioManager.OnAudioFocusChangeListener`, the focus change listener.

Returns: None (`void`).

## Static methods

### getValidBluetoothName(curName, context, callback)
```java
public static synchronized void getValidBluetoothName(String curName, Context context, ValidBluetoothNameCallback callback)
```
Description: Corrects inaccurate Bluetooth names that some device models return from `AudioDeviceInfo.getProductName()`. On Android 12+, mind the `BLUETOOTH_CONNECT` permission.  
Parameters:
- `curName`: `String`, the Bluetooth name currently obtained.
- `context`: `Context`, the context.
- `callback`: `ValidBluetoothNameCallback`, the callback for the corrected name.

Returns: None (`void`).

## Enum AudioOutputDeviceType

| Enum value | Description |
| --- | --- |
| `UN_KNOW` | Unknown / triggers automatic selection according to the policy. |
| `SPEAKER` | Speaker. |
| `EARPIECE` | Earpiece. |
| `WIRED_EARPHONE` | Wired headset. |
| `BLUETOOTH_HEADSET` | Bluetooth headset. |

## Callback interfaces

### AudioRouterCallback
```java
public interface AudioRouterCallback {
    void exitOutputDeviceChange(HashMap<AudioOutputDeviceType, AudioDeviceInfo> audioOutputDevices);
    void activeOutputDeviceChange(Pair<AudioOutputDeviceType, AudioDeviceInfo> audioOutputDevice);
    void onAudioBecomingNoisy();
}
```
- `exitOutputDeviceChange`: The list of currently "selectable" output devices changed (headset plugged in or removed, Bluetooth connected or disconnected, and so on).
- `activeOutputDeviceChange`: The output device "actually in effect" changed; use this to show the current device in the UI.
- `onAudioBecomingNoisy`: The system may produce noise after a route switch (for example, when a headset is unplugged and audio switches to the speaker); you can pause playback or lower the volume here.

### ValidBluetoothNameCallback
```java
public interface ValidBluetoothNameCallback {
    void onValidBluetoothName(String name);
}
```
- `onValidBluetoothName`: Returns the corrected Bluetooth device name.
