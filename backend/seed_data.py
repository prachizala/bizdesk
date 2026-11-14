from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.models import BusinessProfile, Customer, Service, Appointment, Invoice, InvoiceItem

Base.metadata.create_all(bind=engine)
db = SessionLocal()

print("Seeding BizDesk database...")

prof = db.query(BusinessProfile).filter(BusinessProfile.email == "owner@bizdesk.app").first()
if not prof:
    prof = BusinessProfile(
        business_name="Apex Healthcare & Physiotherapy Clinic",
        business_type="clinic",
        email="owner@bizdesk.app",
        hashed_password=hash_password("bizdesk123"),
        phone="+91 98765 43210",
        address="Suite 402, Medical Enclave, Ahmedabad",
        tax_id="GSTIN24AAACG1234D1Z5"
    )
    db.add(prof)
    db.commit()

# Services
s1 = db.query(Service).filter(Service.name == "Physiotherapy Consultation").first()
if not s1:
    s1 = Service(name="Physiotherapy Consultation", price=800.0, duration_minutes=45)
    s2 = Service(name="Postural Rehabilitation Session", price=1200.0, duration_minutes=60)
    s3 = Service(name="Sports Injury Assessment", price=1500.0, duration_minutes=45)
    db.add_all([s1, s2, s3])
    db.commit()

# Customers
c1 = db.query(Customer).filter(Customer.full_name == "Rahul Verma").first()
if not c1:
    c1 = Customer(full_name="Rahul Verma", phone="+91 98250 11223", email="rahul@gmail.com")
    c2 = Customer(full_name="Priya Shah", phone="+91 98790 33445", email="priya@gmail.com")
    c3 = Customer(full_name="Amit Trivedi", phone="+91 99090 55667", email="amit@gmail.com")
    db.add_all([c1, c2, c3])
    db.commit()

    # Appointments
    a1 = Appointment(customer_id=c1.id, service_id=s1.id, appointment_date="2026-11-14", start_time="10:00", end_time="10:45", status="completed")
    a2 = Appointment(customer_id=c2.id, service_id=s2.id, appointment_date="2026-11-14", start_time="11:30", end_time="12:30", status="scheduled")
    a3 = Appointment(customer_id=c3.id, service_id=s3.id, appointment_date="2026-11-15", start_time="14:00", end_time="14:45", status="scheduled")
    db.add_all([a1, a2, a3])
    db.commit()

    # Invoice
    inv = Invoice(
        invoice_number="INV-2026-001",
        customer_id=c1.id,
        issue_date="2026-11-14",
        due_date="2026-11-21",
        subtotal=800.0,
        tax_rate_pct=18.0,
        tax_amount=144.0,
        discount_amount=0.0,
        total_amount=944.0,
        payment_status="paid"
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)

    item = InvoiceItem(invoice_id=inv.id, description="Physiotherapy Consultation (Initial)", quantity=1, unit_price=800.0, line_total=800.0)
    db.add(item)
    db.commit()

print("BizDesk seeded successfully!")
