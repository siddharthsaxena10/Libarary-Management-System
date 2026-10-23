# SQLAlchemy column types import karo
from sqlalchemy import Column, Integer, String, Numeric

# Database ka Base import karo
from app.db.database import Base


# Shop model
class Shop(Base):

    # PostgreSQL table ka naam
    __tablename__ = "shops"

    # Unique ID for each shop
    shop_id = Column(Integer, primary_key=True, index=True)

    # Shop ka naam
    name = Column(String(100), nullable=False)

    # Shop ka address
    address = Column(String(200), nullable=False)

    # Shop ka contact number
    phone = Column(String(15), nullable=False)

    # Shop ki total sales ya amount nahi, yahan example ke liye price field hai
    price = Column(Numeric(10, 2), nullable=False)