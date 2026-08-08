from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal


class IncomeCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="INR", max_length=3)
    date: date
    source: str = Field(max_length=100, description="e.g., Salary, Dividends, Freelance")
    description: Optional[str] = Field(default=None, max_length=255)


class IncomeResponse(IncomeCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
