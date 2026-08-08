from fastapi import APIRouter, Depends
from sqlmodel import Session

from wealth_engine.core.dependencies import get_current_active_user, AuthenticatedUser
from wealth_engine.database import get_db
from wealth_engine.schemas.report_schema import PortfolioValuationResponse
from wealth_engine.services.report_service import ReportService

router = APIRouter(prefix="/api/v1/reports", tags=["Reports & Valuation"])


@router.get("/portfolio-valuation", response_model=PortfolioValuationResponse)
def get_portfolio_valuation(
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> PortfolioValuationResponse:
    """
    Returns multi-currency portfolio breakdown (INR vs USD) and total consolidated
    net worth normalized to USD equivalents for the authenticated user.
    """
    return ReportService.get_portfolio_valuation(db=db, user_id=current_user.id)
