from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Customer, Appointment, Invoice, Service

router = APIRouter()

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).all()
    total_rev = sum(i.total_amount for i in invoices if i.payment_status == "paid")
    appts = db.query(Appointment).all()
    completed = len([a for a in appts if a.status == "completed"])
    customers = db.query(Customer).count()

    return {
        "total_revenue": round(total_rev, 2),
        "total_appointments": len(appts),
        "completed_appointments": completed,
        "total_customers": customers,
        "currency": "INR",
        "reminders": [
            {"id": 1, "title": "Follow up with Rahul Verma (Post-op check)", "due": "Today 4:00 PM"},
            {"id": 2, "title": "Send unpaid invoice reminder to Priya Shah", "due": "Today 5:30 PM"}
        ]
    }
