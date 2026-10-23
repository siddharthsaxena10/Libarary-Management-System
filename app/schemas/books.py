from pydantic import BaseModel, ConfigDict


# POST API se nayi book add karne ke liye
class BookCreate(BaseModel):
    book_name: str
    isbn: str
    publisher: str | None = None  # Publisher optional hai


# API response mein book ki details bhejne ke liye
class BookResponse(BaseModel):
    book_id: int
    book_name: str
    isbn: str
    publisher: str | None = None

    # SQLAlchemy model ke object ko response mein convert karne ke liye
    model_config = ConfigDict(from_attributes=True)