from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


class Student(Base):
    __tablename__ = "students"

    # Har student ki unique ID
    student_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Student ka naam
    name = Column(String(100), nullable=False)

    # Har student ka email unique hona chahiye
    email = Column(String(150), unique=True, nullable=False)

    # Phone number optional hai
    phone = Column(String(15), nullable=True)

    # Foreign key: student ko department se connect karti hai
    department_id = Column(
        Integer,
        ForeignKey("departments.department_id"),
        nullable=False
    )