from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from starlette.responses import JSONResponse

from wealth_engine.core.exceptions import WealthEngineException
from wealth_engine.database import init_db, get_db
from wealth_engine.models import Category
from wealth_engine.routers import auth, expenses, investments, income, accounts, analytics, reports


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

# --- Global Custom Exception Handlers ---
@app.exception_handler(WealthEngineException)
async def wealth_engine_exception_handler(request: Request, exc: WealthEngineException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Fallback handler for unhandled critical runtime exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "An unexpected internal server error occurred.",
            "details": str(exc) if app.debug else None,
            "status_code": 500
        }
    )


# Mount Routers
app.include_router(auth.router)
app.include_router(income.router)
app.include_router(accounts.router)
app.include_router(investments.router)
app.include_router(expenses.router)
app.include_router(analytics.router)
app.include_router(reports.router)


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
