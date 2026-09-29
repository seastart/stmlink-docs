---
title: "Whiteboard"
description: "Authorize, check, and destroy whiteboards"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the rtc-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Get a whiteboard authorization code

`POST /server/v1/white-board/grant-code`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Get a whiteboard authorization code. A whiteboard is a collaborative board independent of channels; users who pass the same board
open the same whiteboard.

The typical flow is similar to the channel token: your backend checks permissions → calls this endpoint to get auth_code and addr →
sends them to the client → the client combines them into &#123;addr&#125;?code=&#123;auth_code&#125; and opens it (the whiteboard is an H5 page,
embedded with an iframe or WebView). The authorization code is valid for 1 hour and expires once connected; get a new one
every time the whiteboard is opened, and don't cache it.

A whiteboard is created automatically the first time it is authorized; you don't need to create it in advance.

Users in a channel have an easier route: the join response already includes a ready-made whiteboard URL (field
white_board, whose authorization code is that user's sid), which you can embed directly without calling this endpoint. This endpoint is for
"people outside the channel also need the whiteboard" and "using the whiteboard independently of channels". For the full integration guide,
see the "Whiteboard" docs.

**Request parameters**

<ParamField body="board" type="string" required>
  Board ID, with the same character set restrictions as channel names. A common practice is to use the channel name directly, so each channel maps to one whiteboard (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="uid" type="string" required>
  Third-party user ID, used to show collaborator cursors and operators (letters, digits, underscores (_), and hyphens (-) only) (max length 100)
  Example: `1001`
</ParamField>

<ParamField body="name" type="string">
  Third-party user name
  Example: `Alice`
</ParamField>

<ParamField body="net" type="string">
  Network line. The value is a Chinese line name; leave empty to let the server choose
  Example: `内网`
</ParamField>

<ParamField body="sg" type="string">
  Server group
</ParamField>


Request example:

```json
{
  "board": "fire",
  "name": "Alice",
  "net": "内网",
  "sg": "",
  "uid": "1001"
}
```

**Response parameters**

<ResponseField name="auth_code" type="string">
  Whiteboard authorization code, issued to the client to open the whiteboard
  Example: `wb-co63jg6g54hu3b0xhtie`
</ResponseField>

<ResponseField name="addr" type="string">
  Whiteboard page URL; combine it with the authorization code as &#123;addr&#125;?code=&#123;auth_code&#125;
  Example: `https://api.example.com/white-board/`
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "addr": "https://api.example.com/white-board/",
    "auth_code": "wb-co63jg6g54hu3b0xhtie"
  }
}
```

---

## Check whether a whiteboard exists

`POST /server/v1/white-board/exist`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Check whether a whiteboard exists, that is, whether it has been created and not destroyed.

Use it to decide "is there still content on this board"—for example, whether to show an "Open whiteboard" entry,
or to confirm that a destroy has taken effect.

**Request parameters**

<ParamField body="board" type="string" required>
  Board ID (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>


Request example:

```json
{
  "board": "fire"
}
```

**Response parameters**

<ResponseField name="is_exist" type="boolean">
  Whether the whiteboard exists (created and not destroyed)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "is_exist": false
  }
}
```

---

## Destroy a whiteboard

`POST /server/v1/white-board/destroy`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Destroy a whiteboard. Content on the board is cleared and can't be recovered; users currently on the whiteboard are disconnected.

Whiteboards also have two automatic destroy paths; this endpoint is for cleaning up proactively before those happen (such as "Close whiteboard" during a call):

- When a channel is destroyed, the whiteboard with the same name is destroyed with it. A channel is destroyed automatically after 2 hours with no one in it, so a whiteboard used the recommended way
(board set to the channel name) also disappears 2 hours after everyone leaves. To keep whiteboard content
long term, don't use the channel name as board.
- A whiteboard with no writes for more than 25 hours is cleaned up by a scheduled job.

**Request parameters**

<ParamField body="board" type="string" required>
  Board ID (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="op_uid" type="string">
  Operator ID, used for auditing
  Example: `1001`
</ParamField>

<ParamField body="op_name" type="string">
  Operator name
  Example: `Alice`
</ParamField>


Request example:

```json
{
  "board": "fire",
  "op_name": "Alice",
  "op_uid": "1001"
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

