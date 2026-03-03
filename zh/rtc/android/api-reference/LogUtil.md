---
title: "LogUtil"
description: "Android SRTC 音视频 SDK LogUtil 接口参考"
---

用户日志收集，使用该日志工具，可以将日志打印到控制台、本地文件、远端日志中心

### v()
收集 VERBOSE 日志

```kotlin
fun v(msg: String, tag: String = TAG)
```kotlin

参数

| msg | String 类型，消息内容 |
| --- | --- |
| tag | String 类型，tag。 |


### d()
收集 DEBUG 日志

```kotlin
fun d(msg: String, tag: String = TAG)
```

参数

| msg | String 类型，消息内容 |
| --- | --- |
| tag | String 类型，tag。 |


### i()
收集 INFO 日志

```kotlin
fun i(msg: String, tag: String = TAG)
```kotlin

参数

| msg | String 类型，消息内容 |
| --- | --- |
| tag | String 类型，tag。 |


### w()
收集 WARN 日志

```kotlin
fun w(msg: String, tag: String = TAG)
```

参数

| msg | String 类型，消息内容 |
| --- | --- |
| tag | String 类型，tag。 |


### e()
收集 ERROR 日志

```java
fun e(msg: String, tag: String = TAG)
```kotlin

参数

| msg | String 类型，消息内容 |
| --- | --- |
| tag | String 类型，tag。 |


### e()
收集 ERROR 日志

```java
fun e(t: Throwable, tag: String = TAG)
```

参数

| t | Throwable 类型，异常信息 |
| --- | --- |
| tag | String 类型，tag。 |


### addFormatLog()
收集格式化日志

```java
fun addFormatLog(type: String, attr: Any?, 
                 body: String?, 
                 level: LoggerLevel = LoggerLevel.Info)
```kotlin

参数

| type | String 类型，消息内容 |
| --- | --- |
| attr | Any 类型，可 json 化的日志内容 |
| body | String 类型，日志内容 |
| level | LoggerLevel 枚举类型，日志等级 |


LoggerLevel 属性说明

| 枚举名称 | 值 | 说明 |
| --- | --- | --- |
| Undefined | 0 | 未定义 |
| Trace | 1 | 跟踪日志等级 |
| Debug | 5 | 调试日志等级 |
| Info | 9 | 信息日志等级 |
| Warn | 13 | 警告日志等级 |
| Error | 17 | 错误日志等级 |
| FATAL | 21 | 致命错误日志等级 |


