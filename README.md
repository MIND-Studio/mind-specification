# Mind — specification

Working notes on the Mind architecture — a privacy-first, pod-centric system spec. Markdown is the source of truth; the HTML files are thin viewers that render the markdown locally (no server required).

**Live site:** https://mind-studio.github.io/mind-specification/

## Folder layout

```
architecture/
├── README.md, CLAUDE.md         project meta
├── build.py                     build script (reads src/, writes site/)
│
├── src/                         all markdown source
│   ├── architecture.md          read this first
│   ├── apps.md
│   ├── roadmap.md
│   ├── workers.md
│   └── protocol/
│       ├── 01-pod-layout.md         §1 pod container layout (drafted)
│       ├── 02-agent-control.md      §2 agent control + observation (drafted)
│       ├── 03-services-manifest.md  §3 services manifest (drafted)
│       ├── capabilities.md          capability interface contracts (companion to §3)
│       └── 04-ldn-inbox-outbox.md   §4 LDN inbox + outbox (drafted)
│
├── site/                        published site (this folder is the GitHub Pages artifact)
│   ├── styles.css               shared CSS
│   ├── index.html               ← entry: architecture overview
│   ├── apps.html, roadmap.html, workers.html
│   ├── protocol-01.html ... 04.html  protocol section viewers
│   └── capabilities.html
│
└── slides/                      Slidev decks (pitch + technical)
    ├── pitch.md, technical.md   the two deck entry files
    ├── shared/                  slide-shaped partials imported by both decks
    ├── components/, layouts/, styles/   the ported Mind brand theme
    └── (builds into site/slides/{pitch,technical}/ — gitignored, generated in CI)
```

| File | Purpose |
|---|---|
| [`src/architecture.md`](src/architecture.md) | The architecture overview |
| [`src/apps.md`](src/apps.md) | Per-app intros for the six Mind apps |
| [`src/protocol/`](src/protocol/) | The Mind Protocol sections |
| `site/*.html` | HTML viewers (one per markdown source), plus shared `site/styles.css` |
| `site/styles.css` | Shared CSS (light + dark via `prefers-color-scheme`, or `?theme=dark` URL param) |
| `build.py` | Inlines markdown from `src/` into the `site/` HTML viewers |

## How to read

Two options, pick whichever:

1. **Open the HTML in a browser** — `open site/index.html`. Includes the Mermaid diagrams and themed styling. No server needed. In-doc `.md` links are auto-rewritten to their HTML viewers.
2. **Read the markdown directly** under `src/` — anywhere that renders Markdown + Mermaid: GitHub, VS Code preview (`⇧⌘V`), Obsidian, etc.

## How to edit

1. Edit a file under `src/`.
2. Re-inline the markdown into the HTML viewers:
   ```bash
   python3 build.py
   ```
3. Reload the HTML viewer in your browser.

Markdown viewers (VS Code, Obsidian, GitHub) see your edits immediately; the HTML viewers need the build step because browsers block `fetch()` from `file://`.

## How to add a new protocol section

To add a hypothetical §5:

1. Create `src/protocol/05-your-section.md`.
2. Copy `site/protocol-04.html` to `site/protocol-05.html`. Adjust the `<title>`, change the `aria-current="page"` link to `protocol-05.html`, and update the fallback error message.
3. Add `<a href="protocol-05.html">§5 your-section</a>` to the top nav in **every** viewer in `site/`.
4. Add `("src/protocol/05-your-section.md", "site/protocol-05.html")` to the `PAIRS` list in `build.py`.
5. Run `python3 build.py`.

## How to add a new page (apps-style)

To add a hypothetical workers page:

1. Create `src/workers.md`.
2. Copy `site/apps.html` to `site/workers.html`. Adjust the `<title>`, set `aria-current="page"` on the workers link, and update the fallback error message.
3. Add `<a href="workers.html">Workers</a>` to the nav in every viewer in `site/`.
4. Add `("src/workers.md", "site/workers.html")` to `PAIRS` in `build.py`.
5. Run `python3 build.py`.

## Deploying

The [live site](https://mind-studio.github.io/mind-specification/) is published from the `site/` folder by GitHub Actions (`.github/workflows/build.yml`). On push to `main`, the workflow runs `build.py`, commits any rebuilt viewers back, then uploads `site/` as the Pages artifact and deploys it.

One-time setup: in the repo's **Settings → Pages**, set **Source** to **GitHub Actions**. Because `site/` is published as the web root, the live URLs are unchanged (`…/apps.html`, `…/protocol-01.html`, etc.).

## Slides

Two [Slidev](https://sli.dev) decks live under `slides/` — a **pitch** deck and a **technical architecture** deck. They share a ported Mind brand theme (the cyan/dark look from `site/styles.css`, with the four-layer stack, the data-ownership shift, and the roadmap ladder recreated as Vue components) and `src:`-import a common set of slide-shaped partials from `slides/shared/`, so edits in one partial flow to both decks.

```bash
cd slides
npm install
npm run dev:pitch     # present the pitch deck   (localhost:3030)
npm run dev:tech      # present the technical deck
npm run build         # build both into ../site/slides/{pitch,technical}/
npm run export        # pitch.pdf + technical.pdf (needs playwright-chromium)
```

The decks are **not** distilled automatically from `src/` — they're authored from it by hand (each partial cites the doc section it came from). On push, CI builds both decks into the Pages artifact, published at:

- `https://mind-studio.github.io/mind-specification/slides/pitch/`
- `https://mind-studio.github.io/mind-specification/slides/technical/`

## Previewing dark mode

Append `?theme=dark` or `?theme=light` to any viewer URL to override your OS preference. Useful for screenshots and reviewing both themes without changing settings.

## How it works

Each HTML viewer has a single delimited block:

```html
<!-- BUILD:MD-START -->
<script type="text/markdown-base64" id="md-source">
<base64 of the markdown file>
</script>
<!-- BUILD:MD-END -->
```

`build.py` reads the markdown source from `src/`, base64-encodes it, and replaces what's between the markers. At page load the viewer decodes the block, runs [`marked`](https://marked.js.org/) to render the markdown, and runs [`mermaid`](https://mermaid.js.org/) on `mermaid` code blocks. Both libraries load from jsDelivr; the rest is plain HTML/CSS.

The viewer script also:

- **Slug-ifies heading text into IDs** so in-page anchor links like `#apps` work.
- **Rewrites `.md` links** in the rendered content to their corresponding `.html` viewer (e.g. `protocol/01-pod-layout.md` → `protocol-01.html`), so cross-doc clicks land on the rendered HTML rather than raw markdown.

## Why a build step

Browsers refuse to `fetch()` local files when the page is opened via `file://` (same-origin policy). Three workable options:

- **Build step** (what's here) — inline the markdown into the HTML. Edit-then-rebuild. No server.
- **Local web server** — `python3 -m http.server`. No build, but a server has to be running.
- **Markdown viewer only** — skip the HTML entirely, read markdown in GitHub/VS Code/Obsidian.

The build step is the lowest-friction path for opening the rendered architecture without remembering to start a server.
