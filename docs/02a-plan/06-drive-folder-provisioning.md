# Google Drive Folder Provisioning Design

**Document ID:** AH-SYS-P2A-006 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Nothing provisioned, nothing connected**

---

## 1. Structure

```
[Shared Drive: company-owned]                     ← never a personal My Drive (ADR-0001)
└── Al-Haram Operations/
    └── {ProjectCode}/
        └── {YYYY}/
            └── {MM}/
                ├── 01_Original_Evidence      write-once · never shared · never modified
                ├── 02_Derived_Images         previews, crops, report-ready renditions
                ├── 03_Draft_Reports
                ├── 04_Approved_Reports
                ├── 05_Completion_Certificates
                ├── 06_Invoice_Support
                ├── 07_Released_Documents
                └── 08_Archive
```

## 2. Provisioning algorithm — idempotent by construction

```
provision(project, year, month):
    parent = resolve_or_create(root_folder_id, project.ProjectCode)
    parent = resolve_or_create(parent, year)
    parent = resolve_or_create(parent, month)
    for name in EIGHT_SUBFOLDERS:
        resolve_or_create(parent, name)
    record every returned folder ID against the project/period

resolve_or_create(parent_id, name):
    hits = list children of parent_id where name == exact match and not trashed
    if len(hits) == 1: return hits[0].id
    if len(hits) == 0: return create(parent_id, name).id
    if len(hits)  > 1: ERROR — duplicate folder, human resolution, never guess
```

Three rules make this safe:

1. **Look up before creating, always.** Drive permits duplicate names in one folder; creating blind eventually produces two `01_Original_Evidence` folders and evidence split between them (P-11).
2. **More than one match is an error, not a choice.** Picking the first would silently divide an archive.
3. **Record the returned folder ID.** Everything downstream addresses folders and files by ID, so an organisational rename never breaks a reference.

Running provisioning twice creates nothing the second time. That is a Phase 3 gate check.

## 3. Permissions

| Folder | Who | Rule |
|---|---|---|
| Shared Drive root | Company | Managers: the general manager and the system administrator. **Never a single personal owner** |
| `01_Original_Evidence` | System account writes; reviewers read through the app | **Never shared with anyone outside the company, ever, by any mechanism** |
| `02_Derived_Images` | System account | Derivatives only; originals are never written here |
| `03_Draft_Reports` | System account, reviewers | Internal |
| `07_Released_Documents` | System account | Least-privilege link at release, recorded in the recipient snapshot |
| `08_Archive` | System account | Read-only after retention review |

**No folder is ever made link-accessible to anyone with the link.** Client-facing access, where it
exists at all, is a specific document shared with a specific named recipient at release.

## 4. Write-once enforcement for originals

The platform cannot make a folder append-only by itself, so the guarantee is enforced by the paths
that exist rather than by a setting:

1. Only the registration scenario writes to `01_Original_Evidence`, and only ever creates.
2. No scenario, action or app view offers update or delete on an original.
3. The checksum is recorded at registration and re-verified; a change is a detectable defect.
4. Every derivative is written to `02_Derived_Images` with its own record.
5. AI analysis receives a **derivative**, never the original — so no processing path ever opens the write-once file (P-07, D-13).

## 5. File naming

Photographs: `{ProjectCode}-{LocationCode}-{YYYYMMDD}-{ActivityCode}-{Stage}-{PhotoID}.{ext}`
Documents: `{YYYY-MM-DD}-{EntityCode}-{DocumentType}-{ProjectCode}-{Period}-{Revision}.{ext}`

Sanitisation: permit `A-Z a-z 0-9 - _ .` only; replace everything else with `-`; collapse repeats;
cap length by truncating the descriptive part and never the identifier. **Arabic never appears in a
filename** — it lives in the record and in the document content, where it renders correctly, while
filenames stay ASCII so every tool, operating system and archive handles them predictably.

## 6. Failure handling

| Failure | Class | Response |
|---|---|---|
| Folder not found after creation | `Conflict` | One delayed retry, then dead-letter. Never create a second |
| Duplicate folder name | `Conflict` | Dead-letter for human resolution. Never guess |
| Quota exceeded | `ProviderUnavailable` | Retriable with backoff; alert the administrator |
| Permission denied | `Authorization` | **Never retried.** Alert immediately; possible security event |
| File already registered | `Duplicate` | Suppressed and logged. Expected, not an error |

## 7. What is required before any of this runs

| Requirement | Status |
|---|---|
| Company Workspace tenant confirmed as paid, with Shared Drive capability | **Pending (EF-01)** |
| The owning system account | **Pending (EF-01)** |
| The Shared Drive and its root folder | **Pending (EF-01)** |
| OAuth connection, authorised by the owner personally in the provider's console | Phase 3 |
| Residency review for each project whose data will be uploaded | **Pending (EF-16)** |

Until all five exist, this design runs against local fixtures and synthetic references only
(D-03, D-14).
