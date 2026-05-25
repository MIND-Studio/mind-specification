# Mind

Most apps today store *your* data on *their* servers. Mind inverts that.

Your data lives in your own store — a **pod**, built on the open [Solid](https://solidproject.org) standard. Apps and background workers read and write your pod over HTTP. Switch apps, your data stays. Switch hosts, your apps follow you. The same calendar entry can be shown by your scheduling app, used by your assistant agent, and shared with a friend's pod — because there's only one copy, and it's yours.

The diagram below shows the four layers, top-down. Apps are what you click; workers do background work on your behalf; the pod is the canonical store; the WebID is your portable login. Sections below explain each one.

## The picture

<div class="diagram-block diagram-layers" aria-label="Mind architecture layers, from apps down to identity">

  <div class="layer">
    <div class="layer-head">
      <span class="layer-num">04</span>
      <div class="layer-meta">
        <div class="layer-name">APPS</div>
        <div class="layer-tag">what you click · web + installed</div>
      </div>
    </div>
    <div class="layer-body">
      <a class="chip" href="apps.html#compass">Compass</a>
      <a class="chip" href="apps.html#marketplace">Marketplace</a>
      <a class="chip" href="apps.html#health">Health</a>
      <a class="chip" href="apps.html#chat">Chat</a>
      <a class="chip" href="apps.html#codespaces">Codespaces</a>
      <a class="chip" href="apps.html#social">Social</a>
    </div>
  </div>

  <div class="layer">
    <div class="layer-head">
      <span class="layer-num">03</span>
      <div class="layer-meta">
        <div class="layer-name">WORKERS</div>
        <div class="layer-tag">background work · holds your pod auth</div>
      </div>
    </div>
    <div class="layer-body">
      <a class="chip" href="workers.html#indexers">indexers</a>
      <a class="chip" href="workers.html#bridges">bridges</a>
      <a class="chip" href="workers.html#agent-runtimes">agent runtimes</a>
    </div>
  </div>

  <div class="layer is-canonical">
    <div class="layer-head">
      <span class="layer-num">02</span>
      <div class="layer-meta">
        <div class="layer-name">POD</div>
        <div class="layer-tag">where your stuff lives · canonical</div>
      </div>
    </div>
    <div class="layer-body">
      <span class="chip chip-pod">Solid pod · hosted anywhere</span>
    </div>
  </div>

  <div class="layer is-external">
    <div class="layer-head">
      <span class="layer-num">01</span>
      <div class="layer-meta">
        <div class="layer-name">WEBID</div>
        <div class="layer-tag">your portable identity · standard Solid + OIDC</div>
      </div>
    </div>
    <div class="layer-body">
      <span class="chip chip-id">WebID + Solid-OIDC</span>
    </div>
  </div>

</div>

### How to read it

Layers stack top-to-bottom. The arrow of dependency points downward: **Apps** and **Workers** both read & write the **Pod** directly — they don't call each other; they meet at the pod. The dotted relation at the bottom is an identity reference (your pod is *named by* your WebID), not a data flow. Every connection above the WebID rail runs over the **Mind Protocol** — a small spec, not a thing that runs.

### Naming convention

Apps in the Mind family are written **with a capital letter** — Compass, Marketplace, Health, Chat, Codespaces, Social. The capital signals a decentralized app: it operates on *your* pod, not on a vendor's database, and the same product name is portable across pod hosts. The lowercase form (`compass`, `marketplace`, …) refers to the folder in your pod (`/apps/marketplace/`) or the codebase, not the product.

Each app eventually gets its own page — for now the diagram chips link to the section below where they're all listed.

---

## Pods and Solid, in plain English

*Already familiar with Solid? [Skip ahead to The four pieces](#the-four-pieces).*

### The shift

Today, when you use Gmail your emails live on Google's servers. When you use Notion, your notes live on Notion's. Your fitness tracker, your bank, your friends' social network — each app keeps *its own copy* of *your* data on *their* servers.

A pod flips that around. There's one copy of your data, in storage you own, and apps just read or write to it.

<div class="diagram-block diagram-shift">
  <div class="shift-pane shift-before">
    <div class="shift-tag">TODAY</div>
    <div class="shift-headline">Apps own your data</div>
    <div class="shift-viz">
      <div class="silo">
        <div class="silo-cell user">you</div>
        <div class="silo-arrow">↓</div>
        <div class="silo-cell app">Gmail</div>
        <div class="silo-arrow">↓</div>
        <div class="silo-cell db">Google's DB</div>
      </div>
      <div class="silo">
        <div class="silo-cell user">you</div>
        <div class="silo-arrow">↓</div>
        <div class="silo-cell app">Notion</div>
        <div class="silo-arrow">↓</div>
        <div class="silo-cell db">Notion's DB</div>
      </div>
      <div class="silo">
        <div class="silo-cell user">you</div>
        <div class="silo-arrow">↓</div>
        <div class="silo-cell app">Strava</div>
        <div class="silo-arrow">↓</div>
        <div class="silo-cell db">Strava's DB</div>
      </div>
    </div>
    <div class="shift-note">Three copies of "you". Three locked databases.</div>
  </div>
  <div class="shift-pane shift-after">
    <div class="shift-tag">WITH PODS</div>
    <div class="shift-headline">You own your data</div>
    <div class="shift-viz">
      <div class="hub">
        <div class="hub-cell user">you</div>
        <div class="hub-arrow">↓</div>
        <div class="hub-apps">
          <div class="hub-app">Mail</div>
          <div class="hub-app">Notes</div>
          <div class="hub-app">Activity</div>
        </div>
        <div class="hub-fan">↘&nbsp;&nbsp;↓&nbsp;&nbsp;↙</div>
        <div class="hub-cell pod">Your Pod</div>
      </div>
    </div>
    <div class="shift-note">One you. One pod. Apps just visit.</div>
  </div>
</div>

### One pod, many apps

Because your data lives in one place, multiple apps see the same information. Your calendar entry "Family Dinner @ Saturday 7pm" can show up in your calendar app, be referenced by your assistant agent when it drafts a reply to your sister, and travel with you when you switch apps next year. One source of truth.

<div class="diagram-block diagram-many">
  <div class="many-row">
    <div class="many-app">
      <div class="many-app-icon">📅</div>
      <div class="many-app-name">Calendar</div>
      <div class="many-app-view">"Family Dinner — Sat 19:00"</div>
    </div>
    <div class="many-app">
      <div class="many-app-icon">🤖</div>
      <div class="many-app-name">Assistant agent</div>
      <div class="many-app-view">"You're busy Sat evening"</div>
    </div>
    <div class="many-app">
      <div class="many-app-icon">✉️</div>
      <div class="many-app-name">Mail</div>
      <div class="many-app-view">"Block out Sat 19:00"</div>
    </div>
  </div>
  <div class="many-fan">↘&nbsp;&nbsp;↓&nbsp;&nbsp;↙</div>
  <div class="many-source">
    <span class="many-source-label">YOUR POD</span>
    <span class="many-source-path">/calendar/2026-05-30.ttl</span>
  </div>
  <div class="many-note">Three different views — one underlying file.</div>
</div>

### What's inside a pod

A pod looks like a folder on the web. It has **folders** (called "containers" in Solid-speak), **files** that each have a URL, and **permissions** that say who can see what.

The top-level folders are shared kinds of data — calendar, contacts, photos, inbox. Then there's an `/apps/` folder where each app you use gets its own sandboxed sub-folder.

<div class="diagram-block diagram-pod-tree">
  <div class="pod-tree-head">
    <span class="pod-tree-dot"></span>
    <span class="pod-tree-host">alice.example.org/</span>
    <span class="pod-tree-chip">your pod</span>
  </div>
  <div class="pod-tree-body">
    <div class="tree-line"><span class="tree-prefix">├─</span><span class="tree-name shared">profile/card</span><span class="tree-comment"># your WebID document</span></div>
    <div class="tree-line"><span class="tree-prefix">├─</span><span class="tree-name shared">calendar/</span><span class="tree-comment"># your events</span></div>
    <div class="tree-line"><span class="tree-prefix">├─</span><span class="tree-name shared">contacts/</span><span class="tree-comment"># your address book</span></div>
    <div class="tree-line"><span class="tree-prefix">├─</span><span class="tree-name shared">photos/</span><span class="tree-comment"># your images</span></div>
    <div class="tree-line"><span class="tree-prefix">├─</span><span class="tree-name shared">inbox/</span><span class="tree-comment"># messages from other pods</span></div>
    <div class="tree-line"><span class="tree-prefix">├─</span><span class="tree-name">agents/</span><span class="tree-comment"># your AI agents (see §1)</span></div>
    <div class="tree-line"><span class="tree-prefix">└─</span><span class="tree-name">apps/</span><span class="tree-comment"># per-app sandboxes</span></div>
    <div class="tree-line indent"><span class="tree-prefix">├─</span><span class="tree-name">marketplace/</span></div>
    <div class="tree-line indent"><span class="tree-prefix">├─</span><span class="tree-name">chat/</span></div>
    <div class="tree-line indent"><span class="tree-prefix">└─</span><span class="tree-name">codespaces/</span></div>
  </div>
  <div class="pod-tree-legend">
    <span class="legend-item"><span class="legend-dot legend-shared"></span> shared — any app can read</span>
    <span class="legend-item"><span class="legend-dot legend-private"></span> private — sandboxed</span>
  </div>
</div>

Apps can read each other's *shared* data (`/calendar/`, `/contacts/`) but they can't peek inside each other's private folders unless you grant access.

### Your WebID — your key

To sign in to apps, you need an identity that's yours, not Google's or Apple's. That's a **WebID**: a URL that points to a document describing you.

<div class="diagram-block diagram-webid">
  <div class="webid-line">
    <span class="webid-part"><span class="webid-text">https://</span><span class="webid-label">scheme</span></span><span class="webid-part highlight"><span class="webid-text">alice.example.org</span><span class="webid-label">your pod host</span></span><span class="webid-part"><span class="webid-text">/profile/card</span><span class="webid-label">the profile file</span></span><span class="webid-part highlight"><span class="webid-text">#me</span><span class="webid-label">"you" inside it</span></span>
  </div>
  <div class="webid-caption">A WebID is just a URL. The fragment <code>#me</code> points to the specific "person" entity inside the profile document.</div>
</div>

When you sign in, you give an app your WebID. The app sends you to your pod's login page; you log in there; you're sent back to the app, authenticated. Your password (or passkey) never touches the app — only your pod host sees it.

<div class="diagram-block diagram-signin">
  <div class="signin-title">SIGN-IN FLOW</div>
  <ol class="signin-steps">
    <li>
      <span class="signin-num">01</span>
      <div class="signin-body">
        <div class="signin-headline">You click <b>Sign in</b> on <b>Marketplace</b>.</div>
      </div>
    </li>
    <li>
      <span class="signin-num">02</span>
      <div class="signin-body">
        <div class="signin-headline">Marketplace asks: "What's your WebID?"</div>
        <div class="signin-detail">You paste <code>https://alice.example.org/profile/card#me</code>.</div>
      </div>
    </li>
    <li>
      <span class="signin-num">03</span>
      <div class="signin-body">
        <div class="signin-headline">Marketplace sends you to your pod's login page.</div>
        <div class="signin-detail">Solid-OIDC redirect — same shape as "Sign in with Google", except the identity provider URL is yours.</div>
      </div>
    </li>
    <li>
      <span class="signin-num">04</span>
      <div class="signin-body">
        <div class="signin-headline">You log in at your pod (password, passkey, hardware key…).</div>
        <div class="signin-detail">Your pod host handles the credentials. Marketplace never sees them.</div>
      </div>
    </li>
    <li>
      <span class="signin-num">05</span>
      <div class="signin-body">
        <div class="signin-headline">You're sent back to Marketplace, authenticated.</div>
        <div class="signin-detail">Marketplace can now read/write the paths you granted — typically <code>/apps/marketplace/</code>.</div>
      </div>
    </li>
  </ol>
</div>

### Where pods can live

Pods aren't owned by any company. You pick where yours runs — and you can move it later without losing your WebID or breaking your apps.

<div class="diagram-block diagram-hosts">
  <div class="hosts-grid">
    <div class="host-card">
      <div class="host-icon">⌂</div>
      <div class="host-name">Home box</div>
      <div class="host-desc">A Raspberry Pi, NAS, or mini-PC in your house.</div>
    </div>
    <div class="host-card">
      <div class="host-icon">☁</div>
      <div class="host-name">Your VPS</div>
      <div class="host-desc">A cheap virtual server you rent.</div>
    </div>
    <div class="host-card">
      <div class="host-icon">▲</div>
      <div class="host-name">Community Verein</div>
      <div class="host-desc">A local non-profit running shared pod infrastructure.</div>
    </div>
    <div class="host-card">
      <div class="host-icon">◆</div>
      <div class="host-name">Commercial host</div>
      <div class="host-desc">A pod-as-a-service provider — you pay monthly, leave anytime.</div>
    </div>
    <div class="host-card">
      <div class="host-icon">◉</div>
      <div class="host-name">A friend's box</div>
      <div class="host-desc">Someone you trust with spare server capacity.</div>
    </div>
    <div class="host-card">
      <div class="host-icon">▢</div>
      <div class="host-name">Your laptop</div>
      <div class="host-desc">Local-first, sync up when you're online.</div>
    </div>
  </div>
  <div class="hosts-note">Whoever hosts your pod just runs the server software — they don't own your data.</div>
</div>

### How Mind fits

Mind is a family of apps and workers that all use Solid pods as their canonical storage. The **Mind Protocol** is a small extra agreement on top of Solid — saying things like "AI agents live under `/agents/`" and "this is the shape of an agent's roster file." Once apps agree on those conventions, they can interoperate freely.

Solid itself comes from [solidproject.org](https://solidproject.org) — a web standard started by Tim Berners-Lee (the inventor of the web). The goal: give people back ownership of their data using the existing web technologies (URLs, HTTP).

Now onward to the architecture itself with the mental model in place.

---

## The four pieces

### Apps

What you click. Six today:

- **Compass** (desktop) — operator UI for a fleet of workers
- **Marketplace** (web) — pod-first listings, cash & meet
- **Health** (web) — personal health records, kept in your pod
- **Chat** (web) — pod-to-pod conversations
- **Codespaces** (web + CLI) — `git push` your site into your pod
- **Social** (web) — posts, friends, async game duels

Each app gets its own folder under `/apps/{name}/` in your pod (see §1) — sandboxed from other apps, but able to read shared containers like `/calendar/` and `/contacts/` so the calendar entry you wrote in one app shows up in another. Adding a new app means writing one that speaks the protocol — no central app store, no platform approval, no business deal with anyone.

Apps come in two shapes:

- **Web apps** — Marketplace, Health, Chat, Codespaces' web side, Social. You visit a URL, sign in with WebID, nothing to install.
- **Installed apps** — Compass, Codespaces' CLI. Run on your machine. May hold local state (UI preferences, operator scratch, cached views), but the canonical data still lives in your pod.

Both shapes speak the same Mind Protocol — only the packaging differs. **Codespaces** is the example that ships both: the web side for managing your sites, the CLI (`codespaces` on your terminal) for `git push`-ing into the pod.

### Workers

The stuff that runs *for* you, not the stuff you click. A worker is a background process that reads and writes your pod **under your auth** (it holds your credentials so it can keep working when you're not at the keyboard). Three flavors today:

- **Indexers** — cache the pod so reads are fast. (Solid pods can be slow when you ask "give me every contact tagged 'family'" — an indexer pre-computes those queries.)
- **Bridges** — translate other protocols to/from the pod. Examples: `git push` lands as files in your pod (Codespaces); your browser's downloads sync into a pod folder; an email account mirrors into pod-shaped messages.
- **Agent runtimes** — host cognitive workers (LLM-backed agents) that take actions on your behalf — drafting messages, summarizing inboxes, watching for changes and reacting. Spec'd in [§2](protocol/02-agent-control.md).

Workers are **replaceable**. The agent runtime today is TS-native. Tomorrow: OpenFang. Or a Claude Code session. Swap one out, your pod is unchanged — including everything your agents have learned about you, because that lives in the pod.

### Pod

Where your stuff lives. A **pod** is a personal data store accessible over HTTP — think "your own private cloud, but tiny and yours." It speaks the [Solid](https://solidproject.org) standard, so any Solid-compatible app can read or write it (subject to your access rules).

Inside it: folders ("containers") for your apps, your agents, your calendar, contacts, inbox, and so on. Each resource has a URL. You decide via per-resource ACLs who can see what.

You can host your pod wherever you want:

- Your own VPS
- A community Verein (e.g. *Bürgernetz Zweibrücken e.V.*)
- A commercial peer host (e.g. *Heusser-und-Nachbarn*)
- A friend with a spare Raspberry Pi
- Your own home box

You own it. You can move it. You can delete it. No host can hold your data hostage — pod-migration tools (which Mind ships, see below) let you carry your pod between hosts without breaking the apps that point at it.

The exact folder layout — `/agents/`, `/apps/{name}/`, `/inbox/`, `/calendar/`, etc. — is specified in [Mind Protocol §1](protocol/01-pod-layout.md).

### WebID

Your portable identity. A **WebID** is a URL that points to a document describing you — usually something like `https://alice.example/profile/card#me`. Apps log you in via [Solid-OIDC](https://solidproject.org/TR/oidc) against that URL, no central account system. Whoever hosts your pod usually hosts your WebID alongside it, but the identity isn't tied to any single app or vendor.

The same WebID moves between every worker and every app. Sign into Marketplace and Social once each; they read different paths in the same pod (`/apps/marketplace/`, `/apps/social/`), but it's still you.

This is all standard Solid — no Mind code involved. Mind just builds on top.

---

## Architecture via C4

The same architecture shown three more ways, using [Simon Brown's C4 model](https://c4model.com) — a notation for system architecture at four levels of zoom. We show Levels 1–3 here. (Level 4 — code — is too low to belong in an architecture overview.)

### L1 — System Context

Who interacts with Mind, and what external systems Mind depends on.

<div class="diagram-block diagram-c4-context">
  <div class="c4-context-grid">
    <div class="c4-actor person">
      <div class="c4-actor-type">PERSON</div>
      <div class="c4-actor-name">Pod Owner</div>
      <div class="c4-actor-desc">Owns the data, runs the apps, operates the worker fleet.</div>
    </div>
    <div class="c4-system">
      <div class="c4-system-tag">SOFTWARE SYSTEM</div>
      <div class="c4-system-name">Mind</div>
      <div class="c4-system-desc">Apps, workers, and the protocol they all speak. Operates on the Pod Owner's Solid pod.</div>
    </div>
    <div class="c4-actor external">
      <div class="c4-actor-type">EXTERNAL</div>
      <div class="c4-actor-name">Pod Host</div>
      <div class="c4-actor-desc">Runs the Solid server. Could be the user, a Verein, a peer host, a friend.</div>
    </div>
    <div class="c4-actor external">
      <div class="c4-actor-type">EXTERNAL</div>
      <div class="c4-actor-name">OIDC Provider</div>
      <div class="c4-actor-desc">Standard Solid-OIDC identity provider. Usually colocated with the pod host.</div>
    </div>
    <div class="c4-actor external">
      <div class="c4-actor-type">EXTERNAL</div>
      <div class="c4-actor-name">Peer Mind Pods</div>
      <div class="c4-actor-desc">Other people's pods. Receive LDN messages from yours and vice versa.</div>
    </div>
    <div class="c4-actor external">
      <div class="c4-actor-type">BUILT ON MIND</div>
      <div class="c4-actor-name">Mind Cube &amp; co.</div>
      <div class="c4-actor-desc">Separate products built using the Mind protocol (e.g. the Raspberry-Pi appliance).</div>
    </div>
  </div>
  <div class="c4-context-rels">
    <span class="c4-rel">Pod Owner <span class="c4-rel-arrow">→</span> Mind <span class="c4-rel-detail">uses (via apps + Compass)</span></span>
    <span class="c4-rel">Mind <span class="c4-rel-arrow">→</span> Pod Host <span class="c4-rel-detail">stores data in (HTTPS, Solid)</span></span>
    <span class="c4-rel">Mind <span class="c4-rel-arrow">→</span> OIDC Provider <span class="c4-rel-detail">authenticates against (Solid-OIDC)</span></span>
    <span class="c4-rel">Mind <span class="c4-rel-arrow">↔</span> Peer Mind Pods <span class="c4-rel-detail">exchanges (LDN, §4)</span></span>
  </div>
</div>

### L2 — Containers

What's inside Mind. Each container is a separately-deployable runnable unit.

<div class="diagram-block diagram-c4-container">
  <div class="c4-boundary">
    <div class="c4-boundary-label">MIND <span class="c4-boundary-sub">— system boundary</span></div>
    <div class="c4-container-grid">
      <div class="c4-container">
        <div class="c4-container-type">[CONTAINER · WEB]</div>
        <div class="c4-container-name">Web Apps</div>
        <div class="c4-container-tech">React / Next.js</div>
        <div class="c4-container-desc">Marketplace, Health, Chat, Codespaces (web), Social. Served from any pod-aware host.</div>
      </div>
      <div class="c4-container">
        <div class="c4-container-type">[CONTAINER · DESKTOP]</div>
        <div class="c4-container-name">Compass</div>
        <div class="c4-container-tech">Electron / Tauri</div>
        <div class="c4-container-desc">Operator UI for worker fleet. Installed on the operator's machine.</div>
      </div>
      <div class="c4-container">
        <div class="c4-container-type">[CONTAINER · BACKGROUND]</div>
        <div class="c4-container-name">Workers</div>
        <div class="c4-container-tech">Node.js / TS (today)</div>
        <div class="c4-container-desc">Indexers, bridges, agent runtimes. Hold the user's pod credentials.</div>
      </div>
      <div class="c4-container canonical">
        <div class="c4-container-type">[CONTAINER · DATA STORE]</div>
        <div class="c4-container-name">Pod</div>
        <div class="c4-container-tech">Solid pod (HTTP)</div>
        <div class="c4-container-desc">The canonical store. All other containers read/write through it.</div>
      </div>
    </div>
  </div>
  <div class="c4-container-rels">
    <span class="c4-rel">Web Apps · Compass · Workers <span class="c4-rel-arrow">↔</span> Pod <span class="c4-rel-detail">read / write — HTTPS</span></span>
    <span class="c4-rel">Workers <span class="c4-rel-arrow">→</span> Pod <span class="c4-rel-detail">under user auth (replaceable)</span></span>
    <span class="c4-rel">Pod <span class="c4-rel-arrow">→</span> Peer Pods <span class="c4-rel-detail">LDN POST to <code>/inbox/</code> (§4)</span></span>
  </div>
</div>

### L3 — Components (Agent Runtime)

Zoom into one container. The Agent Runtime is the most architecturally significant container because it's the only autonomous one — the rest are stateless clients or storage. Its components and how they connect:

<div class="diagram-block diagram-c4-component">
  <div class="c4-comp-title">AGENT RUNTIME · component view</div>
  <div class="c4-comp-grid">
    <div class="c4-comp-group">
      <div class="c4-comp-group-label">INPUT — triggers an iteration</div>
      <div class="c4-comp-card">
        <div class="c4-comp-name">Control Listener</div>
        <div class="c4-comp-desc">Watches <code>/agents/control/</code>; fires on operator commands.</div>
      </div>
      <div class="c4-comp-card">
        <div class="c4-comp-name">Scheduler</div>
        <div class="c4-comp-desc">Fires per <code>state.ttl</code>'s <code>nextActionAt</code>.</div>
      </div>
      <div class="c4-comp-card">
        <div class="c4-comp-name">Change Listener</div>
        <div class="c4-comp-desc">Subscribes to scope paths + <code>/inbox/</code>; fires on writes.</div>
      </div>
    </div>
    <div class="c4-comp-flow">↓</div>
    <div class="c4-comp-group highlight">
      <div class="c4-comp-group-label">EXECUTION — runs one iteration of one agent</div>
      <div class="c4-comp-card primary">
        <div class="c4-comp-name">Agent Executor</div>
        <div class="c4-comp-desc">Runs one iteration. Pluggable backends: prompt, module, external session.</div>
      </div>
    </div>
    <div class="c4-comp-flow">↓</div>
    <div class="c4-comp-group">
      <div class="c4-comp-group-label">SUPPORT — accessed during execution</div>
      <div class="c4-comp-card">
        <div class="c4-comp-name">Memory subsystem</div>
        <div class="c4-comp-desc">Per-agent transcripts + embeddings.</div>
      </div>
      <div class="c4-comp-card">
        <div class="c4-comp-name">Capability client</div>
        <div class="c4-comp-desc">Calls external services declared in §3 manifest.</div>
      </div>
      <div class="c4-comp-card">
        <div class="c4-comp-name">Draft pipeline</div>
        <div class="c4-comp-desc">Bridges agent output → approval queue → outward delivery.</div>
      </div>
    </div>
    <div class="c4-comp-flow">↓</div>
    <div class="c4-comp-group">
      <div class="c4-comp-group-label">OUTPUT — writes to the pod</div>
      <div class="c4-comp-card">
        <div class="c4-comp-name">Audit Logger</div>
        <div class="c4-comp-desc">Append-only, Merkle-chained log of every event.</div>
      </div>
      <div class="c4-comp-card canonical">
        <div class="c4-comp-name">Pod Gateway</div>
        <div class="c4-comp-desc">All writes pass through here. Enforces each agent's <code>hand.ttl</code> scope.</div>
      </div>
    </div>
  </div>
  <div class="c4-comp-note">The Pod Gateway is the choke point. Every byte the runtime writes to the pod passes through it, so per-agent scope enforcement happens in one place — not scattered across components.</div>
</div>

---

## The people involved

Mind isn't just a stack of containers — it's a set of trust relationships. Naming the actors makes the relationships visible.

<div class="diagram-block diagram-people">
  <div class="people-grid">
    <div class="person-card primary">
      <div class="person-badge">ESSENTIAL</div>
      <div class="person-role">Pod Owner</div>
      <div class="person-name">— You</div>
      <div class="person-desc">Owns the data. Runs (or picks) the apps and workers. Sets ACLs. The only actor required for the system to mean anything.</div>
    </div>
    <div class="person-card">
      <div class="person-badge">DRIVES THE FLEET</div>
      <div class="person-role">Operator</div>
      <div class="person-name">— Usually you, sometimes a delegate</div>
      <div class="person-desc">Uses Compass to pause / resume agents, approve drafts, watch the audit log. A family member, an assistant, or a future-you can take this role.</div>
    </div>
    <div class="person-card">
      <div class="person-badge">RUNS THE BOX</div>
      <div class="person-role">Pod Host</div>
      <div class="person-name">— You, a Verein, a peer host, a friend</div>
      <div class="person-desc">Operates the Solid server your pod runs on. Handles uptime and backups. Runs the hardware; does not own the data inside.</div>
    </div>
    <div class="person-card">
      <div class="person-badge">CROSS-POD</div>
      <div class="person-role">Peer Pod Owners</div>
      <div class="person-name">— Other people</div>
      <div class="person-desc">Friends, family, colleagues whose pods exchange LDN messages with yours — offers, invites, mentions. Each has their own pod, their own identity.</div>
    </div>
  </div>
  <div class="people-note">Every role except <b>Pod Owner</b> is replaceable — including yourself in the Operator role. Compass can be handed off. The pod can move hosts. Service providers swap. Friends come and go.</div>
</div>

---

## The Mind Protocol

A small spec — a document, plus optionally a reference SDK. **Doesn't run anywhere; doesn't deploy.**

| § | What | Status |
|---|---|---|
| **1** | Pod layout — paths and shapes apps and workers agree on | [Drafted →](protocol/01-pod-layout.md) |
| **2** | Controlling and observing an agent runtime from outside | [Drafted →](protocol/02-agent-control.md) |
| **3** | How external services advertise themselves | [Drafted →](protocol/03-services-manifest.md) |
| **4** | Cross-pod messaging via LDN | [Drafted →](protocol/04-ldn-inbox-outbox.md) |

---

## What Mind ships besides the protocol

The protocol is the contract. To be useful as a product, Mind also ships operational pieces that aren't part of the spec:

- **Reference pod-host setup** — a turnkey way to stand up a Solid pod (Docker compose around an open-source pod server, sensible ACL defaults, backup script).
- **Pod migration tool** — move a pod from host A to host B without breaking the WebID. (Solid doesn't standardize this; Mind needs to.)
- **Reference workers** — at least one indexer, one bridge, and one agent runtime, all written against the protocol so they're swappable.
- **Reference apps** — the six listed above, plus the Codespaces CLI.

These are *operational* concerns, not part of the protocol contract. Third-party apps and workers that speak the protocol are first-class regardless.

---

## Built with Mind

Things that aren't part of Mind itself, but use Mind:

- **Mind Cube** — a Raspberry Pi appliance with microphone, speakers, display, status LEDs, and a hardware mute switch. Local speech-to-text, text-to-speech, LLM, privacy classification. Separate product, separate lifecycle — but it talks to your pod through the same protocol every Mind app uses.

More can show up here over time. The protocol is what makes them possible without coordinating.

---

## Why this shape

Four load-bearing choices:

- **Pod is canonical.** Only your pod is the source of truth for your stuff. Apps and workers can be replaced without touching it.
  *Consequence: there is no "export my data" feature, because nothing is being held hostage in the first place.*

- **Workers are replaceable.** Swap the agent runtime out and your data — including your agents' memory and what they've learned about you — stays where it is.
  *Consequence: the runtime is a vendor choice, not a lock-in. Today's TypeScript runtime can be replaced by tomorrow's OpenFang without losing your fleet.*

- **Protocol over plumbing.** A spec, not a shared library. Anyone can implement it in any language. Anyone can extend it without coordinating.
  *Consequence: a Rust app and a Python worker can speak to the same pod without ever importing each other's code — they just both speak the protocol.*

- **Coordinate through data.** Components synchronize by writing and reading shared resources in the pod, not by direct RPC. The pod's data model carries the coordination.
  *Consequence: Compass and the agent runtime never call each other — Compass writes a control command to `/agents/control/`, the runtime reads it. Swap either side, the other doesn't notice.*

---

## Open questions

- Should `mind-video` become an app (with a pod), or stay as the experiment that proves "Claude Code session as an agent runtime subtype"?
- Should Compass's repo target and pod target share enough UI to stay one app, or fork into two?
- Is `mind:` the right vocab prefix, or do we want a different brand for the protocol?
- **Where does an agent's behavior actually live?** §2 commits to pluggable per-agent executors; that locks in *what* an agent is but not *where* its code / prompt / config is sourced from. Pod-hosted? Worker-bundled? A skills marketplace?
- **How do skills land in `/agents/{id}/skills/`?** Self-learned through observation, user-installed from somewhere, or both?
- **Pod-host operational deliverables** — the reference setup, migration tool, and backup story are listed above but not yet built. Where do they live (separate repo? part of `mind-cube-product`? a new `mind-podhost`?).
