---
title: "User sync"
description: "Sync users from your business system into the meeting user directory we deploy, get login-free tokens, check online status, and delete users. Used by server-side low-code integration and contact-list scenarios. The endpoint prefix is /stm/srvapi/v1"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the meeting-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Batch sync users

`POST /stm/srvapi/v1/member/sync`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Pushes users from your system in batches, so that the meeting client can show them in its contact list and let people pick participants from it.
If you only use "Get a login-free token" to join meetings, you do not need to sync first: that endpoint creates the user on the spot when a display name is included.

Up to 1,000 users per request. Users are identified by `user_id`: a user who does not exist yet is created, and an existing one is updated, so both full and incremental pushes work.
For existing users, `nickname`, `real_name`, and `department` always take the values from the current request (omitting `department` clears it),
while `avatar`, `mobile`, `password_hash` / `salt`, and `camera_disabled` / `share_disabled` keep their current values when omitted.

Only one sync can run per app at a time. Concurrent calls are rejected with a "too frequent, please wait" error, so push the next batch after the previous one returns.
A failure on one user does not affect the others; results are split by `user_id` into the `success` and `fail` maps.

**Request parameters**

The request body is a **JSON array**. The fields of each element are listed below.

<ParamField body="user_id" type="string" required>
  User ID, i.e. the user's unique ID in your system (max length 100)
</ParamField>

<ParamField body="nickname" type="string" required>
  In-meeting display name (max length 100)
  Example: `Alice`
</ParamField>

<ParamField body="real_name" type="string">
  Real name. Defaults to `nickname` when empty (max length 100)
</ParamField>

<ParamField body="avatar" type="string">
  Leave empty to keep the current avatar; an existing avatar is not cleared (max length 300)
</ParamField>

<ParamField body="mobile" type="string">
  Mobile number. For display only and not used to identify the user, which relies solely on `user_id`. Leave empty to keep the current value (max length 100)
</ParamField>

<ParamField body="password_hash" type="string">
  Pass only if the user also needs to sign in to the meeting page with an account and password: the lowercase hex of sha256(password + salt), sent together with `salt`. Omit to leave unchanged (max length 100)
</ParamField>

<ParamField body="salt" type="string">
  Salt used to compute `password_hash`. Can be empty (max length 100)
</ParamField>

<ParamField body="department" type="string">
  Organization name, a flat string rather than a hierarchy (max length 100)
  Example: `Procurement Dept. 1`
</ParamField>

<ParamField body="camera_disabled" type="boolean">
  Disable camera
</ParamField>

<ParamField body="share_disabled" type="boolean">
  Disable sharing (screen and whiteboard)
</ParamField>


Request example:

```json
[
  {
    "avatar": "",
    "camera_disabled": false,
    "department": "Procurement Dept. 1",
    "mobile": "",
    "nickname": "Alice",
    "password_hash": "",
    "real_name": "",
    "salt": "",
    "share_disabled": false,
    "user_id": ""
  }
]
```

**Response parameters**

<ResponseField name="success" type="object">
  Users that succeeded. Both the key and the value are the `user_id` you passed
</ResponseField>

<ResponseField name="fail" type="object">
  Users that failed. The key is the `user_id` and the value is the failure reason
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "fail": {},
    "success": {}
  }
}
```

---

## Get a login-free token

`POST /stm/srvapi/v1/member/grant`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Call this in real time when the user clicks "Join meeting" to get a login-free token. Add it to the meeting page URL and the user joins without signing in.
`data` is the token string itself.

When you include `nickname` and other profile fields, a user who does not exist is created on the spot and an existing one is updated, so you do not need to call "Batch sync users" first.
Just pass the latest display name and avatar each time. Passing only `user_id` for a user who has never been synced returns an error, because without a display name
the user would have no name in the meeting.

**Request parameters**

<ParamField body="user_id" type="string" required>
  User ID, same as the `user_id` in member/sync (max length 100)
</ParamField>

<ParamField body="nickname" type="string">
  In-meeting display name (max length 100)
</ParamField>

<ParamField body="real_name" type="string">
  Real name. Defaults to `nickname` when empty (max length 100)
</ParamField>

<ParamField body="avatar" type="string">
  Avatar URL. Leave empty to keep the current avatar (max length 300)
</ParamField>

<ParamField body="mobile" type="string">
  Mobile number. For display only and not used to identify the user, which relies solely on `user_id`. Leave empty to keep it unchanged (max length 100)
</ParamField>

<ParamField body="camera_disabled" type="boolean">
  Disable camera
</ParamField>

<ParamField body="share_disabled" type="boolean">
  Disable sharing (screen and whiteboard)
</ParamField>


Request example:

```json
{
  "avatar": "",
  "camera_disabled": false,
  "mobile": "",
  "nickname": "",
  "real_name": "",
  "share_disabled": false,
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

## Query users and online status

`POST /stm/srvapi/v1/member/info`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Queries synced user profiles in batches by `user_id`. The response includes `is_online`, which you can use to show online status in your UI.
Nonexistent `user_id` values are omitted from the response.

**Request parameters**

<ParamField body="user_ids" type="array<string>">
  List of user IDs, i.e. the `user_id` values passed when syncing
</ParamField>


Request example:

```json
{
  "user_ids": [
    ""
  ]
}
```

**Response parameters**

<ResponseField name="user_id" type="string">
  User ID
</ResponseField>

<ResponseField name="mobile" type="string">
  Mobile number
</ResponseField>

<ResponseField name="nickname" type="string">
  Display name
</ResponseField>

<ResponseField name="real_name" type="string">
  Real name
</ResponseField>

<ResponseField name="avatar" type="string">
  Avatar
</ResponseField>

<ResponseField name="is_online" type="boolean">
  Whether the user is online
</ResponseField>

<ResponseField name="created_at" type="integer">
  Creation time, Unix timestamp in seconds
</ResponseField>

<ResponseField name="camera_disabled" type="boolean">
  Disable camera
</ResponseField>

<ResponseField name="share_disabled" type="boolean">
  Sharing disabled
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": [
    {
      "avatar": "",
      "camera_disabled": false,
      "created_at": 0,
      "is_online": false,
      "mobile": "",
      "nickname": "",
      "real_name": "",
      "share_disabled": false,
      "user_id": ""
    }
  ]
}
```

---

## Delete users

`POST /stm/srvapi/v1/member/remove`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Deletes users in batches by `user_id` (for example, when employees leave). A deleted user can no longer get a token to join meetings.
Nonexistent `user_id` values are ignored.

**Request parameters**

<ParamField body="user_ids" type="array<string>">
  List of user IDs, i.e. the `user_id` values passed when syncing
</ParamField>


Request example:

```json
{
  "user_ids": [
    ""
  ]
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

