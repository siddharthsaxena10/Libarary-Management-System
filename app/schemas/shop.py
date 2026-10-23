# Pydantic validation ke liye import
from pydantic import BaseModel, Field


# Shop create karte waqt data validate hoga
class ShopCreate(BaseModel):

    # Shop ka naam: 1 se 100 characters
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    # Shop ka address: 1 se 200 characters
    address: str = Field(
        ...,
        min_length=1,
        max_length=200
    )

    # Phone number ko string rakhenge
    # Kyunki phone number mein starting zero bhi ho sakta hai
    phone: str = Field(
        ...,
        min_length=10,
        max_length=15
    )

    # Price zero se zyada honi chahiye
    price: float = Field(
        ...,
        gt=0
    )