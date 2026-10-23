from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Department(Base):
    __tablename__ = "departments"

    # Har department ki unique ID
    department_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Department ka naam unique hona chahiye
    department_name = Column(
        String(100),
        unique=True,
        nullable=False
    )