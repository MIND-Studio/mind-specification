#!/usr/bin/env python3
"""
Inline the markdown source files into the HTML viewers (base64-encoded).

Run after editing any .md file in this directory:

    python3 build.py

Then open index.html (or any other viewer) directly — no server needed.
"""
import base64
import sys
from pathlib import Path

ARCH = Path(__file__).resolve().parent

# (markdown_source, html_viewer)
# Markdown sources live under src/; HTML viewers live at the root.
PAIRS = [
    ("src/architecture.md",                  "index.html"),
    ("src/apps.md",                          "apps.html"),
    ("src/workers.md",                       "workers.html"),
    ("src/protocol/01-pod-layout.md",        "protocol-01.html"),
    ("src/protocol/02-agent-control.md",     "protocol-02.html"),
    ("src/protocol/03-services-manifest.md", "protocol-03.html"),
    ("src/protocol/capabilities.md",         "capabilities.html"),
    ("src/protocol/04-ldn-inbox-outbox.md",  "protocol-04.html"),
]

START = "<!-- BUILD:MD-START -->"
END   = "<!-- BUILD:MD-END -->"


def inline(md_rel: str, html_rel: str) -> bool:
    md_path   = ARCH / md_rel
    html_path = ARCH / html_rel

    if not md_path.exists():
        print(f"  ✗ missing source: {md_rel}", file=sys.stderr)
        return False
    if not html_path.exists():
        print(f"  ✗ missing viewer: {html_rel}", file=sys.stderr)
        return False

    md_text   = md_path.read_text(encoding="utf-8")
    html_text = html_path.read_text(encoding="utf-8")

    b64 = base64.b64encode(md_text.encode("utf-8")).decode("ascii")

    start = html_text.find(START)
    end   = html_text.find(END, start)
    if start == -1 or end == -1:
        print(f"  ✗ {html_rel}: missing BUILD markers", file=sys.stderr)
        return False

    new_block = (
        f'{START}\n'
        f'<script type="text/markdown-base64" id="md-source">\n'
        f'{b64}\n'
        f'</script>\n'
        f'{END}'
    )

    new_html = html_text[:start] + new_block + html_text[end + len(END):]
    html_path.write_text(new_html, encoding="utf-8")
    print(f"  ✓ inlined {md_rel}  →  {html_rel}  ({len(md_text):,} chars md)")
    return True


def main() -> int:
    print(f"build.py — inlining markdown into HTML viewers in {ARCH}")
    ok = all(inline(md, html) for md, html in PAIRS)
    if ok:
        print("done. open index.html (or any other viewer) directly — no server needed.")
        return 0
    print("done with errors.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
