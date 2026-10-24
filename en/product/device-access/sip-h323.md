---
title: "SIP / H.323 endpoints"
description: "Step-by-step guide to bringing Huawei, Kedacom, and other SIP / H.323 meeting-room endpoints into meetings: register an account or IP in the admin console, configure the endpoint, dial in, or invite it from the platform, with console and endpoint screenshots."
---

This guide uses a Huawei CloudLink endpoint as the example. Other brands use different menu names, but you fill in the same information. Before you start, read the
[Room Connector overview](/en/product/device-access/overview) to decide between "endpoint registration" and "direct IP".

**Have this information ready**:

| Information | Where to get it | Example |
| --- | --- | --- |
| Device gateway address | The "device access gateway IP" set at deployment; ask the deployment team | `192.168.10.5` |
| SIP port | Default 5060 | `5060` |
| H.323 gatekeeper port | Default 1719 | `1719` |
| Admin console account | Platform administrator | — |

---

## Option 1: Endpoint registration (recommended)

The endpoint registers to the device gateway with an account, so the platform can see whether it's online and dialing needs only the meeting ID.

### 1. Create an account in the admin console

Open **Device management** in the admin console, choose the **SIP** (or **H323**) tab → **Endpoint registration** → **Add account**:

![Add a SIP account](/zh/product/device-access/images/admin-sip-reg-add.png)

| Field | What to enter |
| --- | --- |
| Username | The account the endpoint registers with. **For H.323, digits only** (the endpoint's E.164 short number); for SIP, no colons |
| Password | The authentication password the endpoint uses to register |
| Display name | The name shown after the endpoint enters the meeting, for example "Meeting Room 1" |
| Device gateway | Which gateway the endpoint registers to. If there's only one, choose it |

The H.323 dialog has the same fields:

![Add an H.323 account](/zh/product/device-access/images/admin-h323-reg-add.png)

### 2. Enter the registration details on the endpoint

**SIP endpoint**: find the SIP server (registrar) settings, enable registration, and enter:

| Field on the endpoint | What to enter |
| --- | --- |
| Server address / registrar | Device gateway address |
| Port | 5060 |
| URI / username, authentication username | The "Username" created in the console |
| Authentication password | The "Password" created in the console |
| Transport | UDP or TCP |

![Huawei endpoint SIP registration settings](/zh/product/device-access/images/terminal-sip-register.png)

**H.323 endpoint**: find the gatekeeper (GK) settings, enable registration, and enter:

| Field on the endpoint | What to enter |
| --- | --- |
| GK address | Device gateway address (port 1719) |
| E.164 number | The "Username" created in the console (digits) |
| Authentication username / password | The "Username" and "Password" created in the console |

![Huawei endpoint H.323 registration settings](/zh/product/device-access/images/terminal-h323-register.png)

### 3. Confirm it's online

The endpoint usually shows "Registered". Back in the admin console, when the account status changes to **Online**, registration has succeeded:

![Endpoint registration list](/zh/product/device-access/images/admin-sip-reg-list.png)

Can't register? See the [FAQ](/en/product/device-access/faq#endpoint-cant-register).

---

## Option 2: Direct IP

Use this when the endpoint doesn't support registration or has a fixed IP. The platform must be able to reach the endpoint's IP directly.

Go to **Device management** → **SIP** (or **H323**) → **Direct IP** → **Add device**:

![Add a direct IP device](/zh/product/device-access/images/admin-sip-ip-add.png)

| Field | What to enter |
| --- | --- |
| IP address and port | The endpoint's `IP:port`. Usually `:5060` for SIP and `:1720` for H.323 |
| Display name | The name shown after the endpoint enters the meeting |
| Device gateway | Which gateway calls this endpoint |

Direct IP devices have no online status, so `--` in the list is normal.

---

## Bring the endpoint into the meeting

### The endpoint dials in

On the endpoint's call screen, enter the number and call it like a phone call:

**Registered endpoints**: dial only the **meeting ID**.

![Registered endpoint dialing the meeting ID](/zh/product/device-access/images/terminal-dial-number.png)

**Unregistered endpoints**: dial **`meetingID@deviceGatewayAddress`**.

![Unregistered endpoint dialing meetingID@gatewayAddress](/zh/product/device-access/images/terminal-dial-ip.png)

Once the call connects, the endpoint enters the meeting directly and sees the composite video of the whole meeting.

<Note>
The device gateway can enable an **incoming-call IP allowlist**; when it's on, only endpoints on the list can dial in. It's configured at deployment as needed. If dial-in is rejected, first ask the deployment team whether the allowlist is on.
</Note>

### The platform invites the endpoint

The endpoint receives an incoming call and enters the meeting when answered (or directly, if the endpoint is set to auto-answer). There are three entry points:

**Admin console**: **Meeting management** → open the meeting details → **Invite** → **Invite device** → **Conferencing endpoints**, select the endpoints, and confirm.

![Inviting a device from the admin console](/zh/product/device-access/images/admin-meeting-invite-device.png)

**Meeting client**: during the meeting, the host clicks **Invite** → **Invite device**, selects the endpoints, and sends the invitation.

![Inviting a device from the meeting client](/zh/product/device-access/images/client-invite-device.png)

**Business system via API**: call [Invite devices to the channel](/en/rtc/server-api/agent#invite-devices-to-the-channel); see the [Device integration guide](/en/rtc/server-api/guides/agents) for how.
The host side of the conferencing SDK also has a corresponding method (such as `adminInviteAgent` on Web).

---

## During the meeting

+ The endpoint is a member of the meeting, named by its "Display name"
+ The endpoint sees the **whole meeting composited by the MCU** and hears the mixed audio of the whole meeting
+ The host can **turn the endpoint's microphone and camera on or off** and **remove the endpoint from the meeting** from the meeting client or the console; removing it hangs up the endpoint
+ If the endpoint hangs up, it exits the meeting

---

## Registering endpoints to a third-party platform

If the customer already has its own SIP server or H.323 gatekeeper, the device gateway can also **register to it as an endpoint**
and call devices there. This must be configured at deployment; contact us.
