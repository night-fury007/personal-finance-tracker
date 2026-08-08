from sqlmodel import Session, select, func
from decimal import Decimal
from typing import Dict
from wealth_engine.models import Expense, Income, Investment, Account, Category
from wealth_engine.schemas.analytics_schema import (
    AnalyticsSummaryResponse,
    CashFlowSummary,
    NetWorthSummary
)
from wealth_engine.core.exceptions import DatabaseOperationException

class AnalyticsService:
    @staticmethod
    def get_user_analytics(db: Session, user_id: int) -> AnalyticsSummaryResponse:
        """
        Aggregates multi-domain financial data to compute net worth,
        cash flow, and category spending distribution for an authenticated tenant.
        Safely wraps operations in custom exception handlers.
        """
        try:
            # 1. Calculate Total Income
            income_stmt = select(func.sum(Income.amount)).where(Income.user_id == user_id)
            total_income = db.exec(income_stmt).first() or Decimal("0.00")

            # 2. Calculate Total Expenses
            expense_stmt = select(func.sum(Expense.amount)).where(Expense.user_id == user_id)
            total_expenses = db.exec(expense_stmt).first() or Decimal("0.00")

            net_savings = total_income - total_expenses

            # 3. Calculate Total Liquid Accounts Balance
            account_stmt = select(func.sum(Account.current_balance)).where(
                Account.user_id == user_id,
                Account.is_active == True
            )
            total_accounts = db.exec(account_stmt).first() or Decimal("0.00")

            # 4. Calculate Total Investments Capital
            investment_stmt = select(func.sum(Investment.amount)).where(Investment.user_id == user_id)
            total_investments = db.exec(investment_stmt).first() or Decimal("0.00")

            total_net_worth = total_accounts + total_investments

            # 5. Calculate Category-wise Spending Breakdown
            spending_stmt = (
                select(Category.name, func.sum(Expense.amount))
                .join(Expense, Expense.category_id == Category.id)
                .where(Expense.user_id == user_id)
                .group_by(Category.name)
            )
            spending_results = db.exec(spending_stmt).all()
            category_spending: Dict[str, Decimal] = {
                cat_name: total_amt for cat_name, total_amt in spending_results
            }

            return AnalyticsSummaryResponse(
                base_currency="INR",
                cash_flow=CashFlowSummary(
                    total_income=total_income,
                    total_expenses=total_expenses,
                    net_savings=net_savings
                ),
                net_worth=NetWorthSummary(
                    total_liquid_accounts=total_accounts,
                    total_investments=total_investments,
                    total_net_worth=total_net_worth
                ),
                category_spending=category_spending
            )
        except Exception as e:
            raise DatabaseOperationException(message=f"Failed to compute user analytics summary: {str(e)}") from e
