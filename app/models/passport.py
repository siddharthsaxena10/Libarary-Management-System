from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Passport(Base):
    __tablename__ = "passports"

    id = Column(Integer, primary_key=True, index=True)

    passport_number = Column(
        String(20),
        unique=True,
        nullable=False
    )

    # Person ki ID ko foreign key ke through connect kiya
    # unique=True ensure karta hai ki ek person ke saath
    # maximum ek passport record linked ho
    person_id = Column(
        Integer,
        ForeignKey("persons.id"),
        unique=True,
        nullable=False
    )

    # Passport se bhi Person ka data access kar sakte hain
    person = relationship(
        "Person",
        back_populates="passport"
    )