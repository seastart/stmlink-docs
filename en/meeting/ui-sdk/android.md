---
title: "Android UI SDK integration"
description: "Low-code integration with UI for Android: import the open-source `StmLink` meeting UI library as a whole or copy individual modules (base, login, out-of-meeting info, meeting entry, in-meeting), with setup code, entry points, and screenshots. Read this to add a meeting UI to your app."
---

## Integration options
The UI library is integrated mainly by importing its source code. You can integrate it as a whole, or by module/component.

GitHub source code: [https://github.com/seastart/meeting-andriod-demo](https://github.com/seastart/meeting-andriod-demo)

### Whole integration
+ Add the Maven repository to the `build.gradle` in the root directory

```text
allprojects {
    repositories {
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
    }
}
```

+ Import the `StmLink` library
+ Add the dependency to the `build.gradle` in the `app` directory

```text
dependencies {
    implementation project(path: ':StmLink')
}
```

### Module/component integration
+ Add the Maven repository to the `build.gradle` in the root directory

```text
allprojects {
    repositories {
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
    }
}
```

+ Add the dependency to the `build.gradle` in the `app` directory

```text
	dependencies {
    implementation 'cn.seastart.meeting:meeting:xxx'
	}
```

+ Copy the modules or components you need from the `StmLink` library into your project



## Whole integration
1. Create a new project and import the `StmLink` library as described in [Whole integration](#whole-integration)
2. Create `MyApplication` and implement the following code in it

```kotlin
override fun onCreate() {
    super.onCreate()
    // Initialize the library
    SeaStarClient.instance.SSC_Init(this)
    // Register a listener for activity lifecycle changes
    registerActivityLifecycleCallbacks(MyLifecycleCallback())
}
```

3. In `MainActivity`, navigate to a screen in the `StmLink` library

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

4. Implement the activity lifecycle listener. The `LifecycleListener` class comes from `StmLink`

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
```

## Module/component integration
### Project structure
Modules: base module, login module, out-of-meeting info module, meeting entry module, and in-meeting module

```kotlin
stmlink/
├── aboutUs/                # About us
├── activity/               # Activity package
├── authorize/              # Login and registration module
│   └── login/                # Login
│   └── register/             # Registration
├── base/                   # BaseActivity and BaseFragment
├── contactDetail/          # Contact details
├── history/                # Meeting history
├── home/                   # Home page
│   └── contact/              # Contact list page
│   └── meet/                 # Upcoming meetings list page
│   └── mine/                 # "Me" page
├── http/                   # HTTP module
├── inviteMember/           # Member invitation module
├── meetDetail/             # Meeting details
├── meeting/                # In-meeting module
│   └── chat/                 # Chat page
│   └── member/               # In-meeting members page
│   └── room/                 # In-meeting main page
├── preMeetingRoom/         # Meeting entry module
├── service/                # Services
├── ui/                     # Custom UI
├── utils/                  # Utilities
└── webPage/                # Web pages
```

### Base module
The base module includes the SDK entry class, the network request package, the custom UI package, and the utilities package.

#### Import
Copy the `MeetingEngineHelper` file and the `http`, `ui`, and `utils` folders under the `cn.seastart.stmlink` path into your project directory, and they are ready to use.

```kotlin
stmlink/
├── http/                   # HTTP module
├── ui/                     # Custom UI
├── utils/                  # Utilities
└── MeetingEngineHelper     # Unified SDK helper class
```

#### Usage
##### Using the SDK entry file
```kotlin
/**
 * Create the SDK
 */
MeetingEngineHelper.instance.createSDK(application)

/**
 * Initialize the SDK
 */
MeetingEngineHelper.instance.initSDK(token, null,
            object : MeetingResultCallback {
                override fun onFail(code: Int, errorMsg: String?, showMsg: String?) {
                    // Your handling
                }

                override fun onSuccess() {
                    // Your handling
                }
            }
        )

/**
 * Release resources
 */
MeetingEngineHelper.instance.release()


/**
 * Other API calls
 */
```

##### Using the network request module
```kotlin
/**
 * Call this at app startup to initialize the network request module
 * url: host address
 */
ApiHelper.instance.init(url)

/**
 * Reset the host address; the reset address is stored in the DOMAIN_URL field of KvUtil
 */
ApiHelper.instance.resetHost()

/**
 * Release resources
 */
ApiHelper.instance.release()


/**
 * Various network request APIs
 */
```

##### Using the custom UI package
It contains the custom components used in the project, which you can use by referencing them in XML layout files

##### Using the utilities package
It contains the utility classes used in the project, mostly static methods or singletons.

### Login and registration module
The login and registration module mainly includes the login page, the registration page, and the member profile editing page

This is an important module: without login, none of the subsequent operations can run correctly.

This module implements app login authorization, Meet authorization, SDK initialization, and IM initialization.

After app login authorization completes, you get an app-layer user token. Every app-layer network request must include this token in its request headers

#### Import
+ Copy the `authorize` folder under the `cn.seastart.stmlink` path into your project directory, and it is ready to use

```kotlin
stmlink/
├── authorize/              # Login and registration module
│   └── login/                # Login
│   └── register/             # Registration
```

#### Usage
##### Navigation
```kotlin
/**
 * Navigate to the login screen
 */
LoginActivity.startActivity(this)
```

##### SdkLoginHelper
+ This class implements login in one place. The main steps are: authorization -> SDK login -> IM login. It depends on `MeetingEngineHelper` (the SDK entry class wrapped at the app layer), so `MeetingEngineHelper` must be initialized first
+ When an app authorization token already exists and the SDK needs to log in automatically, you can use this class to log in from any screen

```kotlin
SdkLoginHelper.instance.login(object : SdkLoginHelper.LoginListener {
            override fun onSuccess() {
                // Your handling
            }

            override fun onFail(code: Int, errorMsg: String?, showMsg: String?) {
                // Your handling
            }
        })
```

#### Screenshots
| Login page | Registration page | Profile editing page |
| :---: | :---: | :---: |
| ![](/zh/meeting/ui-sdk/images/744263_1736944793072-53ac0392-65f6-4de1-a00d-ff077aad3817.png) | ![](/zh/meeting/ui-sdk/images/351786_1736944827362-f8db82db-6e7f-4542-a02c-04105a70b17b.png) | ![](/zh/meeting/ui-sdk/images/668188_1736944864362-a7e9fdc6-7307-4910-8df1-719d16cb5663.png) |


### Out-of-meeting info module
The out-of-meeting info module mainly includes the upcoming meetings page, the meeting history page, the meeting details page, the contact list page, the contact details page, and the "Me" page

#### Import
+ Copy the `Home`, `history`, `meetDetail`, and `contactDetail` packages under the `cn.seastart.stmlink` path into your project, and they are ready to use

```kotlin
stmlink/
├── contactDetail/          # Contact details
├── history/                # Meeting history
├── home/                   # Home page
│   └── contact/              # Contact list page
│   └── meet/                 # Upcoming meetings list page
│   └── mine/                 # "Me" page
├── meetDetail/             # Meeting details
```

#### Usage
```kotlin
/**
 * Navigate to the Home page, which includes the upcoming meetings page, the contact list page, and the "Me" page
 */
HomeActivity.startActivity(this)

/**
 * Navigate to the meeting history page
 */
 HistoryActivity.startHistoryListPage(this)

 /**
  * Navigate to the meeting details page
  * meetId: meeting ID
  */
 MeetDetailActivity.startMeetDetailPage(this, meetId)

 /**
  * Navigate to the contact details page
  * uid: contact uid
  */
 ContactDetailActivity.startContactInfoPage(requireContext(), uid)
```

#### Screenshots
| Upcoming meetings page | Meeting history page |
| :---: | :---: |
| ![](/zh/meeting/ui-sdk/images/931388_1736945720654-1d76831c-ab48-4851-99a0-4173bbef861c.png) | ![](/zh/meeting/ui-sdk/images/594150_1736945795062-e39c5dfd-8ff2-4c02-8e4d-044eb2620c19.png) |


| Meeting details page | Meeting details page |
| :---: | :---: |
| ![](/zh/meeting/ui-sdk/images/531412_1736945837121-71798d95-d38e-4a04-913d-270f57130e39.png) | ![](/zh/meeting/ui-sdk/images/624938_1736945869039-76b0e4e8-e732-484d-a6a5-b06438f09f7a.png) |


| Contacts page | Contact details page | Contact editing page |
| :---: | :---: | :---: |
| ![](/zh/meeting/ui-sdk/images/459351_1736945902308-925c8a8a-3d35-432e-82ef-3db652719fca.png) | ![](/zh/meeting/ui-sdk/images/451994_1736945920675-323a546f-499f-4806-a8a6-639dee9c02f3.png) | ![](/zh/meeting/ui-sdk/images/305696_1736946154201-8de1fb5a-e78d-44e7-a5c7-17901b05273c.png) |


| "Me" page |
| :---: |
| ![](/zh/meeting/ui-sdk/images/739182_1736946192641-eb7cdab9-8124-4384-beb1-523e95ad6163.png) |


### Meeting entry module
The meeting entry module mainly includes the enter meeting page, the create instant meeting page, the create scheduled meeting page, and the member invitation page

The enter meeting and create instant meeting pages go to the in-meeting page by default; the create scheduled meeting page goes to the upcoming meetings page by default

#### Import
+ Copy the `preMeetingRoom` and `inviteMember` packages under the `cn.seastart.stmlink` path into your project, and they are ready to use.

```kotlin
stmlink/
├── inviteMember/           # Member invitation module
├── preMeetingRoom/         # Meeting entry module
```

#### Usage
```kotlin
/**
 * Navigate to the enter meeting page
 */
PreMeetingActivity.startJoinMeetingPage(this)

/**
 * Navigate to the create instant meeting page
 */
PreMeetingActivity.startCreateImmediateMeetingPage(this)

/**
 * Navigate to the create scheduled meeting page, from which you can go to the member invitation page
 */
PreMeetingActivity.startCreateScheduleMeetingPage(requireContext())
```

#### Screenshots
| Enter meeting page | Create instant meeting page | Create scheduled meeting page |
| :---: | :---: | :---: |
| ![](/zh/meeting/ui-sdk/images/905399_1736946306264-2044c730-4b2e-47e8-a8c6-17ae59b2f42c.png) | ![](/zh/meeting/ui-sdk/images/446908_1736946327653-2d577ec6-c7d4-412a-a2ed-17219e5164c5.png) | ![](/zh/meeting/ui-sdk/images/916464_1736946352239-e9497d24-a919-479c-bd91-2d33717b4432.png) |


| Invitees page | Add invitees page |
| :---: | :---: |
| ![](/zh/meeting/ui-sdk/images/669378_1736946395548-62c217b1-0ae8-4091-b77b-fe10322e3c13.png) | ![](/zh/meeting/ui-sdk/images/143749_1736946420344-72ef19f8-c8bd-4f2b-8e44-768fc471a39a.png) |


### In-meeting module
The in-meeting module mainly includes the meeting main page, the member list page, the invite members page, and the chat page

The meeting main page includes the single-member view, the multi-member view, the screen sharing view, the composite meeting view, and the quality monitoring data window

When you exit the meeting main page, you return to the Home page by default

#### Import
+ Copy the `inviteMember` and `Meeting` packages under the `cn.seastart.stmlink` path into your project, and they are ready to use

```kotlin
stmlink/
├── inviteMember/           # Member invitation module
├── meeting/                # In-meeting module
│   └── chat/                 # Chat page
│   └── member/               # In-meeting members page
│   └── room/                 # In-meeting main page
```

#### Usage
```kotlin
/**
 * Navigate to the meeting main page
 * roomNo: room number
 * name: your own nickname
 * avatar: your own avatar
 * isOpenCamera: whether to turn on the camera
 * isOpenMic: whether to turn on the mic
 */
MeetingRoomActivity.startMeetingRoomPage(
    this, roomNo, name, avatar, 
    isOpenCamera, isOpenMic
)
```

#### Screenshots
| Single-member view | Single-member view | Multi-member view |
| :---: | :---: | :---: |
| ![](/zh/meeting/ui-sdk/images/434319_1736946547704-bf943bf3-a043-43ee-98e6-bc898426378b.png) | ![](/zh/meeting/ui-sdk/images/411149_1736946570490-bb32711c-51d4-421c-9a9d-5b2cc2b4d53d.png) | ![](/zh/meeting/ui-sdk/images/414643_1736946608353-a42a5c9b-6a34-459d-9f42-3daa57ac1b6b.png) |


| Screen sharing view | Audio routing dialog | Quality monitoring dialog |
| :---: | :---: | :---: |
| ![](/zh/meeting/ui-sdk/images/231961_1736946694685-f81eada2-2624-4e5c-8c94-40d67e5008b5.png) | ![](/zh/meeting/ui-sdk/images/106920_1736946770437-af821add-48e0-4b79-8b3e-7aeaf1803b78.png) | ![](/zh/meeting/ui-sdk/images/783592_1736946794109-32ae3463-737a-4d75-8776-ed508983f458.png) |


| Member list page (host) | Host actions dialog | Member list page (regular member) |
| :---: | :---: | :---: |
| ![](/zh/meeting/ui-sdk/images/624984_1736946871871-3ee962a4-543d-4594-b1bd-9ca7a59490c4.png) | ![](/zh/meeting/ui-sdk/images/535563_1736946892788-18f7f40b-dd2d-4990-8d70-b791e8d57026.png) | ![](/zh/meeting/ui-sdk/images/567341_1736946932791-72620c07-d57b-4bc1-8632-4de90e084680.png) |


| Chat page | File picker page |
| :---: | :---: |
| ![](/zh/meeting/ui-sdk/images/653822_1736947186593-92048d8e-03c9-4ebe-ad9e-c164221e478f.png) | ![](/zh/meeting/ui-sdk/images/473907_1736995103180-dfa5baa6-f94a-4ba5-aa36-42d641bc84bf.jpeg) |
