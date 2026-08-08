from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wealth_engine.models.transaction import Expense, Investment, Income, Account

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)

    expenses: List["Expense"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    investments: List["Investment"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    income: List["Income"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    accounts: List["Account"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
