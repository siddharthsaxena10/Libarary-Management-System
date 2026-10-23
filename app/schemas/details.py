# Pydantic validation ke liye BaseModel import kar rahe hain
from pydantic import BaseModel, Field


# Brand details create karte waqt data validate hoga
class DetailsCreate(BaseModel):

    # Brand ka naam: empty nahi hona chahiye
    brand_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Brand name"
    )

    # Price: zero ya negative nahi honi chahiye
    price: float = Field(
        ...,
        gt=0,
        description="Brand price must be greater than zero"
    )