---
theme: default
title: Mind Architecture
info: |
  ## Mind — technical architecture
  A privacy-first, pod-centric protocol built on Solid. Apps & workers read/write your pod; the pod is the source of truth.
colorSchema: dark
canvasWidth: 1000
fonts:
  sans: Inter
  mono: JetBrains Mono
transition: slide-left
mdc: true
layout: cover
---

<div class="mind-kicker">ARCHITECTURE OVERVIEW</div>

# Mind Architecture

A privacy-first, **pod-centric** protocol.
Built on Solid.

<!-- Audience: engineers / architects. We walk the four layers, the C4 zoom, then the protocol §1–§4. -->

---
layout: center
---

# The thesis

<div class="text-2xl leading-relaxed max-w-3xl mx-auto mt-6">
Most apps store <span class="op60">your</span> data on <span class="op60">their</span> servers.<br/>
Mind <strong>inverts</strong> that.
</div>

<div class="mt-8 text-lg op75 max-w-3xl mx-auto">
Your data lives in a <strong>pod</strong> you own. Apps and background workers read & write it over HTTP — they don't call each other. The pod is the single <strong>source of truth</strong>; apps and workers are replaceable around it.
</div>

---
src: ./shared/layers.md
---

---

# What's inside a pod

<div class="grid grid-cols-[1.1fr_1fr] gap-8 items-center mt-2">

<div class="pod-tree">
  <div class="pt-head"><span class="pt-dot" />alice.example.org/ <span class="pt-chip">your pod</span></div>
  <div class="pt-line"><span class="pt-pre">├─</span><span class="sh">profile/card</span><span class="cm"># your WebID document</span></div>
  <div class="pt-line"><span class="pt-pre">├─</span><span class="sh">calendar/</span><span class="cm"># your events</span></div>
  <div class="pt-line"><span class="pt-pre">├─</span><span class="sh">contacts/</span><span class="cm"># your address book</span></div>
  <div class="pt-line"><span class="pt-pre">├─</span><span class="sh">inbox/</span><span class="cm"># messages from other pods</span></div>
  <div class="pt-line"><span class="pt-pre">├─</span><span class="pv">agents/</span><span class="cm"># your AI agents (§1)</span></div>
  <div class="pt-line"><span class="pt-pre">└─</span><span class="pv">apps/</span><span class="cm"># per-app sandboxes</span></div>
  <div class="pt-line in"><span class="pt-pre">├─</span><span class="pv">marketplace/</span></div>
  <div class="pt-line in"><span class="pt-pre">└─</span><span class="pv">codespaces/</span></div>
</div>

<div>

A pod is **a folder on the web**: containers, files (each with a URL), and per-resource permissions.

- <span class="text-cyan-300">Shared</span> top-level data — any app may read (`/calendar/`, `/contacts/`)
- <span class="op75">Private</span> `/apps/{name}/` sandboxes — walled off unless you grant access

The exact layout is **Protocol §1**.

</div>
</div>

<style scoped>
.pod-tree { font-family: var(--mind-font-mono); font-size: 13px; background: linear-gradient(180deg,#0b0d12,#07080b); border: 1px solid #1e2939; border-radius: 10px; padding: 1.1rem 1.3rem; }
.pt-head { color:#cffafe; margin-bottom: 10px; display:flex; align-items:center; gap:8px; }
.pt-dot { width:8px;height:8px;border-radius:50%;background:#22d3ee;display:inline-block; }
.pt-chip { font-size:10px; border:1px solid rgba(34,211,238,0.4); color:#67e8f9; padding:1px 7px; border-radius:999px; }
.pt-line { line-height: 1.8; color:#cbd5e1; }
.pt-line.in { padding-left: 22px; }
.pt-pre { color: rgba(148,163,184,0.5); margin-right: 8px; }
.sh { color: #a5f3fc; }
.pv { color: #e2e8f0; }
.cm { color: rgba(148,163,184,0.55); margin-left: 10px; }
</style>

---

# WebID & sign-in — standard Solid-OIDC

<div class="flow mt-4">
  <div class="step"><span class="n">01</span><div><b>You click "Sign in"</b> on an app (say, Marketplace).</div></div>
  <div class="step"><span class="n">02</span><div>App asks for your <b>WebID</b> — <code>https://alice.example.org/profile/card#me</code></div></div>
  <div class="step"><span class="n">03</span><div>App redirects you to <b>your pod's</b> login page. Same shape as "Sign in with Google" — but the provider is yours.</div></div>
  <div class="step"><span class="n">04</span><div>You authenticate at your pod (password, passkey, hardware key). <b>The app never sees your credentials.</b></div></div>
  <div class="step"><span class="n">05</span><div>Back to the app, authenticated. It can read/write the paths you granted — typically <code>/apps/marketplace/</code>.</div></div>
</div>

<style scoped>
.flow { display: flex; flex-direction: column; gap: 8px; }
.step { display: flex; align-items: center; gap: 16px; background: rgba(15,23,42,0.5); border: 1px solid rgba(71,85,105,0.5); border-radius: 7px; padding: 0.7rem 1rem; font-size: 0.95rem; }
.step .n { font-family: var(--mind-font-mono); font-size: 14px; font-weight: 800; color: #67e8f9; flex: 0 0 auto; }
</style>

---
layout: center
---

# Where pods can live

<div class="hosts mt-6">
  <div class="h"><div class="ic">⌂</div><b>Home box</b><span>Pi, NAS, mini-PC</span></div>
  <div class="h"><div class="ic">☁</div><b>Your VPS</b><span>a cheap rented server</span></div>
  <div class="h"><div class="ic">▲</div><b>Community Verein</b><span>local non-profit infra</span></div>
  <div class="h"><div class="ic">◆</div><b>Commercial host</b><span>pod-as-a-service</span></div>
  <div class="h"><div class="ic">◉</div><b>A friend's box</b><span>spare capacity</span></div>
  <div class="h"><div class="ic">▢</div><b>Your laptop</b><span>local-first</span></div>
</div>

<div class="mt-6 op75 text-sm">Whoever hosts your pod just runs the server software — they don't own the data. Move anytime; your WebID and apps survive.</div>

<style scoped>
.hosts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; max-width: 56rem; margin-inline: auto; }
.h { background: rgba(15,23,42,0.5); border: 1px solid rgba(71,85,105,0.5); border-radius: 8px; padding: 1rem; text-align: center; }
.h .ic { font-size: 1.6rem; color: #67e8f9; }
.h b { display: block; margin-top: 4px; color: #e2e8f0; }
.h span { font-size: 11px; color: rgba(148,163,184,0.8); }
</style>

---

# The four pieces

<div class="grid grid-cols-2 gap-5 mt-4">
  <div class="piece"><div class="mind-label">APPS</div><p>What you click. Web (visit a URL, sign in with WebID) or installed (Compass, the Codespaces CLI). Sandboxed under <code>/apps/{name}/</code>.</p></div>
  <div class="piece"><div class="mind-label">WORKERS</div><p>Background processes that run <em>for</em> you under your auth. Indexers (fast reads), bridges (protocol translation), agent runtimes (LLM-backed action). <strong>Replaceable.</strong></p></div>
  <div class="piece canon"><div class="mind-label">POD</div><p>A personal data store over HTTP, speaking Solid. Containers, URLs, per-resource ACLs. <strong>The source of truth.</strong></p></div>
  <div class="piece"><div class="mind-label">WEBID</div><p>A URL that identifies you. Apps log in via Solid-OIDC against it. The same WebID moves across every app and worker. Pure Solid — no Mind code.</p></div>
</div>

<style scoped>
.piece { background: rgba(15,23,42,0.5); border: 1px solid rgba(71,85,105,0.5); border-radius: 8px; padding: 1.1rem 1.3rem; }
.piece p { font-size: 0.92rem; color: var(--mind-muted); margin-top: 0.5rem; line-height: 1.5; }
.piece.canon { border-color: rgba(34,211,238,0.45); background: rgba(8,32,52,0.55); box-shadow: inset 0 0 18px rgba(34,211,238,0.08); }
</style>

---

# C4 · L1 — System Context

<div class="c4 mt-4">
  <div class="actor person"><div class="t">PERSON</div><b>Pod Owner</b><span>owns the data, runs the apps & worker fleet</span></div>
  <div class="sys"><div class="t">SOFTWARE SYSTEM</div><b>Mind</b><span>apps, workers & the protocol they all speak — operating on your Solid pod</span></div>
  <div class="col">
    <div class="actor ext"><div class="t">EXTERNAL</div><b>Pod Host</b><span>runs the Solid server</span></div>
    <div class="actor ext"><div class="t">EXTERNAL</div><b>OIDC Provider</b><span>Solid-OIDC identity</span></div>
    <div class="actor ext"><div class="t">EXTERNAL</div><b>Peer pods</b><span>exchange LDN messages (§4)</span></div>
  </div>
</div>

<style scoped>
.c4 { display: grid; grid-template-columns: 1fr 1.2fr 1fr; gap: 14px; align-items: center; }
.c4 .col { display: flex; flex-direction: column; gap: 10px; }
.actor, .sys { border-radius: 8px; padding: 0.9rem 1rem; }
.actor { background: rgba(15,23,42,0.55); border: 1px solid rgba(71,85,105,0.55); }
.actor.person { border-color: rgba(34,211,238,0.4); }
.sys { background: rgba(8,32,52,0.6); border: 1px solid rgba(34,211,238,0.5); text-align: center; box-shadow: inset 0 0 18px rgba(34,211,238,0.1); }
.t { font-family: var(--mind-font-mono); font-size: 9px; letter-spacing: 2px; color: rgba(148,163,184,0.7); }
.actor b, .sys b { display: block; margin: 3px 0; color: #e2e8f0; }
.sys b { color: #cffafe; font-size: 1.3rem; }
.actor span, .sys span { font-size: 11.5px; color: rgba(148,163,184,0.8); }
</style>

---

# C4 · L2 — Containers

<div class="boundary mt-4">
  <div class="blabel">MIND <span class="op60">— system boundary</span></div>
  <div class="cgrid">
    <div class="c"><div class="t">[WEB]</div><b>Web Apps</b><span>React / Next.js</span></div>
    <div class="c"><div class="t">[DESKTOP]</div><b>Compass</b><span>Electron / Tauri</span></div>
    <div class="c"><div class="t">[BACKGROUND]</div><b>Workers</b><span>Node.js / TS (today)</span></div>
    <div class="c canon"><div class="t">[DATA STORE]</div><b>Pod</b><span>Solid pod (HTTP)</span></div>
  </div>
</div>

<div class="mt-4 text-sm op75">Web Apps · Compass · Workers <span class="text-cyan-300">↔</span> Pod (HTTPS read/write). Workers act under user auth and are replaceable. Pod <span class="text-cyan-300">→</span> Peer pods via LDN POST to <code>/inbox/</code>.</div>

<style scoped>
.boundary { border: 1px dashed rgba(148,163,184,0.4); border-radius: 10px; padding: 1.2rem; }
.blabel { font-family: var(--mind-font-mono); font-size: 11px; letter-spacing: 2px; color: rgba(148,163,184,0.85); margin-bottom: 0.8rem; }
.cgrid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.c { background: rgba(15,23,42,0.55); border: 1px solid rgba(71,85,105,0.55); border-radius: 8px; padding: 0.9rem; }
.c .t { font-family: var(--mind-font-mono); font-size: 9px; letter-spacing: 1px; color: rgba(148,163,184,0.7); }
.c b { display: block; margin: 4px 0; color: #e2e8f0; }
.c span { font-size: 11px; color: rgba(148,163,184,0.8); }
.c.canon { border-color: rgba(34,211,238,0.5); background: rgba(8,32,52,0.6); }
.c.canon b { color: #cffafe; }
</style>

---

# C4 · L3 — Agent Runtime

The only autonomous container. One iteration flows top to bottom:

<div class="comp mt-3">
  <div class="grp"><div class="gl">INPUT — triggers an iteration</div><div class="cards"><span>Control Listener</span><span>Scheduler</span><span>Change Listener</span></div></div>
  <div class="arr">↓</div>
  <div class="grp hot"><div class="gl">EXECUTION</div><div class="cards"><span class="p">Agent Executor — pluggable: prompt · module · external session</span></div></div>
  <div class="arr">↓</div>
  <div class="grp"><div class="gl">SUPPORT</div><div class="cards"><span>Memory</span><span>Capability client (§3)</span><span>Draft pipeline</span></div></div>
  <div class="arr">↓</div>
  <div class="grp"><div class="gl">OUTPUT</div><div class="cards"><span>Audit Logger</span><span class="canon">Pod Gateway — enforces each agent's scope</span></div></div>
</div>

<div class="mt-3 text-xs op60">The Pod Gateway is the choke point: every byte written to the pod passes through it, so per-agent scope enforcement lives in one place.</div>

<style scoped>
.comp { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.grp { width: 100%; background: rgba(15,23,42,0.45); border: 1px solid rgba(71,85,105,0.5); border-radius: 8px; padding: 0.6rem 0.9rem; }
.grp.hot { border-color: rgba(34,211,238,0.45); background: rgba(8,32,52,0.5); }
.gl { font-family: var(--mind-font-mono); font-size: 9px; letter-spacing: 1.5px; color: rgba(148,163,184,0.7); margin-bottom: 6px; }
.cards { display: flex; flex-wrap: wrap; gap: 8px; }
.cards span { font-size: 12px; background: rgba(15,23,42,0.7); border: 1px solid rgba(71,85,105,0.55); border-radius: 4px; padding: 4px 10px; color: #cbd5e1; }
.cards span.p { border-color: rgba(34,211,238,0.5); color: #cffafe; }
.cards span.canon { border-color: rgba(34,211,238,0.5); color: #cffafe; }
.arr { color: rgba(103,232,249,0.5); font-size: 13px; }
</style>

---
layout: center
---

# The Mind Protocol

A small spec — a document, plus optionally a reference SDK. **Doesn't run anywhere.**

<div class="max-w-3xl mx-auto mt-4">

| §  | What | Status |
|----|------|--------|
| **1** | Pod layout — paths & shapes apps and workers agree on | Drafted |
| **2** | Controlling & observing an agent runtime from outside | Drafted |
| **3** | How external services advertise themselves | Drafted |
| **4** | Cross-pod messaging via LDN | Drafted |

</div>

<div class="mt-5 text-sm op75">Anyone can implement it in any language. A Rust app and a Python worker speak to the same pod without importing each other's code.</div>

---

# §1 Pod layout · §2 Agent control

<div class="grid grid-cols-2 gap-8 mt-4">
<div>

### §1 — Three zones

- **Shared** top-level data: `/calendar/`, `/contacts/`, `/inbox/` — cross-app readable
- **`/agents/`** — your AI agents: roster, per-agent `hand.ttl` scope, memory, control
- **`/apps/{name}/`** — sandboxed per-app storage

Well-known paths + Turtle resource shapes apps can rely on.

</div>
<div>

### §2 — Control & observe

- **Executors** — pluggable per agent: prompt, module, or external session
- **Triggers** — operator command, scheduler, or change-subscription
- **Control via data** — Compass writes to `/agents/control/`; the runtime reads it. Neither calls the other.

</div>
</div>

---

# §3 Services manifest · §4 LDN

<div class="grid grid-cols-2 gap-8 mt-4">
<div>

### §3 — Capabilities

External services publish a manifest declaring **capabilities** (SpeechToText, LocalLLM, OCR, Translation…), auth, and trust level.

```turtle
<#svc> a mind:Service ;
  mind:capability mind:HostedLLM ;
  mind:endpoint <https://…/v1> ;
  mind:trust "user-approved" .
```

Shared HTTP+JSON conventions; agents discover & call them via the capability client.

</div>
<div>

### §4 — Cross-pod messaging

Pods talk via **Linked Data Notifications**:

- Outbox pattern — you write, the runtime delivers
- Peer pods **POST to your `/inbox/`** — offers, invites, mentions
- Filtering + receipts keep it sane

No central server. Pod-to-pod, over plain HTTP.

</div>
</div>

---
layout: center
---

# Why this shape

<div class="grid grid-cols-2 gap-5 mt-6 max-w-4xl mx-auto text-left">
  <div class="ch"><b>Pod is the source of truth.</b><span>The only authoritative copy. No "export" feature — nothing is held hostage.</span></div>
  <div class="ch"><b>Workers are replaceable.</b><span>Swap the runtime; agents' memory stays in the pod.</span></div>
  <div class="ch"><b>Protocol over plumbing.</b><span>A spec, not a shared library. Any language, no coordination.</span></div>
  <div class="ch"><b>Coordinate through data.</b><span>Components sync via shared pod resources, not RPC.</span></div>
</div>

<div class="mt-6 text-sm op60">Built with Mind: <strong>Mind Cube</strong> — a Raspberry-Pi appliance — talks to your pod through this same protocol. Separate product, separate lifecycle.</div>

<style scoped>
.ch { background: rgba(15,23,42,0.5); border: 1px solid rgba(71,85,105,0.5); border-left: 3px solid #22d3ee; border-radius: 6px; padding: 0.9rem 1.1rem; }
.ch b { color: #e2e8f0; }
.ch span { display: block; margin-top: 4px; font-size: 0.9rem; color: var(--mind-muted); }
</style>

---
src: ./shared/close.md
---
