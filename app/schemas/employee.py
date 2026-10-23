# Pydantic ka BaseModel data validation ke liye use hota hai
from pydantic import BaseModel, EmailStr


# Employee API se aane wale data ka structure
class EmployeeCreate(BaseModel):

    # Employee ka naam
    name: str

    # Employee ka department
    department: str

    # Employee ki salary
    salary: int

    # Employee ka valid email
    email: EmailStr