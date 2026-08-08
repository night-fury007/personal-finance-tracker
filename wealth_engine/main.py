from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from wealth_engine.database import init_db, get_db
from wealth_engine.models import Category
from wealth_engine.routers import auth, expenses


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Modern FastAPI lifespan context manager handling startup events.
    Initializes SQLite database tables without seeding default data.
    """
    init_db()
    yield


app = FastAPI(
    title="Wealth Engine API",
    version="1.0.0",
    description="Enterprise Multi-User Personal Finance & Multi-Currency Portfolio Tracking Engine",
    lifespan=lifespan
)

# Configure CORS for Frontend integration (React/Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production to match your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(auth.router)
app.include_router(expenses.router)


@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(get_db)) -> dict:
    """
    System health check endpoint verifying database connectivity.
    """
    # Execute a lightweight query to ensure the database session is actively functional
    db.exec(select(Category)).first()

    return {
        "status": "healthy",
        "system": "Wealth Engine Core Active",
        "database": "Connected"
    }
