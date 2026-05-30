# Roadmap

What to build first. What comes next.

The [apps page](apps.md) lists every app in the family without ranking them. This page is opinionated — it says of those fourteen apps (plus the Dock shell), **here's the order, and here's why**.

The thesis is short:

1. **Hosted pods** are the foundation. Until you can sign up for a pod like you sign up for Dropbox, every Mind app is a self-hosting demo. We'll call the hosting service `pods.mind` — it's the *service*; what each user gets is *a pod*.
2. **Agents** is the wedge. It's the only Mind app with no incumbent — there is no "ChatGPT but your memory is yours" today. Build that first.
3. Everything else is downstream of those two. Make Agents + hosted pods work, and the rest of the family gains value as it lands.

## The build order

<div class="diagram-block diagram-roadmap-ladder">

  <div class="roadmap-phase-header">
    <span class="roadmap-phase-num">PHASE&nbsp;I</span>
    <div class="roadmap-phase-titles">
      <div class="roadmap-phase-title">The Wedge</div>
      <div class="roadmap-phase-sub">Ship to the first hundred users.</div>
    </div>
  </div>

  <div class="roadmap-step roadmap-step-foundation">
    <div class="roadmap-step-num">0</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Pods.mind &nbsp;<span class="roadmap-step-name-sub">— hosted pods</span></div>
      <div class="roadmap-step-tag">A pod normal people can sign up for. The foundation everything else stands on.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-planned">PRE-PRODUCT</span></div>
  </div>

  <div class="roadmap-step roadmap-step-now">
    <div class="roadmap-step-num">1</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Agents + Compass</div>
      <div class="roadmap-step-tag">Your AI's memory belongs to you. The only Mind app with no incumbent.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-building">BUILDING</span></div>
  </div>

  <div class="roadmap-step roadmap-step-now">
    <div class="roadmap-step-num">2</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Codespaces</div>
      <div class="roadmap-step-tag">Developer wedge — already production-alpha. They evangelize.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-building">BUILDING</span></div>
  </div>

  <div class="roadmap-phase-header">
    <span class="roadmap-phase-num">PHASE&nbsp;II</span>
    <div class="roadmap-phase-titles">
      <div class="roadmap-phase-title">Make it Daily</div>
      <div class="roadmap-phase-sub">Surround the wedge with the surfaces a daily user needs.</div>
    </div>
  </div>

  <div class="roadmap-step roadmap-step-next">
    <div class="roadmap-step-num">3</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Drive</div>
      <div class="roadmap-step-tag">Where users look first: "where are my files?" Agents need it too.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-building">BUILDING</span></div>
  </div>

  <div class="roadmap-step roadmap-step-next">
    <div class="roadmap-step-num">4</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Todo</div>
      <div class="roadmap-step-tag">The "hello world" that demos the whole thesis — and it's already built.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-building">BUILDING</span></div>
  </div>

  <div class="roadmap-step roadmap-step-next">
    <div class="roadmap-step-num">5</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Dock &nbsp;<span class="roadmap-step-name-sub">— the shell</span></div>
      <div class="roadmap-step-tag">A home screen to find and launch the growing family. New apps just appear.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-concept">CONCEPT</span></div>
  </div>

  <div class="roadmap-step roadmap-step-next">
    <div class="roadmap-step-num">6</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Calendar · Contacts</div>
      <div class="roadmap-step-tag">Shared-domain basics. Contacts makes human-readable sharing work everywhere.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-concept">CONCEPT</span></div>
  </div>

  <div class="roadmap-step roadmap-step-next">
    <div class="roadmap-step-num">7</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Docs</div>
      <div class="roadmap-step-tag">Rich content surface — Agents write here, humans read here.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-concept">CONCEPT</span></div>
  </div>

  <div class="roadmap-step roadmap-step-next">
    <div class="roadmap-step-num">8</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Flow</div>
      <div class="roadmap-step-tag">Work board for humans and agents — only useful once they exist.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-concept">CONCEPT</span></div>
  </div>

  <div class="roadmap-phase-header">
    <span class="roadmap-phase-num">PHASE&nbsp;III</span>
    <div class="roadmap-phase-titles">
      <div class="roadmap-phase-title">Fill Out the Family</div>
      <div class="roadmap-phase-sub">Network-effect, niche, and external-cooperation apps — once Phases I and II have produced users.</div>
    </div>
  </div>

  <div class="roadmap-step roadmap-step-later">
    <div class="roadmap-step-num">9</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Video</div>
      <div class="roadmap-step-tag">Pod-native AI editor. Strong differentiation, no incumbent.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-concept">CONCEPT</span></div>
  </div>

  <div class="roadmap-step roadmap-step-later">
    <div class="roadmap-step-num">10</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Chat · Social · Marketplace</div>
      <div class="roadmap-step-tag">Need network effects. Gate on having users from Phases I–II first.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-concept">CONCEPT</span></div>
  </div>

  <div class="roadmap-step roadmap-step-later">
    <div class="roadmap-step-num">11</div>
    <div class="roadmap-step-body">
      <div class="roadmap-step-name">Health</div>
      <div class="roadmap-step-tag">High value, slow adoption — depends on doctor-side cooperation.</div>
    </div>
    <div class="roadmap-step-status"><span class="app-pill status status-concept">CONCEPT</span></div>
  </div>

</div>

---

## Step 0 — Pods.mind (hosted pods)

**The unsexy prerequisite.** Right now there's `codespaces-pod.duckdns.org` — developer-grade. No real signup, no password-reset, no backups story, no domain control, no SLA. Every "decentralized app" pitch ends with "…and you also need to self-host a Solid server." That sentence kills adoption.

A note on naming: the *service* is `pods.mind` (or "Mind Hosting" in prose); each user gets *a pod*. Avoid "Mind Pod" as a product name — it collides with the technical term for what every user already has.

What "done" looks like at step 0:

- A signup page. Email → WebID + pod. Done in 30 seconds.
- A pod URL the user can hand out. Backups. Recovery flow.
- A pricing decision — paid product, non-profit, sponsor-funded — whichever, but **decided**.
- Pod migration tools, so users believe the "your data is portable" claim.

This isn't an app in `apps.md`. It's the layer underneath them all. Worth a separate write-up of its own.

## Step 1 — Agents + Compass

Of the fourteen Mind apps, **only Agents has no incumbent**. Drive fights Dropbox; Docs fights Notion; Chat fights Signal; Marketplace fights Facebook; Todo fights Todoist; Calendar fights Google Calendar. But "an AI assistant whose memory belongs to you, not OpenAI / Anthropic" — there is no product in that slot today.

Three reasons it's the wedge:

1. **The pain is fresh.** Anyone using AI daily in 2026 feels the vendor-memory lock-in.
2. **No network effects required.** One user is enough. Compare to Chat or Social where the second user determines whether you stay.
3. **It pulls the rest along.** Once Agents exists, every other app gains value: the agent triages your inbox, edits your video, drafts your docs, ships your code.

The working [`mind-agents-v0`](apps.md#agents) prototype is the closest thing to "shippable", and [Compass](apps.md#compass) is its natural operator surface. They ship as one product.

## Step 2 — Codespaces

Already production-alpha. Developers are the obvious first audience because vendor lock-in is most concrete for them (GitHub, Vercel, Netlify own their content). And developers evangelize — they write the *next* Mind apps once they're on hosted pods.

[Codespaces](apps.md#codespaces) at step 2 is "make it work for one developer using their pod for their personal site". Not "rebuild GitHub". The IDE prototype (`mind-codespaces-ide-v0`) can follow once the bridge is solid.

## Step 3 — Drive

Once a user has Agents and the pod, the next question every single one asks is **"where are my files?"** [Drive](apps.md#drive) is the answer, and the prototype is already feature-complete at v0.1. It also does double duty as the place where every other Mind app's stored data is browseable.

## Step 4 — Todo

[Todo](apps.md#todo) is the smallest app that demonstrates the entire thesis — and the `mind-todo-v0` prototype already runs. A to-do list is the universal "hello world," so all the attention falls on what's new underneath: granting a friend access to a list and assigning a task to an AI agent are the *same* WAC grant, because an agent is just another WebID. It ships early in Phase II because it's built, needs no network effects, and is the cleanest demo of "share == delegate." As the surface over the shared `/tasks/` domain, it also seeds the data that Flow (step 8) later plans over.

## Step 5 — Dock

[Dock](apps.md#the-shell-dock) is the shell — the home screen you land on after signing in, and the app-grid that rides along in every app's navbar. It comes once there are a few apps worth switching between (Agents, Codespaces, Drive, Todo); and once it exists, every later app *just appears* in it, discovered by listing the `/apps/` zone. A minimal version — a post-login home page — may show up earlier alongside hosted pods; the full launcher is a Phase II surface.

## Step 6 — Calendar + Contacts

[Calendar](apps.md#calendar) and [Contacts](apps.md#contacts) are the shared-domain basics every daily user expects — and they're *domain surfaces*, so the events and people they manage live in `/calendar/` and `/contacts/` for every other app to read. Contacts earns its place here for a structural reason: it's what turns named-WebID sharing (in Todo, Drive, Health) from "paste a raw pod URL" into "pick a person." Build them together — they're small, and they make the rest of the family feel coherent.

## Step 7 — Docs

Agents need a place to write rich content; humans need a place to read it. [Docs](apps.md#docs) is that. It's still proposal-stage, but the dependency is clear: agent-generated drafts, research notes, project briefs all want to land somewhere richer than a markdown file. Building Docs after Agents is right; building Docs first would be premature.

## Step 8 — Flow

[Flow](apps.md#flow) is a planning surface over the work happening across the other Mind apps. It's useless without Todo (no tasks to plan), Agents (no agent missions), Codespaces (no issues to aggregate), or Docs (no rich specs to attach to a mission). Once those are real, Flow is the board that ties them together.

## Step 9 — Video

[Video](apps.md#video) is in Phase III because, even though the value is clear and the differentiation strong, it's a vertical app — most users don't need an AI video editor. The `mind-video` / drop-cut prototype shows the *shape*; pod-native version waits until Agents and Drive are working surfaces it can plug into.

## Step 10 — Chat · Social · Marketplace

Three apps grouped together because they share one problem: **they need other people**. A pod-first chat with no one to chat with is worse than WhatsApp. A pod-first marketplace with no listings is worse than eBay Classifieds. A pod-first social network with no friends is worse than nothing.

These apps land *after* Phases I and II have produced a user base. They're not unimportant — they may turn out to be Mind's biggest products long-term — but launching them too early means launching to empty rooms.

## Step 11 — Health

Highest unit value of any Mind app: nobody wants their medical records with a vendor. But it has the hardest activation path — usable only when care providers (doctors, clinics, pharmacies) accept WebID-based time-boxed ACL grants. That's a parallel ecosystem to build.

Health stays in the spec as CONCEPT for a reason: it's a target worth aiming at, but not something to build before the rest of the family makes Mind a real thing.

---

## What this roadmap is *not*

It's not a schedule. There are no dates, because dates depend on team size, funding, and how much serendipity hits in the meantime.

It's not the only valid order. Reasonable people could argue for putting Drive at step 1 ("storage is the most universal pain"). The order here is the one that most strongly favors **differentiation over commodity**.

It's also not permanent. As prototypes mature and the world changes — especially as AI assistants get more entrenched or more loose — the order may shift. This page is the current best opinion, not a contract.

## How this connects to the rest

- The list of all apps and their per-app specs lives in [Apps](apps.md).
- The protocol layers everything is built on: [§1 Pod layout](protocol/01-pod-layout.md), [§2 Agent control](protocol/02-agent-control.md), [§3 Services](protocol/03-services-manifest.md), [§4 LDN](protocol/04-ldn-inbox-outbox.md).
- The replaceable infrastructure that sits beside apps: [Workers](workers.md).
- The whole picture: [Architecture overview](architecture.md).
