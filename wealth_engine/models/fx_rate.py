from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime, timezone
from decimal import Decimal


class FXRate(SQLModel, table=True):
    __tablename__ = "fx_rates"

    id: Optional[int] = Field(default=None, primary_key=True)
    rate_date: date = Field(index=True, unique=True)
    base_currency: str = Field(default="USD", max_length=3)
    target_currency: str = Field(default="INR", max_length=3)
    rate: Decimal = Field()
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
