---
title: "IRTCTrack"
description: "API reference for IRTCTrack, the base class of all Windows SRTC track objects: getTrackInfo returns the track's basic info (ID, desc, kind, codec, resolution, and more). Read to understand the track class hierarchy."
---

## Description
The track base class, providing the track's basic info object.



## Inheritance


## Methods
### Get track info
```cpp
virtual const StatusCode getTrackInfo(RTCTrackInfo* info) = 0;
```

**Returns**

| info | Track info parameters; see [Track info](/en/rtc/windows/types#track-info) |
| --- | --- |
