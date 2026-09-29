---
title: "Meeting authorization"
description: "Issue meeting tokens for users in your system, and force authorized users to log out"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the meeting-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Get meeting authorization

`POST /server/v1/user-auth/grant`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Get a grant

**Request parameters**

<ParamField body="user_id" type="string" required>
  Third-party user ID (max length 100)
</ParamField>

<ParamField body="nickname" type="string">
  Display name (max length 100)
</ParamField>

<ParamField body="net" type="string">
  Network line
</ParamField>

<ParamField body="sg" type="string">
  Server group
</ParamField>


Request example:

```json
{
  "net": "",
  "nickname": "",
  "sg": "",
  "user_id": ""
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

## Log out a user

`POST /server/v1/user-auth/kickout`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Invalidate the user's login session (the session obtained with meet_token) immediately; the next API call requires a new grant.

Note that this endpoint **does not remove the user from an ongoing meeting**. The logged-out user stays in the meeting
until the heartbeat times out (the `reason` of the `user_exit` callback is 4).
To remove someone from the meeting immediately, use "Remove a member" in [In-meeting controls](/en/meeting/server-api/meet-admin).

+ Without device_type: the user is logged out on all devices
+ With device_type: only that device is logged out; other devices are not affected
+ An error is returned if the user currently has no valid login session

**Request parameters**

<ParamField body="user_id" type="string" required>
  Third-party user ID
</ParamField>

<ParamField body="device_type" type="integer">
  Log out only this device type. 0: unknown, 1: Windows, 2: Android, 3: iOS, 4: Linux, 5: macOS, 6: WebRTC, 7: WeChat Mini Program. If omitted, the user is logged out on all devices
  Example: `3`
</ParamField>


Request example:

```json
{
  "device_type": 3,
  "user_id": ""
}
```

**Response parameters**

`data` is null

Response example:

```json
{
  "code": 0,
  "data": null
}
```

---

