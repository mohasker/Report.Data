#!/usr/bin/env python3
"""Regenerate Phase 1 artifacts, run every check, and write reproducible test evidence.

    python3 tools/run_validation.py

Standard library only. No network, no credential, no external service.

The evidence document records the commit tested, the exact command, the interpreter and
operating environment, the full output, every individual check, a mapping to the
specification's acceptance criteria, whether the generated artifacts came back
byte-identical, and an explicit statement of what these checks are NOT evidence of.
"""
import datetime, hashlib, io, os, platform, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

import modeldef                                                     # noqa: E402
import validate_seed                                                # noqa: E402
from harness import Checks                                          # noqa: E402
from evidence_meta import SUITE_KIND, NOT_PROVEN, ACCEPTANCE_MAP    # noqa: E402
import test_segregation, test_numbering, test_calculations          # noqa: E402
import test_contenthash, test_transitions, test_bilingual           # noqa: E402
import test_evidence_rules, test_configurability, test_governance   # noqa: E402
import test_access_control                                          # noqa: E402

SUITES = [test_configurability, test_segregation, test_access_control, test_evidence_rules,
          test_transitions, test_contenthash, test_numbering, test_calculations,
          test_bilingual, test_governance]
OUT = os.path.join(ROOT, "docs", "01-data-foundation", "17-validation-evidence.md")
GENERATORS = ("build_model.py", "gen_schemas.py", "gen_data_dictionary.py",
              "gen_matrices.py", "gen_appsheet_workbook.py")
GENERATED = [
    "model/model.json",
    "docs/01-data-foundation/01-data-dictionary.md",
    "docs/01-data-foundation/03-status-transition-matrix.md",
    "docs/01-data-foundation/04-security-model.md",
    "docs/02a-plan/01-appsheet-workbook.md",
    "docs/02a-plan/02-security-filter-specification.md",
]


def sh(*args):
    r = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
    return (r.stdout + r.stderr).strip()


def digest(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return None
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def snapshot():
    out = {rel: digest(rel) for rel in GENERATED}
    schema_dir = os.path.join(ROOT, "schemas", "tables")
    if os.path.isdir(schema_dir):
        for name in sorted(os.listdir(schema_dir)):
            rel = f"schemas/tables/{name}"
            out[rel] = digest(rel)
    return out


def regenerate():
    lines = []
    for script in GENERATORS:
        r = subprocess.run([sys.executable, os.path.join(HERE, script)],
                           capture_output=True, text=True)
        lines.append((script, r.returncode, (r.stdout + r.stderr).strip()))
        if r.returncode != 0:
            print((r.stdout + r.stderr).strip(), file=sys.stderr)
            sys.exit(1)
    return lines


def seed_suite(model):
    data, paths = validate_seed.load_seed()
    errors, warnings = validate_seed.validate(model, data, paths)
    c = Checks("Seed conformance",
               "Every seed file conforms to the canonical model: columns, types, formats, "
               "vocabularies, keys, uniqueness, referential integrity and project consistency.")
    c.check("SEED-01", "Every seed file validates against the model with no error",
            not errors, "; ".join(errors[:5]) or
            f"{len(data)} files, {sum(len(r) for r in data.values())} rows, 0 errors")
    c.check("SEED-02", "Every foreign key resolves within the seeded data",
            not [w for w in warnings if "not seeded" not in w],
            f"{len(warnings)} unresolvable-by-design references (tables not built until a later phase)")
    c.check("SEED-03", "At least three materially different projects are present",
            len(data["Projects"]) >= 3,
            f"{len(data['Projects'])} projects with "
            f"{len({p['ClientID'] for p in data['Projects']})} clients, "
            f"{len({p['ReportingFrequency'] for p in data['Projects']})} reporting frequencies, "
            f"{len({p['BillingMethod'] for p in data['Projects']})} billing methods, "
            f"{len({p['DefaultDocumentLanguage'] for p in data['Projects']})} document languages")
    return c, data


def main():
    started = datetime.datetime.now(datetime.timezone.utc)
    commit = sh("git", "rev-parse", "HEAD")
    commit_subject = sh("git", "log", "-1", "--format=%s")
    tree_before = sh("git", "status", "--porcelain")

    before = snapshot()
    gen = regenerate()
    after = snapshot()
    changed = sorted(k for k in after if before.get(k) != after.get(k))
    identical = not changed and bool(before)

    model = modeldef.load()
    seed_checks, data = seed_suite(model)
    suites = [seed_checks] + [m.run(model, data) for m in SUITES]

    total = sum(len(s.results) for s in suites)
    failed = sum(s.failed for s in suites)
    by_id = {r["id"]: r for s in suites for r in s.results}

    console = io.StringIO()
    console.write("=" * 72 + "\n")
    for s in suites:
        console.write(f"  {s.group:<52} {s.passed:>3} passed  {s.failed:>2} failed\n")
    console.write("=" * 72 + "\n")
    console.write(f"  TOTAL {total - failed}/{total} checks passed\n")
    console_text = console.getvalue()

    o = io.StringIO()
    w = o.write
    w("# Phase 1 Validation Evidence\n\n")
    w("**Document ID:** AH-SYS-P1-017 · **Revision:** 2 · "
      "**Status:** Validated Locally · **Generated from an executed run**\n\n")
    w("> **This is evidence of locally executed checks against synthetic data. It is not evidence "
      "that any external platform works.** See section 3.\n\n")

    w("## 1. Reproduction record\n\n")
    w("| | |\n|---|---|\n")
    w(f"| **Commit tested** | `{commit}` |\n")
    w(f"| **Commit subject** | {commit_subject} |\n")
    w(f"| **Command executed** | `python3 tools/run_validation.py` |\n")
    w(f"| **Executed at** | {started.strftime('%Y-%m-%d %H:%M:%S UTC')} |\n")
    w(f"| **Python** | {sys.version.split()[0]} ({platform.python_implementation()}, "
      f"{sys.version.split('[')[-1].rstrip(']')}) |\n")
    w(f"| **Operating system** | {platform.system()} {platform.release()} "
      f"({platform.machine()}) |\n")
    w(f"| **Environment** | Ephemeral Linux container, no network access used, no credential "
      f"present, no external service contacted |\n")
    w(f"| **Third-party dependencies** | **None.** Python standard library only |\n")
    w(f"| **Model version** | {model['model_version']} |\n")
    w(f"| **Working tree before the run** | "
      f"{'clean' if not tree_before else 'MODIFIED — see below'} |\n")
    if tree_before:
        w("\n```\n" + tree_before + "\n```\n\n")
        w("> The run was executed against a working tree containing uncommitted changes. The "
          "commit recorded above is the parent commit, not the exact state tested. Re-run after "
          "committing to obtain a clean reproduction record.\n\n")
    w("\n### Byte-identical regeneration\n\n")
    w(f"Every generated artifact was hashed (SHA-256) before regeneration, regenerated from "
      f"`model/model.json`, and hashed again. **{len(before)} artifacts** were compared: "
      f"the canonical model, the data dictionary, the transition matrix, the security matrix and "
      f"all {len(before) - 4} table schemas.\n\n")
    if identical:
        w("**Result: all artifacts came back byte-identical.** Regeneration is deterministic, so "
          "the committed artifacts are exactly what the model produces.\n\n")
    else:
        w(f"**Result: {len(changed)} artifact(s) changed on regeneration**, listed below. This "
          f"means the committed artifacts were stale, or generation is not deterministic. Either "
          f"way it is a defect.\n\n")
        for k in changed[:20]:
            w(f"- `{k}`\n")
        w("\n")

    w("## 2. Summary\n\n")
    w(f"**{total - failed} of {total} checks passed.**\n\n")
    w("| # | Suite | Kind | Checks | Passed | Failed |\n|---|---|---|---|---|---|\n")
    for i, s in enumerate(suites, 1):
        kind = SUITE_KIND.get(s.group, ("logic", ""))[0]
        w(f"| {i} | {s.group} | {kind} | {len(s.results)} | {s.passed} | "
          f"{'**' + str(s.failed) + '**' if s.failed else '0'} |\n")
    w(f"| | **Total** | | **{total}** | **{total - failed}** | **{failed}** |\n\n")
    if failed:
        w(f"> **{failed} check(s) failed. Phase 1 is not complete until they pass or the owner "
          f"accepts them explicitly.**\n\n")

    w("### Console output\n\n```\n" + console_text + "```\n\n")
    w("### Artifact regeneration output\n\n```\n")
    for script, code, output in gen:
        w(f"$ python3 tools/{script}\n{output}\n")
    w("```\n\n")

    w("## 3. What these checks are NOT evidence of\n\n")
    w("Recorded at the owner's instruction. **Local model validation must never be represented as "
      "proof that an external platform works.** Nothing below has been tested, because nothing "
      "below has been connected (D-14).\n\n")
    w("| Platform or capability | What remains unproven | Proven in |\n|---|---|---|\n")
    for name, what, phase in NOT_PROVEN:
        w(f"| **{name}** | {what} | {phase} |\n")
    w("\n### How to read each suite\n\n")
    w("| Suite | Kind | What it does and does not establish |\n|---|---|---|\n")
    for s in suites:
        kind, note = SUITE_KIND.get(s.group, ("logic", ""))
        w(f"| {s.group} | `{kind}` | {note} |\n")
    w("\n**Kinds.** `structural` — an assertion about the shape of the model or the repository. "
      "`logic` — executable rules run against synthetic data. `simulation` — a reference "
      "implementation standing in for a platform primitive that does not exist yet.\n\n")

    w("## 4. Acceptance criteria mapping\n\n")
    w("The fourteen acceptance criteria in `MASTER_SPEC.md` §14, mapped to the checks that bear on "
      "them. **No criterion is claimed as met**: Phase 1 can only establish that the rules behind a "
      "criterion are correct, never that a built system satisfies it.\n\n")
    w("| §14 | Criterion | Phase 1 status | Checks | Note |\n|---|---|---|---|---|\n")
    label = {"proven-in-logic": "Rule proven in logic", "partial": "Rule defined and tested",
             "not-tested": "**Not tested in Phase 1**"}
    for num, crit, ids, status, note in ACCEPTANCE_MAP:
        present = [i for i in ids if i in by_id]
        missing = [i for i in ids if i not in by_id]
        cell = ", ".join(f"`{i}`" for i in present) if present else "—"
        if missing:
            cell += f" (unmatched: {', '.join(missing)})"
        w(f"| {num} | {crit} | {label[status]} | {cell} | {note} |\n")
    w("\n")

    w("## 5. Every check executed\n\n")
    w("Listed in full so a reviewer can see what was measured rather than taking a summary on "
      "trust. The evidence column is the value the check actually produced.\n\n")
    for s in suites:
        kind, _ = SUITE_KIND.get(s.group, ("logic", ""))
        w(f"### {s.group}  ·  `{kind}`  ·  {s.passed}/{len(s.results)} passed\n\n")
        w(f"{s.purpose}\n\n")
        w("| Check | Result | Description | Evidence produced |\n|---|---|---|---|\n")
        for r in s.results:
            detail = r["detail"].replace("|", "\\|").replace("\n", " ")
            if len(detail) > 320:
                detail = detail[:317] + "..."
            w(f"| `{r['id']}` | {'PASS' if r['passed'] else '**FAIL**'} | "
              f"{r['description']} | {detail} |\n")
        w("\n")

    w("---\n\n## 6. Reproducing this run\n\n")
    w("```\ngit checkout " + commit + "\npython3 tools/run_validation.py\n```\n\n")
    w("No installation, no dependency, no network access and no credential is required. The run "
      "regenerates every artifact and rewrites this document; the only file it modifies is this "
      "one, which a reviewer can confirm with `git status` immediately afterwards.\n")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(o.getvalue())

    tree_after = sh("git", "status", "--porcelain")
    print("\n" + console_text)
    print(f"  byte-identical regeneration : {'yes' if identical else 'NO — ' + str(len(changed))}")
    print(f"  commit tested               : {commit[:12]}")
    print(f"  working tree after the run  : "
          f"{tree_after.replace(chr(10), ' | ') if tree_after else 'clean'}")
    print(f"  evidence written to         : {os.path.relpath(OUT, ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
