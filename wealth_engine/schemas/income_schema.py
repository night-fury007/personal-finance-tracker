from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, Literal
from datetime import date
from decimal import Decimal

from pydantic.alias_generators import to_camel

from wealth_engine.core.types import CustomDateTimeIST
from wealth_engine.schemas.custom_types import CurrencyDecimal


class CamelCaseBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # Automatically converts snake_case <-> camelCase for both input and output
        populate_by_name=True,  # Allows internal Python code to still use snake_case if needed
        from_attributes=True,
    )


class IncomeCreate(CamelCaseBaseModel):
    amount: CurrencyDecimal = Field(
        gt=0.00,
        description="Income amount must be greater than zero")
    category_id: int = Field(
        gt=0,
        description="Category ID must be a positive integer")
    public_account_id: str
    currency: Literal["INR", "USD"] = Field(
        default=None,
        description="Currency must be INR or USD")
    income_date: date
    description: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional transaction note")

    @field_validator("income_date")
    @classmethod
    def validate_income_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Income date cannot be in the future")
        return v


class IncomeUpdate(CamelCaseBaseModel):
    id: int
    existing_public_account_id: str
    new_public_account_id: str
    amount: Optional[CurrencyDecimal] = Field(default=None)
    category_id: Optional[int] = Field(default=None)
    public_account_id: str
    currency: Optional[str] = Field(default=None, max_length=3)
    income_date: Optional[date] = Field(default=None)
    description: Optional[str] = Field(default=None, max_length=255)


class IncomeResponse(CamelCaseBaseModel):
    id: int
    user_id: str
    amount: CurrencyDecimal
    public_account_id: str
    category_id: int
    income_type: str
    currency: str
    income_date: date
    description: Optional[str] = Field(default=None, max_length=255)
    created_at: CustomDateTimeIST
    updated_at: Optional[CustomDateTimeIST] = None

    class Config:
        from_attributes = True


class IncomeCategoryResponse(CamelCaseBaseModel):
    id: int
    income_type: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class IncomeSummaryResponse(CamelCaseBaseModel):
    user_id: str
    total_amount_inr: CurrencyDecimal
    total_income_usd: CurrencyDecimal

    class Config:
        from_attributes = True
