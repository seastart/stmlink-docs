---
title: "Sign-in APIs"
description: "C++ sign-in APIs of the SMeeting Windows SDK on ISMeetingChannel: list, create, and finish sign-in activities, get statistics and details, sign in as a member, and export sign-in details to a file."
---

All of the following APIs are called on [ISMeetingChannel](/en/meeting/windows/api-reference/smeeting-channel).

---

## Sign-in list
```cpp
virtual StatusCode signinList(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Create a sign-in
```cpp
virtual StatusCode signinCreate(int dt, std::string desc, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| dt | int | Sign-in duration |
| desc | std::string | Sign-in description |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Sign-in statistics
```cpp
virtual StatusCode signinCount(std::string, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| (unnamed) | std::string | Sign-in ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Finish the sign-in
```cpp
virtual StatusCode signinFinish(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Sign-in details
```cpp
virtual StatusCode signinDetail(std::string id, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| id | std::string | Sign-in ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Sign in
```cpp
virtual StatusCode signinSign(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Export sign-in details
```cpp
virtual StatusCode signinExportDetail(std::string epoch, std::string outFile) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| epoch | std::string | Timestamp |
| outFile | std::string | Output file path |

**Returns**

`StatusCode` - Error code
