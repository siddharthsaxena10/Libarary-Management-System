from sqlalchemy import Column, Integer, Date, ForeignKey

from app.db.database import Base


class BookIssue(Base):
    __tablename__ = "book_issues"

    issue_id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.student_id"),
        nullable=False
    )

    copy_id = Column(
        Integer,
        ForeignKey("book_copies.copy_id"),
        nullable=False
    )

    admin_id = Column(
        Integer,
        ForeignKey("admins.admin_id"),
        nullable=False
    )

    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)