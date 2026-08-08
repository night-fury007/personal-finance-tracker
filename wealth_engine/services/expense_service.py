from typing import Sequence, Any, Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from wealth_engine.models import Expense
from wealth_engine.schemas.expense_schema import ExpenseCreate, ExpenseUpdate
from wealth_engine.core.exceptions import NotFoundException, DatabaseOperationException


class ExpenseService:
    @staticmethod
    def create_expense(db: Session, user_id: int, expense_in: ExpenseCreate) -> Expense:
        """
        Creates and persists a new expense record for a tenant user with integrity handling.
        """
        try:
            expense = Expense(
                user_id=user_id,
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
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(
                message="Invalid category_id or subcategory_id provided. Foreign key constraint failed."
            ) from e
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to create expense: {str(e)}") from e

    @staticmethod
    def get_expenses_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> Sequence[Expense]:
        """
        Retrieves a paginated list of expenses belonging to a tenant user.
        """
        statement = (
            select(Expense)
            .where(Expense.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return db.exec(statement).all()

    @staticmethod
    def get_expense_by_id(db: Session, expense_id: int, user_id: int) -> Optional[Any]:
        """
        Retrieves a single expense by ID with strict multi-tenant verification.
        """
        statement = select(Expense).where(Expense.id == expense_id, Expense.user_id == user_id)
        expense = db.exec(statement).first()
        if not expense:
            raise NotFoundException(message=f"Expense with ID {expense_id} not found or unauthorized access.")
        return expense

    @staticmethod
    def update_expense(db: Session, expense_id: int, user_id: int, expense_in: ExpenseUpdate) -> Optional[Any]:
        """
        Updates an existing expense securely with tenant isolation and constraint validation.
        """
        expense = ExpenseService.get_expense_by_id(db=db, expense_id=expense_id, user_id=user_id)

        update_data = expense_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(expense, key, value)

        try:
            db.add(expense)
            db.commit()
            db.refresh(expense)
            return expense
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(
                message="Invalid category_id or subcategory_id update. Constraint failed."
            ) from e
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to update expense: {str(e)}") from e

    @staticmethod
    def delete_expense(db: Session, expense_id: int, user_id: int) -> None:
        """
        Permanently deletes an expense after verifying tenant ownership.
        """
        expense = ExpenseService.get_expense_by_id(db=db, expense_id=expense_id, user_id=user_id)
        try:
            db.delete(expense)
            db.commit()
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to delete expense: {str(e)}") from e
