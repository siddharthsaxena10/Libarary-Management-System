from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String(200), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    publisher = Column(String(150), nullable=True)