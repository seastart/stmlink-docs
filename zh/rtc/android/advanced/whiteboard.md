---
title: "白板接入"
description: "白板是一个 H5 页面，由 SRTC 在加入频道成功时通过 onJoinSucceed 下发链接；接入方用 WebView 加载并处理约定的交互事件。读它了解链接来源、WebView 配置、JS Bridge 与导出/插图等系统回调的处理"
---

白板本身是一个 H5 页面，绘制与协同逻辑都在 Web 端。接入方只需三步：**拿到链接 → 用 WebView 加载 → 处理约定的交互事件**。

<Note>
本页只讲 Android 端怎么把白板嵌进来。板子与频道的对应关系、白板何时被销毁、"谁开了白板"这个状态要怎么同步给其他人（SRTC **不会**自动广播），见 [电子白板](/zh/rtc/whiteboard)。
</Note>

## 1. 白板链接的来源

白板链接由 SRTC 在**加入频道成功**时下发，通过 `RTCClientEvent.onJoinSucceed` 回调的 `whiteBoard` 参数返回：

```kotlin
interface RTCClientEvent {
    /**
     * 自己加入频道成功
     * @param whiteBoard 白板链接，正常不为空；为 null 说明线路配置异常
     */
    fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?)
    // ...
}
```

接入方实现 `RTCClientEvent`（或继承 `RTCClientSimpleEvent` 只重写需要的方法），在回调里取出链接：

```kotlin
override fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?) {
    if (!whiteBoard.isNullOrEmpty()) {
        // whiteBoard 即白板链接，交给 WebView 加载
        openWhiteBoard(whiteBoard)
    }
}
```

> - 链接形如 `https://<接口域名>/white-board/?code=<会话凭证>&device_type=2&...`。**每人的链接不同**（`code` 是各自的会话凭证，一次性、连接后失效），但指向同一块板（板子 ID 取频道名）—— 所以别把链接转给别人用。
> - `whiteBoard` 正常不为空：白板首次有人进入时自动创建，无需预先开通；为空说明线路配置异常，此时别打开页面。

---

## 2. 如何使用（用 WebView 加载）

### 2.1 WebView 必需配置

```kotlin
val setting = webView.settings
setting.javaScriptEnabled = true                       // 必须：白板依赖 JS
setting.domStorageEnabled = true                       // 必须：白板依赖 DOM Storage
setting.databaseEnabled = true
setting.javaScriptCanOpenWindowsAutomatically = true
```

### 2.2 加载链接（追加控制参数）

加载时在链接后追加控制参数：

```kotlin
val param = "&no_menu=1&export_btn=1"
webView.loadUrl(whiteBoard + param)
```

| 参数 | 值 | 含义 |
|------|----|------|
| `no_menu` | `1` | 隐藏白板内置菜单 |
| `export_btn` | `1` | 显示"导出图片"按钮 |

> 参数以 `&` 拼接，依赖链接本身已带 query。按需选择是否追加：不需要导出功能可不传 `export_btn`，需要展示白板自带菜单可不传 `no_menu`。

### 2.3 注入 JS Bridge

白板通过一个固定名为 **`AndroidInterface`** 的 JS 接口与原生通信，必须在加载前注入：

```kotlin
webView.addJavascriptInterface(JsBridgeForWhiteboard(callback), "AndroidInterface")
```

JS Bridge 实现（可直接复用）：

```kotlin
class JsBridgeForWhiteboard(private val callback: Callback) {

    @JavascriptInterface
    fun onExportImage(dataUrl: String) {   // 白板导出图片
        callback.onExportImage(dataUrl)
    }

    @JavascriptInterface
    fun onWbDestroy(reason: String) {      // 白板销毁通知
        callback.onWbDestroy(reason)
    }

    interface Callback {
        fun onExportImage(dataUrl: String)
        fun onWbDestroy(reason: String)
    }
}
```

### 2.4 释放

页面销毁时释放 WebView：

```kotlin
override fun onDestroy() {
    super.onDestroy()
    webView.destroy()
}
```

---

## 3. 交互事件与指令

交互分三类：**① 原生 → 白板（URL 参数）**、**② 白板 → 原生（JS Bridge）**、**③ 白板对 WebView 系统能力的调用**。

### 3.1 原生 → 白板：URL 控制参数

加载时通过 URL query 传入（见 2.2），用于控制白板 UI：

| 参数 | 说明 |
|------|------|
| `no_menu=1` | 隐藏白板菜单 |
| `export_btn=1` | 显示导出按钮 |

### 3.2 白板 → 原生：JS Bridge 事件

接口对象名固定为 **`AndroidInterface`**，白板侧调用方式为 `window.AndroidInterface.<方法>(...)`。

| 方法 | 参数 | 触发时机 | 说明 |
|------|------|----------|------|
| `onExportImage(dataUrl)` | `dataUrl: String`，Base64 Data URL（形如 `data:image/png;base64,xxxx`） | 白板点击导出按钮 | 原生侧解析 Base64 并保存为图片（示例保存为 PNG 到系统相册；Android 9 及以下需先申请写存储权限） |
| `onWbDestroy(reason)` | `reason: String`，销毁原因 | 白板被销毁 | 原生侧可据此关闭页面或清理资源 |

`onExportImage` 保存图片的参考实现：

```kotlin
private fun saveBase64DataUrl(dataUrl: String) {
    val prefix = "base64,"
    val index = dataUrl.indexOf(prefix)
    if (index == -1) return
    val bytes = Base64.decode(dataUrl.substring(index + prefix.length), Base64.DEFAULT)
    // 将 bytes 写入相册 / 文件（Android 9 及以下先申请 WRITE 权限）
}
```

### 3.3 白板对 WebView 系统能力的调用

白板"插入图片""上传图片"等功能会触发 WebView 的系统回调，需在 `WebChromeClient` 中处理：

| 回调 | 需要做的处理 |
|------|--------------|
| `onPermissionRequest(request)` | 授予白板请求的能力（如相机、麦克风）：`request.grant(request.resources)` |
| `onShowFileChooser(...)` | 白板选取图片时触发，需弹出来源选择（拍照 / 相册），选取后通过 `filePathCallback.onReceiveValue(uris)` 回传给白板；取消时回传 `null` |

```kotlin
webView.webChromeClient = object : WebChromeClient() {
    override fun onPermissionRequest(request: PermissionRequest) {
        request.grant(request.resources)
    }

    override fun onShowFileChooser(
        webView: WebView?,
        filePathCallback: ValueCallback<Array<Uri>>?,
        params: FileChooserParams?
    ): Boolean {
        // 拍照 / 相册取图，得到 uri 后：
        // filePathCallback?.onReceiveValue(arrayOf(uri))
        // 用户取消：filePathCallback?.onReceiveValue(null)
        return true
    }
}
```

> 提示：白板对图片有大小限制，建议接入方在回传前对图片做压缩（例如压到 1MB 以内），避免过大图片上传失败。
