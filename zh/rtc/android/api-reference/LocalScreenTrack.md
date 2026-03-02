+ 提供屏幕共享相关操作
+ 为 publishLocalVideo 提供配置参数

### setEvent()
设置录屏状态回调

```kotlin
fun setEvent(event: RTCScreenStateEvent)
```

参数

| event | RTCScreenStateEvent 事件接口 |
| --- | --- |


RTCScreenStateEvent 接口

| onScreenStateChanged | 说明：录屏状态改变<br/>参数：<br/>eventId：事件类型<br/>VCS_EVENT_TYPE.ScreenRecordError：录屏出错<br/>VCS_EVENT_TYPE.ScreenRecordStart：录屏开始<br/>VCS_EVENT_TYPE.ScreenRecordStop：录屏结束<br/>args：事件描述 |
| --- | --- |


### request()
请求录屏权限

```kotlin
fun request(result: (Boolean, Intent?) -> Unit)
```

参数

| result | 函数型参数，用于返回录屏权限请求结果。<br/>Boolean：是否获得录屏权限<br/>Intent：录屏功能所需的数据，startCapture 函数会用到 |
| --- | --- |


### setRecordNotification()
设置录屏通知栏样式

```kotlin
fun setRecordNotification(smallIcon: Int, title: String?, desc: String?, buttonText: String?)
```

参数

| smallIcon | 通知栏中的小图标 |
| --- | --- |
| title | 通知栏中的标题内容 |
| desc | 通知栏中的描述内容 |
| buttonText | 通知栏中的按钮文案 |


### startCapture()
根据指定参数类型开始屏幕采集

```kotlin
fun startCapture(intent: Intent, hasBar:Boolean)
```

参数：

| intent | Intent 类型数据，从 request 函数中获取到的值 |
| --- | --- |
| hasBar | Boolean 类型，是否需要显示通知栏 |


### stopCapture()
停止屏幕采集

```kotlin
fun stopCapture()
```

