#!/usr/bin/env python3
"""Author the canonical Phase 1 model and write model/model.json.

model/model.json is the single source of truth for Phase 1. The table schemas and
the data dictionary are generated from it, so they cannot drift apart. This script
is the authoring convenience: it expresses the model compactly and emits the JSON.

Run:  python3 tools/build_model.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_VERSION = "1.0.0"
# The deterministic stamp carried into every generated document. Bump it when the model
# changes; never derive it from the system clock.
MODEL_DATE = "2026-09-12"

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
TABLES = {}
ENUMS = {}


def enum(name, description, values):
    """values: list of (code, label_en, label_ar, description)"""
    ENUMS[name] = {
        "description": description,
        "values": [
            {"code": c, "label_en": e, "label_ar": a, "description": d}
            for (c, e, a, d) in values
        ],
    }


def col(name, type_, req=False, **kw):
    c = {"name": name, "type": type_, "required": req}
    c.update(kw)
    return c


def table(name, category, scope, sensitivity, phase, desc_en, desc_ar, pk, columns,
          content_hash=None, notes=None, unique_together=None, at_least_one=None):
    TABLES[name] = {
        "name": name,
        "category": category,          # master | operational | document | financial | control | vocabulary
        "scope": scope,                # global | project | entity
        "sensitivity": sensitivity,    # internal | confidential | financial | personal
        "phase": phase,                # phase in which the table is BUILT (designed now regardless)
        "description_en": desc_en,
        "description_ar": desc_ar,
        "primary_key": pk,
        "columns": columns,
        "content_hash_fields": content_hash or [],
        "unique_together": unique_together or [],
        "at_least_one": at_least_one or [],
        "notes": notes or [],
    }


AUDIT = [
    col("CreatedAt", "datetime", True, src="system", note="UTC. Set once on insert."),
    col("CreatedBy", "email", True, src="system", note="USEREMAIL() or the service identity."),
    col("UpdatedAt", "datetime", True, src="system", note="UTC. Excluded from ContentHash."),
    col("UpdatedBy", "email", True, src="system"),
]
ACTIVE = [col("IsActive", "bool", True, default="TRUE", src="user",
              note="Soft delete. Rows are never hard-deleted; history is evidence.")]
VERSIONED = [
    col("EntityVersion", "int", True, default="1", src="system",
        note="Incremented on every material change. Referenced by Approvals."),
    col("ContentHash", "checksum", True, src="system",
        note="SHA-256 over the canonical serialisation of the fields listed in content_hash_fields."),
]

# --------------------------------------------------------------------------
# enums
# --------------------------------------------------------------------------
enum("Language", "Interface and document languages supported from Phase 1 (D-11).", [
    ("en", "English", "الإنجليزية", "Left-to-right. First generated-report language."),
    ("ar", "Arabic", "العربية", "Right-to-left. Capability is architectural from Phase 1."),
])

enum("ProjectStatus", "Lifecycle of a project. Adding or activating a project is configuration only (D-01).", [
    ("Draft", "Draft", "مسودة", "Being configured. Not visible to field users."),
    ("Active", "Active", "نشط", "Accepting site visits."),
    ("Suspended", "Suspended", "موقوف", "No new visits; existing records remain readable."),
    ("Completed", "Completed", "منجز", "Work finished; reporting may continue until closeout."),
    ("Archived", "Archived", "مؤرشف", "Read-only. Retained per the residency and retention rules."),
])

enum("ReportingFrequency", "Per-project reporting cadence.", [
    ("Daily", "Daily", "يومي", ""),
    ("Weekly", "Weekly", "أسبوعي", ""),
    ("Monthly", "Monthly", "شهري", "MVP default."),
    ("Quarterly", "Quarterly", "ربع سنوي", ""),
    ("OnCompletion", "On completion", "عند الإنجاز", "One-off work orders."),
    ("OnDemand", "On demand", "عند الطلب", ""),
])

enum("BillingMethod", "How a project is billed. Configuration, never logic.", [
    ("MonthlyFixed", "Monthly fixed", "مقطوع شهري", "Recurring maintenance contract."),
    ("MeasuredBOQ", "Measured against BOQ", "بالكميات المنفذة", "Quantities certified per period."),
    ("LumpSumMilestone", "Lump sum by milestone", "مقطوع بالمراحل", ""),
    ("OnCompletion", "On completion", "عند الإنجاز", "One-off work order."),
    ("TimeAndMaterial", "Time and material", "بالوقت والمواد", ""),
])

enum("WorkflowStatus", "SiteVisit lifecycle. Transitions are restricted (see transitions).", [
    ("Draft", "Draft", "مسودة", "Editable by the submitter. Not visible to reviewers."),
    ("Submitted", "Submitted", "مُرسل", "Handed to server-side validation."),
    ("ValidationFailed", "Validation failed", "فشل التحقق", "Specific correctable errors recorded."),
    ("UnderTechnicalReview", "Under technical review", "قيد المراجعة الفنية", "In a reviewer queue."),
    ("CorrectionRequired", "Correction required", "يتطلب تصحيح", "Returned to the submitter with a reason."),
    ("TechnicallyApproved", "Technically approved", "معتمد فنياً", "Evidence may now be used in a report."),
    ("ReadyForReport", "Ready for report", "جاهز للتقرير", "Eligible for a document job snapshot."),
    ("IncludedInDraft", "Included in draft", "مُدرج في مسودة", "Frozen into at least one document snapshot."),
    ("Released", "Released", "صادر", "Part of a released document."),
    ("Archived", "Archived", "مؤرشف", "Read-only."),
    ("Cancelled", "Cancelled", "ملغي", "Cancelled with a recorded reason. Never deleted."),
])

enum("VisitActivityStatus", "Activity-level lifecycle inside a visit.", [
    ("Draft", "Draft", "مسودة", ""),
    ("Submitted", "Submitted", "مُرسل", ""),
    ("UnderReview", "Under review", "قيد المراجعة", ""),
    ("Approved", "Approved", "معتمد", "Approved by the technical reviewer."),
    ("Rejected", "Rejected", "مرفوض", "Excluded from reporting, retained as a record."),
    ("CorrectionRequired", "Correction required", "يتطلب تصحيح", ""),
    ("Cancelled", "Cancelled", "ملغي", ""),
])

enum("EvidenceStage", "What a photograph is evidence of (spec 5.10).", [
    ("Before", "Before", "قبل", ""),
    ("During", "During", "أثناء", ""),
    ("After", "After", "بعد", ""),
    ("Observation", "Observation", "ملاحظة", "Caption mandatory."),
    ("Snag", "Snag", "ملاحظة عدم مطابقة", "Caption mandatory."),
    ("Material", "Material", "مواد", "Caption mandatory."),
    ("Equipment", "Equipment", "معدات", ""),
    ("Safety", "Safety", "السلامة", "Caption mandatory."),
    ("Other", "Other", "أخرى", ""),
])

enum("CaptureMode", "How a submission reaches the main-contractor group (D-16).", [
    ("QuickShare", "Quick share", "مشاركة فورية",
     "Capture, store, then open the native share sheet immediately. AI analysis runs "
     "afterwards and prepares the internal report metadata."),
    ("AIReviewedShare", "AI reviewed share", "مشاركة بعد المراجعة",
     "Capture, AI proposal, supervisor confirmation, then the native share sheet."),
])

enum("ShareStatus", "Outcome of the native share action. Never set by AI (D-16).", [
    ("NotShared", "Not shared", "لم تتم المشاركة", "Default."),
    ("ShareInitiated", "Share initiated", "بدأت المشاركة",
     "The share sheet was opened. The system cannot observe what happened inside it."),
    ("ShareConfirmed", "Share confirmed", "تم تأكيد المشاركة",
     "The supervisor confirmed the share completed. A human claim, not a platform receipt."),
    ("ShareCancelled", "Share cancelled", "أُلغيت المشاركة", "Recoverable; the evidence is retained."),
    ("ShareFailed", "Share failed", "فشلت المشاركة",
     "Recoverable. Re-sharing must never require re-selecting the images (CAP-01)."),
])

enum("AIProposalDisposition", "What the supervisor did with the AI proposal (D-17).", [
    ("NotOffered", "Not offered", "لم تُعرض", "Quick Share, or analysis not yet complete."),
    ("Accepted", "Accepted", "مقبول", "Confirmed unchanged. Still a human decision."),
    ("Corrected", "Corrected", "مُصحح", "The supervisor changed one or more proposed values."),
    ("Rejected", "Rejected", "مرفوض", "The proposal was discarded entirely."),
])

enum("ClassificationStatus", "How far a photograph's activity classification has got (D-23). "
     "Pending is a normal, non-blocking state.", [
    ("Pending", "Pending", "قيد الانتظار",
     "Captured, not yet classified. The normal state immediately after a Quick Share."),
    ("AIProposed", "AI proposed", "اقتراح من الذكاء الاصطناعي",
     "An advisory proposal exists. **Still untrusted.** No report or business rule may use it."),
    ("Confirmed", "Confirmed", "مؤكد",
     "A supervisor or reviewer set ConfirmedActivityTypeID. The only trusted state."),
    ("NotApplicable", "Not applicable", "لا ينطبق",
     "The photograph carries no activity to classify — a safety observation, a material delivery."),
    ("Excluded", "Excluded", "مستبعد",
     "Deliberately left out: a duplicate, an unusable image, or evidence excluded from this report."),
])

enum("QuarantineStatus", "What happened to evidence that was still queued on a device when the "
     "user's access was revoked (D-25). Quarantine preserves evidence without granting the "
     "revoked user anything.", [
    ("NotQuarantined", "Not quarantined", "غير محجوز",
     "The normal state. The photograph was captured and uploaded under a valid assignment."),
    ("Quarantined", "Quarantined", "محجوز للمراجعة",
     "Captured BEFORE revocation and completed into the restricted area after it. Invisible to "
     "the revoked user, excluded from every report, calculation and approval until a reviewer "
     "accepts it."),
    ("AcceptedIntoProject", "Accepted into the project", "مقبول في المشروع",
     "A reviewer accepted it. It becomes a traceable project record, and the quarantine history "
     "is retained."),
    ("Rejected", "Rejected", "مرفوض",
     "A reviewer rejected it, with a mandatory reason. The audit record is retained under the "
     "retention policy; the row is never deleted."),
])

enum("AnalysisEligibility", "Whether a photograph is worth sending to analysis (D-24). Filtering "
     "happens before the call, never after it.", [
    ("Eligible", "Eligible", "مؤهل", "Analysis has value and has not run."),
    ("Analysed", "Analysed", "تم التحليل", "Already analysed. Never analysed twice."),
    ("SkippedDuplicate", "Skipped — duplicate", "تم التخطي - مكرر",
     "A near-identical photograph in the same batch was analysed instead."),
    ("SkippedQuality", "Skipped — unusable", "تم التخطي - جودة غير كافية",
     "Blurred, dark or obstructed beyond usefulness. Retained as evidence, not analysed."),
    ("SkippedExcluded", "Skipped — excluded", "تم التخطي - مستبعد",
     "Deleted or explicitly excluded by the supervisor before analysis ran."),
    ("SkippedDisabled", "Skipped — analysis off", "تم التخطي - التحليل متوقف",
     "Analysis is switched off for this project, or the monthly cap is reached."),
])

enum("SiteNoteCategory", "Why an optional site note was written (D-18). Facts a photograph "
     "cannot establish.", [
    ("ClientInstruction", "Client instruction", "تعليمات العميل", ""),
    ("AccessRestriction", "Access restriction", "قيود الدخول", ""),
    ("PermitIssue", "Permit issue", "مشكلة تصريح", ""),
    ("HiddenDefect", "Hidden or underground defect", "عيب مخفي أو تحت الأرض", ""),
    ("MeasuredQuantity", "Measured quantity", "كمية مقاسة",
     "Typed by a person. Never proposed by image analysis."),
    ("MaterialQuantityOrBatch", "Material quantity or batch", "كمية أو دفعة المواد", ""),
    ("EquipmentFailure", "Equipment failure", "عطل معدات", ""),
    ("NonCompletionReason", "Reason for non-completion", "سبب عدم الإنجاز", ""),
    ("SafetyRestriction", "Safety restriction", "قيد يتعلق بالسلامة", ""),
    ("PostponedByOtherParty", "Work postponed by another party", "تأجيل من طرف آخر", ""),
])

enum("ReviewerDecision", "Per-photograph reviewer decision. Only a human sets this (D-06).", [
    ("Pending", "Pending", "قيد الانتظار", "Default. Never set by AI."),
    ("Approved", "Approved", "معتمد", "May appear in an official report."),
    ("Rejected", "Rejected", "مرفوض", "Retained as a record, excluded from reporting."),
    ("Excluded", "Excluded", "مستبعد", "Valid evidence deliberately left out of this report."),
])

enum("AIAnalysisStatus", "State of the advisory AI analysis for one photograph.", [
    ("NotRequested", "Not requested", "لم يُطلب", ""),
    ("Queued", "Queued", "في الطابور", ""),
    ("Completed", "Completed", "مكتمل", "Advisory observation stored."),
    ("Failed", "Failed", "فشل", "Recorded with a failure class. Never blocks review."),
    ("SchemaInvalid", "Schema invalid", "مخرجات غير مطابقة", "Response rejected before storage."),
    ("Skipped", "Skipped", "متخطى", "Ineligible (for example a duplicate)."),
    ("Disabled", "Disabled for project", "معطل للمشروع", "Residency or contract rule (D-12)."),
])

enum("SnagSeverity", "Snag severity.", [
    ("Low", "Low", "منخفضة", ""), ("Medium", "Medium", "متوسطة", ""),
    ("High", "High", "عالية", ""), ("Critical", "Critical", "حرجة", ""),
])

enum("SnagStatus", "Snag lifecycle.", [
    ("Open", "Open", "مفتوح", ""), ("Assigned", "Assigned", "مُسند", ""),
    ("InProgress", "In progress", "قيد التنفيذ", ""),
    ("PendingVerification", "Pending verification", "بانتظار التحقق", ""),
    ("Closed", "Closed", "مغلق", "Requires closure evidence and a verifier."),
    ("Rejected", "Rejected", "مرفوض", ""), ("Deferred", "Deferred", "مؤجل", ""),
])

enum("DocumentTypeCode", "Controlled document types. Each has its own numbering series (D-10).", [
    ("DailyReport", "Daily report", "تقرير يومي", ""),
    ("WeeklyReport", "Weekly report", "تقرير أسبوعي", ""),
    ("MonthlyTechnicalReport", "Monthly technical report", "تقرير فني شهري", "Only type produced in the MVP."),
    ("InspectionReport", "Inspection report", "تقرير معاينة", ""),
    ("CorrectiveActionReport", "Corrective action report", "تقرير إجراء تصحيحي", ""),
    ("Quotation", "Quotation", "عرض سعر", ""),
    ("CompletionCertificate", "Completion certificate", "شهادة إنجاز", ""),
    ("InvoiceCover", "Invoice cover", "غلاف فاتورة", "Numbering aligned to the accounting process (D-10)."),
    ("Transmittal", "Transmittal", "كتاب إحالة", ""),
])

enum("JobStatus", "DocumentJob lifecycle.", [
    ("Requested", "Requested", "مطلوب", ""),
    ("Validating", "Validating inputs", "تحقق من المدخلات", ""),
    ("InputValidationFailed", "Input validation failed", "فشل تحقق المدخلات", "Specific gaps recorded."),
    ("SnapshotFrozen", "Snapshot frozen", "لقطة مجمدة", "Included record IDs and versions fixed."),
    ("Generating", "Generating", "قيد الإنشاء", ""),
    ("Generated", "Generated", "تم الإنشاء", ""),
    ("Failed", "Failed", "فشل", ""),
    ("Cancelled", "Cancelled", "ملغي", "Any reserved number is cancelled, never reused (D-10)."),
])

enum("DocumentStatus", "Document lifecycle. Release is the only externally visible state.", [
    ("Draft", "Draft", "مسودة", ""),
    ("PendingTechnicalApproval", "Pending technical approval", "بانتظار الاعتماد الفني", ""),
    ("TechnicallyApproved", "Technically approved", "معتمد فنياً", "Revision locked."),
    ("RevisionRequired", "Revision required", "يتطلب مراجعة", "Content changed; approval void."),
    ("PendingRelease", "Pending release", "بانتظار الإصدار", ""),
    ("Released", "Released", "صادر", "Recipient snapshot recorded."),
    ("Superseded", "Superseded", "مُستبدل", "Replaced by a later revision."),
    ("Cancelled", "Cancelled", "ملغي", ""),
])

enum("ApprovalStage", "Approval gates. Each is routed by the approval matrix (D-09).", [
    ("EvidenceReview", "Evidence review", "مراجعة الأدلة", "Visit and photograph level."),
    ("TechnicalReview", "Technical review", "المراجعة الفنية", "Document level."),
    ("FinanceReview", "Finance review", "المراجعة المالية", "Phase 6/7."),
    ("Release", "Release", "الإصدار", "Authorises external delivery."),
    ("OverrideAuthorisation", "Override authorisation", "اعتماد استثناء", "Recorded as an override, never silent."),
])

enum("ApprovalDecision", "Recorded decision. Bound to EntityVersion and ContentHash (ADR-0006).", [
    ("Pending", "Pending", "قيد الانتظار", ""),
    ("Approved", "Approved", "معتمد", ""),
    ("Rejected", "Rejected", "مرفوض", ""),
    ("Delegated", "Delegated", "مفوض", "Acted by a delegate; original responsible user recorded."),
    ("Withdrawn", "Withdrawn", "مسحوب", ""),
    ("Void", "Void — content changed", "لاغٍ لتغير المحتوى", "ContentHash no longer matches."),
])

enum("NumberState", "Document number lifecycle (D-10). A cancelled number is never reused.", [
    ("Reserved", "Reserved", "محجوز", "Allocated atomically to a job before generation."),
    ("Issued", "Issued", "صادر", "Bound to a created document."),
    ("Cancelled", "Cancelled", "ملغي", "Job failed or abandoned. Recorded with a reason."),
])

enum("FailureClass", "Failure taxonomy (spec 12). Determines whether a retry is permitted.", [
    ("Validation", "Validation", "تحقق", "Never retried."),
    ("Authentication", "Authentication", "مصادقة", "Never retried. Alert administrator."),
    ("Authorization", "Authorization", "تخويل", "Never retried. Possible security event."),
    ("RateLimit", "Rate limit", "حد المعدل", "Retriable with backoff."),
    ("Network", "Network", "شبكة", "Retriable with backoff."),
    ("ProviderUnavailable", "Provider unavailable", "المزود غير متاح", "Retriable with backoff."),
    ("FileMissing", "File missing", "ملف مفقود", "One delayed retry; sync latency is normal."),
    ("SchemaMismatch", "Schema mismatch", "عدم تطابق المخطط", "Never retried blindly."),
    ("Duplicate", "Duplicate", "مكرر", "Suppressed and logged. Expected, not an error."),
    ("Conflict", "Conflict", "تعارض", "Human resolution. Never auto-overwrite."),
    ("Unknown", "Unknown", "غير معروف", "Dead-letter immediately."),
])

enum("IntegrationStatus", "Outcome of one external call attempt.", [
    ("Pending", "Pending", "معلق", ""), ("InProgress", "In progress", "قيد التنفيذ", ""),
    ("Succeeded", "Succeeded", "نجح", ""), ("Failed", "Failed", "فشل", ""),
    ("DeadLettered", "Dead lettered", "في طابور المراجعة", "Awaiting an operator."),
    ("DuplicateSuppressed", "Duplicate suppressed", "تم منع التكرار", "Idempotency key already claimed."),
])

enum("InvoiceFinanceStatus", "Finance lifecycle of an invoice request (Phase 6/7).", [
    ("Draft", "Draft", "مسودة", "Calculated but not submitted for finance approval."),
    ("PendingFinanceApproval", "Pending finance approval", "بانتظار الاعتماد المالي", ""),
    ("FinanceApproved", "Finance approved", "معتمد مالياً", "Required before anything may reach the accounting system."),
    ("Rejected", "Rejected", "مرفوض", "Returned with a reason; a new calculation is required."),
    ("Void", "Void - inputs changed", "لاغٍ لتغير المدخلات", "The source content hash changed after approval."),
])

enum("QuickBooksSyncStatus", "Accounting synchronisation lifecycle (Phase 7). Nothing here is "
     "reachable until the owner authorises production posting in writing.", [
    ("NotSent", "Not sent", "لم يُرسل", "Default. The invoice exists only inside this system."),
    ("Queued", "Queued for sandbox", "في الطابور للبيئة التجريبية", "Awaiting a sandbox posting attempt."),
    ("SandboxPosted", "Posted to sandbox", "مُرحّل في البيئة التجريبية", "Posted to a test company only."),
    ("Reconciling", "Reconciling", "قيد المطابقة", "Reading back the posted document to compare totals."),
    ("ReconciliationFailed", "Reconciliation failed", "فشلت المطابقة",
     "Totals differ. Never auto-corrected in either direction; a human resolves it."),
    ("Posted", "Posted to production", "مُرحّل للإنتاج", "Requires written authorisation to enable."),
    ("Failed", "Failed", "فشل", "Classified failure; retried only when the class is retriable."),
])

enum("DataClassificationCode", "Sensitivity classes used to drive residency and sharing rules (D-12).", [
    ("Public", "Public", "عام", ""),
    ("Internal", "Internal", "داخلي", ""),
    ("ClientConfidential", "Client confidential", "سري للعميل", "Default for photographic evidence."),
    ("Personal", "Personal data", "بيانات شخصية", "Identifiable individuals."),
    ("Financial", "Financial", "مالي", "Rates, invoices, accounting identifiers."),
    ("GovernmentRestricted", "Government restricted", "مقيد حكومياً", "Contract-imposed handling."),
])

enum("ResidencyRuleCode", "Storage and processing restrictions assignable per client, contract or project (D-12).", [
    ("NoRestriction", "No restriction", "بدون قيود", "Default until a contract says otherwise."),
    ("RegionRestricted", "Region restricted", "مقيد بالمنطقة", "Named region only."),
    ("CountryRestricted", "Country restricted", "مقيد بالدولة", "Named country only."),
    ("NoThirdPartyAI", "No third-party AI processing", "بدون معالجة ذكاء اصطناعي خارجية", "Disables AI analysis for the project."),
    ("NoCloudStorage", "No third-party cloud storage", "بدون تخزين سحابي خارجي", "Blocks production upload for the project."),
])

enum("DelegationScope", "Breadth of a temporary approval delegation (D-09).", [
    ("AllProjects", "All projects", "كل المشاريع", ""),
    ("SpecificProjects", "Specific projects", "مشاريع محددة", ""),
    ("SpecificStage", "Specific stage only", "مرحلة محددة فقط", ""),
])

enum("TaxTreatmentPlaceholder",
     "Placeholder only. NO CLASSIFICATION IS NAMED OR ASSUMED (D-08). "
     "'Zero-rated', 'exempt', 'out of scope' and 'no tax configured' are distinct and "
     "non-interchangeable; the real values come from the accountant in writing.", [
    ("PENDING_ACCOUNTANT_CONFIRMATION", "Pending accountant confirmation",
     "بانتظار تأكيد المحاسب", "The only value permitted in production before written confirmation."),
    ("SYNTHETIC_TEST_ONLY", "Synthetic test value — not a tax position",
     "قيمة اختبارية فقط وليست موقفاً ضريبياً",
     "Exists solely so the arithmetic can be tested offline. It asserts nothing about any "
     "jurisdiction and must never appear in production data (D-08)."),
])

enum("EvidenceRuleSource", "Where an effective evidence rule came from.", [
    ("Global", "Global activity type", "نوع النشاط العام", ""),
    ("ProjectOverride", "Project override", "تخصيص للمشروع", "Project-specific rule wins."),
])

# --------------------------------------------------------------------------
# 1. Legal entity, vocabularies and global master data
# --------------------------------------------------------------------------
table("LegalEntities", "master", "global", "internal", 1,
      "Registered legal entities that issue documents. Multi-entity from the start (D-02).",
      "الكيانات القانونية المسجلة التي تصدر المستندات",
      "LegalEntityID", [
    col("LegalEntityID", "id", True, key="pk", src="system", ex="LE-A7T3R2"),
    col("EntityCode", "text", True, uniq=True, src="user", validation="2-6 uppercase letters/digits",
        note="Used in document numbers (D-10).", ex="AH"),
    col("LegalNameEN", "text", True, src="user", ar="LegalNameAR",
        note="From the current Commercial Registration. Placeholder until verified.",
        ex="LEGAL_ENTITY_NAME_PENDING_VERIFICATION"),
    col("LegalNameAR", "text", True, src="user", lang="ar",
        note="Arabic legal name preserved exactly; never transliterated (D-11)."),
    col("TradeNameEN", "text", False, src="user", ar="TradeNameAR"),
    col("TradeNameAR", "text", False, src="user", lang="ar"),
    col("CommercialRegistrationNumber", "text", True, src="user",
        note="CR number as registered. Verified before any production document (D-02)."),
    col("EstablishmentCardNumber", "text", False, src="user"),
    col("TaxRegistrationNumber", "text", False, src="user", sens="financial",
        note="Presence does not imply any tax treatment (D-08)."),
    col("TaxRegistrationStatus", "text", True, default="PENDING_ACCOUNTANT_CONFIRMATION", src="user",
        note="Free text placeholder until the accountant confirms in writing (D-08)."),
    col("RegisteredAddressEN", "longtext", True, src="user", ar="RegisteredAddressAR"),
    col("RegisteredAddressAR", "longtext", False, src="user", lang="ar"),
    col("Country", "text", True, src="user", ex="QA"),
    col("Currency", "text", True, src="user", validation="ISO 4217", ex="QAR"),
    col("OfficialEmail", "email", True, src="user"),
    col("OfficialTelephone", "phone", True, src="user"),
    col("OfficialWhatsApp", "phone", False, src="user"),
    col("LogoFileKey", "filekey", False, src="config",
        note="Reference to the approved logo. Aspect ratio preserved (spec 10)."),
    col("DocumentFooterEN", "longtext", False, src="user", ar="DocumentFooterAR"),
    col("DocumentFooterAR", "longtext", False, src="user", lang="ar"),
    col("AuthorisedSignatories", "json", False, src="user",
        note="List of {name_en, name_ar, position_en, position_ar, scope}. No specimen signatures stored."),
    col("EffectiveFrom", "date", True, src="user"),
    col("EffectiveTo", "date", False, src="user"),
    col("Version", "int", True, default="1", src="system",
        note="A change to legal identity creates a new version; documents record the version used."),
] + ACTIVE + AUDIT,
      notes=["Never edited in place for a legal-name correction: a new version is created so that "
             "documents already issued remain explainable."])

table("Languages", "vocabulary", "global", "internal", 1,
      "Supported languages and their direction. Bilingual capability is architectural (D-11).",
      "اللغات المدعومة واتجاه الكتابة", "LanguageCode", [
    col("LanguageCode", "enum", True, key="pk", enum="Language", ex="en"),
    col("NameEN", "text", True, src="config", ar="NameAR"),
    col("NameAR", "text", True, src="config", lang="ar"),
    col("Direction", "text", True, src="config", validation="LTR|RTL", ex="RTL"),
    col("IsDocumentLanguage", "bool", True, src="config",
        note="Whether approved templates exist for this language."),
] + ACTIVE + AUDIT)

table("Roles", "vocabulary", "global", "internal", 1,
      "System roles. Authorisation is enforced by security filters and server-side re-validation, "
      "never by view visibility (spec 7.4).",
      "أدوار النظام", "RoleID", [
    col("RoleID", "id", True, key="pk", ex="ROLE-FIELDUSER"),
    col("RoleCode", "text", True, uniq=True, src="config", ex="FieldUser"),
    col("NameEN", "text", True, src="config", ar="NameAR"),
    col("NameAR", "text", True, src="config", lang="ar"),
    col("Description", "longtext", True, src="config"),
    col("SeesFinancialData", "bool", True, default="FALSE", src="config",
        note="Field roles are FALSE. Financial tables are kept out of the field app entirely (SEC-04)."),
    col("MayApprove", "bool", True, default="FALSE", src="config"),
    col("MayAdministerMasterData", "bool", True, default="FALSE", src="config"),
] + ACTIVE + AUDIT)

table("Users", "master", "global", "personal", 1,
      "People who may sign in. One identity per person — shared accounts destroy attribution.",
      "مستخدمو النظام", "UserID", [
    col("UserID", "id", True, key="pk", ex="USR-R6V1N8"),
    col("Email", "email", True, uniq=True, src="user",
        note="Normalised to lowercase. The sign-in identity and the audit key."),
    col("FullNameEN", "text", True, src="user", ar="FullNameAR"),
    col("FullNameAR", "text", False, src="user", lang="ar",
        note="Arabic name preserved without transliteration loss (D-11)."),
    col("Mobile", "phone", False, src="user", sens="personal"),
    col("RoleID", "ref", True, ref="Roles.RoleID", src="user"),
    col("EmployeeID", "text", False, src="user", sens="personal"),
    col("DefaultProjectID", "ref", False, ref="Projects.ProjectID", src="user",
        note="Convenience only. Never a substitute for ProjectAssignments."),
    col("Language", "enum", True, default="en", enum="Language", src="user",
        note="Interface and notification language preference (D-11)."),
    col("LastLoginAt", "datetime", False, src="system"),
] + ACTIVE + AUDIT,
      notes=["Payroll and HR attributes are deliberately absent (spec 5.13)."])

table("Units", "vocabulary", "global", "internal", 1,
      "Units of measure for quantities.", "وحدات القياس", "UnitID", [
    col("UnitID", "id", True, key="pk", ex="UNIT-M2"),
    col("UnitCode", "text", True, uniq=True, src="config", ex="m2"),
    col("NameEN", "text", True, src="config", ar="NameAR"),
    col("NameAR", "text", True, src="config", lang="ar"),
    col("DecimalPlaces", "int", True, default="2", src="config",
        note="Quantity rounding for this unit. Applied by the calculation module only."),
] + ACTIVE + AUDIT)

table("Disciplines", "vocabulary", "global", "internal", 1,
      "Work disciplines. A project may permit one or many.", "التخصصات", "DisciplineID", [
    col("DisciplineID", "id", True, key="pk", ex="DIS-LAND"),
    col("DisciplineCode", "text", True, uniq=True, src="config", ex="LANDSCAPE"),
    col("NameEN", "text", True, src="config", ar="NameAR"),
    col("NameAR", "text", True, src="config", lang="ar"),
] + ACTIVE + AUDIT)

table("ActivityTypes", "master", "global", "internal", 1,
      "Catalogue of activities with their default evidence and quantity rules. "
      "Per-project overrides live in ProjectActivityRules.",
      "أنواع الأنشطة وقواعد الأدلة الافتراضية", "ActivityTypeID", [
    col("ActivityTypeID", "id", True, key="pk", ex="ACT-0001"),
    col("DisciplineID", "ref", True, ref="Disciplines.DisciplineID", src="config"),
    col("ActivityCode", "text", True, uniq=True, src="config", ex="TURF-MOW"),
    col("ActivityNameEN", "text", True, src="config", ar="ActivityNameAR"),
    col("ActivityNameAR", "text", True, src="config", lang="ar"),
    col("RequiresBeforePhoto", "bool", True, default="FALSE", src="config"),
    col("RequiresAfterPhoto", "bool", True, default="FALSE", src="config"),
    col("RequiresQuantity", "bool", True, default="FALSE", src="config"),
    col("QuantityUnitID", "ref", False, ref="Units.UnitID", src="config",
        validation="Required when RequiresQuantity is TRUE"),
    col("RequiresMaterial", "bool", True, default="FALSE", src="config"),
    col("RequiresSnagCheck", "bool", True, default="FALSE", src="config"),
    col("MinPhotos", "int", True, default="0", src="config"),
    col("DefaultEvidenceStages", "text", False, src="config",
        note="Comma-separated EvidenceStage codes suggested in the form."),
] + ACTIVE + AUDIT)

table("DocumentTypes", "vocabulary", "global", "internal", 1,
      "Controlled document types. Adding a type is configuration, not development (D-10).",
      "أنواع المستندات المعتمدة", "DocumentTypeCode", [
    col("DocumentTypeCode", "enum", True, key="pk", enum="DocumentTypeCode"),
    col("NameEN", "text", True, src="config", ar="NameAR"),
    col("NameAR", "text", True, src="config", lang="ar"),
    col("RequiresTechnicalApproval", "bool", True, default="TRUE", src="config"),
    col("RequiresFinanceApproval", "bool", True, default="FALSE", src="config"),
    col("RequiresReleaseApproval", "bool", True, default="TRUE", src="config"),
    col("IsExternallyIssued", "bool", True, default="TRUE", src="config"),
    col("BuiltInPhase", "text", True, src="config", ex="5",
        note="MonthlyTechnicalReport is the only type produced in the MVP."),
] + ACTIVE + AUDIT)

table("DataClassifications", "master", "global", "internal", 1,
      "Sensitivity classes applied to records and files, driving residency and sharing rules (D-12).",
      "تصنيفات حساسية البيانات", "ClassificationCode", [
    col("ClassificationCode", "enum", True, key="pk", enum="DataClassificationCode"),
    col("NameEN", "text", True, src="config", ar="NameAR"),
    col("NameAR", "text", True, src="config", lang="ar"),
    col("Description", "longtext", True, src="config"),
    col("MayLeaveTenant", "bool", True, default="FALSE", src="config",
        note="Whether data of this class may be sent to any third-party processor."),
    col("MayBeSharedExternally", "bool", True, default="FALSE", src="config"),
    col("DefaultRetentionDays", "int", False, src="config",
        note="Expiry flags for review. Nothing is ever auto-deleted (C-10)."),
] + ACTIVE + AUDIT)

table("ResidencyRequirements", "master", "global", "internal", 1,
      "Storage and processing restrictions that may be assigned to a client, contract or project (D-12).",
      "متطلبات مكان تخزين ومعالجة البيانات", "ResidencyRequirementID", [
    col("ResidencyRequirementID", "id", True, key="pk", ex="RES-G3K9V2"),
    col("RuleCode", "enum", True, enum="ResidencyRuleCode", src="config"),
    col("NameEN", "text", True, src="config", ar="NameAR"),
    col("NameAR", "text", True, src="config", lang="ar"),
    col("AllowedRegions", "text", False, src="config",
        note="Comma-separated region or country codes where storage is permitted."),
    col("BlocksProductionUpload", "bool", True, default="FALSE", src="config",
        note="TRUE blocks production upload for the affected project only, not the system (D-12)."),
    col("BlocksThirdPartyAI", "bool", True, default="FALSE", src="config",
        note="TRUE disables AI analysis for the affected project."),
    col("SourceClauseReference", "text", False, src="user",
        note="Where in the contract the restriction comes from. No contract text is stored."),
] + ACTIVE + AUDIT)

table("TaxRules", "master", "global", "financial", 6,
      "Configurable tax rules. NO CLASSIFICATION IS NAMED OR ASSUMED before the accountant "
      "confirms it in writing (D-08).",
      "قواعد الضريبة القابلة للتهيئة", "TaxRuleID", [
    col("TaxRuleID", "id", True, key="pk", ex="TAX-PLACEHOLDER-PENDING"),
    col("TaxRuleCode", "text", True, uniq=True, src="config", ex="PENDING_ACCOUNTANT_CONFIRMATION"),
    col("NameEN", "text", True, src="config", ar="NameAR"),
    col("NameAR", "text", True, src="config", lang="ar"),
    col("TreatmentLabel", "enum", True, enum="TaxTreatmentPlaceholder", src="config",
        note="'Zero-rated', 'exempt', 'out of scope' and 'no tax configured' are distinct and "
             "non-interchangeable. None may be recorded here without written confirmation (D-08)."),
    col("RatePercent", "decimal", False, src="config", scale=4,
        validation="Null until confirmed. Null means 'unknown', never 'zero'."),
    col("AppliesToCountry", "text", False, src="config"),
    col("EffectiveFrom", "date", True, src="config"),
    col("EffectiveTo", "date", False, src="config"),
    col("Version", "int", True, default="1", src="system",
        note="The rule AND its version are preserved on every invoice calculation (D-08)."),
    col("ConfirmedByAccountant", "bool", True, default="FALSE", src="user",
        note="Production invoicing is blocked while FALSE."),
    col("ConfirmationReference", "text", False, src="user",
        note="Reference to the accountant's written confirmation. No document content stored."),
] + ACTIVE + AUDIT)

table("NumberingSeries", "master", "global", "internal", 5,
      "One configurable series per legal entity x document type x year x scope x optional client "
      "requirement. Never one undifferentiated sequence (D-10).",
      "تسلسلات ترقيم المستندات القابلة للتهيئة", "SeriesID", [
    col("SeriesID", "id", True, key="pk", ex="SER-F9W3C5"),
    col("LegalEntityID", "ref", True, ref="LegalEntities.LegalEntityID", src="config"),
    col("DocumentTypeCode", "enum", True, enum="DocumentTypeCode", src="config"),
    col("ScopeKind", "text", True, src="config", validation="CompanyWide|PerProject|PerClient",
        note="Determines whether the counter is shared or partitioned."),
    col("ProjectID", "ref", False, ref="Projects.ProjectID", src="config",
        validation="Required when ScopeKind = PerProject"),
    col("ClientID", "ref", False, ref="Clients.ClientID", src="config",
        validation="Required when ScopeKind = PerClient"),
    col("YearBasis", "text", True, default="Calendar", src="config", validation="Calendar|Financial|None"),
    col("FinancialYearStartMonth", "int", False, src="config", validation="1-12 when YearBasis=Financial"),
    col("FormatPattern", "text", True, src="config",
        note="Tokens: {ENTITY} {TYPE} {YYYY} {YY} {PROJECT} {CLIENT} {NNN} {REV}. "
             "Illustrative only until the existing manual register is reviewed (D-10).",
        ex="{ENTITY}-TR-{YYYY}-{NNN}"),
    col("PadWidth", "int", True, default="3", src="config"),
    col("StartNumber", "int", True, default="1", src="config",
        note="Continues the existing manual register rather than restarting it (A-18)."),
    col("ResetRule", "text", True, default="PerYear", src="config", validation="PerYear|Never"),
    col("MigratedFromManualRegister", "bool", True, default="FALSE", src="user",
        note="TRUE once the existing manual series has been reviewed and its last number recorded."),
    col("LastManualNumber", "int", False, src="user",
        note="The final number used manually, so the system continues rather than collides."),
    col("AlignedToAccountingProcess", "bool", True, default="FALSE", src="config",
        note="TRUE for invoice-related series: numbering follows the approved accounting process (D-10)."),
] + ACTIVE + AUDIT,
      unique_together=[["LegalEntityID", "DocumentTypeCode", "ScopeKind", "ProjectID", "ClientID", "YearBasis"]])

table("DocumentTemplates", "master", "global", "internal", 5,
      "Approved templates, keyed by document type, language and optionally project or discipline "
      "(D-11, ADR-0007).",
      "القوالب المعتمدة", "TemplateID", [
    col("TemplateID", "id", True, key="pk", ex="TPL-D8Q2H6"),
    col("DocumentTypeCode", "enum", True, enum="DocumentTypeCode", src="config"),
    col("TemplateNameEN", "text", True, src="config", ar="TemplateNameAR"),
    col("TemplateNameAR", "text", False, src="config", lang="ar"),
    col("LanguageCode", "enum", True, enum="Language", src="config",
        note="A template is single-language; bilingual output is two approved templates (D-11)."),
    col("TextDirection", "text", True, src="config", validation="LTR|RTL",
        note="Derived from the language but stored explicitly so RTL is testable."),
    col("ProjectID", "ref", False, ref="Projects.ProjectID", src="config",
        note="Null means available to any project. Project-specific templates override (D-15 item 5)."),
    col("DisciplineID", "ref", False, ref="Disciplines.DisciplineID", src="config"),
    col("LegalEntityID", "ref", True, ref="LegalEntities.LegalEntityID", src="config"),
    col("StorageFileKey", "filekey", False, src="config",
        note="Reference to the controlled template file. No production file ID exists in Phase 1."),
    col("Version", "int", True, default="1", src="config"),
    col("EffectiveFrom", "date", True, src="config"),
    col("EffectiveTo", "date", False, src="config"),
    col("ApprovedByUserID", "ref", False, ref="Users.UserID", src="user"),
    col("Status", "text", True, default="Draft", src="config", validation="Draft|Approved|Superseded|Withdrawn"),
] + ACTIVE + AUDIT)

# --------------------------------------------------------------------------
# 2. Client and project master data
# --------------------------------------------------------------------------
table("Clients", "master", "global", "confidential", 1,
      "Clients the company works for. Bilingual names preserved exactly (D-11).",
      "العملاء", "ClientID", [
    col("ClientID", "id", True, key="pk", ex="CLI-D4F8T2"),
    col("LegalNameEN", "text", False, src="user", ar="LegalNameAR",
        note="Not required: a client may be registered only in Arabic. At least one legal name "
             "must be present (D-11)."),
    col("LegalNameAR", "text", False, src="user", lang="ar",
        note="Some clients are known only by an Arabic legal name; it is stored exactly as given "
             "and is never transliterated to fill an English column."),
    col("DisplayNameEN", "text", False, src="user", ar="DisplayNameAR"),
    col("DisplayNameAR", "text", False, src="user", lang="ar"),
    col("ClientKind", "text", True, src="user", validation="Government|SemiGovernment|Private|MainContractor"),
    col("BillingAddressEN", "longtext", False, src="user", sens="financial", ar="BillingAddressAR"),
    col("BillingAddressAR", "longtext", False, src="user", sens="financial", lang="ar"),
    col("TaxRegistrationNumber", "text", False, src="user", sens="financial",
        note="Hidden from field roles (spec 7.4)."),
    col("PrimaryContactID", "ref", False, ref="Contacts.ContactID", src="user"),
    col("PaymentTermsDays", "int", False, src="user", sens="financial"),
    col("Currency", "text", False, src="user", sens="financial", validation="ISO 4217"),
    col("DefaultClassificationCode", "enum", False, enum="DataClassificationCode", src="user",
        note="Baseline classification for this client's records (D-12)."),
    col("QuickBooksCustomerID", "text", False, src="integration", sens="financial",
        note="Immutable accounting identifier. Never name-matched (spec 8 scenario 10)."),
    col("Status", "text", True, default="Active", src="user", validation="Active|Suspended|Closed"),
] + ACTIVE + AUDIT,
      at_least_one=[["LegalNameEN", "LegalNameAR"], ["DisplayNameEN", "DisplayNameAR"]],
      notes=["A client registered only in Arabic is normal in Qatar. Forcing an English legal name "
             "would invite a transliteration that is not the client's legal name (D-11)."])

table("Contacts", "master", "global", "personal", 1,
      "Client contacts. Only an authorised recipient may receive a released document.",
      "جهات الاتصال لدى العملاء", "ContactID", [
    col("ContactID", "id", True, key="pk", ex="CON-B3H9L5"),
    col("ClientID", "ref", True, ref="Clients.ClientID", src="user"),
    col("NameEN", "text", False, src="user", ar="NameAR"),
    col("NameAR", "text", False, src="user", lang="ar"),
    col("PositionEN", "text", False, src="user", ar="PositionAR"),
    col("PositionAR", "text", False, src="user", lang="ar"),
    col("Email", "email", False, src="user", sens="personal"),
    col("Mobile", "phone", False, src="user", sens="personal"),
    col("PreferredLanguage", "enum", True, default="en", enum="Language", src="user"),
    col("IsAuthorizedRecipient", "bool", True, default="FALSE", src="user",
        note="Only TRUE contacts may appear in a release recipient snapshot."),
    col("Status", "text", True, default="Active", src="user", validation="Active|Inactive"),
] + ACTIVE + AUDIT,
      at_least_one=[["NameEN", "NameAR"]])

table("Projects", "master", "global", "confidential", 1,
      "A project is pure configuration. Adding one never requires changed logic, a cloned app, "
      "duplicated scenarios, rewritten prompts or changed code (D-01).",
      "المشاريع", "ProjectID", [
    col("ProjectID", "id", True, key="pk", ex="PRJ-K7M2Q1"),
    col("ProjectCode", "text", True, uniq=True, src="user",
        validation="Uppercase, no spaces, filename-safe", ex="EXAMPLE-CODE-01",
        note="Used in folder and file names. A display code, never a key."),
    col("ProjectNameEN", "text", True, src="user", ar="ProjectNameAR"),
    col("ProjectNameAR", "text", False, src="user", lang="ar"),
    col("LegalEntityID", "ref", True, ref="LegalEntities.LegalEntityID", src="user",
        note="Which registered entity issues this project's documents (D-02)."),
    col("ClientID", "ref", True, ref="Clients.ClientID", src="user"),
    col("ContractID", "ref", False, ref="Contracts.ContractID", src="user", sens="financial"),
    col("LocationSummaryEN", "text", False, src="user", ar="LocationSummaryAR"),
    col("LocationSummaryAR", "text", False, src="user", lang="ar"),
    col("StartDate", "date", True, src="user"),
    col("EndDate", "date", False, src="user", validation="Must be >= StartDate when present"),
    col("ReportingFrequency", "enum", True, enum="ReportingFrequency", src="user"),
    col("ReportingCutoffDay", "int", False, src="user", validation="1-28",
        note="Latest day evidence may be added to a closing period (OQ-02)."),
    col("DefaultTemplateID", "ref", False, ref="DocumentTemplates.TemplateID", src="user"),
    col("DefaultDocumentLanguage", "enum", True, default="en", enum="Language", src="user"),
    col("ProjectManagerUserID", "ref", False, ref="Users.UserID", src="user"),
    col("Currency", "text", True, src="user", sens="financial", validation="ISO 4217",
        note="Must match the contract currency; a mismatch is a validation failure (C-09)."),
    col("TimeZone", "text", True, default="Asia/Qatar", src="user"),
    col("BillingMethod", "enum", False, enum="BillingMethod", src="user", sens="financial"),
    col("PaymentTermsDays", "int", False, src="user", sens="financial"),
    col("AIAnalysisEnabled", "bool", True, default="TRUE", src="user",
        note="Set FALSE where a contract or residency rule forbids third-party AI processing (D-12)."),
    col("RetentionDays", "int", False, src="user",
        note="Overrides the classification default. Expiry flags for review, never auto-deletes."),
    col("DriveFolderKey", "filekey", False, src="integration",
        note="Provisioned folder reference. Empty in Phase 1 — nothing is connected (D-14)."),
    col("Status", "enum", True, default="Draft", enum="ProjectStatus", src="user"),
] + ACTIVE + AUDIT,
      notes=["Every project-varying behaviour is a column or a child row here, never a branch in code."])

table("ProjectAssignments", "master", "project", "internal", 1,
      "Which users may act on which project, and in what role. A user may be assigned to many "
      "projects, and a project may have many users (D-15 item 2).",
      "إسناد المستخدمين إلى المشاريع", "AssignmentID", [
    col("AssignmentID", "id", True, key="pk", ex="ASG-V7D1G6"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="user"),
    col("UserID", "ref", True, ref="Users.UserID", src="user"),
    col("RoleID", "ref", True, ref="Roles.RoleID", src="user",
        note="The role a user holds ON THIS PROJECT. It may differ from their default role."),
    col("AssignedFrom", "date", True, src="user"),
    col("AssignedTo", "date", False, src="user",
        note="Null means open-ended. An expired assignment grants nothing."),
    col("MaySubmitEvidence", "bool", True, default="TRUE", src="user"),
    col("MayReviewEvidence", "bool", True, default="FALSE", src="user"),
    col("MayRequestDocuments", "bool", True, default="FALSE", src="user"),
] + ACTIVE + AUDIT,
      unique_together=[["ProjectID", "UserID", "RoleID", "AssignedFrom"]],
      notes=["This table is the sole source of row-level access. Absence of a row means no access, "
             "and no view, slice or convenience field may substitute for it."])

table("Locations", "master", "project", "confidential", 1,
      "Hierarchical locations within a project. Choices are always filtered by project (spec 7.3).",
      "المواقع ضمن المشروع", "LocationID", [
    col("LocationID", "id", True, key="pk", ex="LOC-Z5J3D9"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="user"),
    col("LocationCode", "text", True, src="user", validation="Filename-safe; unique within project",
        ex="BLK-A"),
    col("LocationNameEN", "text", True, src="user", ar="LocationNameAR"),
    col("LocationNameAR", "text", False, src="user", lang="ar"),
    col("ParentLocationID", "ref", False, ref="Locations.LocationID", src="user",
        validation="Parent must belong to the SAME project; no cycles; max depth 5",
        note="Supports site > building > floor > room hierarchies (D-15 item 3)."),
    col("LocationKind", "text", False, src="user", validation="Site|Zone|Building|Floor|Room|Asset"),
    col("GPSLatitude", "decimal", False, src="device", scale=7,
        note="Evidence, not a gate. Missing is recorded as missing, never as zero (C-08)."),
    col("GPSLongitude", "decimal", False, src="device", scale=7),
    col("GeofenceRadiusM", "int", False, src="user",
        note="Out-of-geofence capture is flagged for the reviewer, never auto-rejected."),
    col("DisplayOrder", "int", True, default="100", src="user"),
] + ACTIVE + AUDIT,
      unique_together=[["ProjectID", "LocationCode"]])

table("ProjectActivityRules", "master", "project", "internal", 1,
      "Per-project overrides of the global activity and evidence rules (D-15 item 4). "
      "A project that needs a different rule gets a row, never a code change.",
      "قواعد الأنشطة والأدلة الخاصة بالمشروع", "ProjectActivityRuleID", [
    col("ProjectActivityRuleID", "id", True, key="pk", ex="PAR-X1B6M7"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="user"),
    col("ActivityTypeID", "ref", True, ref="ActivityTypes.ActivityTypeID", src="user"),
    col("IsPermitted", "bool", True, default="TRUE", src="user",
        note="FALSE removes the activity from this project's form without deleting history."),
    col("RequiresBeforePhoto", "bool", False, src="user", note="Null inherits the global rule."),
    col("RequiresAfterPhoto", "bool", False, src="user", note="Null inherits the global rule."),
    col("RequiresQuantity", "bool", False, src="user", note="Null inherits the global rule."),
    col("QuantityUnitID", "ref", False, ref="Units.UnitID", src="user"),
    col("MinPhotos", "int", False, src="user"),
    col("RequiresCaption", "bool", False, src="user"),
    col("BOQItemHint", "text", False, src="user", sens="financial",
        note="Optional link to the billing item, used from Phase 6."),
] + ACTIVE + AUDIT,
      unique_together=[["ProjectID", "ActivityTypeID"]])

table("ApprovalMatrix", "master", "project", "internal", 1,
      "Who approves what, per project and stage (D-09, D-15 item 6). The GM is the MVP approver, "
      "and the structure supports delegation without redesign.",
      "مصفوفة الاعتمادات", "ApprovalMatrixID", [
    col("ApprovalMatrixID", "id", True, key="pk", ex="APM-C2S9W3"),
    col("ProjectID", "ref", False, ref="Projects.ProjectID", src="user",
        note="Null means the company-wide default for this stage."),
    col("ApprovalStage", "enum", True, enum="ApprovalStage", src="user"),
    col("DocumentTypeCode", "enum", False, enum="DocumentTypeCode", src="user",
        note="Null applies to every document type."),
    col("ResponsibleUserID", "ref", True, ref="Users.UserID", src="user",
        note="The accountable approver. A delegate acts FOR this person, never instead of them."),
    col("BackupUserID", "ref", False, ref="Users.UserID", src="user",
        note="May remain unassigned until before go-live (D-09)."),
    col("SequenceNumber", "int", True, default="1", src="user",
        note="Supports multi-step approval within a stage."),
    col("SelfApprovalProhibited", "bool", True, default="TRUE", src="config",
        note="No user may approve their own restricted transaction because an approver is "
             "unavailable (D-09). This is not configurable to FALSE for financial stages."),
] + ACTIVE + AUDIT)

table("ApprovalDelegations", "master", "global", "internal", 1,
      "Temporary delegation of an approval authority (D-09). Every delegated decision records both "
      "the acting user and the original responsible user.",
      "تفويض صلاحيات الاعتماد مؤقتاً", "DelegationID", [
    col("DelegationID", "id", True, key="pk", ex="DEL-N5T8J4"),
    col("FromUserID", "ref", True, ref="Users.UserID", src="user",
        note="The original responsible approver."),
    col("ToUserID", "ref", True, ref="Users.UserID", src="user",
        note="The acting delegate. May be unassigned until before go-live."),
    col("ApprovalStage", "enum", False, enum="ApprovalStage", src="user",
        note="Null delegates every stage the delegator holds."),
    col("Scope", "enum", True, enum="DelegationScope", src="user"),
    col("ProjectIDs", "text", False, src="user",
        note="Comma-separated ProjectIDs when Scope = SpecificProjects."),
    col("ValidFrom", "datetime", True, src="user"),
    col("ValidTo", "datetime", True, src="user",
        validation="Must be after ValidFrom. An open-ended delegation is not permitted."),
    col("Reason", "text", True, src="user"),
    col("AuthorisedByUserID", "ref", True, ref="Users.UserID", src="user"),
    col("RevokedAt", "datetime", False, src="user"),
    col("RevokedByUserID", "ref", False, ref="Users.UserID", src="user"),
] + ACTIVE + AUDIT,
      notes=["A delegation is evidence, so it is never deleted — it is revoked, with a timestamp."])

table("ResidencyAssignments", "master", "project", "internal", 1,
      "Binds a residency requirement to a client, contract or project (D-12).",
      "ربط متطلبات الإقامة بالبيانات", "ResidencyAssignmentID", [
    col("ResidencyAssignmentID", "id", True, key="pk", ex="RSA-L6P4Z8"),
    col("ResidencyRequirementID", "ref", True, ref="ResidencyRequirements.ResidencyRequirementID", src="user"),
    col("AppliesToKind", "text", True, src="user", validation="Client|Contract|Project"),
    col("ClientID", "ref", False, ref="Clients.ClientID", src="user"),
    col("ContractID", "ref", False, ref="Contracts.ContractID", src="user"),
    col("ProjectID", "ref", False, ref="Projects.ProjectID", src="user"),
    col("EffectiveFrom", "date", True, src="user"),
    col("EffectiveTo", "date", False, src="user"),
    col("VerifiedFromContract", "bool", True, default="FALSE", src="user",
        note="FALSE means the contract has not yet been reviewed — production upload stays blocked."),
] + ACTIVE + AUDIT)

# --------------------------------------------------------------------------
# 3. Operational records
# --------------------------------------------------------------------------
table("SiteVisits", "operational", "project", "confidential", 1,
      "One reporting event at a location on a date. The unit of submission and review.",
      "زيارة موقع", "VisitID", [
    col("VisitID", "id", True, key="pk", ex="VIS-Q8C4K1"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="system", hash=True,
        auto="Prefilled from the supervisor's single active assignment, or from the last project "
             "used today, or from the project default.",
        prompts_user="only when the supervisor holds more than one active assignment and no "
                     "default resolves — a genuine choice, not a routine question",
        note="Required in storage, never a routine question (D-22). Trusted system data; never "
             "inferred from a photograph (D-19)."),
    col("LocationID", "ref", True, ref="Locations.LocationID", src="system", hash=True,
        validation="Location must belong to ProjectID",
        auto="Prefilled from the project's default location, or the last location used today.",
        prompts_user="only when the project has several active locations and none resolves",
        note="Required in storage, confirmed rather than typed (D-22)."),
    col("WorkOrderID", "ref", False, ref="WorkOrders.WorkOrderID", src="user", hash=True),
    col("VisitDate", "date", True, src="device", hash=True,
        auto="The device date, captured automatically.",
        note="Never typed on the normal path. Correctable by an authorised user (spec 7.3)."),
    col("StartTime", "time", False, src="device", hash=True,
        auto="The device time at the first capture in the batch."),
    col("EndTime", "time", False, src="device", hash=True,
        validation="Must be after StartTime",
        auto="The device time at the last capture in the batch."),
    col("Weather", "text", False, src="user", hash=True),
    col("SupervisorUserID", "ref", True, ref="Users.UserID", src="system", hash=True,
        auto="The signed-in user. Never selected, never typed.",
        note="Resolved from the authenticated identity; must hold an active assignment to "
             "ProjectID."),
    col("GPSLatitude", "decimal", False, src="device", scale=7),
    col("GPSLongitude", "decimal", False, src="device", scale=7),
    col("OverallDescriptionEN", "longtext", False, src="user", hash=True, ar="OverallDescriptionAR",
        optional_by_design=True,
        validation="Optional for a normal photographic submission (D-18)",
        note="NOT mandatory. A normal submission is established by photographs. A written "
             "description is required only in the declared exceptional workflows."),
    col("OverallDescriptionAR", "longtext", False, src="user", hash=True, lang="ar",
        optional_by_design=True,
        validation="Optional for a normal photographic submission (D-18)",
        note="A supervisor may write in either language; both are carried to the report (D-11)."),
    col("AdditionalSiteNote", "longtext", False, src="user", hash=True,
        optional_by_design=True,
        validation="Optional. Mandatory only in the exceptional workflows listed in "
                   "capture_once.optional_note.mandatory_exceptions",
        note="For facts a photograph cannot establish (D-18). Speech-to-text is a future input "
             "method for this field, not a new field."),
    col("SiteNoteCategory", "enum", False, enum="SiteNoteCategory", src="user", hash=True,
        note="Classifies the optional note so it can be routed and reported. Never inferred by AI."),
    col("CaptureMode", "enum", True, default="QuickShare", enum="CaptureMode", src="system",
        auto="Defaults to Quick Share on every visit.",
        prompts_user="never on the normal path — AI Reviewed Share is chosen deliberately, by an "
                     "explicit action, when a reviewed caption is wanted before sharing",
        note="Quick Share is the default so the contractor group is served first and nothing is "
             "waited for (D-22). Both modes capture the images exactly once (D-16)."),
    col("ShareStatus", "enum", True, default="NotShared", enum="ShareStatus", src="user",
        note="Recorded from the supervisor's confirmation. The app cannot observe delivery inside "
             "the messaging application."),
    col("SharedAt", "datetime", False, src="system"),
    col("SharedByUserID", "ref", False, ref="Users.UserID", src="system"),
    col("ShareTargetLabel", "text", False, src="config",
        note="A label for the destination group, held as project configuration. NEVER a telephone "
             "number, group invitation link or messaging identifier (D-19)."),
    col("ShareAttemptCount", "int", True, default="0", src="system",
        note="Incremented on every share attempt. A retry re-uses the stored evidence and must "
             "never ask the supervisor to select the images again (CAP-01)."),
    col("SafetyObservation", "longtext", False, src="user", hash=True),
    col("ClientRepresentative", "text", False, src="user", hash=True, sens="personal"),
    col("ClientAcknowledgementStatus", "text", False, src="user", hash=True,
        validation="NotRequested|Claimed|Declined",
        note="A CLAIM recorded on site. Never treated as a client approval (A-20)."),
    col("WorkflowStatus", "enum", True, default="Draft", enum="WorkflowStatus", src="system"),
    col("SubmittedAt", "datetime", False, src="system"),
    col("TechnicalReviewedAt", "datetime", False, src="system"),
    col("TechnicalReviewedBy", "ref", False, ref="Users.UserID", src="system"),
    col("RejectionReason", "longtext", False, src="user",
        note="Mandatory when returning a record for correction."),
    col("ValidationErrors", "json", False, src="system",
        note="Specific correctable errors from server-side validation, never a generic message."),
    col("CorrelationID", "text", False, src="system",
        note="Links this record to its orchestration jobs and audit entries."),
] + VERSIONED + AUDIT,
      content_hash=["ProjectID", "LocationID", "WorkOrderID", "VisitDate", "StartTime", "EndTime",
                    "Weather", "SupervisorUserID", "OverallDescriptionEN", "OverallDescriptionAR",
                    "SafetyObservation", "ClientRepresentative", "ClientAcknowledgementStatus"])

table("VisitActivities", "operational", "project", "confidential", 1,
      "What was actually done during a visit. One row per activity.",
      "أنشطة الزيارة", "VisitActivityID", [
    col("VisitActivityID", "id", True, key="pk", ex="VAC-T3N6B7"),
    col("VisitID", "ref", True, ref="SiteVisits.VisitID", src="system", hash=True),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="system", hash=True,
        note="Denormalised for row-level security; must equal the parent visit's project."),
    col("ActivityTypeID", "ref", True, ref="ActivityTypes.ActivityTypeID", src="user", hash=True,
        validation="Must be permitted for the project by ProjectActivityRules"),
    col("DescriptionEN", "longtext", False, src="user", hash=True, ar="DescriptionAR"),
    col("DescriptionAR", "longtext", False, src="user", hash=True, lang="ar"),
    col("Quantity", "decimal", False, src="user", hash=True, scale=3,
        validation="Numeric, >= 0, present only where the effective rule requires it"),
    col("UnitID", "ref", False, ref="Units.UnitID", src="user", hash=True),
    col("PercentComplete", "int", False, src="user", hash=True, validation="0-100",
        note="Entered by a human. NEVER inferred by AI (spec 5.9, ADR-0004)."),
    col("EvidenceStatus", "text", True, default="Incomplete", src="system",
        validation="Incomplete|Complete|Waived",
        note="Computed from the effective evidence rule, not typed."),
    col("SupervisorConfirmation", "bool", True, default="FALSE", src="user",
        note="An authorised human confirmation. One of the only two bases for a completion "
             "statement, the other being approved evidence (operating rule 11)."),
    col("TechnicalReviewerComment", "longtext", False, src="user"),
    col("Status", "enum", True, default="Draft", enum="VisitActivityStatus", src="system"),
] + VERSIONED + AUDIT,
      content_hash=["VisitID", "ActivityTypeID", "DescriptionEN", "DescriptionAR", "Quantity",
                    "UnitID", "PercentComplete", "SupervisorConfirmation"])

table("Photos", "operational", "project", "confidential", 1,
      "One photograph per row. The received file is write-once and is never altered (D-13).",
      "الصور الفوتوغرافية كأدلة", "PhotoID", [
    col("PhotoID", "id", True, key="pk", ex="PHO-M9F2X5"),
    col("VisitID", "ref", True, ref="SiteVisits.VisitID", src="system", hash=True),
    col("VisitActivityID", "ref", False, ref="VisitActivities.VisitActivityID", src="system",
        hash=True,
        note="Optional. A photograph belongs to a visit; it is attached to an activity only once "
             "one has been confirmed. A photographic submission with no activity at all is valid "
             "(D-22)."),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="system", hash=True,
        note="Denormalised for row-level security and for folder routing."),
    col("LocationID", "ref", True, ref="Locations.LocationID", src="system", hash=True),
    col("CapturedAt", "datetime", False, src="device",
        note="Device capture time where available. Drives the old-photo warning, never a rejection."),
    col("ReceivedAt", "datetime", True, src="system",
        note="When the controlled system first received the file. The anchor of the write-once "
             "guarantee (D-13)."),
    col("UploadedAt", "datetime", False, src="system"),
    col("CapturedBy", "ref", True, ref="Users.UserID", src="system",
        note="The uploader identity recorded with the original (D-13)."),
    col("OriginalFileKey", "filekey", True, src="system",
        note="WRITE-ONCE. Never overwritten, altered, annotated, resized or deleted."),
    col("OriginalChecksum", "checksum", False, src="integration",
        note="Taken from the storage provider's own file metadata where available (C-03); "
             "computed only as a fallback."),
    col("ChecksumAlgorithm", "text", False, src="integration", ex="MD5",
        note="Recorded so the value is interpretable years later."),
    col("OriginalMimeType", "text", False, src="integration"),
    col("OriginalWidth", "int", False, src="integration"),
    col("OriginalHeight", "int", False, src="integration"),
    col("OriginalSizeBytes", "int", False, src="integration"),
    col("IsOriginalDeviceImageVerified", "bool", True, default="FALSE", src="system",
        note="Stays FALSE until real-device testing proves no upstream re-encoding. No file may be "
             "described as the original device image while this is FALSE (D-13)."),
    col("EvidenceStage", "enum", False, enum="EvidenceStage", src="user", hash=True,
        optional_by_design=True,
        validation="Optional at capture (D-22). Never a mandatory manual field before the "
                   "photograph is taken",
        auto="Proposed by analysis into AIProposedEvidenceStage, or pre-tagged from the activity "
             "rule's default stages, or left Pending for review.",
        note="A supervisor may set it, and often will not. An unclassified photograph is valid "
             "evidence and blocks no submission; ClassificationStatus carries how far it has got."),
    col("CaptionEN", "text", False, src="user", hash=True, ar="CaptionAR",
        validation="Mandatory for Snag, Observation, Material and Safety stages",
        note="The supervisor's own words. Never overwritten by AI (D-06)."),
    col("CaptionAR", "text", False, src="user", hash=True, lang="ar"),
    col("GPSLatitude", "decimal", False, src="device", scale=7),
    col("GPSLongitude", "decimal", False, src="device", scale=7),
    col("CaptureBatchID", "text", False, src="system",
        note="Groups the photographs captured in one action, so the share and the report both "
             "re-use the same stored set. The mechanism behind capture once, use twice (CAP-01)."),
    col("CaptureSequence", "int", False, src="system",
        note="Order within the capture batch. Share order and report order derive from this; the "
             "supervisor never re-orders by re-selecting files."),
    col("IsDuplicateSuspected", "bool", True, default="FALSE", src="system",
        note="Flag only. A suspected duplicate is never deleted or merged (S-09)."),
    col("DuplicateOfPhotoID", "ref", False, ref="Photos.PhotoID", src="system"),
    col("AIAnalysisStatus", "enum", True, default="NotRequested", enum="AIAnalysisStatus", src="system"),
    col("AnalysisEligibility", "enum", True, default="Eligible", enum="AnalysisEligibility",
        src="system",
        note="Decided BEFORE any call is made (D-24). A duplicate, an unusable image, a deleted "
             "or excluded one, and an already-analysed one all cost nothing."),
    col("PerceptualHash", "text", False, src="system",
        note="Computed at registration for near-duplicate detection. A flag only: a suspected "
             "duplicate is never deleted or merged (S-09)."),
    col("QualityScore", "decimal", False, src="system", scale=2, validation="0.00-1.00",
        note="Local blur/exposure measure computed without a model call. Below the project "
             "threshold the photograph is retained as evidence and skipped for analysis."),
    col("AIObservation", "json", False, src="ai",
        advisory=True,
        note="ADVISORY ONLY. Schema-validated output, displayed as an AI observation, visually "
             "distinct from the caption and the reviewer decision (D-06)."),
    col("AIProposedEvidenceStage", "enum", False, enum="EvidenceStage", src="ai", advisory=True,
        note="A PROPOSAL. Never written to EvidenceStage. The supervisor confirms or corrects it "
             "(D-17)."),
    col("AIProposedActivityText", "text", False, src="ai", advisory=True,
        note="Free text describing the visible activity. Untrusted. Never becomes the structured "
             "activity by itself (D-20, D-23)."),
    col("AIProposedActivityTypeID", "ref", False, ref="ActivityTypes.ActivityTypeID", src="ai",
        advisory=True, candidate_only=True,
        validation="Advisory candidate only. No report, rule, calculation, filter or join may read "
                   "this column",
        note="A CANDIDATE code the analysis suggests, held in a typed column so it can be shown "
             "beside the catalogue entry it points at. It is not the activity: nothing reads it "
             "except the confirmation screen, and confirming copies the value into "
             "ConfirmedActivityTypeID by an explicit human action (D-23)."),
    col("ConfirmedActivityTypeID", "ref", False, ref="ActivityTypes.ActivityTypeID", src="user",
        hash=True, trusted=True,
        validation="Must be permitted for the project by the effective activity rule",
        note="**The trusted structured activity.** Set only by a supervisor or reviewer, and only "
             "when ClassificationStatus becomes Confirmed. Reports and business rules read this "
             "column and no other (D-23)."),
    col("ClassificationStatus", "enum", True, default="Pending", enum="ClassificationStatus",
        src="system", hash=True,
        note="Pending is normal after a Quick Share and blocks nothing. Only Confirmed makes the "
             "activity trusted (D-23)."),
    col("ConfirmedByUserID", "ref", False, ref="Users.UserID", src="system",
        note="Who confirmed the classification. Attribution is the point."),
    col("ConfirmedAt", "datetime", False, src="system"),
    col("QuarantineStatus", "enum", True, default="NotQuarantined", enum="QuarantineStatus",
        src="system",
        note="Set by the system when access is revoked while evidence is still queued (D-25). "
             "Only NotQuarantined and AcceptedIntoProject are readable by a report, a "
             "calculation, an approval or a document."),
    col("AccessRevokedAt", "datetime", False, src="system",
        note="When the capturing user's access ended. The dividing line: evidence captured "
             "BEFORE it may complete into quarantine, evidence captured AFTER it is refused."),
    col("UploadCompletedAt", "datetime", False, src="system",
        note="When the upload was confirmed. No local original may be deleted before this is "
             "set (D-25, CAP-GATE G-4)."),
    col("QuarantinedAt", "datetime", False, src="system"),
    col("QuarantineReviewedByUserID", "ref", False, ref="Users.UserID", src="system",
        note="Who accepted or rejected the quarantined evidence. Never the revoked user."),
    col("QuarantineReviewedAt", "datetime", False, src="system"),
    col("QuarantineRejectionReason", "longtext", False, src="user",
        note="MANDATORY when QuarantineStatus is Rejected (D-25). Rejecting evidence without "
             "saying why is how evidence disappears quietly."),
    col("AIProposedCaptionEN", "text", False, src="ai", advisory=True, ar="AIProposedCaptionAR",
        note="Proposed professional caption. Copied into CaptionEN only by a human action."),
    col("AIProposedCaptionAR", "text", False, src="ai", advisory=True, lang="ar"),
    col("AIVisibleCondition", "text", False, src="ai", advisory=True,
        note="Visible condition only. Never a cause, never a compliance judgement (D-20)."),
    col("AIPossibleSnag", "bool", False, src="ai", advisory=True,
        note="Raises a question for the supervisor. Creates no Snag record by itself."),
    col("AIImageQualityWarning", "text", False, src="ai", advisory=True,
        note="Blur, exposure, obstruction, framing. Advisory; never blocks a submission."),
    col("AIUncertaintyNote", "text", False, src="ai", advisory=True,
        note="What the model could not determine. Required by the analysis schema so that "
             "uncertainty is stated rather than hidden."),
    col("AIProposalDisposition", "enum", True, default="NotOffered",
        enum="AIProposalDisposition", src="user",
        note="What the supervisor did with the proposal. Set only by a human (D-17)."),
    col("AIAnalysedAt", "datetime", False, src="system",
        note="In Quick Share this is later than SharedAt, by design."),
    col("AIConfidence", "decimal", False, src="ai", scale=2, validation="0.00-1.00",
        note="Advisory. Never a threshold for automatic approval."),
    col("AIModel", "text", False, src="ai", note="Recorded for reproducibility."),
    col("AIPromptVersion", "text", False, src="ai"),
    col("AIContradictsCaption", "bool", False, src="ai",
        note="Raised for the reviewer's attention; resolves nothing by itself."),
    col("ReviewerDecision", "enum", True, default="Pending", enum="ReviewerDecision", src="user",
        note="Set only by a human reviewer. AI may never write this field."),
    col("ReviewerComment", "longtext", False, src="user"),
    col("ReviewedByUserID", "ref", False, ref="Users.UserID", src="system"),
    col("ReviewedAt", "datetime", False, src="system"),
    col("ApprovedForReport", "bool", True, default="FALSE", src="system", hash=True,
        note="Derived from ReviewerDecision = Approved. Only human-approved evidence may appear in "
             "an official report (D-06)."),
    col("ReportSequence", "int", False, src="user", hash=True),
    col("DerivedFileKey", "filekey", False, src="system",
        note="Report-ready or downscaled derivative, stored SEPARATELY from the original (D-13)."),
    col("ClassificationCode", "enum", True, default="ClientConfidential",
        enum="DataClassificationCode", src="system",
        note="Drives residency and sharing decisions (D-12)."),
] + VERSIONED + AUDIT,
      content_hash=["VisitID", "VisitActivityID", "LocationID", "EvidenceStage",
                    "ConfirmedActivityTypeID", "CaptionEN", "CaptionAR", "ApprovedForReport",
                    "ReportSequence"],
      notes=["Advisory AI fields are deliberately excluded from ContentHash: an AI observation "
             "arriving later must not void a human approval (C-06)."])

table("Snags", "operational", "project", "confidential", 1,
      "Defects and observations tracked to closure with evidence.", "الملاحظات وعدم المطابقات",
      "SnagID", [
    col("SnagID", "id", True, key="pk", ex="SNG-H4L8R2"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="system"),
    col("LocationID", "ref", True, ref="Locations.LocationID", src="user"),
    col("VisitID", "ref", False, ref="SiteVisits.VisitID", src="system"),
    col("VisitActivityID", "ref", False, ref="VisitActivities.VisitActivityID", src="system"),
    col("SourcePhotoID", "ref", False, ref="Photos.PhotoID", src="user"),
    col("Category", "text", True, src="user"),
    col("Severity", "enum", True, enum="SnagSeverity", src="user"),
    col("DescriptionEN", "longtext", True, src="user", ar="DescriptionAR"),
    col("DescriptionAR", "longtext", False, src="user", lang="ar"),
    col("RaisedAt", "datetime", True, src="system"),
    col("RaisedBy", "ref", True, ref="Users.UserID", src="system"),
    col("ResponsibleParty", "text", False, src="user"),
    col("TargetDate", "date", False, src="user"),
    col("Status", "enum", True, default="Open", enum="SnagStatus", src="user"),
    col("ClosureDate", "date", False, src="user", validation="Required when Status = Closed"),
    col("ClosureEvidencePhotoID", "ref", False, ref="Photos.PhotoID", src="user",
        validation="Required when Status = Closed",
        note="A snag cannot be closed on assertion alone."),
    col("VerifiedBy", "ref", False, ref="Users.UserID", src="system",
        validation="Required when Status = Closed"),
    col("VerificationDate", "date", False, src="system"),
] + ACTIVE + AUDIT)

# --------------------------------------------------------------------------
# 4. Document production
# --------------------------------------------------------------------------
table("DocumentJobs", "document", "project", "internal", 5,
      "A request to produce a document from a frozen snapshot of approved records.",
      "مهام إنشاء المستندات", "JobID", [
    col("JobID", "id", True, key="pk", ex="JOB-S4M7B1"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="user"),
    col("LegalEntityID", "ref", True, ref="LegalEntities.LegalEntityID", src="system"),
    col("DocumentTypeCode", "enum", True, enum="DocumentTypeCode", src="user"),
    col("LanguageCode", "enum", True, default="en", enum="Language", src="user"),
    col("PeriodStart", "date", True, src="user"),
    col("PeriodEnd", "date", True, src="user", validation="Must be >= PeriodStart"),
    col("RequestedBy", "ref", True, ref="Users.UserID", src="system",
        validation="Must hold MayRequestDocuments on ProjectID"),
    col("RequestedAt", "datetime", True, src="system"),
    col("InputValidationStatus", "text", True, default="NotRun", src="system",
        validation="NotRun|Passed|Failed"),
    col("InputValidationFindings", "json", False, src="system",
        note="Explicit DATA GAP items rather than silent omissions."),
    col("SnapshotManifest", "json", False, src="system",
        note="Frozen list of included record IDs with their EntityVersion and ContentHash. "
             "Later edits cannot silently alter a draft (spec 8 scenario 05)."),
    col("SnapshotFrozenAt", "datetime", False, src="system"),
    col("WorkflowStatus", "enum", True, default="Requested", enum="JobStatus", src="system"),
    col("AIModel", "text", False, src="system"),
    col("PromptVersion", "text", False, src="system"),
    col("ReservedNumberID", "ref", False, ref="NumberRegister.NumberID", src="system",
        note="A number reserved for this job; cancelled if the job fails (D-10)."),
    col("StartedAt", "datetime", False, src="system"),
    col("FinishedAt", "datetime", False, src="system"),
    col("ErrorClass", "enum", False, enum="FailureClass", src="system"),
    col("ErrorMessage", "longtext", False, src="system", note="Sanitised. Never contains a secret."),
    col("RetryCount", "int", True, default="0", src="system"),
    col("CorrelationID", "text", True, src="system"),
] + AUDIT)

table("Documents", "document", "project", "confidential", 5,
      "A produced document revision. Approval binds to ContentHash (ADR-0006).",
      "المستندات المنتجة", "DocumentID", [
    col("DocumentID", "id", True, key="pk", ex="DOC-Y2R5T9"),
    col("JobID", "ref", True, ref="DocumentJobs.JobID", src="system"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="system"),
    col("LegalEntityID", "ref", True, ref="LegalEntities.LegalEntityID", src="system"),
    col("DocumentTypeCode", "enum", True, enum="DocumentTypeCode", src="system"),
    col("TemplateID", "ref", True, ref="DocumentTemplates.TemplateID", src="system"),
    col("LanguageCode", "enum", True, enum="Language", src="system"),
    col("DocumentNumber", "text", False, uniq=True, src="system",
        note="Issued by the numbering service at creation (D-10)."),
    col("VersionNumber", "int", True, default="1", src="system"),
    col("RevisionLabel", "text", False, src="system", ex="Rev.0"),
    col("DraftFileKey", "filekey", False, src="system"),
    col("PDFFileKey", "filekey", False, src="system"),
    col("ContentHash", "checksum", True, src="system", hash=True,
        note="Recomputed and compared before any release, posting or send."),
    col("TechnicalApprovalStatus", "text", True, default="Pending", src="system",
        validation="Pending|Approved|Rejected|Void"),
    col("FinancialApprovalStatus", "text", True, default="NotRequired", src="system",
        validation="NotRequired|Pending|Approved|Rejected|Void"),
    col("ReleaseStatus", "enum", True, default="Draft", enum="DocumentStatus", src="system"),
    col("ReleasedAt", "datetime", False, src="system"),
    col("ReleasedBy", "ref", False, ref="Users.UserID", src="system"),
    col("RecipientSnapshot", "json", False, src="system",
        note="Authorised recipients as they were AT RELEASE. Later contact edits cannot rewrite "
             "history."),
    col("SupersedesDocumentID", "ref", False, ref="Documents.DocumentID", src="system"),
    col("ClassificationCode", "enum", True, default="ClientConfidential",
        enum="DataClassificationCode", src="system"),
] + AUDIT)

table("NumberRegister", "document", "global", "internal", 5,
      "Every number ever reserved, issued or cancelled. A cancelled number is never reused (D-10).",
      "سجل أرقام المستندات", "NumberID", [
    col("NumberID", "id", True, key="pk", ex="NUM-J7V3F4"),
    col("SeriesID", "ref", True, ref="NumberingSeries.SeriesID", src="system"),
    col("SequenceValue", "int", True, src="system"),
    col("FormattedNumber", "text", True, uniq=True, src="system", ex="{ENTITY}-TR-2026-001 (illustrative)"),
    col("YearKey", "text", True, src="system", ex="2026"),
    col("ScopeKey", "text", True, src="system",
        note="Partition key: company-wide, project or client, per the series configuration."),
    col("State", "enum", True, default="Reserved", enum="NumberState", src="system"),
    col("ReservedForJobID", "ref", False, ref="DocumentJobs.JobID", src="system"),
    col("IssuedToDocumentID", "ref", False, ref="Documents.DocumentID", src="system"),
    col("ReservedAt", "datetime", True, src="system"),
    col("IssuedAt", "datetime", False, src="system"),
    col("CancelledAt", "datetime", False, src="system"),
    col("CancellationReason", "text", False, src="system",
        validation="Required when State = Cancelled",
        note="A gap in the register must always be explainable."),
    col("MigratedFromManual", "bool", True, default="FALSE", src="system",
        note="TRUE for numbers imported from the existing manual register."),
] + AUDIT,
      unique_together=[["SeriesID", "YearKey", "ScopeKey", "SequenceValue"]])

# --------------------------------------------------------------------------
# 5. Control tables
# --------------------------------------------------------------------------
table("Approvals", "control", "project", "internal", 1,
      "Every approval decision, bound to the exact content approved (ADR-0006, D-09).",
      "قرارات الاعتماد", "ApprovalID", [
    col("ApprovalID", "id", True, key="pk", ex="APR-B5X8N2"),
    col("EntityType", "text", True, src="system", validation="Table name"),
    col("EntityID", "text", True, src="system"),
    col("ProjectID", "ref", False, ref="Projects.ProjectID", src="system",
        note="Carried for row-level security even on control records."),
    col("ApprovalStage", "enum", True, enum="ApprovalStage", src="system"),
    col("SequenceNumber", "int", True, default="1", src="system"),
    col("RequestedFromUserID", "ref", True, ref="Users.UserID", src="system",
        note="The ACCOUNTABLE approver from the approval matrix."),
    col("RequestedAt", "datetime", True, src="system"),
    col("Decision", "enum", True, default="Pending", enum="ApprovalDecision", src="user"),
    col("DecisionAt", "datetime", False, src="system"),
    col("DecisionByUserID", "ref", False, ref="Users.UserID", src="system",
        note="The ACTING user. Differs from RequestedFromUserID only under a valid delegation."),
    col("DelegationID", "ref", False, ref="ApprovalDelegations.DelegationID", src="system",
        validation="Required when DecisionByUserID != RequestedFromUserID"),
    col("Comment", "longtext", False, src="user"),
    col("EntityVersion", "int", True, src="system"),
    col("ContentHash", "checksum", True, src="system",
        note="The approval applies to THIS hash only. A change voids it and everything downstream."),
    col("VoidedAt", "datetime", False, src="system"),
    col("VoidReason", "text", False, src="system"),
    col("IsOverride", "bool", True, default="FALSE", src="system",
        note="An override is recorded AS an override, with a reason. Never silent (SEC-05)."),
    col("OverrideReason", "longtext", False, src="user", validation="Required when IsOverride"),
] + AUDIT,
      notes=["Self-approval of a restricted transaction is rejected even when the approver is "
             "unavailable; the correct path is a recorded delegation (D-09)."])

table("EntityVersions", "control", "project", "internal", 1,
      "Immutable version history of hashable entities. Supports proving what a decision applied to.",
      "سجل نسخ السجلات", "VersionID", [
    col("VersionID", "id", True, key="pk", ex="VER-K1G6D7"),
    col("EntityType", "text", True, src="system"),
    col("EntityID", "text", True, src="system"),
    col("ProjectID", "ref", False, ref="Projects.ProjectID", src="system"),
    col("VersionNumber", "int", True, src="system"),
    col("ContentHash", "checksum", True, src="system"),
    col("CanonicalFieldSetVersion", "text", True, src="system",
        note="Which canonical field list produced this hash. Changing the list is a migration."),
    col("ChangedByUserID", "ref", True, ref="Users.UserID", src="system"),
    col("ChangedAt", "datetime", True, src="system"),
    col("ChangeSummary", "text", False, src="system",
        note="Which hashed fields changed. Never the full payload."),
    col("InvalidatedApprovalIDs", "text", False, src="system",
        note="Approvals voided by this change, recorded at the moment it happened."),
] + AUDIT,
      unique_together=[["EntityType", "EntityID", "VersionNumber"]])

table("AuditLog", "control", "global", "internal", 1,
      "Append-only record of every state transition and every consequential action.",
      "سجل التدقيق", "AuditID", [
    col("AuditID", "id", True, key="pk", ex="AUD-P9C4L3"),
    col("TimestampUTC", "datetime", True, src="system"),
    col("UserOrService", "text", True, src="system"),
    col("Action", "text", True, src="system", ex="SiteVisit.Submit"),
    col("EntityType", "text", True, src="system"),
    col("EntityID", "text", True, src="system"),
    col("ProjectID", "ref", False, ref="Projects.ProjectID", src="system"),
    col("BeforeHash", "checksum", False, src="system"),
    col("AfterHash", "checksum", False, src="system"),
    col("SourceIPOrDevice", "text", False, src="system", note="Where available. Not fabricated."),
    col("CorrelationID", "text", False, src="system"),
    col("Result", "text", True, src="system", validation="Success|Failure|Denied"),
    col("Reason", "text", False, src="system"),
] + [],
      notes=["Append-only. No update or delete path exists for any role, including every kind of administrator and break-glass access.",
             "Never stores an access token, a credential or a full sensitive payload."])

table("IntegrationJobs", "control", "global", "internal", 3,
      "One row per external call attempt, with idempotency and failure classification.",
      "سجل عمليات التكامل الخارجي", "IntegrationJobID", [
    col("IntegrationJobID", "id", True, key="pk", ex="INT-T6Z2W8"),
    col("SystemName", "text", True, src="system", ex="Drive"),
    col("OperationName", "text", True, src="system"),
    col("IdempotencyKey", "text", True, src="system",
        note="{Scenario}:{EntityType}:{EntityID}:{TargetState}. Claimed BEFORE any side effect."),
    col("CorrelationID", "text", True, src="system"),
    col("EntityType", "text", True, src="system"),
    col("EntityID", "text", True, src="system"),
    col("ProjectID", "ref", False, ref="Projects.ProjectID", src="system"),
    col("AttemptNumber", "int", True, default="1", src="system"),
    col("StartedAt", "datetime", True, src="system"),
    col("FinishedAt", "datetime", False, src="system"),
    col("Status", "enum", True, default="Pending", enum="IntegrationStatus", src="system"),
    col("SanitizedRequestSummary", "text", False, src="system",
        note="Summary only. Never a payload, a credential or a token."),
    col("SanitizedResponseSummary", "text", False, src="system"),
    col("ErrorClass", "enum", False, enum="FailureClass", src="system"),
    col("ErrorCode", "text", False, src="system"),
    col("RetryAfter", "datetime", False, src="system"),
    col("IsRetriable", "bool", True, default="FALSE", src="system",
        note="Derived from ErrorClass. Validation and authorisation failures are never retried."),
] + [],
      unique_together=[["IdempotencyKey", "AttemptNumber"]])

table("TemporaryAccessGrants", "control", "global", "internal", 1,
      "Time-bound, explicitly authorised access. Covers auditor access and break-glass emergency "
      "access. Without an active grant, the roles that depend on one resolve to no access at all.",
      "صلاحيات وصول مؤقتة ومحددة بزمن", "GrantID", [
    col("GrantID", "id", True, key="pk", ex="TAG-P4K9M2"),
    col("GrantKind", "text", True, src="user", validation="Audit|Emergency|Support",
        note="Audit: a time-bound review. Emergency: break-glass. Support: a bounded "
             "investigation by an administrator into their own technical scope."),
    col("UserID", "ref", True, ref="Users.UserID", src="user",
        note="The individual receiving the grant. A grant is never issued to a shared account."),
    col("RoleID", "ref", True, ref="Roles.RoleID", src="user",
        note="The role the grant activates. It can never exceed that role's own matrix."),
    col("Scope", "text", True, src="user", validation="AllProjects|SpecificProjects|TechnicalOnly",
        note="TechnicalOnly is the break-glass default: administrative capability, no business "
             "content."),
    col("ProjectIDs", "text", False, src="user",
        note="Semicolon-separated, required when Scope = SpecificProjects."),
    col("Reason", "longtext", True, src="user",
        note="MANDATORY. A grant without a stated reason is refused, for every kind."),
    col("RequestedByUserID", "ref", True, ref="Users.UserID", src="user"),
    col("RequestedAt", "datetime", True, src="system"),
    col("AuthorisedByUserID", "ref", True, ref="Users.UserID", src="user",
        note="Must be someone other than the recipient. Self-authorisation is refused."),
    col("AuthorisedAt", "datetime", True, src="system"),
    col("ValidFrom", "datetime", True, src="user"),
    col("ValidTo", "datetime", True, src="user",
        validation="Mandatory, after ValidFrom, and within MaxDurationHours",
        note="MANDATORY. No grant is open-ended, for any kind."),
    col("MaxDurationHours", "int", True, default="24", src="config",
        note="Emergency grants default to 24 hours; audit grants may be configured longer. The "
             "ceiling is configuration, never absent."),
    col("NotificationRecipients", "text", True, src="config",
        note="MANDATORY for Emergency. Who was told that break-glass was used."),
    col("NotificationSentAt", "datetime", False, src="system",
        validation="Required for GrantKind = Emergency before the grant becomes usable",
        note="A break-glass grant that nobody was told about is not break-glass, it is a back door."),
    col("AuditReference", "text", False, src="system",
        note="Correlation identifier linking every action taken under this grant to the audit log."),
    col("UsageCount", "int", True, default="0", src="system",
        note="How many times the grant was actually exercised. Zero is worth reviewing too."),
    col("RevokedAt", "datetime", False, src="user"),
    col("RevokedByUserID", "ref", False, ref="Users.UserID", src="user"),
    col("ReviewedAt", "datetime", False, src="user",
        note="Post-use review. Every exercised emergency grant is reviewed after the fact."),
    col("ReviewedByUserID", "ref", False, ref="Users.UserID", src="user"),
] + ACTIVE + AUDIT,
      notes=["A grant is evidence. It is revoked, expired or reviewed, and never deleted.",
             "Actions performed under a grant are tagged with the GrantID in the audit log, so "
             "'what did break-glass actually do' is answerable."])

table("SystemRecoveryPlan", "control", "global", "internal", 1,
      "How administrative control is recovered when no administrator is available. The system must "
      "not become unrecoverable because one person is unreachable.",
      "خطة استعادة السيطرة الإدارية", "PlanID", [
    col("PlanID", "id", True, key="pk", ex="SRP-B7T2X5"),
    col("PrimaryAdministratorUserID", "ref", False, ref="Users.UserID", src="user",
        note="Left unassigned until the owner names a person."),
    col("BackupAdministratorUserID", "ref", False, ref="Users.UserID", src="user",
        note="The simplest recovery route: a second administrator-capable account."),
    col("RecoveryRouteDocumented", "bool", True, default="FALSE", src="user",
        note="TRUE when a written recovery procedure exists and has been located by someone other "
             "than the administrator."),
    col("RecoveryRouteReference", "text", False, src="user",
        validation="Required when RecoveryRouteDocumented is TRUE",
        note="Where the procedure lives. No credential, and no location of a credential."),
    col("BreakGlassAccountConfigured", "bool", True, default="FALSE", src="user",
        note="Whether an emergency account exists that can be activated by a grant."),
    col("OwnerCanAuthoriseBreakGlass", "bool", True, default="TRUE", src="config",
        note="The system owner can always authorise a break-glass grant."),
    col("LastTestedAt", "date", False, src="user",
        note="An untested recovery route is a hope, not a control."),
    col("TestedByUserID", "ref", False, ref="Users.UserID", src="user"),
    col("TestResult", "text", False, src="user", validation="Passed|Failed|NotTested"),
    col("GoLiveBlocker", "bool", True, default="TRUE", src="system",
        note="Stays TRUE until either a backup administrator exists or a documented recovery route "
             "exists. Go-live is blocked while it is TRUE."),
] + ACTIVE + AUDIT,
      notes=["This table holds no credential and no instruction for obtaining one. It records "
             "WHETHER a route exists and whether it has been tested."])

# --------------------------------------------------------------------------
# 6. Designed now, built later: contracts, billing, resources
# --------------------------------------------------------------------------
table("Contracts", "financial", "project", "financial", 6,
      "Commercial agreement governing a project. Hidden from field roles entirely.",
      "العقود", "ContractID", [
    col("ContractID", "id", True, key="pk", ex="CNT-W2Y7P4"),
    col("LegalEntityID", "ref", True, ref="LegalEntities.LegalEntityID", src="user"),
    col("ClientID", "ref", True, ref="Clients.ClientID", src="user"),
    col("ProjectID", "ref", False, ref="Projects.ProjectID", src="user"),
    col("ContractNumber", "text", True, uniq=True, src="user"),
    col("EffectiveDate", "date", True, src="user"),
    col("ExpiryDate", "date", False, src="user"),
    col("Currency", "text", True, src="user", validation="ISO 4217; must match the project currency"),
    col("PaymentTermsDays", "int", True, src="user"),
    col("RetentionPercent", "decimal", False, src="user", scale=4),
    col("AdvanceAmount", "decimal", False, src="user", scale=3),
    col("AdvanceRecoveryPercent", "decimal", False, src="user", scale=4),
    col("TaxRuleID", "ref", False, ref="TaxRules.TaxRuleID", src="user",
        note="The rule AND its version are preserved on every calculation (D-08)."),
    col("BillingFrequency", "enum", False, enum="ReportingFrequency", src="user"),
    col("BillingMethod", "enum", True, enum="BillingMethod", src="user"),
    col("ContractValue", "decimal", False, src="user", scale=3),
    col("Status", "text", True, default="Draft", src="user",
        validation="Draft|Active|Suspended|Completed|Terminated"),
    col("Version", "int", True, default="1", src="system"),
] + ACTIVE + AUDIT)

table("WorkOrders", "financial", "project", "financial", 6,
      "A discrete instruction under a contract, or a one-off job.", "أوامر العمل", "WorkOrderID", [
    col("WorkOrderID", "id", True, key="pk", ex="WO-H3N7Q5"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="user"),
    col("ContractID", "ref", False, ref="Contracts.ContractID", src="user"),
    col("WorkOrderNumber", "text", True, src="user"),
    col("DescriptionEN", "longtext", True, src="user", ar="DescriptionAR"),
    col("DescriptionAR", "longtext", False, src="user", lang="ar"),
    col("IssuedDate", "date", True, src="user"),
    col("TargetCompletionDate", "date", False, src="user"),
    col("Status", "text", True, default="Open", src="user",
        validation="Open|InProgress|Completed|Cancelled"),
] + ACTIVE + AUDIT,
      unique_together=[["ProjectID", "WorkOrderNumber"]])

table("BOQItems", "financial", "project", "financial", 6,
      "Bill of quantities. Cumulative quantity is controlled, never merely recorded.",
      "بنود جدول الكميات", "BOQItemID", [
    col("BOQItemID", "id", True, key="pk", ex="BOQ-M2D9S6"),
    col("ContractID", "ref", True, ref="Contracts.ContractID", src="user"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="system"),
    col("ItemNumber", "text", True, src="user"),
    col("DescriptionEN", "longtext", True, src="user", ar="DescriptionAR"),
    col("DescriptionAR", "longtext", False, src="user", lang="ar"),
    col("UnitID", "ref", True, ref="Units.UnitID", src="user"),
    col("ContractQuantity", "decimal", True, src="user", scale=3, validation=">= 0"),
    col("UnitRate", "decimal", True, src="user", scale=3, validation=">= 0"),
    col("ApprovedVariationQuantity", "decimal", True, default="0", src="user", scale=3),
    col("PreviouslyCertifiedQuantity", "decimal", True, default="0", src="system", scale=3),
    col("CurrentQuantity", "decimal", True, default="0", src="system", scale=3),
    col("CumulativeQuantity", "decimal", True, default="0", src="system", scale=3,
        note="Computed. Must not exceed ContractQuantity + ApprovedVariationQuantity without a "
             "recorded authorised override (spec 5.17)."),
    col("RemainingQuantity", "decimal", True, default="0", src="system", scale=3, note="Computed."),
    col("QuickBooksItemID", "text", False, src="integration",
        note="Immutable accounting item identifier. Never name-matched."),
] + ACTIVE + AUDIT,
      unique_together=[["ContractID", "ItemNumber"]])

table("InvoiceRequests", "financial", "project", "financial", 6,
      "A calculated billing request. Drafts only until Phase 7; never posted from Phase 1 or 6.",
      "طلبات إصدار الفواتير", "InvoiceRequestID", [
    col("InvoiceRequestID", "id", True, key="pk", ex="INV-R8F1V4"),
    col("LegalEntityID", "ref", True, ref="LegalEntities.LegalEntityID", src="system"),
    col("ClientID", "ref", True, ref="Clients.ClientID", src="system"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="system"),
    col("ContractID", "ref", True, ref="Contracts.ContractID", src="system"),
    col("BillingPeriodStart", "date", True, src="user"),
    col("BillingPeriodEnd", "date", True, src="user"),
    col("Currency", "text", True, src="system",
        note="From the contract. A mismatch anywhere is a validation failure (C-09)."),
    col("PaymentTermsDays", "int", True, src="system"),
    col("InvoiceDate", "date", False, src="user"),
    col("DueDate", "date", False, src="system", note="InvoiceDate + PaymentTermsDays, per contract."),
    col("TaxRuleID", "ref", False, ref="TaxRules.TaxRuleID", src="system"),
    col("TaxRuleVersion", "int", False, src="system",
        note="The version applied, preserved forever (D-08)."),
    col("Subtotal", "decimal", True, default="0", src="calculation", scale=3),
    col("Discount", "decimal", True, default="0", src="calculation", scale=3),
    col("TaxAmount", "decimal", True, default="0", src="calculation", scale=3),
    col("RetentionAmount", "decimal", True, default="0", src="calculation", scale=3),
    col("AdvanceRecovery", "decimal", True, default="0", src="calculation", scale=3),
    col("NetPayable", "decimal", True, default="0", src="calculation", scale=3),
    col("CalculationTrace", "json", False, src="calculation",
        note="Ordered record of every step and rounding decision, reproducible from stored inputs."),
    col("SourceDocumentID", "ref", False, ref="Documents.DocumentID", src="system",
        note="The completion certificate or report this billing derives from."),
    col("FinanceStatus", "enum", True, default="Draft", enum="InvoiceFinanceStatus", src="system"),
    col("QuickBooksStatus", "enum", True, default="NotSent", enum="QuickBooksSyncStatus",
        src="system",
        note="Production posting is unreachable until QBO_POSTING_ENABLED is set by written "
             "authorisation (ADR-0008)."),
    col("QuickBooksInvoiceID", "text", False, src="integration"),
    col("DraftInvoiceNumber", "text", False, src="system",
        note="Internal. Separate from the final accounting number (spec 11)."),
    col("FinalInvoiceNumber", "text", False, src="integration"),
    col("ContentHash", "checksum", True, src="system"),
    col("EntityVersion", "int", True, default="1", src="system"),
] + AUDIT,
      unique_together=[["ClientID", "ProjectID", "ContractID", "BillingPeriodStart",
                        "BillingPeriodEnd", "SourceDocumentID"]],
      notes=["The unique key is the duplicate-billing control (spec 11)."])

table("InvoiceLines", "financial", "project", "financial", 6,
      "Calculated invoice lines. No figure originates from a language model (invariant I-4).",
      "بنود الفاتورة", "InvoiceLineID", [
    col("InvoiceLineID", "id", True, key="pk", ex="INL-C7J5K9"),
    col("InvoiceRequestID", "ref", True, ref="InvoiceRequests.InvoiceRequestID", src="system"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="system"),
    col("BOQItemID", "ref", False, ref="BOQItems.BOQItemID", src="system"),
    col("LineNumber", "int", True, src="system"),
    col("DescriptionEN", "longtext", True, src="user", ar="DescriptionAR",
        note="AI may draft this human-readable description and nothing else (spec 9.4)."),
    col("DescriptionAR", "longtext", False, src="user", lang="ar"),
    col("Quantity", "decimal", True, src="system", scale=3),
    col("UnitRate", "decimal", True, src="system", scale=3),
    col("LineAmount", "decimal", True, src="calculation", scale=3, note="Computed, never entered."),
    col("TaxCode", "text", False, src="system"),
    col("TaxAmount", "decimal", True, default="0", src="calculation", scale=3),
    col("CostCenter", "text", False, src="user"),
    col("Class", "text", False, src="user", note="Maps to an accounting class where available."),
    col("ProjectReference", "text", False, src="system"),
] + AUDIT)

table("Materials", "master", "global", "internal", 5,
      "Approved materials catalogue.", "كتالوج المواد", "MaterialID", [
    col("MaterialID", "id", True, key="pk", ex="MAT-W4B2T1"),
    col("ItemCode", "text", True, uniq=True, src="config"),
    col("DescriptionEN", "text", True, src="config", ar="DescriptionAR"),
    col("DescriptionAR", "text", False, src="config", lang="ar"),
    col("UnitID", "ref", True, ref="Units.UnitID", src="config"),
    col("ApprovedSpecification", "longtext", False, src="config"),
    col("ApprovedBrand", "text", False, src="config"),
    col("Supplier", "text", False, src="config"),
    col("QuickBooksItemID", "text", False, src="integration", sens="financial"),
] + ACTIVE + AUDIT)

table("MaterialUsage", "operational", "project", "internal", 5,
      "Material consumed against a visit activity. Never creates an accounting transaction (spec 5.12).",
      "استهلاك المواد", "MaterialUsageID", [
    col("MaterialUsageID", "id", True, key="pk", ex="MUS-G6L9P3"),
    col("VisitActivityID", "ref", True, ref="VisitActivities.VisitActivityID", src="user"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="system"),
    col("MaterialID", "ref", True, ref="Materials.MaterialID", src="user"),
    col("Quantity", "decimal", True, src="user", scale=3, validation=">= 0"),
    col("UnitID", "ref", True, ref="Units.UnitID", src="user"),
    col("Remarks", "text", False, src="user"),
] + AUDIT)

table("Equipment", "master", "global", "internal", 5,
      "Equipment register.", "سجل المعدات", "EquipmentID", [
    col("EquipmentID", "id", True, key="pk", ex="EQP-N1X7Z5"),
    col("EquipmentCode", "text", True, uniq=True, src="config"),
    col("NameEN", "text", True, src="config", ar="NameAR"),
    col("NameAR", "text", False, src="config", lang="ar"),
    col("Category", "text", False, src="config"),
] + ACTIVE + AUDIT)

table("VisitEquipment", "operational", "project", "internal", 5,
      "Equipment present during a visit.", "المعدات المستخدمة في الزيارة", "VisitEquipmentID", [
    col("VisitEquipmentID", "id", True, key="pk", ex="VEQ-Q3S8M6"),
    col("VisitID", "ref", True, ref="SiteVisits.VisitID", src="user"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="system"),
    col("EquipmentID", "ref", True, ref="Equipment.EquipmentID", src="user"),
    col("Hours", "decimal", False, src="user", scale=2),
    col("Remarks", "text", False, src="user"),
] + AUDIT)

table("Employees", "master", "global", "personal", 5,
      "Crew register for resource reporting. Payroll data is deliberately excluded (spec 5.13).",
      "سجل العمالة", "EmployeeID", [
    col("EmployeeID", "id", True, key="pk", ex="EMP-F5D2H4"),
    col("EmployeeCode", "text", True, uniq=True, src="config"),
    col("FullNameEN", "text", True, src="config", ar="FullNameAR"),
    col("FullNameAR", "text", False, src="config", lang="ar"),
    col("TradeEN", "text", False, src="config", ar="TradeAR"),
    col("TradeAR", "text", False, src="config", lang="ar"),
    col("CrewCode", "text", False, src="config"),
] + ACTIVE + AUDIT,
      notes=["No salary, rate, passport, visa or personal document field exists in this table."])

table("VisitManpower", "operational", "project", "internal", 5,
      "Manpower present during a visit, for resource summaries only.", "العمالة في الزيارة",
      "VisitManpowerID", [
    col("VisitManpowerID", "id", True, key="pk", ex="VMP-V9K1B7"),
    col("VisitID", "ref", True, ref="SiteVisits.VisitID", src="user"),
    col("ProjectID", "ref", True, ref="Projects.ProjectID", src="system"),
    col("EmployeeID", "ref", False, ref="Employees.EmployeeID", src="user"),
    col("TradeEN", "text", False, src="user", ar="TradeAR"),
    col("TradeAR", "text", False, src="user", lang="ar"),
    col("HeadCount", "int", False, src="user", validation=">= 0"),
    col("Hours", "decimal", False, src="user", scale=2),
] + AUDIT,
      notes=["Never exposes payroll detail to field roles."])

# --------------------------------------------------------------------------
# 7. Status transitions
# --------------------------------------------------------------------------
TRANSITIONS = {}


def transitions(entity, field, allowed, forbidden, terminal):
    # Keyed by entity AND field: one table may own more than one lifecycle, and an invoice
    # request owns two (its finance status and its accounting synchronisation status).
    TRANSITIONS[f"{entity}.{field}"] = {
        "entity": entity, "field": field,
        "allowed": [
            {"from": f, "to": t, "roles": r, "preconditions": p, "side_effects": s, "invalidates": i}
            for (f, t, r, p, s, i) in allowed],
        "forbidden": forbidden,
        "terminal_states": terminal,
    }


transitions("SiteVisits", "WorkflowStatus", [
    ("Draft", "Submitted", ["FieldUser", "SiteSupervisor"],
     ["At least one VisitActivity exists",
      "Every effective evidence rule satisfied",
      "Submitter holds an active ProjectAssignment with MaySubmitEvidence",
      "Project.Status = Active"],
     ["SubmittedAt set", "EntityVersion incremented", "ContentHash computed",
      "Protected fields become read-only to the submitter"], []),
    ("Draft", "Cancelled", ["FieldUser", "SiteSupervisor", "ProjectManager"],
     ["Reason recorded"], ["Record retained, never deleted"], []),
    ("Submitted", "UnderTechnicalReview", ["System"],
     ["Server-side validation passed", "Authorisation re-validated from the authoritative record"],
     ["Reviewer notified once", "Idempotency key claimed"], []),
    ("Submitted", "ValidationFailed", ["System"],
     ["Server-side validation failed"],
     ["Specific correctable errors recorded in ValidationErrors", "Submitter notified"], []),
    ("ValidationFailed", "Draft", ["FieldUser", "SiteSupervisor"], [],
     ["Record editable again"], []),
    ("UnderTechnicalReview", "CorrectionRequired", ["TechnicalReviewer", "ProjectManager", "GeneralManager"],
     ["RejectionReason recorded"], ["Returned to the submitter's queue"], []),
    ("UnderTechnicalReview", "TechnicallyApproved", ["TechnicalReviewer", "ProjectManager", "GeneralManager"],
     ["Reviewer is not the submitter (self-approval prohibited, D-09)",
      "Every photograph has a ReviewerDecision other than Pending"],
     ["Approval row written with EntityVersion and ContentHash",
      "TechnicalReviewedAt and TechnicalReviewedBy set"], []),
    ("CorrectionRequired", "Draft", ["FieldUser", "SiteSupervisor"], [],
     ["Record editable again"], []),
    ("TechnicallyApproved", "ReadyForReport", ["System"],
     ["Period open", "Project reporting configuration resolved"], [], []),
    ("TechnicallyApproved", "CorrectionRequired", ["TechnicalReviewer", "GeneralManager"],
     ["Reason recorded"], ["Approval voided"], ["Approvals for this visit"]),
    ("ReadyForReport", "IncludedInDraft", ["System"],
     ["Included in a frozen DocumentJob snapshot"], ["Snapshot records version and hash"], []),
    ("IncludedInDraft", "Released", ["System"],
     ["Parent document reached Released"], [], []),
    ("Released", "Archived", ["SystemAdministrator", "BusinessAdministrator", "GeneralManager"],
     ["Retention review completed"], ["Moved to archive folder; nothing deleted"], []),
    ("IncludedInDraft", "ReadyForReport", ["System"],
     ["The document draft was cancelled"], ["Reserved number cancelled, never reused"], []),
], forbidden=[
    "Draft -> TechnicallyApproved (skips validation and review)",
    "Submitted -> TechnicallyApproved (skips validation)",
    "ValidationFailed -> UnderTechnicalReview (errors must be corrected first)",
    "Any state -> Released without a released parent document",
    "Archived -> any state (archive is terminal)",
    "Any transition performed by a user without an active ProjectAssignment",
], terminal=["Archived", "Cancelled"])

transitions("VisitActivities", "Status", [
    ("Draft", "Submitted", ["FieldUser", "SiteSupervisor"], ["Parent visit submitted"], [], []),
    ("Submitted", "UnderReview", ["System"], ["Parent visit under review"], [], []),
    ("UnderReview", "Approved", ["TechnicalReviewer", "ProjectManager", "GeneralManager"],
     ["Reviewer is not the submitter", "Evidence rule satisfied or a recorded override exists"],
     ["Eligible for reporting"], []),
    ("UnderReview", "Rejected", ["TechnicalReviewer", "ProjectManager", "GeneralManager"],
     ["Comment recorded"], ["Excluded from reporting; record retained"], []),
    ("UnderReview", "CorrectionRequired", ["TechnicalReviewer", "ProjectManager", "GeneralManager"],
     ["Comment recorded"], [], []),
    ("CorrectionRequired", "Draft", ["FieldUser", "SiteSupervisor"], [], [], []),
    ("Approved", "CorrectionRequired", ["TechnicalReviewer", "GeneralManager"],
     ["Reason recorded"], ["Approval voided"], ["Approvals for this activity and its parent visit"]),
    ("Draft", "Cancelled", ["FieldUser", "SiteSupervisor"], ["Reason recorded"], [], []),
], forbidden=[
    "Draft -> Approved",
    "Rejected -> Approved (a new activity record is required instead)",
    "Any approval by the user who submitted the activity",
], terminal=["Cancelled"])

transitions("Photos", "ReviewerDecision", [
    ("Pending", "Approved", ["TechnicalReviewer", "ProjectManager", "GeneralManager"],
     ["Reviewer is not the uploader",
      "Caption present where the evidence stage requires one"],
     ["ApprovedForReport set TRUE", "ReviewedAt and ReviewedByUserID set",
      "EntityVersion incremented"], []),
    ("Pending", "Rejected", ["TechnicalReviewer", "ProjectManager", "GeneralManager"],
     ["ReviewerComment recorded"], ["ApprovedForReport stays FALSE; file retained unchanged"], []),
    ("Pending", "Excluded", ["TechnicalReviewer", "ProjectManager", "GeneralManager"],
     ["ReviewerComment recorded"], ["Valid evidence deliberately left out of this report"], []),
    ("Approved", "Rejected", ["TechnicalReviewer", "GeneralManager"],
     ["Reason recorded", "Not already frozen into a released document"],
     ["ApprovedForReport set FALSE"], ["Approvals for the parent visit", "Unreleased draft documents containing it"]),
    ("Rejected", "Approved", ["TechnicalReviewer", "GeneralManager"],
     ["Reason recorded"], [], ["Approvals for the parent visit"]),
], forbidden=[
    "Any transition performed by AI or by an automation on AI output (ADR-0004, D-06)",
    "Any transition that modifies, replaces or deletes the original received file (D-13)",
    "Approval by the user who uploaded the photograph",
], terminal=[])

transitions("Snags", "Status", [
    ("Open", "Assigned", ["ProjectManager", "TechnicalReviewer", "GeneralManager"],
     ["ResponsibleParty and TargetDate set"], [], []),
    ("Assigned", "InProgress", ["SiteSupervisor", "ProjectManager"], [], [], []),
    ("InProgress", "PendingVerification", ["SiteSupervisor", "ProjectManager"],
     ["Closure evidence photograph attached"], [], []),
    ("PendingVerification", "Closed", ["TechnicalReviewer", "ProjectManager", "GeneralManager"],
     ["ClosureEvidencePhotoID present and approved", "VerifiedBy is not the person who raised it",
      "ClosureDate set"], ["Verification recorded"], []),
    ("PendingVerification", "InProgress", ["TechnicalReviewer", "ProjectManager", "GeneralManager"],
     ["Comment recorded"], [], []),
    ("Open", "Rejected", ["ProjectManager", "GeneralManager"], ["Reason recorded"], [], []),
    ("Open", "Deferred", ["ProjectManager", "GeneralManager"], ["Reason and review date recorded"], [], []),
    ("Deferred", "Open", ["ProjectManager", "GeneralManager"], [], [], []),
], forbidden=[
    "Open -> Closed (closure requires evidence and verification)",
    "Closure verified by the person who raised the snag",
], terminal=["Closed", "Rejected"])

transitions("DocumentJobs", "WorkflowStatus", [
    ("Requested", "Validating", ["System"], ["Requester authorised on the project"], [], []),
    ("Validating", "InputValidationFailed", ["System"],
     ["Completeness check failed"], ["DATA GAP findings recorded explicitly"], []),
    ("Validating", "SnapshotFrozen", ["System"],
     ["All inputs present", "Every included record technically approved"],
     ["Manifest of IDs, versions and hashes frozen", "Number reserved (D-10)"], []),
    ("SnapshotFrozen", "Generating", ["System"], ["Template resolved for type, language and project"], [], []),
    ("Generating", "Generated", ["System"],
     ["Draft and PDF produced", "Content hash computed"], ["Number issued", "Document row created"], []),
    ("Generating", "Failed", ["System"], ["Error classified"],
     ["Reserved number cancelled with a reason, never reused"], []),
    ("Requested", "Cancelled", ["ProjectManager", "GeneralManager"], ["Reason recorded"], [], []),
    ("SnapshotFrozen", "Cancelled", ["ProjectManager", "GeneralManager"],
     ["Reason recorded"], ["Reserved number cancelled"], []),
], forbidden=[
    "Requested -> Generating (a frozen snapshot is mandatory)",
    "Re-freezing a snapshot in place (a new job is required)",
], terminal=["Generated", "Failed", "Cancelled"])

transitions("Documents", "ReleaseStatus", [
    ("Draft", "PendingTechnicalApproval", ["System"], ["Draft and PDF exist"], [], []),
    ("PendingTechnicalApproval", "TechnicallyApproved", ["TechnicalReviewer", "GeneralManager"],
     ["Approver is not the requester where the matrix requires segregation",
      "ContentHash matches the approved content"],
     ["Revision locked", "Approval recorded with hash"], []),
    ("PendingTechnicalApproval", "RevisionRequired", ["TechnicalReviewer", "GeneralManager"],
     ["Comment recorded"], [], []),
    ("TechnicallyApproved", "PendingRelease", ["System"],
     ["Finance approval complete where required for the type"], [], []),
    ("PendingRelease", "Released", ["GeneralManager"],
     ["Explicit release decision recorded", "Recipients are authorised contacts",
      "ContentHash recomputed and unchanged"],
     ["Recipient snapshot stored", "Files moved to released folder"], []),
    ("TechnicallyApproved", "RevisionRequired", ["System"],
     ["A source record changed: ContentHash no longer matches"],
     ["Technical approval voided"], ["Technical approval", "Finance approval", "Release approval"]),
    ("RevisionRequired", "Draft", ["System"], ["New revision created"],
     ["VersionNumber incremented; the previous revision is superseded, not overwritten"], []),
    ("Released", "Superseded", ["System"], ["A later revision was released"], [], []),
    ("Draft", "Cancelled", ["GeneralManager", "ProjectManager"],
     ["Reason recorded", "Document not yet released"],
     ["Any reserved number is cancelled with a reason, never reused"], []),
    ("PendingTechnicalApproval", "Cancelled", ["GeneralManager"],
     ["Reason recorded"], ["Reserved number cancelled"], []),
    ("RevisionRequired", "Cancelled", ["GeneralManager"],
     ["Reason recorded"], ["Reserved number cancelled"], []),
], forbidden=[
    "Draft -> Released",
    "TechnicallyApproved -> Released without a release decision (spec 14 criterion 12)",
    "Release to a recipient not marked IsAuthorizedRecipient",
    "Editing a released document in place (a new revision is mandatory)",
], terminal=["Superseded", "Cancelled"])

transitions("NumberRegister", "State", [
    ("Reserved", "Issued", ["System"], ["Document created successfully"], ["IssuedAt set"], []),
    ("Reserved", "Cancelled", ["System"], ["Job failed or was cancelled", "Reason recorded"],
     ["Number never reused; the gap is explainable"], []),
], forbidden=[
    "Issued -> Reserved",
    "Cancelled -> Reserved or Issued (silent reuse is prohibited, D-10)",
    "Deleting any row from the register",
], terminal=["Issued", "Cancelled"])

transitions("Approvals", "Decision", [
    ("Pending", "Approved", ["GeneralManager", "TechnicalReviewer", "FinanceReviewer"],
     ["Acting user is the responsible approver, or holds a valid unrevoked delegation covering "
      "this stage, project and moment",
      "Acting user is not the originator where SelfApprovalProhibited is TRUE",
      "ContentHash still matches the entity"],
     ["DecisionAt and DecisionByUserID recorded", "DelegationID recorded when acting as a delegate"], []),
    ("Pending", "Rejected", ["GeneralManager", "TechnicalReviewer", "FinanceReviewer"],
     ["Comment recorded"], [], []),
    ("Pending", "Delegated", ["GeneralManager", "TechnicalReviewer", "FinanceReviewer"],
     ["A delegation exists that is active, unrevoked, inside its window, and covers this stage "
      "and project", "The delegate is not the originator of the item being approved"],
     ["Request reassigned to the delegate; the original responsible user is retained"], []),
    ("Delegated", "Approved", ["GeneralManager", "TechnicalReviewer", "FinanceReviewer",
                               "ProjectManager"],
     ["Acting user is the named delegate", "Delegation still valid at the moment of decision",
      "ContentHash still matches the entity"],
     ["DecisionByUserID is the delegate; RequestedFromUserID remains the accountable approver; "
      "DelegationID recorded"], []),
    ("Delegated", "Rejected", ["GeneralManager", "TechnicalReviewer", "FinanceReviewer",
                               "ProjectManager"],
     ["Acting user is the named delegate", "Comment recorded"], ["DelegationID recorded"], []),
    ("Pending", "Withdrawn", ["System"], ["Request superseded"], [], []),
    ("Approved", "Void", ["System"], ["Entity ContentHash changed after approval"],
     ["VoidedAt and VoidReason recorded"], ["Every approval downstream of this one"]),
], forbidden=[
    "Approving one's own restricted transaction because an approver is unavailable (D-09)",
    "Approving with an expired, revoked or out-of-scope delegation",
    "Delegating to the person who originated the item being approved",
    "Void -> Approved (a fresh approval of the new content is required)",
], terminal=["Rejected", "Withdrawn", "Void"])

transitions("InvoiceRequests", "FinanceStatus", [
    ("Draft", "PendingFinanceApproval", ["System"],
     ["Every line recalculated from stored inputs", "Currency agrees across contract, project and request",
      "Cumulative quantities within contract plus approved variation, or an authorised override exists",
      "Tax rule confirmed in writing by the accountant"],
     ["Calculation trace frozen with the request"], []),
    ("PendingFinanceApproval", "FinanceApproved", ["FinanceReviewer", "GeneralManager"],
     ["Approver is not the person who prepared the request",
      "ContentHash of the source document still matches"],
     ["Approval recorded with hash and the applied tax rule version"], []),
    ("PendingFinanceApproval", "Rejected", ["FinanceReviewer", "GeneralManager"],
     ["Reason recorded"], [], []),
    ("Rejected", "Draft", ["System"], ["Recalculated"], [], []),
    ("FinanceApproved", "Void", ["System"],
     ["A source record or certificate changed after approval"],
     ["Finance approval voided"], ["Finance approval", "Any accounting posting authorisation"]),
    ("Void", "Draft", ["System"], ["Recalculated from the current inputs"], [], []),
], forbidden=[
    "Draft -> FinanceApproved (finance approval is a separate, recorded decision)",
    "Any transition to PendingFinanceApproval while the tax treatment is UNDETERMINED (D-08)",
    "Approval by the person who prepared the request",
], terminal=[])

transitions("InvoiceRequests", "QuickBooksStatus", [
    ("NotSent", "Queued", ["System"], ["FinanceStatus = FinanceApproved"], [], []),
    ("Queued", "SandboxPosted", ["System"],
     ["Sandbox company configured", "Customer and item resolved by stored immutable identifier, "
      "never by name"], ["Returned identifier recorded"], []),
    ("SandboxPosted", "Reconciling", ["System"], ["Posted document read back"], [], []),
    ("Reconciling", "Posted", ["System"],
     ["Every line, tax, retention, discount and total matches the local calculation exactly",
      "QBO_POSTING_ENABLED is TRUE by written authorisation of the owner"],
     ["Final invoice number recorded"], []),
    ("Reconciling", "ReconciliationFailed", ["System"],
     ["Any difference, however small"],
     ["Raised for a human. Never auto-corrected in either direction"], []),
    ("ReconciliationFailed", "Queued", ["FinanceReviewer", "GeneralManager"],
     ["Cause identified and corrected in the source, not in the accounting system"], [], []),
    ("Queued", "Failed", ["System"], ["Error classified"], ["Retried only if the class is retriable"], []),
    ("Failed", "Queued", ["System"], ["Retriable class and under the retry cap"], [], []),
], forbidden=[
    "NotSent -> Posted (sandbox and reconciliation are mandatory first)",
    "Reconciling -> Posted while any figure differs from the local calculation",
    "Any posting while QBO_POSTING_ENABLED is FALSE",
    "Creating a customer or item by matching on a similar name",
], terminal=["Posted"])

transitions("Projects", "Status", [
    ("Draft", "Active", ["SystemAdministrator", "BusinessAdministrator", "GeneralManager"],
     ["Client, legal entity, locations, activity rules, approval matrix and template resolved",
      "Residency assignment reviewed or explicitly recorded as unrestricted"],
     ["Project becomes visible to assigned users"], []),
    ("Active", "Suspended", ["SystemAdministrator", "BusinessAdministrator", "GeneralManager"], ["Reason recorded"],
     ["No new visits; existing records readable"], []),
    ("Suspended", "Active", ["SystemAdministrator", "BusinessAdministrator", "GeneralManager"], [], [], []),
    ("Active", "Completed", ["GeneralManager"], ["Closeout reporting complete"], [], []),
    ("Completed", "Archived", ["SystemAdministrator", "BusinessAdministrator", "GeneralManager"], ["Retention review completed"],
     ["Read-only"], []),
], forbidden=[
    "Draft -> Active while a residency requirement blocks production upload and is unreviewed (D-12)",
    "Archived -> any state",
], terminal=["Archived"])

# --------------------------------------------------------------------------
# 8. Role and row-level security matrix
# --------------------------------------------------------------------------
SCOPES = {
    "all": "Every row in the table.",
    "assigned": "Only rows whose ProjectID appears in the user's active ProjectAssignments.",
    "own": "Only rows the user created, within their assigned projects.",
    "none": "No access. The table is not present in this role's data set at all.",
}

ROLE_CODES = ["SystemAdministrator", "BusinessAdministrator", "GeneralManager",
              "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor",
              "FieldUser", "ReadOnlyAuditor", "EmergencyAccess"]

# Roles that function ONLY while a valid, unexpired, authorised TemporaryAccessGrant exists.
# Without a grant they resolve to no access at all.
GRANT_REQUIRED_ROLES = ["ReadOnlyAuditor", "EmergencyAccess"]

GROUPS = {
    # Technical configuration: vocabularies and system behaviour. No client content.
    "techconfig": ["Languages", "Roles", "Units", "Disciplines", "DocumentTypes",
                   "DataClassifications"],
    # Business configuration: what the company sells, issues and is registered as.
    "businessconfig": ["LegalEntities", "ActivityTypes", "ResidencyRequirements",
                       "NumberingSeries", "DocumentTemplates", "Materials", "Equipment"],
    # Access administration: temporary grants and the recovery plan.
    "access": ["TemporaryAccessGrants", "SystemRecoveryPlan"],
    "people": ["Users", "Employees"],
    "clients": ["Clients", "Contacts"],
    "projectmaster": ["Projects", "ProjectAssignments", "Locations", "ProjectActivityRules",
                      "ApprovalMatrix", "ApprovalDelegations", "ResidencyAssignments"],
    "operational": ["SiteVisits", "VisitActivities", "Photos", "Snags", "MaterialUsage",
                    "VisitEquipment", "VisitManpower"],
    "document": ["DocumentJobs", "Documents", "NumberRegister"],
    "control": ["Approvals", "EntityVersions", "AuditLog", "IntegrationJobs"],
    "financial": ["TaxRules", "Contracts", "WorkOrders", "BOQItems", "InvoiceRequests", "InvoiceLines"],
}

# read, create, update  (delete is "none" everywhere: rows are deactivated, never destroyed)
#
# The owner's role distinction (2026-09-11): a technical administrator does not get business
# content merely because they administer configuration, and business master-data administration
# is a separate job from technical administration.
RULES = {
    # Technical configuration, integration monitoring, user provisioning, system health.
    # No ordinary business-content access of any kind.
    "SystemAdministrator": {
        "techconfig": ("all", "all", "all"), "businessconfig": ("all", "none", "none"),
        "people": ("all", "all", "all"), "clients": ("none", "none", "none"),
        "projectmaster": ("all", "none", "none"), "operational": ("none", "none", "none"),
        "document": ("none", "none", "none"), "control": ("all", "none", "none"),
        "access": ("all", "none", "none"), "financial": ("none", "none", "none"),
    },
    # Controlled business master-data administration: clients, projects, locations, activity
    # rules, templates, numbering series. Not evidence, not documents, not money.
    "BusinessAdministrator": {
        "techconfig": ("all", "none", "none"), "businessconfig": ("all", "all", "all"),
        "people": ("all", "none", "none"), "clients": ("all", "all", "all"),
        "projectmaster": ("all", "all", "all"), "operational": ("none", "none", "none"),
        "document": ("none", "none", "none"), "control": ("none", "none", "none"),
        "access": ("none", "none", "none"), "financial": ("none", "none", "none"),
    },
    # The system owner: all authorised company projects and documents.
    "GeneralManager": {
        "techconfig": ("all", "all", "all"), "businessconfig": ("all", "all", "all"),
        "people": ("all", "all", "all"), "clients": ("all", "all", "all"),
        "projectmaster": ("all", "all", "all"), "operational": ("all", "none", "all"),
        "document": ("all", "all", "all"), "control": ("all", "all", "all"),
        "access": ("all", "all", "all"), "financial": ("all", "all", "all"),
    },
    "TechnicalReviewer": {
        "techconfig": ("all", "none", "none"), "businessconfig": ("all", "none", "none"),
        "people": ("all", "none", "none"), "clients": ("all", "none", "none"),
        "projectmaster": ("assigned", "none", "none"),
        "operational": ("assigned", "none", "assigned"), "document": ("assigned", "none", "none"),
        "control": ("assigned", "all", "all"), "access": ("none", "none", "none"),
        "financial": ("none", "none", "none"),
    },
    # Only the commercial and financial records the role actually requires.
    "FinanceReviewer": {
        "techconfig": ("all", "none", "none"), "businessconfig": ("all", "none", "none"),
        "people": ("all", "none", "none"), "clients": ("all", "none", "none"),
        "projectmaster": ("all", "none", "none"), "operational": ("assigned", "none", "none"),
        "document": ("all", "none", "none"), "control": ("all", "all", "all"),
        "access": ("none", "none", "none"), "financial": ("all", "all", "all"),
    },
    "ProjectManager": {
        "techconfig": ("all", "none", "none"), "businessconfig": ("all", "none", "none"),
        "people": ("all", "none", "none"), "clients": ("all", "none", "none"),
        "projectmaster": ("assigned", "none", "assigned"),
        "operational": ("assigned", "assigned", "assigned"),
        "document": ("assigned", "assigned", "none"), "control": ("assigned", "all", "none"),
        "access": ("none", "none", "none"), "financial": ("none", "none", "none"),
    },
    "SiteSupervisor": {
        "techconfig": ("all", "none", "none"), "businessconfig": ("all", "none", "none"),
        "people": ("all", "none", "none"), "clients": ("all", "none", "none"),
        "projectmaster": ("assigned", "none", "none"),
        "operational": ("assigned", "assigned", "own"), "document": ("none", "none", "none"),
        "control": ("none", "none", "none"), "access": ("none", "none", "none"),
        "financial": ("none", "none", "none"),
    },
    "FieldUser": {
        "techconfig": ("all", "none", "none"), "businessconfig": ("all", "none", "none"),
        "people": ("none", "none", "none"), "clients": ("none", "none", "none"),
        "projectmaster": ("assigned", "none", "none"),
        "operational": ("own", "assigned", "own"), "document": ("none", "none", "none"),
        "control": ("none", "none", "none"), "access": ("none", "none", "none"),
        "financial": ("none", "none", "none"),
    },
    # Time-bound and explicitly authorised. Without an active grant this role reads NOTHING.
    "ReadOnlyAuditor": {
        "techconfig": ("all", "none", "none"), "businessconfig": ("all", "none", "none"),
        "people": ("all", "none", "none"), "clients": ("all", "none", "none"),
        "projectmaster": ("all", "none", "none"), "operational": ("all", "none", "none"),
        "document": ("all", "none", "none"), "control": ("all", "none", "none"),
        "access": ("all", "none", "none"), "financial": ("all", "none", "none"),
    },
    # Break-glass. Restores ADMINISTRATIVE capability when no administrator is available.
    # It deliberately does NOT open client evidence, documents or financial records: the
    # emergency is an administrative one, and reading a client's photographs never solves it.
    "EmergencyAccess": {
        "techconfig": ("all", "all", "all"), "businessconfig": ("all", "none", "none"),
        "people": ("all", "all", "all"), "clients": ("none", "none", "none"),
        "projectmaster": ("all", "none", "none"), "operational": ("none", "none", "none"),
        "document": ("none", "none", "none"), "control": ("all", "none", "none"),
        "access": ("all", "none", "none"), "financial": ("none", "none", "none"),
    },
}

# Deliberate per-table exceptions, each with a stated reason.
EXCEPTIONS = {
    ("SystemAdministrator", "AuditLog"): ("all", "none", "none",
        "Append-only for every role. No one may edit or delete the audit trail, including an "
        "administrator."),
    ("GeneralManager", "AuditLog"): ("all", "none", "none", "Append-only for every role."),
    ("FinanceReviewer", "AuditLog"): ("all", "none", "none", "Append-only for every role."),
    ("ReadOnlyAuditor", "AuditLog"): ("all", "none", "none",
        "Read-only, and only while a valid time-bound grant exists."),
    ("EmergencyAccess", "AuditLog"): ("all", "none", "none",
        "Break-glass may read the audit trail to diagnose, and may never alter it."),
    ("TechnicalReviewer", "AuditLog"): ("none", "none", "none",
        "Not needed for the review task; least privilege."),
    ("SystemAdministrator", "ProjectAssignments"): ("all", "all", "all",
        "User provisioning is a technical-administration task: placing a person into a project "
        "is access administration, not business content."),
    ("SystemAdministrator", "TaxRules"): ("none", "none", "none",
        "Separation of duties: a technical administrator has no reason to see or change a "
        "financial rule."),
    ("SystemAdministrator", "Approvals"): ("all", "none", "none",
        "An administrator must never be able to manufacture an approval."),
    ("SystemAdministrator", "IntegrationJobs"): ("all", "none", "none",
        "Integration monitoring and system health are the administrator's job."),
    ("EmergencyAccess", "Approvals"): ("all", "none", "none",
        "Break-glass can see that approvals exist and can never create one."),
    ("EmergencyAccess", "ProjectAssignments"): ("all", "all", "all",
        "Restoring administrative capability means being able to reinstate an administrator."),
    ("BusinessAdministrator", "Users"): ("all", "none", "none",
        "Business administration reads the user register to assign people to projects; creating "
        "and disabling accounts stays with technical administration."),
    ("BusinessAdministrator", "AuditLog"): ("none", "none", "none",
        "Least privilege: business master-data administration does not require the audit trail."),
    ("ProjectManager", "AuditLog"): ("none", "none", "none",
        "Append-only for every role, and a project manager has no need to read it."),
    ("ProjectManager", "IntegrationJobs"): ("assigned", "none", "none",
        "Visibility of failures affecting their own projects, without write access."),
    ("ProjectManager", "Approvals"): ("assigned", "all", "all",
        "Project managers act as first-line reviewers where the approval matrix assigns them."),
    ("FieldUser", "Users"): ("own", "none", "none",
        "A field user may see their own profile only."),
    ("SiteSupervisor", "Photos"): ("assigned", "assigned", "own",
        "Supervisors see all evidence for their projects so they can avoid duplicate captures, but "
        "may edit only their own."),
    ("SiteSupervisor", "Clients"): ("assigned", "none", "none",
        "Client display name only, for the projects they are assigned to."),
}

SECURITY = {"scopes": SCOPES, "roles": ROLE_CODES, "matrix": {}, "exceptions": {}}
for role in ROLE_CODES:
    SECURITY["matrix"][role] = {}
    for group, tables_ in GROUPS.items():
        r, c, u = RULES[role][group]
        for t in tables_:
            key = (role, t)
            if key in EXCEPTIONS:
                er, ec, eu, reason = EXCEPTIONS[key]
                SECURITY["matrix"][role][t] = {"read": er, "create": ec, "update": eu,
                                               "delete": "none", "exception_reason": reason}
                SECURITY["exceptions"][f"{role}.{t}"] = reason
            else:
                SECURITY["matrix"][role][t] = {"read": r, "create": c, "update": u, "delete": "none"}

SECURITY["grant_required_roles"] = GRANT_REQUIRED_ROLES
SECURITY["principles"] = [
    "Row-level access derives from ProjectAssignments only. Absence of an assignment grants nothing.",
    "An expired assignment (AssignedTo in the past) grants nothing.",
    "Field roles have NO access to any financial table: the data is absent from their data set, "
    "not merely hidden (SEC-04).",
    "Delete is 'none' for every role on every table. Rows are deactivated or cancelled, never "
    "destroyed, because history is evidence.",
    "The audit log is append-only for every role, including both administrator roles and break-glass access.",
    "A technical administrator can configure the system, provision users and diagnose failures "
    "without reading client evidence, documents or financial records: support does not require "
    "content access.",
    "Business master-data administration is a separate role from technical administration, and "
    "neither of them opens evidence, documents or money.",
    "ReadOnlyAuditor and EmergencyAccess function ONLY while a valid, unexpired, authorised "
    "TemporaryAccessGrant exists. Without a grant they resolve to no access at all.",
    "Break-glass restores ADMINISTRATIVE capability. It never opens client evidence, documents or "
    "financial records, because an administrative emergency is not solved by reading a client's "
    "photographs.",
    "The system must never become unrecoverable because one administrator is unavailable: either "
    "two administrator-capable accounts exist, or a documented and tested recovery route does.",
    "View, slice and column visibility are presentation, never enforcement. Every state-changing "
    "action is re-validated server-side against the authoritative record (P-04).",
]

# --------------------------------------------------------------------------
# 9. Canonical hashing rules
# --------------------------------------------------------------------------
CANONICAL = {
    "field_set_version": "1.0.0",
    "algorithm": "SHA-256",
    "encoding": "UTF-8, NFC-normalised",
    "rules": [
        "Serialise only the fields listed in the table's content_hash_fields, in that exact order.",
        "Each field is emitted as 'FieldName=value' joined by the record separator U+001F.",
        "Null and empty string both serialise as the empty value, so they never differ by accident.",
        "Text is Unicode NFC-normalised and trimmed of leading and trailing whitespace. Arabic text "
        "is normalised but never transliterated (D-11).",
        "Decimals are emitted at the column's declared scale, with a leading zero and no thousands "
        "separator. Integers carry no decimal point.",
        "Dates are ISO 8601 (YYYY-MM-DD); datetimes are ISO 8601 UTC with a trailing Z.",
        "Booleans are TRUE or FALSE in upper case.",
        "Child collections that affect output (approved photographs and their sequence) are folded "
        "in as an ordered list of child hashes.",
        "Excluded by design: UpdatedAt, UpdatedBy, UI ordering, internal comments and every advisory "
        "AI field. An AI observation arriving later must never void a human approval (C-06).",
        "Changing this field set is a schema migration with its own decision record, because it "
        "changes every hash.",
    ],
}

# --------------------------------------------------------------------------
# 9b. Lean operational MVP (owner instruction, 2026-09-11)
#
# The 46-table model remains the long-term REFERENCE ARCHITECTURE. What gets BUILT
# first is a lean subset, so a supervisor can submit a visit in about a minute and the
# app stays maintainable by one person. Deferring a table never means losing its
# design: every deferred table already has a schema, so adding it later is additive.
# --------------------------------------------------------------------------
LEAN_MVP = {
    "target_range": [12, 18],
    "tables": [
        "Users", "Projects", "ProjectAssignments", "Locations", "ActivityTypes",
        "ProjectActivityRules", "SiteVisits", "VisitActivities", "Photos", "Snags",
        "Approvals", "DocumentJobs", "Documents", "NumberRegister", "LegalEntities",
        "AuditLog", "IntegrationJobs",
    ],
    # A deferred table's job still has to be done. Each entry says how, and what is lost.
    "fold_ins": {
        "Roles": {
            "into": "Users.RoleCode and ProjectAssignments.RoleCode as an enumerated column",
            "cost": "Role descriptions and capability flags live in documentation rather than "
                    "data. Acceptable while the role set is fixed at ten.",
            "restore_when": "A role's capabilities need to be edited by an administrator "
                            "without a rebuild."},
        "Units": {
            "into": "An enumerated UnitCode column on ActivityTypes and VisitActivities",
            "cost": "Per-unit decimal places become a convention rather than configuration.",
            "restore_when": "A unit needs project-specific rounding, or the list grows past "
                            "what a dropdown carries comfortably."},
        "Clients": {
            "into": "ClientNameEN, ClientNameAR and ClientKind columns on Projects",
            "cost": "One client with several projects is repeated per project. Billing "
                    "address, tax number and accounting identifier are absent - none is "
                    "needed before invoicing.",
            "restore_when": "Phase 6, or the first client holding several projects at once."},
        "Contacts": {
            "into": "Deferred entirely. MVP release is manual, so no recipient list is stored",
            "cost": "No authorised-recipient control in the app. The control still exists, "
                    "because a person sends the document deliberately.",
            "restore_when": "Automated delivery, Phase 7."},
        "DocumentTemplates": {
            "into": "TemplateFileKey and DefaultDocumentLanguage columns on Projects",
            "cost": "Template versioning becomes file-level rather than record-level.",
            "restore_when": "A second template revision must be provable after issue, or a "
                            "project needs more than one template."},
        "NumberingSeries": {
            "into": "Format columns on LegalEntities. NumberRegister IS retained",
            "cost": "Series configuration is per entity rather than per entity x type x scope.",
            "restore_when": "A client requires their own numbering run, or a second entity "
                            "issues documents."},
        "ApprovalMatrix": {
            "into": "ReviewerUserID on Projects; the general manager approves everything else",
            "cost": "No multi-step approval and no per-document-type routing.",
            "restore_when": "A delegate is named, or a project needs a different approver."},
        "ApprovalDelegations": {
            "into": "Deferred. The general manager approves; absence is handled by waiting",
            "cost": "**This is the real cost of the lean build.** If the approver is away, "
                    "approvals stop. Accepted only because no delegate has been named yet.",
            "restore_when": "Before go-live if a delegate exists; immediately if approvals "
                            "ever stall."},
        "EntityVersions": {
            "into": "EntityVersion and ContentHash stay on the records; AuditLog carries "
                    "before and after hashes",
            "cost": "Version history is reconstructed from the audit log rather than read "
                    "directly.",
            "restore_when": "A dispute requires the version chain as a first-class record."},
        "TemporaryAccessGrants": {
            "into": "Deferred. No auditor or break-glass role is enabled in the lean build",
            "cost": "Time-bound audit access is unavailable.",
            "restore_when": "An external audit is scheduled, or break-glass is needed."},
        "SystemRecoveryPlan": {
            "into": "Two administrator accounts in the Workspace, plus a written runbook",
            "cost": "The go-live blocker is tracked in the runbook rather than in data.",
            "restore_when": "The estate is large enough that the plan needs testing evidence "
                            "recorded against it."},
        "Languages, Disciplines, DocumentTypes, DataClassifications": {
            "into": "Enumerated columns",
            "cost": "Vocabularies change by editing the app rather than a row.",
            "restore_when": "A vocabulary changes more than about twice a year."},
    },
    # Required references from a lean table to a deferred one. Each must be replaced by a
    # concrete lean column, or the subset does not actually build.
    "column_overrides": {
        "Users.RoleID": {
            "lean_column": "RoleCode",
            "lean_type": "enum of the ten role codes",
            "note": "The role vocabulary is fixed for the MVP, so an enum carries it."},
        "ProjectAssignments.RoleID": {
            "lean_column": "RoleCode",
            "lean_type": "enum of the ten role codes",
            "note": "The role held ON THIS PROJECT, which is what the security filter reads."},
        "Projects.ClientID": {
            "lean_column": "ClientNameEN, ClientNameAR, ClientKind",
            "lean_type": "text columns on Projects",
            "note": "Enough for a report header and a dashboard. Billing address, tax number "
                    "and accounting identifier are absent until Phase 6, where they are needed."},
        "ActivityTypes.DisciplineID": {
            "lean_column": "DisciplineCode",
            "lean_type": "enum of six disciplines",
            "note": "Used to group the activity picker; not referenced anywhere else."},
        "Documents.TemplateID": {
            "lean_column": "TemplateFileKey, LanguageCode",
            "lean_type": "columns on Documents, copied from the project at generation",
            "note": "Records which template file actually produced the document, which is the "
                    "part that matters for reproducibility."},
        "NumberRegister.SeriesID": {
            "lean_column": "SeriesKey",
            "lean_type": "text key composed of entity, document type and year",
            "note": "The register keeps its reserved/issued/cancelled control; only the series "
                    "CONFIGURATION moves to the legal entity."},
    },
    # Release 1: the controlled capture-and-review prototype (owner instruction, 2026-09-11).
    # Twelve tables. No report generation, so no document, numbering or legal-entity table.
    "release_1": {
        "tables": [
            "Users", "Projects", "ProjectAssignments", "Locations", "ActivityTypes",
            "SiteVisits", "VisitActivities", "Photos", "Snags", "Approvals",
            "AuditLog", "IntegrationJobs",
        ],
        "consolidations": {
            "ProjectActivityRules": {
                "into": "ActivityTypes, with an optional ProjectID column",
                "rule": "A row with no ProjectID is the global rule; a row with a ProjectID is a "
                        "project override of it. Same resolution logic, one table.",
                "cost": "The override and the rule it overrides share a table, so an administrator "
                        "reading the catalogue sees both. Acceptable at 34 activities."},
            "Roles": {
                "into": "RoleCode enum on Users and ProjectAssignments",
                "rule": "The role vocabulary is fixed at ten for the prototype.",
                "cost": "Role capabilities are documentation rather than data."},
            "Clients": {
                "into": "ClientNameEN, ClientNameAR and ClientKind on Projects",
                "rule": "Display only; no billing data exists in release 1.",
                "cost": "A client with several projects is repeated per project."},
            "LegalEntities, DocumentJobs, Documents, NumberRegister": {
                "into": "Not present. Release 1 produces no document",
                "rule": "Reports are produced manually from approved evidence exported from the app.",
                "cost": "No document numbering, no release control, no report snapshot. **This is "
                        "the boundary of release 1** and the first thing release 1b adds."},
        },
        "adds_in_release_1b": ["DocumentJobs", "Documents", "NumberRegister", "LegalEntities"],
    },
    "deferred_phases": {
        "Materials": 5, "MaterialUsage": 5, "Equipment": 5, "VisitEquipment": 5,
        "Employees": 5, "VisitManpower": 5,
        "Contracts": 6, "WorkOrders": 6, "BOQItems": 6, "TaxRules": 6,
        "InvoiceRequests": 6, "InvoiceLines": 6,
        "ResidencyRequirements": 3, "ResidencyAssignments": 3,
    },
}

# --------------------------------------------------------------------------
# 9b. Capture once, use twice  (owner operational correction, 2026-09-11)
# --------------------------------------------------------------------------
# The supervisor must never upload, select or describe the same evidence twice.
# Everything below is canonical: the workflow document, the AppSheet action
# specification, the device test protocol and the automated checks are all
# generated from or tested against this block.

CAPTURE_ONCE = {
    "principle": "Capture once, use twice. The supervisor captures or selects the photographs "
                 "exactly once. The same stored files serve the contractor group share and every "
                 "internal report.",
    "acceptance": {
        "id": "CAP-01",
        "statement": "The workflow fails acceptance if the supervisor must select or upload the "
                     "images a second time.",
        "applies_to": ["first share", "retry after a failed or cancelled share",
                       "AI analysis", "reviewer correction", "every report that re-uses the "
                       "evidence"],
        "on_failure": "Do not implement a duplicate-upload workaround. Produce the capture-platform "
                      "decision comparison instead.",
    },
    "workflow": [
        {"step": 1, "actor": "supervisor", "action": "Opens the field application."},
        {"step": 2, "actor": "system",
         "action": "Project, location, date, time, supervisor and capture mode are populated "
                   "automatically. The supervisor is asked nothing unless a genuine choice exists.",
         "source": "ProjectAssignments, the device clock and the authenticated identity — trusted "
                   "system data, never the photograph (D-22)."},
        {"step": 3, "actor": "supervisor",
         "action": "Confirms the location — and only when it does not resolve automatically.",
         "source": "Locations — prefilled from the project default or the last location used "
                   "today. A trusted structured reference, never inferred from the photograph."},
        {"step": 4, "actor": "supervisor",
         "action": "Captures or selects the photographs ONCE.",
         "source": "Device camera or gallery. This is the only file selection in the workflow."},
        {"step": 5, "actor": "system",
         "action": "The photographs are stored in the controlled system, unchanged, and grouped "
                   "under one CaptureBatchID."},
        {"step": 6, "actor": "ai",
         "action": "Analyses the ELIGIBLE photographs and PROPOSES the advisory fields below — "
                   "immediately in AI Reviewed Share, after the share in Quick Share (D-24).",
         "binding": "advisory"},
        {"step": 7, "actor": "supervisor",
         "action": "Confirms or corrects the proposal with minimum interaction. In Quick Share "
                   "this happens later; classification stays Pending and blocks nothing (D-23).",
         "binding": "authoritative"},
        {"step": 8, "actor": "supervisor",
         "action": "Shares the same image files and a formatted summary to the existing "
                   "main-contractor group through ONE native share action.",
         "constraint": "Native share sheet only. No public link, no re-selection, no web automation."},
        {"step": 9, "actor": "system",
         "action": "The same stored evidence is re-used in daily, weekly, monthly, "
                   "corrective-action, inspection and completion reports."},
    ],
    "modes": {
        "QuickShare": {
            "sequence": ["capture", "store", "native share"],
            "default": True,
            "ai": "deferred and filtered: after the share, once duplicates, unusable images and "
                  "exclusions have been removed (D-24)",
            "use_when": "The default. The contractor group is served first and nothing is "
                        "waited for.",
            "capture_count": 1,
        },
        "AIReviewedShare": {
            "sequence": ["capture", "store", "AI proposal", "supervisor confirmation",
                         "native share"],
            "default": False,
            "chosen_by": "an explicit action, never a routine question",
            "ai": "immediate, before the share, on the batch's eligible photographs",
            "use_when": "A reviewed professional caption is wanted before group submission.",
            "capture_count": 1,
        },
    },
    "optional_note": {
        "description_mandatory_for_normal_submission": False,
        "statement": "A written description of completed work must not be mandatory for a normal "
                     "photographic submission.",
        "fields": ["SiteVisits.OverallDescriptionEN", "SiteVisits.OverallDescriptionAR",
                   "SiteVisits.AdditionalSiteNote", "VisitActivities.DescriptionEN",
                   "VisitActivities.DescriptionAR", "Photos.CaptionEN", "Photos.CaptionAR"],
        "future_input_methods": ["voice note", "speech to text"],
        "categories": [v["code"] for v in ENUMS["SiteNoteCategory"]["values"]],
        "mandatory_exceptions": [
            "A record returned for correction — RejectionReason stays mandatory.",
            "A visit reporting non-completion — the reason cannot be photographed.",
            "A caption on an Observation, Snag, Material or Safety photograph — the stage itself "
            "asserts a fact the image alone does not name.",
            "A measured quantity claimed without a photographed measurement.",
        ],
    },
    "ai_proposes": [
        {"item": "visible activity", "column": "Photos.AIProposedActivityText"},
        {"item": "evidence stage", "column": "Photos.AIProposedEvidenceStage",
         "vocabulary": [v["code"] for v in ENUMS["EvidenceStage"]["values"]]},
        {"item": "professional caption", "column": "Photos.AIProposedCaptionEN"},
        {"item": "visible condition", "column": "Photos.AIVisibleCondition"},
        {"item": "possible snag", "column": "Photos.AIPossibleSnag"},
        {"item": "image quality warning", "column": "Photos.AIImageQualityWarning"},
        {"item": "uncertainty", "column": "Photos.AIUncertaintyNote"},
        {"item": "confidence", "column": "Photos.AIConfidence"},
    ],
    "ai_must_not_infer": [
        "measured quantity",
        "hidden defect or its cause",
        "exact material brand",
        "compliance with contract or specification",
        "exact completion percentage",
        "exact project or location from the photograph alone",
        "responsibility or negligence",
        "date, unless supplied as trusted metadata",
        "that Al-Haram executed the visible work merely because it appears in the photograph",
    ],
    "trusted_context_fields": [
        "SiteVisits.ProjectID", "SiteVisits.LocationID", "SiteVisits.VisitDate",
        "SiteVisits.SupervisorUserID", "SiteVisits.WorkOrderID",
        "VisitActivities.ActivityTypeID", "Photos.LocationID",
    ],
    "forbidden_ai_written_columns": [
        "SiteVisits.ProjectID", "SiteVisits.LocationID", "SiteVisits.VisitDate",
        "SiteVisits.SupervisorUserID", "SiteVisits.WorkflowStatus",
        "VisitActivities.ActivityTypeID", "VisitActivities.Quantity",
        "VisitActivities.PercentComplete", "VisitActivities.UnitID",
        "Photos.EvidenceStage", "Photos.CaptionEN", "Photos.CaptionAR",
        "Photos.ReviewerDecision", "Photos.ApprovedForReport",
        "Photos.ConfirmedActivityTypeID", "Photos.ClassificationStatus",
        "Snags.Severity", "Approvals.Decision",
    ],
    # D-22: the normal path asks the supervisor for nothing but the photographs.
    "minimum_interaction": {
        "principle": "Minimum interaction. On the normal path the supervisor supplies the "
                     "photographs and nothing else. Every other value is populated "
                     "automatically, and a question is asked only when a genuine choice exists.",
        "normal_path": ["open the app",
                        "confirm project and location only if necessary",
                        "capture the photographs",
                        "save and share"],
        "mandatory_manual_inputs": [],
        "tables_on_the_normal_path": ["SiteVisits", "Photos"],
        "not_required_on_the_normal_path": {
            "VisitActivities": "Declaring an activity is not the price of submitting evidence "
                               "(D-22). A visit carrying photographs and no activity is a valid "
                               "photographic submission; the classification catches up "
                               "afterwards. An activity that DOES exist still satisfies its "
                               "effective rule in full — quantity, caption and minimum "
                               "photographs are unchanged.",
        },
        "auto_populated": [
            {"field": "SiteVisits.SupervisorUserID",
             "source": "the authenticated identity",
             "asks_user": "never"},
            {"field": "SiteVisits.VisitDate",
             "source": "the device date", "asks_user": "never"},
            {"field": "SiteVisits.StartTime",
             "source": "the device time at first capture", "asks_user": "never"},
            {"field": "SiteVisits.EndTime",
             "source": "the device time at last capture", "asks_user": "never"},
            {"field": "SiteVisits.ProjectID",
             "source": "the single active assignment, else the last project used today, else the "
                       "project default",
             "asks_user": "only when several assignments are active and none resolves"},
            {"field": "SiteVisits.LocationID",
             "source": "the project's default location, else the last location used today",
             "asks_user": "only when several active locations exist and none resolves"},
            {"field": "SiteVisits.CaptureMode",
             "source": "defaults to QuickShare",
             "asks_user": "never on the normal path"},
            {"field": "Photos.EvidenceStage",
             "source": "proposed by analysis, or pre-tagged from the activity rule, or left pending",
             "asks_user": "never before capture"},
            {"field": "Photos.CaptureBatchID",
             "source": "generated at capture", "asks_user": "never"},
            {"field": "Photos.CaptureSequence",
             "source": "the order the device captured them", "asks_user": "never"},
        ],
        "optional_inputs": ["SiteVisits.AdditionalSiteNote", "SiteVisits.SiteNoteCategory",
                            "SiteVisits.SafetyObservation", "SiteVisits.OverallDescriptionEN",
                            "SiteVisits.OverallDescriptionAR", "Photos.CaptionEN",
                            "Photos.CaptionAR", "Photos.EvidenceStage"],
        "required_but_never_typed": ["SiteVisits.ProjectID", "SiteVisits.LocationID",
                                     "SiteVisits.VisitDate", "SiteVisits.SupervisorUserID",
                                     "SiteVisits.CaptureMode", "SiteVisits.ShareStatus",
                                     "SiteVisits.ShareAttemptCount",
                                     "Photos.ClassificationStatus", "Photos.AnalysisEligibility"],
        "note": "Required in storage and required of the supervisor are different things. Every "
                "field above is required for the record to be meaningful, and none of them is a "
                "question on the normal path.",
    },
    # D-23: a controlled activity classification that a human confirms.
    "revocation": {
        "decision": "D-25",
        "principle": "Revoking access must never destroy evidence, and must never let the revoked "
                     "user reach the project again. Those are two separate obligations and the "
                     "design owes both.",
        "dividing_line": "Photos.CapturedAt against Photos.AccessRevokedAt. Provably captured "
                         "before revocation, or it does not complete at all.",
        "before_revocation": "Completes into the restricted quarantine area. Never written "
                             "directly into the active project evidence register.",
        "after_revocation": "REFUSED. Not quarantined, not queued, not stored as evidence.",
        "revoked_user_may": [],
        "revoked_user_may_not": ["view", "edit", "delete", "share", "submit"],
        "preserved_for_every_quarantined_item": [
            "Photos.CapturedAt — the original capture timestamp, unchanged",
            "Photos.CapturedBy — the device and user identity that captured it",
            "Photos.OriginalChecksum — the file hash, with Photos.ChecksumAlgorithm",
            "Photos.UploadCompletedAt — when the upload was confirmed",
            "Photos.AccessRevokedAt — when access ended",
        ],
        "reviewer": {
            "notified": "immediately, on the first quarantined item",
            "may_accept": "creates a traceable project record; the quarantine history is retained",
            "may_reject": "requires a mandatory reason in QuarantineRejectionReason; the audit "
                          "record is retained under the retention policy and the row is never "
                          "deleted",
            "may_not_be": "the revoked user",
        },
        "readable_by_reports": ["NotQuarantined", "AcceptedIntoProject"],
        "never_readable_by_reports": ["Quarantined", "Rejected"],
        "if_the_platform_cannot_enforce_this": "CAP-GATE fails. The queued files stay locally "
                                               "protected — not deleted, not uploaded — pending "
                                               "an authorised recovery procedure.",
        "silent_loss_is_never_acceptable": True,
    },
    "classification": {
        "principle": "AI-generated free text never becomes the trusted structured activity. A "
                     "proposal and a confirmation are different columns, and only the "
                     "confirmation is read by anything.",
        "advisory": ["Photos.AIProposedActivityText", "Photos.AIProposedActivityTypeID"],
        "trusted": "Photos.ConfirmedActivityTypeID",
        "state": "Photos.ClassificationStatus",
        "disposition": "Photos.AIProposalDisposition",
        "pending_is_normal": True,
        "rule": "Only ClassificationStatus = Confirmed makes ConfirmedActivityTypeID readable by a "
                "report, a rule, a calculation or a filter. Pending is the normal state "
                "immediately after a Quick Share and blocks nothing.",
        "quick_share_behaviour": "Classification stays Pending and is reviewed later. The share "
                                 "has already happened; the record catches up.",
        "may_not_read_candidate": ["reports", "business rules", "calculations", "filters",
                                   "joins", "approvals"],
    },
    # D-24: analysis is filtered before it is paid for.
    "ai_analysis_policy": {
        "principle": "Not every captured photograph needs an immediate model call. Filtering "
                     "happens before the call, never after it, and reports still use every "
                     "relevant approved photograph.",
        "policies": {
            "AIReviewedShare": {
                "timing": "immediate, before the share",
                "unit": "one request per capture batch",
                "filtered": "local duplicate and quality checks run first; the rest of the batch "
                            "is analysed",
                "why": "the supervisor is waiting, so the proposal has to exist now",
            },
            "QuickShare": {
                "timing": "deferred, after the share",
                "unit": "one request per capture batch, batched again across visits where the "
                        "queue allows",
                "filtered": "duplicates, unusable images, deleted and explicitly excluded images "
                            "are removed first; only then is a request made",
                "why": "nothing is waiting, so the cheapest correct moment is after the "
                       "supervisor has finished and the obvious waste has been removed",
            },
        },
        "never_analysed": [
            "a near-duplicate of a photograph already analysed in the same batch",
            "an image below the project's quality threshold",
            "an image deleted or explicitly excluded before analysis ran",
            "an image already analysed — analysis never runs twice on the same file",
            "any image in a project where analysis is switched off, or after the monthly cap",
        ],
        "still_analysed": "every photograph a reviewer may approve for a report. Skipping is "
                          "about waste, never about coverage: an excluded image is one nobody "
                          "will report on.",
        "filters_cost_nothing": "Perceptual hashing and the blur measure run locally, without a "
                                "model call.",
        "estimates_only": "Every eligibility proportion below is an ESTIMATE from the stated "
                          "assumptions. None has been measured. The pilot's first month replaces "
                          "them with counts.",
        "estimated_eligibility": {
            "captured_per_month_pilot": 360,
            "assumptions": [
                {"class": "near-duplicate", "share": 0.08,
                 "basis": "supervisors take two or three of the same subject to be sure"},
                {"class": "below quality threshold", "share": 0.05,
                 "basis": "movement, low light, an obstructed lens"},
                {"class": "deleted or excluded before analysis", "share": 0.04,
                 "basis": "wrong subject, accidental capture"},
            ],
            "eligible_share": 0.83,
            "eligible_per_month_quick_share": 299,
            "eligible_per_month_ai_reviewed": 331,
            "ai_reviewed_note": "Immediate mode filters duplicates and unusable images locally "
                                "but cannot know what the supervisor will later exclude, so its "
                                "eligible count is higher.",
        },
    },
    "sharing": {
        "method": "native operating-system share sheet",
        "payload": "the stored image files themselves, plus a formatted text summary",
        "public_link_required": False,
        "public_link_permitted": False,
        "forbidden_methods": [
            "WhatsApp Web automation",
            "group scraping",
            "any unofficial messaging automation",
            "a publicly accessible Drive link",
            "any flow that asks the supervisor to select the files again",
        ],
        "recorded_as": ["SiteVisits.ShareStatus", "SiteVisits.SharedAt",
                        "SiteVisits.ShareAttemptCount"],
        "honest_limit": "The application can record that the share sheet was opened and that the "
                        "supervisor said it completed. It cannot observe delivery inside the "
                        "messaging application, and no document may claim otherwise.",
    },
    "platform_gate": {
        "id": "CAP-GATE",
        "question": "Can AppSheet reliably share multiple actual image files and formatted text "
                    "through the native share sheet to an existing WhatsApp or WhatsApp Business "
                    "group, on iOS and Android?",
        "status": "UNVERIFIED — requires real-device testing in Phase 2A",
        "test_matrix": [
            "one photograph", "six photographs", "portrait and landscape images", "image order",
            "formatted summary", "standard WhatsApp", "WhatsApp Business", "normal connection",
            "weak connection", "offline capture followed by synchronisation",
            "images attached or only links", "whether the user must select the images again",
            "whether a public Drive link is created",
            "whether temporary files remain on the device",
            "failed or cancelled share recovery",
        ],
        "fallback_options": [
            "AppSheet with a proven native-share method",
            "A lightweight custom PWA or mobile field application using supported native file "
            "sharing",
            "Any other official, policy-compliant approach",
        ],
        "invariant": "The data model, Drive security, Make orchestration, Claude controls, "
                     "approval rules and audit requirements must remain re-usable if the capture "
                     "interface changes.",
    },
}


# --------------------------------------------------------------------------
# 10. Assemble and write
# --------------------------------------------------------------------------
def main():
    # sanity checks before writing: a model that contradicts itself is worse than none
    problems = []
    for tname, t in TABLES.items():
        names = [c["name"] for c in t["columns"]]
        if len(names) != len(set(names)):
            problems.append(f"{tname}: duplicate column name")
        if t["primary_key"] not in names:
            problems.append(f"{tname}: primary key {t['primary_key']} is not a column")
        if t["scope"] == "project" and "ProjectID" not in names and tname not in (
                "ProjectAssignments",):
            problems.append(f"{tname}: project-scoped table without a ProjectID column")
        for c in t["columns"]:
            if c["type"] == "ref":
                ref = c.get("ref", "")
                rt, _, rc = ref.partition(".")
                if rt not in TABLES:
                    problems.append(f"{tname}.{c['name']}: reference to unknown table {rt}")
                elif rc not in [x["name"] for x in TABLES[rt]["columns"]]:
                    problems.append(f"{tname}.{c['name']}: reference to unknown column {ref}")
            if c["type"] == "enum" and c.get("enum") not in ENUMS:
                problems.append(f"{tname}.{c['name']}: unknown enum {c.get('enum')}")
            if c.get("ar") and c["ar"] not in names:
                problems.append(f"{tname}.{c['name']}: bilingual pair {c['ar']} missing")
        for combo in t["at_least_one"]:
            for f in combo:
                if f not in names:
                    problems.append(f"{tname}: at_least_one field {f} is not a column")
        for f in t["content_hash_fields"]:
            if f not in names:
                problems.append(f"{tname}: content_hash field {f} is not a column")
    for role, tbls in SECURITY["matrix"].items():
        for t in tbls:
            if t not in TABLES:
                problems.append(f"security matrix references unknown table {t}")
    for t in TABLES:
        for role in SECURITY["matrix"]:
            if t not in SECURITY["matrix"][role]:
                problems.append(f"security matrix missing {role}.{t}")
    for key, spec in TRANSITIONS.items():
        if spec["entity"] not in TABLES:
            problems.append(f"transitions reference unknown table {spec['entity']}")
        cols = [c["name"] for c in TABLES[spec["entity"]]["columns"]]
        if spec["field"] not in cols:
            problems.append(f"transitions reference unknown column {key}")

    for t in LEAN_MVP["tables"]:
        if t not in TABLES:
            problems.append(f"lean MVP names unknown table {t}")
    r1 = LEAN_MVP["release_1"]["tables"]
    if len(r1) != 12:
        problems.append(f"release 1 has {len(r1)} tables, expected 12")
    for t in r1:
        if t not in TABLES:
            problems.append(f"release 1 names unknown table {t}")
        if t not in LEAN_MVP["tables"]:
            problems.append(f"release 1 table {t} is not in the lean MVP")
    lo, hi = LEAN_MVP["target_range"]
    if not lo <= len(LEAN_MVP["tables"]) <= hi:
        problems.append(f"lean MVP has {len(LEAN_MVP['tables'])} tables, outside {lo}-{hi}")
    for t in list(LEAN_MVP["fold_ins"]) + list(LEAN_MVP["deferred_phases"]):
        for name in [x.strip() for x in t.split(",")]:
            if name in TABLES and name in LEAN_MVP["tables"]:
                problems.append(f"{name} is both lean and deferred")

    # capture once: the block must agree with the tables it describes
    for ref in (CAPTURE_ONCE["trusted_context_fields"]
                + CAPTURE_ONCE["forbidden_ai_written_columns"]
                + CAPTURE_ONCE["optional_note"]["fields"]
                + [p["column"] for p in CAPTURE_ONCE["ai_proposes"]]):
        tn, cn = ref.split(".")
        if tn not in TABLES:
            problems.append(f"capture_once names unknown table {tn}")
        elif cn not in [c["name"] for c in TABLES[tn]["columns"]]:
            problems.append(f"capture_once names unknown column {ref}")
    for ref in CAPTURE_ONCE["forbidden_ai_written_columns"]:
        tn, cn = ref.split(".")
        if tn in TABLES:
            for c in TABLES[tn]["columns"]:
                if c["name"] == cn and c.get("src") == "ai":
                    problems.append(f"{ref} is forbidden to AI but declared src=ai")
    for ref in CAPTURE_ONCE["optional_note"]["fields"]:
        tn, cn = ref.split(".")
        if tn in TABLES:
            for c in TABLES[tn]["columns"]:
                if c["name"] == cn and c["required"]:
                    problems.append(f"{ref} must be optional for a photographic submission")
    mi = CAPTURE_ONCE["minimum_interaction"]
    if mi["mandatory_manual_inputs"]:
        problems.append("the normal path declares a mandatory manual input")
    for entry in mi["auto_populated"]:
        tn, cn = entry["field"].split(".")
        if tn not in TABLES or cn not in [c["name"] for c in TABLES[tn]["columns"]]:
            problems.append(f"minimum_interaction names unknown column {entry['field']}")
        else:
            c = [x for x in TABLES[tn]["columns"] if x["name"] == cn][0]
            if c["required"] and not (c.get("auto") or c.get("default")):
                problems.append(f"{entry['field']} is required with no automatic source")
    for ref in mi["optional_inputs"]:
        tn, cn = ref.split(".")
        c = [x for x in TABLES.get(tn, {"columns": []})["columns"] if x["name"] == cn]
        if c and c[0]["required"]:
            problems.append(f"{ref} is listed as optional but is required")
    cl = CAPTURE_ONCE["classification"]
    for ref in cl["advisory"] + [cl["trusted"], cl["state"], cl["disposition"]]:
        tn, cn = ref.split(".")
        if tn not in TABLES or cn not in [c["name"] for c in TABLES[tn]["columns"]]:
            problems.append(f"classification names unknown column {ref}")
    tcol = [c for c in TABLES["Photos"]["columns"] if c["name"] == "ConfirmedActivityTypeID"]
    if not tcol or tcol[0].get("src") == "ai":
        problems.append("the trusted activity column is missing or AI-sourced")
    for m, spec in CAPTURE_ONCE["modes"].items():
        if spec["capture_count"] != 1:
            problems.append(f"capture mode {m} captures more than once")
        if "native share" not in spec["sequence"]:
            problems.append(f"capture mode {m} does not end at a native share")

    if problems:
        print("MODEL PROBLEMS:", file=sys.stderr)
        for p in problems:
            print("  -", p, file=sys.stderr)
        sys.exit(1)

    model = {
        "model_version": MODEL_VERSION,
        "model_date": MODEL_DATE,
        "phase": 1,
        "generated_by": "tools/build_model.py",
        "authority": "MASTER_SPEC.md section 5, as amended by owner decisions D-01..D-15 "
                     "(docs/00-discovery/10-owner-decisions.md)",
        "statement": "Synthetic and structural only. Contains no real client, person, contract, "
                     "credential or account identifier.",
        "enums": ENUMS,
        "tables": TABLES,
        "transitions": TRANSITIONS,
        "security": SECURITY,
        "canonical_hash": CANONICAL,
        "lean_mvp": LEAN_MVP,
        "capture_once": CAPTURE_ONCE,
    }
    out = os.path.join(ROOT, "model", "model.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(model, fh, indent=2, ensure_ascii=False, sort_keys=False)
        fh.write("\n")
    print(f"wrote {out}")
    print(f"  tables      : {len(TABLES)}")
    print(f"  columns     : {sum(len(t['columns']) for t in TABLES.values())}")
    print(f"  enums       : {len(ENUMS)}")
    print(f"  transitions : {sum(len(t['allowed']) for t in TRANSITIONS.values())} allowed, "
          f"{sum(len(t['forbidden']) for t in TRANSITIONS.values())} explicitly forbidden")
    print(f"  security    : {len(SECURITY['roles'])} roles x {len(TABLES)} tables = "
          f"{len(SECURITY['roles']) * len(TABLES)} grants, {len(SECURITY['exceptions'])} exceptions")
    print(f"  lean MVP    : {len(LEAN_MVP['tables'])} tables, "
          f"{len(TABLES) - len(LEAN_MVP['tables'])} deferred but designed")
    print(f"  interaction : {len(CAPTURE_ONCE['minimum_interaction']['mandatory_manual_inputs'])} "
          f"mandatory manual inputs on the normal path, "
          f"{len(CAPTURE_ONCE['minimum_interaction']['auto_populated'])} fields populated "
          f"automatically")
    print(f"  capture once: {len(CAPTURE_ONCE['workflow'])} workflow steps, "
          f"{len(CAPTURE_ONCE['modes'])} modes, "
          f"{len(CAPTURE_ONCE['forbidden_ai_written_columns'])} columns closed to AI")
    print(f"  release 1   : {len(LEAN_MVP['release_1']['tables'])} tables "
          f"(capture and review; no document generation)")


if __name__ == "__main__":
    main()
