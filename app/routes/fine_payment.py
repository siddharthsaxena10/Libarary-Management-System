from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.book_issue import BookIssue
from app.models.fine_payment import FinePayment
from app.schemas.fine_payment import (
    FinePaymentCreate,
    FinePaymentResponse
)


router = APIRouter(
    prefix="/fine-payments",
    tags=["Fine Payments"]
)

# Daily fine rate
FINE_PER_DAY = 5


# Helper: Book issue ka total fine calculate karna
def calculate_total_fine(issue: BookIssue) -> Decimal:
    # Return ho chuki hai toh return date use karo,
    # otherwise aaj ki date use karo
    calculation_date = issue.return_date or date.today()

    late_days = max(
        0,
        (calculation_date - issue.due_date).days
    )

    return Decimal(late_days * FINE_PER_DAY)


# 1. Fine payment record karna
@router.post(
    "/",
    response_model=FinePaymentResponse,
    status_code=201
)
def create_fine_payment(
    payment_data: FinePaymentCreate,
    db: Session = Depends(get_db)
):
    # Book issue record find karo
    issue = db.query(BookIssue).filter(
        BookIssue.issue_id == payment_data.issue_id
    ).first()

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Book issue record not found"
        )

    # Total fine calculate karo
    total_fine = calculate_total_fine(issue)

    # Pehle ki successful payments ka total nikalo
    previous_payments = db.query(FinePayment).filter(
        FinePayment.issue_id == issue.issue_id,
        FinePayment.payment_status == "paid"
    ).all()

    paid_amount = sum(
        (payment.amount for payment in previous_payments),
        Decimal("0.00")
    )

    # Kitna fine abhi pay karna baaki hai
    outstanding_fine = total_fine - paid_amount

    if outstanding_fine <= 0:
        raise HTTPException(
            status_code=400,
            detail="No outstanding fine for this book issue"
        )

    # Client amount ko server-calculated fine se validate karo
    if payment_data.amount != outstanding_fine:
        raise HTTPException(
            status_code=400,
            detail=f"Outstanding fine is {outstanding_fine}"
        )

    # Payment record banao
    new_payment = FinePayment(
        issue_id=issue.issue_id,
        amount=payment_data.amount,
        payment_date=date.today(),
        payment_status="paid"
    )

    try:
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save fine payment"
        )

    return new_payment


# 2. Saari fine payments dekhna
@router.get("/", response_model=list[FinePaymentResponse])
def get_fine_payments(
    db: Session = Depends(get_db)
):
    return db.query(FinePayment).all()


# 3. Payment ID se details dekhna
@router.get(
    "/{payment_id}",
    response_model=FinePaymentResponse
)
def get_fine_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = db.query(FinePayment).filter(
        FinePayment.payment_id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Fine payment not found"
        )

    return payment


# 4. Kisi book issue ki payment history
@router.get(
    "/issue/{issue_id}",
    response_model=list[FinePaymentResponse]
)
def get_issue_payment_history(
    issue_id: int,
    db: Session = Depends(get_db)
):
    # Check karo issue exist karta hai
    issue = db.query(BookIssue).filter(
        BookIssue.issue_id == issue_id
    ).first()

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Book issue record not found"
        )

    return db.query(FinePayment).filter(
        FinePayment.issue_id == issue_id
    ).all()