---
id: 0001
title: Two-session split — browser WebID session vs server-side pod-account session
status: accepted
date: 2026-05-30
deciders: [team]
scope: app:dock
supersedes: []
superseded-by: null
---

## Context

Dock (the pod front door) does two different jobs: read/write the user's pod (profile,
app registry) and manage the pod *account* (create pods, link WebIDs, client
credentials). These need different credentials. Recorded from `mind-home-v0` (Dock's
reference implementation).

## Options considered

1. **One session for both** — use the WebID/OIDC session for account management too.
   - Pros: one mental model.
   - Cons: the CSS account API needs the pod-account credential (email+password, a
     pod-origin cookie) that the WebID session doesn't carry; exposing it to the browser
     would leak a powerful, long-lived credential.
2. **Two sessions** *(chosen)* — the WebID/OIDC session lives in the browser for pod
   I/O; the CSS *account* session is held **server-side** (cookie encrypted in sqlite)
   and proxied via `/api/account/*`. The account cookie never reaches the browser.
   - Pros: least privilege; the dangerous credential stays server-side and encrypted.
   - Cons: two auth flows; the server holds a short-lived account session.

## Decision

Keep the everyday WebID session in the browser; hold the pod-account session
server-side only, encrypted, behind `/api/account/*`. Never expose or log the account
cookie.

## Consequences

- Positive: account-management power is isolated from the browser; a clear privilege boundary.
- Costs: more moving parts (two sessions + a server-side cookie jar).
- Follow-ups: CSS v7 has no "revoke authorized apps" control — link out to the pod's
  `/.account/` page rather than building a fake one.
