from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Author(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String(150), nullable=False)