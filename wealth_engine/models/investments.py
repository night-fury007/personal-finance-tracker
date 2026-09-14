from datetime import date, datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from wealth_engine.models.users import User


class InvestmentCategory(SQLModel, table=True):
    __tablename__ = "investment_categories"
    __table_args__ = {"schema": "wealth_engine"}

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    investment_type: str = Field(max_length=50, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=255)

    investments: List["Investment"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Investment(SQLModel, table=True):
    __tablename__ = "investments"
    __table_args__ = {"schema": "wealth_engine"}

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: str = Field(foreign_key="wealth_engine.users.id", index=True)
    category_id: int = Field(foreign_key="wealth_engine.investment_categories.id", index=True)
    amount: Decimal = Field(default=Decimal("0.00"))
    currency: str = Field(max_length=3)
    investment_date: date = Field(index=True)
    asset_name: str = Field(max_length=100)
    ticker: Optional[str] = Field(default=None, max_length=20)
    units_acquired: Optional[Decimal] = Field(default=None)
    description: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field()
    updated_at: datetime = Field()

    user: Optional["User"] = Relationship(
        back_populates="investments",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    category: Optional["InvestmentCategory"] = Relationship(
        back_populates="investments",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
