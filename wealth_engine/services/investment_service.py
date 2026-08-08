from typing import Sequence, Any, Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from wealth_engine.models import Investment
from wealth_engine.schemas.investment_schema import InvestmentCreate, InvestmentUpdate
from wealth_engine.core.exceptions import NotFoundException, DatabaseOperationException


class InvestmentService:
    @staticmethod
    def create_investment(db: Session, user_id: int, investment_in: InvestmentCreate) -> Investment:
        """
        Persists a new investment asset record securely for an authenticated tenant.
        """
        try:
            investment = Investment(
                user_id=user_id,
                amount=investment_in.amount,
                currency=investment_in.currency,
                investment_date=investment_in.investment_date,
                asset_category=investment_in.asset_category,
                asset_name=investment_in.asset_name,
                ticker=investment_in.ticker,
                units_acquired=investment_in.units_acquired,
                description=investment_in.description
            )
            db.add(investment)
            db.commit()
            db.refresh(investment)
            return investment
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(
                message="Database integrity constraint violated while creating investment."
            ) from e
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to create investment: {str(e)}") from e

    @staticmethod
    def get_investments_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> Sequence[Investment]:
        """
        Retrieves a paginated list of investment portfolio assets for a tenant user.
        """
        statement = (
            select(Investment)
            .where(Investment.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return db.exec(statement).all()

    @staticmethod
    def get_investment_by_id(db: Session, investment_id: int, user_id: int) -> Optional[Any]:
        """
        Retrieves a single investment holding by ID with strict tenant ownership validation.
        """
        statement = select(Investment).where(Investment.id == investment_id, Investment.user_id == user_id)
        investment = db.exec(statement).first()
        if not investment:
            raise NotFoundException(message=f"Investment with ID {investment_id} not found or unauthorized access.")
        return investment

    @staticmethod
    def update_investment(db: Session, investment_id: int, user_id: int, investment_in: InvestmentUpdate) -> Optional[
        Any]:
        """
        Updates an existing portfolio asset record securely.
        """
        investment = InvestmentService.get_investment_by_id(db=db, investment_id=investment_id, user_id=user_id)

        update_data = investment_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(investment, key, value)

        try:
            db.add(investment)
            db.commit()
            db.refresh(investment)
            return investment
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(message="Constraint failed during investment update.") from e
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to update investment: {str(e)}") from e

    @staticmethod
    def delete_investment(db: Session, investment_id: int, user_id: int) -> None:
        """
        Permanently deletes an investment holding after confirming ownership.
        """
        investment = InvestmentService.get_investment_by_id(db=db, investment_id=investment_id, user_id=user_id)
        try:
            db.delete(investment)
            db.commit()
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to delete investment: {str(e)}") from e
