# Representative User and Device Profiles (EF-05)

**Document ID:** AH-SYS-P1-019 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review
**Purpose:** design and synthetic testing while real names, emails and devices remain pending

> **No real person is named anywhere in this repository.** These are profiles, not people. When the
> owner supplies real identities, each profile maps to one or more actual users; until then every
> test runs against the synthetic accounts listed in the last column, all on the reserved
> `@synthetic.example` domain (asserted by check ACC-31).

---

## 1. The seven profiles

| # | Profile | Represents | Assigned projects | Interface language | Device and network | Synthetic account |
|---|---|---|---|---|---|---|
| **P-1** | iPhone supervisor | A supervisor on a recent iOS device with a good camera | One project | English | iOS, current major version, office Wi-Fi and 4G | `USR-0005` |
| **P-2** | Android supervisor | A supervisor on a mid-range Android handset — the commonest real case | One project | Arabic | Android, one or two versions behind current, 4G | `USR-0006` |
| **P-3** | Weak-connectivity supervisor | Works where coverage drops: basements, plant rooms, remote compounds | One project | Arabic | Android, intermittent 3G, long offline periods | `USR-0006` under the offline scenario |
| **P-4** | Single-project user | Sees exactly one project and must never see another | One project | English | Either platform | `USR-0008` |
| **P-5** | Multi-project user | Moves between projects in a single day; the highest-risk case for leakage | **Two projects** | Arabic | Android | `USR-0007` |
| **P-6** | English-interface user | Office or review user working in English | All assigned | English | Desktop browser and mobile | `USR-0003` |
| **P-7** | Arabic-interface user | Field or office user working in Arabic, including Arabic text entry | Assigned | Arabic | Mobile, Arabic keyboard | `USR-0005` (Arabic preference) |

Two negative profiles exist in the fixtures because they are the cases most likely to be got wrong:

| # | Profile | Purpose | Account |
|---|---|---|---|
| **P-8** | Unassigned user | A valid account with no project assignment must see nothing at all | `USR-0011` |
| **P-9** | Expired-assignment user | An assignment that has ended grants nothing, even though the row still exists | `USR-0012` |

## 2. What each profile must demonstrate at the Phase 2 gate

**These are field tests. None has been performed, and none can be performed until real devices and
real supervisors are available (EF-05).**

| Profile | Must demonstrate |
|---|---|
| P-1, P-2 | Camera capture; multiple photographs on one activity; what the stored file actually is compared with the camera file (C-02 / D-13); form completion time |
| P-3 | Start the app offline; complete a visit with photographs offline; keep it queued for hours; sync on reconnection with every photograph and in the right order; behaviour when the device is restarted mid-queue |
| P-4 | Sees exactly one project everywhere: lists, search, dropdowns, and a deep link to another project's record |
| P-5 | Switches projects without any record, location, template, recipient or photograph crossing over; the single most important segregation test on a real device |
| P-6, P-7 | Complete a visit end to end in each language; Arabic text entry preserved exactly; layout usable right-to-left |
| P-8 | Signs in successfully and sees no project data of any kind |
| P-9 | Signs in successfully and sees nothing, despite an assignment row existing |

## 3. What is already proven in logic, and what is not

| Aspect | Proven now | Requires a real device |
|---|---|---|
| Single-project user sees one project | `SEG-01`, `SEG-02` | Confirmation in the app's UI, search and deep links |
| Multi-project user stays separated | `SEG-04` | Confirmation while switching projects on a phone |
| Unassigned user sees nothing | `SEG-02` | Confirmation at the sign-in boundary |
| Expired assignment grants nothing | `SEG-03` | Confirmation that the platform re-evaluates on sync |
| Arabic preserved without transliteration | `LNG-06` … `LNG-13` | Arabic keyboard entry, rendering, and RTL layout |
| Language preference per user | `LNG-03` | Interface actually switching |
| Offline capture | **Nothing** | Everything — the platform's offline behaviour is entirely untested (A-15) |
| Image fidelity | **Nothing** | Everything — the C-02 question can only be answered on a device |

The second column is deliberately short. Local checks prove rules; a phone in a plant room proves a
system.

## 4. Device matrix to confirm before the field test

To be completed by the owner as part of EF-05. Model names and versions are what actually determines
camera behaviour, offline storage and Arabic rendering.

| Item | To confirm |
|---|---|
| iOS devices in use | Models and OS versions |
| Android devices in use | Models and OS versions, particularly the oldest still in service |
| Ownership | Company-managed or personally owned — this affects what may be installed and what a client contract permits (EF-16) |
| Storage headroom | Whether devices have room for an offline photograph queue |
| Data plans | Whether supervisors are syncing on personal data allowances |
| Arabic keyboards | Whether Arabic input is already configured |

## 5. How profiles are used before real people exist

1. **Synthetic accounts** exercise every access rule, today, in the check suites.
2. **Phase 2A prototype design** builds views, slices and security filters against these profiles, so the app is designed for the real cases rather than for an average user who does not exist.
3. **Offline test plan** (`docs/02a-plan/05-offline-test-plan.md`) is written per profile, so that when devices arrive the test is already defined.
4. **When the owner supplies real identities**, each becomes a `Users` row with a `ProjectAssignments` row, and nothing in the design changes — which is the point of building against profiles.
