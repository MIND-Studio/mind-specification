---
id: 0001
title: One shared OIDC issuer — cross-app SSO is a server-side property
status: accepted
date: 2026-05-30
deciders: [team]
scope: architecture
supersedes: []
superseded-by: null
---

## Context

A user has one WebID but many Mind apps, each on its own origin. Solid-OIDC sends
sign-in to the user's identity provider (issuer). We want "sign in once, use
everywhere" without any shared backend between the apps. Recorded retroactively from
the prototype workspace, where every app defaults to the same issuer.

## Options considered

1. **Per-app default issuer + client-side session sharing.**
   - Pros: each app fully self-contained.
   - Cons: browsers isolate storage per origin, so there is no safe client-side way to
     share a session; users re-authenticate in every app.
2. **One shared default issuer; SSO via the IdP cookie** *(chosen)* — every app
   defaults to the same issuer (`NEXT_PUBLIC_SOLID_ISSUER`, currently the production
   pod), overridable per app. On the second app, the IdP recognizes its own session
   cookie on the redirect and skips the prompt.
   - Pros: real SSO across the whole family with no shared backend; a WebID moves
     freely between apps.
   - Cons: the default points at one host; SSO depends on the IdP, not the apps.

## Decision

All apps default to a single shared Solid-OIDC issuer (overridable). Cross-app SSO is
provided **server-side, by the IdP recognizing its session cookie** — not by any
client-side mechanism. The per-app "Continue as <name>" hint is local to each origin
(`mind:<app>:last-identity`) and is **not** shared across apps.

## Consequences

- Positive: one credential entry, recognized across every sibling app.
- Costs: `NEXT_PUBLIC_*` is build-time-inlined — changing the default needs a rebuild
  and a hard reload of open tabs.
- Follow-ups: keep local CSS issuers available as an opt-in override for dev/self-hosting.
