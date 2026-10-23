from pydantic import BaseModel, ConfigDict, EmailStr


# Student register karte waqt request body
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    department_id: int


# API response mein student ki details
class StudentResponse(BaseModel):
    student_id: int
    name: str
    email: EmailStr
    phone: str | None = None
    department_id: int

    # SQLAlchemy object ko Pydantic response mein convert karta hai
    model_config = ConfigDict(from_attributes=True)