# ADR-0009 — Capture once, use twice, and share through the native share sheet

**Status:** Accepted · **Date:** 2026-09-11
**Relates to:** operating rules 9, 12, 13 · owner decisions D-16 to D-21 · R-06 · `CAP-01`, `CAP-GATE`
**Amends:** ADR-0004 (advisory AI) by naming what AI proposes and what it may never touch

## Context

The supervisor already photographs the work. Today they then open a messaging application and
**select the same photographs a second time** to send them to the main-contractor group. The company
ends up with its evidence in a chat thread, and the technical record — when one is written at all —
is reconstructed later from memory.

Any system that asks for a third act (capture, share, then re-enter for the record) is slower than
the habit it replaces, and R-06 says plainly what happens then: the pipeline starves and everything
downstream is worthless.

There is a second temptation with the same shape. Making the supervisor *write* what the photographs
already show is a second description of the same fact. It is the field-reporting equivalent of a
duplicate upload, and it is the field most often left blank or filled with "as per site".

## Options

1. **Capture once, use twice.** One capture. The stored files serve the group share and every
   report. AI proposes the classification; the supervisor confirms with minimum interaction; the
   written description becomes optional.
2. **Capture in the app, share separately.** Simplest to build. Keeps the second selection, keeps
   the habit intact, and leaves the app competing with the habit rather than absorbing it.
3. **Capture in WhatsApp, ingest afterwards.** Matches the habit exactly. Requires reading a group,
   which needs unofficial automation or scraping — forbidden by operating rules 12 and 13, and
   unavailable through the official Business API in any case.
4. **Share by link.** Upload, then send a link. Cheap in bytes. Requires a publicly accessible link
   to client-confidential evidence, which is forbidden, and delivers a worse artefact than the
   files themselves.

## Decision

**Option 1, with the share performed by the operating system's native share sheet.**

The supervisor captures or selects the photographs **exactly once**. The same stored files are
handed to the share sheet, where a human chooses the existing contractor group. The same files are
re-used by every daily, weekly, monthly, corrective-action, inspection and completion report.

**`CAP-01` is the acceptance requirement:** *the workflow fails acceptance if the supervisor must
select or upload the images a second time.* It binds the first share, a retry after a failed or
cancelled share, AI analysis, reviewer correction, and every report that re-uses the evidence.

**Two operating modes**, both capturing once. *Quick Share*: capture, store, share immediately; AI
runs afterwards and prepares the internal metadata. *AI Reviewed Share*: capture, AI proposal,
supervisor confirmation, share.

**The written description becomes optional** for a normal photographic submission. An optional
*Additional Site Note*, classified by `SiteNoteCategory`, carries what a photograph cannot: a client
instruction, an access restriction, a permit issue, a hidden defect, a measured quantity, a material
batch, an equipment failure, a reason for non-completion, a safety restriction, work postponed by
another party.

**AI proposes into its own columns and decides nothing.** Visible activity, evidence stage, caption,
visible condition, possible snag, image-quality warning, uncertainty and confidence — each to a
dedicated advisory field, none in any content hash. Sixteen columns are closed to AI by declaration
and by automated check. The AI's view of the activity is free text, deliberately **not** a reference
to `ActivityTypes`, so no contractual activity can be created by an image.

## Consequences

**Accepted:**

- The share is **unobservable**. The application can record that the share sheet was opened and that
  the supervisor said it completed. It cannot see delivery inside the messaging application, and no
  document may claim otherwise.
- The capture platform now carries a **pass/fail requirement it may not meet**. `CAP-GATE` is
  unverified on every platform; fifteen conditions are tested on real devices.
- Quick Share means the internal metadata is **complete later than the share**. That is deliberate:
  the contractor's need is immediate, the report's need is not.
- Advisory analysis costs money per photograph, and the derivative transfer has a volume ceiling.

**Refused, permanently:**

- A duplicate-upload workaround. If the platform cannot share stored files, the platform changes.
- A publicly accessible link to evidence, for sharing or for analysis.
- WhatsApp Web automation, group scraping, or any unofficial messaging API.

**What this decision does not put at risk.** The canonical data model, Drive security, Make
orchestration, Claude controls, approval rules and audit requirements are defined independently of
the capture interface. If the interface changes, they are re-used unchanged. That is why the capture
platform is an *interface* decision and this ADR does not reopen ADR-0001, 0002, 0003 or 0006.

## Revisit when

- `CAP-GATE` is executed on real devices and returns a result, whichever way it goes.
- The official WhatsApp Business API gains a supported path for sending several image files to an
  existing group from a field application, at which point option 1 could keep its guarantees with
  fewer platform assumptions.
- Measured AI proposal acceptance is low. A supervisor who corrects most proposals is being slowed
  down by the feature, and AI Reviewed Share would then become the exception rather than the default.
