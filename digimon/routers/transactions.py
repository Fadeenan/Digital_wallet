# digimon/routers/transactions.py

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from .. import models, deps

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("", response_model=models.TransactionRead)
async def create_transaction(
    transaction: models.TransactionCreate,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)],
):
    db_wallet = await session.get(models.DBWallet, transaction.wallet_id)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if transaction.type == 'debit':
        if db_wallet.balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        db_wallet.balance -= transaction.amount
    else:
        db_wallet.balance += transaction.amount

    db_transaction = models.DBTransaction(**transaction.model_dump())
    session.add(db_transaction)
    session.add(db_wallet)
    await session.commit()
    await session.refresh(db_transaction)
    return models.TransactionRead.model_validate(db_transaction)

@router.get("/{transaction_id}", response_model=models.TransactionRead)
async def read_transaction(transaction_id: int, session: Annotated[AsyncSession, Depends(models.get_session)]) -> models.TransactionRead:
    db_transaction = await session.get(models.DBTransaction, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return models.TransactionRead.model_validate(db_transaction)
