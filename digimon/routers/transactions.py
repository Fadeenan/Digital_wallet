from fastapi import APIRouter, HTTPException
from sqlmodel import Field, SQLModel, create_engine, Session, select
from ..models import Transaction, CreatedTransaction, UpdatedTransaction, TransactionList, DBTransaction, engine

router = APIRouter(prefix="/transactions")

@router.post("")
async def create_transaction(transaction: CreatedTransaction) -> Transaction:
    data = transaction.dict()
    dbtransaction = DBTransaction(**data)
    with Session(engine) as session:
        session.add(dbtransaction)
        session.commit()
        session.refresh(dbtransaction)
    return Transaction.from_orm(dbtransaction)

@router.get("")
async def read_transactions() -> TransactionList:
    with Session(engine) as session:
        transactions = session.exec(select(DBTransaction)).all()
    return TransactionList.from_orm(dict(transactions=transactions, page_size=0, page=0, size_per_page=0))

@router.get("/{transaction_id}")
async def read_transaction(transaction_id: int) -> Transaction:
    with Session(engine) as session:
        db_transaction = session.get(DBTransaction, transaction_id)
        if db_transaction:
            return Transaction.from_orm(db_transaction)
    raise HTTPException(status_code=404, detail="Transaction not found")

@router.put("/{transaction_id}")
async def update_transaction(transaction_id: int, transaction: UpdatedTransaction) -> Transaction:
    data = transaction.dict()
    with Session(engine) as session:
        db_transaction = session.get(DBTransaction, transaction_id)
        db_transaction.sqlmodel_update(data)
        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)
    return Transaction.from_orm(db_transaction)

@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int) -> dict:
    with Session(engine) as session:
        db_transaction = session.get(DBTransaction, transaction_id)
        session.delete(db_transaction)
        session.commit()
    return dict(message="delete success")
