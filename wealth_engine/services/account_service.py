from typing import Optional

from sqlmodel import Session

from wealth_engine.common.accounts_adapter import AccountAdapter
from wealth_engine.common.pginated_response import PaginatedResponse
from wealth_engine.core.exceptions import DatabaseOperationException
from wealth_engine.core.logger import logger
from wealth_engine.repository.accounts_repository import AccountRepository
from wealth_engine.schemas.account_schema import AccountCreate, AccountUpdate, AccountResponse, AccountCategoryResponse, \
    AccountSummaryResponse


class AccountService:
    @staticmethod
    def create_account(
            db: Session,
            user_id: str,
            account_in: AccountCreate
    ) -> Optional[AccountResponse]:

        try:
            logger.info(f"Creating account for {user_id}")
            account = AccountAdapter.format_create_account_data(user_id=user_id, account_in=account_in)
            created_account = AccountRepository.create_or_update_account(db, account)
            return AccountAdapter.format_account_response(created_account)
        except DatabaseOperationException as e:
            logger.error(f"Database operation failed while creating account for {user_id}: {e}")
            raise DatabaseOperationException(message=f"Failed to get account: {str(e)}") from e
        except Exception as e:
            logger.exception(f"Unexpected error occurred while creating account for {user_id}: {str(e)}")
            raise e

    @staticmethod
    def get_accounts_by_user(
            db: Session,
            user_id: str,
            page: int = 1,
            limit: int = 10
    ) -> PaginatedResponse[AccountResponse]:
        try:
            logger.info(f"Fetching accounts for user {user_id}")
            offset = max(0, (page - 1) * limit) if page > 0 else 0
            items, total = AccountRepository.get_by_user_id(db, user_id, offset, limit)
            return AccountAdapter.format_paginated_account_response(items, total, page, limit)
        except DatabaseOperationException as e:
            logger.error(f"Database operation failed while fetching account for {user_id}: {e}")
            raise DatabaseOperationException(message=f"Failed to get account: {str(e)}") from e
        except Exception as e:
            logger.exception(f"Unexpected error occurred while fetching account for {user_id}: {str(e)}")
            raise e

    @staticmethod
    def get_account_by_id(
            db: Session,
            public_account_id: str,
            user_id: str
    ) -> Optional[AccountResponse]:
        try:
            logger.info(f"Fetching accounts for user {user_id} and account id {public_account_id}")
            account = AccountRepository.get_by_id_and_user(db=db, public_account_id=public_account_id, user_id=user_id)
            if account is None:
                logger.info(f"Account id {public_account_id} not found for user {user_id}")
                return None
            return AccountAdapter.format_account_response(account)
        except DatabaseOperationException as e:
            logger.error(f"Database operation failed while fetching account id {public_account_id} for {user_id}: {e}")
            raise DatabaseOperationException(message=f"Failed to get account: {str(e)}") from e
        except Exception as e:
            logger.exception(
                f"Unexpected error occurred while fetching account id {public_account_id} for {user_id}: {str(e)}")
            raise e

    @staticmethod
    def get_account_by_search_or_filter(
            db: Session,
            user_id: str,
            page: int = 1,
            limit: int = 10,
            search: Optional[str] = None,
            account_type: Optional[str] = None
    ) -> PaginatedResponse[AccountResponse]:
        try:
            logger.info(f"Fetching accounts for user {user_id}")
            offset = max(0, (page - 1) * limit) if page > 0 else 0
            items, total = AccountRepository.get_by_search_or_filter(db, user_id, offset, limit, search, account_type)
            return AccountAdapter.format_paginated_account_response(items, total, page, limit)
        except DatabaseOperationException as e:
            logger.error(f"Database operation failed while fetching account for {user_id}: {str(e)}")
            raise DatabaseOperationException(message=f"Failed to get accounts: {str(e)}") from e
        except Exception as e:
            logger.exception(f"Unexpected error occurred while fetching account for {user_id}: {str(e)}")
            raise e

    @staticmethod
    def update_account(
            db: Session,
            user_id: str,
            account_in: AccountUpdate
    ) -> Optional[AccountResponse]:

        try:
            public_account_id = account_in.public_account_id
            account = AccountRepository.get_by_id_and_user(db=db, public_account_id=public_account_id, user_id=user_id)
            if account is None:
                logger.info(f"Account {public_account_id} not found")
                return None
            logger.info(f"Updating account id {public_account_id} for user {user_id}")
            formatted_account_data = AccountAdapter.format_update_account_data(account=account, account_in=account_in)
            updated_account = AccountRepository.create_or_update_account(db, formatted_account_data)
            return AccountAdapter.format_account_response(updated_account)
        except DatabaseOperationException as e:
            logger.error(f"Database operation failed while updating account id {public_account_id}: {e}")
            raise DatabaseOperationException(message=f"Failed to update account: {str(e)}") from e
        except Exception as e:
            logger.exception(f"Unexpected error occurred while updating account id {public_account_id}: {str(e)}")
            raise e

    @staticmethod
    def delete_account(
            db: Session,
            public_account_id: str,
            user_id: str) -> None:

        try:
            logger.info(f"Deleting account id {public_account_id} for user {user_id}")
            account = AccountRepository.get_by_id_and_user(db=db, public_account_id=public_account_id, user_id=user_id)
            if account is None:
                logger.info(f"Account id {public_account_id} not found for user {user_id}")
                return None
            deleted_account = AccountRepository.delete_account(db=db, account=account)
            logger.info(f"Deleted account details: {deleted_account} for user {user_id}")
        except DatabaseOperationException as e:
            db.rollback()
            logger.error(f"Database operation failed while deleting account id {public_account_id}: {e}")
            raise DatabaseOperationException(message=f"Failed to delete account: {str(e)}") from e
        except Exception as e:
            logger.exception(f"Unexpected error occurred while deleting account id {public_account_id}: {str(e)}")
            raise e

    @staticmethod
    def get_all_categories(
            db: Session
    ) -> list[AccountCategoryResponse]:
        try:
            logger.info(f"Fetching all categories")
            categories = AccountRepository.get_all_categories(db)
            return AccountAdapter.format_category_response(categories=categories)
        except DatabaseOperationException as e:
            logger.error(f"Database operation failed while fetching all categories: {str(e)}")
            raise DatabaseOperationException(message=f"Failed to get accounts: {str(e)}") from e
        except Exception as e:
            logger.exception(f"Unexpected error occurred while fetching all categories: {str(e)}")
            raise e

    @staticmethod
    def get_account_summary(
            db: Session,
            user_id: str,
    ) -> AccountSummaryResponse:
        try:
            logger.info(f"Fetching account summary for user {user_id}")
            total_inr, total_usd = AccountRepository.get_account_summary_by_userid(db, user_id)
            return AccountAdapter.format_account_summary_response(user_id=user_id, total_balance_inr=total_inr,
                                                                  total_balance_usd=total_usd)
        except DatabaseOperationException as e:
            logger.error(f"Database operation failed while fetching account summary for user {user_id}: {str(e)}")
            raise DatabaseOperationException(message=f"Failed to get account summary: {str(e)}") from e
        except Exception as e:
            logger.exception(f"Unexpected error occurred while fetching account summary for user {user_id}: {str(e)}")
            raise e
