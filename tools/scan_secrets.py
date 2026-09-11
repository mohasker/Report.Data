#!/usr/bin/env python3
"""Secret and personal-data scan over the tree that will be packaged.

    python3 tools/scan_secrets.py [root]

Standard library only. Run it before packaging or pushing. It looks for credential
shapes (API keys, tokens, private keys, webhook URLs, assigned secrets), for Drive
links, and for email addresses and telephone numbers that are not recognisably
synthetic.

Known and deliberate: the seed fixtures use @synthetic.example addresses and
sequential placeholder telephone numbers, and MASTER_SPEC.md carries the company's own
publicly published contact details as the owner supplied them in the specification.
Everything else is a finding.
"""
import os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "__pycache__", "dist", ".venv", "node_modules"}

PATTERNS = [
    ("AWS access key id",      re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Anthropic API key",      re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}")),
    ("OpenAI-style key",       re.compile(r"\bsk-[A-Za-z0-9]{32,}")),
    ("Google API key",         re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("Google OAuth client id", re.compile(r"[0-9]+-[0-9a-z]{32}\.apps\.googleusercontent\.com")),
    ("GitHub token",           re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("Slack token",            re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("Bearer token",           re.compile(r"[Bb]earer\s+[A-Za-z0-9_\-\.=]{25,}")),
    ("Private key block",      re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("JWT",                    re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.")),
    ("Make/webhook URL",       re.compile(r"https://hook\.[a-z0-9.\-]*make\.com/[A-Za-z0-9]+")),
    ("Assigned secret",        re.compile(r"(?i)\b(api[_\-]?key|secret|password|passwd|token|client[_\-]?secret)\b\s*[:=]\s*[\"']?[A-Za-z0-9_\-/+=]{12,}")),
    ("Google Drive file id",   re.compile(r"https://drive\.google\.com/[^\s)\"']+")),
    ("Email address",          re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("Qatar phone number",     re.compile(r"\+974[\s\-]?\d{7,8}")),
]

# Known-benign: documented placeholders, synthetic domains, public company contact,
# and the attribution addresses the repository's own commit convention requires.
BENIGN_EMAIL = re.compile(r"(?i)@(alharam\.local|example\.com|example\.org|anthropic\.com|noreply)"
                          r"|synthetic\.example|PENDING|PLACEHOLDER|<|\{|USEREMAIL|your\.name|info@alharam\.qa")

hits = []
declared = []
scanned = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        path = os.path.join(dirpath, fn)
        rel = os.path.relpath(path, ROOT)
        if fn.endswith((".pyc", ".zip", ".bundle", ".pdf")):
            continue
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        for i, line in enumerate(text.splitlines(), 1):
            for name, pat in PATTERNS:
                for m in pat.finditer(line):
                    val = m.group(0)
                    if name == "Email address" and BENIGN_EMAIL.search(val):
                        continue
                    if name == "Qatar phone number" and re.match(r"\+974[\s\-]?(0000000|0000001|3[01]0000\d\d)$", val):
                        continue  # sequential synthetic placeholders in seed fixtures
                    if rel == "MASTER_SPEC.md" and name == "Qatar phone number":
                        declared.append((name, f"{rel}:{i}", val))
                        continue  # the company's own published contact, as the owner supplied it
                    hits.append((name, f"{rel}:{i}", val[:70]))

# filenames that look like credentials
namehits = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if re.search(r"(?i)(credential|client_secret|service-account|\.pem$|\.key$|\.p12$|\.pfx$|^token)", fn):
            namehits.append(os.path.relpath(os.path.join(dirpath, fn), ROOT))

print(f"files scanned: {scanned}")
for n, loc, v in declared:
    print(f"declared and retained: [{n}] {loc} -> {v}  (the company's own published contact details, from the received specification)")
print(f"suspicious filenames: {namehits if namehits else 'none'}")
if hits:
    print(f"MATCHES: {len(hits)}")
    for n, loc, v in hits:
        print(f"  [{n}] {loc}  ->  {v}")
else:
    print("MATCHES: none")

sys.exit(0 if not hits and not namehits else 1)
