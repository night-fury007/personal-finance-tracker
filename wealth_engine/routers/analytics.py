from fastapi import APIRouter, Depends
from sqlmodel import Session

from wealth_engine.core.dependencies import AuthenticatedUser, get_current_active_user
from wealth_engine.database import get_db
from wealth_engine.schemas.analytics_schema import AnalyticsSummaryResponse
from wealth_engine.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics & Reporting"])

@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_financial_summary(
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> AnalyticsSummaryResponse:
    """
    Returns a comprehensive financial intelligence summary including
    net worth, cash flow, and category spending breakdown for the authenticated user.
    """
    return AnalyticsService.get_user_analytics(db=db, user_id=current_user.id)
