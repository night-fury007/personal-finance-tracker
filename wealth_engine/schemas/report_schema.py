from decimal import Decimal
from pydantic import BaseModel, Field


class PortfolioValuationResponse(BaseModel):
    india_portfolio_inr: Decimal = Field(default=Decimal("0.00"))
    us_portfolio_usd: Decimal = Field(default=Decimal("0.00"))
    liquid_accounts_inr: Decimal = Field(default=Decimal("0.00"))
    liquid_accounts_usd: Decimal = Field(default=Decimal("0.00"))
    total_net_worth_usd_equivalent: Decimal = Field(default=Decimal("0.00"))
    exchange_rate_used: Decimal = Field(default=Decimal("83.00"))
