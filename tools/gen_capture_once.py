#!/usr/bin/env python3
"""Generate the capture-once workflow specification from model/model.json.

The owner's operational correction of 2026-09-11: the supervisor must never upload,
select or describe the same evidence twice. That rule lives in the canonical model
(`capture_once`), so this document cannot drift away from what the checks test.
"""
import datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modeldef

OUT = os.path.join(modeldef.ROOT, "docs", "02a-plan", "24-capture-once-workflow.md")
TODAY = datetime.date.today().isoformat()

ACTOR = {"supervisor": "Supervisor", "system": "System", "ai": "AI (advisory)"}


def main():
    m = modeldef.load()
    cap = m["capture_once"]
    o = []
    w = o.append

    w("# Capture Once, Use Twice — Field Workflow Specification")
    w("")
    w("**Document ID:** AH-SYS-P2A-024 · **Revision:** 1 · **Status:** generated — do not hand-edit")
    w(f"**Generated:** {TODAY} from `model/model.json` by `tools/gen_capture_once.py`")
    w("**Authority:** the owner's operational correction of 2026-09-11 (decisions D-16 to D-21)")
    w("")
    w("> This document is generated from the canonical model. The automated checks in")
    w("> `tools/test_capture_once.py` test the same block, so the specification and the tests")
    w("> cannot disagree.")
    w("")
    w("## 1. The principle")
    w("")
    w(f"**{cap['principle']}**")
    w("")
    w(f"### {cap['acceptance']['id']} — the acceptance requirement")
    w("")
    w(f"> **{cap['acceptance']['statement']}**")
    w("")
    w("It applies to every one of these, not only the first share:")
    w("")
    for a in cap["acceptance"]["applies_to"]:
        w(f"- {a}")
    w("")
    w(f"**If the platform cannot meet it:** {cap['acceptance']['on_failure']}")
    w("")
    w("## 2. The workflow")
    w("")
    w("| Step | Actor | Action | Where the fact comes from |")
    w("|---|---|---|---|")
    for s in cap["workflow"]:
        extra = s.get("source") or s.get("constraint") or ""
        if s.get("binding") == "advisory":
            extra = "Advisory only. Binds nothing, approves nothing."
        elif s.get("binding") == "authoritative":
            extra = "The human decision. This is what the record carries."
        w(f"| {s['step']} | {ACTOR[s['actor']]} | {s['action']} | {extra} |")
    w("")
    w("**Step 4 is the only file selection in the entire workflow.** Steps 8 and 9 both re-use")
    w("what step 5 stored.")
    w("")
    w("## 3. The two operating modes")
    w("")
    w("| Mode | Sequence | AI | Use when | Times the evidence is captured |")
    w("|---|---|---|---|---|")
    for name, spec in cap["modes"].items():
        w(f"| **{name}** | {' → '.join(spec['sequence'])} | {spec['ai']} | {spec['use_when']} | "
          f"**{spec['capture_count']}** |")
    w("")
    w("Both modes end at the native share sheet, and both capture exactly once. The difference is")
    w("only whether the AI proposal is waited for.")
    w("")
    w("## 4. The written description is optional")
    w("")
    w(f"> **{cap['optional_note']['statement']}**")
    w("")
    w("These fields are optional by design, and the checks fail if any of them becomes required:")
    w("")
    for f in cap["optional_note"]["fields"]:
        w(f"- `{f}`")
    w("")
    w("### What the optional note is for")
    w("")
    w("Facts a photograph cannot establish. `SiteVisits.SiteNoteCategory` carries the vocabulary:")
    w("")
    w("| Code | Meaning |")
    w("|---|---|")
    for v in m["enums"]["SiteNoteCategory"]["values"]:
        w(f"| `{v['code']}` | {v['label_en']}"
          + (f" — {v['description']}" if v["description"] else "") + " |")
    w("")
    w("**Future input methods** for the same field, not new fields: "
      + ", ".join(cap["optional_note"]["future_input_methods"]) + ".")
    w("")
    w("### The exceptional workflows that DO require a written reason")
    w("")
    for e in cap["optional_note"]["mandatory_exceptions"]:
        w(f"- {e}")
    w("")
    w("Everything outside this list is a normal photographic submission, and a normal")
    w("photographic submission needs no typed description.")
    w("")
    w("## 5. What the AI proposes")
    w("")
    w("Every item below is a **proposal** written to its own advisory column. None of them is")
    w("ever written to the confirmed field, and none enters a content hash, so an analysis")
    w("arriving later can never void a human approval.")
    w("")
    w("| What is proposed | Advisory column |")
    w("|---|---|")
    for p in cap["ai_proposes"]:
        w(f"| {p['item']} | `{p['column']}` |")
    w("")
    w("**Evidence stage vocabulary:** "
      + ", ".join(f"`{v}`" for v in cap["ai_proposes"][1]["vocabulary"]) + ".")
    w("")
    w("The supervisor's response is recorded in `Photos.AIProposalDisposition` — "
      + ", ".join(f"`{v['code']}`" for v in m["enums"]["AIProposalDisposition"]["values"])
      + " — so a confirmation is always distinguishable from a correction.")
    w("")
    w("## 6. What the AI must not infer")
    w("")
    w("AI may describe only visually supportable conditions and activities. It must not infer or")
    w("confirm:")
    w("")
    for i in cap["ai_must_not_infer"]:
        w(f"- {i}")
    w("")
    w("### Trusted context comes from system data, never from the photograph")
    w("")
    for f in cap["trusted_context_fields"]:
        w(f"- `{f}`")
    w("")
    w(f"### The {len(cap['forbidden_ai_written_columns'])} columns closed to AI by declaration")
    w("")
    w("Checked by `CAP-14`. If any of these is ever changed to an AI source, the validation suite")
    w("fails:")
    w("")
    w("| Column | Why it is closed |")
    w("|---|---|")
    reasons = {
        "ProjectID": "Contractual identity. Comes from the assignment.",
        "LocationID": "Structured reference. A photograph cannot name a location reliably.",
        "VisitDate": "Trusted metadata or a human correction, never a guess.",
        "SupervisorUserID": "Attribution. Comes from the signed-in user.",
        "WorkflowStatus": "A state machine, not an opinion.",
        "ActivityTypeID": "A contractual activity. Advisory text exists separately.",
        "Quantity": "Quantitative. Feeds a certificate and eventually an invoice.",
        "PercentComplete": "Quantitative and contractual.",
        "UnitID": "Determines what a quantity means.",
        "EvidenceStage": "The supervisor's assertion about what the photograph shows.",
        "CaptionEN": "The supervisor's own words.",
        "CaptionAR": "The supervisor's own words.",
        "ReviewerDecision": "A human review decision.",
        "ApprovedForReport": "Derived from a human decision.",
        "Severity": "A judgement with commercial consequence.",
        "Decision": "An approval. Only a named person approves.",
    }
    for ref in cap["forbidden_ai_written_columns"]:
        w(f"| `{ref}` | {reasons.get(ref.split('.')[1], 'Trusted structured data.')} |")
    w("")
    w("## 7. Sharing to the main-contractor group")
    w("")
    sh = cap["sharing"]
    w(f"**Method:** {sh['method']}. **Payload:** {sh['payload']}.")
    w("")
    w("| Rule | Value |")
    w("|---|---|")
    w(f"| A public link is required | **{'Yes' if sh['public_link_required'] else 'No'}** |")
    w(f"| A public link is permitted | **{'Yes' if sh['public_link_permitted'] else 'No'}** |")
    w("")
    w("**Forbidden methods:**")
    w("")
    for f_ in sh["forbidden_methods"]:
        w(f"- {f_}")
    w("")
    w("**Recorded as:** " + ", ".join(f"`{r}`" for r in sh["recorded_as"]) + ".")
    w("")
    w(f"> **An honest limit.** {sh['honest_limit']}")
    w("")
    w("## 8. The platform gate — unverified")
    w("")
    g = cap["platform_gate"]
    w(f"**{g['id']}:** {g['question']}")
    w("")
    w(f"**Status: {g['status']}**")
    w("")
    w(f"### The {len(g['test_matrix'])} conditions that must be tested on real devices")
    w("")
    w("| # | Condition |")
    w("|---|---|")
    for i, t in enumerate(g["test_matrix"], 1):
        w(f"| {i} | {t} |")
    w("")
    w(f"**The workflow fails acceptance if the supervisor must select or upload the images a")
    w("second time.** No duplicate-upload workaround will be implemented. If AppSheet cannot meet")
    w("the requirement, the decision comparison is between:")
    w("")
    for i, opt in enumerate(g["fallback_options"], 1):
        w(f"{i}. {opt}")
    w("")
    w(f"> **{g['invariant']}**")
    w("")
    w("This is why the capture platform is an interface decision and not an architecture")
    w("decision: the canonical model, the security filters, the approval binding, the numbering")
    w("contract and the audit trail are all defined independently of it.")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(o) + "\n")
    print(f"wrote {os.path.relpath(OUT, modeldef.ROOT)}: {len(cap['workflow'])} steps, "
          f"{len(cap['platform_gate']['test_matrix'])} device test conditions")


if __name__ == "__main__":
    main()
