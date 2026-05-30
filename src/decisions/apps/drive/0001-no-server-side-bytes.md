---
id: 0001
title: Pod bytes never transit the app server — all file I/O is client-side
status: accepted
date: 2026-05-30
deciders: [team]
scope: app:drive
supersedes: []
superseded-by: null
---

## Context

Drive is a file browser over a Solid pod (upload, download, preview, share). The
question is where file bytes flow. Routing them through the app's own server is the
conventional shortcut, but it would put plaintext user files on our infrastructure.
Recorded from `mind-drive-v0`.

## Options considered

1. **Proxy pod bytes through the app server** (server fetches/streams files).
   - Pros: simpler CORS handling; server-side caching; pod URLs hidden.
   - Cons: the app server sees plaintext bytes — breaks the privacy promise and creates
     a second copy of the data.
2. **Client-side authenticated `fetch` for everything** *(chosen)* — reads, writes, and
   previews all run in the browser with the user's authenticated `fetch`; the server
   holds no bytes; an optional SQLite cache indexes *listing metadata only*, never bytes.
   - Pros: bytes never transit our server; the pod stays the single source of truth.
   - Cons: the client must handle CORS, auth, and previews (and revoke object URLs).

## Decision

Never proxy pod bytes through the app server. All file I/O — including previews — is
client-side with the authenticated `fetch`. Any server-side cache holds rebuildable
listing metadata only.

## Consequences

- Positive: a real privacy guarantee — plaintext files never touch our infrastructure.
- Costs: more client-side complexity (CORS, preview handling, object-URL lifecycle).
- Follow-ups: never log file names, paths, or contents; set `Content-Type` explicitly on
  upload (CSS defaults to `application/octet-stream`).
