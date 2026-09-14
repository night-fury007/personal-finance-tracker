from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os

# SQLite database file stored locally inside the project root
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wealth_engine.db")
DATABASE_URL = "postgresql+psycopg://@localhost:5432/wealth_engine"


# connect_args={"check_same_thread": False} is required for SQLite in FastAPI multi-threaded environments
engine = create_engine(
    DATABASE_URL,
    echo=False
)

def init_db() -> None:
    """
    Creates all database tables defined under SQLModel metadata.
    """
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields an active database session
    and guarantees closure after the request finishes.
    """
    with Session(engine) as session:
        yield session
