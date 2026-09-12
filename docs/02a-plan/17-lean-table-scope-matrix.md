# Lean MVP Scope Matrix — 17 Tables, One Page

**Document ID:** AH-SYS-P2A-017 · **Revision:** 1 · **Status:** generated — do not hand-edit
**Generated:** 2026-09-12 from `model/model.json` by `tools/gen_scope_matrix.py`

> Field counts come from the canonical model and cannot drift. **Row estimates are
> arithmetic from the assumptions in [`14-storage-and-image-volume.md`](14-storage-and-image-volume.md)
> — expected scenario, per project per month. They are not measurements.**

| # | Table | Purpose | Primary user | Fields | Rows /project /month | In the app | Syncs to device | Deferrable | Depends on |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `Users` | Who may sign in, and in what default role | Administrator | 15 | 0.2 | Yes | Yes (small) | No — nothing works without it | - |
| 2 | `Projects` | All project configuration; carries client display name in the lean build | Business admin | 29 | 0.1 | Yes | Yes (small) | No | LegalEntities |
| 3 | `ProjectAssignments` | The only source of row-level access | Administrator | 14 | 0.5 | Yes | Yes (small) | No — removing it removes segregation | Users, Projects |
| 4 | `Locations` | Hierarchical, project-scoped locations | Business admin | 16 | 1 | Yes | Yes | No | Projects, Locations (self) |
| 5 | `ActivityTypes` | Catalogue of 34 activities and default evidence rules | Business admin | 18 | 0.2 | Yes | Yes (small) | No | - |
| 6 | `ProjectActivityRules` | Per-project overrides of those rules | Business admin | 16 | 1 | Yes | Yes (small) | Yes, at the cost of every project behaving identically | Projects, ActivityTypes |
| 7 | `SiteVisits` | One reporting event; the unit of submission and review | Supervisor | 37 | 20 | Yes | Yes | No | Projects, Locations, Users |
| 8 | `VisitActivities` | What was done, quantity, supervisor confirmation | Supervisor | 19 | 40 | Yes | Yes | No | SiteVisits, ActivityTypes |
| 9 | `Photos` | Write-once evidence, reviewer decision, advisory AI fields | Supervisor, reviewer | 64 | 120 | Yes | Yes — **the volume driver** | No | SiteVisits, VisitActivities |
| 10 | `Snags` | Defects tracked to closure with evidence | Supervisor, reviewer | 24 | 3 | Yes | Yes | Yes — a snag can be a photograph with a caption at first | Photos, Locations |
| 11 | `Approvals` | Every decision, bound to a content hash | Reviewer, GM | 23 | 25 | Yes | Reviewers only | No — removing it removes the audit defence | Users |
| 12 | `DocumentJobs` | A report request with a frozen input snapshot | GM, project manager | 27 | 1 | Yes | No | Yes, if reports stay manual at first | Projects |
| 13 | `Documents` | A produced revision, release-controlled | GM | 25 | 1 | Yes | No | Yes, with DocumentJobs | DocumentJobs, LegalEntities |
| 14 | `NumberRegister` | Reserved / issued / cancelled document numbers, with reasons | System | 18 | 1 | Read-only view | No | Only with Documents | Documents, LegalEntities |
| 15 | `LegalEntities` | Company identity printed on every issued document | GM | 29 | ~0 | Admin view only | No | Only if no document is issued | - |
| 16 | `AuditLog` | Append-only record of every state transition | System; auditor reads | 13 | 150 | Admin view only | No | No | - |
| 17 | `IntegrationJobs` | One row per external call, with failure class | Administrator | 18 | 260 | Admin view only | No | Only while nothing is automated | - |
| | **17 tables** | | | **405** | **~624** | | | | |

## What the numbers say

- **405 fields across 17 tables.** The reference architecture holds 857 fields across 46 tables; the rest is designed and deferred.
- **~624 rows per project per month**, of which **120 are photographs** — roughly 19% of all rows. Every capacity question is really a question about photographs.
- **Only six tables sync to a field device**: Users, Projects, ProjectAssignments, Locations, ActivityTypes, ProjectActivityRules — plus the supervisor's own visits, activities and photographs. The five largest tables by growth never reach a phone in full.
- **Four tables are admin-only views**: NumberRegister, LegalEntities, AuditLog, IntegrationJobs. A field user's data set does not contain them.

## What could still be cut, and what it would cost

| Could be cut | Saves | Costs |
|---|---|---|
| `DocumentJobs` + `Documents` + `NumberRegister` | 3 tables, the whole report engine | Reports stay manual. **Capture and review still work** — this is the natural capture-only first release if the field test needs to come sooner |
| `Snags` | 1 table | Defects become photographs with captions; no tracking to closure |
| `ProjectActivityRules` | 1 table | Every project gets identical evidence rules |
| `LegalEntities` | 1 table | Only possible if no document is issued at all |

**A capture-and-review-only first release is 12 tables.** That is the floor of the range the owner set, and it is a legitimate option if getting a phone into a supervisor's hand sooner matters more than producing the first monthly report from the system.

## Sync load on a field device

What a supervisor's phone actually holds, for one project, after one month, under the expected scenario:

| Table | Rows on device | Note |
|---|---|---|
| Users | ~20 | Whole company; small |
| Projects | 1-3 | Only assigned projects |
| ProjectAssignments | ~5 | Only their own |
| Locations | ~30 | Only assigned projects |
| ActivityTypes | 34 | Whole catalogue; static |
| ProjectActivityRules | ~10 | Only assigned projects |
| SiteVisits | ~20/month | Their project, current period |
| VisitActivities | ~40/month | |
| Photos | ~120/month | **Metadata only.** Image bytes stream from storage, not from the row |
| Snags | ~3/month | Open ones |

**Roughly 280 rows after a month, 3,400 after a year on one project.** The sync cost is manageable; the growth risk is the shared Photos table across all projects, which is what the migration thresholds in [`18-migration-threshold-strategy.md`](18-migration-threshold-strategy.md) watch.
