#!/usr/bin/env python3
"""Generate the AppSheet implementation workbook and security-filter specification.

Both are derived from model/model.json, so the app specification cannot drift from the
data foundation it is built on. Expressions are written in AppSheet's expression language
but NOTHING is connected: this is a specification for Phase 2, not a deployment.
"""
import datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modeldef

OUT = os.path.join(modeldef.ROOT, "docs", "02a-plan")
TODAY = datetime.date.today().isoformat()

# The tables the application actually carries come from the lean MVP manifest in the
# model, so this specification and the scope decision can never disagree.
def mvp_tables(model):
    return list(model["lean_mvp"]["tables"])

TYPE_MAP = {
    "id": "Text", "text": "Text", "longtext": "LongText", "email": "Email", "phone": "Phone",
    "uuid": "Text", "checksum": "Text", "filekey": "Text", "url": "Url", "enum": "Enum",
    "ref": "Ref", "date": "Date", "datetime": "DateTime", "time": "Time", "json": "LongText",
    "bool": "Yes/No", "int": "Number", "decimal": "Decimal",
}

# Hand-authored expressions for the columns where the behaviour matters most.
EXPRESSIONS = {
    ("SiteVisits", "VisitID"): ("UNIQUEID()", "initial value, key, not editable"),
    ("SiteVisits", "ProjectID"): (
        'IN([_THIS], SELECT(ProjectAssignments[ProjectID],\n'
        '   AND([UserID] = LOOKUP(USEREMAIL(), Users, Email, UserID),\n'
        '       [IsActive] = TRUE,\n'
        '       [MaySubmitEvidence] = TRUE,\n'
        '       [AssignedFrom] <= TODAY(),\n'
        '       OR(ISBLANK([AssignedTo]), [AssignedTo] >= TODAY()))))',
        "Valid_If. The dropdown offers only projects the signer is actively assigned to, and the "
        "same expression re-validates on save"),
    ("SiteVisits", "LocationID"): (
        'FILTER("Locations", AND([ProjectID] = [_THISROW].[ProjectID], [IsActive] = TRUE))',
        "Valid_If. Locations depend on the chosen project (spec 7.3)"),
    ("SiteVisits", "VisitDate"): ("TODAY()", "initial value; editable by an authorised user"),
    ("SiteVisits", "SupervisorUserID"): (
        'LOOKUP(USEREMAIL(), Users, Email, UserID)',
        "initial value; not editable. Identity comes from the signed-in user, never typed"),
    ("SiteVisits", "WorkflowStatus"): (
        '"Draft"', "initial value; not editable by a field role. Status moves only through actions"),
    ("SiteVisits", "EndTime"): (
        'OR(ISBLANK([StartTime]), ISBLANK([_THIS]), [_THIS] > [StartTime])',
        "Valid_If"),
    ("VisitActivities", "ActivityTypeID"): (
        'FILTER("ActivityTypes",\n'
        '   IN([ActivityTypeID], SELECT(ProjectActivityRules[ActivityTypeID],\n'
        '      AND([ProjectID] = [_THISROW].[ProjectID], [IsPermitted] = TRUE))))\n'
        '+ FILTER("ActivityTypes",\n'
        '   NOT(IN([ActivityTypeID], SELECT(ProjectActivityRules[ActivityTypeID],\n'
        '      [ProjectID] = [_THISROW].[ProjectID]))))',
        "Valid_If. Activities explicitly permitted for the project, plus any with no project rule "
        "at all (which inherit the global catalogue)"),
    ("VisitActivities", "Quantity"): (
        'OR(ISBLANK([_THIS]), [_THIS] >= 0)', "Valid_If. Non-negative"),
    ("VisitActivities", "PercentComplete"): (
        'OR(ISBLANK([_THIS]), AND([_THIS] >= 0, [_THIS] <= 100))', "Valid_If"),
    ("Photos", "CaptionEN"): (
        'OR(IN([_THISROW].[EvidenceStage], LIST("Before","During","After","Equipment","Other")),\n'
        '   NOT(ISBLANK([_THIS])), NOT(ISBLANK([_THISROW].[CaptionAR])))',
        "Valid_If. A caption is mandatory for Snag, Observation, Material and Safety evidence, in "
        "either language"),
    ("Photos", "ReceivedAt"): ("NOW()", "initial value; not editable. Anchors the write-once guarantee"),
    ("Photos", "CapturedBy"): ("LOOKUP(USEREMAIL(), Users, Email, UserID)", "initial value; not editable"),
    ("Photos", "ReviewerDecision"): (
        '"Pending"',
        "initial value. Editable ONLY by a reviewer role; never by AI and never by the uploader"),
    ("Photos", "ApprovedForReport"): (
        '([ReviewerDecision] = "Approved")',
        "app formula, so it can never be set independently of the human decision"),
    ("Snags", "ClosureEvidencePhotoID"): (
        'OR([Status] <> "Closed", NOT(ISBLANK([_THIS])))',
        "Required_If equivalent. A snag cannot be closed on assertion alone"),
}

EDITABLE_NEVER = {"system", "integration", "calculation", "ai"}


def appsheet_type(col, model):
    t = TYPE_MAP.get(col["type"], "Text")
    if col["type"] == "ref":
        return f"Ref → {col['ref'].split('.')[0]}"
    if col["type"] == "enum":
        vals = [v["code"] for v in model["enums"][col["enum"]]["values"]]
        shown = ", ".join(vals[:4]) + ("…" if len(vals) > 4 else "")
        return f"Enum ({shown})"
    return t


def workbook(model):
    o, w = [], None
    w = o.append
    w("# AppSheet Implementation Workbook")
    w("")
    w("**Document ID:** AH-SYS-P2A-001 · **Revision:** 1 · **Status:** generated — do not hand-edit")
    w(f"**Generated:** {TODAY} from `model/model.json` by `tools/gen_appsheet_workbook.py`")
    w("")
    w("> **Nothing here is connected.** This is the specification an implementer follows in Phase 2,")
    w("> derived from the canonical model so the app cannot drift from the data foundation.")
    w("> Expressions are written in AppSheet's expression language and have **not** been executed")
    w("> on the platform — see `12-appsheet-feature-to-plan-matrix.md`, where the platform's")
    w("> capabilities remain UNVERIFIED.")
    w("")
    lean = model["lean_mvp"]
    w("## Workbook structure")
    w("")
    w("One worksheet per table, named exactly as the table. Header row exactly as the column names")
    w("in the data dictionary. No formulas in cells: every derivation is an app formula or a")
    w("virtual column, so the store stays a store.")
    w("")
    w(f"**{len(lean['tables'])} worksheets** are built (the lean operational MVP). The remaining")
    w(f"{len(model['tables']) - len(lean['tables'])} tables of the reference architecture are")
    w("designed and deferred; adding one later is additive, never a migration. Scope and rationale:")
    w("[`11-lean-mvp-scope.md`](11-lean-mvp-scope.md).")
    w("")
    w("### Lean replacements")
    w("")
    w("Where a lean table would otherwise require a deferred one, a replacement column carries the")
    w("job instead:")
    w("")
    w("| Reference-architecture column | Lean replacement | Carries |")
    w("|---|---|---|")
    for key, v in lean.get("column_overrides", {}).items():
        w(f"| `{key}` | `{v['lean_column']}` ({v['lean_type']}) | {v['note']} |")
    w("")
    w("## Column conventions")
    w("")
    w("| Convention | Rule |")
    w("|---|---|")
    w("| Key | The table's primary key column. `UNIQUEID()` as initial value, never editable |")
    w("| Label | The first bilingual name column, so references display readably |")
    w("| `Editable_If` | `FALSE` for every column whose source is system, integration, calculation or AI |")
    w("| `Required_If` | Mirrors the model's required flag, plus any conditional rule stated in the dictionary |")
    w("| `Valid_If` | Mirrors the model's validation and referential rules |")
    w("| Sensitivity | Columns marked financial or personal are omitted entirely from field-role slices, not merely hidden |")
    w("")
    for tname in mvp_tables(model):
        t = model["tables"][tname]
        w(f"## {tname}")
        w("")
        w(f"{t['description_en']}")
        w("")
        w(f"**Key:** `{t['primary_key']}` · **Scope:** {t['scope']} · "
          f"**Sensitivity:** {t['sensitivity']}")
        w("")
        w("| Column | AppSheet type | Required | Editable | Expression / rule |")
        w("|---|---|---|---|---|")
        for c in t["columns"]:
            key = (tname, c["name"])
            editable = "No" if c.get("src") in EDITABLE_NEVER else "Yes"
            req = "Yes" if c.get("required") else ""
            if key in EXPRESSIONS:
                expr, note = EXPRESSIONS[key]
                rule = f"`{expr.replace(chr(10), ' ')}` — {note}"
            elif c.get("key") == "pk":
                rule = "`UNIQUEID()` initial value; key; not editable"
            elif c.get("validation"):
                rule = c["validation"]
            elif c.get("default") is not None:
                rule = f"Initial value `{c['default']}`"
            else:
                rule = ""
            if c.get("sens"):
                rule = (rule + " " if rule else "") + f"**[{c['sens']}]**"
            w(f"| `{c['name']}` | {appsheet_type(c, model)} | {req} | {editable} | "
              f"{rule.replace('|', chr(92) + '|')} |")
        w("")
    w("---")
    w("")
    w("## Key expressions in full")
    w("")
    w("Reproduced unwrapped, because these are the ones where a transcription error would be a")
    w("security or data-integrity defect rather than a cosmetic one.")
    w("")
    for (tname, cname), (expr, note) in EXPRESSIONS.items():
        w(f"### `{tname}.{cname}`")
        w("")
        w(f"*{note}*")
        w("")
        w("```")
        w(expr)
        w("```")
        w("")
    return "\n".join(o) + "\n"


def security_filters(model):
    sec = model["security"]
    o = []
    w = o.append
    w("# Security Filter Specification")
    w("")
    w("**Document ID:** AH-SYS-P2A-002 · **Revision:** 1 · **Status:** generated — do not hand-edit")
    w(f"**Generated:** {TODAY} from `model/model.json` by `tools/gen_appsheet_workbook.py`")
    w("")
    w("> Security filters are the **enforcement** layer, not the presentation layer. Views, slices")
    w("> and column visibility control what is shown; a security filter controls what is delivered")
    w("> to the device at all. Every state-changing automation re-validates the same rule")
    w("> server-side, because a client-side check can never be trusted for security (P-04).")
    w("")
    w("## The building blocks")
    w("")
    w("```")
    w("ME()            = LOOKUP(USEREMAIL(), Users, Email, UserID)")
    w("MY_ROLE()       = LOOKUP(USEREMAIL(), Users, Email, RoleID)")
    w("MY_PROJECTS()   = SELECT(ProjectAssignments[ProjectID],")
    w("                     AND([UserID] = ME(),")
    w("                         [IsActive] = TRUE,")
    w("                         [AssignedFrom] <= TODAY(),")
    w("                         OR(ISBLANK([AssignedTo]), [AssignedTo] >= TODAY())))")
    w("MY_GRANT()      = SELECT(TemporaryAccessGrants[GrantID],")
    w("                     AND([UserID] = ME(), [IsActive] = TRUE,")
    w("                         ISBLANK([RevokedAt]),")
    w("                         [ValidFrom] <= NOW(), [ValidTo] >= NOW(),")
    w("                         NOT(ISBLANK([Reason])),")
    w("                         OR([GrantKind] <> \"Emergency\",")
    w("                            NOT(ISBLANK([NotificationSentAt])))))")
    w("```")
    w("")
    w("`MY_PROJECTS()` is the whole access model in five lines: an assignment that is inactive, has")
    w("not started, or has ended contributes nothing.")
    w("")
    w("## Filter per table")
    w("")
    w("`ROLE_IN(...)` abbreviates `IN(LOOKUP(USEREMAIL(), Users, Email, RoleID), LIST(...))`.")
    w("")
    w("| Table | Security filter | Rationale |")
    w("|---|---|---|")
    grant_roles = sec.get("grant_required_roles", [])
    for tname in mvp_tables(model):
        t = model["tables"][tname]
        # roles by the scope they hold on this table
        by_scope = {}
        for role in sec["roles"]:
            by_scope.setdefault(sec["matrix"][role][tname]["read"], []).append(role)
        alls = [r for r in by_scope.get("all", []) if r not in grant_roles]
        granted = [r for r in by_scope.get("all", []) if r in grant_roles]
        assigned = by_scope.get("assigned", [])
        own = by_scope.get("own", [])
        parts = []
        if alls:
            parts.append(f'ROLE_IN("{chr(34) + ", " + chr(34)}".join)'.replace(
                'ROLE_IN("", "".join)', "") or "")
        clauses = []
        if alls:
            clauses.append("ROLE_IN(" + ", ".join(f'"{r}"' for r in alls) + ")")
        if granted:
            clauses.append("AND(ROLE_IN(" + ", ".join(f'"{r}"' for r in granted)
                           + "), COUNT(MY_GRANT()) > 0)")
        if assigned:
            if t["scope"] == "project":
                clauses.append("AND(ROLE_IN(" + ", ".join(f'"{r}"' for r in assigned)
                               + "), IN([ProjectID], MY_PROJECTS()))")
            else:
                clauses.append("ROLE_IN(" + ", ".join(f'"{r}"' for r in assigned) + ")")
        if own:
            owner_col = {"SiteVisits": "SupervisorUserID", "Photos": "CapturedBy",
                         "Snags": "RaisedBy", "Users": "UserID"}.get(tname, "CreatedBy")
            clauses.append("AND(ROLE_IN(" + ", ".join(f'"{r}"' for r in own)
                           + f"), [{owner_col}] = ME())")
        expr = "FALSE" if not clauses else ("OR(" + ", ".join(clauses) + ")"
                                            if len(clauses) > 1 else clauses[0])
        reason = []
        if granted:
            reason.append("grant-dependent roles read nothing without an active grant")
        if assigned and t["scope"] == "project":
            reason.append("assignment-scoped")
        if own:
            reason.append("own rows only")
        if not clauses:
            reason.append("no role reads this table in the MVP app")
        w(f"| `{tname}` | `{expr}` | {'; '.join(reason) or 'company-wide reference data'} |")
    w("")
    w("## Tables deliberately absent from the application")
    w("")
    w("These are not filtered — they are **not present in the app's data set at all**, which is the")
    w("strongest form of the control: data that is not there cannot leak.")
    w("")
    for tname in sorted(set(model["tables"]) - set(mvp_tables(model))):
        t = model["tables"][tname]
        w(f"- `{tname}` — {t['description_en']}")
    w("")
    w("## Verification required in Phase 2")
    w("")
    w("Every filter above is a **specification**. None has been executed on AppSheet. The Phase 2")
    w("gate must record, for each of these, an attempted access from an unassigned account through")
    w("a view, a search, a deep link and the API — with the result recorded either way.")
    return "\n".join(o) + "\n"


def main():
    m = modeldef.load()
    os.makedirs(OUT, exist_ok=True)
    for name, text in (("01-appsheet-workbook.md", workbook(m)),
                       ("02-security-filter-specification.md", security_filters(m))):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote docs/02a-plan/{name}")


if __name__ == "__main__":
    main()
