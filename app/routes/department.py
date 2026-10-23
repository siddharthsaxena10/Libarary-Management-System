from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentResponse


# Department API ka common URL prefix
router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


# 1. Naya department database mein save karna
@router.post("/", response_model=DepartmentResponse)
def create_department(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db)
):
    # Request se department ka object banao
    new_department = Department(
        department_name=department_data.department_name
    )

    db.add(new_department)

    try:
        db.commit()  # Database mein changes save karo
        db.refresh(new_department)  # Generated department_id load karo
    except IntegrityError:
        # Same department name dobara add hone par error handle karo
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Department already exists"
        )

    return new_department


# 2. Saare departments fetch karna
@router.get("/", response_model=list[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()


# 3. ID se ek department fetch karna
@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.department_id == department_id
    ).first()

    # Department nahi mila toh 404 response do
    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department