from sqlalchemy import Column, Integer, ForeignKey

from app.db.database import Base


class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id = Column(
        Integer,
        ForeignKey("books.book_id"),
        primary_key=True
    )

    author_id = Column(
        Integer,
        ForeignKey("authors.author_id"),
        primary_key=True
    )