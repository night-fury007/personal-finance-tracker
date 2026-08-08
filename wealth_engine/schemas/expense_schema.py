from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(gt=0, description="Expense amount (must be greater than 0)")
    currency: str = Field(default="INR", max_length=3, description="Currency code (e.g., INR, USD)")
    expense_date: date
    description: Optional[str] = Field(default=None, max_length=255)
    category_id: int
    subcategory_id: Optional[int] = Field(default=None)


class ExpenseResponse(ExpenseCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
