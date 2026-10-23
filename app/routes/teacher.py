# Database session aur session dependency import karo
from app.db.database import get_db

# FastAPI dependency use karne ke liye
from fastapi import Depends
# APIRouter API routes banane ke liye use hota hai
from fastapi import APIRouter

# SQLAlchemy database session ka type import kar rahe hain
from sqlalchemy.orm import Session

# BaseModel request data ko validate karne ke liye use hota hai
from pydantic import BaseModel

# PostgreSQL ki teachers table ko represent karne wala model
from app.models.teacher import Teacher as TeacherModel


# Teacher ke API routes banane ke liye router object
router = APIRouter()


# Teachers ka sample data (abhi database use nahi kar rahe)
teachers = [
    {
        "teacher_id": 1,
        "name": "Amit Sharma",
        "subject": "Mathematics",
        "experience": 5,
        "email": "amit@example.com"
    },
    {
        "teacher_id": 2,
        "name": "Priya Verma",
        "subject": "Science",
        "experience": 8,
        "email": "priya@example.com"
    },
    {
        "teacher_id": 3,
        "name": "Rahul Singh",
        "subject": "English",
        "experience": 3,
        "email": "rahul@example.com"
    }
]


# Teacher ke data ka structure define kar rahe hain
class Teacher(BaseModel):
    name: str          # Teacher ka naam text mein hoga
    subject: str       # Teacher ka subject text mein hoga
    experience: int    # Experience integer mein hoga
    email: str         # Email filhaal text ke roop mein lenge


# GET API: Saare teachers ki details return karega
# Database session lekar teachers ka data fetch karna
@router.get("/teachers")########################################################################
def get_teachers(db: Session = Depends(get_db)):
    # Database ki teachers table se saare records fetch karo
    teachers_list = db.query(TeacherModel).all()

    # Saare records return karo
    return teachers_list

# GET API: ID ke according ek teacher ki details dega
# GET API: ID ke according database se ek teacher fetch karega
@router.get("/teachers/{teacher_id}")
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    # Step 1: Database mein di hui ID wala teacher search karo
    teacher = db.query(TeacherModel).filter(
        TeacherModel.teacher_id == teacher_id
    ).first()

    # Step 2: Agar teacher nahi mila
    if teacher is None:
        return {"message": "Teacher not found"}

    # Step 3: Teacher milne par uski details return karo
    return {
        "teacher_id": teacher.teacher_id,
        "name": teacher.name,
        "subject": teacher.subject,
        "experience": teacher.experience,
        "email": teacher.email
    }


# POST API: Naya teacher PostgreSQL mein save karega
@router.post("/teachers")
def create_teacher(
    teacher: Teacher,
    db: Session = Depends(get_db)
):
    # Step 1: SQLAlchemy model ka object banao
    new_teacher = TeacherModel(
        name=teacher.name,
        subject=teacher.subject,
        experience=teacher.experience,
        email=teacher.email
    )

    # Step 2: Object ko database session mein add karo
    db.add(new_teacher)

    # Step 3: Data PostgreSQL mein save karo
    db.commit()

    # Step 4: Database se saved teacher ki details refresh karo
    db.refresh(new_teacher)

    # Step 5: Client ko response return karo
    return {
        "message": "Teacher added successfully",
        "teacher": {
            "teacher_id": new_teacher.teacher_id,
            "name": new_teacher.name,
            "subject": new_teacher.subject,
            "experience": new_teacher.experience,
            "email": new_teacher.email
        }
    }

# PUT API: Database mein existing teacher ki details update karega
@router.put("/teachers/{teacher_id}")
def update_teacher(
    teacher_id: int,
    updated_teacher: Teacher,
    db: Session = Depends(get_db)
):
    # Step 1: Database mein teacher ko uski ID se search karo
    teacher = db.query(TeacherModel).filter(
        TeacherModel.teacher_id == teacher_id
    ).first()

    # Step 2: Agar teacher nahi mila
    if teacher is None:
        return {"message": "Teacher not found"}

    # Step 3: Teacher ki details update karo
    teacher.name = updated_teacher.name
    teacher.subject = updated_teacher.subject
    teacher.experience = updated_teacher.experience
    teacher.email = updated_teacher.email

    # Step 4: Changes ko PostgreSQL mein save karo
    db.commit()

    # Step 5: Updated data database se refresh karo
    db.refresh(teacher)

    # Step 6: Updated details return karo
    return {
        "message": "Teacher updated successfully",
        "teacher": {
            "teacher_id": teacher.teacher_id,
            "name": teacher.name,
            "subject": teacher.subject,
            "experience": teacher.experience,
            "email": teacher.email
        }
    }

    # Agar teacher ki ID nahi mili
    return {"message": "Teacher not found"}

###
# DELETE API: Teacher ko database se delete karega
@router.delete("/teachers/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    # Step 1: ID se teacher ko database mein search karo
    teacher = db.query(TeacherModel).filter(
        TeacherModel.teacher_id == teacher_id
    ).first()

    # Step 2: Agar teacher nahi mila
    if teacher is None:
        return {"message": "Teacher not found"}

    # Step 3: Teacher ko delete karo
    db.delete(teacher)

    # Step 4: Database mein changes save karo
    db.commit()

    # Step 5: Success message return karo
    return {"message": "Teacher deleted successfully"}