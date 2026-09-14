from decimal import Decimal
from typing import Tuple, Sequence, Optional, Any

from sqlmodel import Session, select, func, col

from wealth_engine.core.exceptions import DatabaseOperationException
from wealth_engine.models import Income


class IncomeRepository:

    @staticmethod
    def create_or_update_income(
            db: Session,
            income: Income
    ) -> Optional[Income]:
        try:
            db.add(income)
            db.commit()
            db.refresh(income)

            return income
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to create income : {str(e)}") from e

    @staticmethod
    def get_by_id_and_user(
            db: Session,
            income_id: int,
            user_id: str
    ) -> Optional[Income]:
        try:
            statement = (
                select(Income)
                .where(Income.id == income_id,
                       Income.user_id == user_id)
            )
            return db.exec(statement).first()
        except Exception as e:
            raise DatabaseOperationException(
                message=f"Failed to fetch income by income id and user id : {str(e)}") from e

    @staticmethod
    def get_by_user_id(
            db: Session,
            user_id: str,
            offset: int,
            limit: int
    ) -> Tuple[Sequence[Income], int]:
        try:
            statement = (
                select(Income)
                .where(Income.user_id == user_id)
                .offset(offset)
                .limit(limit)
            )

            count_statement = (
                select(func.count())
                .select_from(Income)
                .where(Income.user_id == user_id)
            )

            items = db.exec(statement).all()
            total = db.exec(count_statement).one() or 0

            return items, total
        except Exception as e:
            raise DatabaseOperationException(message=f"Failed to fetch income by user id : {str(e)}") from e
