# Design Specification
## BizDesk: UI/UX & Component System

### 1. Visual Language & Aesthetics
BizDesk employs a refined, professional fintech aesthetic reminiscent of high-end business platforms like Stripe and Linear. Clean typography and high information density ensure business owners can review appointments and revenue at a glance.

- **Color Palette**:
  - **Executive Navy**: `#0f172a` (Sidebar background, primary headers)
  - **Dynamic Blue**: `#2563eb` (Primary CTA buttons, active calendar blocks)
  - **Emerald Revenue**: `#10b981` (Paid invoices, confirmed status, revenue growth)
  - **Amber Notice**: `#f59e0b` (Pending appointments, unpaid invoices)
  - **Rose Void**: `#ef4444` (Cancelled appointments, overdue notices)
  - **Neutral Canvas**: `#f8fafc` (Background canvas)
- **Typography**: Inter / system UI font stack with monospace tabular numerals for invoice totals and pricing grids.

---

### 2. Screen Workflows & Component Hierarchy
1. **Executive Dashboard**:
   - KPI Stat Cards: Monthly Revenue, Total Completed Appointments, Outstanding Receivables, Active Clients.
   - Revenue Velocity Chart: Area/line chart tracking gross billings over the trailing 30 days.
   - Quick Action Bar: `[+ New Appointment]`, `[+ New Customer]`, `[+ Create Invoice]`.
   - Today's Action Checklist: Chronological appointment timeline with status change toggles.
2. **Interactive Appointment Calendar**:
   - Day / Week / Month toggle views.
   - Color-coded service pills indicating appointment state.
   - Quick Booking Drawer: Select existing customer from auto-complete search, choose service, select time slot, and auto-verify availability.
3. **Invoicing & PDF Preview Screen**:
   - Split layout: Left pane: itemized service editor (line items, rates, GST tax toggle, discount input); Right pane: live interactive visual preview of the generated invoice PDF.
   - One-click triggers for `[Download PDF]`, `[Mark as Paid]`, and `[Copy WhatsApp Receipt Link]`.
