from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


class BookCopy(Base):
    __tablename__ = "book_copies"

    # Har physical copy ki unique ID
    copy_id = Column(Integer, primary_key=True, index=True)

    # Ye copy kis book ki hai
    book_id = Column(
        Integer,
        ForeignKey("books.book_id"),
        nullable=False
    )

    # Copy ki current condition/status
    status = Column(
        String(20),
        nullable=False,
        default="available"
    )