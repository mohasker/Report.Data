#!/usr/bin/env python3
"""Generate the one-page lean MVP scope matrix from model/model.json.

Field counts come from the model, so they cannot drift. Row estimates come from the
stated volume assumptions and are arithmetic, not measurement.
"""
import datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modeldef

OUT = os.path.join(modeldef.ROOT, "docs", "02a-plan", "17-lean-table-scope-matrix.md")
TODAY = datetime.date.today().isoformat()

# purpose, primary user, rows per PROJECT per month (expected scenario), in app?, syncs to device?,
# deferrable?, depends on
PROFILE = {
    "Users":               ("Who may sign in, and in what default role", "Administrator", "0.2", "Yes", "Yes (small)", "No — nothing works without it", "-"),
    "Projects":            ("All project configuration; carries client display name in the lean build", "Business admin", "0.1", "Yes", "Yes (small)", "No", "LegalEntities"),
    "ProjectAssignments":  ("The only source of row-level access", "Administrator", "0.5", "Yes", "Yes (small)", "No — removing it removes segregation", "Users, Projects"),
    "Locations":           ("Hierarchical, project-scoped locations", "Business admin", "1", "Yes", "Yes", "No", "Projects, Locations (self)"),
    "ActivityTypes":       ("Catalogue of 34 activities and default evidence rules", "Business admin", "0.2", "Yes", "Yes (small)", "No", "-"),
    "ProjectActivityRules":("Per-project overrides of those rules", "Business admin", "1", "Yes", "Yes (small)", "Yes, at the cost of every project behaving identically", "Projects, ActivityTypes"),
    "SiteVisits":          ("One reporting event; the unit of submission and review", "Supervisor", "20", "Yes", "Yes", "No", "Projects, Locations, Users"),
    "VisitActivities":     ("What was done, quantity, supervisor confirmation", "Supervisor", "40", "Yes", "Yes", "No", "SiteVisits, ActivityTypes"),
    "Photos":              ("Write-once evidence, reviewer decision, advisory AI fields", "Supervisor, reviewer", "120", "Yes", "Yes — **the volume driver**", "No", "SiteVisits, VisitActivities"),
    "Snags":               ("Defects tracked to closure with evidence", "Supervisor, reviewer", "3", "Yes", "Yes", "Yes — a snag can be a photograph with a caption at first", "Photos, Locations"),
    "Approvals":           ("Every decision, bound to a content hash", "Reviewer, GM", "25", "Yes", "Reviewers only", "No — removing it removes the audit defence", "Users"),
    "DocumentJobs":        ("A report request with a frozen input snapshot", "GM, project manager", "1", "Yes", "No", "Yes, if reports stay manual at first", "Projects"),
    "Documents":           ("A produced revision, release-controlled", "GM", "1", "Yes", "No", "Yes, with DocumentJobs", "DocumentJobs, LegalEntities"),
    "NumberRegister":      ("Reserved / issued / cancelled document numbers, with reasons", "System", "1", "Read-only view", "No", "Only with Documents", "Documents, LegalEntities"),
    "LegalEntities":       ("Company identity printed on every issued document", "GM", "~0", "Admin view only", "No", "Only if no document is issued", "-"),
    "AuditLog":            ("Append-only record of every state transition", "System; auditor reads", "150", "Admin view only", "No", "No", "-"),
    "IntegrationJobs":     ("One row per external call, with failure class", "Administrator", "260", "Admin view only", "No", "Only while nothing is automated", "-"),
}


def main():
    m = modeldef.load()
    lean = m["lean_mvp"]["tables"]
    o, w = [], None
    w = o.append
    w("# Lean MVP Scope Matrix — 17 Tables, One Page")
    w("")
    w("**Document ID:** AH-SYS-P2A-017 · **Revision:** 1 · **Status:** generated — do not hand-edit")
    w(f"**Generated:** {TODAY} from `model/model.json` by `tools/gen_scope_matrix.py`")
    w("")
    w("> Field counts come from the canonical model and cannot drift. **Row estimates are")
    w("> arithmetic from the assumptions in [`14-storage-and-image-volume.md`](14-storage-and-image-volume.md)")
    w("> — expected scenario, per project per month. They are not measurements.**")
    w("")
    w("| # | Table | Purpose | Primary user | Fields | Rows /project /month | In the app | Syncs to device | Deferrable | Depends on |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    total_fields = 0
    total_rows = 0.0
    for i, t in enumerate(lean, 1):
        tbl = m["tables"][t]
        n = len(tbl["columns"])
        total_fields += n
        purpose, user, rows, in_app, syncs, deferrable, deps = PROFILE[t]
        try:
            total_rows += float(rows.replace("~", ""))
        except ValueError:
            pass
        w(f"| {i} | `{t}` | {purpose} | {user} | {n} | {rows} | {in_app} | {syncs} | {deferrable} | {deps} |")
    w(f"| | **17 tables** | | | **{total_fields}** | **~{int(total_rows)}** | | | | |")
    w("")
    w("## What the numbers say")
    w("")
    w(f"- **{total_fields} fields across 17 tables.** The reference architecture holds "
      f"{sum(len(x['columns']) for x in m['tables'].values())} fields across "
      f"{len(m['tables'])} tables; the rest is designed and deferred.")
    w(f"- **~{int(total_rows)} rows per project per month**, of which **120 are photographs** — "
      f"roughly {120 / total_rows * 100:.0f}% of all rows. Every capacity question is really a "
      f"question about photographs.")
    w("- **Only six tables sync to a field device**: Users, Projects, ProjectAssignments, "
      "Locations, ActivityTypes, ProjectActivityRules — plus the supervisor's own visits, "
      "activities and photographs. The five largest tables by growth never reach a phone in full.")
    w("- **Four tables are admin-only views**: NumberRegister, LegalEntities, AuditLog, "
      "IntegrationJobs. A field user's data set does not contain them.")
    w("")
    w("## What could still be cut, and what it would cost")
    w("")
    w("| Could be cut | Saves | Costs |")
    w("|---|---|---|")
    w("| `DocumentJobs` + `Documents` + `NumberRegister` | 3 tables, the whole report engine | "
      "Reports stay manual. **Capture and review still work** — this is the natural "
      "capture-only first release if the field test needs to come sooner |")
    w("| `Snags` | 1 table | Defects become photographs with captions; no tracking to closure |")
    w("| `ProjectActivityRules` | 1 table | Every project gets identical evidence rules |")
    w("| `LegalEntities` | 1 table | Only possible if no document is issued at all |")
    w("")
    w("**A capture-and-review-only first release is 12 tables.** That is the floor of the range "
      "the owner set, and it is a legitimate option if getting a phone into a supervisor's hand "
      "sooner matters more than producing the first monthly report from the system.")
    w("")
    w("## Sync load on a field device")
    w("")
    w("What a supervisor's phone actually holds, for one project, after one month, under the "
      "expected scenario:")
    w("")
    w("| Table | Rows on device | Note |")
    w("|---|---|---|")
    w("| Users | ~20 | Whole company; small |")
    w("| Projects | 1-3 | Only assigned projects |")
    w("| ProjectAssignments | ~5 | Only their own |")
    w("| Locations | ~30 | Only assigned projects |")
    w("| ActivityTypes | 34 | Whole catalogue; static |")
    w("| ProjectActivityRules | ~10 | Only assigned projects |")
    w("| SiteVisits | ~20/month | Their project, current period |")
    w("| VisitActivities | ~40/month | |")
    w("| Photos | ~120/month | **Metadata only.** Image bytes stream from storage, not from the row |")
    w("| Snags | ~3/month | Open ones |")
    w("")
    w("**Roughly 280 rows after a month, 3,400 after a year on one project.** The sync cost is "
      "manageable; the growth risk is the shared Photos table across all projects, which is what "
      "the migration thresholds in "
      "[`18-migration-threshold-strategy.md`](18-migration-threshold-strategy.md) watch.")
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(o) + "\n")
    print(f"wrote {os.path.relpath(OUT, modeldef.ROOT)}")


if __name__ == "__main__":
    main()
