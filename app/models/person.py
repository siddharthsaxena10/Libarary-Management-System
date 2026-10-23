from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

# Person table
class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    # Person ka ek passport ho sakta hai
    passport = relationship(
        "Passport",
        back_populates="person",
        uselist=False
    )