# SQLAlchemy se database connection banane ke tools import kar rahe hain
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# .env file se DATABASE_URL read karne ke liye
import os
from dotenv import load_dotenv


# .env file ki settings load kar rahe hain
load_dotenv()

# PostgreSQL database ka connection URL read kar rahe hain
DATABASE_URL = os.getenv("DATABASE_URL")
# Check kar rahe hain ki database URL mila ya nahi
if not DATABASE_URL:
    raise ValueError("DATABASE_URL .env file mein set nahi hai")

# PostgreSQL ke saath connection engine bana rahe hain
engine = create_engine(DATABASE_URL)

# Database session banane ka setup
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# SQLAlchemy models isi Base se database tables define karenge ################## get_db(session)
Base = declarative_base()

def get_db():
    # Naya database session create karo
    db = SessionLocal()

    try:
        # Session ko API route ke use ke liye provide karo
        yield db

    finally:
        # Kaam complete hone par session close karo
        db.close()