from typing import Any, Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from wealth_engine.adapter.IncomeAdapter import IncomeAdapter
from wealth_engine.common.pginated_response import PaginatedResponse
from wealth_engine.common.utils import calculate_page_offset
from wealth_engine.core.exceptions import NotFoundException, DatabaseOperationException, BadRequestException
from wealth_engine.core.logger import logger
from wealth_engine.models import Income
from wealth_engine.repository import AccountRepository
from wealth_engine.repository.incomes_repository import IncomeRepository
from wealth_engine.schemas.income_schema import IncomeCreate, IncomeUpdate, IncomeResponse


class IncomeService:
    @staticmethod
    def create_income(
            db: Session,
            user_id: str,
            income_in: IncomeCreate
    ) -> Optional[IncomeResponse]:
        try:
            logger.info(f"Creating income for {user_id}")
            account = AccountRepository.get_by_id_and_user(db=db,public_account_id=income_in.public_account_id, user_id=user_id)
            logger.info(f"account: {account}")
            if account is None or not account.is_active:
                raise NotFoundException(message="Target account not found")
            if account.currency != income_in.currency:
                raise BadRequestException(message="Income currency must match account currency")
            income = IncomeAdapter.format_create_income_data(user_id=user_id, income_in=income_in, account=account)
            created_income = IncomeRepository.create_or_update_income(db=db, income=income)
            return IncomeAdapter.format_income_response(created_income)
        except DatabaseOperationException as e:
            logger.error(f"Database operation failed while creating income for {user_id}: {e}")
            raise DatabaseOperationException(message=f"Failed to get income: {str(e)}") from e
        except Exception as e:
            logger.exception(f"Unexpected error occurred while creating income for {user_id}: {str(e)}")
            raise e

    @staticmethod
    def get_incomes_by_user(
            db: Session,
            user_id: str,
            page: int = 1,
            limit: int = 10
    ) -> PaginatedResponse[IncomeResponse]:
        try:
            logger.info(f"Getting incomes for {user_id}")
            offset = calculate_page_offset(page, limit)
            items, total = IncomeRepository.get_by_user_id(db=db, user_id=user_id, offset=offset, limit=limit)
            return IncomeAdapter.format_paginated_income_response(items, total, page, limit)
        except DatabaseOperationException as e:
            logger.error(f"Database operation failed while fetching account for {user_id}: {e}")
            raise DatabaseOperationException(message=f"Failed to get account: {str(e)}") from e
        except Exception as e:
            logger.exception(f"Unexpected error occurred while fetching account for {user_id}: {str(e)}")
            raise e

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
