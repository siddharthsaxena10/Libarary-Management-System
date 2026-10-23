from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# Payment create karne ke liye
class FinePaymentCreate(BaseModel):
    issue_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


# API response ke liye
class FinePaymentResponse(BaseModel):
    payment_id: int
    issue_id: int
    amount: Decimal
    payment_date: date
    payment_status: str

    model_config = ConfigDict(from_attributes=True)