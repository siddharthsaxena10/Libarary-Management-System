# SQLAlchemy ke column types import kar rahe hain
from sqlalchemy import Column, Integer, String

# Database ka Base import kar rahe hain
from app.db.database import Base


# Employee class database ki employees table ko represent karegi
class Employee(Base):

    # PostgreSQL mein table ka naam employees hoga
    __tablename__ = "employees"

    # Employee ki unique ID; database ise automatically generate karega
    employee_id = Column(Integer, primary_key=True, index=True)

    # Employee ka naam; maximum 100 characters
    name = Column(String(100), nullable=False)

    # Employee ka department; maximum 100 characters
    department = Column(String(100), nullable=False)

    # Employee ki salary integer mein store hogi
    salary = Column(Integer, nullable=False)

    # Employee ka email; maximum 150 characters
    email = Column(String(150), nullable=False)