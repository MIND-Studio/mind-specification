---
id: 0002
title: Apps are independent sibling projects, not a monorepo or shared backend
status: accepted
date: 2026-05-30
deciders: [team]
scope: architecture
supersedes: []
superseded-by: null
---

## Context

Many Mind apps share a stack (Next.js 16, Inrupt, CSS v7) and a login/launcher UI. The
obvious move is a monorepo with shared services. Every prototype's `AGENTS.md` instead
states "independent app, own ports, own data, own docs — do not unify." Recorded
retroactively from the prototype workspace.

## Options considered

1. **Monorepo + shared backend/services.**
   - Pros: DRY, one build, shared types.
   - Cons: couples release cycles; a shared backend becomes a central dependency —
     exactly the lock-in Mind rejects; one app breaking can block others.
2. **Independent siblings** *(chosen)* — each app its own project, ports, data dir, and
   docs; they integrate **only** through the pod and the Mind Protocol. Shared UI ships
   as a versioned package (a committed tarball locally, GitHub Packages for published
   apps), never a workspace `file:` symlink.
   - Pros: apps evolve and deploy independently; matches "coordinate through data, not
     RPC"; one WebID moves between them via the shared OIDC issuer.
   - Cons: some duplication; sharing UI needs an explicit package step — Next.js 16's
     Turbopack rejects `file:` symlinks whose target is outside the project root.

## Decision

Each app is an independent sibling. They coordinate only via the pod + protocol, never
by calling each other or a shared service. Shared code is distributed as a versioned
package (tarball / registry), not a symlink.

## Consequences

- Positive: independent lifecycles; no shared service to become a single point of
  failure or lock-in.
- Costs: shared-UI changes need an explicit sync/publish step
  (`mind-shared-ui/scripts/sync.sh`).
- Follow-ups: if a true monorepo is ever adopted, revisit the packaging step.
