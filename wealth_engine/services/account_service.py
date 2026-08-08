from typing import Sequence, Any, Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from wealth_engine.models import Account
from wealth_engine.schemas.account_schema import AccountCreate, AccountUpdate
from wealth_engine.core.exceptions import NotFoundException, DatabaseOperationException


class AccountService:
    @staticmethod
    def create_account(db: Session, user_id: int, account_in: AccountCreate) -> Account:
        """
        Creates and persists a new financial account/wallet securely for a tenant user.
        """
        try:
            account = Account(
                user_id=user_id,
                name=account_in.name,
                account_type=account_in.account_type,
                currency=account_in.currency,
                current_balance=account_in.current_balance,
                is_active=account_in.is_active
            )
            db.add(account)
            db.commit()
            db.refresh(account)
            return account
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(
                message="Database integrity constraint violated while creating account."
            ) from e
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to create account: {str(e)}") from e

    @staticmethod
    def get_accounts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> Sequence[Account]:
        """
        Retrieves a paginated list of accounts belonging to a tenant user.
        """
        statement = (
            select(Account)
            .where(Account.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return db.exec(statement).all()

    @staticmethod
    def get_account_by_id(db: Session, account_id: int, user_id: int) -> Optional[Any]:
        """
        Retrieves a single account by ID with strict tenant ownership validation.
        """
        statement = select(Account).where(Account.id == account_id, Account.user_id == user_id)
        account = db.exec(statement).first()
        if not account:
            raise NotFoundException(message=f"Account with ID {account_id} not found or unauthorized access.")
        return account

    @staticmethod
    def update_account(db: Session, account_id: int, user_id: int, account_in: AccountUpdate) -> Optional[Any]:
        """
        Updates an existing financial account securely.
        """
        account = AccountService.get_account_by_id(db=db, account_id=account_id, user_id=user_id)

        update_data = account_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(account, key, value)

        try:
            db.add(account)
            db.commit()
            db.refresh(account)
            return account
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(message="Constraint failed during account update.") from e
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to update account: {str(e)}") from e

    @staticmethod
    def delete_account(db: Session, account_id: int, user_id: int) -> None:
        """
        Permanently deletes an account record after confirming ownership.
        """
        account = AccountService.get_account_by_id(db=db, account_id=account_id, user_id=user_id)
        try:
            db.delete(account)
            db.commit()
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to delete account: {str(e)}") from e
