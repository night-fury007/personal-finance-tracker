from decimal import Decimal
from sqlmodel import Session, select, func
from wealth_engine.models import Investment, Account
from wealth_engine.schemas.report_schema import PortfolioValuationResponse
from wealth_engine.services.fx_service import FXService
from wealth_engine.core.exceptions import DatabaseOperationException


class ReportService:
    @staticmethod
    def get_portfolio_valuation(db: Session, user_id: int) -> PortfolioValuationResponse:
        """
        Computes multi-currency portfolio valuation and total net worth in USD equivalents
        for an authenticated tenant user, wrapped with robust exception handling.
        """
        try:
            exchange_rate = FXService.get_latest_exchange_rate(db, base="USD", target="INR")

            # 1. Aggregate Investments split by currency
            inv_inr_stmt = select(func.sum(Investment.amount)).where(
                Investment.user_id == user_id,
                Investment.currency == "INR"
            )
            india_portfolio_inr = db.exec(inv_inr_stmt).first() or Decimal("0.00")

            inv_usd_stmt = select(func.sum(Investment.amount)).where(
                Investment.user_id == user_id,
                Investment.currency == "USD"
            )
            us_portfolio_usd = db.exec(inv_usd_stmt).first() or Decimal("0.00")

            # 2. Aggregate Liquid Bank Accounts / Wallets split by currency
            acc_inr_stmt = select(func.sum(Account.current_balance)).where(
                Account.user_id == user_id,
                Account.currency == "INR",
                Account.is_active == True
            )
            liquid_accounts_inr = db.exec(acc_inr_stmt).first() or Decimal("0.00")

            acc_usd_stmt = select(func.sum(Account.current_balance)).where(
                Account.user_id == user_id,
                Account.currency == "USD",
                Account.is_active == True
            )
            liquid_accounts_usd = db.exec(acc_usd_stmt).first() or Decimal("0.00")

            # 3. Compute Consolidated Net Worth in USD Equivalent
            total_inr_assets = india_portfolio_inr + liquid_accounts_inr
            total_usd_assets_from_inr = total_inr_assets / exchange_rate
            total_native_usd_assets = us_portfolio_usd + liquid_accounts_usd

            total_net_worth_usd_equivalent = total_native_usd_assets + total_usd_assets_from_inr

            return PortfolioValuationResponse(
                india_portfolio_inr=india_portfolio_inr,
                us_portfolio_usd=us_portfolio_usd,
                liquid_accounts_inr=liquid_accounts_inr,
                liquid_accounts_usd=liquid_accounts_usd,
                total_net_worth_usd_equivalent=total_net_worth_usd_equivalent.quantize(Decimal("0.01")),
                exchange_rate_used=exchange_rate
            )
        except Exception as e:
            raise DatabaseOperationException(message=f"Failed to compute portfolio valuation: {str(e)}") from e
