---
title: "Device integration"
description: "Integration and in-channel control of SIP, H.323, GB28181 surveillance, and other devices"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the rtc-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Add a device

`POST /server/v1/agent/create`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Register external devices such as SIP / H.323 phones, GB28181 surveillance devices, and RTSP streams under your app; then you can use
"Invite devices to the channel" to bring them into a channel. The response is the device ID—save it;
you need it to update, delete, and query details later.

Request body fields vary with the URL query parameter type (each integration type has different required fields); what to pass for each of the six integration types
is listed below by value. For how to choose an integration type, see the "Device integration guide".

**URL query parameters**

<ParamField query="type" type="string" required>
  Integration type. For values, see the "Device integration guide"
</ParamField>

**Request parameters**

The request body fields depend on the URL query parameter `type`. The fields for each value are listed below.

### `type=ipsip` — SIP phone, direct IP

<ParamField body="uri" type="string" required>
  Device address, ip:port (max length 100)
  Example: `192.168.1.50:5060`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `3rd-floor meeting room phone`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `East wing, 3F`
</ParamField>


Request example:

```json
{
  "display_name": "3rd-floor meeting room phone",
  "gw": "devgw-1",
  "remark": "East wing, 3F",
  "uri": "192.168.1.50:5060"
}
```

### `type=regsip` — SIP phone, registration mode

<ParamField body="username" type="string" required>
  Username; the account the device uses to register with the gateway; must not contain : (max length 100)
  Example: `6001`
</ParamField>

<ParamField body="auth_pwd" type="string" required>
  Password; must match the device configuration (max length 50)
  Example: `Abc123456`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `3rd-floor meeting room phone`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `East wing, 3F`
</ParamField>


Request example:

```json
{
  "auth_pwd": "Abc123456",
  "display_name": "3rd-floor meeting room phone",
  "gw": "devgw-1",
  "remark": "East wing, 3F",
  "username": "6001"
}
```

### `type=iph323` — H.323 endpoint, direct IP

<ParamField body="uri" type="string" required>
  Device address, ip:port (max length 100)
  Example: `192.168.1.60:1720`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `3rd-floor meeting room endpoint`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `East wing, 3F`
</ParamField>


Request example:

```json
{
  "display_name": "3rd-floor meeting room endpoint",
  "gw": "devgw-1",
  "remark": "East wing, 3F",
  "uri": "192.168.1.60:1720"
}
```

### `type=regh323` — H.323 endpoint, registration mode

<ParamField body="username" type="string" required>
  Username; must be a short numeric extension (max length 100)
  Example: `6002`
</ParamField>

<ParamField body="auth_pwd" type="string" required>
  Password; must match the device configuration (max length 50)
  Example: `Abc123456`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `3rd-floor meeting room endpoint`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `East wing, 3F`
</ParamField>


Request example:

```json
{
  "auth_pwd": "Abc123456",
  "display_name": "3rd-floor meeting room endpoint",
  "gw": "devgw-1",
  "remark": "East wing, 3F",
  "username": "6002"
}
```

### `type=gb28181` — GB28181 surveillance device

<ParamField body="sip_no" type="string" required>
  Device SIP number, 18–20 digits; can be generated with "Generate a GB28181 device SIP number" (max length 20)
  Example: `33010806661328458475`
</ParamField>

<ParamField body="auth_pwd" type="string" required>
  Password; must match the GB28181 settings on the device (max length 50)
  Example: `Abc123456`
</ParamField>

<ParamField body="subjects" type="object">
  Channel number → name: the video feeds under one device. After registration, you can also add or change them with "Set a GB28181 device channel"
  Example: `{"33010806661329301268":"Guest seats"}`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `Dome camera 1`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `Lobby entrance`
</ParamField>


Request example:

```json
{
  "auth_pwd": "Abc123456",
  "display_name": "Dome camera 1",
  "gw": "devgw-1",
  "remark": "Lobby entrance",
  "sip_no": "33010806661328458475",
  "subjects": {
    "33010806661329301268": "Guest seats"
  }
}
```

### `type=rtsp` — RTSP stream pull

<ParamField body="uri" type="string" required>
  RTSP stream URL; must start with rtsp (max length 100)
  Example: `rtsp://192.168.1.70:554/stream1`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `Lobby camera`
</ParamField>

<ParamField body="transport_type" type="string">
  Transport: UDP (default) | TCP
  Example: `TCP`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `Lobby entrance`
</ParamField>


Request example:

```json
{
  "display_name": "Lobby camera",
  "gw": "devgw-1",
  "remark": "Lobby entrance",
  "transport_type": "TCP",
  "uri": "rtsp://192.168.1.70:554/stream1"
}
```

**Response parameters**

<ResponseField name="data" type="string">
  ID of the new device, used later to update, delete, and query details
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": ""
}
```

---

## Update a device

`POST /server/v1/agent/update`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Update the connection info or display name of a registered device. The request body fields are the same as for "Add a device" (they vary with type),
plus the device id; the full fields for each value are listed below.

+ type must match how the device was originally integrated; you can't use this to turn a SIP device into an RTSP one. To change the integration type, delete the device and register it again
+ Changes take effect the next time the device connects; devices currently in a channel are not affected

**URL query parameters**

<ParamField query="type" type="string" required>
  Integration type; must match the one used when the device was registered
</ParamField>

**Request parameters**

The request body fields depend on the URL query parameter `type`. The fields for each value are listed below.

### `type=ipsip` — SIP phone, direct IP (update)

<ParamField body="id" type="string" required>
  Device ID, from the response of "Add a device" or from "List devices" (max length 64)
  Example: `sw8kjx`
</ParamField>

<ParamField body="uri" type="string" required>
  Device address, ip:port (max length 100)
  Example: `192.168.1.50:5060`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `3rd-floor meeting room phone`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `East wing, 3F`
</ParamField>


Request example:

```json
{
  "display_name": "3rd-floor meeting room phone",
  "gw": "devgw-1",
  "id": "sw8kjx",
  "remark": "East wing, 3F",
  "uri": "192.168.1.50:5060"
}
```

### `type=regsip` — SIP phone, registration mode (update)

<ParamField body="id" type="string" required>
  Device ID, from the response of "Add a device" or from "List devices" (max length 64)
  Example: `sw8kjx`
</ParamField>

<ParamField body="username" type="string" required>
  Username; the account the device uses to register with the gateway; must not contain : (max length 100)
  Example: `6001`
</ParamField>

<ParamField body="auth_pwd" type="string" required>
  Password; must match the device configuration (max length 50)
  Example: `Abc123456`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `3rd-floor meeting room phone`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `East wing, 3F`
</ParamField>


Request example:

```json
{
  "auth_pwd": "Abc123456",
  "display_name": "3rd-floor meeting room phone",
  "gw": "devgw-1",
  "id": "sw8kjx",
  "remark": "East wing, 3F",
  "username": "6001"
}
```

### `type=iph323` — H.323 endpoint, direct IP (update)

<ParamField body="id" type="string" required>
  Device ID, from the response of "Add a device" or from "List devices" (max length 64)
  Example: `sw8kjx`
</ParamField>

<ParamField body="uri" type="string" required>
  Device address, ip:port (max length 100)
  Example: `192.168.1.60:1720`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `3rd-floor meeting room endpoint`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `East wing, 3F`
</ParamField>


Request example:

```json
{
  "display_name": "3rd-floor meeting room endpoint",
  "gw": "devgw-1",
  "id": "sw8kjx",
  "remark": "East wing, 3F",
  "uri": "192.168.1.60:1720"
}
```

### `type=regh323` — H.323 endpoint, registration mode (update)

<ParamField body="id" type="string" required>
  Device ID, from the response of "Add a device" or from "List devices" (max length 64)
  Example: `sw8kjx`
</ParamField>

<ParamField body="username" type="string" required>
  Username; must be a short numeric extension (max length 100)
  Example: `6002`
</ParamField>

<ParamField body="auth_pwd" type="string" required>
  Password; must match the device configuration (max length 50)
  Example: `Abc123456`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `3rd-floor meeting room endpoint`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `East wing, 3F`
</ParamField>


Request example:

```json
{
  "auth_pwd": "Abc123456",
  "display_name": "3rd-floor meeting room endpoint",
  "gw": "devgw-1",
  "id": "sw8kjx",
  "remark": "East wing, 3F",
  "username": "6002"
}
```

### `type=gb28181` — GB28181 surveillance device (update)

<ParamField body="id" type="string" required>
  Device ID, from the response of "Add a device" or from "List devices" (max length 64)
  Example: `sw8kjx`
</ParamField>

<ParamField body="sip_no" type="string" required>
  Device SIP number, 18–20 digits; can be generated with "Generate a GB28181 device SIP number" (max length 20)
  Example: `33010806661328458475`
</ParamField>

<ParamField body="auth_pwd" type="string" required>
  Password; must match the GB28181 settings on the device (max length 50)
  Example: `Abc123456`
</ParamField>

<ParamField body="subjects" type="object">
  Channel number → name: the video feeds under one device. After registration, you can also add or change them with "Set a GB28181 device channel"
  Example: `{"33010806661329301268":"Guest seats"}`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `Dome camera 1`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `Lobby entrance`
</ParamField>


Request example:

```json
{
  "auth_pwd": "Abc123456",
  "display_name": "Dome camera 1",
  "gw": "devgw-1",
  "id": "sw8kjx",
  "remark": "Lobby entrance",
  "sip_no": "33010806661328458475",
  "subjects": {
    "33010806661329301268": "Guest seats"
  }
}
```

### `type=rtsp` — RTSP stream pull (update)

<ParamField body="id" type="string" required>
  Device ID, from the response of "Add a device" or from "List devices" (max length 64)
  Example: `sw8kjx`
</ParamField>

<ParamField body="uri" type="string" required>
  RTSP stream URL; must start with rtsp (max length 100)
  Example: `rtsp://192.168.1.70:554/stream1`
</ParamField>

<ParamField body="display_name" type="string" required>
  Display name; the device's display name after it joins the channel (max length 100)
  Example: `Lobby camera`
</ParamField>

<ParamField body="transport_type" type="string">
  Transport: UDP (default) | TCP
  Example: `TCP`
</ParamField>

<ParamField body="gw" type="string" required>
  Device gateway. For values, see "List device gateways" (max length 60)
  Example: `devgw-1`
</ParamField>

<ParamField body="remark" type="string">
  Remarks (max length 200)
  Example: `Lobby entrance`
</ParamField>


Request example:

```json
{
  "display_name": "Lobby camera",
  "gw": "devgw-1",
  "id": "sw8kjx",
  "remark": "Lobby entrance",
  "transport_type": "TCP",
  "uri": "rtsp://192.168.1.70:554/stream1"
}
```

**Response parameters**

<ResponseField name="data" type="string">
  ID of the updated device
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": ""
}
```

---

## Set a GB28181 device channel

`POST /server/v1/agent/set-gb28181-subject`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Add or update a channel of a GB28181 device (one GB28181 device can have multiple camera channels).
If the channel number already exists, its name is updated; otherwise a new channel is added.

You can also pass them in bulk with subjects when calling "Add a device".

**Request parameters**

<ParamField body="id" type="string" required>
  Device ID, from the response of "Add a device" or from "List devices" (max length 64)
  Example: `sw8kjx`
</ParamField>

<ParamField body="subject" type="string" required>
  Channel number; must match the device's actual configuration. Can be generated automatically per the standard with "Generate a GB28181 channel number" (max length 20)
  Example: `50010700001320000001`
</ParamField>

<ParamField body="name" type="string" required>
  GB28181 channel name, used in the channel to tell apart the different video feeds of the same device (max length 100)
  Example: `Guest seats`
</ParamField>


Request example:

```json
{
  "id": "sw8kjx",
  "name": "Guest seats",
  "subject": "50010700001320000001"
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

## Delete a GB28181 device channel

`POST /server/v1/agent/del-gb28181-subject`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Delete one channel of a GB28181 device. The device itself is not affected; the GB28181 channel simply can no longer be invited to a channel.
If the GB28181 channel is currently in a channel, it is removed from that channel first.

**Request parameters**

<ParamField body="id" type="string" required>
  Device ID (max length 64)
  Example: `sw8kjx`
</ParamField>

<ParamField body="subject" type="string" required>
  GB28181 channel number (max length 20)
  Example: `50010700001320000001`
</ParamField>


Request example:

```json
{
  "id": "sw8kjx",
  "subject": "50010700001320000001"
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

## Generate a GB28181 channel number

`POST /server/v1/agent/gen-gb28181-subject`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Generate an unused channel number for the specified device according to the GB28181 standard, so you avoid format errors when building numbers yourself
or conflicts with existing channels.

The generated number is only returned to you and is not registered automatically—after getting it, you still need to call "Set a GB28181 device channel"
and provide the channel name.

**Request parameters**

<ParamField body="id" type="string" required>
  Device ID (max length 64)
  Example: `sw8kjx`
</ParamField>


Request example:

```json
{
  "id": "sw8kjx"
}
```

**Response parameters**

<ResponseField name="data" type="string">
  Generated channel number, not registered yet; call "Set a GB28181 device channel" next
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": ""
}
```

---

## Generate a GB28181 device SIP number

`POST /server/v1/agent/gen-gb28181-sip-no`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Generate an unused GB28181 device SIP number for registering a new GB28181 device (sip_no when type=gb28181).
No request parameters.

Likewise, this only returns a number and doesn't create a device automatically.

**Request parameters**

None

**Response parameters**

<ResponseField name="data" type="string">
  Generated device SIP number; no device has been created yet
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": ""
}
```

---

## Control GB28181 device PTZ (direction and zoom)

`POST /server/v1/agent/gb28181-ptz`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Control the PTZ (direction and zoom) of a GB28181 camera.

command supports up/down/left/right/zoomin/zoomout/stop, and a "+" combination of two actions (such as left+up).
Speed ranges from 0 to 255: when speed_h/speed_v/speed_zoom is 0 it falls back to speed; when speed is also 0, the
gateway default speed of 50 is used.

The device must already be registered with "Add a device" (type gb28181); otherwise the gateway it belongs to can't be located.

**Request parameters**

<ParamField body="contact" type="string" required>
  Device number, the SIP number of a GB28181 device (max length 20)
  Example: `33010806661328458475`
</ParamField>

<ParamField body="subject" type="string" required>
  Channel number; must match the device configuration. Can be generated with "Generate a GB28181 channel number" (max length 20)
  Example: `33010806661329301268`
</ParamField>

<ParamField body="command" type="string" required>
  PTZ action; supports a + combination of two actions
  Example: `left+up`
</ParamField>

<ParamField body="speed" type="integer">
  Base speed
  Example: `50`
</ParamField>

<ParamField body="speed_h" type="integer">
  Horizontal rotation speed
  Example: `50`
</ParamField>

<ParamField body="speed_v" type="integer">
  Vertical rotation speed
  Example: `50`
</ParamField>

<ParamField body="speed_zoom" type="integer">
  Zoom speed
  Example: `50`
</ParamField>


Request example:

```json
{
  "command": "left+up",
  "contact": "33010806661328458475",
  "speed": 50,
  "speed_h": 50,
  "speed_v": 50,
  "speed_zoom": 50,
  "subject": "33010806661329301268"
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

## Manage GB28181 device preset positions

`POST /server/v1/agent/gb28181-preset`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Operate the preset positions of a GB28181 camera: set saves the current position, goto moves to a preset position, and delete removes a preset position;
all three actions require the preset number num (1–255).

As with "Control GB28181 device PTZ (direction and zoom)", the device must already be registered.

**Request parameters**

<ParamField body="contact" type="string" required>
  Device number, the SIP number of a GB28181 device (max length 20)
  Example: `33010806661328458475`
</ParamField>

<ParamField body="subject" type="string" required>
  GB28181 channel number (max length 20)
  Example: `33010806661329301268`
</ParamField>

<ParamField body="action" type="string" required>
  Preset action: set saves the current position, goto moves to the preset position, delete removes the preset position
  Example: `goto`
</ParamField>

<ParamField body="num" type="integer" required>
  Preset number
  Example: `1`
</ParamField>


Request example:

```json
{
  "action": "goto",
  "contact": "33010806661328458475",
  "num": 1,
  "subject": "33010806661329301268"
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

## List device gateways

`POST /server/v1/agent/list-gw`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

List the available device gateways. Call this before registering a device to get the value for gw.

A device gateway is the translation layer between external devices and RTC: SIP, H.323, and GB28181 each have their own signaling protocol,
which the gateway handles, converting the media into a format RTC can use. Different gateways support different integration types,
so filter with type; for values, see the "Device integration guide".

**URL query parameters**

<ParamField query="type" type="string" required>
  Filter by integration type; returns only gateways that support it. For values, see the "Device integration guide"
</ParamField>

**Request parameters**

None (all parameters are passed in the URL query string)

**Response parameters**

<ResponseField name="id" type="string">
  gw id
</ResponseField>

<ResponseField name="types" type="array<integer>">
  Agent type
</ResponseField>

<ResponseField name="heartbeat_at" type="integer">
  Last heartbeat time
</ResponseField>

<ResponseField name="host" type="string">
  API endpoint for RTC to call the device gateway
</ResponseField>

<ResponseField name="load" type="object">
  Node load piggybacked on the most recent heartbeat (empty for older gateways that don't report it)
  <Expandable title="Fields">
    <ResponseField name="cpu_usage" type="number">
      CPU usage (0–100)
    </ResponseField>

    <ResponseField name="mem_usage" type="number">
      Memory usage (0–100)
    </ResponseField>

    <ResponseField name="metrics" type="object">
      Business metric name-value pairs (such as tasks = number of tasks in progress)
    </ResponseField>

  </Expandable>
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": [
    {
      "heartbeat_at": 0,
      "host": "",
      "id": "",
      "load": {
        "cpu_usage": 0,
        "mem_usage": 0,
        "metrics": {}
      },
      "types": [
        0
      ]
    }
  ]
}
```

---

## List device gateway platform info

`POST /server/v1/agent/list-gw-info`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Get the gateway's platform-side info for configuring the device side.

The typical use is GB28181 integration: a GB28181 camera needs the "upstream platform" SIP number, domain, IP, and
port filled in on the device side. Take these values from here and enter them on the camera's GB28181 settings page so the device can register.

How this differs from "List device gateways": that one answers "which gateways do we have"; this one answers "to connect a device to a given gateway,
what should be filled in on the device side".

**URL query parameters**

<ParamField query="type" type="string" required>
  Integration type; different types return different platform info fields. For values, see the "Device integration guide"
</ParamField>

**Request parameters**

None (all parameters are passed in the URL query string)

**Response parameters**

<ResponseField name="id" type="string">
  gw id
</ResponseField>

<ResponseField name="types" type="array<integer>">
  Agent type
</ResponseField>

<ResponseField name="heartbeat_at" type="integer">
  Last heartbeat time
</ResponseField>

<ResponseField name="host" type="string">
  API endpoint for RTC to call the device gateway
</ResponseField>

<ResponseField name="load" type="object">
  Node load piggybacked on the most recent heartbeat (empty for older gateways that don't report it)
  <Expandable title="Fields">
    <ResponseField name="cpu_usage" type="number">
      CPU usage (0–100)
    </ResponseField>

    <ResponseField name="mem_usage" type="number">
      Memory usage (0–100)
    </ResponseField>

    <ResponseField name="metrics" type="object">
      Business metric name-value pairs (such as tasks = number of tasks in progress)
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="info" type="any">
  Gateway platform info
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": [
    {
      "heartbeat_at": 0,
      "host": "",
      "id": "",
      "info": null,
      "load": {
        "cpu_usage": 0,
        "mem_usage": 0,
        "metrics": {}
      },
      "types": [
        0
      ]
    }
  ]
}
```

---

## Call a gateway API

`POST /server/v1/agent/call-gw-api`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Pass a call through to the device gateway's own API, for troubleshooting and operations scenarios the regular endpoints don't cover
(such as querying the gateway's internal state or triggering a device reconnect). The data in the response is what the gateway returns, as is.

This is a low-level endpoint for operations: the values of api and params depend on the gateway version, with no stability guarantee.
Don't rely on it in business code; prefer the other named endpoints in this group.

**Request parameters**

<ParamField body="gw" type="string" required>
  Gateway. For values, see "List device gateways"
  Example: `devgw-1`
</ParamField>

<ParamField body="api" type="string" required>
  The gateway's own API path
  Example: `/api/v1/status`
</ParamField>

<ParamField body="params" type="object">
  Parameters passed to the gateway API
  Example: `{"device_id":"sw8kjx"}`
</ParamField>


Request example:

```json
{
  "api": "/api/v1/status",
  "gw": "devgw-1",
  "params": {
    "device_id": "sw8kjx"
  }
}
```

**Response parameters**

<ResponseField name="data" type="any">
  Data returned by the gateway as is (structure varies)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": null
}
```

---

## Delete a device

`POST /server/v1/agent/delete`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Delete a registered device. The data in the response is the ID of the deleted device.

If the device is currently in a channel, it is removed from the channel first. After deletion, the same physical device can be registered again,
but it gets a new device ID.

**Request parameters**

<ParamField body="id" type="string" required>
  Device ID (max length 64)
  Example: `sw8kjx`
</ParamField>


Request example:

```json
{
  "id": "sw8kjx"
}
```

**Response parameters**

<ResponseField name="data" type="string">
  ID of the deleted device
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": ""
}
```

---

## Get device details

`POST /server/v1/agent/detail`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Query the details of a single device, including connection parameters, the gateway it belongs to, and online status.
The device id comes from the response of "Add a device" or from "List devices".

**Request parameters**

<ParamField body="id" type="string" required>
  Device ID (max length 64)
  Example: `sw8kjx`
</ParamField>


Request example:

```json
{
  "id": "sw8kjx"
}
```

**Response parameters**

<ResponseField name="id" type="string">
  agent id
</ResponseField>

<ResponseField name="name" type="string">
  Agent name
</ResponseField>

<ResponseField name="type" type="integer">
  Agent type
</ResponseField>

<ResponseField name="status" type="integer">
  Online status
</ResponseField>

<ResponseField name="heartbeat_at" type="integer">
  Last heartbeat time
</ResponseField>

<ResponseField name="contact" type="string">
  Device identifier
</ResponseField>

<ResponseField name="conn_params" type="object">
  Connection parameters with secrets removed; see NewAgent
</ResponseField>

<ResponseField name="gw" type="string">
  Device gateway
</ResponseField>

<ResponseField name="remark" type="string">
  Remarks
</ResponseField>

<ResponseField name="subjects" type="array<object>">
  List of GB28181 channels, each with its most recently reported location
  <Expandable title="Element fields">
    <ResponseField name="subject" type="string">
      Channel number; empty means device-level location
    </ResponseField>

    <ResponseField name="name" type="string">
      GB28181 channel name
    </ResponseField>

    <ResponseField name="lng" type="number">
      Longitude
    </ResponseField>

    <ResponseField name="lat" type="number">
      Latitude
    </ResponseField>

    <ResponseField name="alt" type="number">
      Altitude (meters)
    </ResponseField>

    <ResponseField name="speed" type="number">
      Speed
    </ResponseField>

    <ResponseField name="dir" type="number">
      Heading (degrees)
    </ResponseField>

    <ResponseField name="pos_at" type="integer">
      Device-side location time; 0 means a location has never been reported
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="pos" type="object">
  Device-level location (the report that carries no channel number)
  <Expandable title="Fields">
    <ResponseField name="lng" type="number">
      Longitude
    </ResponseField>

    <ResponseField name="lat" type="number">
      Latitude
    </ResponseField>

    <ResponseField name="alt" type="number">
      Altitude (meters)
    </ResponseField>

    <ResponseField name="speed" type="number">
      Speed
    </ResponseField>

    <ResponseField name="dir" type="number">
      Heading (degrees)
    </ResponseField>

    <ResponseField name="pos_at" type="integer">
      Device-side location time
    </ResponseField>

  </Expandable>
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "conn_params": {},
    "contact": "",
    "gw": "",
    "heartbeat_at": 0,
    "id": "",
    "name": "",
    "pos": {
      "alt": 0,
      "dir": 0,
      "lat": 0,
      "lng": 0,
      "pos_at": 0,
      "speed": 0
    },
    "remark": "",
    "status": 0,
    "subjects": [
      {
        "alt": 0,
        "dir": 0,
        "lat": 0,
        "lng": 0,
        "name": "",
        "pos_at": 0,
        "speed": 0,
        "subject": ""
      }
    ],
    "type": 0
  }
}
```

---

## List devices

`POST /server/v1/agent/list-invite`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

List the devices available for invitation with pagination, typically so users can pick devices in your UI.

Each channel of a GB28181 device takes its own entry. The contact (device identifier) in the response is the value to pass to
"Invite devices to the channel".

**Request parameters**

<ParamField body="type" type="array<integer>" required>
  Agent type: 2 SIP, 3 H.323, 4 GB28181 surveillance, 5 RTSP stream pull
  Example: `2,4`
</ParamField>

<ParamField body="keyword" type="string">
  Keyword; fuzzy-matches the display name and device identifier (max length 100)
  Example: `meeting room`
</ParamField>

<ParamField body="name" type="string">
  Display name, exact match (max length 100)
  Example: `Guest seats camera`
</ParamField>

<ParamField body="contact" type="string">
  Device identifier, exact match (max length 100)
  Example: `50010700001320000001`
</ParamField>

<ParamField body="page" type="integer">
  Page number, starting from 1
  Example: `1`
</ParamField>

<ParamField body="per-page" type="integer">
  Page size
  Example: `10`
</ParamField>


Request example:

```json
{
  "contact": "50010700001320000001",
  "keyword": "meeting room",
  "name": "Guest seats camera",
  "page": 1,
  "per-page": 10,
  "type": "2,4"
}
```

**Response parameters**

<ResponseField name="id" type="string">
  agent id
</ResponseField>

<ResponseField name="name" type="string">
  Agent name
</ResponseField>

<ResponseField name="type" type="integer">
  Agent type
</ResponseField>

<ResponseField name="status" type="integer">
  Online status
</ResponseField>

<ResponseField name="heartbeat_at" type="integer">
  Last heartbeat time
</ResponseField>

<ResponseField name="contact" type="string">
  Device identifier
</ResponseField>

<ResponseField name="conn_params" type="object">
  Connection parameters with secrets removed; see NewAgent
</ResponseField>

<ResponseField name="gw" type="string">
  Device gateway
</ResponseField>

<ResponseField name="remark" type="string">
  Remarks
</ResponseField>

<ResponseField name="subjects" type="array<object>">
  List of GB28181 channels, each with its most recently reported location
  <Expandable title="Element fields">
    <ResponseField name="subject" type="string">
      Channel number; empty means device-level location
    </ResponseField>

    <ResponseField name="name" type="string">
      GB28181 channel name
    </ResponseField>

    <ResponseField name="lng" type="number">
      Longitude
    </ResponseField>

    <ResponseField name="lat" type="number">
      Latitude
    </ResponseField>

    <ResponseField name="alt" type="number">
      Altitude (meters)
    </ResponseField>

    <ResponseField name="speed" type="number">
      Speed
    </ResponseField>

    <ResponseField name="dir" type="number">
      Heading (degrees)
    </ResponseField>

    <ResponseField name="pos_at" type="integer">
      Device-side location time; 0 means a location has never been reported
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="pos" type="object">
  Device-level location (the report that carries no channel number)
  <Expandable title="Fields">
    <ResponseField name="lng" type="number">
      Longitude
    </ResponseField>

    <ResponseField name="lat" type="number">
      Latitude
    </ResponseField>

    <ResponseField name="alt" type="number">
      Altitude (meters)
    </ResponseField>

    <ResponseField name="speed" type="number">
      Speed
    </ResponseField>

    <ResponseField name="dir" type="number">
      Heading (degrees)
    </ResponseField>

    <ResponseField name="pos_at" type="integer">
      Device-side location time
    </ResponseField>

  </Expandable>
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
      "conn_params": {},
      "contact": "",
      "gw": "",
      "heartbeat_at": 0,
      "id": "",
      "name": "",
      "pos": {
        "alt": 0,
        "dir": 0,
        "lat": 0,
        "lng": 0,
        "pos_at": 0,
        "speed": 0
      },
      "remark": "",
      "status": 0,
      "subjects": [
        {
          "alt": 0,
          "dir": 0,
          "lat": 0,
          "lng": 0,
          "name": "",
          "pos_at": 0,
          "speed": 0,
          "subject": ""
        }
      ],
      "type": 0
    }
  ]
}
```

---

## Invite devices to the channel

`POST /server/v1/agent/invite`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Bring devices into a channel; you can invite several at once. Take each device's type and contact from "List devices".

Devices join asynchronously: a successful response only means the invitation has been sent; the device is actually online when the user_join
callback arrives (the device's uid has the _agent_ prefix). Inviting a device that is already in the channel doesn't bring it in again.

The agent_join callback is triggered before the device accepts the invitation. If you subscribe to this event, you must return sid as required,
otherwise the device can't join the channel—see the "Callback events guide" for details.

**Request parameters**

<ParamField body="agents" type="array<any>" required>
  Devices to invite
</ParamField>

<ParamField body="no" type="string" required>
  Target room number (the meeting number for an SMeeting-layer app, or the channel name for an SRTC-layer app)
  Example: `fire`
</ParamField>


Request example:

```json
{
  "agents": [
    null
  ],
  "no": "fire"
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

## Turn device video on or off

`POST /server/v1/agent/set-camera-enabled`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Turn a device's camera on or off. Unlike a regular client, a device can't operate this itself; it can only be controlled from the server.

If you subscribe to the agent_operate callback, this operation first asks your backend, and a non-zero response means rejection;
if you don't subscribe, it is allowed by default.

**Request parameters**

<ParamField body="uid" type="string">
  In-channel user ID of the device; omit to apply to all devices in the channel. Has the _agent_ prefix; get it from "List online or offline users" or the user_join callback (letters, digits, underscores (_), and hyphens (-) only)
  Example: `_agent_co63jg6g54hu3b0xhtie`
</ParamField>

<ParamField body="channel" type="string" required>
  Channel name (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="enabled" type="boolean">
  Whether to turn it on
</ParamField>

<ParamField body="op_uid" type="string">
  Operator uid, used for auditing
  Example: `1001`
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "enabled": false,
  "op_uid": "1001",
  "uid": "_agent_co63jg6g54hu3b0xhtie"
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

## Turn device audio on or off

`POST /server/v1/agent/set-mic-enabled`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Turn a device's microphone on or off; same semantics as "Turn device video on or off".

**Request parameters**

<ParamField body="uid" type="string">
  In-channel user ID of the device; omit to apply to all devices in the channel. Has the _agent_ prefix (letters, digits, underscores (_), and hyphens (-) only)
  Example: `_agent_co63jg6g54hu3b0xhtie`
</ParamField>

<ParamField body="channel" type="string" required>
  Channel name (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="enabled" type="boolean">
  Whether to turn it on
</ParamField>

<ParamField body="op_uid" type="string">
  Operator uid, used for auditing
  Example: `1001`
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "enabled": false,
  "op_uid": "1001",
  "uid": "_agent_co63jg6g54hu3b0xhtie"
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

