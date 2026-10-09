---
title: "LocalCustomVideoTrack"
description: "Android local track for pushing external raw YUV (I420) video frames into a channel, for whiteboards, canvases, players, or third-party sources: the preOpt preset, inputData frame format requirements, publishing flow, and caveats. Read when publishing custom video on Android."
---

## Description

`LocalCustomVideoTrack` pushes external **raw YUV video frames** (such as a whiteboard, canvas, player output, or third-party capture source) into a published track. Get it through [`RTCEngine.getLocalCustomVideoTrack`](/en/rtc/android/api-reference/RTCEngine). It extends `LocalVideoTrack` and can be passed directly as the input track to `publishLocalVideo` / `unPublishLocalVideo`.

This page is the API reference; for the full integration flow, frame format conversion, and troubleshooting tips, see [Custom tracks](/en/rtc/android/advanced/custom-track).

The input is **unencoded** raw YUV (I420) frames. The SDK encodes them according to the preset parameters, so you don't need to encode them yourself.


## Properties

### preOpt
```kotlin
var preOpt: PreOptionCustomVideo
```
Description: The custom video preset used by this track (capture parameters + publish parameters); see [Custom video preset](/en/rtc/android/presets/custom-video).

- `preOpt.publish.desc` determines the track description of this track, and `inputData` also uses it to locate the target track.
- The SDK caches the track instance as a singleton: repeated calls to `getLocalCustomVideoTrack(preOpt)` return the same instance and overwrite it with the `preOpt` you pass. To distinguish between a "custom track" and a "screen sharing track", republish after switching presets instead of alternating frames between two `desc` values at the same time.

## LocalCustomVideoTrack methods

### inputData(yuv, width, height, strideY, strideU, strideV, rotation, stamp)
```kotlin
fun inputData(
    yuv: ByteArray, width: Int, height: Int,
    strideY: Int, strideU: Int, strideV: Int,
    rotation: Int, stamp: Long
)
```
Description: Pushes one frame of raw YUV data into the published custom video track. Internally, the SDK looks up the published track by `preOpt.publish.desc` and feeds the frame into the encoding pipeline; if the track isn't published yet, the frame is silently dropped.  
Parameters:

| Parameter | Data type | Description |
| --- | --- | --- |
| yuv | `ByteArray` | Tightly packed I420 data, at least `width * height * 3 / 2` bytes long. |
| width | `Int` | Frame width; must be even. |
| height | `Int` | Frame height; must be even. |
| strideY | `Int` | Row stride of the Y plane; pass `width`. |
| strideU | `Int` | Row stride of the U plane; pass `width / 2`. |
| strideV | `Int` | Row stride of the V plane; pass `width / 2`. |
| rotation | `Int` | Frame rotation angle, one of `0` / `90` / `180` / `270`, passed as frame metadata to the encoding and rendering side. |
| stamp | `Long` | Frame timestamp in **nanoseconds** (the same basis as Camera2's `timestampNs`). |

Returns: None (`Unit`).

#### Frame data format requirements

- **Must be tightly packed I420**: the `Y` plane of `width * height` bytes, immediately followed by the `U` plane of `(width/2) * (height/2)` bytes, then a `V` plane of the same size, with no gaps between the three segments.
- **`stride` must match the tightly packed layout** (`width`, `width/2`, `width/2`). The SDK currently computes plane offsets from the tightly packed layout, so passing row strides with padding causes misaligned or corrupted video. If upstream data has padding (for example, Camera2's `rowStride > width`), copy the valid pixels into a tightly packed array first.
- If the data is too short, an `IllegalArgumentException` (`Invalid I420 size`) is thrown before encoding.
- You don't need to align the resolution for the encoder: the SDK aligns and scales according to the device encoder's requirements; however, `width`/`height` must be even.
- You control the frame pacing. The frame rate and bitrate caps are determined by `preOpt`; pushing frames faster than the preset frame rate only adds unnecessary overhead.

## Rendering methods inherited from VideoTrack

`addPlayView` / `replacePlayView` / `removePlayView` / `removeAllPlayView` are provided by the base class `VideoTrack`, with the same signatures as [`LocalScreenTrack`](/en/rtc/android/api-reference/LocalScreenTrack).

> **Note**: The SDK **doesn't** echo frames sent through `inputData` to these render views (local echo only applies to camera tracks). For a local preview of custom video, draw from your data source yourself; you don't need to add render views to this track.

## Typical integration flow

```kotlin
// 1. Get the track (you can customize the preset; the default is PreOptionCustomVideo.def)
val customTrack = rtcEngine.getLocalCustomVideoTrack(PreOptionCustomVideo.def)

// 2. Publish the track; you can only push frames after publishing succeeds
rtcEngine.publishLocalVideo(customTrack, null, object : RTCResultListener {
    override fun onSuccess() {
        // 3. Keep pushing frames at your own pace (a single frame is shown here)
        customTrack.inputData(
            yuv = i420Bytes,          // Tightly packed I420
            width = 1920,
            height = 1080,
            strideY = 1920,
            strideU = 960,
            strideV = 960,
            rotation = 0,
            stamp = System.nanoTime()
        )
    }

    override fun onFail(code: Int, message: String) {
        // See the error codes page for error codes
    }
})

// 4. Stop pushing
rtcEngine.unPublishLocalVideo(customTrack, null)
```

To publish external video with the screen sharing track description (`TRACK_SHARE`), use `PreOptionCustomVideo.screen` instead, or override `desc` with `PublishCustomOptions(desc = ...)` when publishing:

```kotlin
val shareTrack = rtcEngine.getLocalCustomVideoTrack(PreOptionCustomVideo.screen)
rtcEngine.publishLocalVideo(shareTrack, null, null)
```

## Notes

- **Publish first, then push frames**: call `inputData` only after the `publishLocalVideo` success callback; otherwise frames are dropped without any notice.
- **Keep `desc` consistent**: if you override `desc` with `PublishCustomOptions` when publishing, the SDK writes it back to `preOpt.publish.desc`, and `inputData` still locates the track by the latest `desc`; don't keep a separate copy of the old `desc` in your code for decisions.
- **Publish/unpublish callbacks are coalesced**: as with the camera, when `publish`/`unpublish` are called in rapid succession, intermediate coalesced calls may not get a callback; rely on the callback of the last call or the final state.
- **Republish after leaving the channel**: `leave()` releases the media streaming engine. The track instance remains, but its publish state is no longer valid; after joining again, you must call `publishLocalVideo` again before pushing frames. `releaseSDK()` also clears the local track cache, after which you need to call `getLocalCustomVideoTrack` again.
- **Reuse input arrays**: `inputData` copies the data into the encoding buffer internally, so you can reuse the `ByteArray` as soon as the call returns. A buffer pool is recommended to reduce GC pressure.
