# QuickBooks Mapping and Compatibility Inspection

**Document ID:** AH-SYS-P1-013 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Inspection not yet executed**
**Delivers:** D-15 item covering accounting mapping · **Implements:** D-07 · **Relates to:** ADR-0008, R-02

> Al-Haram currently uses QuickBooks Online, so it remains the intended accounting system. What is
> **not** assumed is that every required integration, tax setting, project feature, class, currency
> or API operation is available for the *current company configuration* (D-07).
>
> **Nothing is connected and nothing is posted in Phase 1.** No customer, item, invoice or
> transaction is created (D-14).

---

## 1. Mapping fields

The system stores immutable accounting identifiers and never matches on names. Name matching is how
duplicate customers get created (§8 scenario 10).

| System field | Accounting concept | Rules |
|---|---|---|
| `Clients.QuickBooksCustomerID` | Customer | Stored once, never derived from a name. Absent means "not yet mapped", never "create a new one" |
| `BOQItems.QuickBooksItemID` | Product/service item | Mapped per BOQ item or per category, decided during inspection |
| `Materials.QuickBooksItemID` | Product/service item | Optional; material usage never creates an accounting transaction (§5.12) |
| `InvoiceLines.TaxCode` | Tax code | Comes from the confirmed tax rule, never invented (D-08) |
| `InvoiceLines.Class` | Class | Only if classes exist on the company file |
| `InvoiceLines.ProjectReference` | Project or job | Only if the feature exists on this edition |
| `InvoiceLines.CostCenter` | Location or department | Only if configured |
| `InvoiceRequests.Currency` | Transaction currency | Must match the contract; no conversion is performed (C-09) |
| `InvoiceRequests.PaymentTermsDays` | Terms | Due date is derived here and reconciled against the accounting system's own calculation |
| `InvoiceRequests.DraftInvoiceNumber` | — | **Internal only.** Never sent as the accounting document number |
| `InvoiceRequests.FinalInvoiceNumber` | Document number | Returned by the accounting system, or issued per the approved accounting process (D-10) |
| `InvoiceRequests.QuickBooksInvoiceID` | Invoice identifier | Returned on posting; the key for any later reconciliation |
| Income account mapping | Chart of accounts | Per service line, supplied by the accountant |

## 2. Compatibility inspection checklist

**This is a gate before the financial-integration phase** (D-07). Each answer is recorded with its
date and source. An unanswered row blocks that phase, not Phase 1.

### Company file and edition
1. Which company file (identifier) is the production file, and which region and edition is it?
2. Is a sandbox or test company available? If not, what is the safe test path?
3. Which base currency is the file configured in, and is multi-currency enabled?
4. Is the file's financial year start month the same as the one configured in the numbering series?

### Tax
5. What tax codes exist on the file today, and what does each mean?
6. Which code — if any — corresponds to the treatment the accountant confirms in writing (D-08)?
7. Can a line be posted with no tax code at all, or does the file require one?
8. Does the file compute tax itself, and will its computation agree with ours to the last decimal?

### Customers and items
9. Do customers already exist for these clients, and what are their immutable identifiers?
10. Are duplicate customers already present under variant names? (If so, mapping must resolve it first, not paper over it.)
11. Do product/service items exist that correspond to the BOQ categories, and what are their identifiers?
12. Are items configured with income accounts that match the accountant's expectation?

### Structure
13. Are **classes** enabled on this file?
14. Is the **projects/jobs** feature available on this edition?
15. Are locations or departments in use?
16. What is the existing invoice numbering convention, and is it automatic or manual?

### API
17. Which API operations are available for this edition: create invoice, read customer, read item, read tax code, attach a file?
18. What are the current rate limits, and what do they mean for a monthly billing run?
19. What is the OAuth application setup, and who holds the authorisation? (The owner authorises personally; no credential passes through chat or this repository.)
20. Does the API return enough detail to reconcile totals line by line, or only a summary?

### Process
21. Who currently creates invoices, and would this integration change their role?
22. Is there an approval step in the existing accounting process that must be preserved?
23. What happens to an invoice that is posted and later found wrong — credit note, void, or edit?
24. Does the accountant want drafts to appear in the accounting system, or only finalised invoices?

## 3. Reconciliation rule

Before an invoice request is marked synchronised:

1. Read back the posted document from the accounting system.
2. Compare **subtotal, each line amount, tax, retention treatment, discount and total** against the locally calculated figures.
3. Any difference, however small, sets `QuickBooksStatus = ReconciliationFailed` and raises it for a human. **It is never auto-corrected in either direction.**
4. Only an exact match sets `Posted`.

A difference means either our calculation or the file's configuration is wrong. Both are worth
knowing about; neither is worth hiding.

## 4. Sequencing

| Phase | Accounting activity |
|---|---|
| 1 | Mapping fields defined. Checklist written. **Nothing connected** |
| 6 | Deterministic calculation, certificates and invoice **drafts**. Still nothing connected |
| 7 | Inspection checklist executed. Sandbox posting. Finance approval. Reconciliation |
| 7+ | Production posting — **only after the owner authorises it in writing** (`QBO_POSTING_ENABLED` defaults to FALSE) |

## 5. If the inspection finds a gap

Because the calculation layer is independent of the accounting product (ADR-0008), a gap changes the
integration rather than the system. Options, in order of preference:

1. **Configure the company file** to support what is needed (add a tax code, enable classes).
2. **Adjust the mapping** to work within what exists (map several BOQ categories to one item).
3. **Export for manual entry** for the affected element, keeping the deterministic calculation and its trace.
4. **Reconsider the posting target**, which changes one integration and nothing else.

None of these requires redesigning the evidence pipeline, which is the point of keeping them
separate.
