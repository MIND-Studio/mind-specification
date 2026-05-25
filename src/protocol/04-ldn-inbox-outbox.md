# Mind Protocol §4 — LDN inbox + outbox

Cross-pod messaging. How one user's app sends a message to another user's pod, how workers and external services push asynchronous results into your `/inbox/`, and the shapes those messages take. Built on the W3C [Linked Data Notifications](https://www.w3.org/TR/ldn/) standard.

<div class="diagram-block protocol-intro">
  <div class="protocol-intro-meta">
    <span class="protocol-intro-tag">§4 · DRAFTED v0.1</span>
    <h3 class="protocol-intro-title">Pod-to-pod messaging on top of W3C LDN</h3>
  </div>
  <p class="protocol-intro-body">Every Mind-compliant pod exposes <code>/inbox/</code> as a Linked Data Notifications target. To send something to someone, your app POSTs a Turtle notification to their inbox. To receive, a worker reads your inbox and dispatches to whichever app or agent cares. Mind adds the message <em>shapes</em>; the transport is just LDN.</p>
  <div class="protocol-intro-key">
    <div class="key-item"><span class="key-label">KEY IDEA</span><span class="key-value">Each side stores its own copy. No central server. Idempotent via <code>mind:nonce</code>.</span></div>
    <div class="key-item"><span class="key-label">BUILDS ON</span><span class="key-value"><a href="https://www.w3.org/TR/ldn/">W3C LDN</a> · Solid-OIDC (sender identity)</span></div>
    <div class="key-item"><span class="key-label">USED BY</span><span class="key-value">Marketplace, Chat, Social, async ServiceCall results, draft delivery notices, …</span></div>
  </div>
</div>

<div class="diagram-block diagram-msg-flow">
  <div class="msg-flow-title">CROSS-POD MESSAGE FLOW</div>
  <div class="msg-flow-grid">
    <div class="msg-pod msg-pod-sender">
      <div class="msg-pod-label">ALICE'S POD</div>
      <div class="msg-pod-section"><span class="msg-pod-path">/agents/audit/</span><span class="msg-pod-note">sender records own copy</span></div>
    </div>

    <div class="msg-arrow">
      <div class="msg-arrow-line">POST <code>text/turtle</code></div>
      <div class="msg-arrow-line"><code>Authorization: DPoP</code></div>
      <div class="msg-arrow-line-hr">→</div>
      <div class="msg-arrow-line-note">LDN over HTTPS</div>
    </div>

    <div class="msg-pod msg-pod-recipient">
      <div class="msg-pod-label">BOB'S POD</div>
      <div class="msg-pod-section"><span class="msg-pod-path">/inbox/{id}.ttl</span><span class="msg-pod-note">pod stores the notification</span></div>
      <div class="msg-pod-section accent"><span class="msg-pod-path">router worker</span><span class="msg-pod-note">reads inbox, dispatches by <code>mind:type</code></span></div>
      <div class="msg-pod-section"><span class="msg-pod-path">target app</span><span class="msg-pod-note">processes; optionally sends <code>mind:Received</code> back</span></div>
    </div>
  </div>
  <div class="msg-flow-note">No central server. No queue infrastructure. Both sides keep their own copy in their own pod — Alice in <code>/agents/audit/</code> (or <code>/apps/{x}/sent/</code>), Bob in <code>/inbox/</code> then routed to the relevant app folder.</div>
</div>

> Status: drafted v0.1. Anchored to [README →](../README.md). Depends on [§1](01-pod-layout.md).

---

## Purpose

Mind apps and agents need to send things to other people's pods — a marketplace counter-offer, a chess move in an async duel, a social mention, a draft delivery notice from your agent to your friend's agent. Without a shared messaging contract, each app would invent its own out-of-band channel.

§4 reuses W3C LDN as the transport (every Mind-compliant pod exposes `/inbox/` as an LDN target) and adds Mind-specific **shape conventions** on top — what predicates a notification carries, what types it can be, how recipients verify sender identity, how filtering and rate limiting work.

The Mind protocol does **not** redefine LDN itself. If you can POST to an LDN inbox today, you can already send a Mind notification — you just need to use the right shape.

---

## Inbox semantics

Every Mind-compliant pod exposes `/inbox/` as an LDN target.

- **Discoverable** via a `Link: <inbox-url>; rel="http://www.w3.org/ns/ldp#inbox"` header on the pod's root or on any resource the sender is responding to.
- **Public-write by spec.** CORS allows POST from anywhere. Authentication on the POST is for the *sender* to identify themselves (so the recipient can filter), not to gate write access.
- **Stored on POST.** The pod assigns a URL (e.g. `/inbox/01HVZA1K3M.ttl`) and returns it in the `Location` header.
- **App-level filtering.** What stays vs. gets discarded is decided by workers / apps reading the inbox container, not by the pod itself.

---

## Message shapes

Every Mind notification is a Turtle resource (JSON-LD also acceptable per LDN) carrying a `mind:type` plus a message-type-specific body.

### Base envelope

All Mind notifications share these predicates:

```turtle
@prefix mind: <https://mind.dev/ns/v1#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

<#msg>
  a              mind:Notification ;
  mind:type      mind:DeliveryNotice ;             # the specific type — see below
  mind:from      <https://alice.example/profile/card#me> ;
  mind:to        <https://bob.example/profile/card#me> ;
  mind:sentAt    "2026-05-24T15:00:00Z"^^xsd:dateTime ;
  mind:nonce     "01HVZA1K3M4P9X7B5R0YBNM8W2D" ;   # ULID, prevents replay
  mind:inReplyTo <https://bob.example/inbox/01HVZ9.ttl> ;  # optional — threading
  # ... message-type-specific predicates follow
```

`mind:nonce` is REQUIRED. Recipients dedupe by `(mind:from, mind:nonce)` so a retried POST doesn't fire downstream effects twice.

`mind:inReplyTo` is OPTIONAL but RECOMMENDED for conversational types (Invitation, Mention, ServiceCall). Following the chain reconstructs a thread.

### Types in v0.1

<div class="diagram-block diagram-msg-types">
  <div class="msg-types-grid">
    <div class="msg-type-card">
      <div class="msg-type-iri">mind:DeliveryNotice</div>
      <div class="msg-type-summary">"My agent published something that mentions or affects you."</div>
      <div class="msg-type-meta">
        <span class="meta-row"><span class="meta-k">SENDER</span><span class="meta-v">an agent runtime (e.g. Scribe)</span></span>
        <span class="meta-row"><span class="meta-k">PAYLOAD</span><span class="meta-v"><code>subject</code>, <code>body</code>, <code>ref</code> URL</span></span>
      </div>
    </div>
    <div class="msg-type-card">
      <div class="msg-type-iri">mind:Invitation</div>
      <div class="msg-type-summary">Counter-offer, duel invite, friend request, calendar share.</div>
      <div class="msg-type-meta">
        <span class="meta-row"><span class="meta-k">SENDER</span><span class="meta-v">Marketplace, Social, Chat</span></span>
        <span class="meta-row"><span class="meta-k">PAYLOAD</span><span class="meta-v"><code>subject</code>, <code>context</code>, <code>offer</code>, <code>expiresAt</code></span></span>
      </div>
    </div>
    <div class="msg-type-card">
      <div class="msg-type-iri">mind:Mention</div>
      <div class="msg-type-summary">A social post or document mentioning you.</div>
      <div class="msg-type-meta">
        <span class="meta-row"><span class="meta-k">SENDER</span><span class="meta-v">Social app</span></span>
        <span class="meta-row"><span class="meta-k">PAYLOAD</span><span class="meta-v"><code>context</code>, <code>snippet</code></span></span>
      </div>
    </div>
    <div class="msg-type-card">
      <div class="msg-type-iri">mind:ServiceCall</div>
      <div class="msg-type-summary">Async external service POSTing a result back.</div>
      <div class="msg-type-meta">
        <span class="meta-row"><span class="meta-k">SENDER</span><span class="meta-v">a transcription API, an LLM, …</span></span>
        <span class="meta-row"><span class="meta-k">PAYLOAD</span><span class="meta-v"><code>context</code> (job URL), <code>result</code>, <code>status</code></span></span>
      </div>
    </div>
    <div class="msg-type-card">
      <div class="msg-type-iri">mind:DraftApproval</div>
      <div class="msg-type-summary">Operator approval / rejection of an agent draft (also flows via §2).</div>
      <div class="msg-type-meta">
        <span class="meta-row"><span class="meta-k">SENDER</span><span class="meta-v">Compass on a remote machine</span></span>
        <span class="meta-row"><span class="meta-k">PAYLOAD</span><span class="meta-v">draft ref, decision, reason?</span></span>
      </div>
    </div>
    <div class="msg-type-card receipt">
      <div class="msg-type-iri">mind:Received</div>
      <div class="msg-type-summary">Receipt — "I got your message and processed it."</div>
      <div class="msg-type-meta">
        <span class="meta-row"><span class="meta-k">SENDER</span><span class="meta-v">recipient's router worker</span></span>
        <span class="meta-row"><span class="meta-k">PAYLOAD</span><span class="meta-v"><code>ackOf</code> URL, <code>status</code> (processed / filtered / failed)</span></span>
      </div>
    </div>
  </div>
</div>

Type IRIs are open: third parties may mint their own (`acme:ChessMove`). Apps that don't recognize a type SHOULD store the notification but take no action, so unknown types remain available to other apps.

### Per-type body predicates

**`mind:DeliveryNotice`**
```turtle
  mind:subject "Cafe Bistro brief" ;
  mind:body    "Alice's Scribe agent published a brief mentioning your bakery." ;
  mind:ref     <https://alice.example/agents/scribe/briefs/cafe-bistro.md> .
```

**`mind:Invitation`**
```turtle
  mind:subject     "Counter-offer: €240 for the cargo bike" ;
  mind:context     <https://bob.example/apps/marketplace/listings/cargo-bike.ttl> ;
  mind:offer       <https://alice.example/apps/marketplace/offers/01HVZ.ttl> ;
  mind:expiresAt   "2026-05-31T00:00:00Z"^^xsd:dateTime .
```

**`mind:Mention`**
```turtle
  mind:context  <https://alice.example/apps/social/posts/01HVZ.ttl> ;
  mind:snippet  "great party last night, @bob brought the cake" .
```

**`mind:ServiceCall`**
```turtle
  mind:context   <https://my-cube.local/v1/transcribe/jobs/abc123> ;  # what was called
  mind:result    <https://alice.example/agents/scribe/memory/2026-05-24-call.txt> ;  # where the result was deposited
  mind:status    "completed" .                                        # completed | failed
```

**`mind:Received`**
```turtle
  mind:ackOf  <https://alice.example/inbox/01HVZA.ttl> ;   # the message being acked
  mind:status "processed" .                                # processed | filtered | failed
```

---

## Sending a message (outbox pattern)

There's no central outbox folder — "outbox" is just the *act* of POSTing to another pod's inbox. The pattern:

1. **Compose** the notification (Turtle body, correct type, fresh nonce).
2. **Discover** the recipient's inbox URL by fetching their WebID document and looking for the `ldp:inbox` link.
3. **POST** to that URL with `Content-Type: text/turtle` and your WebID-authenticated DPoP token (so the recipient can verify who you are).
4. **Record** the same message in your own `/agents/audit/{YYYY-MM-DD}/{seq}.ttl` for traceability and conversation history.
5. **Optional: store in your own `/apps/{name}/sent/`** if the sending app wants a "Sent" folder UX (chat does, marketplace probably doesn't).

The sent message lives in **two** places: the recipient's inbox (`/inbox/{id}`) and the sender's audit log. There is intentionally no single source of truth — each side stores its own copy in its own pod.

---

## Receiving a message

What happens after a POST lands in `/inbox/`:

1. **Pod accepts** (or rejects via 403/429 — see [Identity & filtering](#identity--filtering) below) and stores the resource.
2. **A worker watches `/inbox/`** via change subscription (Solid Notifications Protocol; polling fallback). One worker per inbox typically — usually the user's general-purpose inbox-routing worker.
3. **The router worker reads the new notification**, checks the `mind:type`, and dispatches to the right consumer:
   - `mind:DeliveryNotice` → Inbox app, or agent that asked to subscribe
   - `mind:Invitation` → Marketplace, Social, Chat, etc.
   - `mind:Mention` → Social app
   - `mind:ServiceCall` → the agent that originally invoked the service
4. **Consumer processes** the notification: stores something in its own `/apps/{name}/`, fires a notification to the user, triggers an agent run, etc.
5. **Optionally** the consumer POSTs a `mind:Received` receipt back to the sender's inbox.

Notifications stay in `/inbox/` after processing. A separate retention worker reaps them after a configurable window (default: 90 days) into a compact `/inbox/archive/{YYYY-MM}.ttl` summary.

---

## Identity & filtering

Cross-pod messages always present the sender's WebID via a Solid-OIDC-signed request (DPoP token). The recipient's pod can verify the signature and the sender's identity before storing.

Filtering decisions happen in two layers:

### Pod-level (server-side)

The pod itself may reject incoming POSTs without storing them, based on coarse policies:

- **Authenticated-only.** Reject anonymous POSTs (no DPoP). Default ON.
- **Rate limit.** Per-sender cap. Default 100/hour per WebID; configurable.
- **Blocklist.** WebIDs the user explicitly blocks.

Rejection returns `403 Forbidden` (blocked) or `429 Too Many Requests` (rate-limited).

### App-level (after storage)

Once a notification is in `/inbox/`, app-level filters decide whether to act on it. Each app or worker can declare interest:

```turtle
@prefix mind: <https://mind.dev/ns/v1#> .

</apps/marketplace/inbox-filter.ttl#filter>
  a              mind:InboxFilter ;
  mind:type      mind:Invitation ;
  mind:context   </apps/marketplace/> ;
  mind:requires  mind:KnownContact ;       # sender must be in /contacts/
  mind:rateLimit "20/hour/sender" ;
  mind:action    "process" .               # process | quarantine | discard
```

Unmatched notifications are kept in `/inbox/` but not processed by any app. The user can review them via the Inbox app.

### Trust gradients

A `mind:KnownContact` (WebID in `/contacts/`) gets more lenient filtering than an unknown sender. A `mind:Friend` (with reciprocal follow in `/apps/social/friends/`) gets even more. Apps are free to define their own trust gradients; the protocol just provides the inbox + filter shapes.

---

## Receipts (`mind:Received`)

Receipts are **optional** in v0.1 but RECOMMENDED for message types where the sender benefits from knowing the message landed (`mind:Invitation`, `mind:DraftApproval`, `mind:ServiceCall`).

A receipt is itself a notification — same envelope, type `mind:Received`, `mind:ackOf` pointing at the message being acknowledged.

Conventions:

- **`mind:status "processed"`** — recipient's app actually did something with it (e.g. surfaced the invitation to the user).
- **`mind:status "filtered"`** — pod or app accepted but discarded (e.g. rate-limited or blocklisted *after* storage).
- **`mind:status "failed"`** — recipient tried to process but errored.

Senders that need delivery confirmation can wait for the receipt; senders that just need fire-and-forget can ignore it.

---

## Cross-pod threading

Conversations span pods. Each side stores its own copy of each message. The thread is reconstructed by following `mind:inReplyTo` links.

Example, between Alice and Bob:

```
Alice POSTs Invitation → Bob's /inbox/01.ttl
Alice records same msg → Alice's /agents/audit/2026-05-24/01.ttl

Bob POSTs Received     → Alice's /inbox/02.ttl (inReplyTo Bob's /inbox/01.ttl)
Bob records same msg   → Bob's /apps/marketplace/sent/2026-05-24/01.ttl

Alice POSTs reply Inv  → Bob's /inbox/03.ttl (inReplyTo Bob's /inbox/01.ttl)
Alice records          → ...
```

A Chat-style app reconstructs the conversation by reading its own pod's audit + sent + received entries, plus following `mind:inReplyTo` chains across pods (which requires the linked pods to grant read access — usually they do, since they're in conversation).

---

## Spam, blocking, and rate limits

Inboxes are public-write by spec. That's a feature (anyone can reach you) and a risk (anyone can flood you).

Defaults the Mind reference inbox-routing worker SHOULD implement:

- **Per-sender rate limit.** 100 notifications / hour / WebID. Excess returns 429.
- **Anonymous block.** Reject POSTs without DPoP signature. Returns 403.
- **Blocklist.** User-maintained list of WebIDs to reject outright.
- **Greylist.** Unknown senders held in `/inbox/pending/` for user review before reaching app-level routing. Default OFF.

These are policy choices, not protocol requirements. A user who wants an open inbox can disable them; a user who wants a fortress can crank them up.

---

## Out of scope for v0.1

- **End-to-end encryption.** Apps that need it (Chat) can layer per-conversation keys on top — the protocol doesn't define the key exchange.
- **Group conversations.** Native N-to-N messaging needs separate design — fan-out via repeated 1:1 messages works for small groups but doesn't scale.
- **Reliable delivery guarantees.** LDN is fire-and-forget. Receipts give weak ack. True reliable messaging (queues, retries, exactly-once) is a layer above and not specified here.
- **Push to apps.** Mind apps poll their own pod for new inbox items (via change subscription). The pod doesn't push to apps directly.
- **Out-of-band invites.** A URL that bootstraps a contact relationship (e.g. "click this to add me to your contacts and exchange inbox addresses") is useful but not specified in v0.1 — likely v0.2.
- **Federation / search.** Cross-pod search ("find all marketplace listings within 10km") is its own thing; messaging just delivers individual notifications.

---

## Open questions

- **Agent identity when sending on the user's behalf.** Does the agent send with its *own* WebID (cleaner audit) or the user's WebID (recipient sees it as from the user)? Probably the agent's own WebID, with `mind:onBehalfOf <user-webid>` predicate — but this needs more thought.
- **Are receipts opt-in per message or per-type?** v0.1 keeps them optional and per-message. If we move to per-type, the manifest needs a way to declare "I always want receipts for Invitations."
- **Filter declaration location.** Filters live in `/apps/{name}/inbox-filter.ttl` today. Should there be a single user-level `/inbox/filters.ttl` that overrides per-app rules?
- **Inbox sharding.** A heavily-trafficked pod might want `/inbox/marketplace/`, `/inbox/social/`, etc. instead of one inbox. LDN allows multiple inboxes (different `rel="ldp:inbox"` per resource). v0.1 keeps it simple with one root inbox.
- **Schema evolution for shapes.** When `mind:Invitation` v2 adds a required field, what happens to v1 senders? Versioning predicates inside notifications or per-type version IRIs (`mind:InvitationV2`)?
