from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal

from wealth_engine.schemas.custom_types import CurrencyDecimal


class ExpenseCreate(BaseModel):
    amount: CurrencyDecimal = Field(default=Decimal("0.00"))
    currency: str = Field(max_length=3)
    expense_date: date
    description: Optional[str] = Field(default=None, max_length=255)
    category_id: int


class ExpenseUpdate(BaseModel):
    amount: Optional[Decimal] = Field(default=None, gt=0)
    currency: Optional[str] = Field(default=None, max_length=3)
    expense_date: Optional[date] = Field(default=None)
    description: Optional[str] = Field(default=None, max_length=255)
    category_id: Optional[int] = Field(default=None)
    subcategory_id: Optional[int] = Field(default=None)


class ExpenseResponse(ExpenseCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
