#!/usr/bin/env python3
"""Capture once, use twice — the structural guarantees behind the owner's correction.

The supervisor must never upload, select or describe the same evidence twice. These
checks assert the parts of that promise the repository can actually hold: that the
normal description is optional, that project and location stay trusted structured
fields, that AI output is advisory, that quantitative and contractual fields cannot
originate from image analysis, that no public image link is required, and that the
CAP-01 acceptance requirement is present and reachable.

They do NOT prove that any capture platform can perform a native multi-file share.
That is CAP-GATE, a real-device test in Phase 2A.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Checks

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Fields a contract or a bill can rest on. None of them may be written by image analysis.
QUANTITATIVE_OR_CONTRACTUAL = [
    ("VisitActivities", "Quantity"), ("VisitActivities", "PercentComplete"),
    ("VisitActivities", "UnitID"), ("VisitActivities", "ActivityTypeID"),
    ("BOQItems", "ContractQuantity"), ("BOQItems", "UnitRate"),
    ("InvoiceLines", "Quantity"), ("InvoiceLines", "UnitRate"),
    ("Contracts", "ContractValue"), ("TaxRules", "RatePercent"),
]

# The nine inferences the owner ruled out, in the owner's own order.
FORBIDDEN_INFERENCES = [
    "measured quantity", "hidden defect", "material brand", "compliance",
    "completion percentage", "exact project or location", "responsibility",
    "date", "executed the visible work",
]


def col(tables, tname, cname):
    if tname not in tables:
        return None
    for c in tables[tname]["columns"]:
        if c["name"] == cname:
            return c
    return None


def run(model, data):
    cap = model.get("capture_once")
    tables = model["tables"]
    c = Checks("Capture once, use twice",
               "The evidence is captured exactly once; the description is optional; AI proposes "
               "and a human decides; trusted context never comes from a photograph; no public "
               "link is required.")

    c.check("CAP-01", "The capture-once acceptance requirement is present in the canonical model",
            cap and cap["acceptance"]["id"] == "CAP-01"
            and "second time" in cap["acceptance"]["statement"],
            cap["acceptance"]["statement"] if cap else "capture_once block absent")
    if not cap:
        return c

    # ---- the description is optional -------------------------------------------------
    c.check("CAP-02", "A written description is not mandatory for a normal submission",
            cap["optional_note"]["description_mandatory_for_normal_submission"] is False,
            cap["optional_note"]["statement"])

    not_optional = []
    for ref in cap["optional_note"]["fields"]:
        tn, cn = ref.split(".")
        col_ = col(tables, tn, cn)
        if col_ is None or col_["required"]:
            not_optional.append(ref)
    c.check("CAP-03", "Every declared description field is optional in the model",
            not not_optional,
            "all optional" if not not_optional else f"required: {not_optional}")

    c.check("CAP-04", "An optional site note exists, with a category vocabulary for facts a "
                      "photograph cannot establish",
            col(tables, "SiteVisits", "AdditionalSiteNote") is not None
            and len(cap["optional_note"]["categories"]) >= 10,
            f"{len(cap['optional_note']['categories'])} categories")

    c.check("CAP-05", "The exceptional workflows that DO require a written reason are named",
            len(cap["optional_note"]["mandatory_exceptions"]) >= 3,
            f"{len(cap['optional_note']['mandatory_exceptions'])} exceptions declared")

    # ---- project and location stay trusted structured fields -------------------------
    untrusted = []
    for ref in cap["trusted_context_fields"]:
        tn, cn = ref.split(".")
        col_ = col(tables, tn, cn)
        if col_ is None or col_.get("src") == "ai" or col_.get("advisory"):
            untrusted.append(ref)
    c.check("CAP-06", "Project, location, date, assignee and activity are trusted system fields, "
                      "never AI-sourced",
            not untrusted, "all trusted" if not untrusted else f"compromised: {untrusted}")

    for tn, cn in [("SiteVisits", "ProjectID"), ("SiteVisits", "LocationID")]:
        col_ = col(tables, tn, cn)
        c.check(f"CAP-07/{cn}", f"{tn}.{cn} is a structured reference, not free text",
                col_ is not None and col_["type"] == "ref" and col_["required"],
                f"type={col_['type'] if col_ else 'missing'}")

    # ---- AI output is advisory --------------------------------------------------------
    hashed_ai = []
    for tname, t in tables.items():
        hashset = set(t["content_hash_fields"])
        for column in t["columns"]:
            if column.get("src") == "ai" and column["name"] in hashset:
                hashed_ai.append(f"{tname}.{column['name']}")
    c.check("CAP-08", "No AI-sourced column binds an approval: none appears in a content hash",
            not hashed_ai, "none" if not hashed_ai else f"bound: {hashed_ai}")

    proposals = [p["column"] for p in cap["ai_proposes"]]
    missing = [r for r in proposals if col(tables, *r.split(".")) is None]
    c.check("CAP-09", "Every field the AI proposes exists as its own advisory column",
            not missing, f"{len(proposals)} proposal columns"
            if not missing else f"missing: {missing}")

    not_advisory = []
    for ref in proposals:
        col_ = col(tables, *ref.split("."))
        if col_ and not (col_.get("advisory") or col_.get("src") == "ai"):
            not_advisory.append(ref)
    c.check("CAP-10", "Every proposal column is marked advisory or AI-sourced",
            not not_advisory, "all advisory" if not not_advisory else str(not_advisory))

    c.check("CAP-11", "The proposal is separate from the confirmed value: proposed stage and "
                      "confirmed stage are different columns",
            col(tables, "Photos", "AIProposedEvidenceStage") is not None
            and col(tables, "Photos", "EvidenceStage") is not None
            and col(tables, "Photos", "EvidenceStage").get("src") == "user",
            "AIProposedEvidenceStage proposes; EvidenceStage is set by the supervisor")

    c.check("CAP-12", "A human disposition is recorded for every proposal",
            (col(tables, "Photos", "AIProposalDisposition") or {}).get("src") == "user",
            "Photos.AIProposalDisposition is user-sourced")

    # ---- quantitative and contractual fields cannot come from the image ---------------
    leaked = []
    for tn, cn in QUANTITATIVE_OR_CONTRACTUAL:
        col_ = col(tables, tn, cn)
        if col_ and (col_.get("src") == "ai" or col_.get("advisory")):
            leaked.append(f"{tn}.{cn}")
    c.check("CAP-13", "No quantitative or contractual field is sourced from image analysis",
            not leaked, f"{len(QUANTITATIVE_OR_CONTRACTUAL)} fields checked"
            if not leaked else f"leaked: {leaked}")

    closed = []
    for ref in cap["forbidden_ai_written_columns"]:
        col_ = col(tables, *ref.split("."))
        if col_ is None or col_.get("src") == "ai":
            closed.append(ref)
    c.check("CAP-14", "Every column declared closed to AI is genuinely not AI-sourced",
            not closed, f"{len(cap['forbidden_ai_written_columns'])} columns closed"
            if not closed else f"open: {closed}")

    text = " ".join(cap["ai_must_not_infer"]).lower()
    absent = [f for f in FORBIDDEN_INFERENCES if f not in text]
    c.check("CAP-15", "All nine forbidden inferences are declared in the model",
            not absent, f"{len(cap['ai_must_not_infer'])} declared"
            if not absent else f"absent: {absent}")

    # ---- no public link, no unofficial automation -------------------------------------
    share = cap["sharing"]
    c.check("CAP-16", "No public image link is required, and none is permitted",
            share["public_link_required"] is False and share["public_link_permitted"] is False,
            "native share sheet carries the files themselves")

    forbidden = " ".join(share["forbidden_methods"]).lower()
    c.check("CAP-17", "Unofficial messaging automation and group scraping are forbidden by the "
                      "model, not only by prose",
            "whatsapp web" in forbidden and "scraping" in forbidden,
            share["forbidden_methods"][0])

    c.check("CAP-18", "Re-selecting the files is itself a declared forbidden method",
            any("select the files again" in m for m in share["forbidden_methods"]),
            "a retry re-uses stored evidence")

    # ---- both modes capture exactly once ---------------------------------------------
    for mode, spec in cap["modes"].items():
        c.check(f"CAP-19/{mode}", f"{mode} captures the evidence exactly once and ends at a "
                                  f"native share",
                spec["capture_count"] == 1 and spec["sequence"][-1] == "native share",
                " -> ".join(spec["sequence"]))

    # ---- the evidence is stored once and re-used --------------------------------------
    c.check("CAP-20", "Photographs carry a capture batch and a sequence, so the share and the "
                      "report re-use one stored set",
            col(tables, "Photos", "CaptureBatchID") is not None
            and col(tables, "Photos", "CaptureSequence") is not None,
            "CaptureBatchID + CaptureSequence")

    c.check("CAP-21", "A share attempt is counted and recoverable without re-capture",
            col(tables, "SiteVisits", "ShareAttemptCount") is not None
            and col(tables, "SiteVisits", "ShareStatus") is not None,
            "ShareStatus records cancelled and failed as recoverable states")

    c.check("CAP-22", "The share destination is a label, never a telephone number or invitation "
                      "link",
            "NEVER a telephone number" in (col(tables, "SiteVisits", "ShareTargetLabel")
                                           or {}).get("note", ""),
            "ShareTargetLabel is project configuration")

    # ---- the gate is declared unverified, with a fallback -----------------------------
    gate = cap["platform_gate"]
    c.check("CAP-23", "The AppSheet native-share requirement is recorded as UNVERIFIED, with a "
                      "test matrix",
            gate["status"].startswith("UNVERIFIED") and len(gate["test_matrix"]) >= 15,
            f"{len(gate['test_matrix'])} test conditions")

    c.check("CAP-24", "A capture-platform fallback exists, and the backend is declared re-usable "
                      "if the interface changes",
            len(gate["fallback_options"]) >= 3 and "re-usable" in gate["invariant"],
            gate["fallback_options"][1])

    # ---- the requirement is present in the documentation, not only in the model -------
    hits = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "docs")):
        for fn in filenames:
            if fn.endswith(".md"):
                body = open(os.path.join(dirpath, fn), encoding="utf-8").read()
                if "CAP-01" in body:
                    hits.append(os.path.relpath(os.path.join(dirpath, fn), ROOT))
    c.check("CAP-25", "The CAP-01 acceptance requirement appears in the documentation the owner "
                      "reads, not only in the model",
            len(hits) >= 3, f"{len(hits)} documents cite CAP-01")

    # ---- no document may still demand a mandatory description ------------------------
    # A regression guard. It must stay sensitive: seeding the pattern into any document
    # has to fail this check, which is why the exclusions are exact phrases, not "not".
    demands = re.compile(
        r"(work |overall |site )?description[^.\n]{0,30}\b(is|are|must be|remains?)\b"
        r"[^.\n]{0,20}\b(mandatory|required|compulsory)\b"
        r"|\bmandatory\b[^.\n]{0,20}(work |overall |site )?description", re.I)
    allowed = ("superseded", "no longer", "not mandatory", "never mandatory", "withdrawn",
               "only in the declared", "optional")
    stale = []
    scanned = 0
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "docs")):
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            scanned += 1
            for i, line in enumerate(open(path, encoding="utf-8"), 1):
                low = line.lower()
                if demands.search(line) and not any(a in low for a in allowed):
                    stale.append(f"{os.path.relpath(path, ROOT)}:{i}")
    c.check("CAP-26", "No surviving document still makes the work description mandatory",
            not stale, f"{scanned} documents scanned" if not stale else f"stale: {stale}")

    return c


if __name__ == "__main__":
    import json
    m = json.load(open(os.path.join(ROOT, "model", "model.json"), encoding="utf-8"))
    res = run(m, None)
    for r in res.results:
        print(("PASS " if r["passed"] else "FAIL ") + r["id"], "-", r["description"], "|",
              r["detail"])
    print(f"{res.passed} passed, {res.failed} failed")
