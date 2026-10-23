from pydantic import BaseModel, Field


# Passport create karne ke liye required data
class PassportCreate(BaseModel):
    passport_number: str = Field(..., min_length=1, max_length=20)
    person_id: int = Field(..., gt=0)