---
id: 0001
title: No central database — posts, follows, DMs, and duels live only in pods
status: accepted
date: 2026-05-30
deciders: [team]
scope: app:social
supersedes: []
superseded-by: null
---

## Context

A social app needs a feed across many people. The tempting shortcut is a central
database of posts/follows/messages. That recreates exactly the data-ownership problem
Mind exists to remove. Recorded from `mind-social-network-v0`.

## Options considered

1. **Central database** of user data (posts, follows, DMs, in-progress duels, blocks).
   - Pros: trivial feeds, search, ranking.
   - Cons: the platform owns the social graph and content — the thing we reject.
2. **Pod-native + public-only indexer** *(chosen)* — all user data lives in each user's
   pod; an indexer worker may cache **public** data only, to assemble feeds.
   - Pros: users own their graph and content; the indexer (i.e. ranking) is a
     replaceable component.
   - Cons: cross-pod feed assembly is harder; private data is never indexed.

## Decision

Never put user data in a central database. The indexer caches only public data to build
feeds; the pod is the source of truth for posts, follows, DMs, and duels.

## Consequences

- Positive: no platform lock-in on the social graph; swap the indexer to change ranking.
- Costs: feeds rely on indexing/polling public pods — more work than a central table.
- Follow-ups: never log DM contents, post bodies, block lists, or raw LDN payloads.
