from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field


class FXRate(SQLModel, table=True):
    __tablename__ = "fx_rates"
    __table_args__ = {"schema": "wealth_engine"}

    id: Optional[int] = Field(default=None, primary_key=True)
    rate_date: date = Field(index=True, unique=True)
    base_currency: str = Field(max_length=3)
    target_currency: str = Field(max_length=3)
    rate: Decimal = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()
