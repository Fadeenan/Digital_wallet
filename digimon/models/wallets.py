from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .users import DBUser

class BaseWallet(SQLModel):
    user_id: int
    balance: float = 0.0

class WalletCreate(BaseWallet):
    pass

class WalletRead(BaseWallet):
    id: int

class WalletUpdate(SQLModel):
    balance: Optional[float] = None

class DBWallet(BaseWallet, table=True):
    __tablename__ = "wallets"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    
