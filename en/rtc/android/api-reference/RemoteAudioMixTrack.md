---
title: "RemoteAudioMixTrack"
description: "Android remote mixed audio track API: startPlay and stopPlay turn local playback of remote audio on and off. Read when you need to control whether remote users' audio is played on the device."
---

## Description

`RemoteAudioMixTrack` controls local playback of the remote mixed audio track.

## RemoteAudioMixTrack methods

### startPlay()
```kotlin
fun startPlay()
```
Description: Starts playing remote audio (enables speaker output internally).  
Parameters: None.  
Returns: None (`Unit`).

### stopPlay()
```kotlin
fun stopPlay()
```
Description: Stops playing remote audio (disables speaker output internally).  
Parameters: None.  
Returns: None (`Unit`).
