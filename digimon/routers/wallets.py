from fastapi import APIRouter, HTTPException
from sqlmodel import Field, SQLModel, create_engine, Session, select
from ..models import Wallet, CreatedWallet, UpdatedWallet, WalletList, DBWallet, engine

router = APIRouter(prefix="/wallets")

@router.post("")
async def create_wallet(wallet: CreatedWallet) -> Wallet:
    data = wallet.dict()
    dbwallet = DBWallet(**data)
    with Session(engine) as session:
        session.add(dbwallet)
        session.commit()
        session.refresh(dbwallet)
    return Wallet.from_orm(dbwallet)

@router.get("")
async def read_wallets() -> WalletList:
    with Session(engine) as session:
        wallets = session.exec(select(DBWallet)).all()
    return WalletList.from_orm(dict(wallets=wallets, page_size=0, page=0, size_per_page=0))

@router.get("/{wallet_id}")
async def read_wallet(wallet_id: int) -> Wallet:
    with Session(engine) as session:
        db_wallet = session.get(DBWallet, wallet_id)
        if db_wallet:
            return Wallet.from_orm(db_wallet)
    raise HTTPException(status_code=404, detail="Wallet not found")

@router.put("/{wallet_id}")
async def update_wallet(wallet_id: int, wallet: UpdatedWallet) -> Wallet:
    data = wallet.dict()
    with Session(engine) as session:
        db_wallet = session.get(DBWallet, wallet_id)
        db_wallet.sqlmodel_update(data)
        session.add(db_wallet)
        session.commit()
        session.refresh(db_wallet)
    return Wallet.from_orm(db_wallet)

@router.delete("/{wallet_id}")
async def delete_wallet(wallet_id: int) -> dict:
    with Session(engine) as session:
        db_wallet = session.get(DBWallet, wallet_id)
        session.delete(db_wallet)
        session.commit()
    return dict(message="delete success")
