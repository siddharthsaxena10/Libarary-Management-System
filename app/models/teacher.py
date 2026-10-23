# SQLAlchemy column types aur constraints import kar rahe hain
from sqlalchemy import Column, Integer, String

# Database ka Base import kar rahe hain
from app.db.database import Base


# Teacher class PostgreSQL mein teachers table represent karegi
class Teacher(Base):

    # Database table ka naam
    __tablename__ = "teachers"

    # Teacher ki unique ID; primary key aur automatically increment hogi
    teacher_id = Column(Integer, primary_key=True, index=True)

    # Teacher ka naam; maximum 100 characters
    name = Column(String(100), nullable=False)

    # Teacher ka subject; maximum 100 characters
    subject = Column(String(100), nullable=False)

    # Teacher ka experience years mein
    experience = Column(Integer, nullable=False)

    # Teacher ka email; maximum 150 characters
    email = Column(String(150), nullable=False)