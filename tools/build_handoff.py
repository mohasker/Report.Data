#!/usr/bin/env python3
"""Build the portable handoff package into dist/.

    python3 tools/build_handoff.py

Produces, from the committed working tree:

    dist/AlHaram-Field-Reporting-System-Handoff.zip   the complete working tree
    dist/AlHaram-Field-Reporting-System.bundle        full git history, all branches and tags
    dist/HANDOFF-MANIFEST.json                        checksums and provenance
    dist/HANDOFF-MANIFEST.md                          the same, readable
    dist/<the four handoff documents>                 copied for direct upload

Standard library only. It excludes .git, caches, temporary files and anything the
exclusion list below names, and it refuses to build if the secret scan fails.
"""
import datetime, hashlib, json, os, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIST = os.path.join(ROOT, "dist")

ZIP_NAME = "AlHaram-Field-Reporting-System-Handoff.zip"
BUNDLE_NAME = "AlHaram-Field-Reporting-System.bundle"
PACKAGE_VERSION = "1.0"

PRIMARY = [
    "START-HERE-NEW-CLAUDE.md",
    "MASTER-SPEC-CONSOLIDATED.md",
    "CURRENT-STATUS-AND-NEXT-PROMPT.md",
    "DECISIONS-AND-ASSUMPTIONS.md",
]

EXCLUDE_DIRS = {".git", "__pycache__", "dist", ".venv", "venv", "node_modules",
                ".vscode", ".idea", ".cache", "exports", "backups"}
EXCLUDE_SUFFIX = (".pyc", ".pyo", ".log", ".tmp", ".bak", ".swp", ".DS_Store",
                  ".key", ".pem", ".p12", ".pfx")
EXCLUDE_NAMES = {".DS_Store", "Thumbs.db"}

EXCLUDED_CATEGORIES = [
    "Git internals (.git) — the history is carried by the bundle instead",
    "Credentials, tokens, API keys, private keys and certificates — none exist in this repository",
    "Connection exports containing sensitive identifiers — none exist",
    "Python bytecode caches and virtual environments",
    "Editor and operating-system artifacts",
    "Log, temporary and backup files",
    "Real client data, real project data and real photographs — none exist; every fixture is synthetic",
    "Personal information beyond what the specification itself requires",
    "The dist/ build output, so the package never contains a copy of itself",
]


def sh(*args):
    r = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
    return (r.stdout + r.stderr).strip(), r.returncode


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDE_DIRS)
        for fn in sorted(filenames):
            if fn in EXCLUDE_NAMES or fn.endswith(EXCLUDE_SUFFIX):
                continue
            full = os.path.join(dirpath, fn)
            out.append(os.path.relpath(full, ROOT))
    return sorted(out)


def main():
    os.makedirs(DIST, exist_ok=True)

    scan_out, scan_rc = sh(sys.executable, os.path.join(HERE, "scan_secrets.py"))
    if scan_rc != 0:
        print(scan_out)
        print("\nSECRET SCAN FAILED — package not built.", file=sys.stderr)
        sys.exit(1)

    commit, _ = sh("git", "rev-parse", "HEAD")
    branch, _ = sh("git", "rev-parse", "--abbrev-ref", "HEAD")
    status, _ = sh("git", "status", "--porcelain")
    tree_state = "clean" if not status else "DIRTY: " + status.replace("\n", " | ")

    files = tree_files()

    zip_path = os.path.join(DIST, ZIP_NAME)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in files:
            z.write(os.path.join(ROOT, rel), rel)

    bundle_path = os.path.join(DIST, BUNDLE_NAME)
    bundle_out, bundle_rc = sh("git", "bundle", "create", bundle_path, "--all")
    bundle_ok = bundle_rc == 0 and os.path.exists(bundle_path)

    for rel in PRIMARY:
        src = os.path.join(ROOT, rel)
        if os.path.exists(src):
            with open(src, "rb") as a, open(os.path.join(DIST, rel), "wb") as b:
                b.write(a.read())

    pdf = os.path.join(DIST, "OWNER-REVIEW-PACK.pdf")

    checksums = {}
    for rel in PRIMARY:
        p = os.path.join(DIST, rel)
        if os.path.exists(p):
            checksums[rel] = {"sha256": sha256(p), "bytes": os.path.getsize(p)}
    checksums[ZIP_NAME] = {"sha256": sha256(zip_path), "bytes": os.path.getsize(zip_path),
                           "file_count": len(files)}
    if bundle_ok:
        checksums[BUNDLE_NAME] = {"sha256": sha256(bundle_path),
                                  "bytes": os.path.getsize(bundle_path)}
    if os.path.exists(pdf):
        checksums["OWNER-REVIEW-PACK.pdf"] = {"sha256": sha256(pdf),
                                              "bytes": os.path.getsize(pdf)}

    manifest = {
        "package": "AlHaram-Field-Reporting-System handoff",
        "package_version": PACKAGE_VERSION,
        "created_utc": datetime.datetime.now(datetime.timezone.utc)
                               .replace(microsecond=0).isoformat(),
        "repository": "mohasker/Report.Data",
        "branch": branch,
        "package_commit": commit,
        "working_tree_status": tree_state,
        "validation": {
            "command": "python3 tools/run_validation.py",
            "requires": "Python 3.11+, standard library only. No network, no credential, "
                        "no external service, no installation step.",
            "expected_result": "219/219 checks passed across 13 suites; "
                               "byte-identical regeneration: yes",
        },
        "secret_scan": {
            "command": "python3 tools/scan_secrets.py",
            "result": "PASS — no credential, token, private key, webhook URL or "
                      "non-synthetic identity found",
            "declared_and_retained": [
                "MASTER_SPEC.md carries the company's own publicly published contact "
                "details (website, info address, telephone) exactly as the owner supplied "
                "them in the specification. Retained deliberately; flagged here so the "
                "decision is visible rather than silent."
            ],
            "no_secrets_statement": "No credential, API key, token, private key, webhook "
                                    "URL, connection export or real client photograph was "
                                    "intentionally included in this package. Every user, "
                                    "contact, project and legal entity in the seed data is "
                                    "synthetic and marked as such.",
        },
        "included_file_count": len(files),
        "included_files": files,
        "excluded_categories": EXCLUDED_CATEGORIES,
        "checksums": checksums,
        "read_first": "START-HERE-NEW-CLAUDE.md",
    }
    if not bundle_ok:
        manifest["git_bundle"] = {
            "created": False,
            "reason": bundle_out,
            "recovery": {
                "repository": "mohasker/Report.Data",
                "branch": branch,
                "commit": commit,
                "clone": "git clone https://github.com/mohasker/Report.Data && "
                         f"cd Report.Data && git checkout {branch}",
            },
        }
    else:
        manifest["git_bundle"] = {
            "created": True,
            "file": BUNDLE_NAME,
            "contains": "all branches and tags",
            "verify": f"git bundle verify {BUNDLE_NAME}",
            "clone": f"git clone {BUNDLE_NAME} alharam-repo && cd alharam-repo && "
                     f"git checkout {branch}",
        }

    with open(os.path.join(DIST, "HANDOFF-MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    write_markdown_manifest(manifest)

    print(f"dist/ built at {DIST}")
    print(f"  commit        : {commit}")
    print(f"  branch        : {branch}")
    print(f"  working tree  : {tree_state}")
    print(f"  files in zip  : {len(files)}")
    print(f"  zip           : {os.path.getsize(zip_path):,} bytes")
    if bundle_ok:
        print(f"  bundle        : {os.path.getsize(bundle_path):,} bytes")
    else:
        print(f"  bundle        : NOT CREATED — {bundle_out}")


def write_markdown_manifest(m):
    o, w = [], None
    w = o.append
    w("# Handoff Manifest")
    w("")
    w(f"**Package:** {m['package']} · **Version:** {m['package_version']}")
    w(f"**Created (UTC):** {m['created_utc']}")
    w("")
    w("| | |")
    w("|---|---|")
    w(f"| Repository | `{m['repository']}` |")
    w(f"| Branch | `{m['branch']}` |")
    w(f"| **Package commit** | `{m['package_commit']}` |")
    w(f"| Working tree at build | **{m['working_tree_status']}** |")
    w(f"| Files included | **{m['included_file_count']}** |")
    w(f"| Read first | **`{m['read_first']}`** |")
    w("")
    w("## Validation")
    w("")
    w(f"```\n{m['validation']['command']}\n```")
    w("")
    w(f"**Requires:** {m['validation']['requires']}")
    w("")
    w(f"**Expected result:** {m['validation']['expected_result']}")
    w("")
    w("## Secret scan")
    w("")
    w(f"```\n{m['secret_scan']['command']}\n```")
    w("")
    w(f"**Result:** {m['secret_scan']['result']}")
    w("")
    w(f"{m['secret_scan']['no_secrets_statement']}")
    w("")
    w("**Declared and retained deliberately:**")
    w("")
    for d in m["secret_scan"]["declared_and_retained"]:
        w(f"- {d}")
    w("")
    w("## Checksums (SHA-256)")
    w("")
    w("| File | Bytes | SHA-256 |")
    w("|---|---|---|")
    for name, info in m["checksums"].items():
        w(f"| `{name}` | {info['bytes']:,} | `{info['sha256']}` |")
    w("")
    w("Verify with:")
    w("")
    w("```bash")
    w("sha256sum AlHaram-Field-Reporting-System-Handoff.zip")
    w("# or, on macOS")
    w("shasum -a 256 AlHaram-Field-Reporting-System-Handoff.zip")
    w("```")
    w("")
    w("## Git history")
    w("")
    b = m["git_bundle"]
    if b.get("created"):
        w(f"`{b['file']}` contains **{b['contains']}**.")
        w("")
        w("```bash")
        w(b["verify"])
        w(b["clone"])
        w("```")
    else:
        w("**The Git bundle could not be created.** Reason:")
        w("")
        w(f"```\n{b['reason']}\n```")
        w("")
        w("Recover the history from the remote instead:")
        w("")
        w("```bash")
        w(b["recovery"]["clone"])
        w("```")
        w("")
        w(f"Commit to check out: `{b['recovery']['commit']}`")
    w("")
    w("## Excluded from the package")
    w("")
    for c in m["excluded_categories"]:
        w(f"- {c}")
    w("")
    w("## Included files")
    w("")
    w(f"{m['included_file_count']} files:")
    w("")
    w("```")
    for f in m["included_files"]:
        w(f)
    w("```")
    with open(os.path.join(DIST, "HANDOFF-MANIFEST.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(o) + "\n")


if __name__ == "__main__":
    main()
