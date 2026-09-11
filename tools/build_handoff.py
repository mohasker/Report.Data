#!/usr/bin/env python3
"""Build the portable handoff package, validating the exact commit that gets packaged.

    python3 tools/build_handoff.py [--mermaid /path/to/mermaid.min.js]

The flow, in the order the owner specified:

  1. Refuse to run unless the source tree is clean. SOURCE_COMMIT_SHA is HEAD.
  2. Clone that exact commit into a temporary directory outside the repository.
  3. Run the full validation suite inside the clone, with the evidence document written
     OUTSIDE the clone, so no tracked file is modified.
  4. Confirm `git status --porcelain` is empty in the clone before and after.
  5. Build the ZIP from the clone — the exact validated commit, not the working tree.
  6. Extract the ZIP and re-run the whole suite from the extracted copy.
  7. Write the manifest (which describes the SOURCE, and deliberately does NOT contain
     the archive's checksum) and a separate delivery receipt (which does).

Standard library only. No network, no credential, no external service.
"""
import datetime, hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIST = os.path.join(ROOT, "dist")

ZIP_NAME = "AlHaram-Field-Reporting-System-Handoff.zip"
BUNDLE_NAME = "AlHaram-Field-Reporting-System.bundle"
PDF_NAME = "OWNER-REVIEW-PACK.pdf"
PACKAGE_VERSION = "1.2"
EXPECTED_CHECKS = 240

PRIMARY = ["START-HERE-NEW-CLAUDE.md", "MASTER-SPEC-CONSOLIDATED.md",
           "CURRENT-STATUS-AND-NEXT-PROMPT.md", "DECISIONS-AND-ASSUMPTIONS.md"]

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
    "The handoff manifest and the delivery receipt, so no archive contains its own checksum",
]


def sh(*args, cwd=ROOT):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return (r.stdout + r.stderr).strip(), r.returncode


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_files(base):
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDE_DIRS)
        for fn in sorted(filenames):
            if fn in EXCLUDE_NAMES or fn.endswith(EXCLUDE_SUFFIX):
                continue
            out.append(os.path.relpath(os.path.join(dirpath, fn), base))
    return sorted(out)


def run_suite(cwd, out_path, label):
    """Run the validation suite with the evidence written outside `cwd`."""
    r = subprocess.run([sys.executable, os.path.join(cwd, "tools", "run_validation.py"),
                        "--out", out_path],
                       capture_output=True, text=True, cwd=cwd)
    text = r.stdout + r.stderr
    total = next((l.strip() for l in text.splitlines() if "TOTAL" in l), "")
    identical = "byte-identical regeneration : yes" in text
    passed = f"TOTAL {EXPECTED_CHECKS}/{EXPECTED_CHECKS} checks passed" in text
    print(f"  {label:<34} {total}   byte-identical: {'yes' if identical else 'NO'}")
    if not (passed and identical and r.returncode == 0):
        print(text[-3000:], file=sys.stderr)
        print(f"\nVALIDATION FAILED IN {label} — package not built.", file=sys.stderr)
        sys.exit(1)
    return {"total": total, "byte_identical": identical, "checks": EXPECTED_CHECKS}


def main():
    argv = sys.argv[1:]
    mermaid = argv[argv.index("--mermaid") + 1] if "--mermaid" in argv else \
        os.environ.get("AH_MERMAID_JS", "")

    # ---- 1. the source tree must be clean, and HEAD is what gets packaged -------------
    status, _ = sh("git", "status", "--porcelain")
    if status:
        print("The source tree is not clean. Commit first, then package.\n" + status,
              file=sys.stderr)
        sys.exit(1)
    source_commit, _ = sh("git", "rev-parse", "HEAD")
    branch, _ = sh("git", "rev-parse", "--abbrev-ref", "HEAD")
    subject, _ = sh("git", "log", "-1", "--format=%s")
    print(f"SOURCE_COMMIT_SHA {source_commit}")
    print(f"  branch                           {branch}")
    print("  source tree before packaging     clean")

    scan_out, scan_rc = sh(sys.executable, os.path.join(HERE, "scan_secrets.py"))
    if scan_rc != 0:
        print(scan_out + "\n\nSECRET SCAN FAILED — package not built.", file=sys.stderr)
        sys.exit(1)
    print("  secret scan                      PASS")

    os.makedirs(DIST, exist_ok=True)
    work = tempfile.mkdtemp(prefix="ah-handoff-")
    clone = os.path.join(work, "src")
    evidence_dir = os.path.join(work, "evidence")
    os.makedirs(evidence_dir)

    try:
        # ---- 2. clone the exact commit, outside the repository -----------------------
        out, rc = sh("git", "clone", "--quiet", "--no-local", ROOT, clone)
        if rc:
            print(out, file=sys.stderr); sys.exit(1)
        sh("git", "checkout", "--quiet", source_commit, cwd=clone)
        head, _ = sh("git", "rev-parse", "HEAD", cwd=clone)
        assert head == source_commit, f"clone is at {head}, expected {source_commit}"
        before, _ = sh("git", "status", "--porcelain", cwd=clone)
        print(f"  clone at exact commit            {'clean' if not before else 'DIRTY'}")
        if before:
            print(before, file=sys.stderr); sys.exit(1)

        # ---- 3-4. validate the clone, evidence off-tree, tree clean after ------------
        val_source = run_suite(clone, os.path.join(evidence_dir, "evidence-source.md"),
                               "validation @ source commit")
        after, _ = sh("git", "status", "--porcelain", cwd=clone)
        print(f"  clone after validation           {'clean' if not after else 'DIRTY: ' + after}")
        if after:
            print("The validation run modified tracked files. Package not built.", file=sys.stderr)
            sys.exit(1)

        # ---- the review pack, rendered from the clone --------------------------------
        pdf = os.path.join(DIST, PDF_NAME)
        cmd = [sys.executable, os.path.join(clone, "tools", "render_review_pack.py"),
               "--out", pdf]
        if mermaid:
            cmd += ["--mermaid", os.path.abspath(mermaid)]
        env = dict(os.environ, AH_RENDER_TMP=os.path.join(work, "render"))
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=clone, env=env)
        pdf_ok = os.path.exists(pdf) and r.returncode == 0
        print(f"  review pack rendered             {'yes' if pdf_ok else 'NO — ' + r.stderr[-200:]}")
        after, _ = sh("git", "status", "--porcelain", cwd=clone)
        if after:
            print("Rendering modified tracked files. Package not built.", file=sys.stderr)
            sys.exit(1)

        # ---- 5. build the ZIP from the clone, not the working tree -------------------
        files = tree_files(clone)
        zip_path = os.path.join(DIST, ZIP_NAME)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for rel in files:
                z.write(os.path.join(clone, rel), rel)
            if pdf_ok:
                z.write(pdf, "docs/" + PDF_NAME)
        listed = list(files) + ([f"docs/{PDF_NAME} (rendered from this commit; not tracked)"]
                                if pdf_ok else [])
        print(f"  zip built from the clone         {len(listed)} files, "
              f"{os.path.getsize(zip_path):,} bytes")

        # ---- 6. extract and re-run the whole suite from the extracted copy -----------
        extracted = os.path.join(work, "extracted")
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(extracted)
        val_zip = run_suite(extracted, os.path.join(evidence_dir, "evidence-extracted.md"),
                            "validation @ extracted zip")

        bundle_path = os.path.join(DIST, BUNDLE_NAME)
        bundle_out, bundle_rc = sh("git", "bundle", "create", bundle_path, "--all")
        bundle_ok = bundle_rc == 0 and os.path.exists(bundle_path)
        if bundle_ok:
            vout, vrc = sh("git", "bundle", "verify", bundle_path)
            bundle_ok = vrc == 0
            print(f"  git bundle                       verified, "
                  f"{os.path.getsize(bundle_path):,} bytes")
        else:
            print(f"  git bundle                       NOT CREATED — {bundle_out}")

        for rel in PRIMARY:
            shutil.copyfile(os.path.join(clone, rel), os.path.join(DIST, rel))

        # ---- 7. manifest (no archive checksum) then receipt (the archive checksum) ---
        manifest = build_manifest(source_commit, branch, subject, listed, val_source, val_zip,
                                  pdf if pdf_ok else None, scan_out)
        mpath = os.path.join(DIST, "HANDOFF-MANIFEST.json")
        with open(mpath, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        write_manifest_md(manifest)

        receipt = {
            "SOURCE_COMMIT_SHA": source_commit,
            "PACKAGE_SHA256": sha256(zip_path),
            "package_file": ZIP_NAME,
            "package_bytes": os.path.getsize(zip_path),
            "package_file_count": len(listed),
            "branch": branch,
            "repository": "mohasker/Report.Data",
            "created_utc": datetime.datetime.now(datetime.timezone.utc)
                                   .replace(microsecond=0).isoformat(),
            "statement": "The exact packaged source commit was validated without modifying "
                         "tracked files.",
            "how": ["The source tree was clean and HEAD was SOURCE_COMMIT_SHA.",
                    "That commit was cloned into a temporary directory outside the repository.",
                    "The full suite ran inside the clone with the evidence document written "
                    "outside it, so no tracked file was written.",
                    "git status --porcelain was empty in the clone both before and after.",
                    "The ZIP was built from that clone, not from the working tree.",
                    "The ZIP was extracted and the full suite re-run from the extracted copy."],
            "validation": {"at_source_commit": val_source, "from_extracted_zip": val_zip},
            "checksums": {
                ZIP_NAME: sha256(zip_path),
                BUNDLE_NAME: sha256(bundle_path) if bundle_ok else None,
                "HANDOFF-MANIFEST.json": sha256(mpath),
                "HANDOFF-MANIFEST.md": sha256(os.path.join(DIST, "HANDOFF-MANIFEST.md")),
                PDF_NAME: sha256(pdf) if pdf_ok else None,
                **{rel: sha256(os.path.join(DIST, rel)) for rel in PRIMARY},
            },
            "circularity_note": "PACKAGE_SHA256 is recorded here and nowhere inside the archive "
                                "it describes. HANDOFF-MANIFEST.json and .md are not members of "
                                "the ZIP, and neither carries the ZIP's checksum, so no file "
                                "attempts to contain a digest of a file containing itself.",
        }
        rpath = os.path.join(DIST, "DELIVERY-RECEIPT.json")
        with open(rpath, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        write_receipt_md(receipt)

        print(f"\nPACKAGE_SHA256    {receipt['PACKAGE_SHA256']}")
        print(f"SOURCE_COMMIT_SHA {source_commit}")
        print(f"\n{receipt['statement']}")
        final, _ = sh("git", "status", "--porcelain")
        print(f"source tree after packaging      {'clean' if not final else 'DIRTY: ' + final}")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def build_manifest(commit, branch, subject, files, val_source, val_zip, pdf, scan_out):
    checks = {}
    for rel in PRIMARY:
        p = os.path.join(DIST, rel)
        if os.path.exists(p):
            checks[rel] = {"sha256": sha256(p), "bytes": os.path.getsize(p)}
    if pdf:
        checks[PDF_NAME] = {"sha256": sha256(pdf), "bytes": os.path.getsize(pdf)}
    return {
        "package": "AlHaram-Field-Reporting-System handoff",
        "package_version": PACKAGE_VERSION,
        "created_utc": datetime.datetime.now(datetime.timezone.utc)
                               .replace(microsecond=0).isoformat(),
        "repository": "mohasker/Report.Data",
        "branch": branch,
        "SOURCE_COMMIT_SHA": commit,
        "source_commit_subject": subject,
        "source_tree_status": "clean before and after packaging",
        "statement": "The exact packaged source commit was validated without modifying "
                     "tracked files.",
        "validation": {
            "command": "python3 tools/run_validation.py",
            "off_tree_command": "python3 tools/run_validation.py --out /path/outside/the/repo.md",
            "requires": "Python 3.11+, standard library only. No network, no credential, no "
                        "external service, no installation step.",
            "expected_result": f"{EXPECTED_CHECKS}/{EXPECTED_CHECKS} checks passed across 13 "
                               f"suites; byte-identical regeneration: yes",
            "at_source_commit": val_source,
            "from_extracted_zip": val_zip,
        },
        "secret_scan": {
            "command": "python3 tools/scan_secrets.py",
            "result": "PASS — no credential, token, private key, webhook URL or non-synthetic "
                      "identity found",
            "declared_and_retained": [
                "MASTER_SPEC.md carries the company's own publicly published contact details "
                "(website, info address, telephone) exactly as the owner supplied them in the "
                "specification. Retained deliberately; flagged here so the decision is visible "
                "rather than silent."],
            "no_secrets_statement": "No credential, API key, token, private key, webhook URL, "
                                    "connection export or real client photograph was "
                                    "intentionally included in this package. Every user, contact, "
                                    "project and legal entity in the seed data is synthetic and "
                                    "marked as such.",
        },
        "archive": {
            "file": ZIP_NAME,
            "built_from": "a clone of SOURCE_COMMIT_SHA, not the working tree",
            "file_count": len(files),
            "checksum_recorded_in": "DELIVERY-RECEIPT.json → PACKAGE_SHA256",
            "why_not_here": "A manifest that carried the checksum of an archive containing the "
                            "manifest could never be verified. This manifest is NOT a member of "
                            "the archive and does NOT record the archive's digest; the delivery "
                            "receipt does, and it is not a member either.",
        },
        "included_file_count": len(files),
        "included_files": files,
        "excluded_categories": EXCLUDED_CATEGORIES,
        "checksums": checks,
        "read_first": "START-HERE-NEW-CLAUDE.md",
    }


def write_manifest_md(m):
    o = []; w = o.append
    w("# Handoff Manifest")
    w("")
    w(f"**Package:** {m['package']} · **Version:** {m['package_version']}")
    w(f"**Created (UTC):** {m['created_utc']}")
    w("")
    w(f"> **{m['statement']}**")
    w("")
    w("| | |")
    w("|---|---|")
    w(f"| Repository | `{m['repository']}` |")
    w(f"| Branch | `{m['branch']}` |")
    w(f"| **SOURCE_COMMIT_SHA** | `{m['SOURCE_COMMIT_SHA']}` |")
    w(f"| Commit subject | {m['source_commit_subject']} |")
    w(f"| Source tree | **{m['source_tree_status']}** |")
    w(f"| Files in the archive | **{m['included_file_count']}** |")
    w(f"| Read first | **`{m['read_first']}`** |")
    w("")
    w("## Validation")
    w("")
    w("```")
    w(m["validation"]["command"])
    w(m["validation"]["off_tree_command"])
    w("```")
    w("")
    w(f"**Requires:** {m['validation']['requires']}")
    w("")
    w(f"**Expected:** {m['validation']['expected_result']}")
    w("")
    w("| Run | Result | Byte-identical regeneration |")
    w("|---|---|---|")
    for k, label in (("at_source_commit", "At SOURCE_COMMIT_SHA, in a clean clone"),
                     ("from_extracted_zip", "From the extracted archive")):
        v = m["validation"][k]
        w(f"| {label} | {v['total']} | {'yes' if v['byte_identical'] else 'NO'} |")
    w("")
    w("## Where the archive's checksum lives")
    w("")
    w(f"**`{m['archive']['file']}` was built from {m['archive']['built_from']}.**")
    w("")
    w(f"Its SHA-256 is recorded in **{m['archive']['checksum_recorded_in']}**, not here.")
    w(f"{m['archive']['why_not_here']}")
    w("")
    w("## Secret scan")
    w("")
    w(f"```\n{m['secret_scan']['command']}\n```")
    w("")
    w(f"**Result:** {m['secret_scan']['result']}")
    w("")
    w(m["secret_scan"]["no_secrets_statement"])
    w("")
    w("**Declared and retained deliberately:**")
    w("")
    for d in m["secret_scan"]["declared_and_retained"]:
        w(f"- {d}")
    w("")
    w("## Checksums of the documents (SHA-256)")
    w("")
    w("| File | Bytes | SHA-256 |")
    w("|---|---|---|")
    for name, info in m["checksums"].items():
        w(f"| `{name}` | {info['bytes']:,} | `{info['sha256']}` |")
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


def write_receipt_md(r):
    o = []; w = o.append
    w("# Delivery Receipt")
    w("")
    w(f"**Created (UTC):** {r['created_utc']} · **Repository:** `{r['repository']}` · "
      f"**Branch:** `{r['branch']}`")
    w("")
    w(f"> **{r['statement']}**")
    w("")
    w("| | |")
    w("|---|---|")
    w(f"| **SOURCE_COMMIT_SHA** | `{r['SOURCE_COMMIT_SHA']}` |")
    w(f"| **PACKAGE_SHA256** | `{r['PACKAGE_SHA256']}` |")
    w(f"| Package file | `{r['package_file']}` |")
    w(f"| Package size | {r['package_bytes']:,} bytes, {r['package_file_count']} files |")
    w("")
    w("## How that statement was established")
    w("")
    for i, step in enumerate(r["how"], 1):
        w(f"{i}. {step}")
    w("")
    w("| Run | Result | Byte-identical regeneration |")
    w("|---|---|---|")
    for k, label in (("at_source_commit", "At SOURCE_COMMIT_SHA, in a clean clone"),
                     ("from_extracted_zip", "From the extracted archive")):
        v = r["validation"][k]
        w(f"| {label} | {v['total']} | {'yes' if v['byte_identical'] else 'NO'} |")
    w("")
    w("## Verify it yourself")
    w("")
    w("```bash")
    w(f"sha256sum {r['package_file']}      # expect {r['PACKAGE_SHA256']}")
    w(f"unzip -q {r['package_file']} -d handoff && cd handoff")
    w("python3 tools/run_validation.py --out /tmp/evidence.md")
    w("```")
    w("")
    w("## Checksums (SHA-256)")
    w("")
    w("| File | SHA-256 |")
    w("|---|---|")
    for name, digest in r["checksums"].items():
        w(f"| `{name}` | " + (f"`{digest}`" if digest else "*not produced*") + " |")
    w("")
    w("## No circular checksum")
    w("")
    w(r["circularity_note"])
    with open(os.path.join(DIST, "DELIVERY-RECEIPT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(o) + "\n")


if __name__ == "__main__":
    main()
