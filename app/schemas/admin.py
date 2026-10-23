from pydantic import BaseModel, ConfigDict, EmailStr


# Naya admin create karne ke liye request
class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str | None = None


# API response mein admin ki safe details
class AdminResponse(BaseModel):
    admin_id: int
    name: str
    email: EmailStr
    phone: str | None = None
    is_active: bool
    created_at: object

    # SQLAlchemy object se response banane ke liye
    model_config = ConfigDict(from_attributes=True)