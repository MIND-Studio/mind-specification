# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this directory is

Working notes on the **Mind architecture** — a privacy-first, pod-centric system spec. The output is documents (markdown + HTML viewers), not running code.

This is **distinct from `mind-cube-product/`** (described in the parent `/Users/heussers/develop/mind/CLAUDE.md`). Mind Cube is one example of a product **built on** the Mind protocol — a separate product with its own lifecycle. Don't conflate the two: this directory specifies the protocol that Mind Cube (and other apps/workers) speak.

## Folder layout

```
architecture/
├── README.md, CLAUDE.md             project meta
├── build.py                         build script (reads src/, writes site/)
├── src/                             all markdown source
│   ├── architecture.md
│   ├── apps.md
│   ├── roadmap.md
│   ├── workers.md
│   └── protocol/
│       ├── 01-pod-layout.md
│       ├── 02-agent-control.md
│       ├── 03-services-manifest.md
│       ├── capabilities.md          companion to §3 (not a numbered section)
│       └── 04-ldn-inbox-outbox.md
├── site/                            published site (the GitHub Pages artifact)
│   ├── styles.css                   shared CSS
│   ├── index.html                   entry-point viewer
│   ├── apps.html, roadmap.html, workers.html
│   ├── protocol-01.html … 04.html   protocol section viewers
│   └── capabilities.html
└── slides/                          Slidev decks (pitch + technical) — separate toolchain
    ├── pitch.md, technical.md       deck entry files
    ├── shared/                      slide-shaped partials imported by both decks
    └── components/, layouts/, styles/   ported Mind brand theme
```

**Rule:** markdown lives in `src/`, the rendered HTML viewers + `styles.css` live in `site/` (which is what GitHub Pages publishes). The `src/` → `site/` pairing is the `PAIRS` list in `build.py`.

## Slides (`slides/`)

A standalone [Slidev](https://sli.dev) project — **not** part of the `build.py` / `src/` → `site/` flow. Two decks (`pitch.md`, `technical.md`) built on a ported Mind brand theme. They `src:`-import shared partials from `slides/shared/`; the three signature visuals (`LayerStack`, `DataShift`, `RoadmapLadder`) are Vue components in `slides/components/` that reproduce the corresponding `diagram-*` blocks from `site/styles.css`.

- **Source relationship:** decks are distilled *by hand* from `src/*.md` (each partial cites its source section). They are not auto-synced — if the spec changes materially, update the relevant partial/slide too.

### Single source for brand visuals — `shared/brand.css`

Reusable visual blocks (currently the `.mind-mark` animated wordmark) live in **`shared/brand.css`** — one definition, two consumers:

- **Site:** `build.py` injects `shared/brand.css` into `site/styles.css` between the `BUILD:BRAND` markers (same idea as the markdown inlining). Never hand-edit between those markers.
- **Slides:** `slides/styles/index.css` does `@import '../../shared/brand.css'` (Vite; `slides/vite.config.ts` allows reading the parent dir). The Vue wrappers (e.g. `MindMark.vue`) build the markup but carry **no styles** — they rely on the shared classes.

Edit the visual in `shared/brand.css`, run `python3 build.py`, and both the site and the decks update. **Gotchas:** keep it class-scoped and self-contained (literal colors, no host variables); and **no nested `/* */`** inside comments — the raw site load breaks on them (Vite tolerates it, the browser doesn't). To migrate another diagram to single-source, move its CSS into `shared/brand.css`, use identical class-based markup in both the site `.md` and the slide (drop the Vue scoped `<style>`).
- **Workflow:** `cd slides && npm run dev:pitch` (or `dev:tech`) to present; `npm run build` emits into `site/slides/{pitch,technical}/` (gitignored; regenerated in CI). CI builds both decks into the Pages artifact.

## Editing workflow

Markdown is the source of truth. HTML files are thin viewers that base64-inline the markdown so the page works from `file://` without a server (browsers block `fetch()` on `file://` due to same-origin).

After editing any `.md` file under `src/`:

```bash
python3 build.py
```

This rewrites the `<!-- BUILD:MD-START --> … <!-- BUILD:MD-END -->` block in each paired HTML viewer. **Never edit content inside those markers by hand** — the next `build.py` run will overwrite it. Edit the `.md` instead.

Markdown-only viewers (GitHub, VS Code preview, Obsidian) pick up edits without the build step.

## Cross-document links

In markdown, link to other docs using `.md` paths (`protocol/01-pod-layout.md`, `apps.md`, `architecture.md`). Two reasons:

1. Markdown viewers (GitHub, VS Code preview) resolve `.md` paths natively.
2. The HTML viewer script **rewrites** `.md` links to their HTML viewer (`protocol/01-pod-layout.md` → `protocol-01.html`, `apps.md` → `apps.html`, `architecture.md` → `index.html`) at render time. So both worlds work.

The rewriter handles leading `./` or `../` automatically, and emits relative sibling links (`protocol-01.html`) — all viewers sit together in `site/`, so cross-doc links resolve. If you add a new top-level page, extend the `if/else if` block in the viewer JS so it gets rewritten too.

## Adding a new protocol section

To add a hypothetical §5:

1. Create `src/protocol/05-your-section.md`.
2. Copy `site/protocol-04.html` → `site/protocol-05.html`. Adjust `<title>`, move `aria-current="page"` to the §5 link, update the fallback error message.
3. Add `<a href="protocol-05.html">§5 your-section</a>` to the top `<nav>` in **every** viewer in `site/` (there's no shared layout).
4. Add `("src/protocol/05-your-section.md", "site/protocol-05.html")` to `PAIRS` in `build.py`.
5. Run `python3 build.py`.

## Adding a new top-level page (apps-style)

To add a hypothetical workers page:

1. Create `src/workers.md`.
2. Copy `site/apps.html` → `site/workers.html`. Adjust `<title>`, move `aria-current="page"` to the workers link, update the fallback error message.
3. Add `<a href="workers.html">Workers</a>` to the nav in every viewer in `site/`.
4. Add `("src/workers.md", "site/workers.html")` to `PAIRS` in `build.py`.
5. Extend the `.md → .html` rewrite block in the viewer JS so `workers.md` maps to `workers.html` (otherwise cross-doc clicks to it stay as raw markdown).
6. Run `python3 build.py`.

## Verifying changes

`build.py` only checks markers exist; it doesn't validate the rendered output. To actually see Mermaid diagrams, custom HTML/CSS panels, tables, and link resolution:

```bash
open site/index.html   # or any other viewer in site/
```

Append `?theme=dark` or `?theme=light` to override the OS theme preference — useful when checking both palettes. (Many primer/C4 graphics are intentionally cinematic dark in both modes.)

## Visual design system

The doc uses a custom design system (in `site/styles.css`) centered on:

- **Cyan accent** (`#22d3ee` / `#67e8f9`) on canonical / important elements only
- **Dark cinematic panels** for primer / explainer graphics (`#0b0d12` → `#07080b` gradient)
- **Monospace** (`ui-monospace`, JetBrains Mono) for layer numbers, badges, code, technology tags
- **Letter-spaced uppercase** for short labels (layer names, tags) — never for body text
- **Subtle drop-shadows + dot-grid backdrops** for depth without noise

When adding new diagrams, prefer **inline HTML in markdown + CSS in `site/styles.css`** over inline SVG or Mermaid, unless the diagram is genuinely flowchart-shaped and Mermaid output looks good. The user's strong preference is for custom HTML/CSS for design control.

## Status of the spec (as of 2026-05-25)

- `src/architecture.md` — overview with layered hero diagram, Solid primer (6 graphics), C4 showcase (L1/L2/L3), actors, principles, open questions
- `src/apps.md` — apps in general + per-app intros (Compass, Marketplace, Health, Chat, Codespaces, Social)
- `src/protocol/01-pod-layout.md` — **drafted v0.1**
- `src/protocol/02-agent-control.md` — **drafted v0.1** (executors, triggers, change subscription)
- `src/protocol/03-services-manifest.md` — **drafted v0.1** (manifest shape, capability vocab, auth, trust levels)
- `src/protocol/04-ldn-inbox-outbox.md` — **drafted v0.1** (message shapes, outbox pattern, filtering, receipts)

All four protocol sections drafted. The taxonomy is **Apps / Workers / Pod / WebID** (four pieces) — there was a brief experiment with a fifth "Capabilities" category which was pulled back out. Mind Cube is now framed as "Built with Mind" rather than a Capability. Decentralized apps in the Mind family are written with a **capital letter** (Compass, Marketplace, …); lowercase refers to the folder/codebase (`/apps/marketplace/`).

When filling in any new protocol section, follow the §2/§3/§4 conventions: clear purpose section, turtle examples for load-bearing resources, an "Out of scope" section, and an "Open questions" section at the end.
