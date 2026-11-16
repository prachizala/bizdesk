# BizDesk: Small-Business Operations, Invoicing & Scheduling Suite

[![BizDesk CI](https://github.com/prachizala/bizdesk/actions/workflows/ci.yml/badge.svg)](https://github.com/prachizala/bizdesk/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

BizDesk is a high-efficiency business operations suite designed for independent clinics, boutique salons, and tutoring centers. It consolidates customer relationship management, appointment scheduling with automated collision prevention, multi-staff calendar coordination, and automated tax/discount calculations with downloadable vector PDF invoices.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [API Endpoints & curl Samples](#api-endpoints--curl-samples)
- [Local Setup & Run Guide](#local-setup--run-guide)
- [Testing](#testing)
- [Continuous Integration](#continuous-integration)
- [Roadmap & Enhancements](#roadmap--enhancements)
- [Author & License](#author--license)

---

## Project Overview

Independent service providers often spend hours weekly managing fragmented spreadsheets, chasing invoice discrepancies, and resolving scheduling double-bookings. BizDesk provides a clean, API-first backbone accompanied by a lightweight frontend to automate the complete client lifecycle—from initial appointment booking to final invoice generation and financial metrics reporting.

---

## Problem Statement

Small service businesses face three operational bottlenecks:
1. **Schedule Collisions:** Manual calendar tracking leads to overlapping customer slots, staff confusion, and frustrated clients.
2. **Billing Delays:** Handcrafted invoices take time, are prone to calculation errors with GST/VAT and discounts, and lack professional vector formatting.
3. **Fragmented Customer Records:** Client contact info, appointment history, and payment ledgers are scattered across chat apps and physical registers.

BizDesk resolves these challenges with an integrated backend that enforces temporal mathematical non-overlap constraints, dynamic multi-item financial math, and unified relational storage.

---

## Core Features

- **Appointment Scheduler with Collision Prevention**:
  - Enforces temporal interval non-overlap validation:
    $$(A_{start} < B_{end}) \land (A_{end} > B_{start})$$
  - Rejects overlapping appointments with descriptive error responses before database persistence.
- **Client Ledger & CRM Directory**:
  - Centralized customer registry tracking full names, contact info, notes, and cumulative visit history.
- **Multi-Staff & Schedule Coordination**:
  - Associates appointments and services with staff profiles, tracking durations, service tiers, and availability.
- **Automated Invoicing & Vector PDF Generation**:
  - Calculates line item subtotals, configurable GST/VAT tax rates, and fixed/percentage discounts.
  - Generates high-resolution vector PDF invoices on-the-fly using PyMuPDF (`fitz`).
- **Owner KPI Dashboard**:
  - Real-time aggregations for gross billings, total completed visits, active appointments, and pending payments.
- **Pre-Seeded Demo Data**:
  - Built-in idempotent seeding script (`seed_data.py`) providing immediate realistic clinic data for demonstrations and reviewers.

---

## System Architecture

```
bizdesk/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI workflow
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # Modular route controllers
│   │   │   ├── appointments.py  # Appointment booking & collision check
│   │   │   ├── auth.py          # OAuth2 password flow & profile
│   │   │   ├── customers.py     # Customer CRM ledger
│   │   │   ├── dashboard.py     # Owner KPI aggregation
│   │   │   └── invoices.py      # Invoice creation & PDF download
│   │   ├── core/                # Configuration, security, and DB session
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── services/            # Business logic (collision detection, PDF)
│   │   ├── static/              # Lightweight web interface
│   │   └── main.py              # FastAPI application entrypoint
│   ├── tests/
│   │   └── test_bizdesk.py      # Pytest test suite
│   ├── requirements.txt         # Production & testing dependencies
│   └── seed_data.py             # Demo data population script
├── pytest.ini                   # Pytest configuration
├── CHANGES_LOG.md               # Version & change audit trail
└── README.md                    # Enterprise documentation
```

---

## API Endpoints & curl Samples

Base URL: `http://localhost:8000`

| Method | Endpoint | Description | Auth Required |
|:---|:---|:---|:---:|
| `GET` | `/api/health` | Health check and service metadata | No |
| `POST` | `/api/v1/seed` | Seed realistic demo clients and bookings | No |
| `GET` | `/api/v1/customers/` | List all registered clients with visit counts | No |
| `POST` | `/api/v1/customers/` | Register a new client into the CRM | No |
| `GET` | `/api/v1/appointments/` | Retrieve scheduled appointments | No |
| `POST` | `/api/v1/appointments/` | Book an appointment (enforces collision check) | No |
| `GET` | `/api/v1/invoices/` | List all generated invoices | No |
| `GET` | `/api/v1/invoices/{id}/pdf` | Stream or download vector PDF invoice | No |
| `GET` | `/api/v1/dashboard/metrics` | Retrieve business KPI summary | No |
| `POST` | `/api/v1/auth/login` | Authenticate owner / staff user | OAuth2 Form |

### Sample `curl` Commands

#### 1. Health Check
```bash
curl -X GET "http://localhost:8000/api/health"
```
*Response:*
```json
{"status": "healthy", "service": "BizDesk API", "version": "1.0.0"}
```

#### 2. Register a New Customer
```bash
curl -X POST "http://localhost:8000/api/v1/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Aditi Sharma",
    "phone": "+91 98765 43210",
    "email": "aditi.sharma@example.com",
    "notes": "Prefers morning slots"
  }'
```

#### 3. Book an Appointment with Collision Verification
```bash
curl -X POST "http://localhost:8000/api/v1/appointments/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "service_id": 1,
    "appointment_date": "2026-11-20",
    "start_time": "10:00",
    "end_time": "11:00",
    "notes": "Regular consultation"
  }'
```

#### 4. Download Vector PDF Invoice
```bash
curl -X GET "http://localhost:8000/api/v1/invoices/1/pdf" --output invoice_1.pdf
```

#### 5. Fetch Dashboard KPIs
```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/metrics"
```

---

## Local Setup & Run Guide

### Prerequisites
- Python 3.11+
- Git

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/prachizala/bizdesk.git
cd bizdesk
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 3. Initialize Demo Data
```bash
python backend/seed_data.py
```

### 4. Run the Server
From the repository root:
```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
Or from the `backend/` directory:
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- **Interactive API Documentation (Swagger UI):** `http://localhost:8000/docs`
- **Alternative ReDoc UI:** `http://localhost:8000/redoc`
- **Web Interface:** `http://localhost:8000/`

---

## Testing

BizDesk uses `pytest` for unit testing of appointment collision logic, financial math calculations, vector PDF creation, and boundary conditions.

Run the test suite from the repository root:
```bash
pytest backend/tests/test_bizdesk.py -v
```
Or via python module runner:
```bash
python -m pytest backend/tests/test_bizdesk.py -v
```

---

## Continuous Integration

The repository includes a GitHub Actions workflow in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) that automatically runs on every push and pull request to ensure:
- Clean dependency installation
- Full execution and passing of the pytest suite on Python 3.11

---

## Author & License

- **Author:** Prachi Zala ([prachizala](https://github.com/prachizala))
- **Email:** prachizala2003@gmail.com
- **License:** MIT License. See [LICENSE](LICENSE) for details.
