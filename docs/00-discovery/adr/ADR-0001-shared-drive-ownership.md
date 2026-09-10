# ADR-0001 — Company-owned Shared Drive, system-owned account

**Status:** Proposed · **Date:** 2026-09-10 · **Relates to:** BQ-01, R-32, P-12

## Context
The system stores the company's photographic evidence, generated reports, completion certificates
and invoice support. That archive is the evidentiary basis for client claims, disputes and ISO
audits. Google offers two storage models: a personal My Drive, owned by an individual account, and a
Shared Drive, owned by the organisation.

Content in a personal My Drive belongs to that account. If the account is suspended or the person
leaves, access to the archive goes with them, and recovery is an administrative process performed
under pressure at the worst possible moment.

## Options
1. **Individual's My Drive.** Fastest to start. Single point of failure. Ownership transfer is manual and error-prone.
2. **Shared Drive owned by the organisation, with a dedicated system account as technical owner of the app and automations.** Requires a paid Workspace tenant.
3. **Third-party storage** (Dropbox, S3, on-premise). Breaks the native integration between the capture layer, the sheets and the documents, and adds a system to maintain.

## Decision
**Option 2.** All operational storage lives in a company-owned Shared Drive. The AppSheet
application, the operational sheets and the automation connections are owned by a **dedicated system
account** on the company domain (for example `operations@` or `system@`), not by an individual, with
the GM and the nominated system administrator as Shared Drive managers.

## Consequences
**Positive.** The archive survives any individual's departure. Access is administered centrally.
Audit logging is available. Ownership transfer is a permission change rather than a migration.
**Negative.** Requires a paid Workspace tenant (assumption A-01) and one additional licensed
account. Shared Drives have their own item limits, which must be monitored as evidence volume grows.
**Neutral.** The system account's credentials become a controlled asset requiring its own access
policy and recovery plan.

## Revisit if
A-01 proves false (no paid Workspace tenant), or BQ-10 reveals a contractual data-location
restriction that Google Workspace cannot satisfy.
