from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.person import Person
from app.models.passport import Passport
from app.schemas.passport import PassportCreate

router = APIRouter(prefix="/passports", tags=["Passports"])


# POST API: Passport create karegi
@router.post("/")
def create_passport(
    passport: PassportCreate,
    db: Session = Depends(get_db)
):
    # Check karo ki Person database mein exist karta hai
    person = db.query(Person).filter(
        Person.id == passport.person_id
    ).first()

    if person is None:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )

    # Check karo ki Person ka passport pehle se toh nahi hai
    existing_passport = db.query(Passport).filter(
        Passport.person_id == passport.person_id
    ).first()

    if existing_passport:
        raise HTTPException(
            status_code=400,
            detail="This person already has a passport"
        )

    # Passport object create karo
    new_passport = Passport(
        passport_number=passport.passport_number,
        person_id=passport.person_id
    )

    # Database mein save karo
    db.add(new_passport)
    db.commit()
    db.refresh(new_passport)

    return {
        "message": "Passport created successfully",
        "id": new_passport.id,
        "passport_number": new_passport.passport_number,
        "person_id": new_passport.person_id
    }


# GET API: Saare passports fetch karegi
@router.get("/")
def get_passports(db: Session = Depends(get_db)):
    return db.query(Passport).all()