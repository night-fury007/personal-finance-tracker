from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class AccountCreate(BaseModel):
    name: str = Field(max_length=100, description="Account name (e.g., HDFC Savings, Chase Checking)")
    account_type: str = Field(max_length=50, description="Type of account (e.g., Bank, Credit Card, Cash, Wallet)")
    currency: str = Field(default="INR", max_length=3, description="Base currency code (e.g., INR, USD)")
    current_balance: Decimal = Field(default=Decimal("0.00"), description="Opening or current account balance")
    is_active: Optional[bool] = Field(default=True, description="Account active status flag")


class AccountUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    account_type: Optional[str] = Field(default=None, max_length=50)
    currency: Optional[str] = Field(default=None, max_length=3)
    current_balance: Optional[Decimal] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)


class AccountResponse(AccountCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
