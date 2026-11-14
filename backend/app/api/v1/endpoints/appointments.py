from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.models import Appointment, Customer, Service
from app.services.appointment_service import check_time_collision

router = APIRouter()

class AppointmentCreate(BaseModel):
    customer_id: int
    service_id: int
    appointment_date: str
    start_time: str
    end_time: str
    notes: str = ""

@router.get("/")
def list_appointments(db: Session = Depends(get_db)):
    appts = db.query(Appointment).order_by(Appointment.id.desc()).all()
    return [{
        "id": a.id,
        "customer_name": a.customer.full_name if a.customer else "Walk-in",
        "service_name": a.service.name if a.service else "Consultation",
        "price": a.service.price if a.service else 500,
        "date": a.appointment_date,
        "start_time": a.start_time,
        "end_time": a.end_time,
        "status": a.status
    } for a in appts]

@router.post("/")
def book_appointment(req: AppointmentCreate, db: Session = Depends(get_db)):
    # Check collision across active appointments on same date
    existing = db.query(Appointment).filter(
        Appointment.appointment_date == req.appointment_date,
        Appointment.status != "cancelled"
    ).all()

    existing_slots = [(a.start_time, a.end_time) for a in existing]
    if check_time_collision(req.start_time, req.end_time, existing_slots):
        raise HTTPException(
            status_code=409,
            detail=f"Time slot collision: Provider already booked between {req.start_time} and {req.end_time} on {req.appointment_date}."
        )

    appt = Appointment(
        customer_id=req.customer_id,
        service_id=req.service_id,
        appointment_date=req.appointment_date,
        start_time=req.start_time,
        end_time=req.end_time,
        notes=req.notes,
        status="scheduled"
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return {"id": appt.id, "status": "scheduled", "message": "Appointment booked successfully without collisions."}
