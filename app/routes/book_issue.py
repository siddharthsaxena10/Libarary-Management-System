from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

# SQLAlchemy models
from app.models.book_issue import BookIssue
from app.models.book_copy import BookCopy
from app.models.student import Student
from app.models.admin import Admin

# Pydantic schema
from app.schemas.book_issue import BookIssueCreate, BookIssueResponse


# Router configuration
router = APIRouter(
    prefix="/book-issues",
    tags=["Book Issues"]
)


# Fine per late day
FINE_PER_DAY = 5


# 1. Student ko book issue karna
@router.post("/", response_model=BookIssueResponse, status_code=201)
def issue_book(
    issue_data: BookIssueCreate,
    db: Session = Depends(get_db)
):
    # Check karo ki student exist karta hai
    student = db.query(Student).filter(
        Student.student_id == issue_data.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check karo ki admin exist karta hai
    admin = db.query(Admin).filter(
        Admin.admin_id == issue_data.admin_id
    ).first()

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    # Check karo ki book copy exist karti hai
    book_copy = db.query(BookCopy).filter(
        BookCopy.copy_id == issue_data.copy_id
    ).first()

    if not book_copy:
        raise HTTPException(
            status_code=404,
            detail="Book copy not found"
        )

    # Sirf available copy issue ho sakti hai
    if book_copy.status != "available":
        raise HTTPException(
            status_code=400,
            detail="Book copy is not available"
        )

    # Due date issue date se pehle nahi honi chahiye
    if issue_data.due_date < issue_data.issue_date:
        raise HTTPException(
            status_code=400,
            detail="Due date cannot be before issue date"
        )

    # Naya issue record banao
    new_issue = BookIssue(
        student_id=issue_data.student_id,
        copy_id=issue_data.copy_id,
        admin_id=issue_data.admin_id,
        issue_date=issue_data.issue_date,
        due_date=issue_data.due_date,
        return_date=None
    )

    # Book copy ka status issued karo
    book_copy.status = "issued"

    try:
        db.add(new_issue)
        db.commit()
        db.refresh(new_issue)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not issue book"
        )

    return new_issue


# 2. Saare book issue records dekhna
@router.get("/", response_model=list[BookIssueResponse])
def get_book_issues(
    db: Session = Depends(get_db)
):
    return db.query(BookIssue).all()


# 3. Ek specific issue record dekhna
@router.get("/{issue_id}", response_model=BookIssueResponse)
def get_book_issue(
    issue_id: int,
    db: Session = Depends(get_db)
):
    issue = db.query(BookIssue).filter(
        BookIssue.issue_id == issue_id
    ).first()

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Book issue record not found"
        )

    return issue


# 4. Book return karna
@router.put("/{issue_id}/return", response_model=BookIssueResponse)
def return_book(
    issue_id: int,
    db: Session = Depends(get_db)
):
    # Issue record find karo
    issue = db.query(BookIssue).filter(
        BookIssue.issue_id == issue_id
    ).first()

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Book issue record not found"
        )

    # Check karo book pehle hi return toh nahi hui
    if issue.return_date is not None:
        raise HTTPException(
            status_code=400,
            detail="Book has already been returned"
        )

    # Related book copy find karo
    book_copy = db.query(BookCopy).filter(
        BookCopy.copy_id == issue.copy_id
    ).first()

    if not book_copy:
        raise HTTPException(
            status_code=404,
            detail="Book copy not found"
        )

    # Book ki return date save karo
    issue.return_date = date.today()

    # Book copy dobara available karo
    book_copy.status = "available"

    try:
        db.commit()
        db.refresh(issue)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not return book"
        )

    return issue


# 5. Book ka fine calculate karna
@router.get("/{issue_id}/fine")
def calculate_fine(
    issue_id: int,
    db: Session = Depends(get_db)
):
    # Step 1: Issue ID se record find karo
    issue = db.query(BookIssue).filter(
        BookIssue.issue_id == issue_id
    ).first()

    # Step 2: Record nahi mila toh error do
    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Book issue record not found"
        )

    # Step 3: Return date available hai toh use karo,
    # warna aaj ki date use karo
    calculation_date = issue.return_date or date.today()

    # Step 4: Late days calculate karo
    late_days = (calculation_date - issue.due_date).days

    # Step 5: Fine ke late days negative nahi hone chahiye
    late_days = max(0, late_days)

    # Step 6: Total fine calculate karo
    total_fine = late_days * FINE_PER_DAY

    # Step 7: Fine details return karo
    return {
        "issue_id": issue.issue_id,
        "student_id": issue.student_id,
        "due_date": issue.due_date,
        "return_date": issue.return_date,
        "late_days": late_days,
        "fine_per_day": FINE_PER_DAY,
        "total_fine": total_fine
    }