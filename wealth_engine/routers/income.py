from typing import List, Sequence, Any, Optional

from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session

from wealth_engine.core.dependencies import AuthenticatedUser, get_current_active_user
from wealth_engine.database import get_db
from wealth_engine.models import Income
from wealth_engine.schemas.income_schema import IncomeCreate, IncomeUpdate, IncomeResponse
from wealth_engine.services.income_service import IncomeService

router = APIRouter(prefix="/api/v1/income", tags=["Income"])


@router.post("/", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
def create_income(
        income_in: IncomeCreate,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Income:
    """
    Records a new income stream for the authenticated tenant user.
    """
    return IncomeService.create_income(db=db, user_id=current_user.id, income_in=income_in)


@router.get("/", response_model=List[IncomeResponse])
def get_user_incomes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Sequence[Income]:
    """
    Retrieves all income streams belonging strictly to the authenticated tenant user.
    """
    return IncomeService.get_incomes_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{income_id}", response_model=IncomeResponse)
def get_income(
        income_id: int,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Optional[Any]:
    """
    Retrieves a specific income record by ID with tenant security checks.
    """
    return IncomeService.get_income_by_id(db=db, income_id=income_id, user_id=current_user.id)


@router.put("/{income_id}", response_model=IncomeResponse)
def update_income(
        income_id: int,
        income_in: IncomeUpdate,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Income:
    """
    Updates an existing income record securely.
    """
    return IncomeService.update_income(db=db, income_id=income_id, user_id=current_user.id, income_in=income_in)


@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income(
        income_id: int,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Response:
    """
    Deletes an income record securely.
    """
    IncomeService.delete_income(db=db, income_id=income_id, user_id=current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
