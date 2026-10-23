from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.models.book_copy import BookCopy
from app.models.books import Book
from app.schemas.book_copy import BookCopyCreate, BookCopyResponse


router = APIRouter(
    prefix="/book-copies",
    tags=["Book Copies"]
)


# 1. Nayi physical copy add karna
@router.post("/", response_model=BookCopyResponse, status_code=201)
def create_book_copy(
    copy_data: BookCopyCreate,
    db: Session = Depends(get_db)
):
    # Check karo ki ye book database mein exist karti hai
    book = db.query(Book).filter(
        Book.book_id == copy_data.book_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # Nayi copy ka object banao
    new_copy = BookCopy(
        book_id=copy_data.book_id,
        status=copy_data.status
    )

    db.add(new_copy)

    try:
        db.commit()  # Copy ko database mein save karo
        db.refresh(new_copy)  # Generated copy_id load karo
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not create book copy"
        )

    return new_copy


# 2. Saari physical copies fetch karna
@router.get("/", response_model=list[BookCopyResponse])
def get_book_copies(db: Session = Depends(get_db)):
    return db.query(BookCopy).all()


# 3. Copy ID se ek specific copy fetch karna
@router.get("/{copy_id}", response_model=BookCopyResponse)
def get_book_copy(
    copy_id: int,
    db: Session = Depends(get_db)
):
    copy = db.query(BookCopy).filter(
        BookCopy.copy_id == copy_id
    ).first()

    if copy is None:
        raise HTTPException(
            status_code=404,
            detail="Book copy not found"
        )

    return copy