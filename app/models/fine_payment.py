from sqlalchemy import Column, Integer, Numeric, Date, String, ForeignKey
from app.db.database import Base


class FinePayment(Base):
    __tablename__ = "fine_payments"

    # Primary key
    payment_id = Column(Integer, primary_key=True, index=True)

    # Kis book issue ka fine pay hua
    issue_id = Column(
        Integer,
        ForeignKey("book_issues.issue_id"),
        nullable=False,
        index=True
    )

    # Payment amount
    amount = Column(Numeric(10, 2), nullable=False)

    # Payment ki date
    payment_date = Column(Date, nullable=False)

    # Payment status
    payment_status = Column(String(20), nullable=False, default="paid")