from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional, List
from decimal import Decimal

from wealth_engine.common.utils import CustomDateTimeIST
from wealth_engine.models import AccountCategory
from wealth_engine.schemas.custom_types import CurrencyDecimal


class CamelCaseBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # Automatically converts snake_case <-> camelCase for both input and output
        populate_by_name=True,  # Allows internal python code to still use snake_case if needed
        from_attributes=True,
    )


class AccountCreate(CamelCaseBaseModel):
    account_name: str = Field(max_length=100)
    category_id: int = Field()
    currency: str = Field(max_length=3)
    balance: CurrencyDecimal = Field(default=Decimal("0.00"))
    is_active: Optional[bool] = Field(default=True)


class AccountUpdate(CamelCaseBaseModel):
    account_name: Optional[str] = Field(default=None, max_length=100)
    category_id: Optional[int] = Field(default=None)
    currency: Optional[str] = Field(default=None, max_length=3)
    balance: Optional[CurrencyDecimal] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)


class AccountResponse(CamelCaseBaseModel):
    id: int
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


class AccountCreateResponse(AccountCreate):
    id: int
    user_id: int


class AccountUpdateResponse(AccountUpdate):
    id: int
    user_id: int


class AccountCategoryResponse(CamelCaseBaseModel):
    total: int
    categories: List[AccountCategory]

    class Config:
        from_attributes = True
