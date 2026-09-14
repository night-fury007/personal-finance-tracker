from datetime import datetime
from typing import List
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from wealth_engine.models.accounts import Account
    from wealth_engine.models.expenses import Expense
    from wealth_engine.models.incomes import Income
    from wealth_engine.models.investments import Investment


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {"schema": "wealth_engine"}

    id: str = Field(unique=True, index=True, primary_key=True)
    name: str = Field(index=True, unique=True)
    email: str = Field(default=None, unique=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field()
    updated_at: datetime = Field()
    is_active: bool = Field(default=True)

    accounts: List["Account"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    expenses: List["Expense"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    incomes: List["Income"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    investments: List["Investment"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
