---
title: "MCU APIs"
description: "C++ MCU APIs of the SMeeting Windows SDK on ISMeetingChannel: start and stop the MCU composite video with layout data, and get the MCU recording configuration and recording details."
---

All of the following APIs are called on [ISMeetingChannel](/en/meeting/windows/api-reference/smeeting-channel).

---

## Start the MCU
```cpp
virtual StatusCode mcuStart(std::string laydata, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| laydata | std::string | Layout data |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Stop the MCU
```cpp
virtual StatusCode mcuStop(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## MCU recording configuration
```cpp
virtual StatusCode mcuRecordConfig(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## MCU recording details
```cpp
virtual StatusCode mcuRecordDetail(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code
