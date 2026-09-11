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

    # --- release 1: the controlled prototype ---
    r1 = lean.get("release_1", {})
    r1_set = set(r1.get("tables", []))
    c.check("LEAN-14", "Release 1 is exactly twelve tables",
            len(r1_set) == 12, f"{len(r1_set)} tables: {', '.join(r1.get('tables', []))}")
    c.check("LEAN-15", "Every release-1 table is part of the lean MVP",
            r1_set <= lean_set, f"outside the lean set: {sorted(r1_set - lean_set) or 'none'}")

    r1_hard = []
    for t in sorted(r1_set):
        for col in tables[t]["columns"]:
            if col["type"] == "ref" and col.get("required"):
                target = col["ref"].split(".")[0]
                if target not in r1_set and f"{t}.{col['name']}" not in overrides:
                    key = f"{t}.{col['name']} -> {target}"
                    folded = any(target in k for k in r1.get("consolidations", {}))
                    if not folded:
                        r1_hard.append(key)
    c.check("LEAN-16", "No release-1 table requires a table that release 1 does not have",
            not r1_hard, "; ".join(r1_hard) or
            f"{len(r1_set)} tables, every mandatory reference resolved or explicitly folded")

    survives_r1 = {"ProjectAssignments": "segregation", "Approvals": "review decisions",
                   "AuditLog": "audit trail", "IntegrationJobs": "integration failure visibility",
                   "Photos": "evidence", "Snags": "corrective actions"}
    lost_r1 = [v for k, v in survives_r1.items() if k not in r1_set]
    c.check("LEAN-17", "Release 1 keeps segregation, review, audit and failure visibility",
            not lost_r1, "; ".join(lost_r1) or ", ".join(sorted(survives_r1.values())))

    thin_r1 = [k for k, v in r1.get("consolidations", {}).items()
               if len(v.get("cost", "")) < 25 or len(v.get("rule", "")) < 20]
    c.check("LEAN-18", "Every release-1 consolidation states its rule and its cost",
            not thin_r1, "; ".join(thin_r1) or
            f"{len(r1.get('consolidations', {}))} consolidations, each explained")

    c.check("LEAN-19", "Release 1 produces no document, so it carries no document or numbering table",
            not ({"Documents", "DocumentJobs", "NumberRegister", "LegalEntities"} & r1_set),
            "document generation arrives in release 1b: "
            + ", ".join(r1.get("adds_in_release_1b", [])))

    # nothing is both lean and deferred
    both = sorted(lean_set & accounted)
    c.check("LEAN-12", "No table is listed as both built and deferred",
            not both, "; ".join(both) or "the two lists are disjoint")
    return c
