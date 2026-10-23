# SQLAlchemy ke column types import kar rahe hain
from sqlalchemy import Column, Integer, String, Numeric

# Database ka Base import kar rahe hain
from app.db.database import Base


# Details model database mein details table represent karega
class Details(Base):
    __tablename__ = "details"

    # Har record ki unique ID
    id = Column(Integer, primary_key=True, index=True)

    # Brand ka naam
    brand_name = Column(String(100), nullable=False)

    # Brand ki price (Numeric financial values ke liye use hota hai)
    price = Column(Numeric(10, 2), nullable=False)