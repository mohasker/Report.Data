#!/usr/bin/env python3
"""Generate the release-1 scope and field-exposure analysis from model/model.json.

Answers the owner's question directly: how many fields exist in storage, how many
reach a phone, how many a field user ever sees, how many a reviewer sees, how many are
generated rather than typed, and how many are administrative only.
"""
import datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modeldef

OUT = os.path.join(modeldef.ROOT, "docs", "02a-plan", "21-release-1-twelve-tables.md")
TODAY = datetime.date.today().isoformat()

AUTO_SOURCES = {"system", "integration", "calculation", "ai"}
# Tables whose rows reach a field device at all
SYNCS_TO_DEVICE = {"Users", "Projects", "ProjectAssignments", "Locations", "ActivityTypes",
                   "SiteVisits", "VisitActivities", "Photos", "Snags"}
ADMIN_ONLY_TABLES = {"AuditLog", "IntegrationJobs", "Approvals"}
# The fields a supervisor actually touches on the normal form
FIELD_FORM = {
    "SiteVisits": ["ProjectID", "LocationID", "VisitDate", "OverallDescriptionEN",
                   "OverallDescriptionAR", "SafetyObservation"],
    "VisitActivities": ["ActivityTypeID", "DescriptionEN", "Quantity", "PercentComplete"],
    "Photos": ["EvidenceStage", "CaptionEN", "CaptionAR"],
}
REVIEWER_EXTRA = {
    "SiteVisits": ["RejectionReason"],
    "VisitActivities": ["TechnicalReviewerComment", "Status"],
    "Photos": ["ReviewerDecision", "ReviewerComment", "ReportSequence", "AIObservation",
               "AIConfidence", "AIContradictsCaption"],
    "Snags": ["Severity", "Status", "ResponsibleParty", "TargetDate", "ClosureDate",
              "ClosureEvidencePhotoID"],
}


def classify(model, tables):
    """Return per-table counts across the exposure classes."""
    rows = []
    for t in tables:
        cols = model["tables"][t]["columns"]
        total = len(cols)
        auto = sum(1 for c in cols if c.get("src") in AUTO_SOURCES)
        sensitive = sum(1 for c in cols if c.get("sens") in ("financial", "personal"))
        syncs = total if t in SYNCS_TO_DEVICE else 0
        admin = total if t in ADMIN_ONLY_TABLES else 0
        field_form = len(FIELD_FORM.get(t, []))
        reviewer = field_form + len(REVIEWER_EXTRA.get(t, []))
        rows.append({"table": t, "total": total, "auto": auto, "typed": total - auto,
                     "sensitive": sensitive, "syncs": syncs, "admin": admin,
                     "field_form": field_form, "reviewer": reviewer})
    return rows


def main():
    m = modeldef.load()
    r1 = m["lean_mvp"]["release_1"]
    tables = r1["tables"]
    rows = classify(m, tables)
    total = sum(r["total"] for r in rows)
    auto = sum(r["auto"] for r in rows)
    syncs = sum(r["syncs"] for r in rows)
    admin = sum(r["admin"] for r in rows)
    field_form = sum(r["field_form"] for r in rows)
    reviewer = sum(r["reviewer"] for r in rows)

    o, w = [], None
    w = o.append
    w("# Release 1 — Twelve Tables, and What Reaches a Field User")
    w("")
    w("**Document ID:** AH-SYS-P2A-021 · **Revision:** 1 · **Status:** generated — do not hand-edit")
    w(f"**Generated:** {TODAY} from `model/model.json` by `tools/gen_release1_scope.py`")
    w("")
    w("> **Storage field counts come from the canonical model.** Exposure counts come from the")
    w("> declared form and view design, which is a specification and has not been built.")
    w("")
    w("## 1. The twelve tables")
    w("")
    w("Release 1 is **capture and review only**. It produces no document, so it carries no")
    w("document, numbering or legal-entity table.")
    w("")
    w("| # | Table | Fields | Of which generated | Typed by a person |")
    w("|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        w(f"| {i} | `{r['table']}` | {r['total']} | {r['auto']} | {r['typed']} |")
    w(f"| | **Total** | **{total}** | **{auto}** | **{total - auto}** |")
    w("")
    w("## 2. Consolidations, and what each costs")
    w("")
    w("| Folded away | Into | The rule | What it costs |")
    w("|---|---|---|---|")
    for k, v in r1["consolidations"].items():
        w(f"| `{k}` | {v['into']} | {v['rule']} | {v['cost']} |")
    w("")
    w(f"**Release 1b adds** {', '.join('`%s`' % t for t in r1['adds_in_release_1b'])} — the moment")
    w("report generation is switched on.")
    w("")
    w("## 3. Field exposure — the answer to \"do not deploy 377 fields to the field interface\"")
    w("")
    w("| Measure | Fields | What it means |")
    w("|---|---|---|")
    w(f"| **Total in the release-1 storage model** | **{total}** | Every column across twelve tables, including audit columns |")
    w(f"| Of which **generated, never typed** | **{auto}** | System, integration or AI sourced. A person never sees a keyboard for these |")
    w(f"| **Synchronised to a field device** | **{syncs}** | Only from the nine tables a supervisor's phone holds at all |")
    w(f"| **Administrative only** | **{admin}** | Approvals, audit log and integration log. **Absent from the field data set entirely** |")
    w(f"| **On the normal field form** | **{field_form}** | What a supervisor actually fills in |")
    w(f"| **Visible to a reviewer** | **{reviewer}** | The supervisor's fields plus the review controls |")
    w("")
    w("**An honest caveat on the sync number.** A row synchronises whole: if a table is in a")
    w(f"user's data set, all its columns travel, which is why {syncs} is larger than the")
    w(f"{field_form} on the form. Views and slices control what is *shown*, not what is")
    w("*delivered*. The two levers that genuinely reduce the sync payload are keeping a table out")
    w("of the field role's data set altogether — which is what puts Approvals, the audit log and")
    w("the integration log at zero — and keeping row counts down through security filters. The")
    w("form size and the sync size are different problems with different fixes.")
    w("")
    w("### The normal field form, in full")
    w("")
    w("| Screen | Fields the supervisor touches |")
    w("|---|---|")
    for t, fields in FIELD_FORM.items():
        w(f"| {t} | {', '.join('`%s`' % f for f in fields)} |")
    w("")
    w(f"**{field_form} fields across three screens**, and several of those are pre-filled or")
    w("conditional: the project defaults, the date defaults, the Arabic description is an")
    w("alternative to the English one rather than an addition, the quantity appears only when the")
    w("activity rule requires it, and percent complete is optional.")
    w("")
    w(f"So of **{total}** fields in storage, a supervisor meets **{field_form}** — about")
    w(f"**{field_form / total * 100:.0f}%** — and types fewer than that on a normal visit.")
    w("")
    w("### Why the storage model is larger than the form")
    w("")
    w("| Category | Example | Why it exists |")
    w("|---|---|---|")
    w("| Audit columns | `CreatedAt`, `CreatedBy`, `UpdatedAt`, `UpdatedBy` | Four per table, generated. Attribution is the point of the audit trail |")
    w("| Keys and references | `VisitID`, `ProjectID`, `LocationID` | Generated or chosen from a dropdown, never typed |")
    w("| Integrity fields | `EntityVersion`, `ContentHash` | Generated. What an approval binds to |")
    w("| Evidence metadata | `OriginalChecksum`, `OriginalMimeType`, `ReceivedAt` | Captured by the system at registration |")
    w("| Advisory AI fields | `AIObservation`, `AIConfidence` | Written by analysis, read by a reviewer, typed by nobody |")
    w("| Review fields | `ReviewerDecision`, `ReviewerComment` | A reviewer's screen, not a supervisor's |")
    w("")
    w("## 4. Per-table exposure")
    w("")
    w("| Table | Fields | Syncs to device | Field form | Reviewer view | Admin only |")
    w("|---|---|---|---|---|---|")
    for r in rows:
        w(f"| `{r['table']}` | {r['total']} | {'Yes' if r['syncs'] else 'No'} | "
          f"{r['field_form'] or '—'} | {r['reviewer'] or '—'} | "
          f"{'**Yes**' if r['admin'] else 'No'} |")
    w("")
    w("## 5. What release 1 deliberately cannot do")
    w("")
    w("| Cannot | Because | Arrives in |")
    w("|---|---|---|")
    w("| Generate a report or certificate | No document, numbering or legal-entity table | Release 1b |")
    w("| Issue a document number | No numbering register | Release 1b |")
    w("| Release anything to a client | Nothing is generated to release | Release 1b |")
    w("| Delegate an approval | No delegation table; the general manager approves | Before go-live |")
    w("| Enforce residency in the app | Procedural, through the contract-review checklist | Phase 3 |")
    w("| Bill anything | No contract, BOQ, tax or invoice table | Phase 6 |")
    w("")
    w("Reports during release 1 are produced **manually from approved evidence**, exactly as they")
    w("are today. The system's contribution in release 1 is that the evidence behind them is")
    w("captured once, segregated by project, reviewed by a named person and recorded in an audit")
    w("trail — which is the part that does not exist today.")
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(o) + "\n")
    print(f"wrote {os.path.relpath(OUT, modeldef.ROOT)}: {total} fields, "
          f"{field_form} on the field form")


if __name__ == "__main__":
    main()
