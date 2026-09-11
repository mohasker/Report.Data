#!/usr/bin/env python3
"""The lean operational MVP is buildable, self-consistent, and loses nothing by design.

The owner's instruction of 2026-09-11: keep the 46-table model as the long-term
reference architecture, and build roughly 12-18 tables first. These checks confirm the
subset actually holds together — that no lean table depends on a deferred one without a
stated fold-in, and that every deferred table keeps its schema so adding it later is
additive rather than a migration.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Checks

# The capability the owner listed, and the lean table that carries it.
REQUIRED_CAPABILITIES = {
    "Projects and users": ["Projects", "Users"],
    "Project assignments": ["ProjectAssignments"],
    "Locations": ["Locations"],
    "Site visits": ["SiteVisits"],
    "Activities": ["VisitActivities", "ActivityTypes"],
    "Photographs": ["Photos"],
    "Snags": ["Snags"],
    "Reviews and approvals": ["Approvals"],
    "Document jobs": ["DocumentJobs"],
    "Generated reports": ["Documents"],
    "Audit and integration errors": ["AuditLog", "IntegrationJobs"],
}


def run(model, data):
    lean = model["lean_mvp"]
    tables = model["tables"]
    lean_set = set(lean["tables"])
    c = Checks("Lean operational MVP",
               "A 12-18 table subset is built first, the 46-table model stays the reference "
               "architecture, and every deferred table keeps a schema so adding it later is "
               "additive.")

    lo, hi = lean["target_range"]
    c.check("LEAN-01", "The lean MVP is within the size the owner asked for",
            lo <= len(lean_set) <= hi,
            f"{len(lean_set)} tables (target {lo}-{hi}); {len(tables) - len(lean_set)} deferred")

    missing = [cap for cap, req in REQUIRED_CAPABILITIES.items()
               if not set(req) <= lean_set]
    c.check("LEAN-02", "Every capability the owner listed is carried by a lean table",
            not missing, "; ".join(missing) or
            f"all {len(REQUIRED_CAPABILITIES)} listed capabilities covered")

    # a lean table may only REQUIRE a deferred one where a lean replacement column is declared
    overrides = lean.get("column_overrides", {})
    hard, replaced = [], []
    for t in sorted(lean_set):
        for col in tables[t]["columns"]:
            if col["type"] != "ref" or not col.get("required"):
                continue
            target = col["ref"].split(".")[0]
            if target in lean_set:
                continue
            key = f"{t}.{col['name']}"
            if key in overrides:
                replaced.append(f"{key} -> {overrides[key]['lean_column']}")
            else:
                hard.append(f"{key} -> {target}")
    c.check("LEAN-03", "Every required reference to a deferred table has a declared lean "
                       "replacement column",
            not hard, "; ".join(hard) or
            f"{len(replaced)} replacements declared: {'; '.join(replaced)}")

    thin_over = [k for k, v in overrides.items()
                 if not v.get("lean_column") or len(v.get("note", "")) < 20]
    c.check("LEAN-13", "Every lean replacement names its column and explains what it carries",
            not thin_over, "; ".join(thin_over) or
            f"{len(overrides)} overrides, each with a named column and a stated consequence")

    # optional references to deferred tables are allowed, but must be known about
    soft = sorted({col["ref"].split(".")[0] for t in lean_set for col in tables[t]["columns"]
                   if col["type"] == "ref" and not col.get("required")
                   and col["ref"].split(".")[0] not in lean_set})
    c.check("LEAN-04", "Optional references to deferred tables are identified, so they can be "
                       "left empty in the lean build",
            True, f"columns pointing at deferred tables, all optional: {', '.join(soft) or 'none'}")

    # every deferred table is accounted for: either folded in, or scheduled to a phase
    accounted = set()
    for key in lean["fold_ins"]:
        accounted |= {x.strip() for x in key.split(",")}
    accounted |= set(lean["deferred_phases"])
    deferred = set(tables) - lean_set
    unaccounted = sorted(deferred - accounted)
    c.check("LEAN-05", "Every deferred table is either folded into a lean table or scheduled "
                       "to a named phase",
            not unaccounted, "; ".join(unaccounted) or
            f"{len(deferred)} deferred tables, all accounted for")

    # each fold-in states its cost and when to restore it
    thin = [k for k, v in lean["fold_ins"].items()
            if len(v.get("cost", "")) < 25 or len(v.get("restore_when", "")) < 15]
    c.check("LEAN-06", "Every fold-in states what is lost and when the table returns",
            not thin, "; ".join(thin) or
            f"{len(lean['fold_ins'])} fold-ins, each with a stated cost and a restore trigger")

    # deferring never destroys a design
    schemaless = [t for t in deferred if not tables[t]["columns"]]
    c.check("LEAN-07", "Every deferred table keeps its full schema, so returning it is additive",
            not schemaless, f"{len(deferred)} deferred tables retain "
                            f"{sum(len(tables[t]['columns']) for t in deferred)} designed columns")

    # the controls that must survive the trim
    survives = {
        "Project segregation": "ProjectAssignments",
        "Approval bound to content": "Approvals",
        "Audit trail": "AuditLog",
        "Numbering register with cancellation reasons": "NumberRegister",
        "Legal entity identity on documents": "LegalEntities",
        "Per-project evidence rules": "ProjectActivityRules",
        "Integration failure visibility": "IntegrationJobs",
    }
    lost = [k for k, v in survives.items() if v not in lean_set]
    c.check("LEAN-08", "Every load-bearing control survives the trim",
            not lost, "; ".join(lost) or
            "segregation, approval binding, audit, numbering register, legal identity, "
            "evidence rules and failure visibility all retained")

    # project scoping still holds across the lean subset
    unscoped = [t for t in lean_set
                if tables[t]["scope"] == "project"
                and "ProjectID" not in {col["name"] for col in tables[t]["columns"]}]
    c.check("LEAN-09", "Every project-scoped lean table still carries ProjectID",
            not unscoped, "; ".join(unscoped) or "row-level security is unaffected by the trim")

    # content hashing survives
    hashable = [t for t in lean_set if tables[t]["content_hash_fields"]]
    c.check("LEAN-10", "Content hashing survives in the lean subset",
            len(hashable) >= 3, f"hashable lean tables: {', '.join(sorted(hashable))}")

    # the deferred delegation cost is stated honestly rather than hidden
    delegation = lean["fold_ins"].get("ApprovalDelegations", {})
    c.check("LEAN-11", "The cost of deferring delegation is stated plainly, not glossed",
            "approver is away" in delegation.get("cost", "").lower()
            or "stop" in delegation.get("cost", "").lower(),
            delegation.get("cost", "")[:160])

    # nothing is both lean and deferred
    both = sorted(lean_set & accounted)
    c.check("LEAN-12", "No table is listed as both built and deferred",
            not both, "; ".join(both) or "the two lists are disjoint")
    return c
