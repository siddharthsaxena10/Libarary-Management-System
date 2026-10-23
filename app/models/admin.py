from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.database import Base


class Admin(Base):
    __tablename__ = "admins"

    # Har admin ki unique ID
    admin_id = Column(Integer, primary_key=True, index=True)

    # Admin ka naam
    name = Column(String(100), nullable=False)

    # Har admin ka email unique hona chahiye
    email = Column(String(150), unique=True, nullable=False)

    # Password ka hashed version hi store hoga
    password_hash = Column(String(255), nullable=False)

    # Phone number optional hai
    phone = Column(String(15), nullable=True)

    # Admin account banne ka time database set karega
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Admin account active hai ya nahi
    is_active = Column(Boolean, nullable=False, default=True)