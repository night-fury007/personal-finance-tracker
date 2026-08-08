from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal


class InvestmentCreate(BaseModel):
    amount: Decimal = Field(gt=0, description="Total capital invested")
    currency: str = Field(max_length=3, description="USD or INR")
    investment_date: date
    asset_category: str = Field(max_length=50, description="e.g., US_Equity, Indian_Equity, PPF, Mutual_Fund")
    asset_name: str = Field(max_length=100, description="e.g., Apple Inc, Reliance Industries")
    ticker: Optional[str] = Field(default=None, max_length=20)
    units_acquired: Optional[Decimal] = Field(default=None)
    description: Optional[str] = Field(default=None, max_length=255)


class InvestmentUpdate(BaseModel):
    amount: Optional[Decimal] = Field(default=None, gt=0)
    currency: Optional[str] = Field(default=None, max_length=3)
    investment_date: Optional[date] = Field(default=None)
    asset_category: Optional[str] = Field(default=None, max_length=50)
    asset_name: Optional[str] = Field(default=None, max_length=100)
    ticker: Optional[str] = Field(default=None, max_length=20)
    units_acquired: Optional[Decimal] = Field(default=None, ge=0)
    description: Optional[str] = Field(default=None, max_length=255)


class InvestmentResponse(InvestmentCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
