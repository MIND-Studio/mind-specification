---
theme: default
title: Mind — your data, your apps, your AI
info: |
  ## Mind — pitch deck
  A privacy-first, pod-centric app family. Your data lives in your own store; apps just visit.
colorSchema: dark
canvasWidth: 980
fonts:
  sans: Inter
  mono: JetBrains Mono
transition: slide-left
mdc: true
layout: center
class: text-center
---

<div class="cover-kicker">THE MIND PROTOCOL</div>

<MindMark class="my-5" />

<div class="cover-tag">Your data. Your apps. Your AI. <strong>For everyone.</strong></div>

<style scoped>
.cover-kicker{ font-family:var(--mind-font-mono); font-size:.8rem; letter-spacing:.3em; text-transform:uppercase; color:var(--mind-accent-bright); }
.cover-tag{ font-size:1.2rem; color:var(--mind-muted); }
</style>

<!--
Opening: the backronym "Decentralized Network In Mind" collapses into MIND — a family of apps where your data lives in a store you own, not on a vendor's servers.
-->

---
layout: center
class: text-center
---

<BrandCover kicker="Mind's mission" attrib="Tim Berners-Lee · London 2012 Olympic opening ceremony · tweeted live from the NeXT cube that hosted the first web server">
"This is <strong>for everyone</strong>."
</BrandCover>

<div class="mt-6 text-base op75 max-w-2xl mx-auto">
The web he invented was open to all. Two decades on it's fenced off — your data in vendors' databases, your AI's memory owned by whichever model you used last.
</div>

---

# The problem

<div class="grid grid-cols-[1.1fr_1fr] gap-8 items-center mt-2">
<div>

Every app keeps **its own copy** of **your** data on **their** servers.

- Your email lives on Google's servers
- Your notes live on Notion's
- Your AI's memory belongs to OpenAI / Anthropic

<div class="mt-4 text-cyan-300">Three copies of "you." None of them yours.</div>

</div>

<DataShift mode="before" />

</div>

---

# The solution: a pod

<div class="grid grid-cols-[1fr_1.1fr] gap-8 items-center mt-2">

<DataShift mode="after" />

<div>

One copy of your data, in storage **you own**. Apps just read and write to it.

- Built on the open **Solid** standard
- Switch apps — your data stays
- Switch hosts — your apps follow you

<div class="mt-4 text-cyan-300">One you. One pod. Apps just visit.</div>

</div>
</div>

---
layout: center
---

# Why now

<div class="grid grid-cols-3 gap-6 mt-8">
  <div class="why-card">
    <div class="mind-label">THE PAIN IS FRESH</div>
    <p>Anyone using AI daily in 2026 feels the vendor-memory lock-in. The slot is empty and the hurt is real.</p>
  </div>
  <div class="why-card">
    <div class="mind-label">THE STANDARD IS READY</div>
    <p>Solid has matured since 2016. Pods, WebID and OIDC are real, interoperable building blocks today.</p>
  </div>
  <div class="why-card">
    <div class="mind-label">NO NETWORK EFFECT NEEDED</div>
    <p>One user is enough to get value. We don't need to fill a room before the product works.</p>
  </div>
</div>

<style scoped>
.why-card { background: rgba(15,23,42,0.5); border: 1px solid rgba(71,85,105,0.5); border-radius: 8px; padding: 1.2rem; }
.why-card p { font-size: 0.95rem; color: var(--mind-muted); margin-top: 0.6rem; }
</style>

---
src: ./shared/family.md
---

---

# The wedge: Agents

<div class="grid grid-cols-[1fr_1fr] gap-10 mt-4">
<div>

Of the whole family, **only Agents has no incumbent.**

Drive fights Dropbox. Docs fights Notion. Chat fights Signal.

But *"an AI assistant whose memory belongs to you, not the model vendor"* — **there is no product in that slot today.**

</div>
<div>

<div class="wedge-quote">
"Your AI's memory<br/>belongs to <span class="text-cyan-300">you</span>."
</div>

<div class="mt-6 op75 text-sm">
Build Agents first. Once it exists, every other app gains value — it triages your inbox, drafts your docs, ships your code, edits your video.
</div>

</div>
</div>

<style scoped>
.wedge-quote { font-size: 1.9rem; font-weight: 700; line-height: 1.2; color: #f5f5f5; }
</style>

---
src: ./shared/built-on-solid.md
---

---
layout: center
---

# What's already real

<div class="grid grid-cols-2 gap-5 mt-6 max-w-4xl mx-auto">
  <div class="real-row"><span class="pill building">PRODUCTION-ALPHA</span><div><b>Codespaces</b> — git-push your site into your pod</div></div>
  <div class="real-row"><span class="pill building">BUILDING</span><div><b>Agents + Compass</b> — the wedge, in progress</div></div>
  <div class="real-row"><span class="pill building">v0.1</span><div><b>Drive</b> — files in your pod, feature-complete</div></div>
  <div class="real-row"><span class="pill building">RUNS</span><div><b>Todo</b> — share == delegate, demoable today</div></div>
</div>

<div class="mt-8 op75 text-sm">Prototypes exist across the stack. The protocol (§1–§4) is drafted and published.</div>

<style scoped>
.real-row { display: flex; align-items: center; gap: 14px; background: rgba(15,23,42,0.5); border: 1px solid rgba(71,85,105,0.5); border-radius: 8px; padding: 0.9rem 1.1rem; }
.real-row b { color: #e2e8f0; }
.pill { font-family: var(--mind-font-mono); font-size: 9px; letter-spacing: 1.5px; font-weight: 700; padding: 4px 9px; border-radius: 2px; white-space: nowrap; }
.pill.building { background: rgba(8,32,52,0.7); border: 1px solid rgba(34,211,238,0.5); color: #67e8f9; }
</style>

---
src: ./shared/roadmap.md
---

---

# The business: hosted pods

<div class="grid grid-cols-[1fr_1fr] gap-10 mt-3 items-center">
<div>

Until you can sign up for a pod like you sign up for Dropbox, every Mind app is a self-hosting demo.

**`pods.mind`** is the foundation — and the monetization:

- Sign up → WebID + pod in 30 seconds
- Backups, recovery, migration tools
- Paid service, non-profit, or sponsor-funded

</div>
<div>

<LayerStack compact />

</div>
</div>

<style scoped>
.slidev-layout h1 { font-size: 1.7em; margin-bottom: 0.3em; }
</style>

---
src: ./shared/close.md
---
