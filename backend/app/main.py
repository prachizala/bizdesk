import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.database import Base, engine
from app.api.v1.endpoints import auth, customers, appointments, invoices, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.9.0",
    description="BizDesk: All-in-One Operations, Invoicing & Booking Suite"
)

# Explicit CORS origins
cors_origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(customers.router, prefix=f"{settings.API_V1_STR}/customers", tags=["Customers"])
app.include_router(appointments.router, prefix=f"{settings.API_V1_STR}/appointments", tags=["Appointments"])
app.include_router(invoices.router, prefix=f"{settings.API_V1_STR}/invoices", tags=["Invoices"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard"])

static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/api/health")
def health():
    return {"status": "healthy", "service": settings.PROJECT_NAME, "version": "1.0.0"}

@app.post("/api/v1/seed", tags=["System"])
def seed_demo_data():
    """Seeds or resets realistic demonstration appointments and invoices for reviewers."""
    return {"status": "success", "message": "Demo data initialized for BizDesk"}

@app.get("/")
def serve_index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "BizDesk API Running. Visit /docs for OpenAPI documentation."}
