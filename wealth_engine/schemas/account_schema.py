from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel

from wealth_engine.core.types import CustomDateTimeIST
from wealth_engine.schemas.custom_types import CurrencyDecimal


class CamelCaseBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # Automatically converts snake_case <-> camelCase for both input and output
        populate_by_name=True,  # Allows internal Python code to still use snake_case if needed
        from_attributes=True,
    )


class AccountCreate(CamelCaseBaseModel):
    account_name: str = Field(max_length=100)
    category_id: int = Field()
    currency: str = Field(max_length=3)
    balance: CurrencyDecimal = Field(default=Decimal("0.00"))
    is_active: Optional[bool] = Field(default=True)


class AccountUpdate(CamelCaseBaseModel):
    public_account_id: str
    account_name: Optional[str] = Field(default=None, max_length=100)
    category_id: Optional[int] = Field(default=None)
    currency: Optional[str] = Field(default=None, max_length=3)
    balance: Optional[CurrencyDecimal] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)


class AccountResponse(CamelCaseBaseModel):
    public_account_id: str
    user_id: str
    account_name: str
    category_id: int
    account_type: str
    currency: str
    balance: CurrencyDecimal
    is_active: bool
    created_at: CustomDateTimeIST
    updated_at: Optional[CustomDateTimeIST] = None

    class Config:
        from_attributes = True


class AccountCategoryResponse(CamelCaseBaseModel):
    id: int
    account_type: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class AccountSummaryResponse(CamelCaseBaseModel):
    user_id: str
    total_balance_inr: CurrencyDecimal
    total_balance_usd: CurrencyDecimal

    class Config:
        from_attributes = True
