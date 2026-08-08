from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from wealth_engine.core.dependencies import get_current_user
from wealth_engine.database import get_db
from wealth_engine.models import Expense, User
from wealth_engine.schemas.expense_schema import ExpenseCreate, ExpenseResponse

router = APIRouter(prefix="/api/v1/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
        expense_in: ExpenseCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Expense:
    """
    Records a new expense for the authenticated tenant user.
    """
    expense = Expense(
        user_id=current_user.id,
        amount=expense_in.amount,
        currency=expense_in.currency,
        expense_date=expense_in.expense_date,
        description=expense_in.description,
        category_id=expense_in.category_id,
        subcategory_id=expense_in.subcategory_id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("/", response_model=List[ExpenseResponse])
def get_user_expenses(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> List[Expense]:
    """
    Retrieves all expenses belonging strictly to the authenticated tenant user.
    """
    statement = (
        select(Expense)
        .where(Expense.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    expenses = db.exec(statement).all()
    return list(expenses)
