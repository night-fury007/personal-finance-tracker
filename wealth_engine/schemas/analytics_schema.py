from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Dict

class CashFlowSummary(BaseModel):
    total_income: Decimal = Field(default=Decimal("0.00"))
    total_expenses: Decimal = Field(default=Decimal("0.00"))
    net_savings: Decimal = Field(default=Decimal("0.00"))

class NetWorthSummary(BaseModel):
    total_liquid_accounts: Decimal = Field(default=Decimal("0.00"))
    total_investments: Decimal = Field(default=Decimal("0.00"))
    total_net_worth: Decimal = Field(default=Decimal("0.00"))

class AnalyticsSummaryResponse(BaseModel):
    base_currency: str = Field(default="INR")
    cash_flow: CashFlowSummary
    net_worth: NetWorthSummary
    category_spending: Dict[str, Decimal] = Field(default_factory=dict, description="Total expenses grouped by category name")
