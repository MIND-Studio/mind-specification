# Mind Protocol §1 — Pod container layout

The agreed set of paths a Mind-compliant pod has, what each one is for, who owns it, and the RDF shapes for the load-bearing resources. This is the contract that makes "one WebID, many apps" a fact rather than a hope.

<div class="diagram-block protocol-intro">
  <div class="protocol-intro-meta">
    <span class="protocol-intro-tag">§1 · DRAFTED v0.1</span>
    <h3 class="protocol-intro-title">A shared map of every Mind pod</h3>
  </div>
  <p class="protocol-intro-body">A Mind-compliant pod has well-known folders for agents, apps, and shared data. Apps don't invent paths — they use the agreed map. This is what makes your calendar entry visible to multiple apps, your agent fleet operable from any tool, and your inbox findable by senders on other pods.</p>
  <div class="protocol-intro-key">
    <div class="key-item"><span class="key-label">KEY IDEA</span><span class="key-value">Three zones: <code>/agents/</code>, <code>/apps/{name}/</code>, and top-level shared data (<code>/calendar/</code>, <code>/contacts/</code>, …).</span></div>
    <div class="key-item"><span class="key-label">DEPENDS ON</span><span class="key-value">Solid (paths) · WAC/ACP (permissions)</span></div>
    <div class="key-item"><span class="key-label">USED BY</span><span class="key-value">Every app, worker, and external operator</span></div>
  </div>
</div>

<div class="diagram-block diagram-zones">
  <div class="zone zone-agent">
    <div class="zone-head">
      <span class="zone-icon">◆</span>
      <span class="zone-name">AGENT ZONE</span>
      <span class="zone-path"><code>/agents/</code></span>
    </div>
    <div class="zone-desc">Everything the agent runtime owns: roster, drafts, audit log, control queue, per-agent state and memory.</div>
    <div class="zone-paths">
      <span class="zone-path-chip">roster.ttl</span>
      <span class="zone-path-chip">control/</span>
      <span class="zone-path-chip">drafts/</span>
      <span class="zone-path-chip">audit/</span>
      <span class="zone-path-chip">{agent-id}/</span>
    </div>
  </div>

  <div class="zone zone-apps">
    <div class="zone-head">
      <span class="zone-icon">◉</span>
      <span class="zone-name">APPS ZONE</span>
      <span class="zone-path"><code>/apps/{name}/</code></span>
    </div>
    <div class="zone-desc">Per-app private state, sandboxed by app. The Marketplace app reads <code>/apps/marketplace/</code>; it cannot peek into <code>/apps/health/</code> without an explicit grant.</div>
    <div class="zone-paths">
      <span class="zone-path-chip">compass/</span>
      <span class="zone-path-chip">marketplace/</span>
      <span class="zone-path-chip">health/</span>
      <span class="zone-path-chip">chat/</span>
      <span class="zone-path-chip">codespaces/</span>
      <span class="zone-path-chip">social/</span>
    </div>
  </div>

  <div class="zone zone-shared">
    <div class="zone-head">
      <span class="zone-icon">▢</span>
      <span class="zone-name">SHARED USER DATA</span>
      <span class="zone-path">top-level containers</span>
    </div>
    <div class="zone-desc">Top-level domains any app or agent may read (subject to ACLs). The same calendar entry shows up in your scheduling app, your assistant agent, and your mail app.</div>
    <div class="zone-paths">
      <span class="zone-path-chip">calendar/</span>
      <span class="zone-path-chip">contacts/</span>
      <span class="zone-path-chip">photos/</span>
      <span class="zone-path-chip">inbox/</span>
      <span class="zone-path-chip">research/</span>
      <span class="zone-path-chip">tasks/</span>
      <span class="zone-path-chip">projects/</span>
    </div>
  </div>
</div>

> Status: drafted v0.1. Anchored to [README →](../README.md).

---

## Purpose

Today each prototype invents its own pod paths. `marketplace` would want `/listings/`; `codespaces` would want `/codespaces/`; `agents` would want `/agents/`. That works in isolation. The moment a single WebID hosts all six apps' data — and an external operator (e.g. Compass) needs to read state across them — we need a shared map.

§1 is that map. It groups paths into three zones:

- **Agent zone** (`/agents/`) — everything the agent runtime owns
- **Apps zone** (`/apps/{name}/`) — per-app private state, sandboxed by app
- **Shared user data** (`/calendar/`, `/contacts/`, …) — top-level domains that any app or agent may read

---

## Vocab

All Mind-defined terms live under the prefix:

```turtle
@prefix mind: <https://mind.dev/ns/v1#> .  # URI is provisional
```

Where existing standard vocabs cover a need, Mind reuses rather than invents — `schema:` (schema.org), `as:` (ActivityStreams 2), `vcard:`, `ical:`, `ldp:`, `solid:`.

---

## Top-level container layout

A Mind-compliant pod has the following top-level containers. Not every pod has every container — apps create what they need on first run.

```
{pod-root}/
├── profile/card                # WebID document + mind:services predicate (§3)
│
├── agents/                     # the user's private agent fleet
│   ├── roster.ttl              # mind:Agent list — who's on the team
│   ├── user-model.ttl          # shared mind:Observation list
│   ├── audit/                  # append-only Merkle-chained log
│   ├── control/                # operator writes here; runtime watches — §2
│   ├── drafts/                 # agent-produced drafts pending approval
│   │   └── {YYYY-MM-DD}/{seq}.ttl
│   └── {agent-id}/
│       ├── state.ttl           # status, last delivery, next scheduled action
│       ├── memory/             # session transcripts + vector embeddings
│       ├── skills/             # learned skills (v0.2)
│       └── hand.ttl            # agent's pod-scope declaration
│
├── apps/                       # per-app private state — sandboxed by app
│   ├── compass/                # operator state (if/when Compass stores in pod)
│   ├── marketplace/
│   │   └── listings/           # schema:Offer items
│   ├── health/
│   │   └── records/            # health entries (shape TBD)
│   ├── chat/
│   │   └── conversations/      # threaded conversations
│   ├── codespaces/
│   │   ├── repos/{owner}/{name}/   # bare git refs + metadata
│   │   ├── pages-config.ttl        # Mind Pages publishing config
│   │   └── public-sites/{name}/    # world-readable published sites
│   └── social/
│       ├── posts/              # as:Note posts
│       ├── friends/            # as:Follow references
│       └── duels/              # async game state
│
├── inbox/                      # LDN inbox — §4 — app-agnostic
│
├── calendar/                   # ical:Vevent  (v0.2) — shared user data
├── tasks/                      # schema:Action (v0.2)
├── projects/                   # schema:Project (v0.2)
├── contacts/                   # vcard:Individual (v0.2)
├── research/                   # used by Researcher agent + reading-list apps
│   ├── bookmarks/              # schema:WebPage
│   ├── sources/                # downloaded sources
│   └── briefs/{slug}.md        # Researcher's deliverables
├── wishlist/                   # used by Shopper agent (v0.3)
│
└── services/manifest.ttl       # outside-helper services manifest — see §3
```

Three zones, top-to-bottom: **agents** own `/agents/`; **apps** are sandboxed under `/apps/{name}/`; **shared user data** sits at the top level so multiple apps and agents can use it.

---

## Ownership

| Container | Read | Write | Notes |
|---|---|---|---|
| `/agents/` | user; user's runtime; external operator for status | user's runtime only (except `/agents/control/` — operator writes) | Each agent's reach enforced by pod ACLs declared in its `hand.ttl` |
| `/agents/drafts/` | user; user's runtime | user's runtime (the Scribe etc.); user (edits) | Drafts never go outward without explicit user approval |
| `/apps/{name}/` | the app itself; user; agents (if `hand.ttl` grants it) | the app itself; user | Sandboxed per app. Other apps don't see in here by default. |
| `/apps/codespaces/public-sites/` | world | user; codespaces app | The only sub-container that defaults to world-readable |
| `/inbox/` | user; user's runtime; agents | anyone (LDN target — §4) | Public-write by spec; abuse mitigated by app-level filtering |
| `/calendar/`, `/contacts/`, etc. | per-resource ACL | user; apps and agents granted access | Shared user data — every app may read; writes are gated |

---

## RDF shapes (load-bearing resources)

v0.1 specifies shapes only for the resources external operators and runtimes *have to* agree on. Everything else can evolve per-app and use existing standard vocab.

### `roster.ttl`

```turtle
@prefix mind: <https://mind.dev/ns/v1#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

<#engineer>
  a              mind:Agent ;
  mind:id        "engineer" ;
  mind:role      "Engineer" ;
  mind:scope     </apps/codespaces/repos/> ,
                 </apps/codespaces/repos/alice/bakery-site/branches/agent/> ;
  mind:intensity "low" ;
  mind:enabled   true ;
  mind:executor  mind:PromptExecutor ;          # see §2 — pluggable per agent
  mind:triggers  mind:ScheduleTrigger ,         # see §2 — what wakes the agent
                 mind:PodChangeTrigger ,
                 mind:OperatorTrigger ;
  mind:addedAt   "2026-05-24T09:12:00Z"^^xsd:dateTime .
```

### `{agent-id}/state.ttl`

```turtle
<#state>
  a                    mind:AgentState ;
  mind:status          "working" ;    # idle | working | waiting-approval | paused | errored
  mind:lastDelivery    </agents/drafts/2026-05-24/01.ttl> ;
  mind:lastDeliveryAt  "2026-05-24T08:47:00Z"^^xsd:dateTime ;
  mind:nextAction      "scheduled: nightly digest run" ;
  mind:nextActionAt    "2026-05-25T02:00:00Z"^^xsd:dateTime ;
  mind:updatedAt       "2026-05-24T09:30:00Z"^^xsd:dateTime .
```

### `agents/audit/{YYYY-MM-DD}/{seq}.ttl` (append-only, Merkle-chained)

```turtle
<#entry>
  a                mind:AuditEntry ;
  mind:agent       </agents/engineer/> ;
  mind:event       "draft-created" ;
  mind:target      </agents/drafts/2026-05-24/01.ttl> ;
  mind:timestamp   "2026-05-24T08:47:00Z"^^xsd:dateTime ;
  mind:prevHash    "sha256:9b2f…" ;   # hash of previous entry, chained per-day
  mind:hash        "sha256:4c81…" .
```

### `agents/control/{cmd-id}.ttl` (operator → runtime)

```turtle
<#cmd>
  a                   mind:ControlCommand ;
  mind:targetAgent    </agents/engineer/> ;       # or absent → fleet-wide
  mind:action         "pause" ;                   # pause | resume | stop | approve-draft | reject-draft
  mind:targetResource </agents/drafts/2026-05-24/01.ttl> ;  # for draft actions
  mind:issuedBy       <https://alice.example/profile/card#me> ;
  mind:issuedAt       "2026-05-24T09:31:00Z"^^xsd:dateTime ;
  mind:status         "pending" .                # runtime sets to "ack" | "applied" | "failed"
```

### `agents/user-model.ttl`

```turtle
<#alice>
  a  mind:UserModel ;
  mind:observation <#obs-001> , <#obs-002> .

<#obs-001>
  a                mind:Observation ;
  mind:about       "sign-off-line" ;
  mind:value       "Best regards, Alice from the bakery" ;
  mind:learnedBy   </agents/scribe/> ;
  mind:learnedAt   "2026-05-20T14:00:00Z"^^xsd:dateTime ;
  mind:confidence  0.85 ;
  mind:source      </agents/scribe/memory/2026-05-20-cafe-bistro.ttl> .
```

---

## Naming conventions

- **Containers end with `/`**; resources do not. Standard Solid.
- **Resource filenames use lowercase kebab-case** (`cafe-bistro-inquiry.ttl`), not camelCase or spaces.
- **App folder names use lowercase, no prefix**: `marketplace/`, not `mind-marketplace/`.
- **Audit + drafts are date-bucketed** at `{YYYY-MM-DD}/` to keep individual containers bounded.
- **Agent IDs are lowercase, kebab-case, stable** across runtime swaps (`engineer`, `researcher`, `scribe` — not generated UUIDs).

---

## Discovery

A Mind-compliant app, given a WebID, discovers what the pod contains in this order:

1. Resolve the WebID to its profile document (`profile/card`).
2. Read `solid:storage` to find the pod root.
3. `HEAD` or `GET` the top-level containers from the §1 list; existence is the discovery signal.
4. To find its own data, the app probes `/apps/{its-name}/` and creates it if absent.
5. For service discovery, follow the `mind:services` predicate from the profile to `/services/manifest.ttl` (§3).

An app **must not** 404 if an unexpected top-level container exists — pods are user-owned and may carry app data Mind hasn't standardized yet. Unknown containers are ignored, not rejected.

---

## Out of scope for v0.1

- **Cross-app data sharing.** An app reads its own `/apps/{name}/` and the shared user-data containers. Pulling from another app's container requires explicit ACL grant; the protocol doesn't standardize that flow yet.
- **Cross-pod resource references.** v0.1 only specifies the layout within a single pod; cross-pod references are §4 (LDN) territory.
- **ACL / WAC / ACP rule generation.** The protocol declares *what* each container is for; the runtime is responsible for translating `hand.ttl` scope declarations into actual pod ACLs.
- **Versioning of resources within the pod.** Solid doesn't ship versioning by default; apps that need it (codespaces git history, the audit log's Merkle chain) implement it in-resource.
- **Migration from non-Mind layouts.** A future tool can re-shape an existing pod; the protocol just declares the target shape.

---

## Open questions

- Should `/apps/{name}/` be required to declare a manifest (`/apps/{name}/manifest.ttl`) so the user can see which apps have touched their pod?
- Should `research/`, `wishlist/`, `calendar/` etc. move under `/apps/{some-app}/` if no shared use case emerges, or stay top-level as user-data domains?
- Is `mind:` the right vocab prefix, or do we want a different brand prefix (the umbrella might not be called "Mind" by the time we ship)?
- Is the Merkle-chained audit log worth v0.1, or ceremony that belongs in v0.2 once we know what threats we're defending against?
