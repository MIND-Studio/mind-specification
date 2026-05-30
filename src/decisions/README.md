# Decision records

Why Mind is shaped the way it is — one decision per file, kept next to the spec.

The spec pages (`architecture.md`, `apps.md`, `projects.md`, the protocol sections)
say **what** is true today. These records say **why**: the forces, the options we
weighed, who decided, and when. The spec is edited freely to stay current; a decision
record is **append-only** — you don't rewrite an accepted one, you supersede it.

> Prototypes implement *subsets* of the spec — a record describes the decision, not
> the current completeness of any one prototype.

## Layout

Records are split by scope:

- `architecture/` — cross-cutting decisions about the base (pod model, protocol,
  the layer model, shared domains, identity).
- `apps/` — decisions specific to one app, each in its own folder `apps/<app>/`
  (e.g. `apps/todo/`).

Each record is `NNNN-short-title.md`, numbered per folder, copied from `TEMPLATE.md`.

## How to add one

1. Copy `TEMPLATE.md` into the right folder with the next number, e.g.
   `architecture/0003-naming-convention.md`.
2. Fill it in with `status: proposed`, then open a pull request.
3. Discuss on the PR. For bigger calls, talk it through, then capture the outcome
   (and any dissent) back in the file.
4. When agreed, merge with `status: accepted` and set `deciders` + `date`.
5. Changed your mind later? Don't edit the accepted record — write a new one that
   `supersedes` it, and flip the old record's `status` to `superseded`.
6. Fold the *outcome* into the relevant spec page so readers see current truth; the
   record keeps the reasoning.

## Status values

`proposed` · `accepted` · `rejected` · `superseded`

## Log

| ID | Scope | Title | Status | Date |
|----|-------|-------|--------|------|
| `architecture/0001` | architecture | One shared OIDC issuer — SSO is a server-side property | accepted | 2026-05-30 |
| `architecture/0002` | architecture | Apps are independent siblings, not a monorepo | accepted | 2026-05-30 |
| `apps/builder/0001` | app:builder | Thin orchestrator over the Codespaces bridge | accepted | 2026-05-30 |
| `apps/codespaces/0001` | app:codespaces | Pod publishes static sites; the bridge is glue | accepted | 2026-05-30 |
| `apps/dock/0001` | app:dock | Two-session split — browser WebID vs server-side account | accepted | 2026-05-30 |
| `apps/dock/0002` | app:dock | Name the pod front door "Dock", not "Home" | accepted | 2026-05-30 |
| `apps/drive/0001` | app:drive | Pod bytes never transit the app server | accepted | 2026-05-30 |
| `apps/social/0001` | app:social | No central database — user data lives only in pods | accepted | 2026-05-30 |
| `apps/todo/0001` | app:todo | Each list is one Turtle document, not a container of tasks | accepted | 2026-05-30 |

Open a record by its ID path under `src/decisions/`.

_Still to capture (decided, not yet written): naming convention, pod-is-source-of-truth,
coordinate-through-data, workers-are-replaceable, domain-surfaces-vs-sandboxed-apps,
Project / no-Workspace._
