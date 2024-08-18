# digimon/models/transactions.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class BaseTransaction(SQLModel):
    wallet_id: int
    amount: float
    type: str  # 'credit' or 'debit'
    description: Optional[str] = None

class TransactionCreate(BaseTransaction):
    pass

class TransactionRead(BaseTransaction):
    id: int

class DBTransaction(BaseTransaction, table=True):
    __tablename__ = "transactions"
    id: Optional[int] = Field(default=None, primary_key=True)
    wallet_id: int = Field(foreign_key="wallets.id")
    
