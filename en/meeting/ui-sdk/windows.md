---
title: "Windows UI SDK integration"
description: "Low-code integration with UI for Windows: the open-source SMeeting Windows meeting app (MSVC + Qt), its directory structure, how to integrate it as source code or as a DLL, screenshots, and the exported DemoControl functions and enums. Read this to embed a ready-made meeting UI in a Windows app."
---

This is the Windows client project of a video conferencing system that integrates the Windows SDK, built with MSVC + Qt.

GitHub source code: [https://github.com/seastart/meeting-windows-demo](https://github.com/seastart/meeting-windows-demo)

### Directory structure
```cpp
smeeting-windows-demo                   // C++ (Qt framework) demo
├─ BaseWindows							//Base classes for display windows
├─ CJsonObject            				// JSON parsing
├─ DataModel             				// Data entity types
├─ Global                 				// Global parameter configuration
├─ NetWork                				// Network
├─ res                    				// Resources
│  ├─ Images              				// Image resources
│  ├─ Qss              					// Default widget styles (CSS)
├─ SMeetingSdk							// SDK configuration
│  ├─ SMeetControl              		// Basic Meeting SDK call implementation
├─ Tools                  				// Tools
├─ View                  				// Views
│  ├─ Common              				// Common views
│  ├─ Home             					// Main window views
│  │  ├─ MainView             			// Main views in the main window: contacts, meeting list, meeting scheduling
│  │  ├─ ToolView						// Dialog views in the main window: meeting history, enter meeting, rename, create instant meeting
│  │  ├─ ToolWidgets             		// Small widget views in the main window
│  ├─ Login               				// Login views
│  ├─ Room	               				// In-meeting views
│  │  ├─ Chat							//In-meeting chat UI and logic
│  │  ├─ Invite							//In-meeting device invitation UI and logic
│  │  ├─ Mcu							//In-meeting recording and MCU layout UI and logic
│  │  ├─ Member							//In-meeting member control UI and logic
│  │  ├─ RoomMain						//Main in-meeting UI and logic
│  │  │  ├─ Layout						//In-meeting window layout
│  │  │  │  ├─ Auto						//In-meeting window layout - auto layout
│  │  │  │  ├─ Grid						//In-meeting window layout - grid layout
│  │  │  │  ├─ OneMore					//In-meeting window layout - large/small view layout
│  │  ├─ Setting						//In-meeting settings and quality monitoring UI and logic
│  │  ├─ Share							//In-meeting sharing window UI and logic
│  │  ├─ Tool							//In-meeting tool windows
│  ├─ Test                				// Test views
├─ MainWidget                			// Parent main window
├─ DemoControl                			// Shortcut method calls
```



### Integration options
#### Add the source code directly
This UI demo project is built as an MSVC + Qt project.

If you also develop with MSVC + Qt, you can copy the entire source code into your project, then use the methods provided in the shortcut method calls (`DemoControl.h`) to switch windows or call features (you can of course also modify the code to meet your needs)

Note: because QWKWidgets windows are used, call the following before `QApplication` is initialized

```cpp
QGuiApplication::setAttribute(Qt::AA_DontCreateNativeWidgetSiblings);
QApplication a(argc, argv);
...
reutrn a.exec();
```



#### Use the dynamic library
If you don't develop with MSVC + Qt, you can't add this source code to your project. Instead, you can use the compiled DLL and call the code in the program through dynamic library linking. (If you can't build it, contact us for the files.)

The methods in the shortcut method calls (`DemoControl.h`) are exported as C functions, so most developers can call them to launch this program.

Just load the dynamic library and import the exported function names to call them directly

```csharp
//C# loading (example)
[DllImport(DllPath, CallingConvention = CallingConvention.Cdecl, ExactSpelling = true)]
public static extern int MEETING_DEMO_Init();
```

### Screens and windows
#### Login screen
```cpp
Code directory
├─ View                  				// Views
│  ├─ Login             				// 
│  │  ├─ WidLogin             			// Login window view
```

![](/zh/meeting/ui-sdk/images/398177_1736990154109-b9440505-35f2-45a1-9eea-b506f9727ef4.png)



#### Main page
```cpp
Code directory
├─ View                  				// Views
│  ├─ Home             					// 
│  │  ├─ MainView             			// 
│  │  │  ├─ WidHome             		// Main page
│  │  │  ├─ WidInvite             		// Meeting scheduling
│  │  │  ├─ WidMeetingList             	// Meeting list
│  │  │  ├─ WidPhoneList             	// Contacts
```

![](/zh/meeting/ui-sdk/images/299698_1736990171509-d9c591c2-6a39-4c2d-a2f1-7f72d7fdf906.png)

##### Meeting list
![](/zh/meeting/ui-sdk/images/569215_1736990308491-accf3890-c16d-409c-9120-1bdc1fed553d.png)



##### Contacts
![](/zh/meeting/ui-sdk/images/265695_1736990436632-b5e34a9e-e622-4b21-a852-44da6c40e103.png)



#### In-meeting main screen
```cpp
Code directory
├─ View                  				// Views
│  ├─ Room	               				// In-meeting views
│  │  ├─ Chat							//In-meeting chat UI and logic
│  │  ├─ Invite							//In-meeting device invitation UI and logic
│  │  ├─ Mcu							//In-meeting recording and MCU layout UI and logic
│  │  ├─ Member							//In-meeting member control UI and logic
│  │  ├─ RoomMain						//Main in-meeting UI and logic
│  │  │  ├─ Layout						//In-meeting window layout
│  │  │  │  ├─ Auto						//In-meeting window layout - auto layout
│  │  │  │  ├─ Grid						//In-meeting window layout - grid layout
│  │  │  │  ├─ OneMore					//In-meeting window layout - large/small view layout
│  │  ├─ Setting						//In-meeting settings and quality monitoring UI and logic
│  │  ├─ Share							//In-meeting sharing window UI and logic
│  │  ├─ Tool							//In-meeting tool windows
```

![](/zh/meeting/ui-sdk/images/555421_1736990585079-5f917ad7-dd41-465f-b1b0-5e1efe1ec6a0.png)

##### Layout switching
![](/zh/meeting/ui-sdk/images/349898_1736990629898-3f37942e-d99c-4bba-ae68-fea68736bd79.png)

##### Member controls
![](/zh/meeting/ui-sdk/images/389780_1736990655323-47a06377-c71a-4152-8eb9-fcce5f06ae94.png)

##### Chat messages
![](/zh/meeting/ui-sdk/images/865365_1736990750526-71141b3c-7d16-42c8-a911-80f82186cbfc.png)



##### Recording layout settings
![](/zh/meeting/ui-sdk/images/783313_1736990840900-211e0b65-7ca8-4258-a28c-e04521199232.png)



##### Member & device invitation
![](/zh/meeting/ui-sdk/images/829876_1736994609639-f7129db6-64e5-4b89-b5cf-f2eeeb8e5786.png)

### Shortcut method calls
The project includes a `DemoControl` class so developers can quickly use this project (all methods in this class are exported, and developers can use them statically)

#### Settings parameter definitions
```csharp
#define MEETINGDEMO_SETTING_URL_S					0//Server address (string)
```

#### Window enum definitions
```csharp
#define MEETINGDEMO_VIEWTYPE_MAIN					1//Program main window
#define MEETINGDEMO_VIEWTYPE_MEETINGLIST			2//Meeting list
#define MEETINGDEMO_VIEWTYPE_MailList				3//Contacts
#define MEETINGDEMO_VIEWTYPE_ROOM_Chat				4//In-room chat window
#define MEETINGDEMO_VIEWTYPE_ROOM_MemberControl		5//In-room member control window
#define MEETINGDEMO_VIEWTYPE_ROOM_Setting			6//In-room settings & quality monitoring window
```

#### Layout enum definitions
```csharp
#define MEETINGDEMO_VIEWTYPE_Layout_AUTO		0//Auto layout
#define MEETINGDEMO_VIEWTYPE_Layout_1			1//1-grid view
#define MEETINGDEMO_VIEWTYPE_Layout_2			2
#define MEETINGDEMO_VIEWTYPE_Layout_4			4
#define MEETINGDEMO_VIEWTYPE_Layout_5			5
#define MEETINGDEMO_VIEWTYPE_Layout_6			6
#define MEETINGDEMO_VIEWTYPE_Layout_8			8
#define MEETINGDEMO_VIEWTYPE_Layout_9			9
#define MEETINGDEMO_VIEWTYPE_Layout_10			10
#define MEETINGDEMO_VIEWTYPE_Layout_12			12
#define MEETINGDEMO_VIEWTYPE_Layout_16			16
#define MEETINGDEMO_VIEWTYPE_Layout_25			25
#define MEETINGDEMO_VIEWTYPE_Layout_FULL		10000//Full-screen view (no paging buttons)
#define MEETINGDEMO_VIEWTYPE_Layout_L1_R4		1001  //1 left, 4 right

#define MEETINGDEMO_VIEWTYPE_Layout_B1_T4		1002  //1 top, 4 bottom

#define MEETINGDEMO_VIEWTYPE_Layout_LT1_BR7		1003  //1 top-left, 7 bottom-right

#define MEETINGDEMO_VIEWTYPE_Layout_BR1_LT7		1004  //1 bottom-right, 7 top-left
```

#### Methods
##### Initialize
```csharp
MEETING_DEMO_API int MEETING_DEMO_CALL MEETING_DEMO_Init();
```

Only initializes; no window is shown. To show a window, call

MEETING_DEMO_ShowView(MEETINGDEMO_VIEWTYPE_MAIN);

##### Release
```csharp
MEETING_DEMO_API int MEETING_DEMO_CALL MEETING_DEMO_Free();
```



##### SDK user login shortcuts
```csharp
MEETING_DEMO_API int MEETING_DEMO_CALL MEETING_DEMO_Login(const char* name,const char* pass);
MEETING_DEMO_API int MEETING_DEMO_CALL MEETING_DEMO_Login(const char* token);
```

###### Parameters
| name | Username |
| --- | --- |
| pass | Password |
| token | Token required for SDK login |


Note: after a successful call, if the UI window is already shown, it switches to the main window view

##### Global parameter configuration
```csharp
MEETING_DEMO_API int MEETING_DEMO_CALL MEETING_DEMO_SettingData(int tp,int idata,const char* sdata);
```

###### Parameters
| tp | Parameter type |
| --- | --- |


Note: after a successful call, if the UI window is already shown, it switches to the main window view



##### Switch windows
```csharp
MEETING_DEMO_API int MEETING_DEMO_CALL MEETING_DEMO_GotoView(int tp);
```

###### Parameters
| tp | Target window enum |
| --- | --- |


##### Show and hide windows
```csharp
MEETING_DEMO_API int MEETING_DEMO_CALL MEETING_DEMO_ShowView(int tp);
MEETING_DEMO_API int MEETING_DEMO_CALL MEETING_DEMO_HideView(int tp);
```

###### Parameters
| tp | Window enum |
| --- | --- |


Note: after initialization, the main screen is hidden by default. Call showView to show the main page; you can also show it by logging in and entering a meeting directly.

##### Update the window view
```csharp
MEETING_DEMO_API int MEETING_DEMO_CALL MEETING_DEMO_RoomUpdateLayout(int tp);
```

###### Parameters
| tp | View enum |
| --- | --- |




##### Get version information
```csharp
MEETING_DEMO_API void MEETING_DEMO_CALL RTCEngine_Version(const char* version);
```

###### Parameters
| version | Version information |
| --- | --- |


Note: `version` must be a pointer to already allocated memory of at least 100 bytes; this function only copies the version information.

