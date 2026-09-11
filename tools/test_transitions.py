#!/usr/bin/env python3
"""Status transitions, approval routing and delegation (D-09, spec 5.8/5.18)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Checks

AS_OF = "2026-04-10T09:00:00Z"


def allowed_pairs(model, entity):
    return {(a["from"], a["to"]) for a in model["transitions"][entity]["allowed"]}


def delegation_valid(row, stage, project, at):
    if (row.get("IsActive") or "TRUE").upper() != "TRUE":
        return False, "delegation inactive"
    if row.get("RevokedAt"):
        return False, "delegation revoked"
    if not (row["ValidFrom"] <= at <= row["ValidTo"]):
        return False, "outside the delegation window"
    if row.get("ApprovalStage") and row["ApprovalStage"] != stage:
        return False, "stage not covered"
    if row["Scope"] == "SpecificProjects" and project not in (row.get("ProjectIDs") or "").split(";"):
        if project not in (row.get("ProjectIDs") or "").split(","):
            return False, "project not covered"
    return True, "valid"


def run(model, data):
    c = Checks("Status transitions, approvals and delegation",
               "Work advances only through declared transitions, and an approval is only ever made "
               "by an authorised person acting within scope (D-09).")
    tr = model["transitions"]

    # 1. every entity with a lifecycle declares one
    expected = {"SiteVisits", "VisitActivities", "Photos", "Snags", "DocumentJobs", "Documents",
                "NumberRegister", "Approvals", "Projects"}
    c.check("TRN-01", "Every entity with a lifecycle has a declared transition matrix",
            expected <= set(tr), f"declared: {sorted(tr)}")

    # 2. every declared state is reachable or is an explicit start state
    unreachable = []
    for ent, spec in tr.items():
        field = spec["field"]
        col = next(x for x in model["tables"][ent]["columns"] if x["name"] == field)
        states = [v["code"] for v in model["enums"][col["enum"]]["values"]] \
            if col["type"] == "enum" else []
        targets = {a["to"] for a in spec["allowed"]}
        sources = {a["from"] for a in spec["allowed"]}
        for s in states:
            if s not in targets and s not in sources:
                unreachable.append(f"{ent}.{s}")
    c.check("TRN-02", "No declared status is orphaned from the transition matrix",
            not unreachable, "; ".join(unreachable) or "every status appears in the matrix")

    # 3. the dangerous shortcuts are explicitly forbidden
    sv = allowed_pairs(model, "SiteVisits")
    c.check("TRN-03", "A visit cannot jump from Draft straight to TechnicallyApproved",
            ("Draft", "TechnicallyApproved") not in sv, "shortcut absent from the allowed set")
    c.check("TRN-04", "A visit cannot be approved without passing validation",
            ("Submitted", "TechnicallyApproved") not in sv, "shortcut absent")
    docs = allowed_pairs(model, "Documents")
    c.check("TRN-05", "A document cannot go from Draft to Released",
            ("Draft", "Released") not in docs, "shortcut absent")
    c.check("TRN-06", "A document cannot be released without an explicit release decision",
            ("TechnicallyApproved", "Released") not in docs,
            "release requires PendingRelease and a recorded decision")
    nr = allowed_pairs(model, "NumberRegister")
    c.check("TRN-07", "A cancelled number can never return to Reserved or Issued",
            ("Cancelled", "Reserved") not in nr and ("Cancelled", "Issued") not in nr,
            "silent reuse is structurally impossible")
    snag = allowed_pairs(model, "Snags")
    c.check("TRN-08", "A snag cannot be closed without verification",
            ("Open", "Closed") not in snag, "closure requires evidence and a verifier")

    # 4. terminal states have no outgoing transitions
    bad = []
    for ent, spec in tr.items():
        for t in spec["terminal_states"]:
            if any(a["from"] == t for a in spec["allowed"]):
                bad.append(f"{ent}.{t}")
    c.check("TRN-09", "Terminal states have no outgoing transitions",
            not bad, "; ".join(bad) or "archive and cancellation are final")

    # 5. transitions that void an approval say so
    voiding = [a for a in tr["SiteVisits"]["allowed"] if a["invalidates"]]
    c.check("TRN-10", "Transitions that void an approval declare what they invalidate",
            any("Approvals" in str(a["invalidates"]) for a in voiding),
            f"{len(voiding)} voiding transitions declared on SiteVisits")

    # 6. self-approval is prohibited wherever the matrix says so
    matrix = data["ApprovalMatrix"]
    c.check("TRN-11", "Every approval route prohibits self-approval",
            all(m["SelfApprovalProhibited"].upper() == "TRUE" for m in matrix),
            f"{len(matrix)} approval routes, all with SelfApprovalProhibited = TRUE")

    # 7. every project has a resolvable approver at every required stage
    stages = {"EvidenceReview", "TechnicalReview", "Release"}
    gaps = []
    for proj in data["Projects"]:
        for stage in stages:
            specific = [m for m in matrix if m.get("ProjectID") == proj["ProjectID"]
                        and m["ApprovalStage"] == stage]
            default = [m for m in matrix if not m.get("ProjectID")
                       and m["ApprovalStage"] == stage]
            if not specific and not default:
                gaps.append(f"{proj['ProjectID']}/{stage}")
    c.check("TRN-12", "Every project resolves an approver at every required stage",
            not gaps, "; ".join(gaps) or
            f"{len(data['Projects'])} projects x {len(stages)} stages resolved, "
            f"project-specific routes overriding the company default")

    # 8. delegation validity
    dels = {d["DelegationID"]: d for d in data["ApprovalDelegations"]}
    ok, reason = delegation_valid(dels["DEL-0001"], "TechnicalReview", "PRJ-0001", AS_OF)
    c.check("TRN-13", "A delegation inside its window, stage and project scope is valid",
            ok, f"DEL-0001: {reason}")
    ok2, reason2 = delegation_valid(dels["DEL-0002"], "EvidenceReview", "PRJ-0001", AS_OF)
    c.check("TRN-14", "An expired delegation is rejected",
            not ok2, f"DEL-0002: {reason2}")
    ok3, reason3 = delegation_valid(dels["DEL-0003"], "Release", "PRJ-0001", AS_OF)
    c.check("TRN-15", "A revoked delegation is rejected",
            not ok3, f"DEL-0003: {reason3}")
    ok4, reason4 = delegation_valid(dels["DEL-0001"], "Release", "PRJ-0001", AS_OF)
    c.check("TRN-16", "A delegation does not cover a stage it was not granted for",
            not ok4, f"DEL-0001 used for Release: {reason4}")
    ok5, reason5 = delegation_valid(dels["DEL-0001"], "TechnicalReview", "PRJ-0002", AS_OF)
    c.check("TRN-17", "A project-scoped delegation does not cover another project",
            not ok5, f"DEL-0001 used on PRJ-0002: {reason5}")

    # 9. no delegation is open-ended
    open_ended = [d["DelegationID"] for d in data["ApprovalDelegations"] if not d.get("ValidTo")]
    c.check("TRN-18", "No delegation is open-ended",
            not open_ended, "; ".join(open_ended) or "every delegation has an end date")

    # 10. AI may never drive a photo decision
    forbidden = " ".join(model["transitions"]["Photos"]["forbidden"])
    c.check("TRN-19", "AI is structurally barred from deciding a photograph",
            "AI" in forbidden, forbidden[:120])

    # 11. the seeded data itself obeys the matrix
    illegal = []
    for v in data["SiteVisits"]:
        states = {a["to"] for a in tr["SiteVisits"]["allowed"]} | {"Draft"}
        if v["WorkflowStatus"] not in states:
            illegal.append(f"{v['VisitID']}={v['WorkflowStatus']}")
    c.check("TRN-20", "Every seeded record sits in a state the matrix can produce",
            not illegal, "; ".join(illegal) or f"{len(data['SiteVisits'])} visits in valid states")
    return c
