import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Usar SQLite para desarrollo
SQLITE_DATABASE_URL = "sqlite:///./endurain_coach_student.db"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLITE_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()


def get_db():
    # Create a new database session and return it
    db = SessionLocal()

    try:
        # Yield the database session
        yield db
    finally:
        # Close the database session
        db.close()