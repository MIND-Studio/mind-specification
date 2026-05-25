# Workers

The background processes that operate on your pod under your authentication. They keep working when you're not at the keyboard. Three types in the architecture today; the protocol lets anyone add more.

## What's a worker?

A **worker** is a long-running process that reads and writes your pod on your behalf. It holds its own credentials (granted by you once, scoped to specific paths), runs continuously in the background, and has no UI. Workers do the operational work — caching, syncing, translating, deciding — that you don't want to babysit.

The difference from an app:

<div class="diagram-block diagram-app-shape">
  <div class="app-shape-row">
    <div class="app-shape-col">
      <div class="app-shape-tag">APP</div>
      <div class="app-shape-stack">
        <div class="app-shape-cell user">runs when you click</div>
        <div class="app-shape-arrow">↓</div>
        <div class="app-shape-cell app">uses your session</div>
        <div class="app-shape-arrow">↓</div>
        <div class="app-shape-cell vendor">stops when you close it</div>
      </div>
      <div class="app-shape-note">UI-first · foreground · per-session credentials</div>
    </div>
    <div class="app-shape-col highlight">
      <div class="app-shape-tag">WORKER</div>
      <div class="app-shape-stack">
        <div class="app-shape-cell user">runs continuously</div>
        <div class="app-shape-arrow accent">↓ holds scoped credentials</div>
        <div class="app-shape-cell app">acts within its <code>hand.ttl</code> scope</div>
        <div class="app-shape-arrow accent">↓</div>
        <div class="app-shape-cell pod">keeps working when you're away</div>
      </div>
      <div class="app-shape-note">No UI · background · own WebID</div>
    </div>
  </div>
</div>

Both speak the same Mind protocol. Both read and write your pod. The difference is **temporality** (foreground vs background) and **autonomy** (your session vs its own credentials).

## How a worker uses your pod

You grant a worker scoped access via its `hand.ttl` declaration — a small RDF file that says *"this worker can read these paths, write those paths, with these caveats."* Once granted, the worker authenticates as itself (its own WebID, not yours) and acts within that scope.

If you ever want to take a worker offline or rotate its credentials, you revoke the ACL grant in your pod. The worker can no longer act outside the new (or empty) scope. No code change, no contacting the vendor, no waiting for a graceful shutdown.

Workers are designed to be **replaceable**. Today's TypeScript-native agent runtime can be swapped for a Python-native one — your data, including everything the agents have learned about you, stays in your pod. (See the [Why this shape](architecture.md#why-this-shape) principles for why.)

## The three worker types

<div class="diagram-block diagram-app-grid">
  <a class="app-card" href="#indexers">
    <div class="app-card-letter">A</div>
    <div class="app-card-name">Indexers</div>
    <div class="app-card-shape">CACHE LAYER</div>
    <div class="app-card-tag">Pre-computed views over your pod so reads are fast.</div>
  </a>
  <a class="app-card" href="#bridges">
    <div class="app-card-letter">B</div>
    <div class="app-card-name">Bridges</div>
    <div class="app-card-shape">PROTOCOL TRANSLATOR</div>
    <div class="app-card-tag">Speak <code>git</code>, IMAP, CalDAV, … on one side; pod on the other.</div>
  </a>
  <a class="app-card" href="#agent-runtimes">
    <div class="app-card-letter">C</div>
    <div class="app-card-name">Agent runtimes</div>
    <div class="app-card-shape">AGENT HOST</div>
    <div class="app-card-tag">Run cognitive workers (LLM-backed agents) that act on your behalf.</div>
  </a>
</div>

---

## Indexers

<div class="diagram-block diagram-app-detail" id="indexers-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">A</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Indexers</div>
      <div class="app-detail-tag">Make reads fast.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">BACKGROUND · CACHE</span>
      <span class="app-pill status status-building">BUILDING</span>
    </div>
  </div>
</div>

A Solid pod is great at storing your data but slow at answering questions like *"give me every contact tagged 'family' modified in the last 30 days"* or *"every post my friends made this week, in chronological order."* Without help, each query has to walk every file in the relevant container.

An **indexer** is the missing database layer. It subscribes to pod changes, builds derived views (think SQL tables, search indexes, vector embeddings), and exposes a fast query API to apps. When the underlying pod data changes, the indexer updates its views; apps subscribe to indexer updates rather than polling the pod directly.

**What it does**

- Subscribes to pod containers via the Solid Notifications Protocol (polling fallback when not supported)
- Maintains derived views in its own storage (SQLite, Postgres, a vector store — implementation choice)
- Exposes a query API to apps: filters, sorts, full-text search, vector similarity
- Acts as a **fanout point** for change subscriptions — one subscription to the pod, N consumers reading from the indexer (see [§2](protocol/02-agent-control.md) for how Compass and the agent runtime can both rely on this)

**Why it matters**

Without an indexer, every app that wants "all my notes tagged X" has to walk the pod itself. Apps would be slow, the pod would be hammered, and federated views (your social feed across many friends' pods) would be infeasible. The indexer makes the pod-as-canonical-store practical at scale.

**Replaceable**

Your indexer is a vendor choice, not a lock-in. Today it might be a Node.js process running a SQLite store; tomorrow it could be PostgreSQL, Solr, Pinecone, or a custom Rust binary. Swap it out — the apps don't care, because they speak a small query API rather than the indexer's internals. The indexer can be rebuilt from the pod at any time (it holds no canonical state).

**Related parts of Mind**

- Paths in [§1 — Pod layout](protocol/01-pod-layout.md)
- Change subscription mechanics in [§2 — Agent control + observation](protocol/02-agent-control.md)
- Used by federated views in [Social](apps.md#social), search in [Marketplace](apps.md#marketplace), the live audit timeline in [Compass](apps.md#compass)

---

## Bridges

<div class="diagram-block diagram-app-detail" id="bridges-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">B</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Bridges</div>
      <div class="app-detail-tag">Translate other protocols to and from your pod.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">BACKGROUND · TRANSLATOR</span>
      <span class="app-pill status status-building">BUILDING</span>
    </div>
  </div>
</div>

The world is full of protocols that don't speak Solid — `git`, IMAP/SMTP, CalDAV, browser downloads, FTP, S3 buckets, your phone's photo roll. You don't want to abandon those systems; you want their data to land in your pod where everything else lives.

A **bridge** is a daemon that speaks the foreign protocol on one side and writes pod-shaped data on the other. Your existing tools (git client, mail client, calendar app) talk to the bridge as if it were a normal server; the bridge translates and lands the data in your pod.

**Examples**

- **Git ↔ pod** — `git push` to `https://your-pod/apps/codespaces/repos/{name}.git`. The bridge accepts standard git pack protocol; stores refs and packed objects under `/apps/codespaces/repos/{name}/`. Powers [Codespaces](apps.md#codespaces).
- **IMAP/SMTP ↔ pod** — your existing mail client reads/writes against the bridge as a normal mail server; the bridge mirrors messages into `/apps/mail/messages/` as Turtle resources. (Conceptual; not yet built.)
- **CalDAV ↔ pod** — your phone's built-in calendar syncs to the bridge; the bridge keeps `/calendar/` and the CalDAV view in sync. (Conceptual.)
- **Browser downloads → pod** — every file you download lands in `/downloads/` automatically. (Conceptual.)

**Why it matters**

Bridges make migration painless. You don't have to abandon mature tools; you just point them at your pod through a translator. Over time, native Mind apps replace the bridged tools, but until then the bridge keeps your pod populated.

**Stateless and replaceable**

A well-built bridge holds no canonical state — it's a pure translator. If the bridge process dies, you restart it; nothing is lost because the canonical data is in your pod (or in the foreign system, which the bridge re-mirrors on next run).

**Related parts of Mind**

- Whatever the source protocol is (git, IMAP, CalDAV, …) — bridges are inherently per-protocol
- Pod paths in [§1](protocol/01-pod-layout.md)
- The Codespaces bridge specifically: see [Codespaces](apps.md#codespaces)

---

## Agent runtimes

<div class="diagram-block diagram-app-detail" id="agent-runtimes-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">C</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Agent runtimes</div>
      <div class="app-detail-tag">Host cognitive workers that act on your behalf.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">BACKGROUND · AGENT HOST</span>
      <span class="app-pill status status-building">BUILDING</span>
    </div>
  </div>
</div>

An **agent runtime** hosts a fleet of AI agents — small autonomous workers each with a role (Engineer, Researcher, Scribe, Shopper, …), a scope, a memory, and a behavior. Each agent runs on schedules, reacts to changes in its scope, processes inbox messages, and produces drafts that you approve before they go out into the world.

The runtime is the most architecturally significant worker — it's the only autonomous category. Indexers cache, bridges translate; agent runtimes **decide**.

**What it does**

- Loads agent declarations from `/agents/roster.ttl` (each agent has an id, role, scope, executor, triggers)
- Runs each agent on its declared triggers — schedule, pod-change-in-scope, new inbox message, operator command
- Maintains per-agent memory (transcripts, embeddings) under `/agents/{id}/memory/`
- Produces drafts to `/agents/drafts/` — never going outward without operator approval
- Writes append-only Merkle-chained audit entries to `/agents/audit/`
- Calls external services declared in [§3](protocol/03-services-manifest.md) (LLM hosts, transcription, OCR, …)
- Watches `/agents/control/` for operator commands (pause, resume, approve-draft, reject-draft, tick) from Compass

**Pluggable executors**

Each agent declares its **executor** in `roster.ttl` — the mechanism that runs one iteration. Three executor types in v0.1:

- `mind:PromptExecutor` — system prompt + tool list, executed via an LLM client
- `mind:ModuleExecutor` — a JS/TS module loaded by the runtime; exports `run()`
- `mind:ExternalSessionExecutor` — runtime addresses an external process (e.g. a Claude Code session) over a wire protocol

This is the architectural move that makes *"Claude Code session as an agent runtime subtype"* precise. A Claude Code session is just an executor; the agent's identity, scope, memory, and audit trail all live in the pod and outlive any single session.

**Why it matters**

AI agents are useful when they have persistence (they remember last week), accountability (you can see what they did and why), and replaceability (the runtime is a vendor choice, not a forever commitment). Today's runtimes are silos — every vendor wants to own the agent identity, memory, and execution. Mind flips this: identity, memory, audit live in your pod; the runtime is just an executor host.

**Related parts of Mind**

- Full spec: [§2 — Agent control + observation](protocol/02-agent-control.md)
- Paths: [§1 — Pod layout](protocol/01-pod-layout.md)
- External services the agents call: [§3 — Services manifest](protocol/03-services-manifest.md)
- Cross-pod messages from agents: [§4 — LDN inbox + outbox](protocol/04-ldn-inbox-outbox.md)
- Operated by [Compass](apps.md#compass)

---

## Build your own worker

The protocol is open. To add a new worker type:

1. **Write a process** that authenticates against your pod with its own WebID (not yours).
2. **Declare its scope** in a `hand.ttl` file. Be specific — least privilege. The pod's ACLs enforce it.
3. **Have the user grant the scope** in their pod (one-time setup, usually via a UI in Compass or directly editing ACLs).
4. **Speak the Mind protocol** for whatever it does:
   - Paths and shapes: [§1 Pod layout](protocol/01-pod-layout.md)
   - If your worker is agent-runtime-like: [§2 Agent control](protocol/02-agent-control.md)
   - If your worker calls external services: [§3 Services manifest](protocol/03-services-manifest.md)
   - If your worker sends or receives cross-pod messages: [§4 LDN inbox + outbox](protocol/04-ldn-inbox-outbox.md)

That's it. A worker is just a process with credentials. The interesting design decisions are **scope** (least privilege, expressed in `hand.ttl`) and **replaceability** (does the worker hold any canonical state outside the pod? if yes, can it rebuild that state from the pod?).
