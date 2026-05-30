# Apps

The user-facing surfaces of Mind. Fifteen in the family today, framed by the Dock shell, plus an OS showcase at the end; the architecture lets anyone add more.

## What's a decentralized app?

A normal app — Gmail, Notion, Strava — stores *your* data in *its* database. You sign in to the app; the app shows you a view of its database; if it shuts down, your data goes with it.

A **decentralized app** doesn't have a database for your data. It reads and writes *your pod*. You sign in with your WebID; the app gets the access you grant it; if it shuts down, your data stays exactly where it was — in your pod, available to any other app that speaks the same protocol.

<div class="diagram-block diagram-app-shape">
  <div class="app-shape-row">
    <div class="app-shape-col">
      <div class="app-shape-tag">CENTRALIZED APP (TODAY)</div>
      <div class="app-shape-stack">
        <div class="app-shape-cell user">you</div>
        <div class="app-shape-arrow">↓</div>
        <div class="app-shape-cell app">App UI</div>
        <div class="app-shape-arrow">↓</div>
        <div class="app-shape-cell vendor">App's database</div>
      </div>
      <div class="app-shape-note">App owns the data. Switch apps → start over.</div>
    </div>
    <div class="app-shape-col highlight">
      <div class="app-shape-tag">DECENTRALIZED APP (MIND)</div>
      <div class="app-shape-stack">
        <div class="app-shape-cell user">you</div>
        <div class="app-shape-arrow">↓</div>
        <div class="app-shape-cell app">App UI</div>
        <div class="app-shape-arrow accent">↓ reads / writes</div>
        <div class="app-shape-cell pod">Your Pod · <code>/apps/{name}/</code></div>
      </div>
      <div class="app-shape-note">You own the data. Switch apps → same data, new view.</div>
    </div>
  </div>
</div>

### Three things every Mind app does

1. **Signs you in via your WebID.** No central account system. The app sends you to your pod's login page; you authenticate there; you come back signed in. (Details: [Solid-OIDC](https://solidproject.org/TR/oidc).)

2. **Reads and writes inside its own sandbox.** Each app gets a folder under `/apps/{appname}/` in your pod. Other apps can't peek inside that folder unless you grant access. (Layout spec: [Mind Protocol §1](protocol/01-pod-layout.md).)

3. **Reads shared data when relevant.** Top-level pod containers (`/calendar/`, `/contacts/`, `/inbox/`, `/photos/`) are shared — any app you trust can read them. That's how the same calendar entry shows up in your scheduling app, your assistant agent, and your mail app.

### Two flavors: domain surfaces and sandboxed apps

Most Mind apps own their data: Marketplace keeps listings in `/apps/marketplace/`, Social keeps posts in `/apps/social/`. A handful don't — they're *surfaces* over a shared **data domain** that lives at the top level of your pod, readable by every app you trust.

- **Sandboxed apps** keep their data in their own `/apps/{name}/` folder. Other apps can't read it without a grant.
- **Domain surfaces** read and write a shared top-level domain — `/calendar/`, `/contacts/`, `/tasks/` — and keep only their config in `/apps/{name}/`. The data outlives the surface: swap your Calendar app and the events stay put.

<div class="diagram-block diagram-app-shape">
  <div class="app-shape-row">
    <div class="app-shape-col">
      <div class="app-shape-tag">SANDBOXED APP</div>
      <div class="app-shape-stack">
        <div class="app-shape-cell app">Marketplace · Social · Health</div>
        <div class="app-shape-arrow">↓ owns</div>
        <div class="app-shape-cell vendor">Its sandbox · <code>/apps/{name}/</code></div>
      </div>
      <div class="app-shape-note">Data lives inside the app's own folder. No other app reads it without a grant.</div>
    </div>
    <div class="app-shape-col highlight">
      <div class="app-shape-tag">DOMAIN SURFACE</div>
      <div class="app-shape-stack">
        <div class="app-shape-cell app">Calendar · Contacts · Todo</div>
        <div class="app-shape-arrow accent">↓ reads / writes</div>
        <div class="app-shape-cell pod">Shared domain · <code>/calendar/</code> <code>/contacts/</code> <code>/tasks/</code></div>
      </div>
      <div class="app-shape-note">Data lives in a shared top-level domain. Every app you trust reads it.</div>
    </div>
  </div>
</div>

So when you ask *"is Calendar an app?"* — the **data** (`/calendar/`) is a domain, shared by everything. **Calendar**, **Contacts**, and **Todo** are the canonical surfaces over the three core domains, but they're not the only things that touch them: your agents, Flow, and Chat read the same calendar and contacts.

## The shell: Dock

<div class="diagram-block diagram-app-showcase">
  <div class="app-showcase-head">
    <div class="app-showcase-tag">THE SHELL</div>
    <div class="app-showcase-name">Dock</div>
  </div>
  <div class="app-showcase-body">Sign in once with your WebID and land here: every app you use, as a tile. Click to launch. The same grid rides along in every Mind app's navbar — the "waffle" you tap to hop between them without coming home.</div>
</div>

Dock is the front door. It isn't one of the apps in the grid below — it's the surface that *shows* them, the way a phone home screen or Google's app-grid shows yours. Two faces, one backing list:

- **The desktop** — a full home surface after sign-in: every app as a tile, recent activity, your pod identity front and center.
- **The waffle** — a compact app-grid embedded in every Mind app's navbar, so you can jump from Chat to Calendar to Todo without returning home.

How does Dock know which apps you have? It lists the `/apps/` zone of your pod — every app that has stored data there is "installed" — and joins that against a registry of known Mind apps (name → hosted URL → icon). Pin, reorder, and hide tiles; that layout is Dock's own state at `/apps/dock/`. No vendor decides your home screen — you do, and it travels with your pod.

Dock pairs with Drive the way a launcher pairs with a file manager: **Drive browses your data; Dock launches your apps.** Both are just lenses on the same pod.

**Related parts of Mind**

- Discovers apps by listing the `/apps/` zone from [§1 — Pod layout](protocol/01-pod-layout.md); its own layout at `/apps/dock/`
- Consumes the per-app manifests discussed in [§1 open questions](protocol/01-pod-layout.md#open-questions)
- Complements [Drive](#drive) (data) — Dock is the app side of the same idea
- Decisions: `apps/dock/0001` (two-session split), `apps/dock/0002` (named Dock, not Home) (in `decisions/`)

## The fifteen apps

<div class="diagram-block diagram-app-grid">
  <a class="app-card" href="#compass">
    <div class="app-card-letter">A</div>
    <div class="app-card-name">Compass</div>
    <div class="app-card-shape">DESKTOP · INSTALLED</div>
    <div class="app-card-tag">Operator UI for your worker fleet.</div>
  </a>
  <a class="app-card" href="#agents">
    <div class="app-card-letter">B</div>
    <div class="app-card-name">Agents</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">A team of specialists that lives in your pod.</div>
  </a>
  <a class="app-card" href="#drive">
    <div class="app-card-letter">C</div>
    <div class="app-card-name">Drive</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">File browser for your pod — upload, preview, share.</div>
  </a>
  <a class="app-card" href="#docs">
    <div class="app-card-letter">D</div>
    <div class="app-card-name">Docs</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">Notion-style pages and databases, written to your pod.</div>
  </a>
  <a class="app-card" href="#marketplace">
    <div class="app-card-letter">E</div>
    <div class="app-card-name">Marketplace</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">Pod-first listings — cash &amp; meet, no platform tax.</div>
  </a>
  <a class="app-card" href="#chat">
    <div class="app-card-letter">F</div>
    <div class="app-card-name">Chat</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">Pod-to-pod conversations, no central server.</div>
  </a>
  <a class="app-card" href="#social">
    <div class="app-card-letter">G</div>
    <div class="app-card-name">Social</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">Posts, friends, async game duels — your timeline, your rules.</div>
  </a>
  <a class="app-card" href="#codespaces">
    <div class="app-card-letter">H</div>
    <div class="app-card-name">Codespaces</div>
    <div class="app-card-shape">WEB + CLI</div>
    <div class="app-card-tag"><code>git push</code> your site into your pod.</div>
  </a>
  <a class="app-card" href="#health">
    <div class="app-card-letter">I</div>
    <div class="app-card-name">Health</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">Personal health records that don't leave your pod.</div>
  </a>
  <a class="app-card" href="#video">
    <div class="app-card-letter">J</div>
    <div class="app-card-name">Video</div>
    <div class="app-card-shape">WEB + LAN</div>
    <div class="app-card-tag">Drop phone shots, get a finished video — AI as the editor.</div>
  </a>
  <a class="app-card" href="#flow">
    <div class="app-card-letter">K</div>
    <div class="app-card-name">Flow</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">Work control plane — humans and agents on one board.</div>
  </a>
  <a class="app-card" href="#todo">
    <div class="app-card-letter">L</div>
    <div class="app-card-name">Todo</div>
    <div class="app-card-shape">WEB · DOMAIN SURFACE</div>
    <div class="app-card-tag">Shared task lists — hand a task to a friend or an agent, same grant.</div>
  </a>
  <a class="app-card" href="#calendar">
    <div class="app-card-letter">M</div>
    <div class="app-card-name">Calendar</div>
    <div class="app-card-shape">WEB · DOMAIN SURFACE</div>
    <div class="app-card-tag">A surface over your <code>/calendar/</code> — events every app can see.</div>
  </a>
  <a class="app-card" href="#contacts">
    <div class="app-card-letter">N</div>
    <div class="app-card-name">Contacts</div>
    <div class="app-card-shape">WEB · DOMAIN SURFACE</div>
    <div class="app-card-tag">One address book at <code>/contacts/</code>, read by every app.</div>
  </a>
  <a class="app-card" href="#builder">
    <div class="app-card-letter">O</div>
    <div class="app-card-name">Builder</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">Wish an app in chat — it gets built and published for you.</div>
  </a>
</div>

---

## Compass

<div class="diagram-block diagram-app-detail" id="compass-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">A</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Compass</div>
      <div class="app-detail-tag">Operator UI for your worker fleet.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">DESKTOP · INSTALLED</span>
      <span class="app-pill status status-building">BUILDING</span>
    </div>
  </div>
</div>

Compass is the cockpit. It shows you what your AI agents are doing, lets you intervene, and gives you a single timeline of everything that's happened across the fleet.

A typical session: open Compass, see your six agents listed; one of them — the Scribe — has a draft waiting for approval (a reply to an email it offered to send on your behalf). You read the draft, edit a line, hit approve. Compass writes the approval to `/agents/control/`; the agent picks it up; the email goes out. The audit log records both the draft and your approval, Merkle-chained for tamper-evidence.

**What it does**

- Lists the agent fleet from `/agents/roster.ttl` with live status
- Shows pending drafts in a review pane; approve / reject inline
- Streams the audit log in a chronological feed
- Writes operator commands (pause, resume, approve-draft, …) to `/agents/control/`
- Subscribes to pod changes for live updates (Solid Notifications when supported, polling fallback)

**Shape: installed, not web.** Compass lives on your machine because operating a worker fleet wants persistent OS-level capabilities — notifications, a system tray, the ability to run while the browser is closed. Local UI state (which agent's selected, sidebar widths, pending operator scratch) lives in the OS app data directory, not the pod. The real data — agent status, drafts, audit log — all comes from the pod.

**Why this matters**

Without Compass, the only thing that can see or move an agent is the runtime itself. With Compass, *any* tool that speaks the protocol can be the operator. The runtime is a vendor choice; Compass is a separate vendor choice; they don't share code — they share a pod schema.

**Related parts of Mind**

- Uses [§2 — Agent control + observation](protocol/02-agent-control.md) (the command/status protocol)
- Reads `/agents/` paths defined in [§1 — Pod layout](protocol/01-pod-layout.md)
- Pairs with **Agents** (next) — Compass is the operator dashboard; Agents is the team itself

---

## Agents

<div class="diagram-block diagram-app-detail" id="agents-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">B</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Agents</div>
      <div class="app-detail-tag">A team of specialists that lives in your pod.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill status status-building">BUILDING</span>
    </div>
  </div>
</div>

Agents is where you set up and work with your team of specialists — an Engineer, a Researcher, a Scribe, whatever roles you need. Connect your pod once; the team surveys what's there, proposes a roster, and starts working. Their memory, their decisions, what they've learned about you — all in your pod, at `/agents/`.

Compass is the *operator* view (fleet status, approvals, audit log). Agents is the *collaborator* view — where you actually configure roles and work with each agent day to day.

**What it does**

- Roster setup: pick roles, configure prompts, write the team to `/agents/roster.ttl`
- Day-to-day work: chat with an agent, hand it a task, see what each is producing
- Memory in your pod: each agent's learned context lives at `/agents/{role}/memory/`, portable across runtimes
- Deliveries: produced artifacts (drafts, research notes, code) flow into `/agents/{role}/deliveries/`

**Why this matters**

Today's AI assistants are vendor-locked: ChatGPT's memory lives with OpenAI, Claude's lives with Anthropic. If you switch, you start over. Agents flips that — the team's memory is *yours*, in your pod, and the runtime is replaceable.

**Related parts of Mind**

- Roster + control + memory paths from [§1 — Pod layout](protocol/01-pod-layout.md)
- Lifecycle and triggers: [§2 — Agent control + observation](protocol/02-agent-control.md)
- Companion app: [Compass](#compass) is the operator dashboard for a team you've set up here

---

## Drive

<div class="diagram-block diagram-app-detail" id="drive-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">C</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Drive</div>
      <div class="app-detail-tag">File browser for your pod — upload, preview, share.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill status status-building">BUILDING</span>
    </div>
  </div>
</div>

Drive is the file browser for your pod. Upload, share, preview — the basics of Google Drive or Dropbox, except the bytes live in your pod and sharing flows through WAC/ACP grants instead of a vendor's database. No central server ever sees plaintext.

**What it does**

- Drag-drop upload, download, folder create / rename / delete
- Inline preview for image, PDF, text, video, audio
- List / grid view, image thumbnails, filename search
- Share with a WebID (WAC grant), public link toggle, revoke at any time
- Auth state probed via the `WAC-Allow` header

**Shape: web.** Drive is a plain SPA against your pod. Bytes never transit a third-party.

**Why this matters**

A pod is fundamentally a file store with ACL. Drive is the surface that makes that legible to a non-technical user — and it does double duty as the place where every other Mind app's data is browseable on disk.

**Related parts of Mind**

- Files as LDP binary resources from [§1 — Pod layout](protocol/01-pod-layout.md)
- Sharing model: WAC / ACP grants — see §1 "Access control"
- Decision: `apps/drive/0001` — pod bytes never transit the app server (in `decisions/`)

---

## Docs

<div class="diagram-block diagram-app-detail" id="docs-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">D</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Docs</div>
      <div class="app-detail-tag">Notion-style pages and databases, written to your pod.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill status status-concept">CONCEPT</span>
    </div>
  </div>
</div>

Docs is the Notion-style block editor for your pod. Pages built from blocks, nested pages, databases-as-pages-with-schemas, page-link backlinks — written to your pod as RDF. The same WebID that signs into Marketplace, Chat, or Social opens its own workspace here.

**What it does (v0 scope)**

- Pages with nested blocks (paragraph, heading, list, code, callout, image)
- Linking between pages, with backlinks auto-resolved by an indexer worker
- Databases — pages-with-schemas (lightweight tables, kanban, gallery views)
- Selective sharing per page or subtree via WAC grants

**Honest limits.** Cross-pod search, real-time co-editing, and rollups across pods don't fit in v0. The proposal is explicit about what gets punted.

**Why this matters**

The Solid ecosystem has markdown notes apps and wiki experiments — but no serious Notion-style editor that writes to a pod. Docs targets that gap, and gives every other Mind app a place to send rich human-readable context (a project brief, a meeting note, a research dossier).

**Related parts of Mind**

- Pages, blocks, databases under `/apps/docs/` from [§1](protocol/01-pod-layout.md)
- Optional indexer for backlinks and search: see [Workers](architecture.html#workers)

---

## Marketplace

<div class="diagram-block diagram-app-detail" id="marketplace-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">E</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Marketplace</div>
      <div class="app-detail-tag">Pod-first listings — cash &amp; meet, no platform tax.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill status status-concept">CONCEPT</span>
    </div>
  </div>
</div>

Marketplace is local classifieds done right. Your listings live in *your* pod at `/apps/marketplace/listings/`. Other people see them when their Marketplace app browses your pod (or a federated feed). Counter-offers and messages travel pod-to-pod via [§4 LDN](protocol/04-ldn-inbox-outbox.md) — no central server in the middle, no platform charging a fee on every transaction.

You meet up in person, pay each other in cash, the transaction is between you. The app is just the way to find each other.

**What it does**

- Browses listings across pods (your friends', your Verein's, public feeds)
- Lets you create / edit / take down your own listings (`schema:Offer` shapes)
- Sends counter-offers and messages to other pods' `/inbox/`
- Surfaces interest from agents (e.g., Shopper agent flags listings matching your wishlist)

**Why this matters**

Today's listing apps (eBay Classifieds, Facebook Marketplace, etc.) own the listings and the relationships, take a cut, and shut you out if you misbehave. A pod-first marketplace shifts the power: you own your listings; you decide who sees them; the app is replaceable.

**Related parts of Mind**

- Listings: shapes likely under `schema:Offer` in [§1 — Pod layout](protocol/01-pod-layout.md)
- Messaging: [§4 — LDN inbox + outbox](protocol/04-ldn-inbox-outbox.md)

---

## Chat

<div class="diagram-block diagram-app-detail" id="chat-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">F</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Chat</div>
      <div class="app-detail-tag">Pod-to-pod conversations, no central server.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill status status-concept">CONCEPT</span>
    </div>
  </div>
</div>

Chat is messaging where each side stores its own copy of the conversation in its own pod. You write a message; Chat saves it to `/apps/chat/conversations/<id>` in *your* pod and POSTs an LDN notification to *their* pod's `/inbox/`. Their Chat app picks up the notification and threads the message into the same conversation on their side.

No central server. No "the app went down, where are my messages?" If your friend changes pod hosts, your conversation keeps working — only the URL of their inbox changes.

**What it does**

- 1:1 and group conversations across pods
- Messages saved on both sides (each in the sender's and recipient's pods)
- Read receipts as LDN messages (`mind:Received`)
- Optional E2E encryption (per-conversation keypair, stored in pod)

**Why this matters**

Today's messaging apps (WhatsApp, Telegram, Discord) put themselves between every two people who want to talk. A pod-first chat puts the medium back in our hands — and makes it trivial for assistant agents to read and react to ongoing conversations on your behalf if you opt in.

**Related parts of Mind**

- Conversation storage: `/apps/chat/conversations/` from [§1](protocol/01-pod-layout.md)
- Pod-to-pod delivery: [§4 LDN](protocol/04-ldn-inbox-outbox.md)

---

## Social

<div class="diagram-block diagram-app-detail" id="social-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">G</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Social</div>
      <div class="app-detail-tag">Posts, friends, async game duels — your timeline, your rules.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill status status-concept">CONCEPT</span>
    </div>
  </div>
</div>

Social is the playful one — short posts, friend graphs, mentions, and async games (chess duels, daily puzzles, etc.) that travel between pods as LDN messages. Posts live in your pod at `/apps/social/posts/` as ActivityStreams 2 (`as:Note`) resources; friends are `as:Follow` references; mentions land in others' `/inbox/`.

No algorithm picking what you see. No engagement optimization. Your feed is your friends' pods, polled by an indexer worker, ordered the way you want.

**What it does**

- Compose posts (`as:Note`) saved to `/apps/social/posts/`
- Friend graph as `as:Follow` references in `/apps/social/friends/`
- Mentions sent as LDN messages to recipients' `/inbox/`
- Async game state in `/apps/social/duels/{game-id}/` (chess, go, daily Wordle-likes)
- Federated feed via indexer (subscribe to friends' pods, present chronologically)

**Why this matters**

Today's social platforms run on engagement metrics that benefit them, not you. A pod-first social app makes the relationships and posts *yours* — and makes the indexer (the thing that picks what you see) a replaceable component. Don't like your indexer's ranking? Swap it.

**Related parts of Mind**

- Posts, friends, duels storage from [§1 Pod layout](protocol/01-pod-layout.md)
- Mentions delivery: [§4 LDN](protocol/04-ldn-inbox-outbox.md)
- Federated feed: indexer worker, see [Workers](architecture.html#workers)
- Decision: `apps/social/0001` — no central database (in `decisions/`)

---

## Codespaces

<div class="diagram-block diagram-app-detail" id="codespaces-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">H</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Codespaces</div>
      <div class="app-detail-tag"><code>git push</code> your site into your pod.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB + CLI</span>
      <span class="app-pill status status-building">BUILDING</span>
    </div>
  </div>
</div>

Codespaces lets you treat your pod as a git remote *and* as a hosting target. You `git push` your static site (or web app) into your pod; the **Pages** layer serves it back out at a public URL under your pod host.

The CLI handles the push side. The web app is the dashboard — list your repos and sites, see deployment status, manage published versions, configure custom domains.

**What it does**

- `codespaces` CLI: `git push` to `https://your-pod.example/apps/codespaces/repos/{owner}/{name}.git`
- Server-side bridge worker accepts the push, stores bare refs + metadata
- **Mind Pages** publishes selected branches as world-readable sites
- Web app for browsing repos, sites, and publishing config

**Shape: web + CLI.** The web app handles the day-to-day clicking. The CLI handles the part that lives in your terminal — `git push`, `git fetch`, `git clone`. The CLI is the example of "an installed Mind app that's not Compass" — installed because git only knows how to talk to local programs.

**Why this matters**

Today, publishing a personal site means picking a platform (GitHub Pages, Netlify, Vercel) and letting it own the content. Codespaces flips it: your content lives in your pod, and the publishing layer is replaceable. Take your pod elsewhere → your sites come too.

**Related parts of Mind**

- Repo storage: `/apps/codespaces/repos/{owner}/{name}/` from [§1](protocol/01-pod-layout.md)
- Public sites: `/apps/codespaces/public-sites/{name}/` (world-readable)
- Bridge worker: see [Workers](architecture.html#workers) in the architecture overview
- Companion: an in-browser IDE prototype (`mind-codespaces-ide-v0`) clones, edits, commits, and pushes entirely client-side — same pod data, no IDE backend
- Decision: `apps/codespaces/0001` — pod publishes static sites; the bridge is glue (in `decisions/`)

---

## Health

<div class="diagram-block diagram-app-detail" id="health-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">I</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Health</div>
      <div class="app-detail-tag">Personal health records that don't leave your pod.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill status status-concept">CONCEPT</span>
    </div>
  </div>
</div>

Health is a private record-keeping app for medical visits, prescriptions, allergies, lab results, and notes. Everything lives in your pod at `/apps/health/records/`. The data never sits on a third-party health platform.

When you visit a new doctor, you can grant them read access to a specific subset (`/apps/health/records/2026/`) for a limited time — they get what they need, you keep ownership, the grant auto-expires.

**What it does**

- Stores health records (visits, prescriptions, lab results, allergies, conditions)
- Time-boxed sharing with care providers via ACL grants
- Optional import from existing health data exports (FHIR, Apple Health export, etc.)
- Optional connection to a Health-related agent (e.g., "remind me to refill my prescription on the 15th")

**Why this matters**

Health data is among the most personal and most leaky data we generate. Today it's scattered across hospital portals, insurance apps, and tracker companies. A pod-first health app keeps it together in one place you own, and shares only what you choose, when you choose.

**Related parts of Mind**

- Per-app sandbox: `/apps/health/` from [§1](protocol/01-pod-layout.md)
- Optional agent integration: [§2](protocol/02-agent-control.md)

---

## Video

<div class="diagram-block diagram-app-detail" id="video-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">J</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Video</div>
      <div class="app-detail-tag">Drop phone shots, get a finished video — AI as the editor.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB + LAN</span>
      <span class="app-pill status status-concept">CONCEPT</span>
    </div>
  </div>
</div>

Video is the personal film studio. You drop a handful of photos and clips from your phone onto a tab on your laptop; the app auto-captions each asset; you type something like *"make a video about apple trees today"*; an AI agent picks the best 4–12 assets, composes them with transitions and overlays, renders the result, and streams it back to your phone.

The early prototype (`mind-video` / drop-cut) runs **local-only on the Mac** with files on disk. The Mind-protocol version makes one change: those files become pod resources. Captured clips land in `/photos/` (the shared container the pod already has); projects live in `/apps/video/projects/{name}/` with the timeline and render settings; the AI agent is one of your **Agents** roles, following [§2 — Agent control](protocol/02-agent-control.md) so you can approve a render and see what got picked.

**What it does**

- Drop ingestion: drag photos / videos from a phone over LAN; assets get auto-captioned + tagged
- Library browse: scroll the captioned library, search by tag, scrub clips
- Compose by prompt: "make a video about X" — the editor agent picks assets, builds a timeline, renders
- Renders + final cuts saved to `/apps/video/projects/{name}/renders/`
- Phone-side viewing: open a link, watch / share the final cut

**Shape: web + LAN.** The web app runs on your laptop; your phone is the camera and the screen. No cloud upload, no third-party transcoding.

**Why this matters**

Today, "AI video editor" means uploading your footage to a vendor's GPUs and trusting them with your private clips. Video keeps the footage in your pod and the editor on your hardware — and because the editor is just an Agents role, you can swap it for a different model or a different studio without losing your library.

**Related parts of Mind**

- Captured clips in the shared container `/photos/` from [§1 — Pod layout](protocol/01-pod-layout.md)
- Project / render storage under `/apps/video/projects/`
- AI editor as an Agents role, controlled via [§2](protocol/02-agent-control.md)
- Renders served via the pod's static-files surface, like Codespaces' Mind Pages

---

## Flow

<div class="diagram-block diagram-app-detail" id="flow-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">K</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Flow</div>
      <div class="app-detail-tag">Work control plane — humans and agents on one board.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill status status-concept">CONCEPT</span>
    </div>
  </div>
</div>

Flow is the control plane for everything you're working on, with AI agents as first-class teammates. It reads work items from your other Mind apps — Todo lists, Codespaces issues, Docs todos, Agents deliveries — and lets you plan them into sprints, assign to humans or agents, and track through to done.

The novel angle: agents and humans coexist in the same backlog. An agent picks up a mission, posts status into it like a teammate, ships a delivery. You see the same board they do.

**What it does**

- Unified inbox indexing work items across Codespaces, Docs, Agents — without owning them
- **Missions**: spec + owner + status + due date + parent (sprint / project)
- Assign to a human (WebID) or an agent (Agents-role reference)
- Sprints, board, and timeline — agents and humans on the same view
- Source of truth stays with the originating app; Flow is a view, not a copy

**Why this matters**

Today's PM tools with agent features (Linear Agent, Notion External Agents, Devin, Cursor background agents) all put agents *inside one product*. None can see across the products you actually use, keep agent history with *you* instead of the vendor, or scope agent permissions per-resource. The Solid + agentic combination unlocks all four.

**Related parts of Mind**

- Reads from `/tasks/` (shared), `/apps/codespaces/`, `/apps/docs/`, `/agents/{role}/deliveries/`
- Writes mission and sprint data under `/apps/flow/` from [§1](protocol/01-pod-layout.md)
- Runtime collaborator: [§2 — Agent control](protocol/02-agent-control.md)

---

## Todo

<div class="diagram-block diagram-app-detail" id="todo-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">L</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Todo</div>
      <div class="app-detail-tag">Shared task lists — hand a task to a friend or an agent, same grant.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill shape">DOMAIN SURFACE</span>
      <span class="app-pill status status-building">BUILDING</span>
    </div>
  </div>
</div>

Todo is the "hello world" of decentralized apps — a Wunderlist-style task list, and the surface over the shared **`/tasks/`** domain. Your lists live at the top level of your pod, not in an app sandbox, so the same list Todo shows is the one [Flow](#flow) plans into a sprint and your agent works through. The interesting part isn't the checkboxes; it's what *sharing* means here. Granting a friend access to a list and assigning a task to an AI agent are **the same operation** — a WAC grant to a WebID. In a pod an agent is just another WebID, so "share" and "delegate" collapse into one thing.

And tasks aren't strings — they're linked data. Each task is an `ical:Vtodo` (the W3C to-do standard) inside a `schema:ItemList`, and a task can point (`schema:about`) at a file in Drive, a repo in Codespaces, or a contact's WebID. Any Mind app can follow those links.

**What it does**

- Multiple lists, each **one** Turtle document at `/tasks/{id}` (the list plus all its tasks in a single resource)
- Share a whole list with a named WebID — person or agent — with one grant that covers every task, including ones added later
- Cross-app task links via `schema:about` (a task that references a Drive file or a Codespaces repo)
- Hand a task to an agent; its output lands as a draft in `/apps/todo/artifacts/` for you to review
- Discovery is pure pod container listing — no database, no indexer, no central task store

**Shape: web, domain surface.** A plain SPA against your pod. The early prototype (`mind-todo-v0`) stored lists in its own `/apps/todo/` sandbox; the protocol model promotes them to the shared `/tasks/` domain so Flow and your agents read them as ordinary shared user-data — no cross-app grant needed. Todo keeps only its config, share-pointers, and agent artifacts under `/apps/todo/`.

**One-doc-per-list, on purpose.** A WAC grant on a container doesn't automatically reach the resources inside it, so splitting tasks into separate files would turn "share a list" into N grants that miss every newly-added task. Keeping a list as one document means a single grant covers the list and all its tasks — now and later.

**Why this matters**

A to-do app is the smallest thing that exercises the *whole* protocol: a shared data domain, named-WebID sharing, agent delegation, and cross-app linked data. If the boring app works cleanly, the protocol is sound. And the payoff is real — "assign to a person" and "assign to an AI" stop being two different features.

**Related parts of Mind**

- Shared `/tasks/` domain from [§1 — Pod layout](protocol/01-pod-layout.md) — Todo is its surface
- Sharing model: WAC grants to a WebID — see §1 "Access control"; resolved to humans via [Contacts](#contacts)
- Agent delegation as an Agents role, controlled via [§2 — Agent control](protocol/02-agent-control.md)
- Cross-app links into [Drive](#drive) and [Codespaces](#codespaces)
- Aggregated alongside other work items by [Flow](#flow), which reads `/tasks/` directly
- Decision: `apps/todo/0001` — one list = one Turtle document (in `decisions/`)

---

## Calendar

<div class="diagram-block diagram-app-detail" id="calendar-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">M</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Calendar</div>
      <div class="app-detail-tag">A surface over your <code>/calendar/</code> — events every app can see.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill shape">DOMAIN SURFACE</span>
      <span class="app-pill status status-concept">CONCEPT</span>
    </div>
  </div>
</div>

Calendar is the canonical surface for the shared `/calendar/` domain. It reads and writes `ical:Vevent` resources at the top level of your pod — *not* inside an app sandbox — so the same event Calendar shows is the one your assistant agent reschedules and your Chat app links to. Calendar's own private state (which overlay calendars are toggled on, default view, colors) lives at `/apps/calendar/`; the events themselves stay shared at `/calendar/`.

**What it does**

- Read / write events as `ical:Vevent` in the shared `/calendar/` domain
- Multiple overlay calendars (work, personal, a shared Verein calendar) with per-calendar ACLs
- Invites travel pod-to-pod via [§4 LDN](protocol/04-ldn-inbox-outbox.md) to another pod's `/inbox/`; RSVPs come back the same way
- Agent-friendly: a scheduling agent reads `/calendar/` and proposes new events as drafts

**Why this matters**

Today your calendar is Google's or Apple's, and every app that wants your schedule re-implements an integration against their API. Mind makes the calendar a *domain* you own; Calendar is just one — replaceable — view of it, and every other app reads the same events for free.

**Related parts of Mind**

- Shared `/calendar/` domain from [§1 — Pod layout](protocol/01-pod-layout.md) — Calendar is its surface
- Invites and RSVPs: [§4 — LDN inbox + outbox](protocol/04-ldn-inbox-outbox.md)
- Attendees resolved via [Contacts](#contacts); optional scheduling agent via [§2](protocol/02-agent-control.md)

---

## Contacts

<div class="diagram-block diagram-app-detail" id="contacts-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">N</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Contacts</div>
      <div class="app-detail-tag">One address book at <code>/contacts/</code>, read by every app.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill shape">DOMAIN SURFACE</span>
      <span class="app-pill status status-concept">CONCEPT</span>
    </div>
  </div>
</div>

Contacts is the surface for the shared `/contacts/` domain — `vcard:Individual` records at the top level of your pod. Because contacts are shared data, the WebID you message in Chat, the seller you meet in Marketplace, and the person you assign a Todo to are all the *same* contact record, not three copies. Contacts' private state (groups, favorites, display prefs) lives at `/apps/contacts/`; the records stay shared at `/contacts/`.

**What it does**

- Read / write contacts as `vcard:Individual` in the shared `/contacts/` domain
- Link each contact to their WebID, so sharing and messaging resolve to a real pod
- Groups and tags; selective sharing of a group with another pod
- Agent-friendly: agents resolve "email Bob" to Bob's WebID via `/contacts/`

**Why this matters**

Every app today rebuilds its own contact list. A shared contacts domain means one address book, owned by you, read by all your apps — and it's the thing that makes named-WebID sharing (in [Todo](#todo), [Drive](#drive), [Health](#health)) usable by humans instead of raw URLs.

**Related parts of Mind**

- Shared `/contacts/` domain from [§1 — Pod layout](protocol/01-pod-layout.md) — Contacts is its surface
- Underpins named-WebID sharing across [Todo](#todo), [Drive](#drive), [Health](#health), [Calendar](#calendar)
- WebIDs as the identity primitive: see the architecture overview

---

## Builder

<div class="diagram-block diagram-app-detail" id="builder-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">O</div>
    <div class="app-detail-titles">
      <div class="app-detail-name">Builder</div>
      <div class="app-detail-tag">Wish an app in chat — it gets built and published for you.</div>
    </div>
    <div class="app-detail-pills">
      <span class="app-pill shape">WEB</span>
      <span class="app-pill status status-building">BUILDING</span>
    </div>
  </div>
</div>

Builder is the "wish an app" surface. You describe what you want in plain chat — *"a landing page for my honey from my bees"* — and a coding agent builds it, publishes it, and drops a live preview link back into the conversation. No setup, no code, no jargon.

Builder doesn't build anything itself — it **orchestrates [Codespaces](#codespaces)**, which already has the whole engine: repo creation, the coding agent, the build runner, and Pages publishing. Builder owns the chat, the project model, and the conversation — all saved to your pod; Codespaces (and your pod) stay the source of truth for the repo, the build, and the published site.

**What it does**

- Turns a chat wish into a running app — Builder scaffolds the project and hands the wish to the coding agent
- Posts a live preview link into the chat once the build publishes to your pod
- Iterate by chatting follow-ups; the agent resumes the work and republishes
- Conversation + project record saved to your pod at `/apps/builder/projects/{slug}/` (SolidOS long-chat layout)

**Shape: web, orchestrator.** Builder is a thin chat front-end over the Codespaces bridge — it never reimplements git, the coder, the runner, or the publisher. Its local sqlite store is a convenience mirror of pod data, never the source of truth.

**Why this matters**

Today's "wish an app" tools (lovable.dev, v0, …) host your app and own the code on their platform. Builder publishes into *your* pod through Codespaces — you own the repo, the build, and the live site, and the builder itself is replaceable.

**Related parts of Mind**

- Orchestrates [Codespaces](#codespaces) — the build + publish engine (Builder adds none of its own)
- Conversations use the SolidOS long-chat layout, shared with [Chat](#chat)
- The coding agent follows [§2 — Agent control](protocol/02-agent-control.md)
- Decision: `apps/builder/0001` — thin orchestrator over the bridge (in `decisions/`)

---

## And one wild showcase: OS

<div class="diagram-block diagram-app-showcase">
  <div class="app-showcase-head">
    <div class="app-showcase-tag">SHOWCASE</div>
    <div class="app-showcase-name">OS</div>
  </div>
  <div class="app-showcase-body">An unmodified Debian VM in a browser tab, with your pod as the disk. Less a daily-driver app, more a demonstration of how far the pod-as-storage idea stretches.</div>
</div>

`mind-os-v0` boots a real Debian via [CheerpX](https://cheerpx.io) / [WebVM](https://github.com/leaningtech/webvm) inside the browser. A real terminal, real `apt`, real `cat` / `grep` / `vim` — with the home directory backed by your Solid pod. The OS is disposable; your data stays yours.

It's not in the fourteen apps because it isn't a daily-driver surface. It's here because it answers a useful question: *what's the upper limit of what "your pod is your storage" can mean?* The answer turns out to be "the whole filesystem of a Linux box you happen to be using".

---

## Build your own

The protocol is open. There's no central app store, no platform approval, no business deal to negotiate with anyone. To add a new app to your pod:

1. Pick a folder name. Yours will live under `/apps/{name}/`.
2. Speak [Solid-OIDC](https://solidproject.org/TR/oidc) for sign-in. Standard library exists in most languages.
3. Read and write paths under `/apps/{name}/` (your sandbox). Read shared containers (`/calendar/`, `/contacts/`, `/inbox/`) when relevant.
4. If your app sends messages to other pods, use [§4 LDN](protocol/04-ldn-inbox-outbox.md).
5. If your app wants to operate AI agents on the user's behalf, follow [§2](protocol/02-agent-control.md).

That's it. Ship.

If your app turns into a thing other people would use, name it with a capital letter (the [Mind naming convention](architecture.html#naming-convention)), publish a page like this one, and you're a citizen of the Mind family.
