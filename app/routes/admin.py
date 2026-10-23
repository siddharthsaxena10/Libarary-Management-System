from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash

from app.db.database import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminResponse


router = APIRouter(
    prefix="/admins",
    tags=["Admins"]
)

# Password ko hash aur verify karne ke liye
password_hasher = PasswordHash.recommended()


# 1. Naya admin create karna
@router.post("/", response_model=AdminResponse, status_code=201)
def create_admin(
    admin_data: AdminCreate,
    db: Session = Depends(get_db)
):
    # Password ko database mein save karne se pehle hash karo
    hashed_password = password_hasher.hash(admin_data.password)

    new_admin = Admin(
        name=admin_data.name,
        email=admin_data.email,
        password_hash=hashed_password,
        phone=admin_data.phone,
        is_active=True
    )

    db.add(new_admin)

    try:
        db.commit()  # Admin ko database mein save karo
        db.refresh(new_admin)  # Generated ID aur timestamp load karo
    except IntegrityError:
        # Duplicate email jaise database constraint error handle karo
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Admin with this email already exists"
        )

    return new_admin


# 2. Saare admins ki details fetch karna
@router.get("/", response_model=list[AdminResponse])
def get_admins(db: Session = Depends(get_db)):
    return db.query(Admin).all()