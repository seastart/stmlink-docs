---
title: "Sign-in and roll call"
description: "Run in-meeting sign-in with the SMeeting Swift SDK: the host starts and ends timed sign-in rounds, members sign in, and you query counts and lists; plus receiving roll call events and answering them with the right ID. Read when adding attendance features to a meeting."
---

### Sign-in

Sign-in is a timed activity: the host starts it, members tap to sign in within the time limit, and the host can view the statistics and the list at any time. Activities are distinguished by `epoch` (round), and a meeting can run multiple rounds.

#### Start and end

```swift
// Start a sign-in round
// dur is in minutes; here it's 30 minutes
try await meeting.signInCreate(dur: 30, desc: "Morning session sign-in")

// End the current round early
try await meeting.signInFinish()
```

`dur` is the duration of the sign-in activity, **in minutes**; the actual start and end times of the activity are given by `beginAt` / `endAt` in the events and lists below.

#### Members sign in

```swift
try await meeting.signInSign()
```

#### Query

```swift
// All sign-in activities of this meeting; now is the server's current time, which you can use to compute the remaining countdown
let (list, now) = try await meeting.signInList()

// Number of members signed in for a round
let count = try await meeting.signInCount(epoch: epoch)

// Sign-in list of a round, optionally filtered by nickname
let details = try await meeting.signInDetail(epoch: epoch, nickname: nil)
```

`SignInfo` fields: `uid` (initiator), `beginAt`, `dur`, `endAt`, `desc`, `nums` (number signed in).
`SignDetailInfo` fields: `id`, `epoch`, `nickname`, `role`, `userId`, `createdAt`.

#### Sign-in events

```swift
func meeting(_ meeting: SMeetingEngine, signInActivity data: SignInActivityEventData) {
    // data.hostId / data.hostName initiator
    // data.epoch  round
    // data.beginAt / data.dur / data.endAt start, end, and duration
    // data.desc   sign-in description
}

func meeting(_ meeting: SMeetingEngine, signInDidFinish data: SignInFinishEventData) {
    // data.hostId / data.hostName / data.epoch
}
```

A typical approach: when you receive `signInActivity`, show a sign-in button with a countdown to `endAt`; when you receive `signInDidFinish`, hide it.

---

### Roll call

When you're called in a roll call, you receive an event:

```swift
func meeting(_ meeting: SMeetingEngine, rollCallNamed data: RollCallNamedEventData) {
    // data.id   identifier of this member in the roll call record; pass it back as-is when answering
    // data.sid  uid of the host who started this roll call
    // data.time server's current time
}
```

To answer, **pass the event's `id` straight back**:

```swift
func meeting(_ meeting: SMeetingEngine, rollCallNamed data: RollCallNamedEventData) {
    Task {
        try await meeting.rollCallAnswer(rollCallUserId: data.id)
    }
}
```

<Warning>
Don't use `data.sid` as the parameter—it's the uid of the host who started the roll call, not the roll call record identifier.
</Warning>

> The Swift SDK currently provides only the member-side ability to answer a roll call. Starting a roll call and querying roll call details are host-side flows that must be done through the server API.
>
> Roll call also requires the feature to be deployed on the server; in environments where it isn't enabled, calls return an "endpoint not found" error.

---

### Related pages

+ [Host controls](/en/meeting/swift/advanced/host-controls)
+ [Events](/en/meeting/swift/events)
