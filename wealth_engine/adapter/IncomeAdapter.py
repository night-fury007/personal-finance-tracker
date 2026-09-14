from datetime import datetime, timezone
from typing import Sequence

from wealth_engine.common.pginated_response import PaginatedResponse
from wealth_engine.models import Income, Account
# from wealth_engine.routers import income
from wealth_engine.schemas.income_schema import IncomeCreate, IncomeResponse


class IncomeAdapter:
    @staticmethod
    def format_create_income_data(
            user_id: str,
            income_in: IncomeCreate,
            account: Account
    ) -> Income:
        return Income(
            user_id=user_id,
            category_id=income_in.category_id,
            account_id=account.id,
            amount=account.balance + income_in.amount,
            currency=income_in.currency,
            income_date=income_in.income_date,
            description=income_in.description,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

    @staticmethod
    def format_income_response(
            income_data: Income
    ) -> IncomeResponse:
        return IncomeResponse(
            id=income_data.id,
            user_id=income_data.user_id,
            amount=income_data.amount,
            public_account_id=income_data.account.public_account_id if income_data.account else "",
            category_id=income_data.category_id,
            income_type=income_data.category.income_type if income_data.category else "",
            currency=income_data.currency,
            income_date=income_data.income_date,
            description=income_data.description,
            created_at=income_data.created_at,
            updated_at=income_data.updated_at
        )

    @staticmethod
    def format_paginated_income_response(
            incomes: Sequence[Income],
            total: int,
            page: int,
            limit: int
    ) -> PaginatedResponse[IncomeResponse]:
        formatted_income_responses = [
            IncomeAdapter.format_income_response(income) for income in incomes
        ]
        return PaginatedResponse.create(
            items=formatted_income_responses,
            total=total,
            page=page,
            limit=limit
        )
