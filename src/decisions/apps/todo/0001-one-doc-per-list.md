---
id: 0001
title: Each Todo list is one Turtle document, not a container of tasks
status: accepted
date: 2026-05-30
deciders: [team]
scope: app:todo
supersedes: []
superseded-by: null
---

## Context

Todo is the surface over the shared `/tasks/` domain. Sharing a list with a person or
an agent is a single WAC grant to a WebID. In CSS v7, a WAC grant on a *container* does
**not** reach the resources inside it, and `acl:default` inheritance stops the moment a
child resource gets its own `.acl`. Recorded from `mind-todo-v0`.

## Options considered

1. **One file per task** (a list = a container of task resources).
   - Pros: per-task ACLs; smaller writes.
   - Cons: "share a list" becomes N grants that miss every task added later.
2. **One document per list** *(chosen)* — the list aggregation + all its tasks in one
   `text/turtle` resource at `/tasks/{id}`.
   - Pros: a single grant covers the whole list and all future tasks; "share with a
     friend" and "assign to an AI agent" become the same one-grant operation.
   - Cons: whole-document writes (coarse last-write-wins, handled with `If-Match`/412
     retry); no per-task ACL.

## Decision

A list is exactly one Turtle resource holding the `schema:ItemList` plus all its
`ical:Vtodo` tasks. Never split tasks into separate resources.

## Consequences

- Positive: one durable grant per list; share == delegate.
- Costs: no per-task access control; concurrent edits touch one document.
- Follow-ups: Todo has no public surface, so there is **no** index/cache at all — pod
  container listings are the only discovery. Keep config + agent artifacts under
  `/apps/todo/`.
