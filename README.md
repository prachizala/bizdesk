# BizDesk: Small-Business Operations, Invoicing & Booking Suite

BizDesk is a high-efficiency business operations suite designed for independent clinics, boutique salons, and tutoring centers. It consolidates customer management, appointment scheduling with collision prevention, and automated tax/discount calculations with downloadable vector PDF invoices.

---

## Key Features

1. **Appointment Scheduler with Collision Prevention**:
   - Enforces temporal non-overlap constraints: $(A_{start} < B_{end}) \land (A_{end} > B_{start})$ preventing double-booking.
2. **Automated Invoicing & Vector PDF Generator**:
   - Itemized service lines, customizable GST/VAT rates, percentage discounts, and one-click PDF generation via PyMuPDF.
3. **Customer CRM Directory**:
   - Centralized customer contact details and cumulative visit records.
4. **Owner KPI Dashboard**:
   - Real-time gross billings, total appointments, and automated daily reminders.

---

## Quickstart Guide

```bash
cd backend
python seed_data.py
python -m pytest -v tests/
uvicorn app.main:app --reload --port 8000
```
Open `http://localhost:8000` to interact with BizDesk.

---

## Author
**Prachi Zala** | [GitHub](https://github.com/prachizala)
