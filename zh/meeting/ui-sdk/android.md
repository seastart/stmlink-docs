---
title: "Android UI SDK 极简对接"
description: "SMeeting Android UI 套件快速集成指南"
---

## 集成方式
带 UI 的库主要是通过导入代码的方式集成，可以整体集成，也可以模块/组件集成

github源码地址：[https://github.com/seastart/meeting-andriod-demo](https://github.com/seastart/meeting-andriod-demo)

### 整体集成
+ 在根目录下的 build.gradle 中，添加 maven

```plain
allprojects {
    repositories {
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
    }
}
```typescript

+ 引入 StmLink 库
+ 在app目录下的build.gradle中添加依赖

```plain
dependencies {
    implementation project(path: ':StmLink')
}
```

### 模块/组件集成
+ 在根目录下的 build.gradle 中，添加 maven

```plain
allprojects {
    repositories {
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
    }
}
```typescript

+ 在app目录下的build.gradle中添加依赖

```plain
	dependencies {
    implementation 'cn.seastart.meeting:meeting:xxx'
	}
```

+ 将需要的模块或者组件从 StmLink 库拷贝到项目工程中使用



## 整体集成
1. 新建项目，按照[《集成方式》文档中整体集成](https://www.yuque.com/anyconf/eanoso/qyxl89y40h1097y9#wNe8z)方式导入 StmLink 库
2. 新建 MyApplication，在 MyApplication 中实现如下代码

```kotlin
override fun onCreate() {
    super.onCreate()
    // 执行库的初始化操作
    SeaStarClient.instance.SSC_Init(this)
    // 注册监听 activity 的生命周期比变化
    registerActivityLifecycleCallbacks(MyLifecycleCallback())
}
```typescript

3. 在 MainActivity 中执行跳转操作，跳转到 StmLink 库中的界面

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
        ...
    Handler().postDelayed(
        {
            SeaStarClient.instance.SSC_StartHomeActivity(this@MainActivity)
            finish()
        }, 1000)
}
```

4. activity 生命周期变化监听具体实现，其中 LifecycleListener 类是 StmLink 中的内容

```kotlin
class MyLifecycleCallback: Application.ActivityLifecycleCallbacks {

    private val lifecycleListener = LifecycleListener()

    override fun onActivityCreated(activity: Activity, savedInstanceState: Bundle?) {
        lifecycleListener.onActivityCreated(activity, savedInstanceState)
    }

    override fun onActivityStarted(activity: Activity) {
        lifecycleListener.onActivityStarted(activity)
    }

    override fun onActivityResumed(activity: Activity) {
        lifecycleListener.onActivityResumed(activity)
    }

    override fun onActivityPaused(activity: Activity) {
        lifecycleListener.onActivityPaused(activity)
    }

    override fun onActivityStopped(activity: Activity) {
        lifecycleListener.onActivityStopped(activity)
    }

    override fun onActivitySaveInstanceState(activity: Activity, outState: Bundle) {
        lifecycleListener.onActivitySaveInstanceState(activity, outState)
    }

    override fun onActivityDestroyed(activity: Activity) {
        lifecycleListener.onActivityDestroyed(activity)
    }
}
```typescript

## 模块/组件集成
### 项目结构
模块分类：基础模块、登录模块、会议外信息模块、入会模块、会中模块

```kotlin
stmlink/
├── aboutUs/                # 关于我们
├── activity/               # activity 包
├── authorize/              # 登录和注册模块
│   └── login/                # 登录功能相关
│   └── register/             # 注册功能相关
├── base/                   # BaseActivity 和 BaseFragment
├── contactDetail/          # 联系人详情
├── history/                # 历史会议
├── home/                   # home 页
│   └── contact/              # 联系人列表页
│   └── meet/                 # 待加入会议列表页
│   └── mine/                 # 我的页面
├── http/                   # http 模块
├── inviteMember/           # 邀请成员模块
├── meetDetail/             # 会议详情
├── meeting/                # 会中模块
│   └── chat/                 # 聊天页面
│   └── member/               # 会中成员页面
│   └── room/                 # 会中主页
├── preMeetingRoom/         # 加入会议模块
├── service/                # 服务相关
├── ui/                     # 自定义 UI
├── utils/                  # 工具类
└── webPage/                # 网页相关
```

### 基础模块
基础模块包括 SDK 调用入口类、网络请求包、自定义 UI 包、工具类包。

#### 引入
分别将 cn.seastart.stmlink 路径下的 MeetingEngineHelper 文件、http 文件夹、ui 文件夹、utils 文件夹 拷贝到项目目录下，即可使用。

```kotlin
stmlink/
├── http/                   # http 模块
├── ui/                     # 自定义 UI
├── utils/                  # 工具类
└── MeetingEngineHelper     # sdk 统一调用帮助类
```typescript

#### 使用说明
##### sdk 入口文件使用
```kotlin
/**
 * 创建 sdk
 */
MeetingEngineHelper.instance.createSDK(application)

/**
 * 初始化 sdk
 */
MeetingEngineHelper.instance.initSDK(token, null,
            object : MeetingResultCallback {
                override fun onFail(code: Int, errorMsg: String?, showMsg: String?) {
                    // 具体操作
                }

                override fun onSuccess() {
                    // 具体操作
                }
            }
        )

/**
 * 释放资源
 */
MeetingEngineHelper.instance.release()


/**
 * 其他接口调用
 */
```

##### 网络请求模块使用
```kotlin
/**
 * 在应用启动时调用该方法初始化网络请求模块
 * url：主机地址
 */
ApiHelper.instance.init(url)

/**
 * 重置主机地址，重置后的地址存在 KvUtil 中的 DOMAIN_URL 字段中
 */
ApiHelper.instance.resetHost()

/**
 * 释放资源
 */
ApiHelper.instance.release()


/**
 * 各种网络请求接口
 */
```typescript

##### 自定义 ui 包使用
其中包含各种在项目中使用到的自定义组件，可以通过在 xml 布局文件中引入的方式使用

##### 工具包使用
其中包含各种在项目中使用到的工具类，基本是静态方法或者单例模式。

### 登录注册模块
登录注册模块主要包括：登录页、注册页、成员信息修改页

这是一个很重要的模块，没有实现登录，后续所有操作都无法被正确执行。

在这个模块中实现了 应用登录授权、Meet授权、初始化 SDK 组件、初始化 IM 组件。

应用登录授权执行完成后，会获得一个 应用层的用户 token，所有应用层的网络请求，都必须将这个 token 放入请求头

#### 引入
+ 将 cn.seastart.stmlink 路径下的 authorize 文件夹 拷贝到项目目录下，即可使用

```kotlin
stmlink/
├── authorize/              # 登录和注册模块
│   └── login/                # 登录功能相关
│   └── register/             # 注册功能相关
```

#### 使用说明
##### 界面跳转
```kotlin
/**
 * 跳转到登录界面
 */
LoginActivity.startActivity(this)
```typescript

##### SdkLoginHelper 工具说明
+ 在这个类中统一实现登录功能，主要步骤包括：授权->sdk登录->im登录，该类功能依赖于 MeetingEngineHelper（这是应用层封装的 sdk 入口类），一定要先初始化完成 MeetingEngineHelper
+ 由于存在 应用授权 token 已存在，需要自动登录 sdk 的场景，可以通过该类在任意界面实现登录功能

```kotlin
SdkLoginHelper.instance.login(object : SdkLoginHelper.LoginListener {
            override fun onSuccess() {
                // 具体操作
            }

            override fun onFail(code: Int, errorMsg: String?, showMsg: String?) {
                // 具体操作
            }
        })
```

#### 界面展示
| 登录页面 | 注册页面 | 信息修改页面 |
| :---: | :---: | :---: |
| ![](images/744263_1736944793072-53ac0392-65f6-4de1-a00d-ff077aad3817.png) | ![](images/351786_1736944827362-f8db82db-6e7f-4542-a02c-04105a70b17b.png) | ![](images/668188_1736944864362-a7e9fdc6-7307-4910-8df1-719d16cb5663.png) |


### 会议外信息模块
会议外信息模块主要包括：待参加会议展示页、历史会议展示页、会议详情页、联系人列表页、联系人详情页、我的信息页

#### 引入
+ 将 cn.seastart.stmlink 路径下的 Home 包、history 包、meetDetail 包、contactDetail 包 拷贝到项目中，即可使用

```kotlin
stmlink/
├── contactDetail/          # 联系人详情
├── history/                # 历史会议
├── home/                   # home 页
│   └── contact/              # 联系人列表页
│   └── meet/                 # 待加入会议列表页
│   └── mine/                 # 我的页面
├── meetDetail/             # 会议详情
```typescript

#### 使用说明
```kotlin
/**
 * 跳转到 Home 页面，Home 页面包括 待参加会议展示页、联系人列表页、我的信息页
 */
HomeActivity.startActivity(this)

/**
 * 跳转到 历史会议展示页
 */
 HistoryActivity.startHistoryListPage(this)

 /**
  * 跳转到 会议详情页
  * meetId：会议 id
  */
 MeetDetailActivity.startMeetDetailPage(this, meetId)

 /**
  * 跳转到 联系人详情页
  * uid：联系人 uid
  */
 ContactDetailActivity.startContactInfoPage(requireContext(), uid)
```

#### 界面展示
| 待参加会议页面 | 历史会议页面 |
| :---: | :---: |
| ![](images/931388_1736945720654-1d76831c-ab48-4851-99a0-4173bbef861c.png) | ![](images/594150_1736945795062-e39c5dfd-8ff2-4c02-8e4d-044eb2620c19.png) |


| 会议详情页面 | 会议详情页面 |
| :---: | :---: |
| ![](images/531412_1736945837121-71798d95-d38e-4a04-913d-270f57130e39.png) | ![](images/624938_1736945869039-76b0e4e8-e732-484d-a6a5-b06438f09f7a.png) |


| 通讯录页面 | 联系人详情页面 | 联系人信息修改页面 |
| :---: | :---: | :---: |
| ![](images/459351_1736945902308-925c8a8a-3d35-432e-82ef-3db652719fca.png) | ![](images/451994_1736945920675-323a546f-499f-4806-a8a6-639dee9c02f3.png) | ![](images/305696_1736946154201-8de1fb5a-e78d-44e7-a5c7-17901b05273c.png) |


| 我的页面 |
| :---: |
| ![](images/739182_1736946192641-eb7cdab9-8124-4384-beb1-523e95ad6163.png) |


### 入会模块
入会模块主要包括：加入会议页、创建即时会议页、创建预约会议页、成员邀请页

加入会议和创建即时会议页，默认往会中页面跳转；创建预约会议页，默认往待参加会议展示页跳转

#### 引入
+ 将 cn.seastart.stmlink 路径下的 preMeetingRoom 包、inviteMember 包 拷贝到项目中，即可使用。

```kotlin
stmlink/
├── inviteMember/           # 邀请成员模块
├── preMeetingRoom/         # 加入会议模块
```typescript

#### 使用说明
```kotlin
/**
 * 跳转到 加入会议页
 */
PreMeetingActivity.startJoinMeetingPage(this)

/**
 * 跳转到 创建即时会议页
 */
PreMeetingActivity.startCreateImmediateMeetingPage(this)

/**
 * 跳转到 创建预约会议页，预约会议页内可以跳转到成员邀请页
 */
PreMeetingActivity.startCreateScheduleMeetingPage(requireContext())
```

#### 界面展示
| 加入会议页面 | 创建即时会议页面 | 创建预约会议页面 |
| :---: | :---: | :---: |
| ![](images/905399_1736946306264-2044c730-4b2e-47e8-a8c6-17ae59b2f42c.png) | ![](images/446908_1736946327653-2d577ec6-c7d4-412a-a2ed-17219e5164c5.png) | ![](images/916464_1736946352239-e9497d24-a919-479c-bd91-2d33717b4432.png) |


| 已邀请与会人页面 | 邀请与会人页面 |
| :---: | :---: |
| ![](images/669378_1736946395548-62c217b1-0ae8-4091-b77b-fe10322e3c13.png) | ![](images/143749_1736946420344-72ef19f8-c8bd-4f2b-8e44-768fc471a39a.png) |


### 会中模块
会中模块主要包括：会议主页、参会成员列表页、邀请成员入会页、聊天信息页

会议主页中包括：单成员页面、多成员页面、共享页面、合成会议页面，质量监测数据窗口

退出会议主页时，默认退到 Home 页面

#### 引入
+ 将 cn.seastart.stmlink 路径下的 inviteMember 包、Meeting 包 拷贝到项目中，即可使用

```kotlin
stmlink/
├── inviteMember/           # 邀请成员模块
├── meeting/                # 会中模块
│   └── chat/                 # 聊天页面
│   └── member/               # 会中成员页面
│   └── room/                 # 会中主页
```typescript

#### 使用说明
```kotlin
/**
 * 跳转到 会议主页
 * roomNo：会议号
 * name：自己的昵称
 * avatar：自己的头像
 * isOpenCamera：是否打开摄像头
 * isOpenMic：是否打开麦克风
 */
MeetingRoomActivity.startMeetingRoomPage(
    this, roomNo, name, avatar, 
    isOpenCamera, isOpenMic
)
```

#### 界面展示
| 单成员页面 | 单成员页面 | 多成员页面 |
| :---: | :---: | :---: |
| ![](images/434319_1736946547704-bf943bf3-a043-43ee-98e6-bc898426378b.png) | ![](images/411149_1736946570490-bb32711c-51d4-421c-9a9d-5b2cc2b4d53d.png) | ![](images/414643_1736946608353-a42a5c9b-6a34-459d-9f42-3daa57ac1b6b.png) |


| 屏幕共享页面 | 音频路由切换弹窗 | 质量监测弹窗 |
| :---: | :---: | :---: |
| ![](images/231961_1736946694685-f81eada2-2624-4e5c-8c94-40d67e5008b5.png) | ![](images/106920_1736946770437-af821add-48e0-4b79-8b3e-7aeaf1803b78.png) | ![](images/783592_1736946794109-32ae3463-737a-4d75-8776-ed508983f458.png) |


| 主持人的参会成员页面 | 主持人操作弹窗 | 普通成员的参会成员页面 |
| :---: | :---: | :---: |
| ![](images/624984_1736946871871-3ee962a4-543d-4594-b1bd-9ca7a59490c4.png) | ![](images/535563_1736946892788-18f7f40b-dd2d-4990-8d70-b791e8d57026.png) | ![](images/567341_1736946932791-72620c07-d57b-4bc1-8632-4de90e084680.png) |


| 聊天页面 | 文件选择页面 |
| :---: | :---: |
| ![](images/653822_1736947186593-92048d8e-03c9-4ebe-ad9e-c164221e478f.png) | ![](images/473907_1736995103180-dfa5baa6-f94a-4ba5-aa36-42d641bc84bf.jpeg) |


