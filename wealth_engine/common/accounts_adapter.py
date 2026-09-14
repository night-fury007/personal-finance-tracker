from datetime import datetime, timezone
from typing import Sequence

from wealth_engine.common.pginated_response import PaginatedResponse
from wealth_engine.common.utils import generate_public_account_id
from wealth_engine.models import Account, AccountCategory
from wealth_engine.schemas.account_schema import AccountCreate, AccountUpdate, AccountResponse, AccountCategoryResponse, \
    AccountSummaryResponse


class AccountAdapter:
    @staticmethod
    def format_create_account_data(
            user_id: str,
            account_in: AccountCreate
    ) -> Account:
        return Account(
            user_id=user_id,
            public_account_id=generate_public_account_id(),
            account_name=account_in.account_name,
            category_id=account_in.category_id,
            currency=account_in.currency,
            balance=account_in.balance,
            is_active=account_in.is_active,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

    @staticmethod
    def format_update_account_data(
            account_in: AccountUpdate,
            account: Account
    ) -> Account:
        update_data = account_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(account, key, value)
        account.updated_at = datetime.now(timezone.utc)
        return account

    @staticmethod
    def format_account_response(
            acc: Account
    ) -> AccountResponse:
        return AccountResponse(
            public_account_id=acc.public_account_id,
            user_id=acc.user_id,
            account_name=acc.account_name,
            category_id=acc.category_id,
            account_type=acc.category.account_type if acc.category else "",
            currency=acc.currency,
            balance=acc.balance,
            is_active=acc.is_active,
            created_at=acc.created_at,
            updated_at=acc.updated_at
        )

    @staticmethod
    def format_paginated_account_response(
            accounts: Sequence[Account],
            total: int,
            page: int,
            limit: int
    ) -> PaginatedResponse[AccountResponse]:
        formatted_account_responses = [
            AccountAdapter.format_account_response(account) for account in accounts
        ]
        return PaginatedResponse.create(
            items=formatted_account_responses,
            total=total,
            page=page,
            limit=limit
        )

    @staticmethod
    def format_category_response(
            categories: Sequence[AccountCategory]
    ) -> list[AccountCategoryResponse]:
        return [AccountCategoryResponse.model_validate(cat) for cat in categories]

    @staticmethod
    def format_account_summary_response(
            user_id: str,
            total_balance_inr,
            total_balance_usd,
    ) -> AccountSummaryResponse:
        return AccountSummaryResponse(
            user_id=user_id,
            total_balance_inr=total_balance_inr,
            total_balance_usd=total_balance_usd,
        )
