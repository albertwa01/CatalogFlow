# app/database/sync/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Database URL from .env
DATABASE_URL =settings.DATABASE_URL

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,        # Log SQL queries for debugging
    pool_size=10,
    max_overflow=20
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency for FastAPI endpoints
def get_db():
    """
    Yields a DB session for each request, ensures proper closure.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
