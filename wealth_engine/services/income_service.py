from typing import Sequence, Any, Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from wealth_engine.models import Income
from wealth_engine.schemas.income_schema import IncomeCreate, IncomeUpdate
from wealth_engine.core.exceptions import NotFoundException, DatabaseOperationException


class IncomeService:
    @staticmethod
    def create_income(db: Session, user_id: int, income_in: IncomeCreate) -> Income:
        """
        Creates and persists a new income record securely for a tenant user.
        """
        try:
            income = Income(
                user_id=user_id,
                amount=income_in.amount,
                currency=income_in.currency,
                income_date=income_in.income_date,
                source=income_in.source,
                description=income_in.description
            )
            db.add(income)
            db.commit()
            db.refresh(income)
            return income
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(
                message="Database integrity constraint violated while creating income."
            ) from e
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to create income: {str(e)}") from e

    @staticmethod
    def get_incomes_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> Sequence[Income]:
        """
        Retrieves a paginated list of income streams belonging to a tenant user.
        """
        statement = (
            select(Income)
            .where(Income.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return db.exec(statement).all()

    @staticmethod
    def get_income_by_id(db: Session, income_id: int, user_id: int) -> Optional[Any]:
        """
        Retrieves a single income record by ID with strict tenant ownership validation.
        """
        statement = select(Income).where(Income.id == income_id, Income.user_id == user_id)
        income = db.exec(statement).first()
        if not income:
            raise NotFoundException(message=f"Income record with ID {income_id} not found or unauthorized access.")
        return income

    @staticmethod
    def update_income(db: Session, income_id: int, user_id: int, income_in: IncomeUpdate) -> Income:
        """
        Updates an existing income record securely.
        """
        income = IncomeService.get_income_by_id(db=db, income_id=income_id, user_id=user_id)

        update_data = income_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(income, key, value)

        try:
            db.add(income)
            db.commit()
            db.refresh(income)
            return income
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(message="Constraint failed during income update.") from e
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to update income: {str(e)}") from e

    @staticmethod
    def delete_income(db: Session, income_id: int, user_id: int) -> None:
        """
        Permanently deletes an income record after confirming ownership.
        """
        income = IncomeService.get_income_by_id(db=db, income_id=income_id, user_id=user_id)
        try:
            db.delete(income)
            db.commit()
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to delete income: {str(e)}") from e
