from datetime import date, datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from wealth_engine.models.users import User


class IncomeCategory(SQLModel, table=True):
    __tablename__ = "income_categories"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    income_type: str = Field(max_length=50, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=255)

    incomes: List["Income"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Income(SQLModel, table=True):
    __tablename__ = "incomes"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    category_id: int = Field(foreign_key="income_categories.id", index=True)
    amount: Decimal = Field(default=Decimal("0.00"))
    currency: str = Field(max_length=3)
    income_date: date = Field(index=True)
    description: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field()
    updated_at: datetime = Field()

    user: Optional["User"] = Relationship(
        back_populates="incomes",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    category: Optional["IncomeCategory"] = Relationship(
        back_populates="incomes",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
