from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wealth_engine.models.user import User
    from wealth_engine.models.category import Category, SubCategory

class Expense(SQLModel, table=True):
    __tablename__ = "expenses"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    amount: Decimal = Field(ge=0.01)
    currency: str = Field(default="INR", max_length=3)
    expense_date: date = Field(index=True)
    description: Optional[str] = Field(default=None, max_length=255)

    category_id: int = Field(foreign_key="categories.id")
    subcategory_id: Optional[int] = Field(default=None, foreign_key="subcategories.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional["User"] = Relationship(back_populates="expenses")
    category: Optional["Category"] = Relationship(back_populates="expenses")
    subcategory: Optional["SubCategory"] = Relationship(back_populates="expenses")


class Investment(SQLModel, table=True):
    __tablename__ = "investments"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    amount: Decimal = Field(ge=0.01)
    currency: str = Field(max_length=3)
    investment_date: date = Field(index=True)

    asset_category: str = Field(max_length=50)
    asset_name: str = Field(max_length=100)
    ticker: Optional[str] = Field(default=None, max_length=20)
    units_acquired: Optional[Decimal] = Field(default=None)
    description: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional["User"] = Relationship(back_populates="investments")


class Income(SQLModel, table=True):
    __tablename__ = "income"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    amount: Decimal = Field(ge=0.01)
    currency: str = Field(default="INR", max_length=3)
    income_date: date = Field(index=True)
    source: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional["User"] = Relationship(back_populates="income")


class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=100)
    account_type: str = Field(max_length=50)
    currency: str = Field(default="INR", max_length=3)
    current_balance: Decimal = Field(default=Decimal("0.00"))
    is_active: bool = Field(default=True)

    user: Optional["User"] = Relationship(back_populates="accounts")
