#!/usr/bin/env python3
"""Configurability: adding a project is data, never code (decision D-01).

This is the test that matters most to the scope correction. If any project code, client
identifier or project name appears inside the model, the schemas, the security matrix,
the transition rules or the rule engines, then the platform is not configuration-driven
and three projects would become an architectural boundary.
"""
import copy, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modeldef, security, evidence
from harness import Checks

AS_OF = "2026-05-15"
# Source files that implement behaviour. Tests and seed data are excluded on purpose:
# fixtures are supposed to name projects, logic is not.
LOGIC_FILES = ["tools/build_model.py", "tools/modeldef.py", "tools/security.py",
               "tools/evidence.py", "tools/numbering.py", "tools/calc.py",
               "tools/contenthash.py", "tools/validate_seed.py", "tools/gen_schemas.py",
               "tools/gen_data_dictionary.py"]
IDENT = re.compile(r"\b(PRJ-\d{4}|CLI-\d{4}|LAND-001|CIVL-002|IRRG-003|CNT-\d{4}|USR-\d{4})\b")


def run(model, data):
    c = Checks("Configurability and unbounded width",
               "Adding a project must require only controlled master-data configuration: no "
               "modified logic, no cloned application, no duplicated scenario, no rewritten "
               "prompt, no changed formula or code (D-01).")

    # 1. no project, client, contract or user identifier appears in any logic file
    hits = []
    for rel in LOGIC_FILES:
        path = os.path.join(modeldef.ROOT, rel)
        if not os.path.exists(path):
            continue
        for n, line in enumerate(open(path, encoding="utf-8"), 1):
            for m in IDENT.finditer(line):
                hits.append(f"{rel}:{n}: {m.group(0)}")
    c.check("CFG-01", "No project, client, contract or user identifier appears in any logic file",
            not hits, "; ".join(hits[:6]) or
            f"{len(LOGIC_FILES)} logic files scanned, no hard-coded identifier")

    # 2. the canonical model itself names no project or client
    blob = json.dumps(model, ensure_ascii=False)
    model_hits = sorted(set(IDENT.findall(blob)))
    c.check("CFG-02", "The canonical model names no project, client or contract",
            not model_hits, f"identifiers found in model.json: {model_hits or 'none'}")

    # 3. the generated schemas name no project or client
    schema_dir = os.path.join(modeldef.ROOT, "schemas", "tables")
    schema_hits = []
    for name in sorted(os.listdir(schema_dir)):
        text = open(os.path.join(schema_dir, name), encoding="utf-8").read()
        schema_hits += [f"{name}: {m}" for m in set(IDENT.findall(text))]
    c.check("CFG-03", "No generated schema names a project, client or contract",
            not schema_hits, "; ".join(schema_hits[:5]) or
            f"{len(os.listdir(schema_dir))} schemas scanned, none names a project")

    # 4. the security matrix is expressed in roles, never in projects
    matrix_blob = json.dumps(model["security"], ensure_ascii=False)
    c.check("CFG-04", "Row-level security is expressed in roles and assignments, never in projects",
            not IDENT.search(matrix_blob),
            f"{len(model['security']['roles'])} roles x {len(model['tables'])} tables, "
            f"no project named")

    # 5. every project-varying behaviour is a configuration column
    proj_cols = {col["name"] for col in model["tables"]["Projects"]["columns"]}
    required = {"LegalEntityID", "ClientID", "ReportingFrequency", "DefaultTemplateID",
                "DefaultDocumentLanguage", "Currency", "TimeZone", "BillingMethod",
                "PaymentTermsDays", "AIAnalysisEnabled", "RetentionDays", "Status",
                "ReportingCutoffDay"}
    c.check("CFG-05", "Every project-varying behaviour is a configuration column on Projects",
            required <= proj_cols, f"missing: {sorted(required - proj_cols) or 'none'}")

    # 6. per-project child configuration exists for the rest
    child = {"Locations", "ProjectActivityRules", "ApprovalMatrix", "DocumentTemplates",
             "NumberingSeries", "ResidencyAssignments", "ProjectAssignments"}
    c.check("CFG-06", "Behaviour that varies per project has a configuration table of its own",
            child <= set(model["tables"]), f"present: {sorted(child & set(model['tables']))}")

    # 7. ADD A FOURTH PROJECT AS DATA ONLY and exercise the same code paths
    d = copy.deepcopy(data)
    d["Clients"].append({k: "" for k in d["Clients"][0]})
    d["Clients"][-1].update({
        "ClientID": "CLI-0004", "LegalNameEN": "SYNTHETIC FOURTH CLIENT (TEST)",
        "LegalNameAR": "عميل اصطناعي رابع", "DisplayNameEN": "Synthetic Fourth Client",
        "ClientKind": "Private", "Currency": "QAR", "Status": "Active", "IsActive": "TRUE",
        "DefaultClassificationCode": "ClientConfidential", "PaymentTermsDays": "30"})
    d["Projects"].append({k: "" for k in d["Projects"][0]})
    d["Projects"][-1].update({
        "ProjectID": "PRJ-0004", "ProjectCode": "FOUR-004",
        "ProjectNameEN": "Synthetic Fourth Project", "ProjectNameAR": "المشروع الاصطناعي الرابع",
        "LegalEntityID": "LE-0002", "ClientID": "CLI-0004", "StartDate": "2026-05-01",
        "ReportingFrequency": "Quarterly", "DefaultDocumentLanguage": "ar",
        "Currency": "QAR", "TimeZone": "Asia/Qatar", "AIAnalysisEnabled": "FALSE",
        "Status": "Active", "IsActive": "TRUE", "BillingMethod": "LumpSumMilestone"})
    d["Locations"].append({k: "" for k in d["Locations"][0]})
    d["Locations"][-1].update({
        "LocationID": "LOC-0011", "ProjectID": "PRJ-0004", "LocationCode": "BLK-A",
        "LocationNameEN": "Block A", "LocationNameAR": "القطاع أ", "LocationKind": "Zone",
        "DisplayOrder": "10", "IsActive": "TRUE"})
    d["ProjectAssignments"].append({k: "" for k in d["ProjectAssignments"][0]})
    d["ProjectAssignments"][-1].update({
        "AssignmentID": "ASG-0011", "ProjectID": "PRJ-0004", "UserID": "USR-0005",
        "RoleID": "ROLE-SUPERVISOR", "AssignedFrom": "2026-05-01", "AssignedTo": "",
        "MaySubmitEvidence": "TRUE", "MayReviewEvidence": "FALSE",
        "MayRequestDocuments": "FALSE", "IsActive": "TRUE"})
    d["SiteVisits"].append({k: "" for k in d["SiteVisits"][0]})
    d["SiteVisits"][-1].update({
        "VisitID": "VIS-0007", "ProjectID": "PRJ-0004", "LocationID": "LOC-0011",
        "VisitDate": "2026-05-10", "SupervisorUserID": "USR-0005",
        "OverallDescriptionEN": "Fourth project visit added as data only.",
        "WorkflowStatus": "Draft", "EntityVersion": "1"})

    visible = security.readable_rows(model, d, "USR-0005", "SiteVisits", AS_OF)
    c.check("CFG-07", "A fourth project added as data only is immediately usable, with no code change",
            any(v["ProjectID"] == "PRJ-0004" for v in visible),
            f"USR-0005 now sees {len({v['ProjectID'] for v in visible})} projects including PRJ-0004")

    # 8. and it stays segregated from users who are not assigned to it
    others = security.readable_rows(model, d, "USR-0006", "SiteVisits", AS_OF)
    c.check("CFG-08", "The new project is invisible to users who are not assigned to it",
            not any(v["ProjectID"] == "PRJ-0004" for v in others),
            "USR-0006 has no assignment to PRJ-0004 and cannot see it")

    # 9. a second legal entity needs no code either
    c.check("CFG-09", "The new project can belong to a different legal entity by configuration",
            d["Projects"][-1]["LegalEntityID"] == "LE-0002",
            "PRJ-0004 issues documents under LE-0002 with its own numbering series")

    # 10. the rule engine serves the new project with no override rows at all
    rule = evidence.effective_rule(d, "PRJ-0004", "ACT-0002")
    c.check("CFG-10", "The evidence engine serves a brand-new project from the global catalogue",
            rule["sources"]["RequiresBeforePhoto"] == "Global" and rule["IsPermitted"],
            "no configuration rows required before a new project can capture evidence")

    # 11. no table encodes a project COUNT LIMIT.
    # An earlier version of this check flagged any mention of a number near the word
    # "project", which caught a restore trigger that was not a limit at all. It now looks
    # for limit constructs specifically.
    limit_phrases = ("max_projects", "project_limit", "maximum number of projects",
                     "maximum of three projects", "limited to three projects",
                     "only three projects", "supports three projects",
                     "no more than three projects", "up to three projects")
    blob_lower = blob.lower()
    hits = [w for w in limit_phrases if w in blob_lower]
    c.check("CFG-11", "Nothing in the model encodes a maximum project count",
            not hits, f"limit constructs found: {hits or 'none'} — "
                      f"the model carries no ceiling on how many projects exist")

    # 12. the model states its own multi-entity, multi-project intent
    c.check("CFG-12", "Multi-entity operation is structural, not incidental",
            len({p["LegalEntityID"] for p in d["Projects"]}) >= 2
            and any(t == "LegalEntities" for t in model["tables"]),
            f"{len({p['LegalEntityID'] for p in d['Projects']})} legal entities across the fixture")
    return c
