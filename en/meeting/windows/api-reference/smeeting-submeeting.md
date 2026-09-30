---
title: "Sub-meeting APIs"
description: "C++ sub-meeting APIs of the SMeeting Windows SDK on ISMeetingChannel: create sub-meetings under a main meeting, rename them, assign and move members, list, start, stop, and delete them, and ask the host for help from inside a sub-meeting."
---

All of the following APIs are called on [ISMeetingChannel](/en/meeting/windows/api-reference/smeeting-channel).

---

## Create sub-meetings
```cpp
virtual StatusCode createSubMeeting(std::string par_meet_id, std::vector<std::string> title, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| par_meet_id | std::string | Main meeting ID |
| title | `std::vector<std::string>` | List of sub-meeting titles |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Update a sub-meeting title
```cpp
virtual StatusCode updateSubMeetingTitle(std::string sub_id, std::string newTitle, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| sub_id | std::string | Sub-meeting ID |
| newTitle | std::string | New title |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Update sub-meeting members
```cpp
virtual StatusCode updateSubMeetingUsers(std::string sub_id, std::vector<SMeetingMeetingAttachments> users, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| sub_id | std::string | Sub-meeting ID |
| users | `std::vector<SMeetingMeetingAttachments>` | List of members |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Delete sub-meetings
```cpp
virtual StatusCode deleteSubMeeting(std::vector<std::string> sub_id, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| sub_id | `std::vector<std::string>` | List of sub-meeting IDs |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Get the sub-meeting list
```cpp
virtual StatusCode getSubMeetingList(std::string meet_id, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| meet_id | std::string | Meeting ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Start sub-meetings
```cpp
virtual StatusCode startSubMeeting(std::vector<std::string> sub_id, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| sub_id | `std::vector<std::string>` | List of sub-meeting IDs |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Stop sub-meetings
```cpp
virtual StatusCode stopSubMeeting(std::vector<std::string> sub_id, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| sub_id | `std::vector<std::string>` | List of sub-meeting IDs |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Move a sub-meeting member
```cpp
virtual StatusCode moveSubMeetingUser(std::string uid, std::string src_sub_id, std::string des_sub_id, Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| uid | std::string | User ID |
| src_sub_id | std::string | Source sub-meeting ID |
| des_sub_id | std::string | Target sub-meeting ID |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code

## Ask for help
```cpp
virtual StatusCode helpSubMeeting(Callback back = NULL) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| back | Callback | Asynchronous callback |

**Returns**

`StatusCode` - Error code
