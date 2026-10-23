from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db

# SQLAlchemy models
from app.models.student import Student
from app.models.department import Department
from app.models.book_issue import BookIssue

# Pydantic schemas
from app.schemas.student import StudentCreate, StudentResponse
from app.schemas.book_issue import BookIssueResponse


# Student APIs ka common prefix
router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# 1. Naya student register karna
@router.post("/", response_model=StudentResponse)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    # Check karo department exist karta hai ya nahi
    department = db.query(Department).filter(
        Department.department_id == student_data.department_id
    ).first()

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    # Naya student object banao
    new_student = Student(
        name=student_data.name,
        email=student_data.email,
        phone=student_data.phone,
        department_id=student_data.department_id
    )

    db.add(new_student)

    try:
        # Database mein save karo
        db.commit()
        db.refresh(new_student)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Student with this email may already exist"
        )

    return new_student


# 2. Saare students fetch karna
@router.get("/", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db)
):
    return db.query(Student).all()


# 3. ID se ek student fetch karna
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.student_id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# 4. Student ki book issue history fetch karna
@router.get(
    "/{student_id}/book-history",
    response_model=list[BookIssueResponse]
)
def get_student_book_history(
    student_id: int,
    db: Session = Depends(get_db)
):
    # Check karo student exist karta hai ya nahi
    student = db.query(Student).filter(
        Student.student_id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Student ki saari issued books ki history nikalo
    book_history = db.query(BookIssue).filter(
        BookIssue.student_id == student_id
    ).all()

    return book_history