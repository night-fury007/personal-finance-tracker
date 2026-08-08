from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wealth_engine.models.transaction import Expense

class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)

    subcategories: List["SubCategory"] = Relationship(back_populates="category", sa_relationship_kwargs={"lazy": "selectin"})
    expenses: List["Expense"] = Relationship(back_populates="category", sa_relationship_kwargs={"lazy": "selectin"})


class SubCategory(SQLModel, table=True):
    __tablename__ = "subcategories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=50)
    category_id: int = Field(foreign_key="categories.id")

    category: Optional["Category"] = Relationship(back_populates="subcategories")
    expenses: List["Expense"] = Relationship(back_populates="subcategory", sa_relationship_kwargs={"lazy": "selectin"})
