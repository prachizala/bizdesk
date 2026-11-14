from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models.models import BusinessProfile

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    profile = db.query(BusinessProfile).filter(BusinessProfile.email == form_data.username).first()
    if not profile or not verify_password(form_data.password, profile.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid business credentials")
    token = create_access_token({"sub": profile.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "business_name": profile.business_name,
        "business_type": profile.business_type
    }

@router.get("/profile")
def profile(current_user: BusinessProfile = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "business_name": current_user.business_name,
        "business_type": current_user.business_type,
        "email": current_user.email,
        "phone": current_user.phone
    }
