---
title: "In-meeting controls"
description: "Actions the host can take during a meeting: audio and video controls for everyone, member roles and removal, raise-hand handling, and calling users into the meeting"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the meeting-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## End a meeting

`POST /server/v1/meet-admin/destroy`

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

## Update room video status

`POST /server/v1/meet-admin/update-room-camera-state`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="self_unmute_camera_disabled" type="boolean">
  Whether members are prevented from turning their camera back on when the camera is off for everyone. false: not prevented (default), true: prevented. Reset to false as well when camera_disabled is false
</ParamField>

<ParamField body="camera_disabled" type="boolean">
  Turn the camera off for everyone. false: no (default), true: yes
</ParamField>


Request example:

```json
{
  "camera_disabled": false,
  "meeting_id": "",
  "room_no": "",
  "self_unmute_camera_disabled": false
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

## Update room audio status

`POST /server/v1/meet-admin/update-room-mic-state`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="self_unmute_mic_disabled" type="boolean">
  Whether members are prevented from unmuting themselves when everyone is muted. false: not prevented (default), true: prevented. Reset to false as well when mic_disabled is false
</ParamField>

<ParamField body="mic_disabled" type="boolean">
  Mute all. false: no (default), true: yes
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "mic_disabled": false,
  "room_no": "",
  "self_unmute_mic_disabled": false
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

## Update room sharing permission

`POST /server/v1/meet-admin/update-room-share-disabled`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Update room sharing permission

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="share_disabled" type="boolean">
  Disable sharing. false: no (default), true: yes
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": "",
  "share_disabled": false
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

## Update room chat permission

`POST /server/v1/meet-admin/update-room-chat-disabled`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Update room chat permission

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="chat_disabled" type="boolean" required>
  Disable chat for everyone. false: no, true: yes
</ParamField>


Request example:

```json
{
  "chat_disabled": false,
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

## Update room screenshot permission

`POST /server/v1/meet-admin/update-room-screenshot-disabled`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Update room screenshot permission

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="screenshot_disabled" type="boolean" required>
  Disable screenshots. false: no, true: yes
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": "",
  "screenshot_disabled": false
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

## Update room watermark setting

`POST /server/v1/meet-admin/update-watermark-disabled`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Update room watermark setting

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="watermark_disabled" type="boolean" required>
  Turn off the watermark. false: watermark on, true: watermark off
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": "",
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

## Update room lock status

`POST /server/v1/meet-admin/update-locked`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Update room lock status

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="locked" type="boolean" required>
  Lock the meeting; once locked, no one new can enter. false: unlocked, true: locked
</ParamField>


Request example:

```json
{
  "locked": false,
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

## Stop the current share

`POST /server/v1/meet-admin/stop-room-share`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Stop the current share

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

## Update a member's in-meeting role

`POST /server/v1/meet-admin/update-user-role`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Update a member's role

By default, in-meeting roles use three built-in tiers: 0 regular member, 1 host, 2 co-host. Each SDK uses the role to decide whether meeting-control
entry points are available. You can also turn off the built-in roles entirely and use your own role system (external role mode); the values and meaning of role
are then defined by you, and this endpoint is how you change it during the meeting (in that mode you can also change your own role). See the "Custom roles" section
of "Key concepts". The notes below apply to the default case with built-in roles.

This endpoint switches a member between "regular member ⇄ co-host": pass 2 to promote a member to co-host, or 0 to revoke it.
The change is also written to the meeting's co_hosts list, so it still applies when the member enters the meeting again later.

A meeting has exactly one host, determined by the meeting's host_uid (set to creator when the meeting is created on the server),
so you **cannot** use this endpoint to change a role to 1.
The target user must be in the meeting, and the operator cannot change their own role. Role changes are broadcast to all members as an in-meeting custom message,
and each SDK refreshes its member list accordingly.

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="target_id" type="string" required>
  User ID
</ParamField>

<ParamField body="role" type="integer" required>
  Target role. 0: regular member, 2: co-host. The host (1) is determined by the meeting's host_uid and cannot be set here
  Example: `2`
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "role": 2,
  "room_no": "",
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

## Update a member's in-meeting display name

`POST /server/v1/meet-admin/update-user-name`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Update a member's in-meeting display name

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="target_id" type="string" required>
  User ID
</ParamField>

<ParamField body="nickname" type="string" required>
  New in-meeting display name
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "nickname": "",
  "room_no": "",
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

## Update a member's chat permission

`POST /server/v1/meet-admin/update-user-chat-disabled`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Update a member's chat permission

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="target_id" type="string" required>
  User ID
</ParamField>

<ParamField body="chat_disabled" type="boolean" required>
  Disable chat for this member. false: no, true: yes
</ParamField>


Request example:

```json
{
  "chat_disabled": false,
  "meeting_id": "",
  "room_no": "",
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

## Turn off a member's camera

`POST /server/v1/meet-admin/close-user-camera`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Turn off a member's camera

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="target_id" type="string" required>
  User ID
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": "",
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

## Turn off a member's microphone

`POST /server/v1/meet-admin/close-user-mic`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Turn off a member's microphone

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="target_id" type="string" required>
  User ID
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": "",
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

## Ask a member to share

`POST /server/v1/meet-admin/request-user-share`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="target_id" type="string" required>
  User ID
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": "",
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

## Ask a member to turn on video

`POST /server/v1/meet-admin/request-user-open-camera`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="target_id" type="string" required>
  User ID
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": "",
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

## Ask a member to unmute

`POST /server/v1/meet-admin/request-user-open-mic`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="target_id" type="string" required>
  User ID
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": "",
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

## Remove a member

`POST /server/v1/meet-admin/kickout-user`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="target_id" type="string" required>
  User ID
</ParamField>

<ParamField body="remove_conferee" type="boolean">
  Whether to remove the user from the allowlist
</ParamField>

<ParamField body="join_disabled" type="boolean">
  Whether to block the user from entering again
</ParamField>


Request example:

```json
{
  "join_disabled": false,
  "meeting_id": "",
  "remove_conferee": false,
  "room_no": "",
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

## Handle a raise-hand request

`POST /server/v1/meet-admin/confirm-handup`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Handle a raise-hand request

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="target_id" type="string" required>
  User ID
</ParamField>

<ParamField body="code" type="integer" required>
  Request type. 1: unmute, 2: turn on video, 3: chat, 4: share, 5: draw (annotate)
</ParamField>

<ParamField body="approve" type="boolean" required>
  true: approve, false: reject
</ParamField>


Request example:

```json
{
  "approve": false,
  "code": 0,
  "meeting_id": "",
  "room_no": "",
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

## Call users into the meeting

`POST /server/v1/meet-admin/call-users`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

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

