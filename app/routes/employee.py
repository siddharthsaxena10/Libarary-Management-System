# FastAPI mein routes banane ke liye
from fastapi import APIRouter, Depends

# Database session ka type
from sqlalchemy.orm import Session

# Database session provide karne wala function
from app.db.database import get_db

# Employee ka SQLAlchemy model
from app.models.employee import Employee as EmployeeModel

# Employee request data ka Pydantic schema
from app.schemas.employee import EmployeeCreate


# Employee ke API routes banane ke liye router
router = APIRouter()


# POST API: Naya employee database mein save karegi##############################
@router.post("/employees")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    # Step 1: Request data se Employee model ka object banao
    new_employee = EmployeeModel(
        name=employee.name,
        department=employee.department,
        salary=employee.salary,
        email=employee.email
    )

    # Step 2: Object ko database session mein add karo
    db.add(new_employee)

    # Step 3: Data PostgreSQL mein save karo
    db.commit()

    # Step 4: Database se generated employee_id fetch karo
    db.refresh(new_employee)

    # Step 5: Client ko response return karo
    return {
        "message": "Employee added successfully",
        "employee": {
            "employee_id": new_employee.employee_id,
            "name": new_employee.name,
            "department": new_employee.department,
            "salary": new_employee.salary,
            "email": new_employee.email
        }
    }
# GET API: Database se saare employees fetch karegi##########################################
@router.get("/employees")
def get_employees(db: Session = Depends(get_db)):

    # Step 1: Database ki employees table se saare records fetch karo
    employees = db.query(EmployeeModel).all()

    # Step 2: Saare employees ka data return karo
    return employees

# GET API: ID ke according ek employee ki details fetch karegi
@router.get("/employees/{employee_id}")###############################################
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    # Step 1: Database mein employee ko ID se search karo
    employee = db.query(EmployeeModel).filter(
        EmployeeModel.employee_id == employee_id
    ).first()

    # Step 2: Agar employee nahi mila
    if employee is None:
        return {"message": "Employee not found"}

    # Step 3: Employee ki details return karo
    return {
        "employee_id": employee.employee_id,
        "name": employee.name,
        "department": employee.department,
        "salary": employee.salary,
        "email": employee.email
    }