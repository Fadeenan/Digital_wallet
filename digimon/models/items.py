# digimon/models/items.py

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from . import merchants
from . import users

class BaseItem(SQLModel):
    name: str
    description: Optional[str] = None
    price: float = 0.12
    tax: Optional[float] = None
    merchant_id: Optional[int] = None
    user_id: Optional[int] = None

class CreatedItem(BaseItem):
    pass

class UpdatedItem(BaseItem):
    pass

class Item(BaseItem):
    id: int
    merchant_id: int
    user_id: int

class DBItem(BaseItem, table=True):
    __tablename__ = "items"
    id: Optional[int] = Field(default=None, primary_key=True)
    merchant_id: int = Field(foreign_key="merchants.id")
    user_id: int = Field(foreign_key="users.id")
    merchant: Optional[merchants.DBMerchant] = Relationship()
    user: Optional[users.DBUser] = Relationship()

class ItemList(SQLModel):
    items: list[Item]
    page: int
    size_per_page: int
    page_count: int
