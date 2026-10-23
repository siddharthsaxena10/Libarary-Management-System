from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorResponse

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)


# Naya author create karna
@router.post("/", response_model=AuthorResponse)
def create_author(
    author_data: AuthorCreate,
    db: Session = Depends(get_db)
):
    # Request se author ka naam lekar SQLAlchemy object banao
    new_author = Author(
        author_name=author_data.author_name
    )

    # Database mein save karo
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author


# Saare authors fetch karna
@router.get("/", response_model=list[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()


# ID se ek author fetch karna
@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(
    author_id: int,
    db: Session = Depends(get_db)
):
    author = db.query(Author).filter(
        Author.author_id == author_id
    ).first()

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return author