from datetime import datetime
from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from wealth_engine.models.users import User


class AccountCategory(SQLModel, table=True):
    __tablename__ = "account_categories"
    __table_args__ = {"schema": "wealth_engine"}

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    account_type: str = Field(max_length=50, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=255)

    accounts: List["Account"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Account(SQLModel, table=True):
    __tablename__ = "accounts"
    __table_args__ = {"schema": "wealth_engine"}

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    public_account_id: str = Field(max_length=36, unique=True, index=True)
    user_id: str = Field(foreign_key="wealth_engine.users.id", index=True)
    category_id: int = Field(foreign_key="wealth_engine.account_categories.id", index=True)
    account_name: str = Field(max_length=100)
    currency: str = Field(max_length=3)
    balance: Decimal = Field(default=Decimal("0.00"))
    is_active: bool = Field(default=True)
    created_at: datetime = Field()
    updated_at: datetime = Field()

    user: Optional["User"] = Relationship(
        back_populates="accounts",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    category: Optional[AccountCategory] = Relationship(
        back_populates="accounts",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
