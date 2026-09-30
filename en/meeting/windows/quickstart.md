---
title: "C++ quickstart"
description: "Step-by-step C++ code for the SMeeting Windows SDK: initialize the engine, log in, create a meeting, create an ISMeetingChannel and enter, control the camera, microphone, speaker, and screen sharing, host actions, MCU playback, and cleanup. Read this after integration to get a first meeting running."
---

This page shows how to integrate the SMeeting SDK with C++ on Windows.

## Basic concepts

+ **ISMeetingEngine**: the SDK engine class. It handles login, the meeting management HTTP APIs, device enumeration, IM, the resource drive, and the channel object lifecycle.
+ **ISMeetingChannel**: each meeting corresponds to one channel object, created by `ISMeetingEngine::createChannel()`. It contains all in-meeting operations and media objects.
+ Some APIs can only be called after you enter the meeting.

Because `ISMeetingEngine` / `ISMeetingChannel` and the callbacks are all pure virtual interfaces, **any change to an API signature changes the vtable**. After upgrading the SDK you must recompile your project; replacing only the DLLs is not enough.

---

## Initialize the SDK

```cpp
#include "SMeeting.h"

// Initialize the engine
SMeeting::ISMeetingEngine* engine = nullptr;
SMeeting::StatusCode ret = SMeeting::SMeetingEngine_Init(&engine);
if (ret != SMeeting::StatusCode::OK) {
    return ret;
}

// Set the engine-level event handler (the current class must inherit ISMeetingEngineEvent)
engine->setEventHandler(this);
```

### Implement the engine event handler class

```cpp
class MyEngineHandler : public SMeeting::ISMeetingEngineEvent {
public:
    void onDeviceChange(SMeeting::DeviceType tp, bool isadd, std::string name) override {
        // Handle device changes
    }

    void onImEnabled(std::string uid, std::string sid) override {
        // IM is enabled
    }

    // ... Implement the other engine-level callbacks you need
};
```

---

## Log in and log out

### Log in

```cpp
std::string token = "your_token_here";
engine->login(token, [&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // Login succeeded
    } else {
        // Login failed
    }
});
```

### Log out

```cpp
engine->logout([&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // Logout succeeded
    }
});
```

---

## Create a meeting

```cpp
SMeeting::SMeetingCreateMeetingModel model;
model.title = "My meeting";
model.content = "Meeting description";
model.meeting_type = 1;  // 1: instant meeting, 2: scheduled meeting
model.meeting_mode = 1;  // 1: normal

engine->createRoom(model, [&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // msg is the meeting number
        std::cout << "Meeting created, meeting number: " << msg << std::endl;
    }
});
```

---

## Enter a meeting

### Create and configure the channel object

```cpp
std::string roomno = "123456789";
SMeeting::ISMeetingChannel* channel = nullptr;
SMeeting::StatusCode sc = engine->createChannel(roomno, &channel);
if (sc != SMeeting::StatusCode::OK) {
    return;
}

// Set the channel-level configuration
SMeeting::ISMeetingChannelSetting* csetting = nullptr;
channel->getSetting(&csetting);
if (csetting) {
    csetting->set_stream_model(1);           // Set the streaming mode
    csetting->set_speaker_interval(500);     // Audio level callback interval (ms)
    csetting->set_stat_interval(10000);      // Network statistics callback interval (ms)
    csetting->set_enable_audio_record(1);    // Enable audio recording
    csetting->set_room_name("Alice");         // Display name for entering the meeting
}
```

### Set the channel event handler and enter

```cpp
// Set the channel-level event handler (the current class must inherit ISMeetingChannelEvent)
channel->setEventHandler(this);

// Enter the meeting
std::string pass = "";  // Meeting password; empty if there is none
channel->enter(pass, [&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // Entered the room successfully
    } else {
        // Failed to enter the room; you still need to call leaveChannel to release the object
    }
});
```

### Implement the channel event handler class

```cpp
class MyChannelHandler : public SMeeting::ISMeetingChannelEvent {
public:
    void onDisconnected(SMeeting::DisconnectReason reason,
                        SMeeting::StatusCode code,
                        std::string message) override {
        // Handle the disconnect event
    }

    void onReconnected() override {
        // Reconnected
    }

    void onUserEnter(std::string userdata) override {
        // Handle a user entering
    }

    // ... Implement the other channel-level callbacks you need
};
```

---

## Exit the meeting

```cpp
// The channel object is destroyed after you exit; don't use the original pointer again
engine->leaveChannel(channel->getChannelId(), [&](SMeeting::StatusCode status, std::string msg) {
    // Result of exiting the room
});
channel = nullptr;
```

---

## End the meeting (host)

```cpp
// The host ends the meeting
channel->adminDestroyRoom([&](SMeeting::StatusCode status, std::string msg) {
    // Result of ending the meeting
});
```

---

## Cancel a meeting (outside the meeting)

```cpp
std::string meeting_id = "sw46gz";
engine->cancelRoom(meeting_id, [&](SMeeting::StatusCode status, std::string msg) {
    // Result of canceling the meeting
});
```

---

## Get room and member info

```cpp
std::string s;

// Get your own info
channel->getMe(s);

// Get the room info
channel->getRoom(s);

// Get info for all members
channel->getMembers(s);

// Get info for a specific member
std::string uid = "user_123";
channel->getMember(uid, s);
```

---

## Update your nickname

```cpp
std::string new_name = "New nickname";
channel->updateName(new_name, [&](SMeeting::StatusCode status, std::string msg) {
    // Result of changing the nickname
});
```

---

## Get the device list

```cpp
// type: 1 = microphone, 2 = speaker, 3 = camera
std::vector<int> types = {1, 2, 3};
int page = 1;
std::string find_key = "";

engine->listAgent(types, page, find_key, [&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // msg is the device list as a JSON string
    }
});
```

---

## Camera operations

### Get the camera object

```cpp
SMeeting::IMEETLocalCamera* camera = nullptr;
SMeeting::StatusCode sc = channel->getLocalCamera(&camera);
if (sc != SMeeting::StatusCode::OK) {
    return;
}
```

### Turn on the camera

```cpp
// Set the render window (hwnd is the window handle)
camera->addPlayView(hwnd);

// Request to turn on the camera
camera->requestOpenCamera([&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // Camera turned on
    }
});
```

### Switch cameras

```cpp
std::string camera_name = "Integrated Camera";
int width = 640;
int height = 480;
camera->switchCamera(camera_name, width, height);
```

### Turn off the camera

```cpp
camera->closeCamera([&](SMeeting::StatusCode status, std::string msg) {
    // Result of turning off the camera
});
```

---

## Remote video playback

### Get the remote video object

```cpp
std::string uid = "user_123";
std::string track_desc = SMeeting::TRACK_DESC_CAMERA_BIG;  // Or TRACK_DESC_CAMERA_SMALL

SMeeting::IMEETRemoteVideo* remote_video = nullptr;
channel->getRemoteVideo(uid, track_desc, &remote_video);
```

### Start playback

```cpp
// Set the render window
remote_video->addPlayView(hwnd);

// Start loading the remote video stream
remote_video->loadRemoteVideo();
```

### Stop playback

```cpp
remote_video->unLoadRemoteVideo();
remote_video->removeAllPlayView();
```

---

## Microphone operations

### Get the microphone object

```cpp
SMeeting::IMEETLocalMic* mic = nullptr;
channel->getLocalMic(&mic);
```

### Turn on the microphone

```cpp
mic->requestOpenMic([&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // Microphone turned on
    }
});
```

### Switch microphones

```cpp
std::string mic_name = "Default Microphone";
mic->switchMic(mic_name);
```

### Turn off the microphone

```cpp
mic->closeMic([&](SMeeting::StatusCode status, std::string msg) {
    // Result of turning off the microphone
});
```

---

## Speaker operations

### Get the remote audio object

```cpp
SMeeting::IMEETRemoteAudio* audio = nullptr;
channel->getRemoteAudio("", &audio);
```

### Turn on the speaker

```cpp
audio->openSpeaker();
```

### Switch speakers

```cpp
std::string speaker_name = "Default Speakers";
audio->switchSpeaker(speaker_name);
```

### Turn off the speaker

```cpp
audio->closeSpeaker();
```

---

## Screen sharing

### Get the screen sharing object

```cpp
SMeeting::IMEETLocalScreen* screen = nullptr;
channel->getLocalScreen(&screen);
```

### Start sharing

```cpp
// tp: 1 = screen sharing, 2 = window sharing
// data: screen index or window handle string
int tp = 1;
std::string data = "0,0,1920,1080";  // Primary screen
//std::string data_hwnd = "hwnd:123321";//Window capture

screen->requestShare(tp, data, [&](SMeeting::StatusCode status, std::string msg) {
    if (status == SMeeting::StatusCode::OK) {
        // Sharing started
    }
});
```

### Stop sharing

```cpp
screen->stopShare([&](SMeeting::StatusCode status, std::string msg) {
    // Result of stopping sharing
});
```

---

## Chat messages

### Send a chat message

```cpp
// tp: 1 = text, 2 = file, 3 = image, 4 = audio
int msg_type = 1;
std::string msg = "Hello, everyone!";

channel->sendRoomChatMessage(msg_type, msg, [&](SMeeting::StatusCode status, std::string m) {
    // Send result
});
```

---

## Host management APIs

### Ask a member to turn on the camera

```cpp
std::string uid = "user_123";
channel->adminRequestUserOpenCamera(uid, [&](SMeeting::StatusCode status, std::string msg) {
    // Request result
});
```

### Turn off a member's camera

```cpp
channel->adminCloseUserCamera(uid, [&](SMeeting::StatusCode status, std::string msg) {
    // Operation result
});
```

### Ask a member to turn on the microphone

```cpp
channel->adminRequestUserOpenMic(uid, [&](SMeeting::StatusCode status, std::string msg) {
    // Request result
});
```

### Turn off a member's microphone

```cpp
channel->adminCloseUserMic(uid, [&](SMeeting::StatusCode status, std::string msg) {
    // Operation result
});
```

### Remove a member

```cpp
channel->adminKickUserOut(uid, [&](SMeeting::StatusCode status, std::string msg) {
    // Removal result
});
```

### Set the room's microphone permissions

```cpp
bool self_unmute_mic_disabled = true;   // Whether members are prevented from unmuting themselves
bool mic_disabled = true;               // Whether room audio is disabled

channel->adminUpdateRoomMicState(self_unmute_mic_disabled, mic_disabled, 
    [&](SMeeting::StatusCode status, std::string msg) {
        // Result of the setting
    });
```

---

## MCU composite video

### Get the MCU video object

```cpp
SMeeting::IMEETRemoteVideo* mcu_video = nullptr;
channel->getMcuVideo(&mcu_video);
```

### Play the composite stream

```cpp
mcu_video->addPlayView(hwnd);
mcu_video->loadRemoteVideo();
```

### Stop playback

```cpp
mcu_video->unLoadRemoteVideo();
```

---

## Release resources

```cpp
// First exit all meetings
engine->leaveAllChannel();

// Release the engine
if (engine) {
    engine->del();
    engine = nullptr;
}
```

---

## Complete example

```cpp
#include "SMeeting.h"
#include <iostream>

class MyEngineHandler : public SMeeting::ISMeetingEngineEvent {
public:
    void onDeviceChange(SMeeting::DeviceType tp, bool isadd, std::string name) override {
        // Handle device changes
    }

    void onImEnabled(std::string uid, std::string sid) override {
        // IM is enabled
    }
};

class MyChannelHandler : public SMeeting::ISMeetingChannelEvent {
public:
    void onDisconnected(SMeeting::DisconnectReason reason,
                        SMeeting::StatusCode code,
                        std::string message) override {
        std::cout << "Disconnected: " << (int)code << std::endl;
    }

    void onUserEnter(std::string userdata) override {
        std::cout << "User entered: " << userdata << std::endl;
    }

    // Implement the other callbacks you need...
};

int main() {
    // Initialize the engine
    SMeeting::ISMeetingEngine* engine = nullptr;
    SMeeting::StatusCode ret = SMeeting::SMeetingEngine_Init(&engine);
    if (ret != SMeeting::StatusCode::OK) {
        return -1;
    }

    MyEngineHandler engine_handler;
    engine->setEventHandler(&engine_handler);

    // Log in
    std::string token = "your_token";
    engine->login(token, [&](SMeeting::StatusCode status, std::string msg) {
        if (status != SMeeting::StatusCode::OK) {
            return;
        }

        // Create a meeting
        SMeeting::SMeetingCreateMeetingModel model;
        model.title = "Test meeting";
        engine->createRoom(model, [&](SMeeting::StatusCode status, std::string roomno) {
            if (status != SMeeting::StatusCode::OK) {
                return;
            }

            // Create the channel object
            SMeeting::ISMeetingChannel* channel = nullptr;
            engine->createChannel(roomno, &channel);
            if (!channel) {
                return;
            }

            MyChannelHandler channel_handler;
            channel->setEventHandler(&channel_handler);

            // Enter the meeting
            channel->enter("", [&](SMeeting::StatusCode status, std::string msg) {
                if (status == SMeeting::StatusCode::OK) {
                    std::cout << "Entered the meeting" << std::endl;
                }
            });
        });
    });

    // Wait for the asynchronous operations to complete (a real app should have an event loop)
    std::this_thread::sleep_for(std::chrono::seconds(30));

    // Clean up
    engine->logout();
    engine->del();

    return 0;
}
```
