from typing import List, Sequence, Any, Optional

from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session

from wealth_engine.core.dependencies import AuthenticatedUser, get_current_active_user
from wealth_engine.database import get_db
from wealth_engine.models import Investment
from wealth_engine.schemas.investment_schema import InvestmentCreate, InvestmentUpdate, InvestmentResponse
from wealth_engine.services.investment_service import InvestmentService

router = APIRouter(prefix="/api/v1/investments", tags=["Investments"])


@router.post("/", response_model=InvestmentResponse, status_code=status.HTTP_201_CREATED)
def create_investment(
        investment_in: InvestmentCreate,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Investment:
    """
    Records a new investment portfolio asset for the authenticated tenant user.
    """
    return InvestmentService.create_investment(db=db, user_id=current_user.id, investment_in=investment_in)


@router.get("/", response_model=List[InvestmentResponse])
def get_user_investments(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Sequence[Investment]:
    """
    Retrieves all investment portfolio holdings belonging strictly to the authenticated tenant user.
    """
    return InvestmentService.get_investments_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{investment_id}", response_model=InvestmentResponse)
def get_investment(
        investment_id: int,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Optional[Any]:
    """
    Retrieves a specific investment holding by ID with tenant security checks.
    """
    return InvestmentService.get_investment_by_id(db=db, investment_id=investment_id, user_id=current_user.id)


@router.put("/{investment_id}", response_model=InvestmentResponse)
def update_investment(
        investment_id: int,
        investment_in: InvestmentUpdate,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Optional[Any]:
    """
    Updates an existing investment holding securely.
    """
    return InvestmentService.update_investment(db=db, investment_id=investment_id, user_id=current_user.id,
                                               investment_in=investment_in)


@router.delete("/{investment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_investment(
        investment_id: int,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Response:
    """
    Deletes an investment record securely.
    """
    InvestmentService.delete_investment(db=db, investment_id=investment_id, user_id=current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
