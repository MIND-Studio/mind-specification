# Mind — architecture

Working notes on the Mind architecture. Markdown is the source of truth; the HTML files are thin viewers that render the markdown locally (no server required).

## Folder layout

```
architecture/
├── README.md, CLAUDE.md         project meta
├── build.py, styles.css         build script + shared CSS
│
├── index.html                   ← entry: architecture overview
├── apps.html                    ← apps page
├── protocol-01.html ... 04.html ← protocol section viewers
│
└── src/                         all markdown source
    ├── architecture.md          read this first
    ├── apps.md
    └── protocol/
        ├── 01-pod-layout.md         §1 pod container layout (drafted)
        ├── 02-agent-control.md      §2 agent control + observation (drafted)
        ├── 03-services-manifest.md  §3 services manifest (drafted)
        └── 04-ldn-inbox-outbox.md   §4 LDN inbox + outbox (drafted)
```

| File | Purpose |
|---|---|
| [`src/architecture.md`](src/architecture.md) | The architecture overview |
| [`src/apps.md`](src/apps.md) | Per-app intros for the six Mind apps |
| [`src/protocol/`](src/protocol/) | The Mind Protocol sections |
| `index.html` / `apps.html` / `protocol-NN.html` | HTML viewers (one per markdown source) |
| `styles.css` | Shared CSS (light + dark via `prefers-color-scheme`, or `?theme=dark` URL param) |
| `build.py` | Inlines markdown into the HTML viewers |

## How to read

Two options, pick whichever:

1. **Open the HTML in a browser** — `open index.html`. Includes the Mermaid diagrams and themed styling. No server needed. In-doc `.md` links are auto-rewritten to their HTML viewers.
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
2. Copy `protocol-04.html` to `protocol-05.html`. Adjust the `<title>`, change the `aria-current="page"` link to `protocol-05.html`, and update the fallback error message.
3. Add `<a href="protocol-05.html">§5 your-section</a>` to the top nav in **every** viewer.
4. Add the `(md_source, html_viewer)` pair to the `PAIRS` list in `build.py`.
5. Run `python3 build.py`.

## How to add a new page (apps-style)

To add a hypothetical workers page:

1. Create `src/workers.md`.
2. Copy `apps.html` to `workers.html`. Adjust the `<title>`, set `aria-current="page"` on the workers link, and update the fallback error message.
3. Add `<a href="workers.html">Workers</a>` to the nav in every viewer.
4. Add `("src/workers.md", "workers.html")` to `PAIRS` in `build.py`.
5. Run `python3 build.py`.

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
