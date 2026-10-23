from pydantic import BaseModel, ConfigDict


# Naya author create karne ke liye
class AuthorCreate(BaseModel):
    author_name: str


# API response ke liye
class AuthorResponse(BaseModel):
    author_id: int
    author_name: str

    # SQLAlchemy model se data read karne ki permission
    model_config = ConfigDict(from_attributes=True)