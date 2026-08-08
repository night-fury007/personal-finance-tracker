from typing import List, Sequence, Any, Optional
from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session

from wealth_engine.core.dependencies import get_current_active_user, AuthenticatedUser
from wealth_engine.database import get_db
from wealth_engine.models import Expense
from wealth_engine.schemas.expense_schema import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from wealth_engine.services.expense_service import ExpenseService

router = APIRouter(prefix="/api/v1/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
        expense_in: ExpenseCreate,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Expense:
    """
    Records a new expense for the authenticated tenant user.
    current_user.id is strictly guaranteed to be an int.
    """
    return ExpenseService.create_expense(db=db, user_id=current_user.id, expense_in=expense_in)


@router.get("/", response_model=List[ExpenseResponse])
def get_user_expenses(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Sequence[Expense]:
    return ExpenseService.get_expenses_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
        expense_id: int,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Optional[Any]:
    return ExpenseService.get_expense_by_id(db=db, expense_id=expense_id, user_id=current_user.id)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
        expense_id: int,
        expense_in: ExpenseUpdate,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Optional[Any]:
    return ExpenseService.update_expense(db=db, expense_id=expense_id, user_id=current_user.id, expense_in=expense_in)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
        expense_id: int,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Response:
    ExpenseService.delete_expense(db=db, expense_id=expense_id, user_id=current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
