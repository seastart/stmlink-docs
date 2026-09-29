---
title: "Device management"
description: "Use DeviceManager in the SRTC Swift SDK to enumerate cameras and audio devices, switch devices, and handle hot-plugging and interruption recovery. For output routing control on iOS, see the Audio routing page."
---

### Overview

The Swift SDK abstracts device management into `DeviceManager.shared`, so you don't have to piece together platform differences from scratch for device enumeration, hot-plug monitoring, and audio session interruption handling.

Common needs include:

+ Enumerating cameras, microphones, and speakers
+ Letting the user switch devices manually
+ Monitoring device plug and unplug events
+ Recovering after an interruption on iOS such as an incoming call or Siri

---

### Enumerate devices

#### Enumerate cameras

```swift
let cameras = DeviceManager.shared.cameras()
```

#### macOS: enumerate microphones and speakers

```swift
let microphones = DeviceManager.shared.microphones()
let speakers = DeviceManager.shared.speakers()
```

#### iOS: enumerate audio input ports

```swift
let inputs = DeviceManager.shared.audioInputs()
```

This returns the **input ports** currently available to `AVAudioSession` (built-in microphone, Bluetooth, wired headset, and so on).

> iOS doesn't have the independent output device model of desktop systems, so this list **doesn't include the speaker**. "Whether sound comes out of the speaker or the receiver" is a separate mechanism—see [Audio routing](/en/rtc/swift/advanced/audio-routing).

#### Generic query

If you want to build a single device-picker UI layer, you can also use:

```swift
let allDevices = DeviceManager.shared.getDevices()
let camerasOnly = DeviceManager.shared.getDevices(kind: .videoInput)
```

---

### Switch cameras

For an existing `LocalCameraTrack`, you can switch to a specific device directly:

```swift
try await cameraTrack.changeDeviceId(deviceId)
```

To switch between the front and back cameras on iOS, use:

```swift
try await cameraTrack.switchCamera()
```

The key point: the switch happens inside the track object, so you don't need to create a new `LocalCameraTrack`.

---

### Switch microphones or audio routes

#### macOS

```swift
try micTrack.changeDeviceId(deviceId)
```

#### iOS

```swift
try micTrack.changeDeviceId(deviceId)
```

The call looks the same, but the meaning differs:

+ macOS: switches the input device
+ iOS: switches the **input port** (`AVAudioSession.setPreferredInput`); `deviceId` comes from `audioInputs()`

<Warning>
On iOS this method only handles input. It **can't be used to switch between the speaker and the receiver**, and it doesn't accept values like `"speaker"`. For output, use `AudioRouteSession.shared.setAudioRoute(_:)`—see [Audio routing](/en/rtc/swift/advanced/audio-routing).

Also, this path doesn't take part in the audio routing module's fallback policy, and the switch isn't recorded as an "explicit user choice".
</Warning>

---

### Switch speakers on macOS

On macOS, output device switching goes through `DeviceManager`:

```swift
try DeviceManager.shared.setOutputDevice(deviceId)
```

This is separate from microphone switching because the output device isn't bound to `LocalMicTrack`; it's bound to the output path of the underlying audio module.

---

### Monitor device changes

Register a listener through `DeviceManagerDelegate`:

```swift
final class DeviceState: DeviceManagerDelegate {
    init() {
        DeviceManager.shared.delegates.add(delegate: self)
    }

    func deviceManager(_ manager: DeviceManager, didAddDevice device: DeviceInfo) {
        print("device added:", device.name)
    }

    func deviceManager(_ manager: DeviceManager, didRemoveDevice device: DeviceInfo) {
        print("device removed:", device.name)
    }
}
```

Recommended approach:

+ In the callback, only refresh the local device list state
+ Have the UI layer update its dropdown or picker automatically based on the new device list

---

### Automatic recovery built into the SDK

The Swift SDK already handles several common recovery cases internally:

+ When the camera in use is unplugged, it tries to switch to an available camera
+ On macOS, when the microphone in use is unplugged, it tries to switch back to the default input
+ On iOS, after the audio session is interrupted by an incoming call or similar, it recovers when conditions allow (including waiting for the system call to end and retrying on failure—see [Audio routing](/en/rtc/swift/advanced/audio-routing))
+ On iOS, camera capture can recover when the app returns to the foreground after going to the background

This means you usually don't need to build a full set of fault-tolerance logic yourself, but we still recommend that you:

+ Show error messages to the user
+ Refresh the UI after the device list changes
+ Don't cache stale `deviceId` values

---

### Recommended approach in your app

Recommended approach:

+ Call `refreshDeviceList()` when the page initializes
+ Save the currently selected `deviceId`
+ After a device change, if the original `deviceId` no longer exists, fall back to the default device automatically

This matters because in hot-plug scenarios, "an old device ID still lingering in local state" is the root cause of many switching failures.
