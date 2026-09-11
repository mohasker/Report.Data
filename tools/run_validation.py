#!/usr/bin/env python3
"""Regenerate Phase 1 artifacts, run every check, and write the validation evidence.

    python3 tools/run_validation.py

Standard library only. No network, no credential, no external service. The evidence
document records the result of each check whether it passed or failed, because a record
that only ever says PASS is not evidence.
"""
import datetime, io, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

import modeldef                                                   # noqa: E402
import validate_seed                                              # noqa: E402
from harness import Checks                                        # noqa: E402
import test_segregation, test_numbering, test_calculations        # noqa: E402
import test_contenthash, test_transitions, test_bilingual         # noqa: E402
import test_evidence_rules, test_configurability, test_governance  # noqa: E402

SUITES = [test_configurability, test_segregation, test_evidence_rules, test_transitions,
          test_contenthash, test_numbering, test_calculations, test_bilingual, test_governance]
OUT = os.path.join(ROOT, "docs", "01-data-foundation", "17-validation-evidence.md")


def regenerate():
    lines = []
    for script in ("build_model.py", "gen_schemas.py", "gen_data_dictionary.py",
                   "gen_matrices.py"):
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
    gen = regenerate()
    model = modeldef.load()
    seed_checks, data = seed_suite(model)
    suites = [seed_checks] + [m.run(model, data) for m in SUITES]

    total = sum(len(s.results) for s in suites)
    failed = sum(s.failed for s in suites)

    out = io.StringIO()
    w = out.write
    w("# Phase 1 Validation Evidence\n\n")
    w("**Document ID:** AH-SYS-P1-017 · **Revision:** 1 · **Status:** generated from an executed run\n")
    w(f"**Executed:** {started.strftime('%Y-%m-%d %H:%M UTC')} · "
      f"**Model version:** {model['model_version']} · "
      f"**Python:** {sys.version.split()[0]}\n\n")
    w("> Produced by `python3 tools/run_validation.py`. Every result below comes from code that\n")
    w("> actually ran; nothing here is asserted by hand. Re-run the command to reproduce it.\n\n")
    w("## What this run does and does not prove\n\n")
    w("**It proves** that the Phase 1 data foundation is internally consistent: the model, the\n")
    w("generated schemas and the data dictionary agree; the synthetic data conforms; the rules for\n")
    w("segregation, evidence, transitions, delegation, hashing, numbering, calculation and\n")
    w("bilingual handling behave as specified when executed against that data.\n\n")
    w("**It does not prove** that any built system works. No AppSheet app, Google Drive folder,\n")
    w("Make scenario, Claude call or QuickBooks connection exists or was contacted. Those are\n")
    w("Phase 2 and later, and will carry their own recorded evidence (D-14).\n\n")
    w(f"## Summary — {total - failed} of {total} checks passed\n\n")
    w("| Suite | Checks | Passed | Failed |\n|---|---|---|---|\n")
    for s in suites:
        w(f"| {s.group} | {len(s.results)} | {s.passed} | "
          f"{'**' + str(s.failed) + '**' if s.failed else '0'} |\n")
    w(f"| **Total** | **{total}** | **{total - failed}** | "
      f"**{failed}** |\n\n")
    if failed:
        w(f"> **{failed} check(s) failed. Phase 1 is not complete until they pass or the owner "
          f"accepts them explicitly.**\n\n")
    else:
        w("> Every check passed. Each is listed below with the evidence it produced, so a reviewer\n")
        w("> can see what was actually measured rather than taking a summary on trust.\n\n")
    w("## Artifact regeneration\n\n")
    w("| Step | Result | Output |\n|---|---|---|\n")
    for script, code, output in gen:
        w(f"| `{script}` | {'ok' if code == 0 else 'FAILED'} | "
          f"{output.replace(chr(10), '; ')} |\n")
    w("\n")
    for s in suites:
        w(f"## {s.group}\n\n{s.purpose}\n\n")
        w("| Check | Result | Description | Evidence |\n|---|---|---|---|\n")
        for r in s.results:
            detail = r["detail"].replace("|", "\\|").replace("\n", " ")
            if len(detail) > 300:
                detail = detail[:297] + "..."
            w(f"| `{r['id']}` | {'PASS' if r['passed'] else '**FAIL**'} | "
              f"{r['description']} | {detail} |\n")
        w("\n")
    w("---\n\n")
    w("## Reproducing this run\n\n")
    w("```\npython3 tools/run_validation.py\n```\n\n")
    w("No installation, no dependency, no network access and no credential is required.\n")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(out.getvalue())

    print(f"\n{'=' * 68}")
    for s in suites:
        print(f"  {s.group:<42} {s.passed:>3} passed  {s.failed:>2} failed")
    print(f"{'=' * 68}")
    print(f"  TOTAL {total - failed}/{total} checks passed")
    print(f"  evidence written to {os.path.relpath(OUT, ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
