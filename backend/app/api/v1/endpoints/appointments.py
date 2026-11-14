from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from app.core.database import get_db
from app.models.models import Appointment, Customer, Service
from app.services.appointment_service import check_time_collision, time_to_minutes

router = APIRouter()

class AppointmentCreate(BaseModel):
    customer_id: int
    service_id: int
    appointment_date: str
    start_time: str
    end_time: str
    notes: str = ""

    @field_validator("end_time")
    @classmethod
    def validate_times(cls, end_val, info):
        start_val = info.data.get("start_time")
        if start_val:
            try:
                s_min = time_to_minutes(start_val)
                e_min = time_to_minutes(end_val)
                if s_min >= e_min:
                    raise ValueError("End time must be strictly after start time.")
            except Exception as e:
                raise ValueError(f"Invalid time format: {str(e)}")
        return end_val

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
    # Verify customer and service exist
    customer = db.query(Customer).filter(Customer.id == req.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer ID {req.customer_id} not found")

    service = db.query(Service).filter(Service.id == req.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail=f"Service ID {req.service_id} not found")

    # Check collision across active appointments on same date
    existing = db.query(Appointment).filter(
        Appointment.appointment_date == req.appointment_date,
        Appointment.status != "cancelled"
    ).all()

    existing_slots = [(a.start_time, a.end_time) for a in existing]
    try:
        collision = check_time_collision(req.start_time, req.end_time, existing_slots)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    if collision:
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
