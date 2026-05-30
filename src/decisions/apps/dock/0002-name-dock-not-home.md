---
id: 0002
title: Name the pod front door "Dock", not "Home"
status: accepted
date: 2026-05-30
deciders: [team]
scope: app:dock
supersedes: []
superseded-by: null
---

## Context

The prototype `mind-home-v0` is the branded front door — app launcher + profile editor
+ account management. The architecture spec already names the launcher shell **Dock**
(`apps.md` → "The shell: Dock"). Having both "Home" (prototype) and "Dock" (spec) for
one thing is two names for one concept.

## Options considered

1. **Keep "Home".**
   - Pros: familiar; matches the current prototype directory name.
   - Cons: generic (collides with "home page" / OS home screen); the spec already says
     "Dock"; leaves two names for one thing.
2. **Rename to "Dock"** *(chosen)* — adopt the spec's shell name everywhere.
   - Pros: one canonical name; evocative single capitalized word (Mind naming
     convention); aligns prototype ↔ spec; distinguishes the launcher from a generic page.
   - Cons: the prototype directory is still `mind-home-v0` (rename is a follow-up); some
     existing docs/notes still say "Home".

## Decision

The pod front-door app is **Dock**. Decision records for it use `scope: app:dock`. The
`mind-home-v0` prototype is Dock's reference implementation; its profile editor and
account management are part of Dock in this implementation (broader than the minimal
launcher concept in the spec).

## Consequences

- Positive: one name across spec, records, and product; on-brand.
- Costs: a follow-up rename of the `mind-home-v0` directory and lingering "Home"
  references in docs/memory.
- Follow-ups: rename the prototype dir; update `apps.md`'s Dock section to note it also
  covers profile + account; carry the launcher registry at `/apps/dock/`.
