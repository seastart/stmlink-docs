---
title: "BoardShareCallback"
description: "发起白板共享后的成功/失败回调，成功时返回白板对象"
---

说明：`BoardShareCallback` 是白板共享结果回调接口，用于反馈发起白板共享的成功或失败。

## 回调方法

### onSucceed(whiteBoard)
```kotlin
fun onSucceed(whiteBoard: String)
```
方法说明：发起白板共享成功回调。  
参数说明：
- `whiteBoard`：`String`，白板共享信息。
返回值说明：无（`Unit`）。

### onFail(code, message)
```kotlin
fun onFail(code: Int, message: String?)
```
方法说明：发起白板共享失败回调。  
参数说明：
- `code`：`Int`，Meeting 自产错误为 `202xxx`，上游错误保留原始值。
- `message`：`String?`，面向开发者的诊断信息，不保证可以直接展示给用户。
返回值说明：无（`Unit`）。
