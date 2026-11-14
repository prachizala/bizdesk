# Technical Interview Questions & Answers — BizDesk

Based on the actual codebase in `bizdesk`.

---

### Question 1: How does the temporal collision detection algorithm prevent double-booking in `appointment_service.py`?
**Answer:**
In `app/services/appointment_service.py`, appointment intervals are modeled as half-open or closed temporal ranges.
1. **Conversion:** Start and end times in `"HH:MM"` format are converted to absolute minutes from midnight:
   $$\text{minutes} = \text{hours} \times 60 + \text{minutes}$$
2. **Interval Overlap Condition:** An incoming booking $[N_{start}, N_{end}]$ collides with an existing booking $[E_{start}, E_{end}]$ if and only if:
   $$(N_{start} < E_{end}) \land (N_{end} > E_{start})$$
3. **Boundary Semantics:** If Appointment 1 is `09:00 - 10:00` (minutes 540 to 600) and Appointment 2 is `10:00 - 11:00` (minutes 600 to 660):
   $$(540 < 660) \land (600 > 600) = \text{True} \land \text{False} = \text{False}$$
   No collision is detected, allowing seamless back-to-back scheduling. However, if Appointment 2 requests `09:59 - 10:30`:
   $$(540 < 630) \land (600 > 599) = \text{True} \land \text{True} = \text{True}$$
   A collision is detected, and the API returns an HTTP 409 Conflict.

---

### Question 2: How does the vector PDF invoice generator work in `invoice_service.py`?
**Answer:**
`generate_invoice_pdf()` uses PyMuPDF (`fitz`) to build an A4 invoice directly in memory:
1. **Document Setup:** A new page is created with dimensions $595 \times 842$ points (standard A4).
2. **Vector Primitives:** Rectangles and header banners are rendered via `page.draw_rect()`, and typography is positioned using `page.insert_text()` with point coordinates, Helvetica fonts, and RGB color tuples.
3. **Dynamic Calculations:**
   - Subtotal: $\sum (\text{quantity} \times \text{unit\_price})$
   - Taxable Amount: $\max(0.0, \text{subtotal} - \text{discount})$
   - Tax: $\text{taxable} \times \frac{\text{tax\_rate\_pct}}{100.0}$
   - Total: $\text{taxable} + \text{tax}$
4. **Deterministic Resource Cleanup:** The document creation is wrapped in a strict `try...finally` block:
   ```python
   doc = fitz.open()
   try:
       # Draw header, table headers, item rows, totals...
       doc.save(output_path)
   finally:
       doc.close()
   ```
   Invoking `doc.close()` guarantees immediate C-level memory reclamation, preventing leaks in long-running services.

---

### Question 3: Describe a schema validation bug you fixed in BizDesk.
**Answer:**
**The Bug:** An appointment request payload with an inverted time window (e.g., `start_time: "14:00"`, `end_time: "13:00"`) bypassed schema validation and reached `check_time_collision()`, which raised a generic Python `ValueError("Start time must be strictly before end time.")`. This caused FastAPI to return an unhandled HTTP 500 Internal Server Error.  
**The Solution:** I implemented a Pydantic v2 model validator on the request schema:
```python
@field_validator("end_time")
@classmethod
def validate_time_order(cls, v: str, info: ValidationInfo) -> str:
    start_time = info.data.get("start_time")
    if start_time and time_to_minutes(start_time) >= time_to_minutes(v):
        raise ValueError("end_time must be strictly after start_time")
    return v
```
This rejected chronological inversions at the schema boundary, returning an immediate, structured HTTP 422 Unprocessable Entity with clear error messaging before any database interaction.

---

### Question 4: How does the dashboard endpoint aggregate financial metrics?
**Answer:**
In `app/api/v1/endpoints/dashboard.py`, SQLite executes single-pass aggregations:
- **Total Revenue:** `SUM(total_amount)` where `status = 'paid'`
- **Pending Receivables:** `SUM(total_amount)` where `status = 'sent'` or `'unpaid'`
- **Active Appointments:** `COUNT(id)` where `status = 'confirmed'` and `date >= date('now')`
- **Customer Volume:** `COUNT(id)` from `customers` table
This delivers sub-10ms response times for small-to-medium enterprise management without external caching layers.
