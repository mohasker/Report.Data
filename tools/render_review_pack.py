#!/usr/bin/env python3
"""Render docs/OWNER-REVIEW-PACK.md to dist/OWNER-REVIEW-PACK.pdf.

    python3 tools/render_review_pack.py [--mermaid /path/to/mermaid.min.js] [--out FILE]

Needs a Chromium or Chrome binary and the  package; both are environment
dependencies rather than repository ones, which is why the PDF is a build output and is
not tracked. Without a mermaid bundle the diagrams render as labelled source blocks and
the tool says so rather than producing a document with holes in it.
"""
import os, re, subprocess, sys, html as htmlmod

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SP = os.environ.get("AH_RENDER_TMP") or os.path.join(ROOT, "dist", "_render")
os.makedirs(SP, exist_ok=True)


def arg(flag, default=None):
    a = sys.argv[1:]
    return a[a.index(flag) + 1] if flag in a and a.index(flag) + 1 < len(a) else default


MERMAID = arg("--mermaid", os.environ.get("AH_MERMAID_JS", ""))
SRC = os.path.join(ROOT, "docs", "OWNER-REVIEW-PACK.md")
DIST = os.path.join(ROOT, "dist")
HTML = os.path.join(SP, "review-pack.html")
PDF = arg("--out", os.path.join(DIST, "OWNER-REVIEW-PACK.pdf"))
CANDIDATES = [os.environ.get("AH_CHROME", ""),
              "/opt/pw-browsers/chromium/chrome-linux/chrome",
              "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
              "/usr/bin/chromium", "/usr/bin/chromium-browser",
              "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable"]
CHROME = next((c for c in CANDIDATES if c and os.path.exists(c)), "")
if not CHROME:
    print("No Chromium or Chrome binary found. Set AH_CHROME to one.", file=sys.stderr)
    sys.exit(2)

import markdown

text = open(SRC, encoding="utf-8").read()

# pull mermaid fences out before markdown sees them
blocks = []
def grab(m):
    blocks.append(m.group(1))
    return f"\n\nMERMAIDBLOCK{len(blocks)-1}ENDBLOCK\n\n"
text = re.sub(r"```mermaid\n(.*?)```", grab, text, flags=re.S)

# Metadata blocks wrap one label per line in the source. Markdown would join them into
# a paragraph, which reads as a run-on. Give each bold-label line its own hard break.
out, prev_fence = [], False
for line in text.split("\n"):
    if line.startswith("```"):
        prev_fence = not prev_fence
    if (not prev_fence and out and re.match(r"^\*\*[^*]{1,40}:\*\*", line)
            and out[-1].strip() and not re.match(r"^\s*([-+>#|]|\* |\d+\.)", out[-1])):
        out[-1] = out[-1].rstrip() + "  "
    out.append(line)
text = "\n".join(out)

body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "attr_list"])

def put(m):
    i = int(m.group(1))
    return ('<div class="mermaid-wrap"><pre class="mermaid">'
            + htmlmod.escape(blocks[i]) + "</pre></div>")
body = re.sub(r"<p>MERMAIDBLOCK(\d+)ENDBLOCK</p>", put, body)
body = re.sub(r"MERMAIDBLOCK(\d+)ENDBLOCK", put, body)

CSS = """
@page { size: A4; margin: 16mm 13mm 18mm 13mm; }
* { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
       font-size: 9.4pt; line-height: 1.48; color: #14181d; margin: 0;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
h1 { font-size: 20pt; line-height: 1.2; margin: 0 0 6pt; color: #0b2545;
     border-bottom: 2.5pt solid #0b2545; padding-bottom: 5pt; }
h2 { font-size: 13.5pt; margin: 17pt 0 7pt; color: #0b2545;
     page-break-after: avoid; break-after: avoid;
     border-bottom: 0.8pt solid #c3ccd8; padding-bottom: 3pt; }
h3 { font-size: 11.3pt; margin: 14pt 0 5pt; color: #123a63; page-break-after: avoid; }
h4 { font-size: 10pt; margin: 11pt 0 4pt; color: #123a63; page-break-after: avoid; }
p { margin: 0 0 7pt; orphans: 3; widows: 3; }
ul, ol { margin: 0 0 8pt; padding-left: 17pt; }
li { margin-bottom: 2.5pt; }
hr { border: 0; border-top: 0.7pt solid #d5dce5; margin: 13pt 0; }
a { color: #14508c; text-decoration: none; word-break: break-word; }
code { font-family: "SFMono-Regular", Menlo, Consolas, monospace; font-size: 8.3pt;
       background: #eef2f7; padding: 0.5pt 3pt; border-radius: 2.5pt;
       word-break: break-word; }
pre { background: #f4f7fa; border: 0.6pt solid #d9e1ea; border-radius: 3pt;
      padding: 7pt 9pt; font-size: 8pt; line-height: 1.42; overflow-wrap: break-word;
      white-space: pre-wrap; page-break-inside: avoid; margin: 0 0 9pt; }
pre code { background: none; padding: 0; font-size: 8pt; }
blockquote { margin: 0 0 9pt; padding: 6pt 11pt; border-left: 3pt solid #0b2545;
             background: #f2f6fb; page-break-inside: avoid; }
blockquote p:last-child { margin-bottom: 0; }
table { width: 100%; border-collapse: collapse; margin: 0 0 11pt; font-size: 8.1pt;
        table-layout: auto; page-break-inside: auto; }
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th, td { border: 0.5pt solid #ccd5df; padding: 3.4pt 5pt; text-align: left;
         vertical-align: top; overflow-wrap: break-word; word-break: normal;
         hyphens: none; }
th { background: #e8eef6; font-weight: 600; color: #0b2545; }
tbody tr:nth-child(even) { background: #fafbfd; }
td code, th code { font-size: 7.6pt; padding: 0.3pt 2pt; }
.mermaid-wrap { page-break-inside: avoid; break-inside: avoid; margin: 0 0 13pt;
                text-align: center; }
.mermaid { background: #fff; border: 0.6pt solid #dde4ec; border-radius: 3pt;
           padding: 8pt; white-space: normal; }
.mermaid svg { max-width: 100% !important; height: auto !important; max-height: 168mm; }
strong { color: #0a1a2b; }
"""

MERMAID_TAG = (f'<script src="file://{MERMAID}"></script>' if MERMAID and os.path.exists(MERMAID)
               else "")
if not MERMAID_TAG:
    print("WARNING: no mermaid bundle given (--mermaid). Diagrams will render as source "
          "blocks, not pictures.", file=sys.stderr)
    body = body.replace('<pre class="mermaid">', '<pre class="mermaid-source">')

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Owner Review Pack</title>
<style>{CSS}</style></head>
<body>
{body}
{MERMAID_TAG}
<script>
if (typeof mermaid === "undefined") {{ document.body.setAttribute("data-ready", "1"); }} else {{
mermaid.initialize({{ startOnLoad: false, theme: "neutral", securityLevel: "loose",
  flowchart: {{ useMaxWidth: true, htmlLabels: true }},
  er: {{ useMaxWidth: true }}, state: {{ useMaxWidth: true }},
  themeVariables: {{ fontSize: "13px", fontFamily: "Arial, sans-serif" }} }});
(async () => {{
  try {{ await mermaid.run({{ querySelector: ".mermaid" }}); }}
  catch (e) {{ document.title = "MERMAID ERROR: " + e.message; }}
  document.querySelectorAll(".mermaid svg").forEach(s => {{
    s.removeAttribute("height");
    s.style.maxWidth = "100%";
  }});
  document.body.setAttribute("data-ready", "1");
}})(); }}
</script>
</body></html>"""

open(HTML, "w", encoding="utf-8").write(page)
os.makedirs(DIST, exist_ok=True)

cmd = [CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
       "--run-all-compositor-stages-before-draw", "--virtual-time-budget=40000",
       "--no-pdf-header-footer", f"--print-to-pdf={PDF}", "file://" + HTML]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
if not os.path.exists(PDF):
    print("PDF was not produced", file=sys.stderr)
    sys.exit(1)
print(f"wrote {PDF}: {os.path.getsize(PDF):,} bytes")
