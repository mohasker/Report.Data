#!/usr/bin/env python3
"""Governance rules that the model itself must enforce.

These are the operating rules expressed as assertions about the model and the
repository, so a later edit that quietly weakens one of them fails a check instead of
passing unnoticed.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modeldef
from harness import Checks

SECRET_PATTERNS = [
    (re.compile(r"(?i)\b(api[_-]?key|secret|password|passwd|client[_-]?secret|access[_-]?token)"
                r"\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+]{12,}"), "credential assignment"),
    (re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b"), "Google API key"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"), "provider secret key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"\bya29\.[0-9A-Za-z\-_]+"), "OAuth access token"),
    (re.compile(r"https://hook\.[a-z]+\.make\.com/[A-Za-z0-9]+"), "live webhook URL"),
]
ALLOWED_EMAIL_DOMAINS = {"synthetic.example", "pending.example", "alharam.qa",
                         "noreply@anthropic.com"}
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
SKIP_DIRS = {".git", "__pycache__"}


def repo_files():
    for root, dirs, files in os.walk(modeldef.ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith((".md", ".py", ".json", ".csv", ".txt", ".example", ".gitignore")):
                yield os.path.join(root, f)


def run(model, data):
    c = Checks("Governance and safety rules",
               "The operating rules the owner approved, expressed as assertions so that weakening "
               "one of them fails a check rather than passing unnoticed.")
    tables, matrix = model["tables"], model["security"]["matrix"]

    # 1. no secret anywhere in the repository
    found = []
    for path in repo_files():
        rel = os.path.relpath(path, modeldef.ROOT)
        if rel.startswith("tools/test_governance"):
            continue                                   # this file holds the patterns themselves
        text = open(path, encoding="utf-8", errors="replace").read()
        for pattern, label in SECRET_PATTERNS:
            if pattern.search(text):
                found.append(f"{rel}: {label}")
    c.check("GOV-01", "No credential, key, token or live webhook URL exists anywhere in the repository",
            not found, "; ".join(found) or "every file scanned, nothing matching a secret pattern")

    # 2. every email address is synthetic or a published company address
    bad = []
    for path in repo_files():
        rel = os.path.relpath(path, modeldef.ROOT)
        if rel.startswith("tools/test_governance"):
            continue
        for m in EMAIL.findall(open(path, encoding="utf-8", errors="replace").read()):
            domain = m.split("@")[-1].lower()
            if domain not in ALLOWED_EMAIL_DOMAINS and m.lower() not in ALLOWED_EMAIL_DOMAINS:
                bad.append(f"{rel}: {m}")
    c.check("GOV-02", "Every email address is synthetic, or the company's own published address",
            not bad, "; ".join(sorted(set(bad))[:5]) or
            "only @synthetic.example, @pending.example and the published company address appear")

    # 3. the legal entity is a pending placeholder, not a guess between two names
    le = data["LegalEntities"][0]
    c.check("GOV-03", "Legal identity is an explicit pending placeholder, never a guess (D-02)",
            "PENDING_VERIFICATION" in le["LegalNameEN"],
            f"LegalNameEN = {le['LegalNameEN']}")

    # 4. no tax classification is named anywhere in the seeded rules
    forbidden_words = ("zero-rated", "zero rated", "exempt", "out of scope")
    named = []
    for r in data["TaxRules"]:
        blob = " ".join(str(v) for v in r.values()).lower()
        named += [w for w in forbidden_words if w in blob]
    c.check("GOV-04", "No tax classification is named before written confirmation (D-08)",
            not named, f"classification words found: {named or 'none'}; "
                       f"treatment = {data['TaxRules'][0]['TreatmentLabel']}")

    # 5. an unconfirmed tax rule blocks production invoicing
    c.check("GOV-05", "The seeded tax rule is explicitly unconfirmed, so invoicing stays blocked",
            data["TaxRules"][0]["ConfirmedByAccountant"].upper() == "FALSE",
            "ConfirmedByAccountant = FALSE")

    # 6. delete is denied to every role on every table
    deletes = [f"{role}.{t}" for role, grants in matrix.items()
               for t, g in grants.items() if g.get("delete") != "none"]
    c.check("GOV-06", "No role may delete any row: history is evidence",
            not deletes, "; ".join(deletes[:5]) or
            f"{sum(len(g) for g in matrix.values())} grants, every delete denied")

    # 7. the audit log is append-only for everyone, including the administrator
    writable = [role for role, grants in matrix.items()
                if grants["AuditLog"]["update"] != "none" or grants["AuditLog"]["create"] != "none"]
    c.check("GOV-07", "The audit log is append-only for every role including SystemAdmin",
            not writable, f"roles able to alter the audit log: {writable or 'none'}")

    # 8. the administrator cannot manufacture an approval
    c.check("GOV-08", "An administrator cannot create or alter an approval",
            matrix["SystemAdmin"]["Approvals"]["create"] == "none"
            and matrix["SystemAdmin"]["Approvals"]["update"] == "none",
            "SystemAdmin holds read-only access to Approvals")

    # 9. AI fields exist but are excluded from every content hash
    ai_cols = [(t, col["name"]) for t, tbl in tables.items() for col in tbl["columns"]
               if col.get("src") == "ai"]
    hashed_ai = [f"{t}.{n}" for t, n in ai_cols if n in tables[t]["content_hash_fields"]]
    c.check("GOV-09", "No advisory AI field is part of any content hash (D-06, C-06)",
            ai_cols and not hashed_ai,
            f"{len(ai_cols)} AI fields, {len(hashed_ai)} in a hash")

    # 10. AI never owns a decision field
    decision_fields = {("Photos", "ReviewerDecision"), ("Photos", "ApprovedForReport"),
                       ("VisitActivities", "PercentComplete"), ("SiteVisits", "WorkflowStatus")}
    wrong = [f"{t}.{n}" for t, n in decision_fields
             if next(col for col in tables[t]["columns"] if col["name"] == n).get("src") == "ai"]
    c.check("GOV-10", "No decision or completion field is sourced from AI",
            not wrong, f"AI-sourced decision fields: {wrong or 'none'}")

    # 11. no monetary or quantity field is sourced from AI.
    # An advisory confidence score is numeric but is neither money nor a measured quantity,
    # so the rule is stated in terms of what the number MEANS, not merely its type.
    MONEY_WORDS = ("amount", "rate", "total", "subtotal", "quantity", "payable", "retention",
                   "discount", "tax", "value", "percentcomplete")
    money_ai = [f"{t}.{col['name']}" for t, tbl in tables.items() for col in tbl["columns"]
                if col.get("src") == "ai"
                and (tbl["sensitivity"] == "financial"
                     or any(w in col["name"].lower() for w in MONEY_WORDS))]
    c.check("GOV-11", "No monetary or measured-quantity field is sourced from AI (invariant I-4)",
            not money_ai,
            f"AI-sourced monetary or quantity fields: {money_ai or 'none'} "
            f"(AIConfidence is advisory metadata, not a measurement)")

    # 12. the write-once evidence contract is fully represented
    photo_cols = {col["name"] for col in tables["Photos"]["columns"]}
    required = {"OriginalFileKey", "OriginalChecksum", "ChecksumAlgorithm", "OriginalMimeType",
                "OriginalSizeBytes", "ReceivedAt", "CapturedBy", "DerivedFileKey",
                "IsOriginalDeviceImageVerified"}
    c.check("GOV-12", "The approved write-once evidence contract is fully represented (D-13)",
            required <= photo_cols, f"missing: {sorted(required - photo_cols) or 'none'}")

    # 13. no photograph claims to be a verified original device image before testing
    claimed = [p["PhotoID"] for p in data["Photos"]
               if p.get("IsOriginalDeviceImageVerified", "FALSE").upper() == "TRUE"]
    c.check("GOV-13", "No file is described as the original device image before device testing",
            not claimed, f"photographs claiming verification: {claimed or 'none'}")

    # 14. residency model is complete and unverified assignments are marked as such
    unverified = [r["ResidencyAssignmentID"] for r in data["ResidencyAssignments"]
                  if r["VerifiedFromContract"].upper() != "TRUE"]
    c.check("GOV-14", "Residency assignments exist and are marked unverified until a contract is read",
            data["ResidencyAssignments"] and unverified,
            f"{len(unverified)} of {len(data['ResidencyAssignments'])} assignments await contract review")

    # 15. a residency rule that forbids third-party AI is reflected on its project
    blocking = {r["ResidencyRequirementID"] for r in data["ResidencyRequirements"]
                if r["BlocksThirdPartyAI"].upper() == "TRUE"}
    affected = {a["ProjectID"] for a in data["ResidencyAssignments"]
                if a["ResidencyRequirementID"] in blocking and a.get("ProjectID")}
    disabled = {p["ProjectID"] for p in data["Projects"]
                if p["AIAnalysisEnabled"].upper() == "FALSE"}
    c.check("GOV-15", "A project restricted by a residency rule has AI analysis disabled",
            affected <= disabled, f"restricted: {sorted(affected)}; disabled: {sorted(disabled)}")

    # 16. financial sensitivity is declared, not implied
    fin_tables = [t for t, tbl in tables.items() if tbl["sensitivity"] == "financial"]
    c.check("GOV-16", "Financial tables are declared as such so access rules can act on it",
            len(fin_tables) >= 5, f"financial tables: {', '.join(fin_tables)}")

    # 17. every table carries the audit columns
    missing_audit = [t for t, tbl in tables.items()
                     if t not in ("AuditLog", "IntegrationJobs")
                     and not {"CreatedAt", "CreatedBy", "UpdatedAt", "UpdatedBy"}
                     <= {col["name"] for col in tbl["columns"]}]
    c.check("GOV-17", "Every table carries creation and update attribution",
            not missing_audit, f"missing: {missing_audit or 'none'}")

    # 18. the repository declares its synthetic status
    readme = open(os.path.join(modeldef.ROOT, "seed", "README.md"), encoding="utf-8").read()
    c.check("GOV-18", "The seed directory states plainly that its data is synthetic",
            "SYNTHETIC TEST DATA ONLY" in readme, "stated in seed/README.md")
    return c
