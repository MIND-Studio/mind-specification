# Mind Protocol §2 — Agent control + observation

How an external app (Compass, or anything else that speaks the protocol) reads agent state and sends control signals through the pod — without being the agent runtime itself. Also: how an agent runtime knows when to run.

<div class="diagram-block protocol-intro">
  <div class="protocol-intro-meta">
    <span class="protocol-intro-tag">§2 · DRAFTED v0.1</span>
    <h3 class="protocol-intro-title">Operator ↔ runtime coordination, through the pod</h3>
  </div>
  <p class="protocol-intro-body">The agent runtime and any external operator (Compass, scripts, automation) never call each other directly. They both read and write the pod, and the pod's data model carries the coordination. Swap the runtime out — as long as it watches <code>/agents/control/</code> and writes the same shapes, the operator doesn't notice.</p>
  <div class="protocol-intro-key">
    <div class="key-item"><span class="key-label">KEY IDEA</span><span class="key-value">Pod is the queue, output stream, and shared state. No RPC.</span></div>
    <div class="key-item"><span class="key-label">DEPENDS ON</span><span class="key-value"><a href="01-pod-layout.md">§1 Pod layout</a></span></div>
    <div class="key-item"><span class="key-label">USED BY</span><span class="key-value"><a href="../apps.md#compass">Compass</a>, any agent-runtime worker</span></div>
  </div>
</div>

<div class="diagram-block diagram-coord-flow">
  <div class="coord-actor coord-operator">
    <div class="coord-actor-tag">OPERATOR</div>
    <div class="coord-actor-name">Compass</div>
    <div class="coord-actor-desc">writes commands, reads everything else</div>
  </div>

  <div class="coord-bus">
    <div class="coord-bus-label">POD · <code>/agents/</code></div>
    <div class="coord-bus-cells">
      <div class="coord-cell cmd"><span class="coord-cell-path">control/</span><span class="coord-cell-role">queue · operator → runtime</span></div>
      <div class="coord-cell out"><span class="coord-cell-path">drafts/</span><span class="coord-cell-role">output · runtime → operator</span></div>
      <div class="coord-cell out"><span class="coord-cell-path">audit/</span><span class="coord-cell-role">output · runtime → operator</span></div>
      <div class="coord-cell state"><span class="coord-cell-path">{id}/state.ttl</span><span class="coord-cell-role">shared state</span></div>
    </div>
  </div>

  <div class="coord-actor coord-runtime">
    <div class="coord-actor-tag">RUNTIME</div>
    <div class="coord-actor-name">Agent runtime</div>
    <div class="coord-actor-desc">watches commands, writes drafts / audit / state</div>
  </div>
</div>

---

## Purpose

The agent runtime is a worker. The operator UI (Compass) is an app. They have to coordinate — the operator pauses, resumes, approves drafts; the runtime reports status, produces drafts, writes to the audit log. §2 specifies how that coordination happens.

The whole section rests on one architectural choice: **the operator and the runtime never call each other**. They both read and write the pod, and the pod's data model carries the coordination. This is the "coordinate through data" principle from the architecture overview, made concrete.

```
                      ┌─────────────────────────────────────────────┐
                      │                                             │
                      │     Pod paths under /agents/                │
                      │                                             │
   ┌─────────┐        │  control/    ←─── operator writes commands  │        ┌─────────┐
   │ Compass │ ─writes┼─▶  drafts/    ←─── runtime writes drafts    │ writes─┤ Agent   │
   │ or any  │        │   audit/     ←─── runtime writes log        │        │ runtime │
   │ §2-     │ reads ─┼─▶  state.ttl  ←─── runtime writes status    │ ◀reads─┤         │
   │ speaker │        │                                             │        │         │
   └─────────┘        │                                             │        └─────────┘
                      └─────────────────────────────────────────────┘
```

A new runtime drops in transparently — as long as it watches `/agents/control/` and writes the shapes from §1, Compass doesn't notice the swap.

---

## Reading agent state

Operator-side observability uses four pod paths (all defined in §1):

| Path | Read | Purpose |
|---|---|---|
| `/agents/roster.ttl` | the fleet roster | who's on the team, with role / scope / enabled flag / executor |
| `/agents/{id}/state.ttl` | per-agent status | `mind:status`, `mind:lastDeliveryAt`, `mind:nextActionAt` |
| `/agents/drafts/{YYYY-MM-DD}/{seq}.ttl` | pending approvals | drafts waiting for operator review |
| `/agents/audit/{YYYY-MM-DD}/{seq}.ttl` | recent activity | append-only, Merkle-chained event log |

Live updates: see [Change subscription](#change-subscription) below.

---

## Sending commands

The operator writes a `mind:ControlCommand` to `/agents/control/{cmd-id}.ttl`. The runtime watches the container, picks up the command, executes, and updates the command's `mind:status` in place.

```turtle
@prefix mind: <https://mind.dev/ns/v1#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

<#cmd>
  a                   mind:ControlCommand ;
  mind:targetAgent    </agents/engineer/> ;       # absent → fleet-wide
  mind:action         "pause" ;
  mind:targetResource </agents/drafts/2026-05-24/01.ttl> ;  # for draft actions
  mind:issuedBy       <https://alice.example/profile/card#me> ;
  mind:issuedAt       "2026-05-24T09:31:00Z"^^xsd:dateTime ;
  mind:nonce          "01HVZ8K4P3Q9X2J1R0YBNM5W4D" ;  # ULID, prevents replay
  mind:status         "pending" .                     # runtime updates: ack | applied | failed
```

### Commands in v0.1

| Action | Targets | Effect |
|---|---|---|
| `pause` | agent or fleet | Runtime stops scheduling new runs for the target. Current run completes. |
| `resume` | agent or fleet | Reverse of pause. |
| `stop` | agent or fleet | Pause + cancel current run if possible. |
| `approve-draft` | `targetResource` | Runtime promotes draft → outward delivery (e.g. POSTs LDN). |
| `reject-draft` | `targetResource` | Runtime deletes the draft and writes a `draft-rejected` audit entry. |
| `tick` | agent | Force a scheduler tick now (debugging / responsiveness override). |

### Status lifecycle

`pending` → `ack` (runtime saw it) → `applied` (executed successfully) | `failed` (with `mind:error` predicate).

Commands are append-only from the operator's side; the runtime updates `mind:status` and adds `mind:appliedAt`. The operator never deletes commands — old commands are reaped by a runtime sweep after a retention window (default: 30 days).

### Idempotency

Every command carries a `mind:nonce`. Runtimes deduplicate by nonce so a retried command (network blip, operator double-click) doesn't fire twice.

---

## Triggers — when an agent runs

An agent can fire from four sources, in any combination. The roster entry declares which triggers the agent accepts.

```turtle
<#engineer>
  a                mind:Agent ;
  mind:id          "engineer" ;
  mind:executor    mind:PromptExecutor ;
  mind:triggers    mind:ScheduleTrigger ,
                   mind:PodChangeTrigger ,
                   mind:InboxTrigger ,
                   mind:OperatorTrigger .
```

<div class="diagram-block diagram-triggers">
  <div class="trigger-grid">
    <div class="trigger-card">
      <div class="trigger-icon">⏱</div>
      <div class="trigger-iri">mind:ScheduleTrigger</div>
      <div class="trigger-fires">fires on time</div>
      <div class="trigger-detail"><code>state.ttl</code>'s <code>mind:nextActionAt</code> passes — runtime's local clock</div>
    </div>
    <div class="trigger-card">
      <div class="trigger-icon">∆</div>
      <div class="trigger-iri">mind:PodChangeTrigger</div>
      <div class="trigger-fires">fires on pod writes</div>
      <div class="trigger-detail">change subscription on the agent's <code>hand.ttl</code> scope paths</div>
    </div>
    <div class="trigger-card">
      <div class="trigger-icon">✉</div>
      <div class="trigger-iri">mind:InboxTrigger</div>
      <div class="trigger-fires">fires on LDN messages</div>
      <div class="trigger-detail">new notifications in <code>/inbox/</code> matching <code>mind:interest</code></div>
    </div>
    <div class="trigger-card required">
      <div class="trigger-icon">▶</div>
      <div class="trigger-iri">mind:OperatorTrigger</div>
      <div class="trigger-fires">fires on commands</div>
      <div class="trigger-detail">a <code>mind:ControlCommand</code> targeting the agent — always implicitly accepted</div>
    </div>
  </div>
</div>

`mind:OperatorTrigger` is always implicitly accepted — every agent must honor `pause` / `resume` / `stop` regardless of its other trigger declarations.

Inbox interest is declared per-agent:

```turtle
<#engineer>
  mind:interest [ mind:matches "mind:DraftApproval" ] ,
                [ mind:matches "mind:DeliveryNotice" ; mind:about </apps/codespaces/> ] .
```

---

## Change subscription

Both the operator and the runtime need to know when things change in the pod. Without an efficient change feed, every consumer falls back to polling, which is wasteful and laggy.

**Primary mechanism: [Solid Notifications Protocol](https://solid.github.io/notifications/protocol)** — WebSocket subscriptions on containers. Mind-compliant pod hosts SHOULD support it.

**Fallback: polling.** When the pod host doesn't support SNP, clients poll the relevant containers. Default cadence:

- `/agents/control/` — runtime polls every 5 seconds (operator responsiveness matters)
- `/agents/{id}/state.ttl`, `/agents/drafts/`, `/agents/audit/` — operator polls every 10 seconds
- `/inbox/` — runtime polls every 30 seconds
- Per-agent `hand.ttl` scope paths — runtime polls every 30 seconds

**Optimization: indexer as fanout.** When an indexer worker is present, both Compass and the runtime can subscribe to the indexer instead of the pod. The indexer holds a single SNP subscription (or polling loop) and broadcasts changes to N consumers. Optional, not required by the protocol.

### Subscription surfaces

| Subscriber | Container | Purpose |
|---|---|---|
| Runtime | `/agents/control/` | pick up operator commands |
| Runtime | `/inbox/` | inbox-trigger fan-in |
| Runtime | each agent's `hand.ttl` scope | pod-change-trigger fan-in |
| Operator (Compass) | `/agents/{id}/state.ttl` | live status |
| Operator (Compass) | `/agents/drafts/` | new drafts to review |
| Operator (Compass) | `/agents/audit/` | event timeline |

---

## Pluggable executors

An agent declares its **executor** in `roster.ttl`. The executor is the mechanism that runs one iteration of the agent — distinct from the agent's identity, role, and memory (all of which live in the pod and are runtime-agnostic).

```turtle
<#engineer>
  a              mind:Agent ;
  mind:executor  mind:PromptExecutor ;
  mind:executorConfig </agents/engineer/executor.ttl> .
```

### Executor classes in v0.1

<div class="diagram-block diagram-executors">
  <div class="executor-grid">
    <div class="executor-card">
      <div class="executor-iri">mind:PromptExecutor</div>
      <div class="executor-name">Prompt</div>
      <div class="executor-desc">System prompt + tool list, executed via an LLM client. The agent IS a prompt — runtime calls the LLM with it.</div>
      <div class="executor-config"><span class="key">CONFIG</span><span class="val"><code>executor.ttl</code> with <code>mind:systemPrompt</code>, <code>mind:tools</code>, <code>mind:model</code></span></div>
      <div class="executor-example">Best for: routine deciders (digest summarizer, calendar agent, Scribe)</div>
    </div>
    <div class="executor-card">
      <div class="executor-iri">mind:ModuleExecutor</div>
      <div class="executor-name">Module</div>
      <div class="executor-desc">JS/TS module loaded by the runtime; exports a <code>run()</code> function. The agent IS code, not a prompt.</div>
      <div class="executor-config"><span class="key">CONFIG</span><span class="val"><code>executor.ttl</code> with <code>mind:moduleSource</code> (URL or relative path)</span></div>
      <div class="executor-example">Best for: deterministic agents (filters, validators, schedulers)</div>
    </div>
    <div class="executor-card primary">
      <div class="executor-iri">mind:ExternalSessionExecutor</div>
      <div class="executor-name">External session</div>
      <div class="executor-desc">Runtime addresses an external process (e.g. a Claude Code session) over a wire protocol. The agent IS a session.</div>
      <div class="executor-config"><span class="key">CONFIG</span><span class="val"><code>executor.ttl</code> with <code>mind:sessionEndpoint</code>, <code>mind:sessionAuth</code></span></div>
      <div class="executor-example">Best for: full agents (Claude Code, OpenFang, anything with its own runtime)</div>
    </div>
  </div>
</div>

Runtimes are not required to support all three. A runtime that only supports `mind:PromptExecutor` MUST refuse roster entries declaring other executor classes (and write a `mind:status "errored"` with `mind:error "unsupported-executor"` to that agent's `state.ttl`).

Runtimes declare what they support in their own state file (path TBD, likely `/agents/runtime/capabilities.ttl`).

### Why this matters

This is the architectural move that makes "Claude Code session as an agent runtime subtype" precise. A Claude Code session is just an executor; the agent's identity, scope, memory, and audit trail all live in the pod and outlive any single session.

---

## Push notifications (optional)

When SNP is unavailable and polling latency is unacceptable, the runtime MAY also push notifications to the operator's `/inbox/` via §4 LDN:

- `mind:DraftCreated` — a new draft is in `/agents/drafts/`
- `mind:AgentStateChanged` — `state.ttl` transitioned (e.g. `working` → `waiting-approval`)
- `mind:AuditEntryWritten` — a significant audit event (drafts, command applications, errors)

This is a redundancy mechanism, not a replacement for the pod-based coordination. Operators can ignore it if they're already subscribed via SNP.

---

## Out of scope for v0.1

- **Multi-operator coordination.** §2 assumes a single operator at a time. If two Compass instances both issue `pause` to the same agent, both succeed (idempotent), but conflicting commands (e.g. simultaneous `approve` and `reject` on the same draft) are first-write-wins; the second fails with `mind:error "conflict"`.
- **Cross-pod agent delegation.** An operator on pod A controlling an agent in pod B isn't specified yet; cross-pod is §4's territory.
- **Runtime auto-discovery of executor implementations.** The runtime knows its capabilities at startup; dynamic executor loading is v0.2.

---

## Open questions

- **Indexer dependency.** If indexer-as-fanout is the practical answer for pods that don't speak SNP, should the indexer become a *required* worker in v0.2 rather than optional?
- **Command retention.** Is 30 days the right default for `/agents/control/` history, or should commands self-delete on `applied`?
- **Interest matching language.** The `mind:interest` predicate uses string matching (`mind:matches "mind:DraftApproval"`). Is that enough, or do we need a small filter DSL (regex, RDF queries)?
- **Executor capability discovery.** Where does the runtime publish what it supports — `/agents/runtime/capabilities.ttl`, or somewhere else that's read before the runtime processes the roster?
- **Audit + commands relationship.** Should every applied command also write an audit entry, or is the command record (with its `mind:appliedAt`) the audit?
