# Naming, Numbering and File Conventions

**Document ID:** AH-SYS-P1-006 · **Revision:** 1 · **Date:** 2026-09-11
**Delivers:** D-15 item 9 · **Implements:** D-10, ADR-0005 rev 1 · **Closes:** C-04
**Executable statement:** `tools/numbering.py` · **Evidence:** `17-validation-evidence.md` (NUM-01 … NUM-13)

---

## 1. Document numbering

### 1.1 One service, many series — never one sequence

A series is configured by **legal entity × document type × year basis × scope × optional client
requirement**, with its own format, padding, start number and reset rule. Nothing about this is in
code; it is all `NumberingSeries` rows (D-10).

| Dimension | Options | Why it exists |
|---|---|---|
| Legal entity | Any configured entity | A second registered entity must not share a sequence with the first (NUM-05) |
| Document type | Any configured type | A technical report and a quotation are different series in different registers |
| Year basis | Calendar, financial (with a start month), or none | The company's own convention decides, not the software |
| Scope | Company-wide, per project, or per client | Some clients require their own run; most do not (NUM-04) |
| Reset rule | Per year, or never | Continues however the existing register behaves |

Illustrative formats, **pending review of the existing manual register** (D-10):

```
{ENTITY}-TR-{YYYY}-{NNN}     technical report
{ENTITY}-QT-{YYYY}-{NNN}     quotation
{ENTITY}-CC-{YYYY}-{NNN}     completion certificate
{ENTITY}-{PROJECT}-TR-{YYYY}-{NNN}   a project-scoped run
```

Invoice-related series carry `AlignedToAccountingProcess = TRUE`: their numbering follows the
approved accounting process rather than this system's convention (D-10, D-07).

### 1.2 Lifecycle: reserved → issued → cancelled

| State | When | Rules |
|---|---|---|
| **Reserved** | Atomically, when a document job freezes its snapshot | Bound to the job. No two callers can ever receive the same number (NUM-01) |
| **Issued** | When the document is actually created | Bound to the document. Cannot be re-issued or cancelled (NUM-10, NUM-11) |
| **Cancelled** | When the job fails or is abandoned | **A reason is mandatory** (NUM-08). The number is never reused (NUM-09, TRN-07) |

Revision 0 of ADR-0005 said numbers would never be reserved, to avoid gaps. The owner replaced that
with this explicit lifecycle, and the reasoning is better: a gap is going to happen anyway when a
generation fails, so the honest design records **why** each gap exists. An unexplained gap invites
exactly the suspicion a numbering system exists to prevent.

### 1.3 Migration from the existing manual register

Each series records `MigratedFromManualRegister` and `LastManualNumber`. Seeding the last manual
number makes the system continue the register rather than restart it — verified by NUM-12, where a
series seeded at 147 issues 148 next.

**Until the existing register has actually been reviewed, no production number may be issued.** That
review is an outstanding external fact (`16-external-facts-register.md`, EF-08).

### 1.4 Concurrency

The reference implementation uses an atomic read-and-increment inside a transaction. Eight
concurrent threads reserving 25 numbers each produce 200 distinct numbers with no collisions and no
errors (NUM-01). In production the same contract is met by the orchestration platform's atomic
data-store update. **A spreadsheet never performs an increment** (C-04, P-01).

## 2. File naming

### 2.1 Photographs

```
{ProjectCode}-{LocationCode}-{YYYYMMDD}-{ActivityCode}-{Stage}-{PhotoID}.{ext}
```

### 2.2 Documents

```
{YYYY-MM-DD}-{EntityCode}-{DocumentType}-{ProjectCode}-{Period}-{Revision}.{ext}
```

### 2.3 Sanitisation

- Permitted characters: `A-Z a-z 0-9 - _ .` Everything else is replaced with `-`.
- Arabic text never appears in a filename. Arabic identity lives in the record and in the document content, where it renders correctly; filenames stay ASCII so that every tool, operating system and archive handles them predictably.
- Leading and trailing separators collapsed; consecutive separators reduced to one.
- Length capped, truncating the descriptive portion and never the `PhotoID` or revision.
- Reserved device names avoided.

### 2.4 Names are not keys

A filename is a convenience for a human opening a folder. Every database reference uses the storage
provider's file identifier, so a moved or renamed file never breaks a reference (P-11). Two files
may legitimately share a name in different folders; nothing in the system cares.

## 3. Folder provisioning

```
Al-Haram Operations/{ProjectCode}/{Year}/{Month}/
    01_Original_Evidence      write-once; never shared; never modified
    02_Derived_Images         previews, crops, report-ready renditions
    03_Draft_Reports
    04_Approved_Reports
    05_Completion_Certificates
    06_Invoice_Support
    07_Released_Documents
    08_Archive
```

Provisioning is idempotent: look up by parent and exact name, create only if absent, and record the
returned identifier. Running it twice creates nothing the second time — a Phase 3 gate check.

**Nothing is provisioned in Phase 1.** No production Drive account is connected (D-14), so these
columns hold synthetic references until Phase 3 is authorised.
