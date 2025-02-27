import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# Retrieve the DB_URL environment variable
db_url = os.getenv("DB_URL")
if db_url is None:
    raise EnvironmentError("DB_URL environment variable is not set.")
DB_URL: str = db_url

# Create a SQLAlchemy engine instance using the DB_URL
engine = create_engine(DB_URL)

# Create a session factory bound to this engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the declarative base for model definitions
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that creates a new SQLAlchemy SessionLocal object,
    yields it for use, and ensures that it is closed after use.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
