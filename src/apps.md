# Apps

The user-facing surfaces of Mind. Six in the family today; the architecture lets anyone add more.

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

## The six apps

<div class="diagram-block diagram-app-grid">
  <a class="app-card" href="#compass">
    <div class="app-card-letter">A</div>
    <div class="app-card-name">Compass</div>
    <div class="app-card-shape">DESKTOP · INSTALLED</div>
    <div class="app-card-tag">Operator UI for your worker fleet.</div>
  </a>
  <a class="app-card" href="#marketplace">
    <div class="app-card-letter">B</div>
    <div class="app-card-name">Marketplace</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">Pod-first listings — cash &amp; meet, no platform tax.</div>
  </a>
  <a class="app-card" href="#health">
    <div class="app-card-letter">C</div>
    <div class="app-card-name">Health</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">Personal health records that don't leave your pod.</div>
  </a>
  <a class="app-card" href="#chat">
    <div class="app-card-letter">D</div>
    <div class="app-card-name">Chat</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">Pod-to-pod conversations, no central server.</div>
  </a>
  <a class="app-card" href="#codespaces">
    <div class="app-card-letter">E</div>
    <div class="app-card-name">Codespaces</div>
    <div class="app-card-shape">WEB + CLI</div>
    <div class="app-card-tag"><code>git push</code> your site into your pod.</div>
  </a>
  <a class="app-card" href="#social">
    <div class="app-card-letter">F</div>
    <div class="app-card-name">Social</div>
    <div class="app-card-shape">WEB</div>
    <div class="app-card-tag">Posts, friends, async game duels — your timeline, your rules.</div>
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

**Shape: installed, not web.** Compass lives on your machine because operating a worker fleet wants persistent OS-level capabilities — notifications, a system tray, the ability to run while the browser is closed. Local UI state (which agent's selected, sidebar widths, pending operator scratch) lives in the OS app data directory, not the pod. The canonical data — agent status, drafts, audit log — all comes from the pod.

**Why this matters**

Without Compass, the only thing that can see or move an agent is the runtime itself. With Compass, *any* tool that speaks the protocol can be the operator. The runtime is a vendor choice; Compass is a separate vendor choice; they don't share code — they share a pod schema.

**Related parts of Mind**

- Uses [§2 — Agent control + observation](protocol/02-agent-control.md) (the command/status protocol)
- Reads `/agents/` paths defined in [§1 — Pod layout](protocol/01-pod-layout.md)

---

## Marketplace

<div class="diagram-block diagram-app-detail" id="marketplace-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">B</div>
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

## Health

<div class="diagram-block diagram-app-detail" id="health-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">C</div>
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

## Chat

<div class="diagram-block diagram-app-detail" id="chat-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">D</div>
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

## Codespaces

<div class="diagram-block diagram-app-detail" id="codespaces-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">E</div>
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

---

## Social

<div class="diagram-block diagram-app-detail" id="social-card">
  <div class="app-detail-head">
    <div class="app-detail-letter">F</div>
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
