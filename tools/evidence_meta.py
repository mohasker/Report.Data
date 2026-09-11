"""What each check suite is, and what it is NOT evidence of.

The owner's instruction of 2026-09-11: local model validation must never be represented
as proof that AppSheet, Google Drive, Make, the Claude API, QuickBooks, mobile offline
synchronisation or document rendering works in production.
"""

# kind: "logic"      - executable rules run against synthetic data in this repository
#       "structural" - an assertion about the shape of the model or the repository itself
#       "simulation" - a reference implementation standing in for a platform primitive
SUITE_KIND = {
    "Seed conformance": ("structural",
        "Validates the synthetic data against the canonical model. Says nothing about any platform."),
    "Capture once, use twice": ("structural",
        "Asserts the structural guarantees behind the owner's capture-once correction: the normal "
        "description is optional, project and location stay trusted structured fields, AI output "
        "is advisory and excluded from every content hash, no quantitative or contractual field "
        "is AI-sourced, no public image link is required, and CAP-01 is present in the model and "
        "the documentation. It says NOTHING about whether any capture platform can perform a "
        "native multi-file share to a messaging group - that is CAP-GATE, a real-device test."),
    "Lean operational MVP": ("structural",
        "Asserts that the 12-18 table build subset holds together, that no lean table requires a "
        "deferred one, and that every deferred table keeps its schema. Says nothing about whether "
        "the app built from it is fast enough - that is the Phase 2B field measurement."),
    "Configurability and unbounded width": ("structural",
        "Scans the model, schemas, security matrix and logic files for hard-coded identifiers, and "
        "exercises the rule engines with a fourth project added in memory."),
    "Project segregation": ("logic",
        "Runs the reference access rules against synthetic rows. It proves the RULE is correct. It "
        "does NOT prove that AppSheet security filters implement it — that is a Phase 2 "
        "integration test on the real platform."),
    "Role separation, time-bound access and recoverability": ("logic",
        "Runs the reference access rules and grant validation. Proves the rule, not its "
        "enforcement by any platform."),
    "Evidence rules": ("logic",
        "Runs the effective-rule resolver and completeness evaluator against synthetic visits. "
        "Does NOT prove that a mobile form enforces them, on any device, online or offline."),
    "Status transitions, approvals and delegation": ("structural",
        "Asserts the declared transition matrix forbids the dangerous paths and that fixtures sit "
        "in reachable states. Does NOT prove a running workflow honours it."),
    "Content hashing and approval binding": ("logic",
        "Executes the canonical serialisation and hashing. This one is genuinely complete: the "
        "algorithm here is the algorithm. Its INTEGRATION into a workflow is not tested."),
    "Document numbering": ("simulation",
        "Exercises a reference numbering service whose atomic counter is a SQLite transaction, "
        "standing in for the orchestration platform's atomic data-store update. Proves the "
        "CONTRACT holds under concurrency. Does NOT prove Make's data store behaves identically — "
        "that is a Phase 3 integration test."),
    "Deterministic calculation": ("logic",
        "Executes the calculation engine. The arithmetic and the tax-blocking behaviour are real "
        "and complete. Reconciliation against QuickBooks is NOT tested and cannot be until Phase 7."),
    "Bilingual and right-to-left readiness": ("structural",
        "Asserts bilingual structure and Unicode integrity through hashing. Does NOT prove that "
        "any template, PDF renderer or mobile keyboard handles Arabic or RTL correctly."),
    "Governance and safety rules": ("structural",
        "Scans the repository and the model for secrets, non-synthetic identities, AI fields in "
        "hashes, delete grants and missing attribution."),
}

NOT_PROVEN = [
    ("AppSheet", "That security filters, offline capture, image fidelity, dependent dropdowns or "
                 "sync behave as designed on the real platform or on real devices.", "Phase 2"),
    ("Google Drive", "That folder provisioning is idempotent, that originals survive registration "
                     "byte-for-byte, or that permissions are least-privilege in practice.", "Phase 3"),
    ("Make.com", "That scenarios run, that idempotency keys suppress duplicates in the real data "
                 "store, or that error routes catch what they are meant to.", "Phase 3"),
    ("Claude API", "That prompts return schema-valid output, that injection defences hold against "
                   "a real model, or what analysis actually costs.", "Phase 4"),
    ("Document rendering", "That any template merges, paginates, or renders Arabic and "
                           "right-to-left text correctly in a PDF.", "Phase 5"),
    ("QuickBooks Online", "That the company file supports the required tax codes, classes, "
                          "currencies or API operations, or that totals reconcile.", "Phase 7"),
    ("Mobile offline sync", "That a visit captured offline on a real phone syncs completely, in "
                            "order, with its photographs.", "Phase 2 field test"),
    ("Field usability", "That a supervisor can complete a visit faster than the habit it "
                        "replaces — the single largest risk to the whole system (R-06).",
     "Phase 2 field test"),
    ("Native multi-file share (CAP-GATE)",
     "That any capture platform can hand several actual image files and a formatted summary to an "
     "existing WhatsApp or WhatsApp Business group through the operating system share sheet, on "
     "iOS and Android, without the supervisor selecting the images a second time. Nothing in this "
     "repository can establish this; only a real device can.", "Phase 2A device test"),
]

# MASTER_SPEC section 14 acceptance criteria -> what Phase 1 can and cannot say about each
ACCEPTANCE_MAP = [
    (1, "Visit with multiple activities and unlimited child photo rows",
     ["SEED-01", "EVD-05"], "partial",
     "The model supports it and fixtures exercise it. The practical limit is a Phase 2 measurement."),
    (2, "Project-dependent locations function correctly",
     ["SEG-10", "SEG-11", "EVD-02"], "partial",
     "Rule proven against synthetic data; the dependent dropdown itself is Phase 2."),
    (3, "No cross-project leakage; multi-project users switch cleanly",
     ["SEG-01", "SEG-02", "SEG-03", "SEG-04", "SEG-05", "SEG-06", "SEG-07", "SEG-08",
      "SEG-09", "SEG-10", "SEG-12", "ACC-02", "ACC-06", "ACC-15"], "partial",
     "The rule is proven exhaustively. Enforcement by AppSheet security filters is the Phase 2 gate."),
    (4, "Originals in the correct protected location and unchanged",
     ["GOV-12", "GOV-13"], "not-tested",
     "The write-once CONTRACT is represented in the model. Nothing has been stored anywhere."),
    (5, "Mandatory evidence rules prevent incomplete submission",
     ["EVD-05", "EVD-06", "EVD-07", "EVD-08", "EVD-09", "EVD-10", "EVD-11", "EVD-12"], "partial",
     "The rules are executable and correct. On-device enforcement is Phase 2."),
    (6, "Reviewers approve/reject visits and individual photographs with comments",
     ["TRN-03", "TRN-11", "TRN-19"], "partial",
     "Transitions and prohibitions are declared. The review UI is Phase 2."),
    (7, "Duplicate triggers do not create duplicate jobs or documents",
     ["NUM-01", "NUM-09", "TRN-07"], "partial",
     "Numbering uniqueness is proven under concurrency in a simulation. Webhook idempotency is Phase 3."),
    (8, "Claude produces schema-valid analysis and flags uncertainty",
     [], "not-tested",
     "Schemas are written; no API call has been made. Phase 4."),
    (9, "Monthly draft generated from an immutable approved snapshot",
     ["HASH-07", "HASH-08", "TRN-05"], "partial",
     "Snapshot and hash mechanics are defined and tested. Generation is Phase 5."),
    (10, "Rendered PDF passes visual inspection",
     [], "not-tested", "No document has been rendered. Phase 5."),
    (11, "Editing approved source data invalidates or versions the approval",
     ["HASH-03", "HASH-04", "HASH-05", "HASH-06", "HASH-07", "HASH-08", "TRN-10"], "proven-in-logic",
     "The hashing algorithm is the real one; this is as close to complete as Phase 1 can get."),
    (12, "No external email or accounting posting without the correct approval",
     ["TRN-06", "GOV-05", "CALC-01"], "not-tested",
     "Neither capability exists. Phase 7."),
    (13, "Tested failures produce actionable logs and recover without data loss",
     ["NUM-07", "NUM-08"], "not-tested",
     "The failure taxonomy and error queue are specified; nothing has failed for real. Phase 3."),
    (14, "Operator and administrator guides exist",
     [], "partial",
     "The operator runbook outline exists; it is completed in Phase 3 when the scenarios do."),
    (15, "Capture once, use twice: the supervisor never selects or uploads the same evidence twice",
     ["CAP-01", "CAP-18", "CAP-19/QuickShare", "CAP-19/AIReviewedShare", "CAP-20", "CAP-21"],
     "not-tested",
     "The model forbids re-selection, groups evidence under one capture batch and makes a retry "
     "re-use stored files. Whether the platform honours it is CAP-GATE, a real-device test."),
    (16, "A written description is never mandatory for a normal photographic submission",
     ["CAP-02", "CAP-03", "CAP-04", "CAP-05", "CAP-26"], "proven-in-logic",
     "Every description field is optional in the canonical model, the optional-note vocabulary "
     "exists, the exceptional workflows that do require a reason are named, and a regression guard "
     "fails if any document reintroduces the requirement."),
    (17, "AI proposes; a human decides; trusted context never comes from a photograph",
     ["CAP-06", "CAP-07/ProjectID", "CAP-07/LocationID", "CAP-08", "CAP-09", "CAP-10", "CAP-11",
      "CAP-12", "CAP-13", "CAP-14", "CAP-15"], "proven-in-logic",
     "Proposal columns are separate from confirmed columns, no AI column enters a content hash, "
     "and sixteen columns are closed to AI by declaration and by test. Whether a real model obeys "
     "its prompt is Phase 4."),
]
