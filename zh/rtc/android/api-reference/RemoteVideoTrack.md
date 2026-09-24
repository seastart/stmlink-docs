---
title: "RemoteVideoTrack"
description: "远端视频轨道：画面渲染与接收卡顿状态监听"
---

## 说明

`RemoteVideoTrack` 用于远端视频渲染与远端流状态监听。

## RemoteVideoTrack 自身方法

### setRemoteVideoEvent(event)
```kotlin
fun setRemoteVideoEvent(event: RTCRemoteVideoEvent)
```
方法说明：设置远端视频流状态监听，并注册全局时钟检测。  
参数说明：
- `event`：`RTCRemoteVideoEvent`，远端流状态事件回调实现。
返回值说明：无（`Unit`）。

状态触发说明：
- 订阅后连续约 3 秒未收到有效帧时，回调 `isChoke = true`。
- 收到有效帧并恢复后，回调 `isChoke = false`。

### removeRemoteVideoEvent()
```kotlin
fun removeRemoteVideoEvent()
```
方法说明：移除远端流状态监听，并取消全局时钟检测。  
参数说明：无。  
返回值说明：无（`Unit`）。

## 继承自 VideoTrack 的渲染方法

### addPlayView(view)
```kotlin
fun addPlayView(view: View): Boolean
```
方法说明：添加单个渲染控件。仅支持 `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView`。  
参数说明：
- `view`：`View`，渲染控件。
返回值说明：`Boolean`，`true` 表示添加成功；类型不支持或重复添加时为 `false`。

### replacePlayView(views)
```kotlin
fun replacePlayView(views: MutableList<View>)
```
方法说明：替换全部渲染控件列表。  
参数说明：
- `views`：`MutableList<View>`，渲染控件集合，仅支持 `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView`。
返回值说明：无（`Unit`）。

### removePlayView(view)
```kotlin
fun removePlayView(view: View)
```
方法说明：移除指定渲染控件。  
参数说明：
- `view`：`View`，目标渲染控件。
返回值说明：无（`Unit`）。

### removeAllPlayView()
```kotlin
fun removeAllPlayView()
```
方法说明：移除全部渲染控件。  
参数说明：无。  
返回值说明：无（`Unit`）。

## RTCRemoteVideoEvent 回调接口

`RTCRemoteVideoEvent` 为远端视频流状态回调接口，通过 `setRemoteVideoEvent(event)` 注册。

### onReceiveStreamStatusChange(channel, uid, trackDesc, isChoke)
```kotlin
fun onReceiveStreamStatusChange(
    channel: String,
    uid: String,
    trackDesc: String,
    isChoke: Boolean
)
```
方法说明：远端视频流状态变化回调。  
参数说明：
- `channel`：`String`，远端流所属频道 ID。
- `uid`：`String`，远端用户 ID。
- `trackDesc`：`String`，轨道描述。
- `isChoke`：`Boolean`，是否卡顿；`true` 为卡顿，`false` 为恢复正常。
返回值说明：无（`Unit`）。

## 视频渲染控件

视频显示使用 SDK 提供的 `VcsPlayerGlTextureView` 或 `VcsPlayerGlSurfaceView`。以下用法同时适用于远端视频显示与本地摄像头预览：

```kotlin
import cn.seastart.rtc.media.original.render.VcsPlayerGlTextureView
import cn.seastart.rtc.media.original.render.VcsPlayerGlSurfaceView
import cn.seastart.rtc.media.original.render.RenderConstants

val view = VcsPlayerGlTextureView(context)
view.setViewScaleType(RenderConstants.CENTERINSIDE)
remoteTrack.addPlayView(view)
```

XML 示例：

```xml
<cn.seastart.rtc.media.original.render.VcsPlayerGlTextureView
    android:layout_width="match_parent"
    android:layout_height="match_parent" />
```

应用应随页面生命周期调用控件的 `onResume()` / `onPause()`；不用时先从轨道移除控件，再调用 `onDestroy()` 释放渲染资源。销毁后的控件不要复用。轨道负责送帧，正常订阅或摄像头预览无需自行调用 `updateFrame`。

### 显示配置

以下接口在两种控件上均可使用，返回值均为 `Unit`：

```kotlin
fun customDisplayCtrl(use: Boolean)
fun setViewRotate(rotateAngle: Int)
fun setViewflip(flipX: Boolean, flipY: Boolean)
fun setViewScaleType(ScaleType: Int)
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `use` | Boolean | 是 | 默认 `false`，使用帧自身方向及 SDK 的预览镜像配置；`true` 使用当前控件的自定义旋转和翻转。 |
| `rotateAngle` | Int | 是 | 自定义显示角度，正值为逆时针，传 `0/90/180/270` 或其整圈等价值。覆盖帧方向，不与帧方向累加；默认 `0`。 |
| `flipX` / `flipY` | Boolean | 是 | 自定义模式下沿显示坐标水平 / 垂直翻转；默认均为 `false`，不叠加默认前置镜像。 |
| `ScaleType` | Int | 是 | 使用下表 `RenderConstants` 缩放常量；正常模式和自定义模式均可设置，默认 `CENTERINSIDE`。 |

旋转、翻转和模式切换从**下一帧**生效；没有新帧时不会改变已显示帧。缩放方式可作用于当前画面。配置仅属于当前控件，不改变推送给远端的视频。

| 缩放常量 | 值 | 效果 |
| --- | --- | --- |
| `FITXY` | 0 | 拉伸填满控件，可能改变比例。 |
| `CENTERCROP` | 1 | 等比填满并居中裁剪。 |
| `CENTERINSIDE` | 2 | 等比完整显示并居中，可能留边。 |
| `FITSTART` | 3 | 等比完整显示，沿留边方向靠左 / 靠上。 |
| `FITEND` | 4 | 等比完整显示，沿留边方向靠右 / 靠下。 |

### updateFrame(y, u, v, width, height, format, rotationDegrees)

仅在应用直接向渲染控件提交原始帧时使用：

```kotlin
fun updateFrame(
    y: ByteArray?, u: ByteArray?, v: ByteArray?,
    width: Int, height: Int, format: Int, rotationDegrees: Int
)
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `y` | ByteArray | 是 | 紧密排列的 Y 平面，至少 `width × height` 字节。 |
| `u` | ByteArray | 是 | I420 的 U 平面，至少 `width × height / 4` 字节；NV12 / NV21 的交错 UV / VU 平面，至少 `width × height / 2` 字节。 |
| `v` | ByteArray? | I420 必填 | I420 的 V 平面，至少 `width × height / 4` 字节；NV12 / NV21 可传 `null`。 |
| `width` / `height` | Int | 是 | 原始像素宽高，均为正偶数，不传旋转后的宽高；不支持行尾 padding。 |
| `format` | Int | 是 | `YuvFormat.I420`、`NV12` 或 `NV21`，完整常量见 [类型定义](/zh/rtc/android/types)。 |
| `rotationDegrees` | Int | 是 | 像素仍需执行的**顺时针**旋转：`0/90/180/270` 或其整圈等价值。 |

返回值：`Unit`。帧数据在方法返回前复制，之后应用可复用数组。无效尺寸、数据长度、像素格式或非 90 度整数倍角度会使本帧被拒绝，保留上一帧；没有单独的失败回调。自定义模式会覆盖帧方向，但传入帧角度仍必须合法。
