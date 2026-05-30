---
id: 0001
title: Builder is a thin orchestrator over the Codespaces bridge — no second source of truth
status: accepted
date: 2026-05-30
deciders: [team]
scope: app:builder
supersedes: []
superseded-by: null
---

## Context

Builder is a "wish an app" chat that turns a request into a running app. It needs to
build, host, and store that app somewhere. Recorded from `mind-builder-v0`. (Note:
Builder is not yet in the `apps.md` catalog.)

## Options considered

1. **Builder builds and hosts apps itself** (own build runner, own storage).
   - Pros: self-contained, no dependency on another service.
   - Cons: duplicates the Codespaces bridge; a second store of repos/build state/
     artifacts becomes a competing source of truth and a lock-in point.
2. **Thin orchestrator over the Codespaces bridge** *(chosen)* — Builder drives the
   bridge over HTTP (repo create → commit → workflow build → Pages publish). The pod
   (via the bridge) holds repos, build state, and the published site; Builder keeps only
   thin session/orchestration state and reuses the bridge's delegated pod auth.
   - Pros: one source of truth (the pod via the bridge); no duplicated build/host logic;
     the chat → spec → build loop stays legible.
   - Cons: depends on the bridge's HTTP API; Builder can't do anything the bridge can't.

## Decision

Builder orchestrates the Codespaces bridge over HTTP and never re-implements build/host
logic or invents a parallel pod-auth path. The pod (via the bridge) is the only store;
Builder holds only thin orchestration state.

## Consequences

- Positive: no duplicate infrastructure; reuses the bridge's pod ownership + auth model.
- Costs: hard dependency on the bridge HTTP API; Builder's capabilities track the bridge's.
- Follow-ups: keep the loop visible to the user (show the spec, build status, preview
  URL); decide whether Builder joins the `apps.md` catalog.
