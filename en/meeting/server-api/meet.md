---
title: "Meeting management"
description: "Meeting scheduling before and after the meeting: create, update, cancel, and query meetings, plus attendance records and chat history"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the meeting-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Configure event notifications

`POST /server/v1/meet/set-callback`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Configure callback settings

**Request parameters**

<ParamField body="events" type="array<string>">
  Events to subscribe to
</ParamField>

<ParamField body="cb_url" type="string">
  Callback URL
</ParamField>


Request example:

```json
{
  "cb_url": "",
  "events": [
    ""
  ]
}
```

**Response parameters**

<ResponseField name="data" type="string">
  Response data
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": ""
}
```

---

## List meetings

`POST /server/v1/meet/list-meet`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Meeting list

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="meeting_ids" type="array<string>">
  Meeting ID list
</ParamField>

<ParamField body="meeting_type" type="integer">
  Filter by meeting type. 1: instant meeting, 2: scheduled meeting
</ParamField>

<ParamField body="meeting_status" type="array<integer>">
  Filter by meeting status, multiple allowed. 1: not started, 2: in progress, 3: ended
</ParamField>

<ParamField body="creator" type="string">
  Filter by creator user ID
</ParamField>

<ParamField body="begin_at" type="integer">
  Start time
</ParamField>

<ParamField body="end_at" type="integer">
  End time
</ParamField>

<ParamField body="plan_begin_at" type="integer">
  Range of scheduled meeting start time
</ParamField>

<ParamField body="plan_end_at" type="integer">
  Range of scheduled meeting start time
</ParamField>

<ParamField body="plan_time" type="integer">
  Start time (timestamp); required for scheduled meetings
</ParamField>

<ParamField body="sort" type="string">
  Sort order. Sortable field: created_at; prefix - for descending order (sortable fields: created_at)
</ParamField>

<ParamField body="page" type="integer">
  Page number, starting from 1
  Example: `1`
</ParamField>

<ParamField body="per-page" type="integer">
  Items per page
  Example: `10`
</ParamField>


Request example:

```json
{
  "begin_at": 0,
  "creator": "",
  "end_at": 0,
  "meeting_id": "",
  "meeting_ids": [
    ""
  ],
  "meeting_status": [
    0
  ],
  "meeting_type": 0,
  "page": 1,
  "per-page": 10,
  "plan_begin_at": 0,
  "plan_end_at": 0,
  "plan_time": 0,
  "room_no": "",
  "sort": ""
}
```

**Response parameters**

<ResponseField name="id" type="string">
  Meeting ID
</ResponseField>

<ResponseField name="room_no" type="string">
  Room number
</ResponseField>

<ResponseField name="title" type="string">
  Meeting title
</ResponseField>

<ResponseField name="content" type="string">
  Meeting description
</ResponseField>

<ResponseField name="meeting_status" type="integer">
  Meeting status. 1: not started, 2: in progress, 3: ended
</ResponseField>

<ResponseField name="attend_type" type="integer">
  1: unrestricted (default), 2: password required, 3: invitees only
</ResponseField>

<ResponseField name="meeting_type" type="integer">
  Meeting type. 1: instant meeting, 2: scheduled meeting
</ResponseField>

<ResponseField name="plan_time" type="integer">
  Start time (timestamp); required for scheduled meetings
</ResponseField>

<ResponseField name="plan_dur" type="integer">
  Duration (minutes); required for scheduled meetings
</ResponseField>

<ResponseField name="begin_time" type="integer">
  Start time
</ResponseField>

<ResponseField name="end_time" type="integer">
  End time
</ResponseField>

<ResponseField name="last_exit_time" type="integer">
  Timestamp when the last member exited; 0 if the meeting has not ended
</ResponseField>

<ResponseField name="entry_mute_policy" type="integer">
  Mute-on-entry option
</ResponseField>

<ResponseField name="watermark_disabled" type="boolean">
  Whether the watermark is off. false: on, true: off
</ResponseField>

<ResponseField name="screenshot_disabled" type="boolean">
  Whether screenshots are disabled. false: allowed, true: disabled
</ResponseField>

<ResponseField name="self_unmute_mic_disabled" type="boolean">
  Whether members can unmute themselves when audio is disabled in the room. false: allowed, true: not allowed
</ResponseField>

<ResponseField name="self_unmute_camera_disabled" type="boolean">
  Whether members can turn their camera back on when the camera is off for everyone in the room. false: allowed, true: not allowed
</ResponseField>

<ResponseField name="mic_disabled" type="boolean">
  Audio disabled in the room. false: allowed, true: disabled
</ResponseField>

<ResponseField name="camera_disabled" type="boolean">
  Camera off for everyone in the room. false: no, true: yes
</ResponseField>

<ResponseField name="share_disabled" type="boolean">
  Disable sharing. false: no (default), true: yes
</ResponseField>

<ResponseField name="chat_disabled" type="boolean">
  Chat disabled in the room. false: allowed, true: disabled
</ResponseField>

<ResponseField name="waiting_room_disabled" type="boolean">
  Whether the waiting room is off. false: on, true: off
</ResponseField>

<ResponseField name="enter_before_host_disabled" type="boolean">
  Block entry before the host. false: allowed, true: blocked
</ResponseField>

<ResponseField name="force_join" type="boolean">
  Force entry
</ResponseField>

<ResponseField name="locked" type="boolean">
  Lock status. false: unlocked, true: locked
</ResponseField>

<ResponseField name="extend_info" type="object">
  Extension field
</ResponseField>

<ResponseField name="creator" type="string">
  Meeting creator ID
</ResponseField>

<ResponseField name="creator_name" type="string">
  Meeting creator name
</ResponseField>

<ResponseField name="host_uid" type="string">
  Host user ID
</ResponseField>

<ResponseField name="co_hosts" type="array<string>">
  Co-host user ID list
</ResponseField>

<ResponseField name="conferee" type="array<string>">
  Invitee ID list
</ResponseField>

<ResponseField name="conferee_details" type="array<object>">
  Invitee details list
  <Expandable title="Element fields">
    <ResponseField name="user_id" type="string">
      User ID
    </ResponseField>

    <ResponseField name="real_name" type="string">
      Real name
    </ResponseField>

    <ResponseField name="nickname" type="string">
      In-meeting display name
    </ResponseField>

    <ResponseField name="avatar" type="string">
      User avatar
    </ResponseField>

    <ResponseField name="role" type="integer">
      User role. 0: regular member, 1: host, 2: co-host
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="meeting_mode" type="integer">
  Meeting mode. 1: normal, 2: composite
</ResponseField>

<ResponseField name="auto_record" type="boolean">
  Whether to record automatically
</ResponseField>

<ResponseField name="layout_data" type="any">
  Layout data
</ResponseField>

<ResponseField name="record_status" type="integer">
  Recording status. 0: pending, 1: in progress, 2: stopping, 3: ended abnormally, 4: ended normally
</ResponseField>

<ResponseField name="created_at" type="integer">
  Creation time (timestamp)
</ResponseField>

<ResponseField name="updated_at" type="integer">
  Update time
</ResponseField>


Response example:

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "attend_type": 0,
      "auto_record": false,
      "begin_time": 0,
      "camera_disabled": false,
      "chat_disabled": false,
      "co_hosts": [
        ""
      ],
      "conferee": [
        ""
      ],
      "conferee_details": [
        {
          "avatar": "",
          "nickname": "",
          "real_name": "",
          "role": 0,
          "user_id": ""
        }
      ],
      "content": "",
      "created_at": 0,
      "creator": "",
      "creator_name": "",
      "end_time": 0,
      "enter_before_host_disabled": false,
      "entry_mute_policy": 0,
      "extend_info": {},
      "force_join": false,
      "host_uid": "",
      "id": "",
      "last_exit_time": 0,
      "layout_data": null,
      "locked": false,
      "meeting_mode": 0,
      "meeting_status": 0,
      "meeting_type": 0,
      "mic_disabled": false,
      "plan_dur": 0,
      "plan_time": 0,
      "record_status": 0,
      "room_no": "",
      "screenshot_disabled": false,
      "self_unmute_camera_disabled": false,
      "self_unmute_mic_disabled": false,
      "share_disabled": false,
      "title": "",
      "updated_at": 0,
      "waiting_room_disabled": false,
      "watermark_disabled": false
    }
  ]
}
```

---

## List in-meeting members

`POST /server/v1/meet/list-user`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

In-meeting members

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="page" type="integer">
  Page number, starting from 1
  Example: `1`
</ParamField>

<ParamField body="per-page" type="integer">
  Items per page
  Example: `10`
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "page": 1,
  "per-page": 10,
  "room_no": ""
}
```

**Response parameters**

<ResponseField name="user_id" type="string">
  User ID
</ResponseField>

<ResponseField name="nickname" type="string">
  In-meeting display name
</ResponseField>

<ResponseField name="role" type="integer">
  User role. 0: regular member, 1: host, 2: co-host
</ResponseField>

<ResponseField name="mic_state" type="integer">
  Audio status. 1: on, 2: off
</ResponseField>

<ResponseField name="camera_state" type="integer">
  Video status. 1: on, 2: off
</ResponseField>

<ResponseField name="share_state" type="integer">
  Sharing status. 0: none, 1: screen, 2: whiteboard
</ResponseField>

<ResponseField name="is_kickout" type="boolean">
  Whether the member has been removed
</ResponseField>

<ResponseField name="chat_disabled" type="boolean">
  Whether chat is disabled for this member. false: allowed, true: disabled
</ResponseField>

<ResponseField name="device_type" type="integer">
  Device type. 0: unknown, 1: Windows, 2: Android, 3: iOS, 4: Linux, 5: macOS, 6: WebRTC, 7: Mini Program; 80 and above: devices connected via device integration
</ResponseField>

<ResponseField name="extend_info" type="string">
  Extension field, supplied by the client when entering the meeting
</ResponseField>

<ResponseField name="join_at" type="integer">
  Entry time
</ResponseField>


Response example:

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "camera_state": 0,
      "chat_disabled": false,
      "device_type": 0,
      "extend_info": "",
      "is_kickout": false,
      "join_at": 0,
      "mic_state": 0,
      "nickname": "",
      "role": 0,
      "share_state": 0,
      "user_id": ""
    }
  ]
}
```

---

## List meeting-related users

`POST /server/v1/meet/meeting-users`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Meeting-related users

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="page" type="integer">
  Page number, starting from 1
  Example: `1`
</ParamField>

<ParamField body="per-page" type="integer">
  Items per page
  Example: `10`
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "page": 1,
  "per-page": 10,
  "room_no": ""
}
```

**Response parameters**

<ResponseField name="user_id" type="string">
  User ID
</ResponseField>

<ResponseField name="real_name" type="string">
  Real name
</ResponseField>

<ResponseField name="nickname" type="string">
  In-meeting display name
</ResponseField>

<ResponseField name="avatar" type="string">
  User avatar
</ResponseField>

<ResponseField name="role" type="integer">
  User role. 0: regular member, 1: host, 2: co-host
</ResponseField>

<ResponseField name="is_invite" type="boolean">
  Whether invited (allowlist)
</ResponseField>

<ResponseField name="enter_at" type="integer">
  First entry time
</ResponseField>

<ResponseField name="exit_at" type="integer">
  Last exit time
</ResponseField>


Response example:

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "avatar": "",
      "enter_at": 0,
      "exit_at": 0,
      "is_invite": false,
      "nickname": "",
      "real_name": "",
      "role": 0,
      "user_id": ""
    }
  ]
}
```

---

## List attendance records

`POST /server/v1/meet/list-record`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Attendance records

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="user_id" type="string">
  User ID
</ParamField>

<ParamField body="begin_at" type="integer">
  Start time
</ParamField>

<ParamField body="end_at" type="integer">
  End time
</ParamField>

<ParamField body="sort" type="string">
  Sort order. Sortable fields: updated_at / created_at, comma-separated; prefix - for descending order (sortable fields: updated_at, created_at)
</ParamField>

<ParamField body="page" type="integer">
  Page number, starting from 1
  Example: `1`
</ParamField>

<ParamField body="per-page" type="integer">
  Items per page
  Example: `10`
</ParamField>


Request example:

```json
{
  "begin_at": 0,
  "end_at": 0,
  "meeting_id": "",
  "page": 1,
  "per-page": 10,
  "room_no": "",
  "sort": "",
  "user_id": ""
}
```

**Response parameters**

<ResponseField name="app_id" type="string">
  App ID
</ResponseField>

<ResponseField name="meeting_id" type="string">
  Meeting ID
</ResponseField>

<ResponseField name="user_id" type="string">
  User ID
</ResponseField>

<ResponseField name="nickname" type="string">
  In-meeting display name
</ResponseField>

<ResponseField name="mobile" type="string">
  Mobile number
</ResponseField>

<ResponseField name="role" type="integer">
  User role. 0: regular member, 1: host, 2: co-host
</ResponseField>

<ResponseField name="enter_time" type="integer">
  Entry time
</ResponseField>

<ResponseField name="exit_time" type="integer">
  Exit time
</ResponseField>

<ResponseField name="device_type" type="integer">
  Device type. 0: unknown, 1: Windows, 2: Android, 3: iOS, 4: Linux, 5: macOS, 6: WebRTC, 7: Mini Program; 80 and above: devices connected via device integration
</ResponseField>

<ResponseField name="extend_info" type="string">
  Extension field, supplied by the client when entering the meeting
</ResponseField>


Response example:

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "app_id": "",
      "device_type": 0,
      "enter_time": 0,
      "exit_time": 0,
      "extend_info": "",
      "meeting_id": "",
      "mobile": "",
      "nickname": "",
      "role": 0,
      "user_id": ""
    }
  ]
}
```

---

## Send an in-meeting custom message

`POST /server/v1/meet/send-room-custom-message`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

**Request parameters**

<ParamField body="meeting_id" type="string" required>
  Meeting ID
</ParamField>

<ParamField body="content" type="string" required>
  Message content, up to 500 characters (max length 500)
</ParamField>

<ParamField body="target_id" type="string">
  User ID
</ParamField>


Request example:

```json
{
  "content": "",
  "meeting_id": "",
  "target_id": ""
}
```

**Response parameters**

<ResponseField name="data" type="string">
  Response data
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": ""
}
```

---

## Get meeting details

`POST /server/v1/meet/detail`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": ""
}
```

**Response parameters**

<ResponseField name="id" type="string">
  Device ID
</ResponseField>

<ResponseField name="room_no" type="string">
  Room number
</ResponseField>

<ResponseField name="title" type="string">
  Meeting title
</ResponseField>

<ResponseField name="content" type="string">
  Meeting description
</ResponseField>

<ResponseField name="meeting_status" type="integer">
  Meeting status. 1: not started, 2: in progress, 3: ended
</ResponseField>

<ResponseField name="attend_type" type="integer">
  1: unrestricted (default), 2: password required, 3: invitees only
</ResponseField>

<ResponseField name="meeting_type" type="integer">
  Meeting type. 1: instant meeting, 2: scheduled meeting
</ResponseField>

<ResponseField name="password" type="string">
  Password; required when attend_type is 2
</ResponseField>

<ResponseField name="plan_time" type="integer">
  Start time (timestamp); required for scheduled meetings
</ResponseField>

<ResponseField name="plan_dur" type="integer">
  Duration (minutes); required for scheduled meetings
</ResponseField>

<ResponseField name="begin_time" type="integer">
  Actual start time (timestamp); 0 if not started
</ResponseField>

<ResponseField name="end_time" type="integer">
  End time
</ResponseField>

<ResponseField name="last_exit_time" type="integer">
  Timestamp when the last member exited; 0 if the meeting has not ended
</ResponseField>

<ResponseField name="online_num" type="integer">
  Current number of online members
</ResponseField>

<ResponseField name="entry_mute_policy" type="integer">
  Mute on entry. 1: on (everyone is muted on entry), 2: off (follows the client's initial audio state), 3: mute beyond 6 (members entering after the first 6 are muted). Default: 3
</ResponseField>

<ResponseField name="watermark_disabled" type="boolean">
  Whether the watermark is off. false: on, true: off
</ResponseField>

<ResponseField name="screenshot_disabled" type="boolean">
  Whether screenshots are disabled. false: allowed, true: disabled
</ResponseField>

<ResponseField name="self_unmute_mic_disabled" type="boolean">
  Whether members are prevented from unmuting themselves when everyone is muted. false: not prevented, true: prevented
</ResponseField>

<ResponseField name="self_unmute_camera_disabled" type="boolean">
  Whether members are prevented from turning their camera back on when the camera is off for everyone. false: not prevented, true: prevented
</ResponseField>

<ResponseField name="mic_disabled" type="boolean">
  Mute all. false: not muted, true: muted
</ResponseField>

<ResponseField name="camera_disabled" type="boolean">
  Camera off for everyone. false: no, true: yes
</ResponseField>

<ResponseField name="share_disabled" type="boolean">
  Disable sharing. false: no (default), true: yes
</ResponseField>

<ResponseField name="chat_disabled" type="boolean">
  Whether chat is disabled for everyone. false: allowed, true: disabled
</ResponseField>

<ResponseField name="waiting_room_disabled" type="boolean">
  Whether the waiting room is off. false: on, true: off
</ResponseField>

<ResponseField name="enter_before_host_disabled" type="boolean">
  Whether others are blocked from entering before the host. false: allowed, true: blocked
</ResponseField>

<ResponseField name="force_join" type="boolean">
  Force entry
</ResponseField>

<ResponseField name="locked" type="boolean">
  Lock status; once locked, no one new can enter. false: unlocked, true: locked
</ResponseField>

<ResponseField name="extend_info" type="object">
  Extension field
</ResponseField>

<ResponseField name="creator" type="string">
  Meeting creator ID
</ResponseField>

<ResponseField name="creator_name" type="string">
  Meeting creator name
</ResponseField>

<ResponseField name="host_uid" type="string">
  Host user ID
</ResponseField>

<ResponseField name="co_hosts" type="array<string>">
  Co-host user ID list
</ResponseField>

<ResponseField name="conferee" type="array<string>">
  Invitee ID list
</ResponseField>

<ResponseField name="conferee_details" type="array<object>">
  Invitee details list
  <Expandable title="Element fields">
    <ResponseField name="user_id" type="string">
      User ID
    </ResponseField>

    <ResponseField name="real_name" type="string">
      Real name
    </ResponseField>

    <ResponseField name="nickname" type="string">
      In-meeting display name
    </ResponseField>

    <ResponseField name="avatar" type="string">
      User avatar
    </ResponseField>

    <ResponseField name="role" type="integer">
      User role. 0: regular member, 1: host, 2: co-host
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="meeting_mode" type="integer">
  Meeting mode. 1: normal, 2: composite, 3: voice, 4: training, 5: sub-meeting
</ResponseField>

<ResponseField name="auto_record" type="boolean">
  Whether to record automatically
</ResponseField>

<ResponseField name="layout_data" type="any">
  Layout data
</ResponseField>

<ResponseField name="record_status" type="integer">
  Recording status. 0: pending, 1: in progress, 2: stopping, 3: ended abnormally, 4: ended normally
</ResponseField>

<ResponseField name="created_at" type="integer">
  Creation time (timestamp)
</ResponseField>

<ResponseField name="updated_at" type="integer">
  Update time
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "attend_type": 0,
    "auto_record": false,
    "begin_time": 0,
    "camera_disabled": false,
    "chat_disabled": false,
    "co_hosts": [
      ""
    ],
    "conferee": [
      ""
    ],
    "conferee_details": [
      {
        "avatar": "",
        "nickname": "",
        "real_name": "",
        "role": 0,
        "user_id": ""
      }
    ],
    "content": "",
    "created_at": 0,
    "creator": "",
    "creator_name": "",
    "end_time": 0,
    "enter_before_host_disabled": false,
    "entry_mute_policy": 0,
    "extend_info": {},
    "force_join": false,
    "host_uid": "",
    "id": "",
    "last_exit_time": 0,
    "layout_data": null,
    "locked": false,
    "meeting_mode": 0,
    "meeting_status": 0,
    "meeting_type": 0,
    "mic_disabled": false,
    "online_num": 0,
    "password": "",
    "plan_dur": 0,
    "plan_time": 0,
    "record_status": 0,
    "room_no": "",
    "screenshot_disabled": false,
    "self_unmute_camera_disabled": false,
    "self_unmute_mic_disabled": false,
    "share_disabled": false,
    "title": "",
    "updated_at": 0,
    "waiting_room_disabled": false,
    "watermark_disabled": false
  }
}
```

---

## Cancel a meeting

`POST /server/v1/meet/cancel`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Cancel a meeting (only before it starts)

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": ""
}
```

**Response parameters**

<ResponseField name="data" type="string">
  Response data
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": ""
}
```

---

## Create a meeting

`POST /server/v1/meet/create`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

**Request parameters**

<ParamField body="creator" type="string">
  Creator, i.e. the meeting host. Use the user's unique ID in your system, the same value as user_id in conferee_details
</ParamField>

<ParamField body="creator_name" type="string">
  Creator's display name
</ParamField>

<ParamField body="room_no" type="string">
  Room number (max length 50)
</ParamField>

<ParamField body="title" type="string" required>
  Meeting title (max length 100)
</ParamField>

<ParamField body="content" type="string">
  Meeting description (max length 500)
</ParamField>

<ParamField body="password" type="string">
  Meeting password (max length 50)
</ParamField>

<ParamField body="meeting_type" type="integer" required>
  Meeting type. 1: instant meeting, 2: scheduled meeting
</ParamField>

<ParamField body="attend_type" type="integer">
  Entry type. 1: unrestricted, 2: password required, 3: invitees only, 4: password + allowlist
</ParamField>

<ParamField body="co_hosts" type="array<string>">
  Co-host ID list. Use the users' unique IDs in your system, the same values as user_id in conferee_details
</ParamField>

<ParamField body="conferee" type="array<string>">
  Invitee list (for compatibility with the legacy API)
</ParamField>

<ParamField body="conferee_details" type="array<object>">
  Invitee details list (new API)
  <Expandable title="Element fields">
    <ParamField body="user_id" type="string">
      User ID, i.e. the user's unique ID in your system
    </ParamField>

    <ParamField body="real_name" type="string">
      Real name
    </ParamField>

    <ParamField body="nickname" type="string">
      In-meeting display name; defaults to real_name if empty
    </ParamField>

    <ParamField body="avatar" type="string">
      User avatar
    </ParamField>

    <ParamField body="role" type="integer">
      User role. 0: regular member, 1: host, 2: co-host. Ignored with built-in roles: use creator to set the host and co_hosts to set co-hosts. The in-meeting role takes this value only when you use your own custom roles (external role mode); see the "Custom roles" section of "Key concepts". If omitted or 0, the role registered for this user in the user database is used; set it explicitly rather than relying on this fallback
    </ParamField>

  </Expandable>
</ParamField>

<ParamField body="plan_time" type="integer">
  Start time
</ParamField>

<ParamField body="plan_dur" type="integer">
  Duration (minutes)
</ParamField>

<ParamField body="entry_mute_policy" type="integer">
  Mute-on-entry option
</ParamField>

<ParamField body="watermark_disabled" type="boolean">
  Whether the watermark is off. false: on, true: off
</ParamField>

<ParamField body="screenshot_disabled" type="boolean">
  Whether screenshots are disabled. false: allowed, true: disabled
</ParamField>

<ParamField body="self_unmute_mic_disabled" type="boolean">
  Whether members can unmute themselves when audio is disabled in the room. false: allowed, true: not allowed
</ParamField>

<ParamField body="self_unmute_camera_disabled" type="boolean">
  Whether members can turn their camera back on when the camera is off for everyone in the room. false: allowed, true: not allowed
</ParamField>

<ParamField body="mic_disabled" type="boolean">
  Audio disabled in the room. false: allowed, true: disabled
</ParamField>

<ParamField body="camera_disabled" type="boolean">
  Camera off for everyone in the room. false: no, true: yes
</ParamField>

<ParamField body="share_disabled" type="boolean">
  Sharing disabled in the room. false: allowed, true: disabled
</ParamField>

<ParamField body="chat_disabled" type="boolean">
  Chat disabled in the room. false: allowed, true: disabled
</ParamField>

<ParamField body="waiting_room_disabled" type="boolean">
  Whether the waiting room is off. false: on, true: off
</ParamField>

<ParamField body="enter_before_host_disabled" type="boolean">
  Whether others are blocked from entering before the host. false: allowed, true: blocked
</ParamField>

<ParamField body="force_join" type="boolean">
  Whether to force entry
</ParamField>

<ParamField body="extend_info" type="object">
  Extension field
</ParamField>

<ParamField body="meeting_mode" type="integer">
  Meeting mode. 1: normal, 2: composite
</ParamField>

<ParamField body="auto_record" type="boolean">
  Whether to record automatically
</ParamField>

<ParamField body="layout_data" type="object">
  Layout data
  <Expandable title="Fields">
    <ParamField body="layout" type="string" required>
      Layout type
    </ParamField>

    <ParamField body="watermark" type="object">
      Watermark
      <Expandable title="Fields">
        <ParamField body="type" type="integer">
          Type. 0: default, 1: none, 2: single row, 3: multiple rows
        </ParamField>

        <ParamField body="text" type="string">
          Custom text; empty means automatic (meeting title)
        </ParamField>

        <ParamField body="size" type="integer">
          Font size; 0 means the default
        </ParamField>

        <ParamField body="color" type="string">
          Font color; empty means the default
        </ParamField>

        <ParamField body="ol_color" type="string">
          Outline color; empty means the default
        </ParamField>

        <ParamField body="ol_width" type="integer">
          Outline width; 0 means the default
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="nobody_text" type="string">
      Text shown when no one is in the meeting; empty means recording stops when no one is present
    </ParamField>

    <ParamField body="tag" type="object">
      Default name label
      <Expandable title="Fields">
        <ParamField body="type" type="string">
          Type, a letter or combination: L left, R right, T top, B bottom
        </ParamField>

        <ParamField body="text" type="string">
          Custom text; empty means automatic (in-meeting display name)
        </ParamField>

        <ParamField body="size" type="integer">
          Font size; 0 means default
        </ParamField>

        <ParamField body="color" type="string">
          Font color; empty means default
        </ParamField>

        <ParamField body="bg_color" type="string">
          Background color; empty means default
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="polling_dur" type="integer">
      Rotation interval (seconds); 0 disables rotation
    </ParamField>

    <ParamField body="div_list" type="array<object>">
      Logical block list
      <Expandable title="Element fields">
        <ParamField body="cells" type="array<object>">
          Grid cell list; empty means the remaining cells share the users here
        </ParamField>

        <ParamField body="uids" type="array<string>">
          User ID list. Empty: rotate through all remaining online users; multiple IDs: rotate among these users only
        </ParamField>

      </Expandable>
    </ParamField>

  </Expandable>
</ParamField>


Request example:

```json
{
  "attend_type": 0,
  "auto_record": false,
  "camera_disabled": false,
  "chat_disabled": false,
  "co_hosts": [
    ""
  ],
  "conferee": [
    ""
  ],
  "conferee_details": [
    {
      "avatar": "",
      "nickname": "",
      "real_name": "",
      "role": 0,
      "user_id": ""
    }
  ],
  "content": "",
  "creator": "",
  "creator_name": "",
  "enter_before_host_disabled": false,
  "entry_mute_policy": 0,
  "extend_info": {},
  "force_join": false,
  "layout_data": {
    "div_list": [
      {
        "cells": [
          {
            "bind_share": false,
            "idx": 0,
            "tag": {
              "bg_color": "",
              "color": "",
              "size": 0,
              "text": "",
              "type": ""
            }
          }
        ],
        "uids": [
          ""
        ]
      }
    ],
    "layout": "",
    "nobody_text": "",
    "polling_dur": 0,
    "tag": {
      "bg_color": "",
      "color": "",
      "size": 0,
      "text": "",
      "type": ""
    },
    "watermark": {
      "color": "",
      "ol_color": "",
      "ol_width": 0,
      "size": 0,
      "text": "",
      "type": 0
    }
  },
  "meeting_mode": 0,
  "meeting_type": 0,
  "mic_disabled": false,
  "password": "",
  "plan_dur": 0,
  "plan_time": 0,
  "room_no": "",
  "screenshot_disabled": false,
  "self_unmute_camera_disabled": false,
  "self_unmute_mic_disabled": false,
  "share_disabled": false,
  "title": "",
  "waiting_room_disabled": false,
  "watermark_disabled": false
}
```

**Response parameters**

<ResponseField name="meeting_id" type="string">
  Meeting ID, used by all subsequent meeting endpoints
</ResponseField>

<ResponseField name="room_no" type="string">
  Room number; users enter this number in the client to enter the meeting
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "meeting_id": "",
    "room_no": ""
  }
}
```

---

## Update a meeting before it starts

`POST /server/v1/meet/update`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Update a meeting

**Request parameters**

<ParamField body="meeting_id" type="string" required>
  Meeting ID
</ParamField>

<ParamField body="creator" type="string">
  Creator, i.e. the meeting host. Use the user's unique ID in your system, the same value as user_id in conferee_details
</ParamField>

<ParamField body="title" type="string">
  Meeting title (max length 100)
</ParamField>

<ParamField body="content" type="string">
  Meeting description (max length 500)
</ParamField>

<ParamField body="attend_type" type="integer">
  Entry type. 1: unrestricted, 2: password required, 3: invitees only, 4: password + allowlist
</ParamField>

<ParamField body="password" type="string">
  Meeting password (max length 50)
</ParamField>

<ParamField body="conferee" type="array<string>">
  Invitee list (for compatibility with the legacy API)
</ParamField>

<ParamField body="conferee_details" type="array<object>">
  Invitee details list (new API)
  <Expandable title="Element fields">
    <ParamField body="user_id" type="string">
      User ID, i.e. the user's unique ID in your system
    </ParamField>

    <ParamField body="real_name" type="string">
      Real name
    </ParamField>

    <ParamField body="nickname" type="string">
      In-meeting display name; defaults to real_name if empty
    </ParamField>

    <ParamField body="avatar" type="string">
      User avatar
    </ParamField>

    <ParamField body="role" type="integer">
      User role. 0: regular member, 1: host, 2: co-host. Ignored with built-in roles: use creator to set the host and co_hosts to set co-hosts. The in-meeting role takes this value only when you use your own custom roles (external role mode); see the "Custom roles" section of "Key concepts". If omitted or 0, the role registered for this user in the user database is used; set it explicitly rather than relying on this fallback
    </ParamField>

  </Expandable>
</ParamField>

<ParamField body="plan_time" type="integer">
  Start time
</ParamField>

<ParamField body="plan_dur" type="integer">
  Duration (minutes)
</ParamField>

<ParamField body="entry_mute_policy" type="integer">
  Mute-on-entry option
</ParamField>

<ParamField body="watermark_disabled" type="boolean">
  Whether the watermark is off. false: on, true: off
</ParamField>

<ParamField body="screenshot_disabled" type="boolean">
  Whether screenshots are disabled. false: allowed, true: disabled
</ParamField>

<ParamField body="chat_disabled" type="boolean">
  Chat disabled in the room. false: allowed, true: disabled
</ParamField>

<ParamField body="waiting_room_disabled" type="boolean">
  Whether the waiting room is off. false: on, true: off
</ParamField>

<ParamField body="enter_before_host_disabled" type="boolean">
  Whether others are blocked from entering before the host. false: allowed, true: blocked
</ParamField>

<ParamField body="force_join" type="boolean">
  Whether to force entry
</ParamField>

<ParamField body="co_hosts" type="array<string>">
  Co-host ID list. Use the users' unique IDs in your system, the same values as user_id in conferee_details
</ParamField>

<ParamField body="extend_info" type="object">
  Extension field
</ParamField>

<ParamField body="meeting_mode" type="integer">
  Meeting mode. 1: normal, 2: composite
</ParamField>

<ParamField body="auto_record" type="boolean">
  Whether to record automatically
</ParamField>

<ParamField body="layout_data" type="object">
  Layout data
  <Expandable title="Fields">
    <ParamField body="layout" type="string" required>
      Layout type
    </ParamField>

    <ParamField body="watermark" type="object">
      Watermark
      <Expandable title="Fields">
        <ParamField body="type" type="integer">
          Type. 0: default, 1: none, 2: single row, 3: multiple rows
        </ParamField>

        <ParamField body="text" type="string">
          Custom text; empty means automatic (meeting title)
        </ParamField>

        <ParamField body="size" type="integer">
          Font size; 0 means the default
        </ParamField>

        <ParamField body="color" type="string">
          Font color; empty means the default
        </ParamField>

        <ParamField body="ol_color" type="string">
          Outline color; empty means the default
        </ParamField>

        <ParamField body="ol_width" type="integer">
          Outline width; 0 means the default
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="nobody_text" type="string">
      Text shown when no one is in the meeting; empty means recording stops when no one is present
    </ParamField>

    <ParamField body="tag" type="object">
      Default name label
      <Expandable title="Fields">
        <ParamField body="type" type="string">
          Type, a letter or combination: L left, R right, T top, B bottom
        </ParamField>

        <ParamField body="text" type="string">
          Custom text; empty means automatic (in-meeting display name)
        </ParamField>

        <ParamField body="size" type="integer">
          Font size; 0 means default
        </ParamField>

        <ParamField body="color" type="string">
          Font color; empty means default
        </ParamField>

        <ParamField body="bg_color" type="string">
          Background color; empty means default
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="polling_dur" type="integer">
      Rotation interval (seconds); 0 disables rotation
    </ParamField>

    <ParamField body="div_list" type="array<object>">
      Logical block list
      <Expandable title="Element fields">
        <ParamField body="cells" type="array<object>">
          Grid cell list; empty means the remaining cells share the users here
        </ParamField>

        <ParamField body="uids" type="array<string>">
          User ID list. Empty: rotate through all remaining online users; multiple IDs: rotate among these users only
        </ParamField>

      </Expandable>
    </ParamField>

  </Expandable>
</ParamField>


Request example:

```json
{
  "attend_type": 0,
  "auto_record": false,
  "chat_disabled": false,
  "co_hosts": [
    ""
  ],
  "conferee": [
    ""
  ],
  "conferee_details": [
    {
      "avatar": "",
      "nickname": "",
      "real_name": "",
      "role": 0,
      "user_id": ""
    }
  ],
  "content": "",
  "creator": "",
  "enter_before_host_disabled": false,
  "entry_mute_policy": 0,
  "extend_info": {},
  "force_join": false,
  "layout_data": {
    "div_list": [
      {
        "cells": [
          {
            "bind_share": false,
            "idx": 0,
            "tag": {
              "bg_color": "",
              "color": "",
              "size": 0,
              "text": "",
              "type": ""
            }
          }
        ],
        "uids": [
          ""
        ]
      }
    ],
    "layout": "",
    "nobody_text": "",
    "polling_dur": 0,
    "tag": {
      "bg_color": "",
      "color": "",
      "size": 0,
      "text": "",
      "type": ""
    },
    "watermark": {
      "color": "",
      "ol_color": "",
      "ol_width": 0,
      "size": 0,
      "text": "",
      "type": 0
    }
  },
  "meeting_id": "",
  "meeting_mode": 0,
  "password": "",
  "plan_dur": 0,
  "plan_time": 0,
  "screenshot_disabled": false,
  "title": "",
  "waiting_room_disabled": false,
  "watermark_disabled": false
}
```

**Response parameters**

<ResponseField name="data" type="string">
  Response data
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": ""
}
```

---

## Update invitees

`POST /server/v1/meet/update-conferee`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Update invitees during the meeting

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="conferee" type="array<string>">
  Invitees (for compatibility with the legacy API)
</ParamField>

<ParamField body="conferee_details" type="array<object>">
  Invitee details list (new API)
  <Expandable title="Element fields">
    <ParamField body="user_id" type="string">
      User ID, i.e. the user's unique ID in your system
    </ParamField>

    <ParamField body="real_name" type="string">
      Real name
    </ParamField>

    <ParamField body="nickname" type="string">
      In-meeting display name; defaults to real_name if empty
    </ParamField>

    <ParamField body="avatar" type="string">
      User avatar
    </ParamField>

    <ParamField body="role" type="integer">
      User role. 0: regular member, 1: host, 2: co-host. Ignored with built-in roles: use creator to set the host and co_hosts to set co-hosts. The in-meeting role takes this value only when you use your own custom roles (external role mode); see the "Custom roles" section of "Key concepts". If omitted or 0, the role registered for this user in the user database is used; set it explicitly rather than relying on this fallback
    </ParamField>

  </Expandable>
</ParamField>

<ParamField body="is_additional" type="boolean">
  Whether to append
</ParamField>

<ParamField body="force_join" type="boolean">
  Whether to force entry (takes effect only when calling users into the meeting)
</ParamField>


Request example:

```json
{
  "conferee": [
    ""
  ],
  "conferee_details": [
    {
      "avatar": "",
      "nickname": "",
      "real_name": "",
      "role": 0,
      "user_id": ""
    }
  ],
  "force_join": false,
  "is_additional": false,
  "meeting_id": "",
  "room_no": ""
}
```

**Response parameters**

<ResponseField name="data" type="string">
  Response data
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": ""
}
```

---

## Remove invitees

`POST /server/v1/meet/delete-conferee`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Remove users from the allowlist

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="user_ids" type="array<string>" required>
  User ID list
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": "",
  "user_ids": [
    ""
  ]
}
```

**Response parameters**

<ResponseField name="data" type="string">
  Response data
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": ""
}
```

---

## List chat history

`POST /server/v1/meet/user-chat-record`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

User chat history

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="sender_id" type="string">
  Filter by sender user ID
</ParamField>

<ParamField body="msg_type" type="integer">
  Message type. 1: text, 2: file, 3: image, 4: voice
</ParamField>

<ParamField body="msg" type="string">
  Message content
</ParamField>

<ParamField body="begin_at" type="integer">
  Chat time range
</ParamField>

<ParamField body="end_at" type="integer">
  Chat time range
</ParamField>

<ParamField body="sort" type="string">
  Sort fields, comma-separated; prefix - for descending order, e.g. -created_at
</ParamField>

<ParamField body="page" type="integer">
  Page number, starting from 1
  Example: `1`
</ParamField>

<ParamField body="per-page" type="integer">
  Items per page
  Example: `10`
</ParamField>


Request example:

```json
{
  "begin_at": 0,
  "end_at": 0,
  "meeting_id": "",
  "msg": "",
  "msg_type": 0,
  "page": 1,
  "per-page": 10,
  "room_no": "",
  "sender_id": "",
  "sort": ""
}
```

**Response parameters**

<ResponseField name="id" type="string">
  Device ID
</ResponseField>

<ResponseField name="meeting_id" type="string">
  Meeting ID
</ResponseField>

<ResponseField name="sender_id" type="string">
  Sender's third-party user ID
</ResponseField>

<ResponseField name="sender_name" type="string">
  Sender name
</ResponseField>

<ResponseField name="real_name" type="string">
  Sender's real name
</ResponseField>

<ResponseField name="role" type="integer">
  Sender role. 0: regular member, 1: host, 2: co-host
</ResponseField>

<ResponseField name="msg_type" type="integer">
  Message type. 1: text, 2: file, 3: image, 4: voice
</ResponseField>

<ResponseField name="msg" type="string">
  Message content
</ResponseField>

<ResponseField name="created_at" type="integer">
  Sent time (timestamp)
</ResponseField>


Response example:

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "created_at": 0,
      "id": "",
      "meeting_id": "",
      "msg": "",
      "msg_type": 0,
      "real_name": "",
      "role": 0,
      "sender_id": "",
      "sender_name": ""
    }
  ]
}
```

---

## List files in chat history

`POST /server/v1/meet/chat-record-files`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Chat history files

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": ""
}
```

**Response parameters**

<ResponseField name="name" type="string">
  File name
</ResponseField>

<ResponseField name="size" type="string">
  File size (bytes)
</ResponseField>

<ResponseField name="key" type="string">
  File key
</ResponseField>

<ResponseField name="url" type="string">
  Playback/download URL, valid for 2 hours
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": [
    {
      "key": "",
      "name": "",
      "size": "",
      "url": ""
    }
  ]
}
```

---

## Get today's meeting overview

`POST /server/v1/meet/today`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Today's data

**Request parameters**

None

**Response parameters**

<ResponseField name="time" type="integer">
  Date
</ResponseField>

<ResponseField name="num" type="integer">
  Count
</ResponseField>

<ResponseField name="dur" type="integer">
  Duration (seconds)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "dur": 0,
    "num": 0,
    "time": 0
  }
}
```

---

## Get meeting count statistics

`POST /server/v1/meet/stats`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Meeting statistics

**Request parameters**

<ParamField body="begin_at" type="integer">
  Start time
</ParamField>

<ParamField body="end_at" type="integer">
  End time
</ParamField>


Request example:

```json
{
  "begin_at": 0,
  "end_at": 0
}
```

**Response parameters**

<ResponseField name="day" type="string">
  Date
</ResponseField>

<ResponseField name="num" type="integer">
  Count
</ResponseField>

<ResponseField name="dur" type="integer">
  Duration (seconds)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": [
    {
      "day": "",
      "dur": 0,
      "num": 0
    }
  ]
}
```

---

