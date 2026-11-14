from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.models import Customer

router = APIRouter()

class CustomerCreate(BaseModel):
    full_name: str
    phone: str
    email: str = ""
    notes: str = ""

@router.get("/")
def list_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).order_by(Customer.id.desc()).all()
    return [{
        "id": c.id,
        "full_name": c.full_name,
        "phone": c.phone,
        "email": c.email,
        "visit_count": len(c.appointments)
    } for c in customers]

@router.post("/")
def create_customer(req: CustomerCreate, db: Session = Depends(get_db)):
    c = Customer(full_name=req.full_name, phone=req.phone, email=req.email, notes=req.notes)
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "full_name": c.full_name, "phone": c.phone}
