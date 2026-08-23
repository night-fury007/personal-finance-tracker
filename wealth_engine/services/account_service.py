from typing import Optional

from sqlmodel import Session

from wealth_engine.common.accounts_adapter import AccountAdapter
from wealth_engine.common.pginated_response import PaginatedResponse
from wealth_engine.core.exceptions import DatabaseOperationException
from wealth_engine.repository.accounts_repository import AccountRepository
from wealth_engine.schemas.account_schema import AccountCreate, AccountUpdate, AccountResponse, AccountCategoryResponse


class AccountService:
    @staticmethod
    def create_account(
            db: Session,
            user_id: str,
            account_in: AccountCreate
    ) -> Optional[AccountResponse]:

        try:
            account = AccountAdapter.format_create_account_data(user_id=user_id, account_in=account_in)
            created_account = AccountRepository.create_or_update_account(db, account)
            return AccountAdapter.format_account_response(created_account)
        except DatabaseOperationException as e:
            print(f"Exception Occurred : {e}")
            raise DatabaseOperationException(message=f"Failed to get account: {str(e)}") from e
        except Exception as e:
            raise e

    @staticmethod
    def get_accounts_by_user(
            db: Session,
            user_id: str,
            page: int = 1,
            limit: int = 10
    ) -> PaginatedResponse[AccountResponse]:
        try:
            offset = max(0, (page - 1) * limit) if page > 0 else 0
            items, total = AccountRepository.get_by_user_id(db, user_id, offset, limit)
            return AccountAdapter.format_paginated_account_response(items, total, page, limit)
        except DatabaseOperationException as e:
            print(f"Exception Occurred : {e}")
            raise DatabaseOperationException(message=f"Failed to get account: {str(e)}") from e
        except Exception as e:
            raise e

    @staticmethod
    def get_account_by_id(
            db: Session,
            account_id: int,
            user_id: str
    ) -> Optional[AccountResponse]:
        try:
            account = AccountRepository.get_by_id_and_user(db=db, account_id=account_id, user_id=user_id)
            if account is None:
                print(f"Account {account_id} not found")
                return None
            return AccountAdapter.format_account_response(account)
        except DatabaseOperationException as e:
            print(f"Exception Occurred : {e}")
            raise DatabaseOperationException(message=f"Failed to get account: {str(e)}") from e
        except Exception as e:
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
            offset = max(0, (page - 1) * limit) if page > 0 else 0
            items, total = AccountRepository.get_by_search_or_filter(db, user_id, offset, limit, search, account_type)
            return AccountAdapter.format_paginated_account_response(items, total, page, limit)
        except DatabaseOperationException as e:
            print(f"Exception Occurred : {e}")
            raise DatabaseOperationException(message=f"Failed to get accounts: {str(e)}") from e
        except Exception as e:
            raise e

    @staticmethod
    def update_account(
            db: Session,
            account_id: int,
            user_id: str,
            account_in: AccountUpdate
    ) -> Optional[AccountResponse]:

        try:
            account = AccountRepository.get_by_id_and_user(db=db, account_id=account_id, user_id=user_id)
            formatted_account_data = AccountAdapter.format_update_account_data(account=account, account_in=account_in)
            updated_account = AccountRepository.create_or_update_account(db, formatted_account_data)
            return AccountAdapter.format_account_response(updated_account)
        except DatabaseOperationException as e:
            print(f"Exception Occurred : {e}")
            raise DatabaseOperationException(message=f"Failed to update account: {str(e)}") from e
        except Exception as e:
            raise e

    @staticmethod
    def delete_account(
            db: Session,
            account_id: int,
            user_id: str) -> None:

        try:
            account = AccountRepository.get_by_id_and_user(db=db, account_id=account_id, user_id=user_id)
            deleted_account = AccountRepository.delete_account(db=db, account=account)
            print(deleted_account)
        except DatabaseOperationException as e:
            db.rollback()
            print(f"Exception Occurred : {e}")
            raise DatabaseOperationException(message=f"Failed to delete account: {str(e)}") from e
        except Exception as e:
            raise e

    @staticmethod
    def get_all_categories(
            db: Session
    ) -> AccountCategoryResponse:
        try:
            categories = AccountRepository.get_all_categories(db)
            return AccountAdapter.format_category_response(categories=categories)
        except DatabaseOperationException as e:
            print(f"Exception Occurred : {e}")
            raise DatabaseOperationException(message=f"Failed to get accounts: {str(e)}") from e
        except Exception as e:
            raise e
