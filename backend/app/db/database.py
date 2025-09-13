from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

engine = create_engine(
    str(settings.DATABASE_URL) if settings.DATABASE_URL else "",
    echo=False,  # Set to True for SQL logging during development
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()