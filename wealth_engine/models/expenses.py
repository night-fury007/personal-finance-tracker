from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from wealth_engine.models.users import User


class ExpenseCategory(SQLModel, table=True):
    __tablename__ = "expense_categories"
    __table_args__ = {"schema": "wealth_engine"}

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    expense_type: str = Field(max_length=50, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=255)

    expenses: List["Expense"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"
    __table_args__ = {"schema": "wealth_engine"}

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: str = Field(foreign_key="wealth_engine.users.id", index=True)
    category_id: int = Field(foreign_key="wealth_engine.expense_categories.id", index=True)
    amount: Decimal = Field(default=Decimal("0.00"))
    currency: str = Field(max_length=3)
    expense_date: date = Field(index=True)
    description: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field()
    updated_at: datetime = Field()

    user: Optional["User"] = Relationship(
        back_populates="expenses",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    category: Optional["ExpenseCategory"] = Relationship(
        back_populates="expenses",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
