# digimon/routers/merchants.py

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import models, deps

router = APIRouter(prefix="/merchants" , tags=["merchants"])

@router.get("")
async def read_merchants(session: Annotated[AsyncSession, Depends(models.get_session)]) -> models.MerchantList:
    result = await session.exec(select(models.DBMerchant))
    merchants = result.all()

    return models.MerchantList(merchants=merchants, page=1, size_per_page=50, page_count=1)

@router.post("")
async def create_merchant(
    merchant: models.CreatedMerchant,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.Merchant:
    db_merchant = models.DBMerchant(**merchant.model_dump(), user_id=current_user.id)
    session.add(db_merchant)
    await session.commit()
    await session.refresh(db_merchant)
    return models.Merchant.model_validate(db_merchant)

@router.get("/{merchant_id}")
async def read_merchant(merchant_id: int, session: Annotated[AsyncSession, Depends(models.get_session)]) -> models.Merchant:
    db_merchant = await session.get(models.DBMerchant, merchant_id)
    if db_merchant:
        return models.Merchant.model_validate(db_merchant)
    raise HTTPException(status_code=404, detail="Merchant not found")

@router.put("/{merchant_id}")
async def update_merchant(
    merchant_id: int,
    merchant: models.UpdatedMerchant,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.Merchant:
    db_merchant = await session.get(models.DBMerchant, merchant_id)
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    db_merchant.update(merchant.model_dump())
    session.add(db_merchant)
    await session.commit()
    await session.refresh(db_merchant)

    return models.Merchant.model_validate(db_merchant)

@router.delete("/{merchant_id}")
async def delete_merchant(
    merchant_id: int,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> dict:
    db_merchant = await session.get(models.DBMerchant, merchant_id)
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    await session.delete(db_merchant)
    await session.commit()

    return {"message": "Merchant deleted successfully"}
