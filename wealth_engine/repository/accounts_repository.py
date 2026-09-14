from decimal import Decimal
from typing import Tuple, Sequence, Optional, Any

from sqlmodel import Session, select, func, col

from wealth_engine.core.exceptions import DatabaseOperationException
from wealth_engine.models import Account, AccountCategory


class AccountRepository:

    @staticmethod
    def create_or_update_account(
            db: Session,
            account: Account
    ) -> Optional[Account]:
        try:
            db.add(account)
            db.commit()
            db.refresh(account)

            return account
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to create account : {str(e)}") from e

    @staticmethod
    def delete_account(
            db: Session,
            account: Account
    ) -> Optional[Account]:
        try:
            account.is_active = False
            db.add(account)
            db.commit()
            db.refresh(account)
            return account
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(message=f"Failed to delete account : {str(e)}") from e

    @staticmethod
    def get_by_id_and_user(
            db: Session,
            public_account_id: str,
            user_id: str
    ) -> Optional[Account]:
        try:
            statement = (
                select(Account)
                .where(
                    Account.public_account_id == public_account_id,
                    Account.user_id == user_id,
                    Account.is_active == True)
            )
            return db.exec(statement).first()
        except Exception as e:
            raise DatabaseOperationException(
                message=f"Failed to fetch account by account id and user id : {str(e)}") from e

    @staticmethod
    def get_by_user_id(
            db: Session,
            user_id: str,
            offset: int,
            limit: int
    ) -> Tuple[Sequence[Account], int]:

        try:
            statement = (
                select(Account)
                .where(Account.user_id == user_id, Account.is_active == True)
                .offset(offset)
                .limit(limit)
            )

            count_statement = (
                select(func.count())
                .select_from(Account)
                .where(Account.user_id == user_id, Account.is_active == True)
            )

            items = db.exec(statement).all()
            total = db.exec(count_statement).one() or 0

            return items, total
        except Exception as e:
            raise DatabaseOperationException(message=f"Failed to fetch account by user id : {str(e)}") from e

    @staticmethod
    def get_by_search_or_filter(
            db: Session,
            user_id: str,
            offset: int,
            limit: int,
            search: Optional[str] = None,
            account_type: Optional[str] = None
    ) -> Tuple[Sequence[Account], int]:
        try:
            query = select(Account).join(AccountCategory).where(Account.user_id == user_id, Account.is_active == True)
            count_query = select(func.count()).select_from(Account).join(AccountCategory).where(
                Account.user_id == user_id, Account.is_active == True)

            if search:
                search_filter = col(Account.account_name).ilike(f"%{search}%")
                query = query.where(search_filter)
                count_query = count_query.where(search_filter)

            if account_type and account_type != "All":
                type_filter = (AccountCategory.account_type == account_type)
                query = query.where(type_filter)
                count_query = count_query.where(type_filter)

            total = db.exec(count_query).one() or 0

            query = query.offset(offset).limit(limit)
            items = db.exec(query).all()

            return items, total

        except Exception as e:
            raise DatabaseOperationException(message=f"Failed to fetch account by search or filter : {str(e)}") from e

    @staticmethod
    def get_all_categories(db: Session) -> Sequence[Any]:
        try:
            statement = select(AccountCategory).where(AccountCategory.id != 1)
            categories = db.exec(statement).all()
            return categories
        except Exception as e:
            raise DatabaseOperationException(message=f"Failed to fetch account by search or filter : {str(e)}") from e

    @staticmethod
    def get_account_summary_by_userid(
            db: Session,
            user_id: str,
    ) -> Sequence[Any]:
        try:
            # Calculate sum for INR accounts
            stmt_inr = select(func.coalesce(func.sum(Account.balance), Decimal("0.00"))).where(
                Account.user_id == user_id,
                Account.currency == "INR",
                Account.is_active == True
            )
            total_inr = db.exec(stmt_inr).one()

            stmt_usd = select(func.coalesce(func.sum(Account.balance), Decimal("0.00"))).where(
                Account.user_id == user_id,
                Account.currency == "USD",
                Account.is_active == True
            )
            total_usd = db.exec(stmt_usd).one()

            return total_inr, total_usd
        except Exception as e:
            raise DatabaseOperationException(message=f"Failed to fetch account summary by user id : {str(e)}") from e
