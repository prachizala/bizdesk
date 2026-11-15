import pytest
from app.services.appointment_service import check_time_collision
from app.services.invoice_service import calculate_invoice_totals, generate_invoice_pdf
import os

def test_booking_collision_prevention():
    # Existing slot: 10:00 to 11:00
    existing = [("10:00", "11:00")]

    # Direct collision: 10:15 to 10:45
    assert check_time_collision("10:15", "10:45", existing) is True

    # Partial overlap start: 09:30 to 10:30
    assert check_time_collision("09:30", "10:30", existing) is True

    # Free adjacent slot: 11:00 to 12:00
    assert check_time_collision("11:00", "12:00", existing) is False

    # Free early slot: 09:00 to 10:00
    assert check_time_collision("09:00", "10:00", existing) is False

def test_invoice_financial_math():
    items = [
        {"description": "Dental Cleaning", "quantity": 1, "unit_price": 1000.0},
        {"description": "X-Ray Scan", "quantity": 2, "unit_price": 500.0}
    ]
    totals = calculate_invoice_totals(items, tax_rate_pct=18.0, discount_amount=200.0)

    assert totals["subtotal"] == 2000.0
    assert totals["discount_amount"] == 200.0
    # Tax on 1800 at 18% = 324.0
    assert totals["tax_amount"] == 324.0
    assert totals["total_amount"] == 2124.0

def test_pdf_invoice_generation():
    items = [{"description": "Medical Consultation", "quantity": 1, "unit_price": 800.0, "line_total": 800.0}]
    totals = {"subtotal": 800.0, "tax_rate_pct": 18.0, "tax_amount": 144.0, "discount_amount": 0.0, "total_amount": 944.0}
    out_file = "./invoices/test_generated_invoice.pdf"

    res = generate_invoice_pdf(
        invoice_number="TEST-001",
        business_name="Apex Healthcare Clinic",
        customer_name="Test Patient",
        customer_phone="+91 90000 00000",
        issue_date="2026-11-14",
        items=items,
        totals=totals,
        output_path=out_file
    )
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 1000
    os.remove(out_file)


def test_invalid_time_sequence():
    from app.services.appointment_service import check_time_collision
    with pytest.raises(ValueError) as exc:
        # Start time after end time must raise ValueError
        check_time_collision("14:00", "13:00", [("10:00", "11:00")])
    assert "strictly before" in str(exc.value)


def test_p2_empty_state_and_invalid_appointment_payload():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)

    # Missing fields should return 422 Unprocessable Entity
    res = client.post("/api/v1/appointments", json={})
    assert res.status_code == 422

    # Invoices list endpoint returns 200 array
    inv_res = client.get("/api/v1/invoices")
    assert inv_res.status_code == 200
    assert isinstance(inv_res.json(), list)
