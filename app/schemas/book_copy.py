from typing import Literal
from pydantic import BaseModel, ConfigDict


# Copy create karte waqt allowed status
CopyStatus = Literal["available", "issued", "damaged", "lost"]


# Nayi physical copy add karne ke liye
class BookCopyCreate(BaseModel):
    book_id: int
    status: CopyStatus = "available"


# API response mein copy ki details
class BookCopyResponse(BaseModel):
    copy_id: int
    book_id: int
    status: CopyStatus

    # SQLAlchemy object ko response mein convert karne ke liye
    model_config = ConfigDict(from_attributes=True)