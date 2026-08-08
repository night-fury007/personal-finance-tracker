from decimal import Decimal

from pydantic import BaseModel


class PortfolioValuationResponse(BaseModel):
    india_portfolio_inr: Decimal
    us_portfolio_usd: Decimal
    liquid_accounts_inr: Decimal
    liquid_accounts_usd: Decimal
    total_net_worth_usd_equivalent: Decimal
    exchange_rate_used: Decimal
