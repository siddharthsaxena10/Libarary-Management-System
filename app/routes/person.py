from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.person import Person
from app.schemas.person import PersonCreate

router = APIRouter(prefix="/persons", tags=["Persons"])


# POST API: Naya person create karegi
@router.post("/")
def create_person(
    person: PersonCreate,
    db: Session = Depends(get_db)
):
    # Request data se Person object banao
    new_person = Person(name=person.name)

    # Database session mein add karo
    db.add(new_person)

    # Database mein save karo
    db.commit()

    # Database-generated ID object mein lao
    db.refresh(new_person)

    return {
        "message": "Person created successfully",
        "id": new_person.id,
        "name": new_person.name
    }


# GET API: Saare persons fetch karegi
@router.get("/")
def get_persons(db: Session = Depends(get_db)):
    persons = db.query(Person).all()

    return persons


# GET API: Particular person fetch karegi
@router.get("/{person_id}")
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(
        Person.id == person_id
    ).first()

    if person is None:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )

    return person