import os
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.core.database import get_db
from app.models.models import Invoice, InvoiceItem, Customer, BusinessProfile
from app.services.invoice_service import calculate_invoice_totals, generate_invoice_pdf

router = APIRouter()

class InvoiceItemSchema(BaseModel):
    description: str
    quantity: int = 1
    unit_price: float

class InvoiceCreate(BaseModel):
    customer_id: int
    issue_date: str
    due_date: str
    items: List[InvoiceItemSchema]
    discount: float = 0.0

@router.get("/")
def list_invoices(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).order_by(Invoice.id.desc()).all()
    return [{
        "id": inv.id,
        "invoice_number": inv.invoice_number,
        "customer_name": inv.customer.full_name if inv.customer else "Unknown",
        "date": inv.issue_date,
        "total": inv.total_amount,
        "status": inv.payment_status
    } for inv in invoices]

@router.get("/{id}/pdf")
def download_invoice_pdf(id: int, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter(Invoice.id == id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")

    items_list = [{
        "description": it.description,
        "quantity": it.quantity,
        "unit_price": it.unit_price,
        "line_total": it.line_total
    } for it in inv.items]

    totals = {
        "subtotal": inv.subtotal,
        "tax_rate_pct": inv.tax_rate_pct,
        "tax_amount": inv.tax_amount,
        "discount_amount": inv.discount_amount,
        "total_amount": inv.total_amount
    }

    pdf_path = f"./invoices/invoice_{inv.invoice_number}.pdf"
    generate_invoice_pdf(
        invoice_number=inv.invoice_number,
        business_name="Apex Healthcare & Wellness Clinic",
        customer_name=inv.customer.full_name if inv.customer else "Client",
        customer_phone=inv.customer.phone if inv.customer else "N/A",
        issue_date=inv.issue_date,
        items=items_list,
        totals=totals,
        output_path=pdf_path
    )

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=invoice_{inv.invoice_number}.pdf"}
    )
