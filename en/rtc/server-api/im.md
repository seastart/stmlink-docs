---
title: "IM messages"
description: "Out-of-channel IM messages and IM device presence management"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the rtc-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Get an IM token

`POST /server/v1/im/grant`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Get an IM connection credential. The IM channel (out-of-channel messaging) is a message path separate from SRTC channels—users can send and receive even when they aren't in any channel,
suited to scenarios such as meeting invitation notifications, incoming calls, and offline reminders.

Typical flow: after a user logs in to your business, your backend calls this endpoint to get a token → sends it to the client →
the client uses it to connect to IM. After that you can push messages to them with "Send an IM message" and receive their online/offline callbacks
(im_connect / im_disconnect).

The same uid can connect from multiple devices at once, and each connection has its own sid—so "sending a message to a person"
and "sending a message to a device" are two different things; see "Send an IM message".

**Request parameters**

<ParamField body="uid" type="string" required>
  Third-party user ID (letters, digits, underscores (_), and hyphens (-) only) (max length 100)
  Example: `1001`
</ParamField>

<ParamField body="net" type="string">
  Network line. The value is a Chinese line name determined by the deployment's network configuration; leave empty to let the server choose
  Example: `内网`
</ParamField>

<ParamField body="sg" type="string">
  Server group
</ParamField>


Request example:

```json
{
  "net": "内网",
  "sg": "",
  "uid": "1001"
}
```

**Response parameters**

<ResponseField name="sid" type="string">
  ID of this IM session; each connection of the same uid on multiple devices has its own sid
</ResponseField>

<ResponseField name="token" type="string">
  IM connection credential, issued to the client to establish the IM long-lived connection
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "sid": "",
    "token": ""
  }
}
```

---

## Send an IM message

`POST /server/v1/im/send-msg`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Push messages to specified users or devices through the IM channel; recipients don't need to be in any channel.

Choose one of the two recipient types: ruids sends by user, and every online device of that user receives it; rsids sends by session,
only to specific devices. When rsids is set, ruids is ignored; the two are not combined.

Messages are not persisted: important only guarantees resending during reconnection; it is not an offline message queue.
For messages to recipients who stay offline for a long time, you need a fallback on your own side.

**Request parameters**

<ParamField body="action" type="string" required>
  Message command, defined by you; the client dispatches on it
  Example: `meeting_invite`
</ParamField>

<ParamField body="content" type="any">
  Message body, any JSON; you define the structure
  Example: `&#123;"meeting_no": "818595664", "title": "Weekly project sync"&#125;`
</ParamField>

<ParamField body="uid" type="string">
  Sender user ID, used by the client to show "who sent it"; can be empty for system messages sent by the server (letters, digits, underscores (_), and hyphens (-) only)
  Example: `1001`
</ParamField>

<ParamField body="sid" type="string">
  Sender session ID
</ParamField>

<ParamField body="name" type="string">
  Sender name
  Example: `Alice`
</ParamField>

<ParamField body="ruids" type="array<string>">
  List of recipient user IDs (ignored when Rsids is set)
  Example: `["1002","1003"]`
</ParamField>

<ParamField body="rsids" type="array<string>">
  List of recipient session IDs, for delivery to specific devices
</ParamField>

<ParamField body="important" type="boolean">
  Whether the message is important. Important messages are resent after reconnecting to make sure they arrive. Enable it for messages that must not be lost, such as invitations and calls; ordinary state sync doesn't need it
</ParamField>


Request example:

```json
{
  "action": "meeting_invite",
  "content": "{\"meeting_no\": \"818595664\", \"title\": \"Weekly project sync\"}",
  "important": false,
  "name": "Alice",
  "rsids": [
    ""
  ],
  "ruids": [
    "1002",
    "1003"
  ],
  "sid": "",
  "uid": "1001"
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

## Force an IM device offline

`POST /server/v1/im/kick-device`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Forcibly disconnect the IM connection of specified users or devices, typically to force an old device offline when the account logs in elsewhere.
The disconnected device receives a notification and the im_disconnect callback is triggered.

This only disconnects the IM connection; it doesn't affect any channel call the user is already in, and it doesn't prevent them from reconnecting—
to block reconnection, stop issuing IM tokens on your side.

**Request parameters**

<ParamField body="uid" type="string">
  Operator user ID, used for auditing (letters, digits, underscores (_), and hyphens (-) only)
  Example: `1001`
</ParamField>

<ParamField body="ruids" type="array<string>">
  List of user IDs to force offline; this disconnects all of their devices (ignored when Rsids is set)
  Example: `["1002"]`
</ParamField>

<ParamField body="rsids" type="array<string>">
  List of session IDs to force offline; this disconnects only those devices
</ParamField>


Request example:

```json
{
  "rsids": [
    ""
  ],
  "ruids": [
    "1002"
  ],
  "uid": "1001"
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

## Get users' online devices

`POST /server/v1/im/user-device-list`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Query users' current online IM devices in bulk, to decide "can this person receive a push right now"
or to show multi-device online status.

The data in the response maps "user ID → device list"; users who are offline don't appear in the result.
Each device has its own sid and device_type, which you can use to send messages to or disconnect a specific device.

**Request parameters**

<ParamField body="uids" type="array<string>" required>
  List of user IDs
  Example: `["1001","1002"]`
</ParamField>


Request example:

```json
{
  "uids": [
    "1001",
    "1002"
  ]
}
```

**Response parameters**

<ResponseField name="<key>" type="array<object>">
  Keys are dynamic; see the description above
  <Expandable title="Element fields">
    <ResponseField name="uid" type="string">
      User ID
    </ResponseField>

    <ResponseField name="sid" type="string">
      Session ID
    </ResponseField>

    <ResponseField name="device_type" type="integer">
      Device type
    </ResponseField>

    <ResponseField name="device_id" type="string">
      Unique device ID
    </ResponseField>

  </Expandable>
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {}
}
```

---

