# Product Requirements Document (PRD)
## BizDesk: Small-Business Operations, Invoicing & Booking Suite

### 1. Executive Summary & Problem Statement
Independent service providers (dental/physiotherapy clinics, boutique salons, freelance consultants, private coaching academies) frequently organize business operations across disparate paper ledgers, fragmented WhatsApp threads, and ad-hoc spreadsheets. This manual workflow causes double-booked client slots, unbilled service add-ons, forgotten follow-ups, and unprofessional handwritten receipts. Enterprise ERP and SaaS platforms are prohibitive in cost and burdened with unnecessary enterprise complexity.

**BizDesk** is an agile, all-in-one business management toolkit tailored specifically for independent service operators. It brings client customer directory management, real-time appointment booking, automated tax/discount calculations, downloadable professional PDF invoices, and executive KPI dashboards into a single, cohesive workflow.

---

### 2. User Personas
- **Dr. Mehta (Clinic Practitioner)**: Needs to schedule patient appointments across morning/evening slots, view patient visit histories, and print neat itemized prescription/consultation invoices.
- **Priya (Salon & Spa Owner)**: Manages multi-service stylist bookings, tracks walk-in versus repeat customers, and issues invoices with tax and discounts.
- **Rohan (Academic Tutor / Coaching Academy)**: Tracks enrolled student batches, generates monthly fee receipts as professional PDFs, and monitors pending fee collections.

---

### 3. Scope & Prioritization (MoSCoW)
Scope is strictly frozen at the conclusion of Day 1.

#### MUST HAVE (Target MVP - Days 1-5)
- **Business Profile Customization**: Flexible presets allowing the workspace to adapt terminology for Clinics (Patients/Consultations), Salons (Clients/Treatments), or Coaching (Students/Classes).
- **Customer Directory (CRM)**: Add, update, search, and view client profiles, contact numbers, and cumulative visit histories.
- **Interactive Appointment Booking**: Time-slot calendar with double-booking collision prevention, service assignment, and status lifecycle management (Scheduled -> Completed -> Cancelled -> No-Show).
- **Automated Billing & Professional PDF Invoices**: Itemized service lines, customizable tax (GST/VAT) rates, percentage/flat discounts, and one-click downloadable PDF invoice generation using standard PDF rendering.
- **Actionable Reminders Checklist**: Dedicated daily planner highlighting today's scheduled appointments, unpaid overdue invoices, and pending client follow-ups.
- **Executive KPI Dashboard**: Visual revenue trajectory charts, total appointment metrics, top 5 booked services, and client retention rates powered by Recharts.
- **JWT Security & Auth**: Password-protected owner portal with bcrypt encryption and token persistence.

#### SHOULD HAVE (Days 5-6)
- Instant WhatsApp / SMS reminder text generator (one-click copy message pre-formatted with appointment details).
- CSV export for customer lists and monthly financial ledgers.

#### COULD HAVE (Deferred to Post-MVP)
- Online self-service appointment booking link for external customers.
- Payment gateway webhook integration (Razorpay / Stripe).

#### WON'T HAVE (Out of Scope for 7-Day Sprint)
- Complex multi-warehouse inventory physical barcode scanning.
- Automated payroll and employee tax deduction filing.

---

### 4. Non-Functional Requirements
- **Performance**: PDF invoice generation latency under 800ms; booking conflict check response under 50ms.
- **Data Integrity**: Enforced database constraints preventing duplicate booking of identical provider time slots.
- **Usability**: High-efficiency, zero-friction UI enabling an appointment to be booked in fewer than 3 clicks.
