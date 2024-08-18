# digimon/models/merchants.py

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from . import users

class BaseMerchant(SQLModel):
    name: str
    description: Optional[str] = None
    tax_id: Optional[str] = None
    user_id: Optional[int] = None

class CreatedMerchant(BaseMerchant):
    pass

class UpdatedMerchant(BaseMerchant):
    pass

class Merchant(BaseMerchant):
    id: int

class DBMerchant(BaseMerchant, table=True):
    __tablename__ = "merchants"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: Optional[users.DBUser] = Relationship()

class MerchantList(SQLModel):
    merchants: list[Merchant]
    page: int
    size_per_page: int
    page_count: int
