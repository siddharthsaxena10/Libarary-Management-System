from pydantic import BaseModel, Field


# POST request mein aane wale data ko validate karega
class PersonCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)