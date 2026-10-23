from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.books import Book
from app.schemas.books import BookCreate, BookResponse


# Saare book-related endpoints ka common prefix
router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# 1. Database mein nayi book add karna
@router.post("/", response_model=BookResponse)
def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db)
):
    # Request ke data se SQLAlchemy object banana
    new_book = Book(
        book_name=book_data.book_name,
        isbn=book_data.isbn,
        publisher=book_data.publisher
    )

    db.add(new_book)       # Insert ke liye object session mein add karo
    db.commit()            # Changes database mein save karo
    db.refresh(new_book)   # Database se generated values, jaise ID, load karo

    return new_book


# 2. Database se saari books fetch karna
@router.get("/", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


# 3. Book ID se ek specific book fetch karna
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):

    # Di hui ID wali book ko database mein search karo
    book = db.query(Book).filter(
        Book.book_id == book_id
    ).first()

    # Agar book nahi milti toh 404 error return karo
    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book