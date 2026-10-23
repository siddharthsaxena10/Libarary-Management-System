from pydantic import BaseModel, ConfigDict


# Naya department create karne ke liye
class DepartmentCreate(BaseModel):
    department_name: str


# Department ki details response mein bhejne ke liye
class DepartmentResponse(BaseModel):
    department_id: int
    department_name: str

    # SQLAlchemy object ko Pydantic response mein convert karta hai
    model_config = ConfigDict(from_attributes=True)