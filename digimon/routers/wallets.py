# digimon/routers/wallets.py

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from .. import models, deps

router = APIRouter(prefix="/wallets")

@router.post("", response_model=models.WalletRead)
async def create_wallet(
    wallet: models.WalletCreate,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)],
):
    db_wallet = models.DBWallet(**wallet.dict(), user_id=current_user.id)
    session.add(db_wallet)
    await session.commit()
    await session.refresh(db_wallet)
    return models.WalletRead.from_orm(db_wallet)

@router.get("/{wallet_id}", response_model=models.WalletRead)
async def read_wallet(wallet_id: int, session: Annotated[AsyncSession, Depends(models.get_session)]) -> models.WalletRead:
    db_wallet = await session.get(models.DBWallet, wallet_id)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return models.WalletRead.from_orm(db_wallet)

@router.put("/{wallet_id}", response_model=models.WalletRead)
async def update_wallet(
    wallet_id: int,
    wallet_update: models.WalletUpdate,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.WalletRead:
    db_wallet = await session.get(models.DBWallet, wallet_id)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet_update.balance is not None:
        db_wallet.balance = wallet_update.balance

    session.add(db_wallet)
    await session.commit()
    await session.refresh(db_wallet)
    return models.WalletRead.from_orm(db_wallet)
