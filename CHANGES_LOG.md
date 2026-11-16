# Changes Log - BizDesk

## Work Package 5: Boilerplate Repos and Profile Review

### Summary of Changes
1. **README.md Overhaul**:
   - Upgraded documentation to enterprise standard with clear badges, project overview, and problem statement.
   - Documented core business features: appointment scheduler with collision prevention $(A_{start} < B_{end}) \land (A_{end} > B_{start})$, client ledger / CRM directory, multi-staff coordination, and automated invoicing with vector PDF generation.
   - Added complete API Endpoints table and reproducible `curl` examples for health check, client registration, appointment booking, PDF download, and dashboard metrics.
   - Added clear local run instructions with `uvicorn` (both root and backend execution paths) and Pytest execution guide.
2. **CI & Pytest Configuration**:
   - Added `pytest.ini` configuring `pythonpath = backend` so `pytest backend/tests/test_bizdesk.py` executes cleanly from repository root.
   - Refined `.github/workflows/ci.yml` to trigger on `push` (including `review-fixes`) and `pull_request`, running the pytest test suite under Python 3.11.
3. **Verification & Tests**:
   - Executed test suite locally: 7 passed out of 7 tests (`backend/tests/test_bizdesk.py`).

### Items Skipped & Rationale
- **Major Frontend Rewrite**: Skipped building an external React/Next.js client at this stage, as BizDesk functions as a lightweight operational prototype with working static assets and complete OpenAPI backend endpoints. Kept lean as recommended in the audit report.

### Manual Steps Needed
- None required for local testing or CI. If deploying to cloud (e.g. Render / Railway), configure persistent storage volume for `backend/bizdesk.db` and output directory `invoices/`.
