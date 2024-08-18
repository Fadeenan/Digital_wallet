# digimon/routers/items.py

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import math

from .. import models, deps

router = APIRouter(prefix="/items")

SIZE_PER_PAGE = 50

@router.get("")
async def read_items(
    session: Annotated[AsyncSession, Depends(models.get_session)],
    page: int = 1,
) -> models.ItemList:
    offset = (page - 1) * SIZE_PER_PAGE
    result = await session.exec(select(models.DBItem).offset(offset).limit(SIZE_PER_PAGE))
    items = result.all()

    total_items = await session.exec(select(func.count(models.DBItem.id)))
    page_count = math.ceil(total_items / SIZE_PER_PAGE)

    return models.ItemList(items=items, page=page, size_per_page=SIZE_PER_PAGE, page_count=page_count)

@router.post("")
async def create_item(
    item: models.CreatedItem,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.Item:
    db_item = models.DBItem(**item.dict(), user_id=current_user.id)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return models.Item.from_orm(db_item)

@router.get("/{item_id}")
async def read_item(item_id: int, session: Annotated[AsyncSession, Depends(models.get_session)]) -> models.Item:
    db_item = await session.get(models.DBItem, item_id)
    if db_item:
        return models.Item.from_orm(db_item)
    raise HTTPException(status_code=404, detail="Item not found")

@router.put("/{item_id}")
async def update_item(
    item_id: int,
    item: models.UpdatedItem,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.Item:
    db_item = await session.get(models.DBItem, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.update(item.dict())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)

    return models.Item.from_orm(db_item)

@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> dict:
    db_item = await session.get(models.DBItem, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.delete(db_item)
    await session.commit()

    return {"message": "Item deleted successfully"}
