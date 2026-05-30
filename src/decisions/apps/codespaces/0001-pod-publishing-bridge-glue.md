---
id: 0001
title: Codespaces publishes static sites into the pod; the bridge is protocol glue
status: accepted
date: 2026-05-30
deciders: [team]
scope: app:codespaces
supersedes: []
superseded-by: null
---

## Context

You `git push` to a bridge, which can publish the result as a website. Two questions:
where do the repo and the published output live, and how much does the bridge own?
Recorded from `mind-codespaces-v0`.

## Options considered

1. **Bridge owns everything** (repos + published sites + metadata on the bridge, a
   service account writing them).
   - Pros: simplest server model.
   - Cons: the bridge becomes the source of truth → the exact lock-in Mind rejects.
2. **Pod owns the durable artifacts; bridge is glue** *(chosen)* — identity, repo
   metadata, issues (Turtle), and the published **static** site (Mind Pages,
   world-readable) all live in the user's pod, written under the user's own delegated
   OIDC session (refresh token encrypted at rest). The bridge keeps bare git repos on
   local disk and a SQLite registry as operational state.
   - Pros: the pod owns and can carry the shareable artifacts + metadata; the bridge
     acts as the user, not a service account; everything pod-side is restart-safe.
   - Cons: git *history* lives on the bridge disk, not the pod (a non-pod store for repo
     objects); published output is **static only** (workflow builds run in a sandbox;
     the artifact is a static export).

## Decision

The pod is the source of truth for identity, repo metadata, issues, and the published
static site. The bridge holds bare repos + a registry as replaceable operational state
and always acts as the signed-in user. Published output is static-only.

## Consequences

- Positive: published sites + metadata are user-owned and portable; the bridge is replaceable.
- Costs: repo git objects are not yet pod-resident; no SSR in published sites.
- Follow-ups: whether repos themselves move into the pod is open; never log push tokens,
  session/hook secrets, or refresh tokens.
